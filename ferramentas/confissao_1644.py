"""Importa a Primeira Confissão de Fé Batista de Londres (1644) para data/confissoes/confissao-batista-1644.json.

O texto de 1644 é de domínio público; a transcrição usada é a do The Reformed Reader
(https://www.reformedreader.org/ccc/1644lbc.htm), com as 149 notas de margem do original (os textos de prova).
A edição de 1644 numera mal alguns artigos (XXVI no lugar de XXXVI, XLIII sem ponto e dois LII); aqui eles
são simplesmente numerados de 1 a 53, na ordem. O original não tem títulos: os títulos em português são do Sola.

Uso (o HTML baixado fica em ferramentas/fontes/1644/, fora do git; o host reformedreader.org precisa estar
liberado na rede do ambiente):
    python3 ferramentas/confissao_1644.py
O português (campos "titulo" e "pt") é a tradução do Sola, feita na sessão do agente sem API, e é preservado quando o
importador roda de novo; enquanto não houver tradução, fica só o inglês. Depois: python3 ferramentas/gerar_paginas.py"""
import html, json, re, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from confissoes import DESTINO, OSIS, bl, converter                # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "ferramentas" / "fontes" / "1644" / "1644lbc.htm"
URL = "https://www.reformedreader.org/ccc/1644lbc.htm"
ARQUIVO = DESTINO / "confissao-batista-1644.json"
LIVROS = {   # abreviações das notas de 1644 -> OSIS
    "Gen": "Gen", "Ex": "Exod", "Num": "Num", "Deut": "Deut", "Job": "Job", "Psa": "Ps", "Psalm": "Ps",
    "Prov": "Prov", "Ecc": "Eccl", "Cant": "Song", "Song": "Song", "Isa": "Isa", "Jer": "Jer", "Ezek": "Ezek",
    "Dan": "Dan", "Mal": "Mal", "Matt": "Matt", "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts",
    "Rom": "Rom", "1 Cor": "1Cor", "2 Cor": "2Cor", "1 Co": "1Cor", "Gal": "Gal", "Eph": "Eph", "Phil": "Phil",
    "Col": "Col", "1 Thess": "1Thess", "2 Thess": "2Thess", "1 Tim": "1Tim", "2 Tim": "2Tim", "Titus": "Titus",
    "Heb": "Heb", "1 Pet": "1Pet", "2 Pet": "2Pet", "1 John": "1John", "Jude": "Jude", "Rev": "Rev"}
RE_LIVRO = re.compile(r"\b(" + "|".join(sorted((re.escape(k) for k in LIVROS), key=len, reverse=True)) + r")\b\.?\s*")
# erros de impressão ou de transcrição nas notas (texto da nota -> texto corrigido)
CORRECOES = {"Acts 2;41, 47": "Acts 2:41, 47", "Rev. 2;10": "Rev. 2:10", "Gal. 19, 20 [sic]": "Gal. 2:19, 20",
             "Titus 3. [sic]": "Titus 3:1", "Rom. 12: 1, 8": "Rom. 12:1, 8", "Isa. 44:67": "Isa. 44:6, 7",
             "Co. 2:3": "Col. 2:3", "Esa. [sic] 44:10": "Isa. 44:10", "Ecc. 7:31": "Ecc. 7:29",
             "Col. 21: 18, 23 [sic]": "Col. 2:18, 23", "Dan. 7;13": "Dan. 7:13", "Isa. 53;3-5": "Isa. 53:3-5",
             "Job 17:2 with 6, 37": "Job 17:2, 6", "1 Cor. 15:58-59": "1 Cor. 15:58", "Jude vs. 4": "Jude v. 4",
             "Job chaps 1": "Job chaps. 1"}


def baixar():
    if not FONTE.exists():
        FONTE.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Sola; importador)"})
        FONTE.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    return FONTE.read_text(encoding="latin-1")


def texto_puro(s):
    s = re.sub(r'<a href="[^"]*bc1644\.htm#(\d+)">\s*\d+\s*</a>', r" [\1] ", s)    # chamadas das notas -> [n]
    s = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S | re.I)
    s = re.sub(r"<br\s*/?>|</p>|</h\d>", "\n", s, flags=re.I)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    s = re.sub(r"[ \t\r]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n\n", s)


def junta(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,.;:)])", r"\1", s)
    return re.sub(r"\[(\d+)\](?=\w)", r"[\1] ", s)


