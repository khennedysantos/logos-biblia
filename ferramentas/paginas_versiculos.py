"""Uma página estática por versículo: /biblia/joao/3/16/ (31.102 páginas), como as do BibleHub.

Chamado pelo gerar_paginas.py depois das páginas de capítulo (não rode sozinho). HTML avulso, leve e compacto (sem o
app, com /lexico.css), porque são muitas páginas: o texto na Bíblia Livre, na King James e na Reina-Valera, o original
palavra por palavra com link para o léxico, o começo do comentário (Calvino ou Matthew Henry), as referências
cruzadas principais e o botão para estudar o versículo no Sola (/biblia/joao/3/#v16)."""
import html, json, re
from pathlib import Path

e = html.escape
NUM_VERSO = re.compile(r"^\s*\d+(?:\s*[-,]\s*\d+)*\s*[\.:]?\s*")
REFS_COM_TEXTO = 3          # referências cruzadas com o texto do versículo
REFS_SO_LINK = 9            # depois delas, só o link
COMENTARIO = 420            # caracteres do começo do comentário


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def url_lexico(cod):
    m = re.fullmatch(r"([GH])(\d+)", cod or "")
    return f"/lexico/{'grego' if m.group(1) == 'G' else 'hebraico'}/{int(m.group(2))}/" if m else ""


def comentario_proximo(com, v):
    """o mesmo do app.js: o comentário do versículo, ou o do bloco que o contém, ou o primeiro do capítulo"""
    if not com:
        return None
    if str(v) in com:
        return v, com[str(v)]
    nums = [int(k) for k in com if k.isdigit()]
    antes = max((n for n in nums if n < v), default=0)
    if antes:
        return antes, com[str(antes)]
    depois = min((n for n in nums if n > v), default=0)
    return (depois, com[str(depois)]) if depois else None


def cortar_texto(t, n):
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"


