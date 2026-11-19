"""Confere as notas das palavras-chave e as definições do vocabulário com fontes abertas e grava
ferramentas/notas_fontes.json, que o gerar_palavras.py aplica por cima do texto escrito à mão.

As notas e definições foram redigidas por IA e o mantenedor não as pode revisar uma a uma. Em vez disso, cada item vai
ao modelo junto com as FONTES que tratam dele, e o modelo só pode manter (ou reescrever) o que elas sustentam:
- léxico grego: Abbott-Smith (via STEPBible, CC BY) — definições completas;
- léxico hebraico: glosa da STEPBible (CC BY) e o léxico de Strong (domínio público). As definições do BDB resumido
  do arquivo da STEPBible NÃO são usadas: o próprio arquivo pede licença do Online Bible para usá-las;
- Confissão de Fé e Catecismo Maior de Westminster: os parágrafos cujos textos de prova contêm a palavra original;
- comentário de Calvino (ou Matthew Henry) ao versículo, nas notas de contexto;
- o texto da Bíblia Livre dos versículos que a nota cita.
Cada item volta com a lista das fontes usadas, que o cartão do site mostra.

Chave: ANTHROPIC_API_KEY (ambiente ou .env). Uso:
  python ferramentas/tradutor/notas_llm.py preparar                # baixa os léxicos, conta itens e custo
  python ferramentas/tradutor/notas_llm.py amostra [--modelo M]    # 24 itens, relatório para ler
  python ferramentas/tradutor/notas_llm.py conferir [--modelo M]   # todos (retoma de onde parou)
  python ferramentas/tradutor/notas_llm.py aplicar                 # grava ferramentas/notas_fontes.json
Depois: python3 ferramentas/gerar_palavras.py e python3 ferramentas/gerar_paginas.py
"""
import argparse, collections, html, json, random, re, sys, urllib.parse, urllib.request
from pathlib import Path

PASTA = Path(__file__).resolve().parent
FERR = PASTA.parent
RAIZ = FERR.parent
DATA = RAIZ / "data"
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(FERR))
from calvino_llm import gravar_atomico, http_json, ler_json, obter_chave, pos_processar   # noqa: E402

TRAB = PASTA / "trabalho"
SAIDA = TRAB / "notas_llm_saida.json"
FINAL = FERR / "notas_fontes.json"
FONTES_DIR = FERR / "fontes"
LEXICOS = {"G": "TBESG - Translators Brief lexicon of Extended Strongs for Greek - STEPBible.org CC BY.txt",
           "H": "TBESH - Translators Brief lexicon of Extended Strongs for Hebrew - STEPBible.org CC BY.txt"}
URL = "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Lexicons/"
MODELO_PADRAO = "claude-sonnet-5-5"
PRECOS = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0)}
GRUPO = 6

PROMPT = """Você confere notas de estudo bíblico de um site reformado gratuito. As notas foram escritas por IA e
precisam ficar ancoradas em fontes. Para cada item você recebe o texto atual e uma lista de FONTES numeradas (léxicos,
Confissão de Westminster, comentário de Calvino ou Henry, versículos da Bíblia).

Regras:
- Mantenha só o que as fontes dadas sustentam. Afirmação sem apoio nas fontes: tire ou reescreva para o que as fontes
  dizem. Não acrescente nada que não esteja nelas (nem datas, nem nomes, nem curiosidades, nem citações).
- Se o texto atual já está correto e sustentado, devolva-o igual (mudanca "nenhuma").
- Definição de vocabulário ("significado"): uma frase curta e simples em português do Brasil, para leigos.
  Palavra comum do português sem fonte específica (ex.: "botija"): mantenha se for o sentido usual do dicionário.
- Notas: curtas (até ~300 caracteres), claras, sem jargão desnecessário, em português do Brasil.
- Fiel à teologia das fontes reformadas dadas; não tome partido em pontos que elas não tratam.
- "fontes": os números das fontes que sustentam o texto final (só os dados). Use [] se nenhuma foi necessária.
- Responda SOMENTE com JSON: {"ID": {"significado"?: "...", "nota": "... ou vazio", "fontes": [1, 3],
  "mudanca": "nenhuma|ajuste|reescrita|removida"}}. Itens de vocabulário têm "significado" e "nota"; palavras-chave
  e notas de contexto têm só "nota"."""


