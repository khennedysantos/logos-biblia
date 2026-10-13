"""Gera data/crossrefs/ a partir do cross_references.txt do openbible.info (CC-BY).
uso: python3 ferramentas/gerar_crossrefs.py cross_references.txt data/crossrefs
Fonte: https://raw.githubusercontent.com/neuu-org/bible-crossrefs-dataset/main/data/00_raw/openbible/cross_references.txt"""
import json, sys
from collections import defaultdict
from pathlib import Path
SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OB = {"Gen":"GEN","Exod":"EXO","Lev":"LEV","Num":"NUM","Deut":"DEU","Josh":"JOS","Judg":"JDG","Ruth":"RUT","1Sam":"1SA","2Sam":"2SA","1Kgs":"1KI","2Kgs":"2KI","1Chr":"1CH","2Chr":"2CH","Ezra":"EZR","Neh":"NEH","Esth":"EST","Job":"JOB","Ps":"PSA","Prov":"PRO","Eccl":"ECC","Song":"SNG","Isa":"ISA","Jer":"JER","Lam":"LAM","Ezek":"EZK","Dan":"DAN","Hos":"HOS","Joel":"JOL","Amos":"AMO","Obad":"OBA","Jonah":"JON","Mic":"MIC","Nah":"NAM","Hab":"HAB","Zeph":"ZEP","Hag":"HAG","Zech":"ZEC","Mal":"MAL","Matt":"MAT","Mark":"MRK","Luke":"LUK","John":"JHN","Acts":"ACT","Rom":"ROM","1Cor":"1CO","2Cor":"2CO","Gal":"GAL","Eph":"EPH","Phil":"PHP","Col":"COL","1Thess":"1TH","2Thess":"2TH","1Tim":"1TI","2Tim":"2TI","Titus":"TIT","Phlm":"PHM","Heb":"HEB","Jas":"JAS","1Pet":"1PE","2Pet":"2PE","1John":"1JN","2John":"2JN","3John":"3JN","Jude":"JUD","Rev":"REV"}
def ref(r):
    l, c, v = r.split("."); u = OB.get(l)
    return (u, int(c), int(v)) if u else None
por = defaultdict(lambda: defaultdict(list)); n = 0
for linha in SRC.read_text(encoding="utf-8").splitlines()[1:]:
    p = linha.split("\t")
    if len(p) < 3: continue
    try: votos = int(p[2])
    except ValueError: continue
    if votos < 0: continue
    o = ref(p[0])
    ini, _, fim = p[1].partition("-")
    d = ref(ini); df = ref(fim) if fim else d
    if not o or not d or not df: continue
    vfim = df[2] if (df[0], df[1]) == (d[0], d[1]) else d[2]
    por[(o[0], o[1])][o[2]].append([d[0], d[1], d[2], vfim, votos])
for (u, c), versos in por.items():
    saida = {str(v): sorted(rs, key=lambda r: -r[4])[:20] for v, rs in versos.items()}
    n += sum(len(x) for x in saida.values())
    (OUT / u).mkdir(parents=True, exist_ok=True)
    (OUT / u / f"{c}.json").write_text(json.dumps(saida, separators=(",", ":")), encoding="utf-8")
print(n, "referências em", len(por), "capítulos")
