"""Importa o Catecismo de Heidelberg (1563) e a Confissão Belga (1561, revista em Dort, 1619) para data/confissoes/,
a partir de Philip Schaff, The Creeds of Christendom, vol. 3 (1877, domínio público), na CCEL:
https://ccel.org/ccel/schaff/creeds3.html (arquivo ThML creeds3.xml).

Schaff traz o original e o inglês lado a lado, linha por linha:
- Heidelberg: alemão (3ª edição de 1563) e o inglês da edição do tricentenário (Nova York, 1863). Sem textos de prova
  (o Heidelberg original só tinha remissões na margem, que Schaff não reproduz). Cada pergunta ganha o seu Domingo
  (a divisão em 52 Domingos, das edições de 1563 em diante).
- Belga: francês (manuscrito de 1580 com a revisão de Dort) e o inglês da Reformed (Dutch) Church in America. Os textos
  de prova estão em notas na coluna francesa; aqui ficam no fim de cada parágrafo, marcados [1] (as notas da coluna
  inglesa, só comentários de Schaff, ficam de fora).

Uso (o creeds3.xml baixado fica em ferramentas/fontes/ccel/, fora do git):
    python3 ferramentas/confissoes_ccel.py
O português (campos "p", "r", "titulo" e "pt") é a tradução do Sola, feita na sessão do agente sem API, e é
preservado quando o importador roda de novo. Depois: python3 ferramentas/gerar_paginas.py"""
import json, re, sys, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from confissoes import DESTINO, bl, converter                      # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "ferramentas" / "fontes" / "ccel" / "creeds3.xml"
URL = "https://ccel.org/ccel/s/schaff/creeds3.xml"
# Domingos do Heidelberg: a primeira pergunta de cada um dos 52
DOMINGOS = [1, 3, 6, 9, 12, 16, 20, 24, 26, 27, 29, 31, 33, 35, 37, 40, 45, 46, 50, 53, 54, 57, 59, 62, 65, 69, 72, 75,
            78, 80, 83, 86, 88, 92, 96, 99, 101, 103, 104, 105, 108, 110, 112, 113, 116, 120, 122, 123, 124, 125, 126, 127]
# referências que a CCEL não entendeu ou que têm erro de impressão em Schaff (texto da referência -> OSIS)
CORRECOES = {"Eph. ii. 8, 9, 10": "Eph.2.8-Eph.2.10", "Fal. ii. 6": "Gal.2.16",       # "justifiés par la seule foi"
             "Phil. i. l, 29": "Phil.1.29", "Gal. v. l": "Gal.5.1", "Gal. xxx. 15": "Gal.3.15",
             "Jean xvi. 38": "John.16.33"}
# a coluna francesa numera os Salmos como o hebraico, que conta o título como versículo 1: nestes, a Bíblia Livre
# (como as Bíblias inglesas) fica 1 versículo atrás (2 nos Salmos 51, 52, 54 e 60)
TITULO_SALMO = {**{n: 1 for n in (3, 4, 5, 6, 7, 8, 9, 12, 13, 18, 19, 20, 21, 22, 30, 31, 34, 36, 38, 39, 40, 41, 42,
                                   44, 45, 46, 47, 48, 49, 53, 55, 56, 57, 58, 59, 61, 62, 63, 64, 65, 67, 68, 69, 70,
                                   75, 76, 77, 80, 81, 83, 84, 85, 88, 89, 92, 102, 108, 140, 142)},
                **{n: 2 for n in (51, 52, 54, 60)}}
# erros de digitalização do inglês de Schaff na CCEL
ERRATA = [(r"\bthon\b", "thou"), (r"\bns\b", "us"), (r"\boar\b", "our"), (r"before trod\b", "before God"),
          (r"\barid promote", "and promote"), (r"have eo earthly", "have no earthly"), (r"God sp strictly", "God so strictly"),
          (r"Christi ascension", "Christ's ascension"), (r"commandmen;", "commandment;"), (r"from, thence", "from thence"),
          (r"He\. that believeth", "He that believeth"), (r"saved y but", "saved; but"), (r"the day\. of rest", "the day of rest"),
          (r"shall he born", "shall be born"), (r"by the, grace", "by the grace"), (r"by the month of", "by the mouth of"),
          (r"might he a merciful", "might be a merciful"), (r"by Mm\b", "by him"), (r"able, also", "able also"),
          (r"\bassumer\b", "assume"), (r"truer Church", "true Church"), (r"\bnpon\b", "upon"), (r"\btbeir\b", "their"),
          (r"\bsonls\b", "souls"), (r"\bJesns\b", "Jesus"), (r"belie vers", "believers"), (r"\btheii\b", "their")]