# ---------------- fontes ----------------
def baixar_lexicos():
    FONTES_DIR.mkdir(exist_ok=True)
    for nome in LEXICOS.values():
        destino = FONTES_DIR / nome
        if not destino.exists():
            print(f"baixando {nome[:5]}…")
            urllib.request.urlretrieve(URL + urllib.parse.quote(nome), destino)


def limpar(t):
    t = re.sub(r"<ref='[^']*'>([^<]*)</ref>", r"\1", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def lexico_aberto():
    """{"G26": [(glosa, definição)], "H2617": [(glosa, "")]} — no hebraico, só a glosa (veja o cabeçalho)"""
    baixar_lexicos()
    lex = collections.defaultdict(list)
    for letra, nome in LEXICOS.items():
        for linha in (FONTES_DIR / nome).read_text(encoding="utf-8").split("\n"):
            m = re.match(rf"^{letra}(\d{{4}})([a-zA-Z]?)\t", linha)
            if not m:
                continue
            c = linha.split("\t")
            if len(c) < 8:
                continue
            definicao = limpar(c[7])[:1100] if letra == "G" else ""
            lex[f"{letra}{int(m.group(1))}"].append((c[6].strip(), definicao))
    return lex


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


class Fontes:
    def __init__(self):
        self.lex = lexico_aberto()
        self.strong = {"G": ler(DATA / "strongs" / "G.json"), "H": ler(DATA / "strongs" / "H.json")}
        self.livros = ler(DATA / "books.json")["books"]
        self.info = {b["id"]: b for b in self.livros}
        self.por_nome = {}
        for b in self.livros:
            self.por_nome[b["pt"].lower()] = b["id"]
        self.bl = {b["id"]: ler(DATA / "bibles" / "blivre" / f"{b['id']}.json") for b in self.livros}
        # onde cada Strong aparece (versículos)
        self.versos = collections.defaultdict(set)
        for arq in (DATA / "interlinear").glob("*/*.json"):
            l, c = arq.parent.name, int(arq.stem)
            for v, ps in enumerate(ler(arq), 1):
                for p in ps:
                    if p[2]:
                        self.versos[p[2]].add((l, c, v))
        # parágrafos da Confissão e perguntas do Catecismo Maior, com os versículos das provas
        self.paragrafos = []
        wcf = ler(DATA / "confissoes" / "westminster.json")
        for parte in wcf["partes"]:
            for it in parte["itens"]:
                self.paragrafos.append((f"CFW {parte['n']}.{it['n']}", it["pt"], self._versos_provas(it["provas"])))
        cm = ler(DATA / "confissoes" / "catecismo-maior.json")
        for q in cm["itens"]:
            self.paragrafos.append((f"Catecismo Maior {q['n']}", f"{q['p']} {q['r']}", self._versos_provas(q["provas"])))
        self.comentarios = {}

    @staticmethod
    def _versos_provas(provas):
        vs = set()
        for refs in provas.values():
            for r in refs:
                l, c, a, b = r[:4]
                if a:
                    vs.update((l, c, v) for v in range(a, (b if len(r) == 4 else a) + 1))
        return vs

    def lexico(self, s):
        letra = s[0]
        st = self.strong[letra].get(s, {})
        entradas = self.lex.get(s, [])
        if letra == "G":
            corpo = " | ".join(f"{g}: {d}" for g, d in entradas)[:1400] or st.get("def", "")
            return f"Léxico grego Abbott-Smith (STEPBible, CC BY) — {s} {st.get('lemma', '')}", corpo
        glosas = ", ".join(dict.fromkeys(g for g, _ in entradas))
        return (f"Léxico de Strong; glosa STEPBible (CC BY) — {s} {st.get('lemma', '')}",
                f"glosa: {glosas}. Strong: {st.get('def', '')} (KJV: {st.get('kjv', '')})")

    def confissao(self, strong, n=3):
        vs = self.versos.get(strong, set())
        if not vs:
            return []
        pont = sorted(((len(vs & pv), rot, txt) for rot, txt, pv in self.paragrafos if vs & pv), reverse=True)[:n]
        return [(rot, re.sub(r"\s?\[\d+\]", "", txt)) for _, rot, txt in pont]

    def comentario(self, l, c, v):
        for pasta, autor in (("calvin", "Calvino"), ("henry", "Matthew Henry")):
            arq = DATA / "commentaries" / pasta / "pt" / l / f"{c}.json"
            if arq.exists():
                com = ler(arq)
                ks = sorted(int(k) for k in com if k.isdigit())
                alvo = v if v in ks else max([k for k in ks if k < v], default=ks[0] if ks else None)
                if alvo:
                    txt = re.sub(r"^\s*\d+(?:\s*[-,]\s*\d+)*\s*[\.:]?\s*", "", com[str(alvo)])
                    return f"{autor} sobre {self.info[l]['pt']} {c}:{alvo}", txt[:2200]
        return None

    def versiculos_citados(self, texto):
        saida = []
        nomes = sorted(self.por_nome, key=len, reverse=True)
        padrao = r"((?:[1-3] )?(?:" + "|".join(re.escape(n) for n in nomes) + r")) (\d+):(\d+)(?:-(\d+))?"
        for m in re.finditer(padrao, texto, re.I):
            l = self.por_nome.get(m.group(1).lower())
            c, a, b = int(m.group(2)), int(m.group(3)), int(m.group(4) or m.group(3))
            try:
                txt = " ".join(self.bl[l][c - 1][a - 1:b])
            except (IndexError, KeyError):
                continue
            if txt:
                saida.append((f"{m.group(1)} {c}:{a}" + (f"-{b}" if b != a else ""), txt[:600]))
        return saida[:4]


# ---------------- itens ----------------
def itens(fontes):
    sys.path.insert(0, str(FERR))
    import gerar_palavras as gp
    from vocabulario import TERMOS
    saida = []
    for s, l in gp.LEMAS.items():
        if not l["nota"]:
            continue
        fs = [fontes.lexico(s)] + fontes.confissao(s) + fontes.versiculos_citados(l["nota"])
        saida.append({"id": f"lema|{s}", "tipo": "palavra-chave", "palavra": f"{l['pt']} ({s})", "nota": l["nota"], "fontes": fs})
    for (ref, s, n), c in gp.CONTEXTOS.items():
        l_, cap, v = ref.split(".")
        fs = [fontes.lexico(s)]
        com = fontes.comentario(l_, int(cap), int(v))
        if com:
            fs.append(com)
        fs += fontes.confissao(s, 2) + [(f"{fontes.info[l_]['pt']} {cap}:{v} (o versículo)", fontes.bl[l_][int(cap) - 1][int(v) - 1])]
        fs += fontes.versiculos_citados(c["nota"])
        saida.append({"id": f"contexto|{ref}|{s}|{n}", "tipo": "nota do versículo", "palavra": f"{gp.LEMAS[s]['pt']} ({s}) em {ref}",
                      "nota": c["nota"], "fontes": fs})
    for tm in TERMOS:
        fs = [fontes.lexico(s) for s in tm["s"][:3] if s[0] in "GH" and s in fontes.strong[s[0]]]
        fs += fontes.versiculos_citados((tm["nota"] or "") + " " + tm["significado"])
        saida.append({"id": f"termo|{tm['palavra']}", "tipo": "vocabulário", "palavra": tm["palavra"],
                      "significado": tm["significado"], "nota": tm["nota"] or "", "fontes": fs})
    return saida


def mensagem(grupo):
    blocos = []
    for it in grupo:
        linhas = [f"### {it['id']} — {it['tipo']}: {it['palavra']}"]
        if "significado" in it:
            linhas.append(f"significado atual: {it['significado']}")
        linhas.append(f"nota atual: {it['nota'] or '(sem nota)'}")
        linhas += [f"FONTE {i}. {rot}: {txt}" for i, (rot, txt) in enumerate(it["fontes"], 1)]
        blocos.append("\n".join(linhas))
    return "\n\n".join(blocos)


# ---------------- chamada e validação ----------------
def pedir(modelo, chave, grupo):
    corpo = {"model": modelo, "max_tokens": 8000,
             "system": [{"type": "text", "text": PROMPT, "cache_control": {"type": "ephemeral"}}],
             "messages": [{"role": "user", "content": mensagem(grupo)}]}
    if "haiku-5" in modelo:
        corpo["thinking"] = {"type": "disabled"}
    else:
        corpo["output_config"] = {"effort": "low"}
    resp = http_json("https://api.anthropic.com/v1/messages", metodo="POST",
                     cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"}, corpo=corpo)
    txt = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt.strip())
    try:
        obj = json.loads(t[t.find("{"):t.rfind("}") + 1])
    except (json.JSONDecodeError, ValueError):
        obj = {}
    if not obj:                                          # para investigar: o texto que não deu para ler
        with open(TRAB / "notas_llm_erros.txt", "a", encoding="utf-8") as f:
            f.write(f"--- {resp.get('stop_reason')}\n{txt}\n")
    return obj, resp.get("usage", {})


INGLES = re.compile(r"\b(?:the|of|and|which|that|with|from|this|is|are)\b")


def avaliar(it, r):
    if not isinstance(r, dict):
        return "sem resposta"
    nota = pos_processar(r.get("nota") or "")
    if "significado" in it and not (r.get("significado") or "").strip():
        return "sem significado"
    fs = r.get("fontes") or []
    if not isinstance(fs, list) or any(not isinstance(i, int) or not 1 <= i <= len(it["fontes"]) for i in fs):
        return "fontes inválidas"
    if r.get("mudanca") in ("ajuste", "reescrita") and not fs:
        return "mudou sem fonte"
    if len(nota) > 480 or len(r.get("significado") or "") > 220:
        return "longo demais"
    if INGLES.search(nota + " " + (r.get("significado") or "")):
        return "inglês"
    return ""


def chave_normal(k):
    return re.sub(r"\|\d+$", "", re.sub(r"^(?:contexto|lema|termo)\|", "", str(k).strip()))


def conferir(lista, modelo, chave, est, arq):
    uso = collections.Counter()
    pend = [it for it in lista if it["id"] not in est["ok"]]
    for i in range(0, len(pend), GRUPO):
        g = pend[i:i + GRUPO]
        obj, u = pedir(modelo, chave, g)
        uso.update({k: v for k, v in u.items() if isinstance(v, int)})
        normal = {chave_normal(k): v for k, v in obj.items()}
        for it in g:                       # o modelo às vezes tira o prefixo ("contexto|") ou o "|1" do fim da chave
            r = obj.get(it["id"]) or normal.get(chave_normal(it["id"]))
            motivo = avaliar(it, r)
            if motivo:
                est["recusas"][it["id"]] = {"motivo": motivo, "r": r}
            else:
                est["ok"][it["id"]] = {"nota": pos_processar(r.get("nota") or ""), "significado": pos_processar(r.get("significado") or ""),
                                       "fontes": [it["fontes"][k - 1][0] for k in r.get("fontes") or []],
                                       "mudanca": r.get("mudanca", "")}
                est["recusas"].pop(it["id"], None)
        print(f"  {len(est['ok'])} prontos, {len(est['recusas'])} recusados", flush=True)
        gravar_atomico(arq, est, indent=None)
    pe, ps = PRECOS.get(modelo, (0, 0))
    ent = uso["input_tokens"] + uso["cache_read_input_tokens"] + uso["cache_creation_input_tokens"]
    return (ent * pe + uso["output_tokens"] * ps) / 1e6


def relatorio(lista, est, caminho):
    linhas = []
    for it in lista:
        r = est["ok"].get(it["id"])
        if not r:
            continue
        antes = (f"significado: {it['significado']}\n" if "significado" in it else "") + f"nota: {it['nota'] or '-'}"
        depois = (f"significado: {r['significado']}\n" if "significado" in it else "") + f"nota: {r['nota'] or '-'}"
        linhas.append(f"## {it['id']}  [{r['mudanca']}]\nANTES:\n{antes}\nDEPOIS:\n{depois}\nFONTES: {'; '.join(r['fontes']) or '-'}\n")
    caminho.write_text("\n".join(linhas), encoding="utf-8")


def cmd_preparar(a):
    lista = itens(Fontes())
    chars = sum(len(mensagem([it])) for it in lista)
    print(f"[preparar] {len(lista)} itens ({collections.Counter(it['tipo'] for it in lista)}), {chars:,} caracteres")
    for m, (pe, ps) in PRECOS.items():
        ent, sai = chars / 3.4, len(lista) * 110
        print(f"  {m}: ~US$ {(ent * pe + sai * ps) / 1e6:.2f}")


def cmd_amostra(a):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    lista = itens(Fontes())
    rnd = random.Random(3)
    por_tipo = collections.defaultdict(list)
    for it in lista:
        por_tipo[it["tipo"]].append(it)
    amostra = [x for t, v in sorted(por_tipo.items()) for x in rnd.sample(v, min(8, len(v)))]
    est = {"ok": {}, "recusas": {}}
    gasto = conferir(amostra, modelo, chave, est, TRAB / "notas_llm_amostra.json")
    relatorio(amostra, est, TRAB / "relatorio_notas.txt")
    print(f"[amostra] {len(est['ok'])} ok, {len(est['recusas'])} recusados; gasto US$ {gasto:.3f}; "
          f"tudo ~US$ {gasto * len(lista) / len(amostra):.2f}; mudanças: {collections.Counter(r['mudanca'] for r in est['ok'].values())}")
    print(f"[amostra] relatório: {TRAB / 'relatorio_notas.txt'}")


def cmd_conferir(a):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    lista = itens(Fontes())
    est = ler_json(SAIDA, {"ok": {}, "recusas": {}})
    gasto = conferir(lista, modelo, chave, est, SAIDA)
    for it in [x for x in lista if x["id"] in est["recusas"]]:      # segunda tentativa, um por vez
        gasto += conferir([it], modelo, chave, est, SAIDA)
    relatorio(lista, est, TRAB / "relatorio_notas.txt")
    print(f"[conferir] {len(est['ok'])} ok, {len(est['recusas'])} recusados; gasto US$ {gasto:.2f}; "
          f"mudanças: {collections.Counter(r['mudanca'] for r in est['ok'].values())}")


def cmd_aplicar(a):
    est = ler_json(SAIDA, {"ok": {}})
    saida = {"lemas": {}, "contextos": {}, "termos": {}}
    for id_, r in sorted(est["ok"].items()):
        tipo, resto = id_.split("|", 1)
        if tipo == "lema":
            saida["lemas"][resto] = {"nota": r["nota"], "f": r["fontes"]}
        elif tipo == "contexto":
            saida["contextos"][resto] = {"nota": r["nota"] or "", "f": r["fontes"]}
        else:
            saida["termos"][resto] = {"s": r["significado"], "n": r["nota"], "f": r["fontes"]}
    FINAL.write_text(json.dumps(saida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[aplicar] {sum(len(v) for v in saida.values())} itens em {FINAL.relative_to(RAIZ)}")


def main():
    ap = argparse.ArgumentParser(description="Notas e vocabulário conferidos com fontes abertas")
    ap.add_argument("acao", choices=["preparar", "amostra", "conferir", "aplicar"])
    ap.add_argument("--modelo", default=None)
    ap.add_argument("--chave", default=None)
    a = ap.parse_args()
    {"preparar": cmd_preparar, "amostra": cmd_amostra, "conferir": cmd_conferir, "aplicar": cmd_aplicar}[a.acao](a)


if __name__ == "__main__":
    main()
