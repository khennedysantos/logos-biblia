"""Gera as páginas estáticas do Sola: a página inicial (dentro do index.html), uma página por livro
(/biblia/joao/), uma por capítulo (/biblia/joao/3/), o sitemap.xml, o robots.txt e o 404.html.

Cada página é o próprio index.html com título, descrição, endereço canônico e o conteúdo já escritos
no HTML. O Google lê o texto direto; para o visitante, o app assume e funciona igual.

RODE DE NOVO SEMPRE QUE index.html, app.js, style.css OU sw.js MUDAREM (as páginas copiam o index.html,
e o index.html carrega app.js/style.css com a versão no endereço):
    python3 ferramentas/gerar_paginas.py
Rodar duas vezes seguidas não muda nada: o GitHub Actions usa isso para conferir se alguém esqueceu.
"""
import hashlib, html, json, re, shutil, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SITE = "https://solabiblia.com.br"
TRAD = "blivre"
ORNAMENTO = '<div class="ornamento" aria-hidden="true"><i></i></div>'
# os mesmos grupos estão no app.js (GRUPOS)
GRUPOS = [
    ("AT", "Pentateuco", "GEN EXO LEV NUM DEU"),
    ("AT", "Históricos", "JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST"),
    ("AT", "Poéticos e sapienciais", "JOB PSA PRO ECC SNG"),
    ("AT", "Profetas maiores", "ISA JER LAM EZK DAN"),
    ("AT", "Profetas menores", "HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL"),
    ("NT", "Evangelhos e Atos", "MAT MRK LUK JHN ACT"),
    ("NT", "Cartas de Paulo", "ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM"),
    ("NT", "Cartas gerais e Apocalipse", "HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV"),
]
TESTAMENTO = {"AT": "Antigo Testamento", "NT": "Novo Testamento"}
e = html.escape


def ler(caminho):
    return json.loads((RAIZ / caminho).read_text(encoding="utf-8"))


def slug(nome):
    s = unicodedata.normalize("NFD", nome)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", "-", s.lower())


def cortar(texto, n=155):
    if len(texto) <= n:
        return texto
    return texto[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def carimbar_versoes():
    """Põe ?v=<hash> no style.css e no app.js do index.html: quando o arquivo muda, o endereço muda,
    e o navegador baixa a versão nova na hora em vez de usar a guardada em cache (10 min no GitHub Pages)."""
    idx = RAIZ / "index.html"
    texto = idx.read_text(encoding="utf-8")
    for arq in ("style.css", "app.js"):
        h = hashlib.sha1((RAIZ / arq).read_bytes()).hexdigest()[:10]
        texto = re.sub(rf'"/{re.escape(arq)}(\?v=[0-9a-f]+)?"', f'"/{arq}?v={h}"', texto)
    idx.write_text(texto, encoding="utf-8")


def carimbar_sw():
    """O service worker guarda o app com o nome da versão: mudou qualquer arquivo do app, muda a versão,
    e o navegador troca o que tinha guardado."""
    h = hashlib.sha1(b"".join((RAIZ / a).read_bytes() for a in ("index.html", "app.js", "style.css"))).hexdigest()[:10]
    sw = RAIZ / "sw.js"
    texto, n = re.subn(r'const VERSAO = "[^"]*";', f'const VERSAO = "{h}";', sw.read_text(encoding="utf-8"), count=1)
    assert n == 1, "linha VERSAO ausente no sw.js"
    sw.write_text(texto, encoding="utf-8")


def cabeca_seo(url, titulo, desc, tipo, migalhas):
    """Bloco entre <!--SEO--> e <!--/SEO-->: canônico, Open Graph e o caminho da página para o Google."""
    trilha = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": nome, "item": SITE + caminho}
        for i, (nome, caminho) in enumerate(migalhas, 1)]}
    return f"""<link rel="canonical" href="{url}">
<meta property="og:type" content="{tipo}">
<meta property="og:site_name" content="Sola">
<meta property="og:locale" content="pt_BR">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(trilha, ensure_ascii=False)}</script>"""