MINUSCULAS = {"a", "an", "and", "as", "by", "for", "from", "in", "of", "on", "or", "the", "to", "unto", "with"}


def titulo_ingles(s):
    """"OF THE WRITTEN WORD OF GOD." -> "Of the Written Word of God"."""
    s = re.sub(r"\bOP\b", "OF", re.sub(r"\bPROM\b", "FROM", re.sub(r"CHRIST' ", "CHRIST'S ", s.upper())))
    palavras = limpo(s).rstrip(".").lower().split()
    return " ".join(w if i and w in MINUSCULAS else w[:1].upper() + w[1:] for i, w in enumerate(palavras))


ROMANOS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def romano(s):
    n = 0
    for a, b in zip(s, s[1:] + " "):
        v = ROMANOS[a]
        n += -v if ROMANOS.get(b, 0) > v else v
    return n


def secao(titulo):
    if not FONTE.exists():
        FONTE.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, FONTE)
    s = FONTE.read_text(encoding="utf-8")
    i = s.index(f'<div2 title="{titulo}')
    return ET.fromstring(s[i:s.index("<div2", i + 10)])


def texto(el):
    """o texto da célula, sem as notas de rodapé"""
    partes = [el.text or ""]
    for f in el:
        if f.tag != "note":
            partes.append(texto(f))
        partes.append(f.tail or "")
    return "".join(partes)


def limpo(s):
    s = re.sub(r"\s+", " ", s).strip()
    for errado, certo in ERRATA:
        s = re.sub(errado, certo, s)
    return re.sub(r" ([,.;:?!)])", r"\1", s)


def linhas(raiz):
    """(estilo, texto inglês, célula original) de cada linha da tabela de duas colunas"""
    for tr in raiz.iter("tr"):
        tds = tr.findall("td")
        if tds:
            yield tds[-1].get("style", ""), limpo(texto(tds[-1])), tds[0] if len(tds) > 1 else None


def heidelberg():
    itens, atual, campo = [], None, None
    for estilo, en, _ in linhas(secao("The Heidelberg Catechism")):
        m = re.fullmatch(r"\(?Q ?uestion ?(\d+)\.", en)        # "(Question 80." : acrescentada na 2ª edição
        if m:
            atual = {"n": m.group(1), "p_en": [], "r_en": []}
            itens.append(atual)
            campo = "p_en"
        elif not atual or not en or "text-align:center" in estilo:
            if re.fullmatch(r"A ?nswer\.", en) and atual:
                campo = "r_en"
            continue                                     # títulos das partes, separadores
        elif "text-indent" in estilo or not atual[campo]:
            atual[campo].append(en)                      # parágrafo novo
        else:
            atual[campo][-1] += " " + en                 # continuação depois da quebra de página
    assert [int(q["n"]) for q in itens] == list(range(1, 130)), "esperava as perguntas 1 a 129"
    for q in itens:
        assert q["p_en"] and q["r_en"], f"pergunta {q['n']} sem texto"
        q["p_en"] = " ".join(q["p_en"])
        q["r_en"] = "\n".join(limpo(p) for p in q["r_en"])
        if q["n"] == "80":                               # Schaff põe a 80 inteira entre parênteses
            q["r_en"] = q["r_en"].removesuffix(")")
        q["domingo"] = sum(1 for d in DOMINGOS if d <= int(q["n"]))
    return itens


def referencias(sr):
    """partes OSIS de uma referência: o livro vem da CCEL, mas o capítulo (em romano) e os versículos vêm do texto,
    porque a CCEL lê mal alguns romanos ("Psa. cii. 19" -> Ps.2.19; "Psa. c. 3" -> Ps.3)"""
    if sr.text in CORRECOES:
        return CORRECOES[sr.text].split()
    osis = (sr.get("osisRef") or "").replace("Bible:", "")
    m = re.search(r"\b([ivxlc]+)\.?\s+(\d[\d\s,.\-–]*)$", (sr.text or "").lower())
    if not m or not osis:
        return osis.split()
    livro, cap = osis.split(".")[0], romano(m.group(1).upper())
    tira = TITULO_SALMO.get(cap, 0) if livro == "Ps" else 0
    partes = []
    for trecho in m.group(2).split(","):
        vs = [max(1, int(v) - tira) for v in re.findall(r"\d+", trecho)]
        if vs:
            partes.append(f"{livro}.{cap}.{vs[0]}" + (f"-{livro}.{cap}.{vs[-1]}" if len(vs) > 1 else ""))
    return partes