def gerar(raiz, site, livros, slug, cortar, css, citacoes=None):
    """grava biblia/<livro>/<cap>/<v>/index.html e devolve os endereços para o sitemap"""
    info = {b["id"]: b for b in livros}
    s_de = {b["id"]: slug(b["pt"]) for b in livros}
    autores = {}
    for pasta, nome in (("henry", "Matthew Henry"), ("calvin", "João Calvino")):
        for i in ler(raiz / "data" / "commentaries" / pasta / "manifest.json")["books"]:
            autores[i] = (pasta, nome)
    ordem = [(b["id"], c) for b in livros for c in range(1, b["ch"] + 1)]
    urls = []
    textos_bl = {}

    def bl(l, c, v):
        if l not in textos_bl:
            textos_bl[l] = ler(raiz / "data" / "bibles" / "blivre" / f"{l}.json")
        try:
            return textos_bl[l][c - 1][v - 1] or ""
        except IndexError:
            return ""

    def ref_txt(l, c, a, b=None):
        return f"{info[l]['pt']} {c}:{a}" + (f"-{b}" if b and b != a else "")

    def link(l, c, a, b=None):
        return f'<a href="/biblia/{s_de[l]}/{c}/{a}/">{e(ref_txt(l, c, a, b))}</a>'

    # lista de todos os versículos, para o anterior/próximo atravessar capítulos e livros
    for l in info:
        bl(l, 1, 1)
    todos = [(l, c, v) for l, c in ordem for v in range(1, len(textos_bl[l][c - 1]) + 1) if textos_bl[l][c - 1][v - 1]]
    pos = {x: i for i, x in enumerate(todos)}

    for l in info:
        b = info[l]
        kjv, rva = ler(raiz / "data" / "bibles" / "kjv" / f"{l}.json"), ler(raiz / "data" / "bibles" / "rva" / f"{l}.json")
        pasta, autor = autores.get(l, (None, None))
        lang = "he" if b["t"] == "AT" else "grc"
        for c in range(1, b["ch"] + 1):
            inter = ler(raiz / "data" / "interlinear" / l / f"{c}.json") if (raiz / "data" / "interlinear" / l / f"{c}.json").exists() else []
            refs = ler(raiz / "data" / "crossrefs" / l / f"{c}.json") if (raiz / "data" / "crossrefs" / l / f"{c}.json").exists() else {}
            com = None
            if pasta:
                arq = raiz / "data" / "commentaries" / pasta / "pt" / l / f"{c}.json"
                com = ler(arq) if arq.exists() else None
            versos = textos_bl[l][c - 1]
            for v in range(1, len(versos) + 1):
                texto = versos[v - 1] or ""
                if not texto:
                    continue
                nome = ref_txt(l, c, v)
                caminho = f"/biblia/{s_de[l]}/{c}/{v}/"
                corpo = [f'<p class="lex-sobre"><a href="/biblia/{s_de[l]}/">{e(b["pt"])}</a> · '
                         f'<a href="/biblia/{s_de[l]}/{c}/">capítulo {c}</a></p>',
                         f"<h1>{e(nome)}</h1>", f'<p class="lex-resumo">{e(texto)}</p>']
                outras = []
                for sigla, fonte in (("KJV", kjv), ("RVA", rva)):
                    try:
                        t = fonte[c - 1][v - 1]
                    except IndexError:
                        t = ""
                    if t:
                        outras.append(f"<p><b>{sigla}</b> {e(t)}</p>")
                if outras:
                    corpo.append('<div class="vs-trad">' + "".join(outras) + "</div>")
                palavras = inter[v - 1] if v - 1 < len(inter) else []
                if palavras:
                    itens = []
                    for p in palavras:
                        u = url_lexico(p[2])
                        orig = e(re.sub(r"[\\׃׀]", "", p[0]).strip())
                        orig = f'<a href="{u}">{orig}</a>' if u else orig
                        itens.append(f"<li>{orig}<i>{e(p[1])}</i>{e(p[3])}</li>")
                    corpo.append(f'<h2>{"Hebraico" if lang == "he" else "Grego"} palavra por palavra</h2>'
                                 f'<ol class="vs-inter" lang="{lang}">{"".join(itens)}</ol>')
                achado = comentario_proximo(com, v)
                if achado:
                    vc, txt = achado
                    txt = NUM_VERSO.sub("", txt, count=1)
                    nota = "" if vc == v else f" (comentário a partir do v. {vc})"
                    corpo.append(f'<h2>Comentário de {autor}</h2><p class="vs-com">{e(cortar_texto(txt, COMENTARIO))}</p>'
                                 f'<p class="fonte">{autor}, tradução automática do inglês{nota}. '
                                 f'<a href="/biblia/{s_de[l]}/{c}/#v{v}">Ler o comentário completo no Sola ›</a></p>')
                cit = (citacoes or {}).get((l, c, v), [])
                if cit:
                    corpo.append('<h2>Nas confissões de fé</h2><ul class="vs-refs">' +
                                 "".join(f'<li><a href="{u}">{e(r)}</a></li>' for r, u, *_ in cit[:8]) + "</ul>" +
                                 (f'<p class="lex-mais">e mais {len(cit) - 8}.</p>' if len(cit) > 8 else ""))
                lista = refs.get(str(v), [])
                if lista:
                    itens = []
                    for rl, rc, ra, rb, _ in lista[:REFS_COM_TEXTO]:
                        if rl in info:
                            itens.append(f"<li>{link(rl, rc, ra, rb)} {e(cortar_texto(bl(rl, rc, ra), 200))}</li>")
                    resto = [link(rl, rc, ra, rb) for rl, rc, ra, rb, _ in lista[REFS_COM_TEXTO:REFS_COM_TEXTO + REFS_SO_LINK] if rl in info]
                    corpo.append('<h2>Referências cruzadas</h2><ul class="vs-refs">' + "".join(itens) + "</ul>" +
                                 (f'<p class="lex-mais">{", ".join(resto)}</p>' if resto else ""))
                corpo.append(f'<a class="lex-abrir" href="/biblia/{s_de[l]}/{c}/#v{v}">Estudar {e(nome)} no Sola</a>')
                i = pos[(l, c, v)]
                ant = todos[i - 1] if i else None
                pro = todos[i + 1] if i + 1 < len(todos) else None
                corpo.append('<nav class="lex-viz">' + (f"<span>‹ {link(*ant)}</span>" if ant else "<span></span>") +
                             (f"<span>{link(*pro)} ›</span>" if pro else "<span></span>") + "</nav>")
                corpo.append('<p class="fonte">Bíblia Livre; King James (1769) e Reina-Valera Antigua, domínio público. '
                             'Interlinear: STEPBible/Tyndale House (CC BY). Referências: openbible.info (CC BY).</p>')
                titulo = f"{nome} — {cortar_texto(texto, 60)} | Sola"
                desc = cortar(f"{nome}: {texto}", 158)
                trilha = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "name": n_, "item": site + u_} for i, (n_, u_) in enumerate(
                        [("Sola", "/"), (b["pt"], f"/biblia/{s_de[l]}/"), (f"{b['pt']} {c}", f"/biblia/{s_de[l]}/{c}/"), (nome, caminho)])]}
                seo = (f'<link rel="canonical" href="{site}{caminho}"><meta property="og:title" content="{e(nome)} — Sola">'
                       f'<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{site}{caminho}">'
                       f'<meta property="og:image" content="{site}/og.png"><meta property="og:type" content="article">'
                       f'<script type="application/ld+json">{json.dumps(trilha, ensure_ascii=False)}</script>')
                pagina = pagina_versiculo(titulo, desc, css, "".join(corpo), seo)
                arq = raiz / caminho.strip("/") / "index.html"
                arq.parent.mkdir(parents=True, exist_ok=True)
                arq.write_text(pagina, encoding="utf-8")
                urls.append(site + caminho)
    return urls


def pagina_versiculo(titulo, desc, css, corpo, seo):
    """como paginas_lexico.pagina, mas compacta (sem quebras de linha): são 31 mil páginas"""
    from paginas_lexico import LOGO, TEMA
    return (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{e(titulo)}</title>'
            f'<meta name="description" content="{e(desc)}"><meta name="theme-color" content="#FAF7F0">{TEMA}'
            f'<link rel="stylesheet" href="{css}"><link rel="icon" href="/favicon.svg" type="image/svg+xml">{seo}</head><body>'
            f'<header class="topo"><a class="marca" href="/" aria-label="Sola — página inicial">{LOGO}Sola</a>'
            '<nav aria-label="Seções"><a href="/biblia/joao/1/">Bíblia</a><a href="/lexico/">Léxico</a>'
            '<a href="/dicionario/">Dicionário</a><a href="/temas/">Temas</a></nav></header>'
            f'<main class="lex">{corpo}</main><footer class="rodape"><em>Sola Scriptura</em> · Estudo bíblico gratuito e em '
            'português · <a href="/">solabiblia.com.br</a></footer></body></html>\n')
