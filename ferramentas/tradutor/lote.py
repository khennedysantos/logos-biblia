"""Tradução em lote retomável.
uso: python3 lote.py entrada.json saida.json [pasta_modelo]
entrada: lista de {"id":..., "texto":...}; saida: {id: traducao}.
Salva a cada bloco: se for interrompido, rode de novo e ele continua de onde parou."""
import json, sys, re, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from tradutor import Tradutor


def pos(orig, pt):
    if not pt:
        return pt
    pt = re.sub(r"\s+([,;:.)\]])", r"\1", pt).replace("( ", "(")
    pt = re.sub(r"éia\b", "eia", pt)
    if orig[:1].islower() and pt[:1].isupper() and not pt[:2].isupper():
        pt = pt[0].lower() + pt[1:]
    if not orig.rstrip().endswith(".") and pt.endswith(".") and not pt.endswith("..."):
        pt = pt[:-1]
    return pt


def main():
    ent, sai = Path(sys.argv[1]), Path(sys.argv[2])
    modelo = sys.argv[3] if len(sys.argv) > 3 else str(Path(__file__).parent / "modelo")
    itens = json.loads(ent.read_text(encoding="utf-8"))
    feitos = json.loads(sai.read_text(encoding="utf-8")) if sai.exists() else {}
    pend = [i for i in itens if i["id"] not in feitos and i["texto"].strip()]
    total = len(pend)
    print(f"{len(itens)} itens, {len(feitos)} já feitos, {total} pendentes", flush=True)
    if not pend:
        return
    T = Tradutor(modelo)
    t0, chars, falta = time.time(), 0, sum(len(i["texto"]) for i in pend)
    for k in range(0, total, 100):
        bloco = pend[k:k + 100]
        res = T.traduzir([b["texto"] for b in bloco])
        for b, r in zip(bloco, res):
            feitos[b["id"]] = pos(b["texto"], r)
            chars += len(b["texto"])
        tmp = sai.with_suffix(".tmp")
        tmp.write_text(json.dumps(feitos, ensure_ascii=False), encoding="utf-8")
        tmp.replace(sai)
        vel = chars / max(time.time() - t0, 1e-6)
        resta = (falta - chars) / max(vel, 1)
        print(f"  {min(k + 100, total)}/{total}  {vel:.0f} car/s  faltam ~{resta / 60:.0f} min", flush=True)
    print("fim", flush=True)


if __name__ == "__main__":
    main()