def osis(nota, biblia, problemas):
    """"1 Tim. 6:3, 13, 14; Gal. 1:8, 9; John chap. 14" -> ["1Tim.6.3", "1Tim.6.13-1Tim.6.14", ...]"""
    nota = nota.strip().rstrip(".")
    for de, para in CORRECOES.items():
        nota = nota.replace(de.rstrip("."), para)
    nota = re.sub(r"\s+with\s+", "; ", nota)
    partes, livro, cap = [], None, None
    for trecho in re.split(r";", nota):
        trecho = trecho.strip()
        m = RE_LIVRO.match(trecho)
        if m:
            livro, trecho = LIVROS[m.group(1)], trecho[m.end():]
        if not livro or not trecho:
            problemas.append(f"nota não entendida: {nota}")
            continue
        if mc := re.fullmatch(r"chaps?\.\s*(\d+)(?:\s*and\s*(\d+))?", trecho):            # capítulo(s) inteiro(s)
            partes += [f"{livro}.{c}" for c in mc.groups() if c]
            continue
        if mv := re.fullmatch(r"v\.\s*([\d,\s\-]+)", trecho):                              # Judas, um só capítulo
            trecho = "1:" + mv.group(1)
        if ":" in trecho:
            cap, trecho = trecho.split(":", 1)
            cap = int(cap)
        elif cap is None:
            problemas.append(f"nota sem capítulo: {nota}")
            continue
        if "to the end" in trecho:                                                       # "12:12 to the end"
            caps = biblia.get(OSIS[livro], [])
            trecho = trecho.replace("to the end", f"-{len(caps[cap - 1]) if cap <= len(caps) else 0}")
        for vs in trecho.split(","):
            n = re.findall(r"\d+", vs)
            if not n:
                continue
            a, b = int(n[0]), int(n[-1])
            partes.append(f"{livro}.{cap}.{a}" + (f"-{livro}.{cap}.{b}" if b != a else ""))
    return partes


def main():
    biblia, problemas = bl(), []
    t = texto_puro(baixar())
    ini = t.index("which are commonly (though falsely) called ANABAPTISTS.")
    notas_ini = t.index("[1] 1 Tim. 6:16")
    corpo = t[ini:notas_ini]
    corpo = corpo[:corpo.index("[149]") + len("[149]")]                 # o fim: as citações depois do artigo LIII saem
    cabecas = list(re.finditer(r"\n\s*[IVXL]+\.?(?:\s*\[sic\])?\s*\n", corpo))
    artigos = [junta(corpo[c.end():(cabecas[i + 1].start() if i + 1 < len(cabecas) else len(corpo))])
               for i, c in enumerate(cabecas)]
    assert len(artigos) == 53, len(artigos)
    fim_notas = re.search(r"\n\s*Home\s", t[notas_ini:]).start() + notas_ini
    pedacos = re.split(r"\[(\d+)\]\s*", re.sub(r"\s+", " ", t[notas_ini:fim_notas]))
    notas = {pedacos[k]: pedacos[k + 1].strip() for k in range(1, len(pedacos), 2)}
    assert sorted(map(int, notas)) == list(range(1, 150)), "notas faltando"
    antigo = json.loads(ARQUIVO.read_text(encoding="utf-8")) if ARQUIVO.exists() else {}
    antigas = {p["n"]: p for p in antigo.get("partes", [])}
    partes = []
    for i, en in enumerate(artigos, 1):
        n = str(i)
        provas = {}
        for k in re.findall(r"\[(\d+)\]", en):
            refs = []
            for o in osis(notas[k], biblia, problemas):
                refs += converter(o, biblia, problemas)
            provas[k] = refs
        velho = antigas.get(n, {})
        item_velho = (velho.get("itens") or [{}])[0]
        item = {"n": "1", "en": en, "provas": provas}
        if item_velho.get("pt"):
            if sorted(re.findall(r"\[\d+\]", item_velho["pt"])) != sorted(re.findall(r"\[\d+\]", en)):
                problemas.append(f"artigo {n}: as marcas [n] do português não batem com as do inglês")
            item["pt"] = item_velho["pt"]
        parte = {"n": n, "titulo_en": f"Article {n}"}
        if velho.get("titulo"):
            parte["titulo"] = velho["titulo"]
        parte["itens"] = [item]
        partes.append(parte)
    doc = {"id": "confissao-batista-1644", "titulo": "Primeira Confissão de Fé Batista de Londres",
           "titulo_en": "The First London Baptist Confession of Faith", "ano": 1644, "tipo": "confissao",
           "fonte": "The Confession of Faith of those Churches which are commonly (though falsely) called Anabaptists "
                    "(Londres, 1644), domínio público, com as notas de margem do original. Transcrição do The Reformed "
                    "Reader: " + URL,
           "partes": partes}
    ARQUIVO.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    nprovas = sum(len(r) for p in partes for r in p["itens"][0]["provas"].values())
    print(f"{len(partes)} artigos, {sum(len(p['itens'][0]['provas']) for p in partes)} notas, {nprovas} referências, "
          f"{sum(1 for p in partes if p['itens'][0].get('pt'))} traduzidos")
    for p in problemas:
        print("  ⚠", p)


if __name__ == "__main__":
    main()
