"""
Aplica glosas_auto.json (traduções compostas) em data/interlinear/.
Rode a partir da pasta ferramentas/:   python aplicar_glosas.py
Pode rodar mais de uma vez — só troca o que ainda está em inglês.
Ao final, funde o mapa em glosas_pt.json para que extrair_glosas.py
não cobre de novo pelo que já está traduzido.
"""
import json
from pathlib import Path

AQUI = Path(__file__).parent
BASE = AQUI.parent / "data" / "interlinear"
AUTO = AQUI / "glosas_auto.json"
MANUAL = AQUI / "glosas_pt.json"

if not AUTO.exists():
    raise SystemExit("glosas_auto.json não encontrado nesta pasta.")

mapa = json.loads(AUTO.read_text(encoding="utf-8"))
trocadas = arquivos = 0
for arq in sorted(BASE.glob("*/*.json")):
    versos = json.loads(arq.read_text(encoding="utf-8"))
    mudou = False
    for verso in versos:
        for palavra in verso:
            pt = mapa.get(palavra[3])
            if pt and pt != palavra[3]:
                palavra[3] = pt
                trocadas += 1
                mudou = True
    if mudou:
        arq.write_text(json.dumps(versos, ensure_ascii=False, separators=(",", ":")),
                       encoding="utf-8")
        arquivos += 1

if MANUAL.exists():
    juntos = json.loads(MANUAL.read_text(encoding="utf-8"))
    juntos.update(mapa)
else:
    juntos = mapa
MANUAL.write_text(json.dumps(juntos, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"{trocadas} palavras traduzidas em {arquivos} arquivos.")
print("Agora: cd .. && git add . && git commit -m 'Interlinear em português' && git push")
