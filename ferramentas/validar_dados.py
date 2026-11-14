"""Confere os dados do site antes de publicar. Sai com erro se algo essencial estiver quebrado.
    python3 ferramentas/validar_dados.py
Roda em segundos; o GitHub Actions (.github/workflows/verificar.yml) roda a cada envio."""
import json, sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
erros, avisos = [], []


def ler(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception as ex:   # arquivo ausente ou JSON inválido
        erros.append(f"{Path(p).relative_to(DATA)}: {ex.__class__.__name__}")
        return None


def main():
    meta = ler(DATA / "books.json")
    livros = meta["books"]
    assert len(livros) == 66, "books.json deveria ter 66 livros"
    lexico = {l: ler(DATA / "strongs" / f"{l}.json") or {} for l in "GH"}
    autores = {a: set((ler(DATA / "commentaries" / a / "manifest.json") or {}).get("books", [])) for a in ("calvin", "henry")}
    palavras = sem_lexico = em_ingles = 0

    for b in livros:
        i, at = b["id"], b["t"] == "AT"
        # texto bíblico: todas as traduções com o número certo de capítulos
        textos = {}
        for tr in ["blivre", "kjv", "rva", "orig"] + ([] if at else ["byz"]):
            t = textos[tr] = ler(DATA / "bibles" / tr / f"{i}.json")
            if t is not None and len(t) != b["ch"]:
                erros.append(f"bibles/{tr}/{i}: {len(t)} capítulos, esperados {b['ch']}")
        base = textos.get(meta["translations"][0]["id"]) or []   # a tradução em português
        for cap in range(1, b["ch"] + 1):
            # interlinear: um arquivo por capítulo, alinhado com a numeração das traduções
            arq = DATA / "interlinear" / i / f"{cap}.json"
            if not arq.exists():
                erros.append(f"interlinear/{i}/{cap}.json não existe")
                continue
            inter = ler(arq) or []
            esperado = len(base[cap - 1]) if len(base) >= cap else 0
            if len(inter) != esperado:
                erros.append(f"interlinear/{i}/{cap}: {len(inter)} versículos, a tradução tem {esperado}")
            if any(not verso and base[cap - 1][n] for n, verso in enumerate(inter[:esperado])):
                erros.append(f"interlinear/{i}/{cap}: versículo com texto na tradução e sem palavras no original")
            for verso in inter:
                for p in verso:
                    palavras += 1
                    if len(p) != 4:
                        erros.append(f"interlinear/{i}/{cap}: palavra com {len(p)} campos")
                    elif p[2] and p[2] not in lexico.get(p[2][0], {}):
                        sem_lexico += 1
            if not (DATA / "crossrefs" / i / f"{cap}.json").exists():
                erros.append(f"crossrefs/{i}/{cap}.json não existe")
        # comentário: quem está no manifesto tem pasta, e a tradução não cobre capítulo que não existe
        for autor, lista in autores.items():
            if i in lista and not (DATA / "commentaries" / autor / i).is_dir():
                erros.append(f"commentaries/{autor}/{i}: está no manifesto mas a pasta não existe")

    for autor in autores:
        for arq in (DATA / "commentaries" / autor / "pt").glob("*/*.json"):
            if not (DATA / "commentaries" / autor / arq.parent.name / arq.name).exists():
                erros.append(f"commentaries/{autor}/pt/{arq.parent.name}/{arq.name}: tradução sem o original")
    sem_comentario = [b["id"] for b in livros if b["id"] not in autores["calvin"] | autores["henry"]]
    for tipo in ("dictionary", "topics"):
        indice = ler(DATA / tipo / "index.json") or []
        letras = {n[0].upper() for n in indice}
        for letra in letras:
            for pasta in ("", "pt/"):
                if not (DATA / tipo / f"{pasta}{letra}.json").exists():
                    erros.append(f"{tipo}/{pasta}{letra}.json não existe")
    for nome in ("context.json", "plans.json", "timeline.json", "places.json", "journeys.json"):
        ler(DATA / nome)
    ids = {b["id"] for b in livros}
    for plano in ler(DATA / "plans.json") or []:
        for dia in plano["dias"]:
            for l, c in dia:
                if l not in ids:
                    erros.append(f"plans.json: livro desconhecido {l}")

    # palavras-chave sublinhadas: posições dentro do versículo da Bíblia Livre, sem sobreposição, com palavra no índice
    indice = ler(DATA / "palavras" / "indice.json")
    sublinhadas = 0
    if indice:
        for arq in (DATA / "palavras").glob("*.json"):
            if arq.stem != "indice" and arq.stem not in indice["livros"]:
                erros.append(f"palavras/{arq.name}: não está no índice")
        for i in indice["livros"]:
            texto, do_livro = ler(DATA / "bibles" / "blivre" / f"{i}.json") or [], ler(DATA / "palavras" / f"{i}.json") or {}
            for cap, versos in do_livro.items():
                for v, marcas in versos.items():
                    try:
                        verso = texto[int(cap) - 1][int(v) - 1]
                    except (IndexError, ValueError):
                        erros.append(f"palavras/{i} {cap}:{v}: versículo não existe na Bíblia Livre")
                        continue
                    fim = 0
                    for m in marcas:
                        sublinhadas += 1
                        if not (fim <= m[0] < m[1] <= len(verso)) or not verso[m[0]:m[1]].strip():
                            erros.append(f"palavras/{i} {cap}:{v}: posição {m[:2]} fora do versículo ou sobreposta")
                        if m[2] not in indice["lemas"]:
                            erros.append(f"palavras/{i} {cap}:{v}: {m[2]} não está no índice")
                        fim = m[1]
        avisos.append(f"{sublinhadas} palavras-chave sublinhadas")

    if sem_lexico > palavras * 0.002:
        erros.append(f"{sem_lexico} palavras do interlinear apontam para um Strong que não está no léxico")
    elif sem_lexico:
        avisos.append(f"{sem_lexico} palavras do interlinear com Strong fora do léxico")
    avisos.append(f"livros sem comentário: {', '.join(sem_comentario) or 'nenhum'}")
    print(f"{palavras} palavras no interlinear, {len(livros)} livros")
    for a in avisos:
        print("aviso:", a)
    for x in erros[:40]:
        print("ERRO:", x)
    if erros:
        sys.exit(f"{len(erros)} erro(s) nos dados")
    print("dados íntegros")


if __name__ == "__main__":
    main()
