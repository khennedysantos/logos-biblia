"""Pais da Igreja: importa da CCEL (domínio público) as obras dos pais para data/pais/<obra>.json.

Por enquanto, as Confissões de Agostinho na tradução de J. G. Pilkington revista por Philip Schaff (Nicene and
Post-Nicene Fathers, série 1, vol. 1, 1886; https://www.ccel.org/ccel/schaff/npnf101.xml, baixado para
ferramentas/fontes/ccel/pais/): 13 livros, 276 capítulos, com as seções numeradas da tradição (1, 2, 3… em cada livro).

As notas de fim da edição são de dois tipos. As que só dizem de onde vem a citação bíblica ("Ps. cxlv. 3") viram
marcadores [n] no texto, como os textos de prova das confissões, e as referências vão para "provas" (formato
[livro, cap, v1, v2] da Bíblia Livre, por converter() do confissoes.py). As notas de comentário dos editores (Schaff,
Pusey, Watts…) ficam de fora: são longas, citam outros autores e não são do Agostinho.

A tradução em português ("titulo" do livro e do capítulo e "pt" de cada seção) é preservada quando o importador roda
de novo, desde que o inglês da seção não mude. Ela vem de ferramentas/tradutor/gemini_pais.py (ou da sessão do agente).

uso: python3 ferramentas/pais_ccel.py          (depois: python3 ferramentas/gerar_paginas.py)"""
import json, re, sys, urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from confissoes import bl, converter                     # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
FONTES = RAIZ / "ferramentas" / "fontes" / "ccel" / "pais"
DESTINO = RAIZ / "data" / "pais"
ROMANOS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
# o que pode sobrar numa nota de citação além das referências ("Comp.", "and", "See also", "ver.")
SOBRA_CITACAO = re.compile(r"^(?:[\s.,;:()\[\]—–-]|and|also|see|comp|cf|ver|vers|ibid|marg|lxx|vulg|ch|chap|&)*$", re.I)

# seções com o número errado na edição (livro, capítulo, número impresso) -> número certo; o Livro IX pula a seção 30
NUMERO_ERRADO = {(11, 17, "2"): "22"}
# referências que a CCEL leu errado (texto impresso da referência -> OSIS certo)
CORRECOES = {"1 Cor. v. 17": "2Cor.5.17", "Ps. cxxxix. 8": "Ps.139.8", "Ps. cxxiv. 5": "Ps.124.5", "Ps. cxxxvi. 6": "Ps.136.6"}

OBRAS = {
    "agostinho-confissoes": {
        "arquivo": "npnf101.xml", "url": "https://www.ccel.org/ccel/schaff/npnf101.xml", "div1": "vi",
        "autor": "Agostinho de Hipona", "autor_id": "agostinho", "obra_id": "confissoes",
        "titulo": "Confissões", "titulo_en": "The Confessions", "ano": "c. 397–400",
        "fonte": "Agostinho de Hipona, Confissões (c. 397–400), na tradução inglesa de J. G. Pilkington revista por Philip "
                 "Schaff (Nicene and Post-Nicene Fathers, série 1, vol. 1, 1886), domínio público. Texto da CCEL: "
                 "https://www.ccel.org/ccel/schaff/npnf101.vi.html",
    },
    # o sermão de Natal de Gregório de Nazianzo (25/12/380), em 18 seções (I–XVIII); um capítulo só, página única
    "gregorio-nazianzeno-natal": {
        "arquivo": "npnf207.xml", "url": "https://www.ccel.org/ccel/schaff/npnf207.xml", "div": ("div2", "iii.xxi"),
        "leitor": "sermao", "autor": "Gregório de Nazianzo", "autor_id": "gregorio-nazianzeno", "obra_id": "natal",
        "titulo": "Sermão 38: Sobre o Natal de Cristo", "titulo_en": "Oration XXXVIII. On the Theophany, or Birthday of Christ",
        "ano": "380",
        "fonte": "Gregório de Nazianzo, Sermão 38, Sobre a Teofania, ou o Nascimento de Cristo (Constantinopla, 380), na "
                 "tradução inglesa de C. G. Browne e J. E. Swallow (Nicene and Post-Nicene Fathers, série 2, vol. 7, 1894), "
                 "domínio público. Texto da CCEL: https://www.ccel.org/ccel/schaff/npnf207.iii.xxi.html",
    },
    # leituras clássicas fora dos Pais (data/leituras/, páginas em /leituras/)
    "spurgeon-encarnacao": {
        "arquivo": "spurgeon-sermons02.xml", "url": "https://www.ccel.org/ccel/spurgeon/sermons02.xml", "div": ("div1", "iv"),
        "leitor": "spurgeon", "destino": "leituras", "autor": "Charles H. Spurgeon", "autor_id": "spurgeon",
        "obra_id": "encarnacao-e-nascimento-de-cristo", "titulo": "A encarnação e o nascimento de Cristo",
        "titulo_en": "The Incarnation and Birth of Christ", "ano": "1855",
        "fonte": "Charles H. Spurgeon, The Incarnation and Birth of Christ, sermão nº 57, pregado na manhã de domingo, "
                 "23 de dezembro de 1855, na New Park Street Chapel, Southwark (The New Park Street Pulpit, vol. 2), "
                 "domínio público. Texto da CCEL: https://www.ccel.org/ccel/spurgeon/sermons02.iv.html",
    },
}


