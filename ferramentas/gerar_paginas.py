"""Gera uma página estática por capítulo (/biblia/joao/3/), o sitemap.xml, o robots.txt e o 404.html.

Cada página é o próprio index.html com título, descrição, endereço canônico e o texto do capítulo
já escritos no HTML. O Google lê o texto direto; para o visitante, o app assume e funciona igual.

RODE DE NOVO SEMPRE QUE O index.html MUDAR (as páginas são cópias dele):
    python3 ferramentas/gerar_paginas.py
"""
import html, json, re, shutil, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = "https://solabiblia.com.br"
TRAD = "blivre"


def slug(nome):
    s = unicodedata.normalize("NFD", nome)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", "-", s.lower())


def cortar(texto, n=155):
    if len(texto) <= n:
        return texto
    return texto[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def main():
    modelo = (RAIZ / "index.html").read_text(encoding="utf-8")
    assert "<!--SEO-->" in modelo and "<!--CONTEUDO-->" in modelo, "marcadores ausentes no index.html"
    seo_ini, seo_fim = modelo.index("<!--SEO-->"), modelo.index("<!--/SEO-->") + len("<!--/SEO-->")
    meta = json.loads((RAIZ / "data/books.json").read_text(encoding="utf-8"))
    nome_trad = next(t["name"] for t in meta["translations"] if t["id"] == TRAD)
    livros = meta["books"]

    # apaga as páginas geradas antes
    slugs = {slug(b["pt"]) for b in livros}
    assert len(slugs) == len(livros), "dois livros com o mesmo endereço"
    if (RAIZ / "biblia").is_dir():
        shutil.rmtree(RAIZ / "biblia")

    urls = [f"{SITE}/"]
    ordem = [(b, c) for b in livros for c in range(1, b["ch"] + 1)]
    for i, (b, cap) in enumerate(ordem):
        versos = json.loads((RAIZ / f"data/bibles/{TRAD}/{b['id']}.json").read_text(encoding="utf-8"))[cap - 1]
        nome = f"{b['pt']} {cap}"
        url = f"{SITE}/biblia/{slug(b['pt'])}/{cap}/"
        urls.append(url)
        inicio = " ".join(v for v in versos[:3] if v)
        desc = cortar(f"{nome}: {inicio}")
        titulo = f"{nome} — Bíblia de estudo com grego, hebraico e comentários | Sola"

        cabeca = f"""<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Sola">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{html.escape(nome)} — Sola">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">"""

        corpo = [f'<h1 class="titulo-cap escritura">{html.escape(nome)}</h1>',
                 f'<p class="sub-cap">{html.escape(nome_trad)}</p>']
        for n, v in enumerate(versos, 1):
            if v:
                corpo.append(f'<div class="verso" data-v="{n}"><p class="escritura"><sup>{n}</sup>{html.escape(v)}</p></div>')
        links = []
        if i > 0:
            pb, pc = ordem[i - 1]
            links.append(f'<a href="/biblia/{slug(pb["pt"])}/{pc}/">‹ {html.escape(pb["pt"])} {pc}</a>')
        if i < len(ordem) - 1:
            nb, nc = ordem[i + 1]
            links.append(f'<a href="/biblia/{slug(nb["pt"])}/{nc}/">{html.escape(nb["pt"])} {nc} ›</a>')
        corpo.append(f'<nav class="seo-nav">{"".join(links)}</nav>')

        pagina = modelo[:seo_ini] + cabeca + modelo[seo_fim:]
        pagina = re.sub(r"<title>.*?</title>", f"<title>{html.escape(titulo)}</title>", pagina, count=1)
        pagina = re.sub(r'<meta name="description" content="[^"]*">',
                        f'<meta name="description" content="{html.escape(desc)}">', pagina, count=1)
        pagina = pagina.replace("<!--CONTEUDO-->", "\n".join(corpo), 1)
        pagina = pagina.replace('<span id="lblLivroAtual">João 1</span>', f'<span id="lblLivroAtual">{html.escape(nome)}</span>', 1)
        destino = RAIZ / "biblia" / slug(b["pt"]) / str(cap) / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina, encoding="utf-8")

    # 404: o próprio app (endereços desconhecidos abrem em João 1), fora do Google
    erro = modelo.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)
    (RAIZ / "404.html").write_text(erro, encoding="utf-8")

    itens = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{itens}\n</urlset>\n',
        encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"{len(ordem)} páginas de capítulo, sitemap com {len(urls)} endereços, robots.txt e 404.html")


if __name__ == "__main__":
    main()
