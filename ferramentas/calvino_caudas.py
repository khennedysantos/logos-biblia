"""Tira do comentário de Calvino (data/commentaries/calvin/) o texto que a edição da CCEL deixou colado no último
versículo de um capítulo:

  - o cabeçalho do capítulo seguinte com o texto bíblico dele ("CHAPTER 12 1 Corinthians 12:1-7 1. Now concerning…",
    em inglês e latim; no português, "CAPÍTULO 12", a tradução dos versículos e o latim), que aparecia no fim do último
    versículo de ~300 capítulos — o comentário desses versículos já está no arquivo do capítulo seguinte;
  - no inglês, os apêndices do fim de cada volume ("END OF THE COMMENTARIES…", "A TRANSLATION OF CALVIN'S VERSION OF…",
    prefácios e índices do livro seguinte), que a tradução para o português já deixava de fora (limpar_calvino, em
    tradutor/calvino_llm.py).

  - dentro dos capítulos, o cabeçalho e o texto bíblico da seção seguinte ("1 Corinthians 13:4-8 4. Charity suffereth
    long… 4. Caritas patiens est…"; no português, "1 Coríntios 13:4-8", a tradução e o latim), colados no fim do último
    versículo comentado da seção anterior — o comentário deles começa na chave do primeiro versículo da seção; só corta
    quando o que vem depois do cabeçalho em português é texto bíblico (versículos numerados, latim, outras referências),
    e não toca nos poucos casos em que vem junto a introdução da seção (MANTER).

Os livros refeitos da CCEL por calvino_ccel.py (Salmos, Pastorais, Zacarias, Malaquias) já vêm sem nada disso.
O script é idempotente e só corta quando o resto do texto continua do tamanho esperado nos dois idiomas.

uso:  python3 ferramentas/calvino_caudas.py [--conferir]"""
import json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "data" / "commentaries" / "calvin"
FIM_VOLUME = re.compile(r"\s*(?:END OF (?:THE )?(?:COMMENTAR|EPISTLE|BOOK|VOLUME)|End [Oo]f (?:the )?(?:Prophecies|[Cc]ommentar)"
                        r"|The addenda to|(?i:A TRANSLATION OF CALVIN))")
# frase de passagem antes do cabeçalho ("Segue-se agora —", "Now follows —"), que fica sem sentido sozinha
PASSAGEM_PT = re.compile(r"\s*(?:(?:Segue(?:-se)?|Em seguida vem)(?: agora| então)?,?(?: outra profecia| uma oração| o)?:?\s*—?\s*)$")
PASSAGEM_EN = re.compile(r"\s*(?:(?:(?:Now |There |It |Then )?follows?(?: now)?(?: another prophecy| a prayer)?|Let us (?:go on|proceed))[,:]?\s*—?\s*)$", re.I)
NOVOS = {"PSA", "1TI", "2TI", "TIT", "ZEC", "MAL"}                  # refeitos da CCEL por calvino_ccel.py
# seções em que depois do texto bíblico vem a introdução de Calvino à seção seguinte: ficam como estão
MANTER = {("DAN", 8, "21"), ("EXO", 23, "24"), ("MAT", 23, "18"), ("MAT", 23, "11"), ("MAT", 26, "65"),
          ("MAT", 27, "55")}
VERSO_PT = re.compile(r"^(?:\*?\d+\s?[.,:]?\s|\*|(?:[1-3] )?[A-ZÀ-Ú][\wçãéíóúâêôõ ]+,?(?: capítulo)? \d+(?::\d+)?)")
LATIM = re.compile(r"\b(?:et|est|quod|qui|quae|non|ad|in|sed|enim|vel|nos|vos|eius|ejus|autem)\b")
# título da preleção seguinte ("Lecture Forty-Second", "Quadragésima Segunda Preleção"), que também ficaria solto
PRELECAO_EN = re.compile(r"\s*Lecture [A-Za-z -]+\.?$")
PRELECAO_PT = re.compile(r"\s*(?:(?:[A-Za-zÀ-ú-]+ ){1,5}(?:Preleção|Lição|Palestra|Conferência)|(?:Preleção|Lição|Palestra|Conferência)(?: [A-Za-zÀ-ú-]+){1,5})\.?$", re.I)


