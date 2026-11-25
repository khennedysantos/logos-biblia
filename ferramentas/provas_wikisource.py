"""Textos de prova que faltavam, tirados do Wikisource (domínio público):

- Catecismo de Heidelberg: a edição de 1879 da Reformed Church in America "com os textos de prova" (E. R. Good & Bro.,
  Tiffin, Ohio), transcrita e revisada no Wikisource a partir do escaneamento do Internet Archive
  (heidelbergcatech00refo). Cada pergunta traz as referências entre parênteses na resposta e, abaixo, mais versículos.
- Confissão Batista de Londres de 1689: a página "1689 Baptist Confession of Faith", com as referências de cada
  parágrafo (as da edição original, reunidas no fim do parágrafo).

O texto dessas edições difere do inglês que o Sola traduziu (o Heidelberg é o de 1863, de Schaff; a 1689, a do
Creeds.json), então as provas não têm marcadores [n] no texto: entram como um grupo só, "1", por pergunta ou
parágrafo, e aparecem na lista de provas, na Estante e nas páginas de versículo. O texto traduzido não é tocado.

Uso (as páginas baixadas ficam em ferramentas/fontes/wikisource/, fora do git; en.wikisource.org precisa estar
liberado na rede do ambiente). Rode depois de confissoes.py e confissoes_ccel.py, que zeram as provas ao reimportar:
    python3 ferramentas/provas_wikisource.py
Depois: python3 ferramentas/gerar_paginas.py"""
import json, re, sys, urllib.parse, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from confissoes import DESTINO, bl, converter                      # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "ferramentas" / "fontes" / "wikisource"
WS = "https://en.wikisource.org/w/index.php?action=raw&title="
PAGINAS_HC = "Page:The_Heidelberg_catechism.._(IA_heidelbergcatech00refo).pdf/{}"
PAGINA_1689 = "1689_Baptist_Confession_of_Faith"
NOMES = {   # nomes e abreviações das duas fontes -> OSIS
    "Gen": "Gen", "Genesis": "Gen", "Ex": "Exod", "Exod": "Exod", "Exodus": "Exod", "Lev": "Lev", "Leviticus": "Lev",
    "Num": "Num", "Numbers": "Num", "Deut": "Deut", "Deuteronomy": "Deut", "Josh": "Josh", "Joshua": "Josh",
    "Judg": "Judg", "Judges": "Judg", "Ruth": "Ruth", "1 Sam": "1Sam", "1 Samuel": "1Sam", "2 Sam": "2Sam",
    "2 Samuel": "2Sam", "1 Kings": "1Kgs", "2 Kings": "2Kgs", "1 Chron": "1Chr", "1 Chronicles": "1Chr",
    "2 Chron": "2Chr", "2 Chronicles": "2Chr", "Ezra": "Ezra", "Neh": "Neh", "Nehemiah": "Neh", "Esther": "Esth",
    "Job": "Job", "Ps": "Ps", "Psa": "Ps", "Psalm": "Ps", "Psalms": "Ps", "Prov": "Prov", "Proverbs": "Prov",
    "Ecc": "Eccl", "Eccl": "Eccl", "Ecclesiastes": "Eccl", "Song of Solomon": "Song", "Canticles": "Song",
    "Isa": "Isa", "Isaiah": "Isa", "Jer": "Jer", "Jeremiah": "Jer", "Lam": "Lam", "Lamentations": "Lam",
    "Ezek": "Ezek", "Ezekiel": "Ezek", "Dan": "Dan", "Daniel": "Dan", "Hos": "Hos", "Hosea": "Hos", "Joel": "Joel",
    "Amos": "Amos", "Micah": "Mic", "Nahum": "Nah", "Hab": "Hab", "Habakkuk": "Hab", "Zech": "Zech",
    "Zechariah": "Zech", "Mal": "Mal", "Malachi": "Mal", "Matt": "Matt", "Math": "Matt", "Matthew": "Matt",
    "Mark": "Mark", "Luke": "Luke", "John": "John", "Acts": "Acts", "Rom": "Rom", "Romans": "Rom",
    "1 Cor": "1Cor", "1 Corinthians": "1Cor", "2 Cor": "2Cor", "2 Corinthians": "2Cor", "Gal": "Gal",
    "Galatians": "Gal", "Eph": "Eph", "Ephesians": "Eph", "Phil": "Phil", "Philippians": "Phil", "Col": "Col",
    "Colossians": "Col", "1 Thess": "1Thess", "1 Thes": "1Thess", "1 Thessalonians": "1Thess", "2 Thess": "2Thess",
    "2 Thes": "2Thess", "2 Thessalonians": "2Thess", "1 Tim": "1Tim", "1 Timothy": "1Tim", "2 Tim": "2Tim",
    "2 Timothy": "2Tim", "Titus": "Titus", "Tit": "Titus", "Philemon": "Phlm", "Heb": "Heb", "Hebrews": "Heb",
    "James": "Jas", "1 Pet": "1Pet", "1 Peter": "1Pet", "2 Pet": "2Pet", "2 Peter": "2Pet", "1 John": "1John",
    "2 John": "2John", "3 John": "3John", "Jude": "Jude", "Rev": "Rev", "Revelation": "Rev"}