def montar(modelo, *, vista, conteudo, rotulo, titulo=None, desc=None, seo=None):
    pagina = re.sub(r"<!--CONTEUDO-->.*?<!--/CONTEUDO-->", lambda _: f"<!--CONTEUDO-->{conteudo}<!--/CONTEUDO-->",
                    modelo, count=1, flags=re.S)
    pagina = re.sub(r'<body data-vista="[a-z]+">', f'<body data-vista="{vista}">', pagina, count=1)
    pagina = re.sub(r'<span id="lblLivroAtual">[^<]*</span>', f'<span id="lblLivroAtual">{e(rotulo)}</span>', pagina, count=1)
    if seo:
        pagina = re.sub(r"<!--SEO-->.*?<!--/SEO-->", lambda _: f"<!--SEO-->\n{seo}\n<!--/SEO-->", pagina, count=1, flags=re.S)
    if titulo:
        pagina = re.sub(r"<title>.*?</title>", lambda _: f"<title>{e(titulo)}</title>", pagina, count=1)
    if desc:
        pagina = re.sub(r'<meta name="description" content="[^"]*">',
                        lambda _: f'<meta name="description" content="{e(desc)}">', pagina, count=1)
    return pagina


def pagina_inicial(livros):
    por_id = {b["id"]: b for b in livros}
    partes = [f"""<div class="inicio">
<section class="heroi">
<p class="heroi-sobre">Sola Scriptura</p>
<h1>A Escritura, <em>em profundidade</em></h1>{ORNAMENTO}
<p class="heroi-texto">A Bíblia completa com o grego e o hebraico palavra por palavra, léxico de Strong, comentários de Calvino e Matthew Henry, referências cruzadas e atlas. Gratuito, sem anúncios, em português.</p>
<div class="heroi-acoes"><a class="btn-ouro" href="/biblia/joao/1/">Começar por João</a></div>
</section>"""]
    for sigla, nome in TESTAMENTO.items():
        partes.append(f'<section class="testamento"><h2>{nome}</h2>{ORNAMENTO}<div class="grupos">')
        for t, grupo, ids in GRUPOS:
            if t != sigla:
                continue
            links = "".join(f'<a href="/biblia/{slug(por_id[i]["pt"])}/">{e(por_id[i]["pt"])}<span>{por_id[i]["ch"]}</span></a>'
                            for i in ids.split())
            partes.append(f'<div class="grupo-livros"><h3>{grupo}</h3>{links}</div>')
        partes.append("</div></section>")
    partes.append("</div>")
    return "\n".join(partes)


def pagina_livro(b, ant, pro, grupo, ctx, autor):
    nome, s = b["pt"], slug(b["pt"])
    ficha = ""
    if ctx:
        ficha = f"""<div class="livro-ficha"><dl class="ctx-grade">
<dt>Autor</dt><dd>{e(ctx["a"])}</dd>
<dt>Data</dt><dd>{e(ctx["d"])}</dd>
<dt>Local</dt><dd>{e(ctx["l"])}</dd>
<dt>Público</dt><dd>{e(ctx["p"])}</dd>
<dt>Tema</dt><dd>{e(ctx["t"])}</dd>
</dl></div>"""
    caps = "".join(f'<a href="/biblia/{s}/{c}/">{c}</a>' for c in range(1, b["ch"] + 1))
    viz = (f'<a href="/biblia/{slug(ant["pt"])}/">‹ {e(ant["pt"])}</a>' if ant else "<span></span>") + \
          (f'<a href="/biblia/{slug(pro["pt"])}/">{e(pro["pt"])} ›</a>' if pro else "<span></span>")
    return f"""<div class="livro-pagina">
<header class="cap-cabeca">
<p class="cap-sobre"><a href="/">{TESTAMENTO[b["t"]]}</a> · {grupo}</p>
<h1 class="titulo-cap">{e(nome)}</h1>{ORNAMENTO}
<p class="sub-cap">{b["ch"]} capítulos{f" · Comentário: {autor}" if autor else ""}</p>
</header>
{ficha}
<h2>capítulos</h2>
<nav class="caps" aria-label="capítulos">{caps}</nav>
<div class="livro-vizinhos">{viz}</div>
</div>"""


