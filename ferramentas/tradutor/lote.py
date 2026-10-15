"""Tradução em lote retomável.
uso: python3 lote.py entrada.json saida.json [pasta_modelo] [--motor argos|nllb] [--parte K/N]
entrada: lista de {"id":..., "texto":...}; saida: {id: traducao}.
Salva a cada bloco: se for interrompido, rode de novo e ele continua de onde parou.
--parte K/N traduz só a fatia K (0..N-1) — é assim que o GitHub Actions divide o trabalho em N máquinas."""
import argparse, json, sys, re, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))


def pos(orig, pt):
    if not pt:
        return pt
    pt = re.sub(r"[ \t]+([,;:.)\]])", r"\1", pt).replace("( ", "(")
    pt = re.sub(r"éia\b", "eia", pt)
    if orig[:1].islower() and pt[:1].isupper() and not pt[:2].isupper():
        pt = pt[0].lower() + pt[1:]
    if not orig.rstrip().endswith(".") and pt.endswith(".") and not pt.endswith("..."):
        pt = pt[:-1]
    return pt


def fatia(itens, parte):
    """Divide por tamanho (não por contagem), para as máquinas terminarem juntas."""
    if not parte:
        return itens
    k, n = map(int, parte.split("/"))
    cargas = [0] * n
    minha = []
    for it in sorted(itens, key=lambda i: -len(i["texto"])):
        j = cargas.index(min(cargas))
        cargas[j] += len(it["texto"])
        if j == k:
            minha.append(it)
    return minha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("entrada"); ap.add_argument("saida")
    ap.add_argument("modelo", nargs="?", default=None)
    ap.add_argument("--motor", default="argos", choices=["argos", "nllb"])
    ap.add_argument("--parte", default=None)
    ap.add_argument("--bloco", type=int, default=100, help="itens por gravação")
    ap.add_argument("--max-car", type=int, default=0, help="grava também ao passar destes caracteres (0 = sem limite)")
    a = ap.parse_args()
    ent, sai = Path(a.entrada), Path(a.saida)
    itens = fatia(json.loads(ent.read_text(encoding="utf-8")), a.parte)
    feitos = json.loads(sai.read_text(encoding="utf-8")) if sai.exists() else {}
    pend = [i for i in itens if i["id"] not in feitos and i["texto"].strip()]
    total = len(pend)
    print(f"{len(itens)} itens, {len(feitos)} já feitos, {total} pendentes", flush=True)
    if not pend:
        return
    if a.motor == "nllb":
        from nllb import NLLB
        T = NLLB(a.modelo or str(Path(__file__).parent / "modelo-nllb"))
    else:
        from tradutor import Tradutor
        T = Tradutor(a.modelo or str(Path(__file__).parent / "modelo"))
    t0, chars, falta = time.time(), 0, sum(len(i["texto"]) for i in pend)
    blocos, atual, tam = [], [], 0
    for it in pend:
        if atual and (len(atual) >= a.bloco or (a.max_car and tam + len(it["texto"]) > a.max_car)):
            blocos.append(atual); atual, tam = [], 0
        atual.append(it); tam += len(it["texto"])
    if atual:
        blocos.append(atual)
    k = 0
    for bloco in blocos:
        res = T.traduzir([b["texto"] for b in bloco])
        for b, r in zip(bloco, res):
            feitos[b["id"]] = pos(b["texto"], r)
            chars += len(b["texto"])
        tmp = sai.with_suffix(".tmp")
        tmp.write_text(json.dumps(feitos, ensure_ascii=False), encoding="utf-8")
        tmp.replace(sai)
        vel = chars / max(time.time() - t0, 1e-6)
        resta = (falta - chars) / max(vel, 1)
        k += len(bloco)
        print(f"  {k}/{total}  {vel:.0f} car/s  faltam ~{resta / 60:.0f} min", flush=True)
    print("fim", flush=True)


if __name__ == "__main__":
    main()