def romano(s):
    n = 0
    for a, b in zip(s, s[1:] + " "):
        v = ROMANOS[a]
        n += -v if ROMANOS.get(b, 0) > v else v
    return n


def limpo(t):
    t = re.sub(r"\s+", " ", t).strip()
    return re.sub(r"\s+([,.;:!?])", r"\1", t)


def nota_de_citacao(nota):
    """as referências de uma nota que só aponta a Escritura (senão, None)"""
    refs = list(nota.iter("scripRef"))
    if not refs:
        return None
    resto = "".join(_texto_fora_de_refs(nota))
    return refs if SOBRA_CITACAO.match(resto) else None


def _texto_fora_de_refs(el):
    if el.tag != "scripRef":
        yield el.text or ""
        for f in el:
            yield from _texto_fora_de_refs(f)
    yield el.tail or "" if el.tag != "note" else ""


def secao_com_marcas(p, biblia, problemas):
    """texto de um <p> com as notas de citação trocadas por [n] e as outras notas tiradas -> (texto, provas)"""
    partes, provas = [], {}

    def andar(el):
        for f in el:
            if f.tag == "note":
                refs = nota_de_citacao(f)
                lista = []
                for sr in refs or []:
                    impresso = re.sub(r"\s+", " ", "".join(sr.itertext())).strip()
                    for osis in (CORRECOES.get(impresso) or sr.get("osisRef") or "").replace("Bible:", "").split():
                        if ":" in osis:
                            continue                    # Bible.vul:… (numeração da Vulgata) ou apócrifos
                        lista += [r for r in converter(osis, biblia, problemas) if r not in lista]
                if lista:
                    n = str(len(provas) + 1)
                    provas[n] = lista
                    partes.append(f"[{n}]")
            else:
                partes.append(f.text or "")
                andar(f)
            partes.append(f.tail or "")

    partes.append(p.text or "")
    andar(p)
    texto = limpo("".join(partes))
    texto = re.sub(r"\s*\[(\d+)\]", r"[\1]", texto)          # marcador colado na palavra (como nas confissões)
    return texto, provas


def baixar(obra):
    arq = FONTES / obra["arquivo"]
    if not arq.exists():
        FONTES.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(obra["url"], headers={"User-Agent": "Mozilla/5.0 (Sola)"})
        arq.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    s = arq.read_text(encoding="utf-8")
    tag, ident = obra.get("div", ("div1", obra.get("div1")))
    i = s.index(f'id="{ident}"')
    i = s.rindex(f"<{tag} ", 0, i)
    j = s.find(f"<{tag} ", i + 10)
    return ET.fromstring(s[i:j if j > 0 else None].replace("&nbsp;", " "))


def confissoes(obra, biblia, problemas):
    raiz = baixar(obra)
    livros = []
    for d2 in raiz.findall("div2"):
        m = re.fullmatch(r"Book ([IVXL]+)", d2.get("shorttitle", ""))
        if not m:
            continue                                    # prefácio do tradutor, opinião de Agostinho
        livro = {"n": romano(m.group(1)), "resumo_en": limpo(d2.get("title", "")), "caps": []}
        for d3 in d2.findall("div3"):
            cap = {"n": romano(d3.get("n")), "titulo_en": limpo(d3.get("title", "")).rstrip("."), "secoes": []}
            for p in d3.findall("p"):
                txt, provas = secao_com_marcas(p, biblia, problemas)
                if re.match(r"Chapter [IVXL]+\.\s*—", txt):
                    continue                            # o título do capítulo, repetido no texto
                m2 = re.match(r"(\d+)\.\s*(.*)", txt, re.S)
                if m2:
                    n = NUMERO_ERRADO.get((livro["n"], cap["n"], m2.group(1)), m2.group(1))
                    cap["secoes"].append({"n": n, "en": m2.group(2), "provas": provas})
                elif txt and cap["secoes"]:                 # outro parágrafo da mesma seção
                    sec = cap["secoes"][-1]
                    base = len(sec["provas"])
                    sec["en"] += "\n\n" + re.sub(r"\[(\d+)\]", lambda x: f"[{int(x.group(1)) + base}]", txt)
                    sec["provas"].update({str(int(k) + base): v for k, v in provas.items()})
                elif txt:
                    problemas.append(f"texto antes da 1ª seção (livro {livro['n']}, cap. {cap['n']}): {txt[:60]}")
            if not cap["secoes"]:
                problemas.append(f"livro {livro['n']}, capítulo {cap['n']} sem texto")
            livro["caps"].append(cap)
        livros.append(livro)
    assert [l["n"] for l in livros] == list(range(1, 14)), "esperava os livros I a XIII"
    return livros