def pagina_capitulo(b, cap, versos, nome_trad, grupo, anterior, proximo):
    s = slug(b["pt"])
    corpo = [f"""<header class="cap-cabeca">
<p class="cap-sobre"><a href="/">{TESTAMENTO[b["t"]]}</a> · <a href="/biblia/{s}/">{grupo}</a></p>
<h1 class="titulo-cap">{e(b["pt"])} {cap}</h1>{ORNAMENTO}
<p class="sub-cap"><span>{e(nome_trad)}</span> <a class="btn-contexto" href="/biblia/{s}/">Todos os capítulos</a></p>
</header>"""]
    for n, v in enumerate(versos, 1):
        if v:
            corpo.append(f'<div class="verso" id="v{n}" data-v="{n}"><p class="escritura"><sup>{n}</sup>{e(v)}</p></div>')
    links = []
    if anterior:
        pb, pc = anterior
        links.append(f'<a href="/biblia/{slug(pb["pt"])}/{pc}/">‹ {e(pb["pt"])} {pc}</a>')
    if proximo:
        nb, nc = proximo
        links.append(f'<a href="/biblia/{slug(nb["pt"])}/{nc}/">{e(nb["pt"])} {nc} ›</a>')
    corpo.append(f'<nav class="seo-nav">{"".join(links)}</nav>')
    return "\n".join(corpo)


