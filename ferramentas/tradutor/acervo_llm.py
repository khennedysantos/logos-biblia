"""Nova tradução de Matthew Henry, Easton (dicionário) e Nave (temas) via LLM, pela Batch API da Anthropic.

Mesmo esquema do calvino_llm.py e do strong_llm.py (e as funções HTTP do calvino_llm.py, só biblioteca padrão), mas
genérico: a entrada é a de `etapas.py preparar <etapa>` (trabalho/<etapa>.json, itens {id, texto}) e a saída é a que
`etapas.py aplicar <etapa>` já sabe gravar (trabalho/<etapa>_pt.json, {id: tradução}). Assim as regras de cada etapa
continuam valendo: referências do Easton em formato USFM ("GEN 3:15", que o app transforma em link), número do
versículo do Henry fora da tradução, frases fixas do Nave (FRASES_NAVE).

- Textos curtos vão em grupos (um objeto JSON por pedido); textos longos vão sozinhos, como texto puro; os muito
  longos (Henry) são fatiados em parágrafos e remontados.
- Cada tradução é conferida: números de capítulo:versículo e referências USFM preservados, grego e hebraico
  intactos, nada de inglês sobrando, tamanho compatível com o original. A recusada pode ser refeita com outro modelo
  (`reenviar --modelo claude-sonnet-5-5`); se continuar recusada, fica a tradução atual (NLLB/Argos).

Chave: ANTHROPIC_API_KEY no ambiente ou em ferramentas/tradutor/.env.

Uso (etapa = henry, dicionario ou temas):
  python ferramentas/tradutor/acervo_llm.py amostra <etapa> [--modelo M] [--n N]    # síncrono, relatório HTML
  python ferramentas/tradutor/acervo_llm.py preparar <etapa>                        # também mostra o custo
  python ferramentas/tradutor/acervo_llm.py enviar <etapa> [--modelo M]
  python ferramentas/tradutor/acervo_llm.py status <etapa>
  python ferramentas/tradutor/acervo_llm.py baixar <etapa>
  python ferramentas/tradutor/acervo_llm.py reenviar <etapa> --modelo claude-sonnet-5-5
  python ferramentas/tradutor/acervo_llm.py aplicar <etapa>        # grava trabalho/<etapa>_pt.json e chama etapas.py aplicar
"""
import argparse
import html
import json
import random
import re
import sys
import time
from collections import Counter
from pathlib import Path

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA))
import etapas                                                                                   # noqa: E402
from calvino_llm import (fatiar_com_sep, gravar_atomico, http_json, http_texto, ler_json,      # noqa: E402
                         obter_chave, pos_processar)

TRAB = PASTA / "trabalho"
DATA = PASTA.parent.parent / "data"
MODELO_PADRAO = "claude-haiku-5-5"
PRECOS = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0)}

COMUM = """
Regras gerais:
- Fidelidade integral: não resuma, não omita nenhuma frase, item de lista ou referência, não acrescente comentários.
- Português brasileiro culto e natural. Vocabulário reformado clássico: "the godly" = os piedosos, "the wicked" = os
  ímpios, "covenant" = aliança, "atonement" = expiação, "propitiation" = propiciação, "righteousness" = justiça,
  "sanctification" = santificação, "the elect" = os eleitos, "grace" = graça.
- Inglês arcaico (thee, thou, hath, doth, unto) vira português correto, com "tu"/"vós" quando for tratamento bíblico.
- Nomes bíblicos na forma tradicional das Bíblias em português (Almeida/Bíblia Livre): Moisés, Josué, Ezequias,
  Jeroboão, Nabucodonosor, Belém, Hebrom, filisteus, cananeus.
- Copie exatamente, sem traduzir nem transliterar, palavras em grego e hebraico e os números de capítulo e versículo.
- Texto puro, sem Markdown (nada de ** ou #), com aspas curvas (“ ”).
- Formato da resposta: se a mensagem for um objeto JSON {"chave": "texto", ...}, responda só com um objeto JSON com as
  mesmas chaves e cada texto traduzido. Se for texto comum, responda só com a tradução, sem preâmbulo nem notas."""