def sermao(obra, biblia, problemas):
    """um sermão dos Pais numerado em romanos (I., II., …): um livro, um capítulo, as seções; a introdução do editor fica de fora"""
    raiz = baixar(obra)
    cap = {"n": 1, "titulo_en": obra["titulo_en"], "secoes": []}
    for p in raiz.iter("p"):
        if "endnote" in (p.get("class") or "") or (p.get("class") or "") in ("c27", "c51", "c52", "c39"):
            continue
        txt, provas = secao_com_marcas(p, biblia, problemas)
        m = re.match(r"([IVXL]+)\.\s+(.*)", txt, re.S)
        if m:
            cap["secoes"].append({"n": str(romano(m.group(1))), "en": m.group(2), "provas": provas})
        elif txt and cap["secoes"]:
            sec = cap["secoes"][-1]
            base = len(sec["provas"])
            sec["en"] += "\n\n" + re.sub(r"\[(\d+)\]", lambda x: f"[{int(x.group(1)) + base}]", txt)
            sec["provas"].update({str(int(k) + base): v for k, v in provas.items()})
    assert [int(x["n"]) for x in cap["secoes"]] == list(range(1, len(cap["secoes"]) + 1)), "seções fora de ordem"
    return [{"n": 1, "resumo_en": "", "caps": [cap]}]


def spurgeon(obra, biblia, problemas):
    """um sermão de Spurgeon: o texto bíblico do título fica em "texto_en" e cada parágrafo vira uma seção numerada"""
    raiz = baixar(obra)
    cap = {"n": 1, "titulo_en": obra["titulo_en"], "secoes": []}
    verso = False                                       # a linha anterior era de um hino (linhas curtas seguidas)
    for p in raiz.iter("p"):
        txt, provas = secao_com_marcas(p, biblia, problemas)
        if not txt or re.match(r"(\(No\. \d+\)|A Sermon|The Incarnation and Birth of Christ$|Delivered on|At New Park|"
                               r"(by the )?REV\. C\.H\.)", txt, re.I):
            continue
        if not cap["secoes"] and txt.startswith("“But thou, Beth"):
            cap["texto_en"] = txt                         # Miqueias 5:2, o texto do sermão
            continue
        linha_de_hino = len(txt) < 70
        if linha_de_hino and verso:
            cap["secoes"][-1]["en"] += "\n" + txt          # as estrofes citadas ficam juntas, linha a linha
        else:
            cap["secoes"].append({"n": str(len(cap["secoes"]) + 1), "en": txt, "provas": provas})
            if linha_de_hino:
                cap["secoes"][-1]["hino"] = True
        verso = linha_de_hino
    return [{"n": 1, "resumo_en": "", "caps": [cap]}]


def preservar(novo, antigo):
    """traz a tradução já feita (títulos e seções cujo inglês não mudou)"""
    if not antigo:
        return
    velhos = {l["n"]: l for l in antigo.get("livros", [])}
    for l in novo["livros"]:
        vl = velhos.get(l["n"])
        if not vl:
            continue
        if vl.get("resumo") and vl.get("resumo_en") == l["resumo_en"]:
            l["resumo"] = vl["resumo"]
        vcaps = {c["n"]: c for c in vl["caps"]}
        for c in l["caps"]:
            vc = vcaps.get(c["n"])
            if not vc:
                continue
            if vc.get("titulo") and vc.get("titulo_en") == c["titulo_en"]:
                c["titulo"] = vc["titulo"]
            if vc.get("texto") and vc.get("texto_en") == c.get("texto_en"):
                c["texto"] = vc["texto"]
            vsec = {s["n"]: s for s in vc["secoes"]}
            for s in c["secoes"]:
                vs = vsec.get(s["n"])
                if vs and vs.get("pt") and vs["en"] == s["en"]:
                    s["pt"] = vs["pt"]


def main():
    biblia, problemas = bl(), []
    for oid, obra in OBRAS.items():
        leitor = {"sermao": sermao, "spurgeon": spurgeon}.get(obra.get("leitor"), confissoes)
        livros = leitor(obra, biblia, problemas)
        destino = RAIZ / "data" / obra.get("destino", "pais")
        destino.mkdir(parents=True, exist_ok=True)
        doc = {"id": oid, **{k: obra[k] for k in ("autor", "autor_id", "obra_id", "titulo", "titulo_en", "ano", "fonte")},
               "livros": livros}
        arq = destino / f"{oid}.json"
        preservar(doc, json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else None)
        arq.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        secs = [s for l in livros for c in l["caps"] for s in c["secoes"]]
        provas = sum(len(s["provas"]) for s in secs)
        print(f"{oid}: {len(livros)} livros, {sum(len(l['caps']) for l in livros)} capítulos, {len(secs)} seções, "
              f"{provas} citações bíblicas, {sum(len(s['en']) for s in secs) / 1e3:.0f} mil caracteres, "
              f"{sum(1 for s in secs if s.get('pt'))} seções traduzidas")
    for p in sorted(set(problemas)):
        print("  !", p)


if __name__ == "__main__":
    main()
