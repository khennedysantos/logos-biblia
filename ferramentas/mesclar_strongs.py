"""
Mescla as traduções do léxico de Strong (entradas_strongs.json -> traducoes.json)
nos dicionários do site. Rode a partir da pasta ferramentas/:
    python mesclar_strongs.py
Adiciona o campo "defpt" a cada entrada — o site passa a exibir a definição
em português automaticamente, mantendo a original como referência.
"""
import json
from pathlib import Path

AQUI = Path(__file__).parent
DESTINO = AQUI.parent / "data" / "strongs"
TRAD = AQUI / "traducoes.json"

if not TRAD.exists():
    raise SystemExit("traducoes.json não encontrado. Rode antes o "
                     "traduzir_comentarios.py com entradas_strongs.json.")

traducoes = json.loads(TRAD.read_text(encoding="utf-8"))
dics = {L: json.loads((DESTINO / f"{L}.json").read_text(encoding="utf-8"))
        for L in ("G", "H")}

n = 0
for tid, texto in traducoes.items():
    if not tid.startswith("strong-"):
        continue
    num = tid.split("-", 1)[1]           # ex.: G3056
    dic = dics.get(num[0])
    if dic and num in dic:
        # o lote traduz "def || kjv"; guardamos só a definição principal
        dic[num]["defpt"] = texto.split("||")[0].strip()
        n += 1

for L, dic in dics.items():
    (DESTINO / f"{L}.json").write_text(
        json.dumps(dic, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8")

print(f"{n} definições do léxico atualizadas para português.")
