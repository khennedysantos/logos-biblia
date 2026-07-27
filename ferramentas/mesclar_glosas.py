"""Aplica as glosas traduzidas (traducoes.json) em todos os arquivos de
data/interlinear/. Rode a partir da pasta ferramentas/:
    python mesclar_glosas.py
Pode rodar mais de uma vez; só substitui o que tem tradução."""
import json, hashlib
from pathlib import Path

AQUI = Path(__file__).parent
BASE = AQUI.parent / "data" / "interlinear"
TRAD = AQUI / "traducoes.json"

if not TRAD.exists():
    raise SystemExit("traducoes.json não encontrado. Rode antes o "
                     "traduzir_comentarios.py com entradas_glosas.json.")

def hid(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]

mapa = {}
for tid, texto in json.loads(TRAD.read_text(encoding="utf-8")).items():
    if tid.startswith("glosa-"):
        mapa[tid.split("-", 1)[1]] = texto.strip()

if not mapa:
    raise SystemExit("Nenhuma glosa em traducoes.json — confira o lote enviado.")

trocadas, arquivos = 0, 0
for arq in BASE.glob("*/*.json"):
    versos = json.loads(arq.read_text(encoding="utf-8"))
    mudou = False
    for verso in versos:
        for palavra in verso:
            pt = mapa.get(hid(palavra[3])) if palavra[3] else None
            if pt and pt != palavra[3]:
                palavra[3] = pt
                trocadas += 1
                mudou = True
    if mudou:
        arq.write_text(json.dumps(versos, ensure_ascii=False,
                                  separators=(",", ":")), encoding="utf-8")
        arquivos += 1

print(f"{trocadas} glosas traduzidas em {arquivos} arquivos.")
print("Agora é só dar git add/commit/push para as mudanças irem ao ar.")
