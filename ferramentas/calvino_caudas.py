"""Tira do comentário de Calvino (data/commentaries/calvin/) o texto que a edição da CCEL deixou colado no último
versículo de um capítulo:

  - o cabeçalho do capítulo seguinte com o texto bíblico dele ("CHAPTER 12 1 Corinthians 12:1-7 1. Now concerning…",
    em inglês e latim; no português, "CAPÍTULO 12", a tradução dos versículos e o latim), que aparecia no fim do último
    versículo de ~300 capítulos — o comentário desses versículos já está no arquivo do capítulo seguinte;
  - no inglês, os apêndices do fim de cada volume ("END OF THE COMMENTARIES…", "A TRANSLATION OF CALVIN'S VERSION OF…",
    prefácios e índices do livro seguinte), que a tradução para o português já deixava de fora (limpar_calvino, em
    tradutor/calvino_llm.py).

Os Salmos ficam de fora: lá o comentário de cada salmo inteiro está repetido em todos os versículos, e o problema é outro.
O script é idempotente e só corta quando o resto do texto continua do tamanho esperado.

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
# título da preleção seguinte ("Lecture Forty-Second", "Quadragésima Segunda Preleção"), que também ficaria solto
PRELECAO_EN = re.compile(r"\s*Lecture [A-Za-z -]+\.?$")
PRELECAO_PT = re.compile(r"\s*(?:[A-Za-zÀ-ú-]+ ){1,5}(?:Preleção|Lição)\.?$", re.I)


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
        if livro in ("pt", "PSA") or not livro.isupper():
            continue
        en, arq_pt = ler(arq), BASE / "pt" / livro / arq.name
        pt = ler(arq_pt)
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
