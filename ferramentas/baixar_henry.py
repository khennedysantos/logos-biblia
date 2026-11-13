"""Baixa o comentário de Matthew Henry (completo, domínio público) do HelloAO Free Use Bible API
para data/commentaries/henry/{USFM}/{cap}.json, no mesmo formato do Calvino: {versículo: texto}.

Só os livros que Calvino não comentou (o Henry preenche as lacunas):
    python3 ferramentas/baixar_henry.py
Fonte: https://bible.helloao.org/api/c/matthew-henry/  (Public Domain Mark 1.0)
"""
import json, sys, time, urllib.error, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
API = "https://bible.helloao.org/api/c/matthew-henry"
DEST = RAIZ / "data" / "commentaries" / "henry"


def baixar(url, tentativas=3):
    for i in range(tentativas):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None   # capítulo sem comentário nesta fonte
            if i == tentativas - 1:
                raise
            time.sleep(2 * (i + 1))
        except Exception:
            if i == tentativas - 1:
                raise
            time.sleep(2 * (i + 1))


def texto(item):
    partes = []
    for c in item.get("content", []):
        if isinstance(c, str):
            partes.append(c)
        elif isinstance(c, dict):
            partes.append(c.get("text", ""))
    return " ".join(p.strip(" ") for p in partes if p).strip()


def main():
    livros = {b["id"]: b for b in json.loads((RAIZ / "data/books.json").read_text(encoding="utf-8"))["books"]}
    calvino = set(json.loads((RAIZ / "data/commentaries/calvin/manifest.json").read_text(encoding="utf-8"))["books"])
    alvo = [u for u in livros if u not in calvino]
    disponiveis = {b["id"]: b for b in baixar(f"{API}/books.json")["books"]}
    feitos, total, faltam = [], 0, []
    for usfm in alvo:
        if usfm not in disponiveis:
            print(f"  {usfm}: Henry não tem este livro nesta fonte")
            continue
        for cap in range(1, livros[usfm]["ch"] + 1):
            d = baixar(f"{API}/{usfm}/{cap}.json")
            if d is None:
                faltam.append(f"{usfm} {cap}")
                continue
            versos = {str(i["number"]): texto(i) for i in d.get("chapter", {}).get("content", [])
                      if i.get("type") == "verse" and texto(i)}
            if versos:
                (DEST / usfm).mkdir(parents=True, exist_ok=True)
                (DEST / usfm / f"{cap}.json").write_text(json.dumps(versos, ensure_ascii=False, separators=(",", ":")),
                                                         encoding="utf-8")
                total += sum(len(v) for v in versos.values())
        feitos.append(usfm)
        print(f"  {usfm} ok", flush=True)
    (DEST / "manifest.json").write_text(json.dumps(
        {"id": "henry", "name": "Matthew Henry (1662–1714)", "lang": "en", "books": feitos},
        ensure_ascii=False), encoding="utf-8")
    print(f"{len(feitos)} livros, {total / 1e6:.1f} milhões de caracteres")
    if faltam:
        print("capítulos sem comentário na fonte:", ", ".join(faltam))


if __name__ == "__main__":
    sys.exit(main())
