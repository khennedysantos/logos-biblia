"""Prepara e aplica cada etapa da tradução do Sola.
uso: python3 etapas.py preparar|aplicar  glosas|temas|dicionario|calvino

Os originais em inglês nunca são apagados: as traduções vão para pastas pt/
(ou, no caso das glosas, substituem só o que ainda estava em inglês)."""
import json, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SITE = AQUI.parents[1]
DATA = SITE / "data"
TRAB = AQUI / "trabalho"
TRAB.mkdir(exist_ok=True)
REF = re.compile(r"\b[1-3]?[A-Z]{2,3} \d")


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def gravar(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def entradas(etapa, itens):
    gravar(TRAB / f"{etapa}.json", itens)
    print(f"[{etapa}] {len(itens)} itens, {sum(len(i['texto']) for i in itens) / 1e6:.2f} milhões de caracteres")


def traducoes(etapa):
    arq = TRAB / f"{etapa}_pt.json"
    return ler(arq) if arq.exists() else {}


# ---------------- glosas do interlinear (só o que ainda está em inglês) ----------------
def mapa_glosas():
    arq = SITE / "ferramentas" / "glosas_pt.json"
    return ler(arq) if arq.exists() else {}


PT_COMUNS = set("""de do da dos das para pelo pela em no na nos nas ao aos à que não e ele ela eles elas
dele dela deles dEle dEla eu tu nós vós seu sua seus suas meu minha teu tua nosso nossa este esta estes
isso isto aquele antes depois diante sobre entre contra até com sem dentro fora porque pois mas ou se
então assim também todo toda todos cada um uma era foi será são é disse diz sendo tendo""".split())


def parece_pt(g):
    palavras = re.findall(r"[A-Za-zÀ-ú]+", g)
    return bool(re.search(r"[ãõáéíóúâêôçà]", g)) or any(w in PT_COMUNS for w in palavras)


def preparar_glosas():
    mapa = mapa_glosas()
    ja_pt = set(mapa.values())
    vistas = {}
    for arq in (DATA / "interlinear").glob("*/*.json"):
        for verso in ler(arq):
            for p in verso:
                g = p[3]
                if g and g not in ja_pt and g not in vistas and re.search(r"[A-Za-z]{2}", g) \
                        and not parece_pt(g):
                    vistas[g] = True
    entradas("glosas", [{"id": g, "texto": g} for g in vistas])


# glosas que aparecem sem contexto e saem erradas no tradutor automático
GLOSAS_FIXAS = {
    "beginning": "princípio", "beginning,": "princípio,", "true": "verdadeiro", "will": "vontade",
    "grasped [it].": "compreenderam [-na].", "grasped [it]": "compreenderam [-na]",
    "only begotten": "unigênito", "bosom": "seio", "dwelt": "habitou", "dwelling": "habitação",
    "world": "mundo", "world,": "mundo,", "kingdom": "reino", "righteous": "justo", "saying": "dizendo",
    "blessed": "bem-aventurado", "Blessed": "Bem-aventurados", "mercy": "misericórdia",
    "repent": "arrependei-vos", "believing": "crendo", "believe": "crer", "believes": "crê",
    "may believe": "creiam", "having believed": "tendo crido", "believed": "creram",
}
CONTRACOES = [(r"\b([Ee])m \[o\]", lambda m: "[" + ("N" if m.group(1) == "E" else "n") + "o]"),
              (r"\b([Ee])m \[a\]", lambda m: "[" + ("N" if m.group(1) == "E" else "n") + "a]"),
              (r"\b([Dd])e \[o\]", lambda m: "[" + m.group(1) + "o]"),
              (r"\b([Dd])e \[a\]", lambda m: "[" + m.group(1) + "a]")]


def ajusta_glosa(g):
    for padrao, troca in CONTRACOES:
        g = re.sub(padrao, troca, g)
    return g


def aplicar_glosas():
    tr = traducoes("glosas")
    tr.update(GLOSAS_FIXAS)
    n = 0
    for arq in (DATA / "interlinear").glob("*/*.json"):
        versos, mudou = ler(arq), False
        for verso in versos:
            for p in verso:
                pt = ajusta_glosa(tr.get(p[3], p[3]))
                if pt != p[3]:
                    p[3] = pt; n += 1; mudou = True
        if mudou:
            gravar(arq, versos)
    mapa = mapa_glosas()
    mapa.update(tr)
    gravar(SITE / "ferramentas" / "glosas_pt.json", mapa)
    print(f"[glosas] {n} palavras atualizadas no interlinear")


# ---------------- temas (Nave) ----------------
def arquivos_temas():
    return [a for a in sorted((DATA / "topics").glob("*.json"))
            if a.name not in ("index.json", "aliases_pt.json", "titulos_pt.json")]


def separa(linha):
    corpo = linha.lstrip("-").strip()
    m = REF.search(corpo)
    texto = (corpo[:m.start()] if m else corpo).strip(" ,;:")
    resto = corpo[m.start():] if m else ""
    return texto, resto


# cabeçalhos que se repetem centenas de vezes no Nave: tradução fixa, revisada
FRASES_NAVE = {
    "general scriptures concerning": "Textos gerais sobre", "figurative": "Figurado",
    "instances of": "Exemplos de", "symbolical": "Simbólico", "prophecies concerning": "Profecias sobre",
    "prophecy concerning": "Profecia sobre", "unclassified scriptures relating to": "Outros textos sobre",
    "death of": "Morte de", "descendants of": "Descendentes de", "exemplified": "Exemplificado",
    "forbidden": "Proibido", "enjoined": "Ordenado", "spiritual": "Espiritual", "of god": "De Deus",
    "of jesus": "De Jesus", "of david": "De Davi", "an ancestor of jesus": "Antepassado de Jesus",
    "a city of the tribe of judah": "Cidade da tribo de Judá", "a levite": "Um levita",
    "a priest": "Um sacerdote", "a benjamite": "Um benjamita", "one of the nethinim": "Um dos netineus",
    "israelites": "Israelitas", "instances of, see": "Exemplos de, veja",
}


def chave_nave(texto):
    return texto.lower().rstrip(":. ")


def texto_para_traduzir(texto):
    # o modelo não traduz texto todo em maiúsculas: normaliza para frase comum
    return texto.capitalize() if texto.isupper() else texto


def preparar_temas():
    itens = []
    for arq in arquivos_temas():
        for assunto, linhas in ler(arq).items():
            for i, l in enumerate(linhas):
                texto, _ = separa(l)
                if texto and re.search("[A-Za-z]", texto) and chave_nave(texto) not in FRASES_NAVE:
                    itens.append({"id": f"{arq.stem}|{assunto}|{i}", "texto": texto_para_traduzir(texto)})
    entradas("temas", itens)


def aplicar_temas():
    tr = traducoes("temas")
    if not tr:
        return print("[temas] nada traduzido ainda")
    for arq in arquivos_temas():
        sec = ler(arq)
        for assunto, linhas in sec.items():
            for i, l in enumerate(linhas):
                texto, _ = separa(l)
                pt = FRASES_NAVE.get(chave_nave(texto)) or tr.get(f"{arq.stem}|{assunto}|{i}")
                if pt and texto.lower().startswith("see "):
                    # remissões ("See music"): padroniza como "Veja ..."
                    pt = re.sub(r"(?i)^(veja|ver|consulte|vide)\s+", "", pt)
                    pt = "Veja " + pt[:1].lower() + pt[1:]
                if pt:
                    _, resto = separa(l)
                    linhas[i] = "-" + pt + (" " + resto if resto else "")
        sec["__pt"] = True
        gravar(DATA / "topics" / "pt" / arq.name, sec)
    print(f"[temas] {len(tr)} linhas gravadas em data/topics/pt/")


# ---------------- dicionário (Easton) ----------------
def arquivos_dic():
    return [a for a in sorted((DATA / "dictionary").glob("*.json"))
            if a.name not in ("index.json", "titulos_pt.json")]


def preparar_dicionario():
    itens = []
    for arq in arquivos_dic():
        for termo, defs in ler(arq).items():
            for i, d in enumerate(defs):
                if d.strip():
                    itens.append({"id": f"{arq.stem}|{termo}|{i}", "texto": d})
    entradas("dicionario", itens)


def aplicar_dicionario():
    tr = traducoes("dicionario")
    if not tr:
        return print("[dicionario] nada traduzido ainda")
    for arq in arquivos_dic():
        d = ler(arq)
        for termo, defs in d.items():
            d[termo] = [tr.get(f"{arq.stem}|{termo}|{i}", x) for i, x in enumerate(defs)]
        d["__pt"] = True
        gravar(DATA / "dictionary" / "pt" / arq.name, d)
    print(f"[dicionario] {len(tr)} definições gravadas em data/dictionary/pt/")


# ---------------- comentários de Calvino ----------------
def preparar_calvino():
    base = DATA / "commentaries" / "calvin"
    itens = []
    for livro in sorted(p for p in base.iterdir() if p.is_dir() and p.name != "pt"):
        for arq in sorted(livro.glob("*.json"), key=lambda a: int(a.stem)):
            for v, txt in ler(arq).items():
                if v.isdigit() and txt.strip():
                    # o número do versículo no início ("16.") vai separado, senão vira "16 anos."
                    corpo = NUM_VERSO.sub("", txt, count=1)
                    itens.append({"id": f"{livro.name}|{arq.stem}|{v}", "texto": corpo})
    entradas("calvino", itens)


NUM_VERSO = re.compile(r"^\s*\d+(?:\s*[-,]\s*\d+)*\s*[\.:]?\s*")


def aplicar_calvino():
    tr = traducoes("calvino")
    if not tr:
        return print("[calvino] nada traduzido ainda")
    base = DATA / "commentaries" / "calvin"
    por_cap, originais = {}, {}
    for k, v in tr.items():
        livro, cap, verso = k.split("|")
        if (livro, cap) not in originais:
            originais[(livro, cap)] = ler(base / livro / f"{cap}.json")
        m = NUM_VERSO.match(originais[(livro, cap)].get(verso, ""))
        prefixo = m.group(0) if m else ""
        por_cap.setdefault((livro, cap), {})[verso] = prefixo + v
    for (livro, cap), versos in por_cap.items():
        versos["__pt"] = True
        gravar(DATA / "commentaries" / "calvin" / "pt" / livro / f"{cap}.json", versos)
    print(f"[calvino] {len(tr)} blocos em {len(por_cap)} capítulos gravados em data/commentaries/calvin/pt/")


if __name__ == "__main__":
    acao, etapa = sys.argv[1], sys.argv[2]
    globals()[f"{acao}_{etapa}"]()
