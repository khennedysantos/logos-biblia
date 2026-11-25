"""Importa os símbolos de fé (domínio público) para data/confissoes/: a Confissão de Fé de Westminster, o Catecismo
Maior e o Breve Catecismo de Westminster (1647, com os textos de prova da Assembleia), os Cânones de Dort (1619, na
tradução inglesa antiga, também em domínio público) e a Confissão Batista de Londres de 1689 (sem as provas, que a fonte
não traz). A tradução da 1689 foi feita na sessão do agente (sem API), partindo da tradução da Westminster do Sola nas
seções que as duas têm em comum.

Fonte: o repositório NonlinearFruit/Creeds.json (estrutura sob Unlicense; os textos usados aqui são de domínio público
segundo o próprio repositório, que lista à parte os poucos que têm direitos — nenhum destes). O Heidelberg e a
Confissão Belga desse repositório NÃO são importados: lá estão em traduções inglesas modernas, com direitos autorais.

Uso (o repositório baixado fica fora do git):
    git clone --depth 1 https://github.com/NonlinearFruit/Creeds.json /tmp/creeds
    python3 ferramentas/confissoes.py /tmp/creeds/creeds
Grava o texto em inglês e as provas; o português (campos "pt", "p" e "r") vem de tradutor/confissoes_llm.py e é
preservado quando o importador roda de novo. Depois: python3 ferramentas/gerar_doutrinas.py e gerar_paginas.py."""
import json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "data" / "confissoes"
OSIS = dict(zip(
    "Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song Isa Jer Lam "
    "Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal Matt Mark Luke John Acts Rom 1Cor 2Cor Gal Eph Phil "
    "Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet 2Pet 1John 2John 3John Jude Rev".split(),
    "GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG ISA JER LAM "
    "EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP "
    "COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV".split()))
RE_PARTE = re.compile(r"^([1-3]?[A-Za-z]+)\.(\d+)(?:\.(\d+))?(?:-(?:[1-3]?[A-Za-z]+\.)?(\d+)(?:\.(\d+))?)?$")
DOCUMENTOS = {
    "westminster": ("westminster_confession_of_faith", "Confissão de Fé de Westminster", 1647, "confissao"),
    "catecismo-maior": ("westminster_larger_catechism", "Catecismo Maior de Westminster", 1647, "catecismo"),
    "breve-catecismo": ("westminster_shorter_catechism", "Breve Catecismo de Westminster", 1647, "catecismo"),
    "canones-de-dort": ("canons_of_dort", "Cânones de Dort", 1619, "canones"),
    # batista reformada: a Segunda Confissão de Londres (redigida em 1677, adotada em 1689); a fonte não traz as provas
    "confissao-batista-1689": ("london_baptist_1689", "Confissão de Fé Batista de Londres de 1689", 1689, "confissao"),
}


def bl():
    return {b["id"]: json.loads((RAIZ / "data" / "bibles" / "blivre" / f"{b['id']}.json").read_text(encoding="utf-8"))
            for b in json.loads((RAIZ / "data" / "books.json").read_text(encoding="utf-8"))["books"]}


def converter(ref, biblia, problemas):
    """"Rom.3.24-Rom.3.25" -> [["ROM", 3, 24, 25]]; capítulo inteiro -> [l, c, 0, 0]; de um capítulo a outro ->
    [l, c, a, b, c2] (de c:a até c2:b)"""
    saida = []
    for parte in ref.split(","):
        m = RE_PARTE.match(parte.strip())
        if not m or m.group(1) not in OSIS:
            problemas.append(f"referência não entendida: {ref}")
            continue
        l, c, a = OSIS[m.group(1)], int(m.group(2)), int(m.group(3) or 0)
        if m.group(5):                                   # Rom.3.24-Rom.3.25 ou Job.3.1-Job.4.2
            c2, b = int(m.group(4)), int(m.group(5))
        elif m.group(4) and m.group(3):                  # Rom.3.24-25 (sem livro e capítulo)
            c2, b = c, int(m.group(4))
        elif m.group(4):                                 # Job.38-Job.41 (capítulos)
            c2, b = int(m.group(4)), 0
        else:
            c2, b = c, a
        caps = biblia.get(l, [])
        if not (1 <= c <= len(caps)) or (a and a > len(caps[c - 1])) or not (1 <= c2 <= len(caps)) or \
                (b and b > len(caps[c2 - 1])):
            problemas.append(f"fora da Bíblia Livre: {ref}")
            continue
        saida.append([l, c, a, b] if c2 == c else [l, c, a, b, c2])
    return saida


def provas(lista, biblia, problemas):
    return {str(p["Id"]): [r for ref in p["References"] for r in converter(ref, biblia, problemas)] for p in lista or []}


def importar(origem):
    biblia = bl()
    DESTINO.mkdir(parents=True, exist_ok=True)
    for doc_id, (arquivo, titulo, ano, tipo) in DOCUMENTOS.items():
        fonte = json.loads((Path(origem) / f"{arquivo}.json").read_text(encoding="utf-8"))
        meta = fonte["Metadata"]
        assert meta.get("SourceAttribution") == "Public Domain", f"{arquivo}: não está marcado como domínio público"
        anterior = json.loads((DESTINO / f"{doc_id}.json").read_text(encoding="utf-8")) if (DESTINO / f"{doc_id}.json").exists() else {}
        pt_antigo = {}
        for parte in anterior.get("partes", []):
            pt_antigo[("t", parte["n"])] = parte.get("titulo", "")
            for it in parte["itens"]:
                pt_antigo[(parte["n"], it["n"])] = it.get("pt", "")
        for it in anterior.get("itens", []):
            pt_antigo[("q", it["n"])] = (it.get("p", ""), it.get("r", ""))
        problemas = []
        doc = {"id": doc_id, "titulo": titulo, "titulo_en": meta["Title"], "ano": ano, "tipo": tipo,
               "fonte": f"{meta['Title']} ({meta['Year']}), domínio público. Texto inglês: {meta.get('SourceUrl', '')} "
                        "(via github.com/NonlinearFruit/Creeds.json)."}
        if tipo == "catecismo":
            doc["itens"] = []
            for q in fonte["Data"]:
                n = str(q["Number"])
                p, r = pt_antigo.get(("q", n), ("", ""))
                doc["itens"].append({"n": n, "p_en": q["Question"], "r_en": q.get("AnswerWithProofs") or q["Answer"],
                                     "p": p, "r": r, "provas": provas(q.get("Proofs"), biblia, problemas)})
        else:
            doc["partes"] = []
            for cap in fonte["Data"]:
                n = str(cap["Chapter"])
                parte = {"n": n, "titulo_en": cap.get("Title", ""), "titulo": pt_antigo.get(("t", n), ""), "itens": []}
                for i, s in enumerate(cap["Sections"], 1):
                    sn = str(s.get("Section") or i)
                    parte["itens"].append({"n": sn, "en": s.get("ContentWithProofs") or s["Content"],
                                           "pt": pt_antigo.get((n, sn), ""), "provas": provas(s.get("Proofs"), biblia, problemas)})
                doc["partes"].append(parte)
        (DESTINO / f"{doc_id}.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        refs = sum(len(v) for it in doc.get("itens", []) + [x for p in doc.get("partes", []) for x in p["itens"]]
                   for v in it["provas"].values())
        print(f"[{doc_id}] {len(doc.get('itens') or doc.get('partes'))} {'perguntas' if tipo == 'catecismo' else 'partes'}, "
              f"{refs} referências; {len(problemas)} problemas: {problemas[:6]}")


if __name__ == "__main__":
    importar(sys.argv[1])