def cabecalho_en(n):
    """"CHAPTER 12 1 Corinthians 12:1-7", "CHAPTER 5 Lecture Seventeeth Lamentations 5:1", "CHAPTER 16 Ezekiel 16: 1",
    "CHAPTER 2 In this second chapter…" (a introdução do capítulo, que vai para o v. 1 dele) ou "CHAPTER 2" no fim"""
    return re.compile(r"\s*CHAPTER " + str(n) + r"\.?(?:\s*$|\s+(?P<intro>[A-Z](?:(?!CHAPTER).){100,}?)?\s*"
                      r"(?:Lecture [A-Za-z -]+?\.?\s+)?(?:[1-3] )?[A-Z][a-z]+(?: of [A-Z][a-z]+)?(?: Chapter)? "
                      + str(n) + r":\s?\d)", re.S)


def cabecalho_pt(n):
    return re.compile(r"\s*CAP[ÍI]TULO " + str(n) + r"\b\.?")


def corte_en(texto, cap):
    """(posição do corte, introdução do capítulo seguinte ou None)"""
    fim, cab = FIM_VOLUME.search(texto), cabecalho_en(cap + 1).search(texto)
    achados = [(m.start(), m) for m in (fim, cab) if m and m.start() > 0]
    if not achados:
        return None, None
    pos, m = min(achados, key=lambda x: x[0])
    return pos, (m.group("intro") if m is cab and m.group("intro") else None)


def cortar(texto, pos, passagem, prelecao):
    cabeca = texto[:pos].rstrip()
    return passagem.sub("", prelecao.sub("", cabeca).rstrip()).rstrip()


def secao_pt(cap):
    """linha com o cabeçalho de uma seção deste capítulo: "1 Coríntios 13:4-8", "Hebreus, capítulo 8:1-6" """
    return re.compile(r"\n\n(?:[1-3] )?[A-ZÀ-Ú][\wçãéíóúâêôõ]+(?: [a-zà-ú]+ [A-ZÀ-Ú][\wçã]+)?,?(?: capítulo)? "
                      + str(cap) + r":(\d+)(?:\s?[-–,]\s?\d+)?[^\n]{0,30}\n")


def so_texto_biblico(cauda):
    """o que vem depois do cabeçalho é só texto bíblico: versículos numerados, outras referências, latim, linhas curtas"""
    for par in (p.strip() for p in cauda.split("\n") if p.strip()):
        if not (VERSO_PT.match(par) or len(par) < 90 or len(LATIM.findall(par)) >= 3):
            return False
    return True


SEG = re.compile(r"(?:^|(?<=[\s.;:,”\"’)\]]))\*?(\d+)\s?[.,]\s")
# a última frase só anunciava o texto bíblico que saiu: "It follows, —", "Let us now proceed —", "Segue-se:", "Prossigamos —"
ANUNCIO_EN = re.compile(r"(?<=[.?!”)\]])\s*(?:(?:For |And |But )?(?:it|It|there|There) (?:now )?follows?|(?:Now|Then) follows?|"
                        r"Let us (?:now )?(?:go on|proceed)|We (?:now )?proceed|He (?:now |afterwards |then |therefore )?(?:adds|subjoins))"
                        r"[^.?!—]{0,25}?[,:.]?\s*—?\s*$")
ANUNCIO_PT = re.compile(r"(?<=[.?!”)\]])\s*(?:(?:Pois |E |Mas )?se segue|Segue(?:-se)?|Prossigamos|Em seguida vem|Vem a seguir|"
                        r"(?:Por fim |Em seguida |Depois |Então |Agora )?(?:ele )?acrescenta)(?: agora| então| depois)?[^.?!—]{0,25}?"
                        r"[,:.]?\s*—?\s*$")


def cauda_en(texto, cap):
    """onde começa, no inglês, o cabeçalho + texto bíblico da seção seguinte no fim do versículo: (posição, números, 1º v.)"""
    for m in re.finditer(r"\s(?:[A-Z]{3,}(?: [A-Z]+)* \d+:\d+(?:\s?[-–]\s?\d+)?[;,]?\s+)*(?:[1-3] )?[A-Z][a-z]+(?: of [A-Za-z]+)?,?"
                         r"(?: Chapter)? " + str(cap) + r":(\d+)(?:\s?[-–]\s?\d+)?\s+\1\.\s", texto):
        cauda = texto[m.start():]
        segs = re.split(r"\s(?=\d+\.\s)", cauda)
        if len(cauda) < 8000 and len(segs) >= 2 and all(len(s) < 900 for s in segs[1:]):
            return m.start(), {int(x) for x in re.findall(r"(?:^|\s)(\d+)\.\s", cauda)}, m.group(1)
    return None, None, None