def pagina_de_texto(modelo, arq):
    """Página de texto avulsa (privacidade): HTML próprio, sem o app. O conteúdo fica em ferramentas/paginas/."""
    corpo = arq.read_text(encoding="utf-8")
    titulo = re.search(r"<!-- titulo: (.*?) -->", corpo).group(1)
    desc = re.search(r"<!-- descricao: (.*?) -->", corpo).group(1)
    corpo = re.sub(r"<!-- (titulo|descricao): .*? -->\n", "", corpo)
    estilo = re.search(r'<link rel="stylesheet" href="(/style\.css[^"]*)">', modelo).group(1)
    tema = re.search(r"<script>/\* tema antes.*?</script>", modelo, re.S).group(0)
    url = f"{SITE}/{arq.stem}/"
    logo = ('<svg class="ico ico-marca" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="3.4" r="1.7" fill="currentColor" stroke="none"/>'
            '<path d="M3 8c3-1.8 6-1.8 9 0c3-1.8 6-1.8 9 0v12c-3-1.8-6-1.8-9 0c-3-1.8-6-1.8-9 0z"/><path d="M12 8v12"/></svg>')
    return url, f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(titulo)} — Sola</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#F7F3EA">
{tema}
<link rel="stylesheet" href="{estilo}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="{url}">
</head>
<body data-vista="texto">
<header class="topo"><a class="marca" href="/" aria-label="Sola — página inicial">{logo}<span class="nome">Sola</span></a></header>
<main class="texto-pagina">
<header class="cap-cabeca">
<p class="cap-sobre"><a href="/">Sola</a></p>
<h1 class="titulo-cap">{e(titulo)}</h1>{ORNAMENTO}
</header>
{corpo}
<p class="texto-voltar"><a class="btn-ouro" href="/">Voltar ao Sola</a></p>
</main>
<footer class="rodape"><p class="rodape-legal"><em>Sola Scriptura</em> · Estudo bíblico gratuito e em português · <a href="/" style="display:inline">solabiblia.com.br</a></p></footer>
</body>
</html>
"""


def main():
    carimbar_versoes()
    meta = ler("data/books.json")
    livros = meta["books"]
    nome_trad = next(t["name"] for t in meta["translations"] if t["id"] == TRAD)
    contexto = ler("data/context.json")
    autores = {i: nome for pasta, nome in (("henry", "Matthew Henry"), ("calvin", "João Calvino"))
               for i in ler(f"data/commentaries/{pasta}/manifest.json")["books"]}
    grupo_de = {i: g for _, g, ids in GRUPOS for i in ids.split()}
    assert set(grupo_de) == {b["id"] for b in livros}, "GRUPOS não cobre os 66 livros"
    slugs = {slug(b["pt"]) for b in livros}
    assert len(slugs) == len(livros), "dois livros com o mesmo endereço"

    # página inicial: fica dentro do próprio index.html (que é também o modelo das outras)
    idx = RAIZ / "index.html"
    modelo = idx.read_text(encoding="utf-8")
    for marca in ("<!--SEO-->", "<!--/SEO-->", "<!--CONTEUDO-->", "<!--/CONTEUDO-->", 'id="lblLivroAtual"', '<body data-vista="'):
        assert marca in modelo, f"marcador ausente no index.html: {marca}"
    modelo = montar(modelo, vista="inicio", conteudo=pagina_inicial(livros), rotulo="Livros")
    idx.write_text(modelo, encoding="utf-8")
    carimbar_sw()

    if (RAIZ / "biblia").is_dir():   # apaga as páginas geradas antes
        shutil.rmtree(RAIZ / "biblia")
    urls = [f"{SITE}/"]
    ordem = [(b, c) for b in livros for c in range(1, b["ch"] + 1)]
    for n, b in enumerate(livros):
        s, nome = slug(b["pt"]), b["pt"]
        url = f"{SITE}/biblia/{s}/"
        urls.append(url)
        ctx = contexto.get(b["id"])
        desc = cortar(f"{nome}: {ctx['t']}. {b['ch']} capítulos com o texto original, léxico de Strong, comentário e referências cruzadas."
                      if ctx else f"{nome}: {b['ch']} capítulos com o texto original, léxico de Strong, comentário e referências cruzadas.")
        pagina = montar(modelo, vista="livro", rotulo=nome,
                        conteudo=pagina_livro(b, livros[n - 1] if n else None, livros[n + 1] if n + 1 < len(livros) else None,
                                              grupo_de[b["id"]], ctx, autores.get(b["id"])),
                        titulo=f"{nome} — capítulos, autor, data e contexto | Sola", desc=desc,
                        seo=cabeca_seo(url, f"{nome} — Sola", desc, "website", [("Sola", "/"), (nome, f"/biblia/{s}/")]))
        destino = RAIZ / "biblia" / s / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina, encoding="utf-8")

    textos = {}
    for i, (b, cap) in enumerate(ordem):
        if b["id"] not in textos:
            textos = {b["id"]: ler(f"data/bibles/{TRAD}/{b['id']}.json")}
        versos = textos[b["id"]][cap - 1]
        s, nome = slug(b["pt"]), f"{b['pt']} {cap}"
        url = f"{SITE}/biblia/{s}/{cap}/"
        urls.append(url)
        desc = cortar(f"{nome}: " + " ".join(v for v in versos[:3] if v))
        pagina = montar(modelo, vista="cap", rotulo=nome,
                        conteudo=pagina_capitulo(b, cap, versos, nome_trad, grupo_de[b["id"]],
                                                 ordem[i - 1] if i else None, ordem[i + 1] if i + 1 < len(ordem) else None),
                        titulo=f"{nome} — Bíblia de estudo com grego, hebraico e comentários | Sola", desc=desc,
                        seo=cabeca_seo(url, f"{nome} — Sola", desc, "article",
                                       [("Sola", "/"), (b["pt"], f"/biblia/{s}/"), (nome, f"/biblia/{s}/{cap}/")]))
        destino = RAIZ / "biblia" / s / str(cap) / "index.html"
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(pagina, encoding="utf-8")

    # páginas de texto avulsas (cada arquivo de ferramentas/paginas/ vira /nome/)
    for arq in sorted((RAIZ / "ferramentas" / "paginas").glob("*.html")):
        url, pagina = pagina_de_texto(modelo, arq)
        destino = RAIZ / arq.stem / "index.html"
        destino.parent.mkdir(exist_ok=True)
        destino.write_text(pagina, encoding="utf-8")
        urls.append(url)

    # 404: o próprio app (endereços desconhecidos abrem na página inicial), fora do Google
    erro = modelo.replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"', 1)
    (RAIZ / "404.html").write_text(erro, encoding="utf-8")

    itens = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (RAIZ / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{itens}\n</urlset>\n',
        encoding="utf-8")
    (RAIZ / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"página inicial, {len(livros)} páginas de livro, {len(ordem)} de capítulo, "
          f"sitemap com {len(urls)} endereços, robots.txt e 404.html")


if __name__ == "__main__":
    main()