PROMPTS = {
    "henry": """Você traduz para o português o Comentário Bíblico de Matthew Henry (1706–1721), puritano e reformado,
para um site gratuito de estudo bíblico. Preserve o tom pastoral e a estrutura do autor: os marcadores de tópico
("I.", "II.", "1.", "(1.)", "[1.]") ficam exatamente onde estão. As citações bíblicas são traduzidas das próprias
palavras de Henry: NUNCA as substitua por uma Bíblia pronta (ARA, NAA, NVI, NVT, NTLH — têm direitos autorais).
As referências já vêm com o livro abreviado em português ("1Sm 3:4", "Rm 8:28", "Jó 21:33"): copie-as exatamente.
Se aparecer alguma ainda em inglês, use a mesma forma abreviada ("Gen. 3" -> "Gn 3", "ch. 2:4" -> "cap. 2:4",
"v. 12" -> "v. 12"). Expressões em latim ficam em latim.""" + COMUM,
    "dicionario": """Você traduz para o português o Dicionário Bíblico de Easton (1897) para um site gratuito de estudo
bíblico, no estilo de verbete de dicionário. As referências bíblicas já estão no formato de código ("GEN 3:15",
"1SA 13:20; PSA 45:2", "ISA 53"): copie cada uma exatamente como está, com o código em maiúsculas — o site as
transforma em links. Mantenha "R.V." (Revised Version) e "A.V." (Authorized Version) como estão. Medidas: "cubit" =
côvado, "shekel" = siclo, "ephah" = efa, "talent" = talento; mantenha os números e as unidades como estão — milhas
continuam milhas, nunca converta para quilômetros. Remissões "See X" / "(See X.)" viram "Veja X" / "(Veja X.)".
O verbete começa muitas vezes pelo significado do nome ("Whose God is Jehovah", "The people is victor"): traduza
literalmente esse significado.""" + COMUM,
    "temas": """Você traduz para o português os subtítulos do índice temático de Nave (Nave's Topical Bible) para um
site gratuito de estudo bíblico. Cada texto é o começo de uma linha que será seguida por uma lista de referências
bíblicas, por isso costuma ser um fragmento ("Lineage of", "Meets Moses in the wilderness", "Instances of"):
traduza mantendo o mesmo caráter de fragmento e a mesma concisão ("Linhagem de", "Encontra Moisés no deserto",
"Exemplos de"), sem completar a frase, sem ponto final que o original não tenha. Remissões "See X" viram "Veja X".
Títulos de verbete em MAIÚSCULAS que aparecem dentro do texto (remissões "See IRON", "Also called JEHOASH") ficam
em maiúsculas, na forma portuguesa do nome ("Veja FERRO", "Também chamado JEOÁS"); fora isso, mantenha as
maiúsculas do original.
A mensagem é um objeto JSON agrupado por verbete: {"Josué": {"0": "Conquers Hazor", "1": "Death of"}, "Ana": {...}}.
O verbete (a chave de fora) serve SÓ para entender o sentido: NÃO o traduza nem o repita; traduza apenas cada texto
("Conquista Hazor", nunca "Josué conquista Hazor" nem "Josué: conquista Hazor").
Responda com um objeto JSON simples, sem os verbetes: {"0": "Conquista Hazor", "1": "Morte de", ...}, com todos os
números recebidos.""" + COMUM,
}
# códigos de livro da fonte do Henry (estilo e-Sword: "Sa1 3:4", "Kg2 5:1") -> abreviações em português, trocados
# antes da tradução para que o modelo só precise copiá-los
HENRY_LIVROS = dict(zip(
    "Gen Exo Lev Num Deu Jos Jdg Rut Sa1 Sa2 Kg1 Kg2 Ch1 Ch2 Ezr Neh Est Job Psa Pro Ecc Sol Isa Jer Lam Eze Dan Hos "
    "Joe Amo Oba Jon Mic Nah Hab Zep Hag Zac Mal Mat Mar Luk Joh Act Rom Co1 Co2 Gal Eph Phi Col Th1 Th2 Ti1 Ti2 Tit "
    "Plm Heb Jam Pe1 Pe2 Jo1 Jo2 Jo3 Jde Rev".split(),
    "Gn Êx Lv Nm Dt Js Jz Rt 1Sm 2Sm 1Rs 2Rs 1Cr 2Cr Ed Ne Et Jó Sl Pv Ec Ct Is Jr Lm Ez Dn Os "
    "Jl Am Ob Jn Mq Na Hc Sf Ag Zc Ml Mt Mc Lc Jo At Rm 1Co 2Co Gl Ef Fp Cl 1Ts 2Ts 1Tm 2Tm Tt "
    "Fm Hb Tg 1Pe 2Pe 1Jo 2Jo 3Jo Jd Ap".split()))