def cauda_pt(texto, cap, primeiro, nums):
    """no português, a referência da seção ("1 Coríntios 7:6-9") perto do fim, seguida só dos versículos dela"""
    janela = max(0, len(texto) - 12000)
    refs = list(re.finditer(r"(?:[1-3] )?[A-ZÀ-Ú][\wçãéíóúâêôõ]+(?: [a-zà-ú]+ [A-ZÀ-Ú][\wçã]+)?,?(?: capítulo)? " + str(cap) + ":"
                            + primeiro + r"(?:\s?[-–]\s?\d+)?(?:,\s?\d+(?:\s?[-–]\s?\d+)?)*\.?", texto[janela:]))
    for r in reversed(refs):
        resto = texto[janela + r.end():].strip(" \n—–-:")
        partes = list(SEG.finditer(resto))
        if not partes or partes[0].start() > 80:
            continue
        fins = [p.start() for p in partes[1:]] + [len(resto)]
        if all(int(p.group(1)) in nums and f - p.start() < 900 for p, f in zip(partes, fins)):
            return janela + r.start()
    return None


def fechar(texto):
    """"…o que se segue:" -> "…o que se segue." quando o que ele anunciava saiu"""
    sem = ANUNCIO_PT.sub("", ANUNCIO_EN.sub("", texto)).rstrip()
    if len(sem) > 40:
        texto = sem
    return re.sub(r"[\s:,;—–-]+$", ".", texto) if re.search(r"[:,;—–-]$", texto) else texto


def cortar_secoes(livro, cap, en, pt, avisos):
    mudou = False
    for k, tp in list(pt.items()):
        t = en.get(k)
        if not isinstance(tp, str) or not t or (livro, cap, k) in MANTER:
            continue
        m = secao_pt(cap).search(tp)
        if not m or m.start() < 40 or not so_texto_biblico(tp[m.end():]):
            pe, nums, primeiro = cauda_en(t, cap)               # pelo inglês: o cabeçalho e os versículos que ele traz
            pp = cauda_pt(tp, cap, primeiro, nums) if pe else None
            if pp and pe > 40 and 0.75 < pp / pe < 1.35:
                en[k] = fechar(cortar(t, pe, PASSAGEM_EN, PRELECAO_EN))
                pt[k] = fechar(cortar(tp, pp, PASSAGEM_PT, PRELECAO_PT))
                mudou = True
            continue
        a = m.group(1)
        esperado = m.start() * len(t) / len(tp)
        cands = [c.start() for c in re.finditer(r"\s(?:[1-3] )?[A-Z][a-z]+(?: of [A-Za-z]+)?,?(?: Chapter)? "
                                                + str(cap) + ":" + a + r"\b", t)]
        if not cands:
            avisos.append(f"{livro} {cap}:{k}: seção {cap}:{a} sem o cabeçalho no inglês; ficou como está")
            continue
        pos = min(cands, key=lambda c: abs(c - esperado))
        antes = re.search(r"\s[A-Z]{3,}(?: [A-Z]+)* \d+:\d+(?:\s?[-–]\s?\d+)?\s*$", t[:pos])   # "MATTHEW 2:7-12 Matthew 2:7-12"
        if antes:
            pos = antes.start()
        if pos < 40 or not 0.75 < m.start() / pos < 1.35:
            avisos.append(f"{livro} {cap}:{k}: corte da seção {cap}:{a} fora do lugar; ficou como está")
            continue
        en[k] = fechar(cortar(t, pos, PASSAGEM_EN, PRELECAO_EN))
        pt[k] = fechar(cortar(tp, m.start(), PASSAGEM_PT, PRELECAO_PT))
        mudou = True
    return mudou


