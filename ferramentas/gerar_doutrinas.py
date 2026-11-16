"""Gera data/topics/doutrinas.json a partir de ferramentas/doutrinas.py.

Confere cada referência na Bíblia Livre (livro, capítulo e versículo existentes) e grava junto o texto dos
versículos, para o cartão do tema mostrar a passagem sem carregar o livro inteiro.

uso:  python3 ferramentas/gerar_doutrinas.py           (grava)
      python3 ferramentas/gerar_doutrinas.py --texto   (não grava; imprime cada referência com o texto, para revisar)
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from doutrinas import DOUTRINAS                                   # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
SAIDA = DATA / "topics" / "doutrinas.json"


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def expandir(refs, biblia, erros, onde):
    """'GEN 17:7-12; ACT 2:38-39, 41' → [[usfm, cap, v1, v2, [textos]], ...]"""
    saida = []
    for parte in [p.strip() for p in refs.split(";") if p.strip()]:
        m = re.fullmatch(r"([1-3]?[A-Z]{2,3}) (\d+):([\d,\- ]+)", parte)
        if not m:
            erros.append(f"{onde}: referência mal escrita “{parte}”")
            continue
        livro, cap, versos = m.group(1), int(m.group(2)), m.group(3)
        if livro not in biblia:
            erros.append(f"{onde}: livro desconhecido “{livro}”")
            continue
        caps = biblia[livro]
        if not 1 <= cap <= len(caps):
            erros.append(f"{onde}: {livro} não tem capítulo {cap}")
            continue
        for trecho in [t.strip() for t in versos.split(",") if t.strip()]:
            a, _, b = trecho.partition("-")
            a, b = int(a), int(b or a)
            if not (1 <= a <= b <= len(caps[cap - 1])):
                erros.append(f"{onde}: {livro} {cap}:{trecho} não existe ({len(caps[cap - 1])} versículos)")
                continue
            textos = [caps[cap - 1][v - 1] for v in range(a, b + 1)]
            if not all(textos):
                erros.append(f"{onde}: {livro} {cap}:{trecho} tem versículo vazio na Bíblia Livre")
            saida.append([livro, cap, a, b, textos])
    return saida


def main():
    livros = [b["id"] for b in ler(DATA / "books.json")["books"]]
    biblia = {l: ler(DATA / "bibles" / "blivre" / f"{l}.json") for l in livros}
    erros, ids, saida = [], set(), []
    for d in DOUTRINAS:
        assert d["id"] not in ids, f"id repetido: {d['id']}"
        ids.add(d["id"])
        secoes = [{"t": t, "v": expandir(refs, biblia, erros, f"{d['id']} / {t}")} for t, refs in d["secoes"]]
        saida.append({"id": d["id"], "t": d["titulo"], "s": d["sin"], "f": d["fonte"], "r": d["resumo"], "sec": secoes})
    if erros:
        sys.exit("ERROS:\n  " + "\n  ".join(erros))
    if "--texto" in sys.argv:
        for d in saida:
            print(f"\n######## {d['t']}")
            for s in d["sec"]:
                print(f"  == {s['t']}")
                for l, c, a, b, tx in s["v"]:
                    print(f"     {l} {c}:{a}{'-' + str(b) if b != a else ''}  " + " / ".join(tx)[:230])
        return
    SAIDA.write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    n = sum(len(s["v"]) for d in saida for s in d["sec"])
    print(f"{len(saida)} doutrinas, {n} referências → {SAIDA.relative_to(RAIZ)} ({SAIDA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
