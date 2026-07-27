"""Extrai as glosas únicas de todo o interlinear e gera entradas_glosas.json
para o lote de tradução. O id de cada glosa é um hash do texto, então o
mesclar_glosas.py consegue mapear as traduções de volta sem tabela auxiliar."""
import json, hashlib
from pathlib import Path

BASE = Path(__file__).parent.parent / "data" / "interlinear"
SAIDA = Path(__file__).parent / "entradas_glosas.json"

def hid(s):
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:12]

# glosas já traduzidas manualmente (custo zero) — pular tanto a chave EN
# quanto o valor PT, para não pagar de novo pelo que já está pronto
ja_pt = set()
mapa_arq = Path(__file__).parent / "glosas_pt.json"
if mapa_arq.exists():
    m = json.loads(mapa_arq.read_text(encoding="utf-8"))
    ja_pt = set(m.keys()) | set(m.values())

unicas = {}
total = 0
for arq in BASE.glob("*/*.json"):
    versos = json.loads(arq.read_text(encoding="utf-8"))
    for verso in versos:
        for palavra in verso:
            g = palavra[3]
            total += 1
            if g and g not in unicas and g not in ja_pt:
                unicas[g] = hid(g)

entradas = [{"id": f"glosa-{h}", "fonte": "glosa interlinear",
             "livro": "", "capitulo": 0, "verso_inicio": 0, "verso_fim": 0,
             "texto": g} for g, h in unicas.items()]
SAIDA.write_text(json.dumps(entradas, ensure_ascii=False), encoding="utf-8")
chars = sum(len(g) for g in unicas)
print(f"{total} palavras no interlinear -> {len(unicas)} glosas únicas "
      f"({chars/1e6:.2f}M caracteres) salvas em {SAIDA.name}")