RE_REF = re.compile(r"\b(" + "|".join(sorted((re.escape(k) for k in NOMES), key=len, reverse=True)) +
                    r")\b\.?\s*(\d+)(?:\s*[;:]\s*|\.)(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)")
# erros de impressão ou de transcrição nas fontes (texto -> texto corrigido)
CORRECOES = {"Psalms 76;10": "Psalms 76:10", "Matt. 29;41": "Matt. 25;41", "Acts 22;38": "Acts 2;38",
             "Mark 16;46": "Mark 16;16", "2 John 10;11": "2 John 1;10, 11", "Ezra 18;13": "Ezek. 18;13",
             "—Ps. 50;53.": "—", "Genesis 1:20; Isaiah 10": "Genesis 50:20; Isaiah 10", "Psalms 1:21": "Psalms 50:21"}
RE_CONTINUA = re.compile(r"\s*;\s*(\d+):(\d+(?:\s*[-–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-–]\s*\d+)?)*)")
# livros de um capítulo só, citados só com o versículo ("Jude 6, 7")
RE_UM_CAPITULO = re.compile(r"\b(Jude|2 John|3 John|Philemon)\s+(\d+(?:\s*,\s*\d+)*)(?![:;]\d)")


def baixar(titulo):
    arq = FONTES / (re.sub(r"[^\w.-]+", "_", titulo) + ".txt")
    if not arq.exists():
        FONTES.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(WS + urllib.parse.quote(titulo), headers={"User-Agent": "Mozilla/5.0 (Sola)"})
        arq.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    return arq.read_text(encoding="utf-8")


def refs(texto, biblia, problemas, sem_capitulo=False):
    """todas as referências do trecho, convertidas para o formato do Sola, sem repetir"""
    texto = re.sub(r"''+", "", texto)
    for de, para in CORRECOES.items():
        texto = texto.replace(de, para)
    saida = []
    texto = RE_UM_CAPITULO.sub(r"\1 1:\2", texto)
    def guardar(livro, cap, versos):
        for vs in versos.split(","):
            n = re.findall(r"\d+", vs)
            osis = f"{livro}.{cap}.{n[0]}" + (f"-{livro}.{cap}.{n[-1]}" if n[-1] != n[0] else "")
            for r in converter(osis, biblia, problemas):
                ult = saida[-1] if saida else None
                if ult and len(r) == len(ult) == 4 and r[:2] == ult[:2] and ult[3] and r[2] == ult[3] + 1:
                    ult[3] = r[3]                        # versículos seguidos: "João 10:28, 29" -> 10:28-29
                elif r not in saida:
                    saida.append(r)
    for m in RE_REF.finditer(texto):
        livro = NOMES[m.group(1)]
        guardar(livro, m.group(2), m.group(3))
        j = m.end()
        while c := RE_CONTINUA.match(texto, j):          # "II Tim. 1:13; 3:16": o "3:16" é do mesmo livro
            guardar(livro, c.group(1), c.group(2))
            j = c.end()
    unicas = []
    for r in saida:                                      # a fusão pode repetir uma referência que já estava antes
        if r not in unicas:
            unicas.append(r)
    return unicas


