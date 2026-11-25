"""Importa o Catecismo Batista de Benjamin Keach (1693, "The Baptist Catechism") para
data/confissoes/catecismo-batista.json.

O catecismo de Keach segue de perto o Breve Catecismo de Westminster, com as diferenças batistas (batismo dos que
creem, Ceia, igreja); foi publicado em 1693 e adotado pelas associações batistas de Filadélfia e de Charleston. O
texto usado é o da edição da Associação de Charleston (1813), domínio público, na transcrição do The Reformed Reader
(https://www.reformedreader.org/ccc/bapcat.htm), que não numera as perguntas (aqui de 1 a 114, na ordem) e traz os
textos de prova entre parênteses depois de cada trecho da resposta: eles viram os marcadores [1], [2]… como no
Catecismo Maior.

Uso (o HTML baixado fica em ferramentas/fontes/keach/, fora do git; reformedreader.org precisa estar liberado):
    python3 ferramentas/catecismo_batista.py
O português (campos "p" e "r") é a tradução do Sola, feita na sessão do agente sem API (aproveitando a do Breve
Catecismo nas perguntas iguais), e é preservado quando o importador roda de novo. Depois: gerar_paginas.py"""
import html, json, re, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from confissoes import DESTINO, bl                                 # noqa: E402
from provas_wikisource import refs                                 # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "ferramentas" / "fontes" / "keach" / "bapcat.htm"
URL = "https://www.reformedreader.org/ccc/bapcat.htm"
ARQUIVO = DESTINO / "catecismo-batista.json"
# erros de impressão ou de digitação nas provas (texto -> correção)
CORRECOES = {"John 5:38; Rev. 17:18, 19; 1:3": "John 5:39; Deut. 17:18, 19; Rev. 1:3", "Ps. 110:2": "Ps. 90:2",
             "Ex. 33:14": "Ex. 3:14", "Heb. 6:24, 25": "Heb. 7:24, 25", "Deut. 7:31, 32": "Deut. 12:31, 32",
             "Deut. 23:58": "Deut. 28:58", "1 Tim. 3:15, 16, 17": "2 Tim. 3:15, 16, 17",
             "Rom. 1: 15, 16, 10: 13": "Rom. 1:15, 16; 10:13", "8:33 to the end": "8:33-36",
             "1 Cor. 4:16; Rev. 11:20; 22:20": "1 Cor. 14:16; Rev. 22:20", "(Mt. 26:31)": "(Mt. 26:41)",
             "being justify to the freedom": "being left to the freedom", "by sinning a against": "by sinning against",
             "Is. any man": "Is any man", "ordinances,,": "ordinances,", "of our own neighbour's good name":
             "of our own and our neighbour's good name"}
# abreviações curtas desta edição -> nomes que o leitor de referências conhece
ABREV = {"Gn": "Genesis", "Is": "Isaiah", "Ez": "Ezekiel", "Jas": "James", "Jn": "John", "Lk": "Luke", "Mk": "Mark",
         "Mt": "Matthew", "Mic": "Micah", "Ph": "Philippians", "Pr": "Proverbs"}
RE_ABREV = re.compile(r"\b(" + "|".join(ABREV) + r")\b\.?(?=\s*\d)")
SEM_PROVAS = {"11"}                                       # perguntas que a fonte traz sem provas


def baixar():
    if not FONTE.exists():
        FONTE.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Sola)"})
        FONTE.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    return FONTE.read_text(encoding="latin-1")


def main():
    biblia, problemas = bl(), []
    t = re.sub(r"<br\s*/?>|</p>", "\n", baixar(), flags=re.I)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    perguntas = re.findall(r"Q\.\s*(.*?)\s*A\.\s*(.*?)(?=\s*Q\.\s|\s*Home\s|$)", t, flags=re.S)
    assert len(perguntas) == 114, len(perguntas)
    antigo = json.loads(ARQUIVO.read_text(encoding="utf-8")) if ARQUIVO.exists() else {}
    antigas = {q["n"]: q for q in antigo.get("itens", [])}
    itens = []
    for i, (p, r) in enumerate(perguntas, 1):
        n = str(i)
        p, r = " ".join(p.split()), " ".join(r.split())
        r = r.removesuffix(" The Reformed Reader")         # o rodapé do site, colado na última resposta
        for de, para in CORRECOES.items():
            p, r = p.replace(de, para), r.replace(de, para)
        provas, k = {}, 0

        def marca(m):
            nonlocal k
            lista = refs(RE_ABREV.sub(lambda a: ABREV[a.group(1)], m.group(1)), biblia, problemas)
            if not lista:
                problemas.append(f"pergunta {n}: parênteses sem referência: ({m.group(1)})")
                return m.group(0)
            k += 1
            provas[str(k)] = lista
            return f"[{k}]"
        r = re.sub(r"\s*\(([^()]*\d[^()]*)\)", marca, r)
        r = re.sub(r"\[(\d+)\]([.,;:])", r"\2[\1]", r)            # "sinners[2]." -> "sinners.[2]"
        r = re.sub(r"\s+\.$", "", r).replace(",,", ",")             # "others.[2] ." e ",," (sobras da fonte)
        if not provas and n not in SEM_PROVAS:
            problemas.append(f"pergunta {n} sem textos de prova")
        velho = antigas.get(n, {})
        if velho.get("r") and sorted(re.findall(r"\[\d+\]", velho["r"])) != sorted(re.findall(r"\[\d+\]", r)):
            problemas.append(f"pergunta {n}: os marcadores do português não batem com os do inglês")
        itens.append({"n": n, "p_en": p, "r_en": r, "p": velho.get("p", ""), "r": velho.get("r", ""), "provas": provas})
    doc = {"id": "catecismo-batista", "titulo": "Catecismo Batista", "titulo_en": "The Baptist Catechism",
           "ano": 1693, "tipo": "catecismo",
           "fonte": "The Baptist Catechism, de Benjamin Keach (Londres, 1693), na edição da Associação Batista de Charleston "
                    "(1813), domínio público, com os textos de prova. Transcrição do The Reformed Reader: " + URL,
           "itens": itens}
    ARQUIVO.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Catecismo Batista: {len(itens)} perguntas, "
          f"{sum(len(v) for q in itens for v in q['provas'].values())} referências, "
          f"{sum(1 for q in itens if q['r'])} traduzidas")
    for p in problemas:
        print("  ⚠", p)


if __name__ == "__main__":
    main()