RE_HENRY_REF = re.compile(r"\b(" + "|".join(HENRY_LIVROS) + r")\.? (?=\d+:\d)")


def texto_fonte(etapa, texto):
    if etapa == "henry":
        return RE_HENRY_REF.sub(lambda m: HENRY_LIVROS[m.group(1)] + " ", texto)
    return texto


CODIGOS = set(etapas.EASTON.values())
GRUPO_MAX = {"henry": 6000, "dicionario": 4000, "temas": 3500}
FATIA = 9000


# ---------------- arquivos ----------------
def arq(etapa, nome):
    return TRAB / f"{etapa}_llm_{nome}.json"


def itens_da_etapa(etapa):
    entrada = TRAB / f"{etapa}.json"
    if not entrada.exists():
        sys.exit(f"Rode antes: python ferramentas/tradutor/acervo_llm.py preparar {etapa}")
    return json.loads(entrada.read_text(encoding="utf-8"))


def unidades(etapa, itens):
    """(uid, texto): os textos longos viram partes "id#0", "id#1"... para nunca serem cortados nem resumidos"""
    saida = []
    for it in itens:
        texto = texto_fonte(etapa, it["texto"])
        partes = fatiar_com_sep(texto, FATIA)
        if len(partes) == 1:
            saida.append((it["id"], texto))
        else:
            saida += [(f"{it['id']}#{k}", p) for k, (p, _) in enumerate(partes)]
    return saida


def grupos(etapa, unids):
    """lista de pedidos: [(cid, [(uid, texto), ...])]; um texto longo vai sozinho"""
    lim, saida, atual, tam = GRUPO_MAX[etapa], [], [], 0
    for u in unids:
        if len(u[1]) > lim:
            saida.append([u])
            continue
        if atual and tam + len(u[1]) > lim:
            saida.append(atual)
            atual, tam = [], 0
        atual.append(u)
        tam += len(u[1])
    if atual:
        saida.append(atual)
    return [(f"{etapa[:3]}{i:05d}", g) for i, g in enumerate(saida)]


# ---------------- pedidos ----------------
_TITULOS = {}


def assunto(uid):
    """Nave: o subtítulo sozinho ("Are multiplied") é ambíguo; vai junto o assunto em português"""
    if not _TITULOS:
        _TITULOS.update(ler_json(DATA / "topics" / "titulos_pt.json"))
    a = uid.split("|")[1]
    return _TITULOS.get(a) or a.title()


def mensagem(grupo, etapa=None):
    if etapa == "temas":
        por_assunto = {}
        for i, (u, t) in enumerate(grupo):
            por_assunto.setdefault(assunto(u), {})[str(i)] = t
        return json.dumps(por_assunto, ensure_ascii=False, indent=0)
    if len(grupo) == 1:
        return grupo[0][1]
    return json.dumps({str(i): t for i, (_, t) in enumerate(grupo)}, ensure_ascii=False, indent=0)


def payload(etapa, modelo, grupo):
    msg = mensagem(grupo, etapa)
    corpo = {"model": modelo, "max_tokens": max(8192, min(64000, int(len(msg) * 0.75) + 4096)),
             "system": [{"type": "text", "text": PROMPTS[etapa], "cache_control": {"type": "ephemeral"}}],
             "messages": [{"role": "user", "content": msg}]}
    if "haiku-5" in modelo:
        corpo["thinking"] = {"type": "disabled"}
    else:
        corpo["output_config"] = {"effort": "low"}
    return corpo