HARMONIA = re.compile(r"\s*(?:[A-ZÁÊÚ]{3,}(?: [A-ZÁÊÚ]+)* \d+:\d+(?:\s?[-–]\s?\d+)?(?:[;,]\s?\d+(?::\d+)?(?:\s?[-–]\s?\d+)?)*[;,]?\s*)+\.?$")


def arrumar_final(texto, prelecao):
    """título solto no fim do versículo: a preleção seguinte ou o cabeçalho da harmonia ("MATTHEW 3:11-12; MARK 1:7-8.")"""
    novo = texto
    for _ in range(3):
        novo = HARMONIA.sub("", prelecao.sub("", novo)).rstrip()
    sem = ANUNCIO_PT.sub("", ANUNCIO_EN.sub("", novo)).rstrip()
    if len(sem) > 40:
        novo = sem
    novo = re.sub(r"[:;,]\.$", ".", novo)
    if re.search(r"[:;,—–]$", novo):
        novo = re.sub(r"[\s:;,—–-]+$", ".", novo)
    return novo if len(novo) > 40 else texto


def main():
    conferir = "--conferir" in sys.argv
    arquivos, avisos = {}, []

    def ler(arq):
        if arq not in arquivos:
            arquivos[arq] = json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else {}
        return arquivos[arq]

    originais = {}
    for arq in sorted(BASE.glob("*/*.json")):
        livro, cap = arq.parent.name, int(arq.stem)
        if livro == "pt" or livro in NOVOS or not livro.isupper():
            continue
        en, arq_pt = ler(arq), BASE / "pt" / livro / arq.name
        pt = ler(arq_pt)
        antes = (json.dumps(en, sort_keys=True), json.dumps(pt, sort_keys=True))
        mexeu = cortar_secoes(livro, cap, en, pt, avisos)
        for d, prelecao in ((en, PRELECAO_EN), (pt, PRELECAO_PT)):
            for k, v in d.items():
                if isinstance(v, str) and arrumar_final(v, prelecao) != v:
                    d[k], mexeu = arrumar_final(v, prelecao), True
        if mexeu:
            originais.setdefault(arq, antes[0])
            originais.setdefault(arq_pt, antes[1])
        for k, t in list(en.items()):
            pos, intro = corte_en(t, cap)
            if pos is None:
                continue
            tp = pt.get(k, "")
            m = cabecalho_pt(cap + 1).search(tp)
            if m and m.start() > 0 and not 0.8 < m.start() / pos < 1.3:   # o comentário que fica tem o mesmo tamanho
                avisos.append(f"{livro} {cap}:{k}: corte do português fora do lugar; ficou como está")
                continue
            for a in (arq, arq_pt):
                originais.setdefault(a, json.dumps(ler(a), sort_keys=True))
            en[k] = cortar(t, pos, PASSAGEM_EN, PRELECAO_EN)
            if m and m.start() > 0:
                pt[k] = cortar(tp, m.start(), PASSAGEM_PT, PRELECAO_PT)
            if intro:                                     # a introdução do capítulo seguinte vai para o v. 1 dele
                prox_en, prox_pt = BASE / livro / f"{cap + 1}.json", BASE / "pt" / livro / f"{cap + 1}.json"
                intro_pt = re.split(r"\n\s*(?:[1-3] )?[A-ZÀ-Ú][a-zà-ú]+ " + str(cap + 1) + r":\d", tp[m.end():])[0].strip()
                for a in (prox_en, prox_pt):
                    originais.setdefault(a, json.dumps(ler(a), sort_keys=True))
                ler(prox_en)["1"] = intro.strip() + " " + ler(prox_en).get("1", "")
                ler(prox_pt)["1"] = intro_pt + "\n\n" + ler(prox_pt).get("1", "")
    mudou = [a for a, txt in originais.items() if json.dumps(arquivos[a], sort_keys=True) != txt]
    if not conferir:
        for destino in mudou:
            bruto = destino.read_text(encoding="utf-8")
            ind = 1 if bruto.startswith("{\n") else None
            saida = json.dumps(arquivos[destino], ensure_ascii=False, indent=ind, separators=None if ind else (",", ":"))
            destino.write_text(saida + ("\n" if bruto.endswith("\n") else ""), encoding="utf-8")
    print(f"{len(mudou)} arquivos {'mudariam' if conferir else 'gravados'}")
    for a in avisos:
        print("  ⚠", a)


if __name__ == "__main__":
    main()