def provas_da_celula(td, biblia, problemas):
    refs = []
    for nota in td.iter("note"):
        for sr in nota.iter("scripRef"):
            for parte in referencias(sr):
                refs += converter(parte, biblia, problemas)
    return refs


def belga(biblia, problemas):
    artigos, atual, esperando_titulo = [], None, False
    for estilo, en, fr in linhas(secao("The Belgic Confession")):
        m = re.fullmatch(r"A ?rt\. ([IVXL]+)\.?", en)
        if m:
            atual = {"n": str(romano(m.group(1))), "titulo_en": "", "itens": []}
            artigos.append(atual)
            esperando_titulo = True
            continue
        if not atual or not en:
            continue
        if esperando_titulo and "text-align:center" in estilo:
            atual["titulo_en"] = titulo_ingles(en)
            esperando_titulo = False
            continue
        refs = provas_da_celula(fr, biblia, problemas) if fr is not None else []
        if "text-indent" in estilo or not atual["itens"]:
            atual["itens"].append({"en": en, "refs": refs})
        else:
            atual["itens"][-1]["en"] += " " + en
            atual["itens"][-1]["refs"] += refs
    assert [int(a["n"]) for a in artigos] == list(range(1, 38)), "esperava os artigos 1 a 37"
    for a in artigos:
        for i, it in enumerate(a["itens"], 1):
            it["n"] = str(i)
            it["en"] = limpo(it["en"])
            unicas = []
            for r in it.pop("refs"):
                if r not in unicas:
                    unicas.append(r)
            it["provas"] = {"1": unicas} if unicas else {}
            if unicas:
                it["en"] += " [1]"
    return artigos


def main():
    biblia, problemas = bl(), []
    docs = {
        "heidelberg": {"id": "heidelberg", "titulo": "Catecismo de Heidelberg", "titulo_en": "The Heidelberg Catechism",
                       "ano": 1563, "tipo": "catecismo",
                       "fonte": "Heidelberg Catechism (1563), domínio público. Texto inglês da edição do tricentenário "
                                "(Nova York, 1863), em Philip Schaff, The Creeds of Christendom, vol. 3 (1877): "
                                "https://ccel.org/ccel/schaff/creeds3.iv.vi.html",
                       "itens": heidelberg()},
        "confissao-belga": {"id": "confissao-belga", "titulo": "Confissão Belga", "titulo_en": "The Belgic Confession",
                            "ano": 1561, "tipo": "confissao",
                            "fonte": "Belgic Confession (1561, revista no Sínodo de Dort, 1619), domínio público. Texto "
                                     "inglês da Reformed (Dutch) Church in America e textos de prova da edição francesa, "
                                     "em Philip Schaff, The Creeds of Christendom, vol. 3 (1877): "
                                     "https://ccel.org/ccel/schaff/creeds3.iv.viii.html",
                            "partes": belga(biblia, problemas)},
    }
    for d, doc in docs.items():
        arq = DESTINO / f"{d}.json"
        antigo = json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else {}
        for q, velho in zip(doc.get("itens", []), antigo.get("itens", [])):
            q["p"], q["r"] = velho.get("p", ""), velho.get("r", "")
        for a, velho in zip(doc.get("partes", []), antigo.get("partes", [])):
            a["titulo"] = velho.get("titulo", "")
            for it, v in zip(a["itens"], velho["itens"]):
                it["pt"] = v.get("pt", "")
        for q in doc.get("itens", []):
            q.setdefault("p", ""); q.setdefault("r", ""); q.setdefault("provas", {})
        for a in doc.get("partes", []):
            a.setdefault("titulo", "")
            for it in a["itens"]:
                it.setdefault("pt", "")
            # ordem das chaves igual à dos outros documentos
            a.update({k: a.pop(k) for k in ("titulo_en", "titulo", "itens")})
            a["itens"] = [{"n": it["n"], "en": it["en"], "pt": it["pt"], "provas": it["provas"]} for it in a["itens"]]
        chave = "itens" if "itens" in doc else "partes"
        doc[chave] = doc.pop(chave)                      # a lista por último, depois dos metadados
        arq.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    refs = sum(len(v) for a in docs["confissao-belga"]["partes"] for it in a["itens"] for v in it["provas"].values())
    print(f"Heidelberg: 129 perguntas em 52 Domingos; Belga: 37 artigos, {refs} textos de prova; "
          f"{len(problemas)} problemas: {problemas[:8]}")


if __name__ == "__main__":
    main()