def ler_resposta(grupo, txt, etapa=None):
    """{uid: tradução} a partir do texto devolvido"""
    if etapa == "temas":
        t = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt.strip())
        try:
            obj = json.loads(t[t.find("{"):t.rfind("}") + 1])
        except (json.JSONDecodeError, ValueError):
            return {}
        plano = {}
        for k, v in obj.items():                     # aceita também a resposta ainda agrupada por verbete
            plano.update({kk: vv for kk, vv in v.items()} if isinstance(v, dict) else {k: v})
        res = {u: pos_processar(plano[str(i)]) for i, (u, _) in enumerate(grupo)
               if isinstance(plano.get(str(i)), str) and plano[str(i)].strip()}
        saida = {}
        for (u, en), t in ((x, res[x[0]]) for x in grupo if x[0] in res):
            a = assunto(u)
            if t.lower().startswith(a.lower() + ":") and not en.lower().startswith(a.lower()):
                t = t[len(a) + 1:].strip()                               # "Josué: conquista Hazor"
                t = t[:1].upper() + t[1:]
            saida[u] = t
        return saida
    if etapa == "dicionario":
        res = ler_resposta(grupo, txt)
        return {u: repoe_codigos(en, res[u]) for u, en in grupo if u in res}
    if len(grupo) == 1:
        return {grupo[0][0]: re.sub(r"\n{2,}", "\n", pos_processar(txt))} if txt.strip() else {}
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt.strip())
    ini, fim = t.find("{"), t.rfind("}")
    try:
        obj = json.loads(t[ini:fim + 1]) if ini >= 0 else {}
    except json.JSONDecodeError:
        return {}
    return {uid: re.sub(r"\n{2,}", "\n", pos_processar(obj[str(i)])) for i, (uid, _) in enumerate(grupo)
            if isinstance(obj.get(str(i)), str) and obj[str(i)].strip()}


# ---------------- referências do Easton ----------------
RE_REF_PT = re.compile(r"\b([1-3]?[A-ZÀ-Ú]{1,3}) (\d+(?::\d+)?)")


def repoe_codigos(en, pt):
    """O modelo às vezes "traduz" o código USFM ("1KI 17:1" -> "1RS 17:1", "ACT 13:5" -> "AT 13:5"). Se as
    referências do português batem uma a uma em número com as do inglês, os códigos do inglês voltam no lugar."""
    ref_en = [(m.group(1), m.group(2)) for m in re.finditer(r"\b([1-3]?[A-Z]{2,3}) (\d+(?::\d+)?)", en)
              if m.group(1) in CODIGOS]
    ref_pt = list(RE_REF_PT.finditer(pt))
    if not ref_en or len(ref_en) != len(ref_pt) or any(a[1] != b.group(2) for a, b in zip(ref_en, ref_pt)):
        return pt
    saida, i = [], 0
    for (cod, _), m in zip(ref_en, ref_pt):
        saida += [pt[i:m.start(1)], cod]
        i = m.end(1)
    return "".join(saida) + pt[i:]


# ---------------- validação ----------------
RE_CV = re.compile(r"\d+:\d+")
RE_USFM = re.compile(r"\b[1-3]?[A-Z]{2,3} \d+(?::\d+)?")
RE_ORIG = re.compile(r"[Ͱ-Ͽἀ-῿֐-׿]{2,}")
INGLES = re.compile(r"\b(?:the|of|and|which|that|with|from|this|shall|unto|thee|thou|his|they|their|was|were|"
                    r"have|been|would|should)\b")