def heidelberg(biblia, problemas):
    texto = ""
    for n in range(5, 85):
        texto += re.sub(r"<noinclude>.*?</noinclude>", "", baixar(PAGINAS_HC.format(n)), flags=re.S) + "\n"
    # "{{*}}4. ''Pergunta?''", "''Question'' 1.—''…''" e "35 ''…''" (sem o ponto)
    cabecas = list(re.finditer(r"^(?:\{\{\*\}\})?\s*(?:''Question''\s*)?(\d+)\.?\s*(?:—\s*)?''", texto, flags=re.M))
    por_pergunta, anterior = {}, 0
    for i, c in enumerate(cabecas):
        fim = cabecas[i + 1].start() if i + 1 < len(cabecas) else len(texto)
        n = int(c.group(1))
        if n == anterior:                                # a edição imprime 73 duas vezes; a segunda é a 74
            n += 1
        anterior = n
        por_pergunta[str(n)] = refs(texto[c.end():fim], biblia, problemas)
    assert sorted(map(int, por_pergunta)) == list(range(1, 130)), "esperava as perguntas 1 a 129"
    return por_pergunta


def batista_1689(biblia, problemas):
    por_secao, cap, sec = {}, None, None
    for linha in baixar(PAGINA_1689).splitlines():
        linha = linha.strip()
        if m := re.match(r"==\s*Chapter (\d+)", linha):
            cap, sec = m.group(1), None
        elif cap and not sec and linha and not linha.startswith("("):
            sec = "1"                                    # capítulo de um parágrafo só, sem número (o 12)
        elif cap and (m := re.match(r"(\d+)\.\s", linha)):
            sec = m.group(1)
        elif cap and sec and linha.startswith("("):
            por_secao.setdefault((cap, sec), []).extend(
                r for r in refs(linha, biblia, problemas) if r not in por_secao.get((cap, sec), []))
    return por_secao


def main():
    biblia, problemas = bl(), []
    arq = DESTINO / "heidelberg.json"
    doc = json.loads(arq.read_text(encoding="utf-8"))
    provas = heidelberg(biblia, problemas)
    for q in doc["itens"]:
        q["provas"] = {"1": provas[q["n"]]} if provas[q["n"]] else {}
    arq.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Heidelberg: {sum(1 for q in doc['itens'] if q['provas'])} perguntas com provas, "
          f"{sum(len(v) for q in doc['itens'] for v in q['provas'].values())} referências")

    arq = DESTINO / "confissao-batista-1689.json"
    doc = json.loads(arq.read_text(encoding="utf-8"))
    provas = batista_1689(biblia, problemas)
    usadas = 0
    for parte in doc["partes"]:
        for it in parte["itens"]:
            lista = provas.get((parte["n"], it["n"]), [])
            it["provas"] = {"1": lista} if lista else {}
            usadas += bool(lista)
    faltam = [f"{c}.{s}" for c, s in provas if not any(p["n"] == c and any(i["n"] == s for i in p["itens"])
                                                       for p in doc["partes"])]
    if faltam:
        problemas.append(f"1689: parágrafos do Wikisource que não existem no Sola: {faltam}")
    arq.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    total = sum(len(p["itens"]) for p in doc["partes"])
    print(f"1689: {usadas} de {total} parágrafos com provas, "
          f"{sum(len(v) for p in doc['partes'] for i in p['itens'] for v in i['provas'].values())} referências")
    for p in problemas:
        print("  ⚠", p)


if __name__ == "__main__":
    main()
