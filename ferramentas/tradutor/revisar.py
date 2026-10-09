"""Revisa etapas já traduzidas: refaz só os trechos com suspeita de omissão
(tradução muito mais curta que o original) e grava de novo no site.
uso: ./venv/bin/python revisar.py temas dicionario"""
import json, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from tradutor import Tradutor
from lote import pos
import etapas


def revisar(etapa, T):
    ent_arq, tr_arq = etapas.TRAB / f"{etapa}.json", etapas.TRAB / f"{etapa}_pt.json"
    if not ent_arq.exists() or not tr_arq.exists():
        return print(f"[{etapa}] ainda não foi traduzida; rode traduzir_tudo.sh antes")
    orig = {e["id"]: e["texto"] for e in etapas.ler(ent_arq)}
    tr = etapas.ler(tr_arq)
    ruins = [k for k, o in orig.items() if k in tr and T.suspeita(o, tr[k])]
    print(f"[{etapa}] {len(ruins)} trechos suspeitos de {len(tr)}; retraduzindo...", flush=True)
    melhorou = 0
    for i in range(0, len(ruins), 100):
        bloco = ruins[i:i + 100]
        for k, novo in zip(bloco, T.traduzir([orig[k] for k in bloco])):
            novo = pos(orig[k], novo)
            if len(novo) > len(tr[k]):
                tr[k] = novo; melhorou += 1
        print(f"  {min(i + 100, len(ruins))}/{len(ruins)}", flush=True)
    tr_arq.write_text(json.dumps(tr, ensure_ascii=False), encoding="utf-8")
    print(f"[{etapa}] {melhorou} trechos corrigidos")
    getattr(etapas, f"aplicar_{etapa}")()


if __name__ == "__main__":
    T = Tradutor(AQUI / "modelo")
    for etapa in sys.argv[1:] or ["temas", "dicionario"]:
        revisar(etapa, T)
    print("\nPronto. Para publicar: cd ../.. && git add . && git commit -m 'Revisao da traducao' && git push")