def problemas(etapa, en, pt, uid=""):
    if not pt.strip():
        return ["vazia"]
    p = []
    if etapa == "temas" and uid:
        a = assunto(uid).lower()
        if (pt.lower().startswith(a) or pt.lower().rstrip(".") == a) and a.split()[0] not in en.lower():
            p.append("repetiu o verbete")
    falta = Counter(RE_CV.findall(en)) - Counter(RE_CV.findall(pt))
    if falta:
        p.append("referência perdida: " + " ".join(sorted(falta)[:5]))
    if etapa != "henry":
        falta = Counter(RE_USFM.findall(en)) - Counter(RE_USFM.findall(pt))
        if falta:
            p.append("código de livro alterado: " + " ".join(sorted(falta)[:5]))
    orig = [w for w in set(RE_ORIG.findall(en)) if w not in pt]
    if orig:
        p.append("grego/hebraico alterado: " + " ".join(orig[:4]))
    sem_aspas = re.sub(r"[“\"][^”\"]*[”\"]", " ", pt)
    ingl = INGLES.findall(sem_aspas)
    if len(ingl) >= max(3, len(pt) // 400):
        p.append("inglês na tradução: " + ", ".join(ingl[:5]))
    r = len(pt) / max(1, len(en))
    if len(en) > 300 and not 0.8 <= r <= 1.7 or 60 < len(en) <= 300 and not 0.5 <= r <= 2.5:
        p.append(f"tamanho suspeito ({len(pt)} x {len(en)})")
    return p


# ---------------- tradução atual (para o que for recusado) ----------------
def atual(etapa, id_):
    if etapa == "henry":
        livro, cap, v = id_.split("|")
        d = ler_json(DATA / "commentaries" / "henry" / "pt" / livro / f"{cap}.json")
        return etapas.NUM_VERSO.sub("", d.get(v, ""), count=1)
    letra, chave, i = id_.split("|")
    if etapa == "dicionario":
        d = ler_json(DATA / "dictionary" / "pt" / f"{letra}.json")
        lista = d.get(chave, [])
        return lista[int(i)] if int(i) < len(lista) else ""
    d = ler_json(DATA / "topics" / "pt" / f"{letra}.json")
    lista = d.get(chave, [])
    return etapas.separa(lista[int(i)])[0] if int(i) < len(lista) else ""


# ---------------- comandos ----------------
def custo(etapa, modelo, unids, lote=True):
    ent = sum(len(t) for _, t in unids) / 3.6 + len(grupos(etapa, unids)) * len(PROMPTS[etapa]) / 3.6
    sai = sum(len(t) for _, t in unids) * 1.15 / 3.4
    pe, ps = PRECOS.get(modelo, (0, 0))
    f = 0.5 if lote else 1
    return ent, sai, (ent * pe + sai * ps) / 1e6 * f


def cmd_preparar(a):
    getattr(etapas, f"preparar_{a.etapa}")()
    unids = unidades(a.etapa, itens_da_etapa(a.etapa))
    gs = grupos(a.etapa, unids)
    for m in PRECOS:
        e, s, c = custo(a.etapa, m, unids)
        print(f"  {m}: ~{e / 1e6:.1f} M tokens de entrada, ~{s / 1e6:.1f} M de saída, ~US$ {c:.2f} no lote")
    print(f"[preparar] {len(unids):,} partes em {len(gs):,} pedidos")


def traduzir_sincrono(etapa, modelo, chave, grupo):
    resp = http_json("https://api.anthropic.com/v1/messages", metodo="POST",
                     cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"},
                     corpo=payload(etapa, modelo, grupo))
    txt = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
    return ler_resposta(grupo, txt, etapa), resp.get("usage", {})


def cmd_amostra(a):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    itens = itens_da_etapa(a.etapa)
    a.n = a.n or {"henry": 10, "dicionario": 40, "temas": 200}[a.etapa]
    rnd = random.Random(7)
    escolha = sorted(itens, key=lambda x: -len(x["texto"]))[:max(1, a.n // 4)] + rnd.sample(itens, a.n - max(1, a.n // 4))
    unids = unidades(a.etapa, escolha)
    res, uso = {}, Counter()
    for _, g in grupos(a.etapa, unids):
        r, u = traduzir_sincrono(a.etapa, modelo, chave, g)
        res.update(r)
        uso.update({k: v for k, v in u.items() if isinstance(v, int)})
        print(f"  {len(res)}/{len(unids)} partes", flush=True)
    linhas, recusas = [], 0
    for uid, en in unids:
        pt = res.get(uid, "")
        pr = problemas(a.etapa, en, pt, uid)
        recusas += bool(pr)
        velho = atual(a.etapa, uid.split("#")[0]) if "#" not in uid else "(parte de texto longo)"
        aviso = f"<div class='p'>{html.escape('; '.join(pr))}</div>" if pr else ""
        linhas.append(f"<tr><td><b>{html.escape(uid)}</b></td><td>{html.escape(en)}</td><td>{html.escape(velho)}</td>"
                      f"<td>{html.escape(pt)}{aviso}</td></tr>")
    entrada = uso["input_tokens"] + uso["cache_read_input_tokens"] + uso["cache_creation_input_tokens"]
    pe, ps = PRECOS.get(modelo, (0, 0))
    gasto = (entrada * pe + uso["output_tokens"] * ps) / 1e6
    total_itens = itens_da_etapa(a.etapa)
    fator = sum(len(x["texto"]) for x in total_itens) / max(1, sum(len(t) for _, t in unids))
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{a.etapa}: amostra</title>
<style>body{{font:14px/1.5 system-ui,sans-serif;margin:16px;background:#fbf8f1;color:#222}}table{{border-collapse:collapse}}
td,th{{border:1px solid #d8cfbd;padding:6px 8px;vertical-align:top;max-width:32vw}}th{{background:#efe6d3}}
.p{{color:#a00;font-size:12px;margin-top:4px}}</style></head><body>
<h1>{a.etapa} — amostra com {html.escape(modelo)}</h1><p>{len(unids)} partes, {recusas} recusadas pela validação.
Esta amostra: US$ {gasto:.3f}. Estimativa do lote completo (Batch API, 50% de desconto): US$ {gasto * fator / 2:.2f}.</p>
<table><tr><th>id</th><th>Inglês</th><th>Atual</th><th>Novo</th></tr>{''.join(linhas)}</table></body></html>"""
    saida = TRAB / f"relatorio_{a.etapa}.html"
    saida.write_text(doc, encoding="utf-8")
    print(f"[amostra] {recusas} recusadas de {len(unids)}; gasto US$ {gasto:.3f}; lote completo ~US$ {gasto * fator / 2:.2f}")
    print(f"[amostra] relatório: {saida}")


def enviar(a, so_recusadas=False):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    unids = unidades(a.etapa, itens_da_etapa(a.etapa))
    est = ler_json(arq(a.etapa, "saida"), {"partes": {}, "recusas": {}})
    lotes = ler_json(arq(a.etapa, "lotes"), [])
    em_lote = {u for lt in lotes if not lt.get("baixado") for u in lt["uids"]}
    falta = [u for u in unids if u[0] not in est["partes"] and u[0] not in em_lote]
    if so_recusadas:
        falta = [u for u in falta if u[0] in est["recusas"]]
        gs = [(f"r{len(lotes)}_{i:05d}", [u]) for i, u in enumerate(falta)]     # cada recusada sozinha
    else:
        gs = grupos(a.etapa, falta)
    if a.limite:
        gs = gs[:a.limite]
    print(f"[enviar] {sum(len(g) for _, g in gs):,} partes em {len(gs):,} pedidos ({len(est['partes']):,} já prontas)")
    if not gs:
        return
    for i in range(0, len(gs), 5000):
        bloco = gs[i:i + 5000]
        resp = http_json("https://api.anthropic.com/v1/messages/batches", metodo="POST",
                         cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"},
                         corpo={"requests": [{"custom_id": cid, "params": payload(a.etapa, modelo, g)} for cid, g in bloco]})
        lotes.append({"id": resp["id"], "modelo": modelo, "criado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
                      "grupos": {cid: [u for u, _ in g] for cid, g in bloco}, "uids": [u for _, g in bloco for u, _ in g],
                      "baixado": False})
        gravar_atomico(arq(a.etapa, "lotes"), lotes, indent=None)
        print(f"  lote {resp['id']}: {len(bloco)} pedidos")


def cmd_status(a):
    chave = obter_chave("anthropic", a.chave)
    for lt in ler_json(arq(a.etapa, "lotes"), []):
        info = http_json(f"https://api.anthropic.com/v1/messages/batches/{lt['id']}",
                         cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"})
        c = info.get("request_counts", {})
        print(f"  {lt['id']} ({lt['modelo']}): {info.get('processing_status')} | ok={c.get('succeeded', 0)} "
              f"proc={c.get('processing', 0)} erro={c.get('errored', 0)} | baixado={lt.get('baixado')}")


def cmd_baixar(a):
    chave = obter_chave("anthropic", a.chave)
    cab = {"x-api-key": chave, "anthropic-version": "2023-06-01"}
    textos = dict(unidades(a.etapa, itens_da_etapa(a.etapa)))
    est = ler_json(arq(a.etapa, "saida"), {"partes": {}, "recusas": {}})
    lotes = ler_json(arq(a.etapa, "lotes"), [])
    novos = 0
    for lt in lotes:
        if lt.get("baixado"):
            continue
        info = http_json(f"https://api.anthropic.com/v1/messages/batches/{lt['id']}", cabecalhos=cab)
        if info.get("processing_status") != "ended":
            print(f"  {lt['id']}: ainda em '{info.get('processing_status')}'")
            continue
        bruto = http_texto(info.get("results_url") or f"https://api.anthropic.com/v1/messages/batches/{lt['id']}/results", cab)
        for linha in bruto.splitlines():
            if not linha.strip():
                continue
            obj = json.loads(linha)
            res = obj.get("result", {})
            if res.get("type") != "succeeded" or res["message"].get("stop_reason") == "max_tokens":
                continue
            grupo = [(u, textos[u]) for u in lt["grupos"].get(obj["custom_id"], []) if u in textos]
            txt = "".join(b.get("text", "") for b in res["message"].get("content", []) if b.get("type") == "text")
            for uid, pt in ler_resposta(grupo, txt, a.etapa).items():
                pr = problemas(a.etapa, textos[uid], pt, uid)
                if pr:
                    est["recusas"][uid] = {"pt": pt, "motivos": pr, "modelo": lt["modelo"]}
                else:
                    est["partes"][uid] = pt
                    est["recusas"].pop(uid, None)
                    novos += 1
        lt["baixado"] = True
        gravar_atomico(arq(a.etapa, "saida"), est, indent=None)
        gravar_atomico(arq(a.etapa, "lotes"), lotes, indent=None)
    print(f"[baixar] +{novos:,} partes; total {len(est['partes']):,} de {len(textos):,}; {len(est['recusas'])} recusadas")
    motivos = Counter(m.split(":")[0].split(" (")[0] for r in est["recusas"].values() for m in r["motivos"])
    if motivos:
        print("  motivos:", dict(motivos))


def remissao_nave(en):
    """ "See IRON" -> "Veja FERRO", com o mesmo título em português que o site mostra para o verbete"""
    m = re.fullmatch(r"See ([A-Z][A-Z ,'()\-]+?)\.?", en.strip())
    if not m:
        return None
    assunto("x|x|0")
    t = _TITULOS.get(m.group(1).strip())
    return "Veja " + t.upper() if t else None


def cmd_aplicar(a):
    itens = itens_da_etapa(a.etapa)
    est = ler_json(arq(a.etapa, "saida"), {"partes": {}, "recusas": {}})
    tr, novos, antigos = {}, 0, []
    for it in itens:
        partes = fatiar_com_sep(texto_fonte(a.etapa, it["texto"]), FATIA)
        if len(partes) == 1:
            pt = est["partes"].get(it["id"])
        else:
            pedacos = [est["partes"].get(f"{it['id']}#{k}") for k in range(len(partes))]
            pt = "".join(p + sep for p, (_, sep) in zip(pedacos, partes)).strip() if all(pedacos) else None
        if a.etapa == "temas":
            pt = remissao_nave(it["texto"]) or pt
        if pt:
            tr[it["id"]] = pt
            novos += 1
        else:
            velho = atual(a.etapa, it["id"])
            if velho:
                tr[it["id"]] = velho
            antigos.append(it["id"])
    gravar_atomico(TRAB / f"{a.etapa}_pt.json", tr, indent=None)
    print(f"[aplicar] {novos:,} traduções novas; {len(antigos)} ficam com a tradução atual: {antigos[:10]}")
    getattr(etapas, f"aplicar_{a.etapa}")()


def main():
    ap = argparse.ArgumentParser(description="Henry, Easton e Nave via LLM (Batch API)")
    ap.add_argument("acao", choices=["amostra", "preparar", "enviar", "status", "baixar", "reenviar", "aplicar"])
    ap.add_argument("etapa", choices=list(PROMPTS))
    ap.add_argument("--modelo", default=None)
    ap.add_argument("--chave", default=None)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--limite", type=int, default=0)
    a = ap.parse_args()
    {"amostra": cmd_amostra, "preparar": cmd_preparar, "enviar": enviar, "status": cmd_status, "baixar": cmd_baixar,
     "reenviar": lambda x: enviar(x, so_recusadas=True), "aplicar": cmd_aplicar}[a.acao](a)


if __name__ == "__main__":
    main()
