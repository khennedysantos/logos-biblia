"""Páginas estáticas do léxico de Strong: /lexico/, /lexico/grego/ e /lexico/hebraico/ (índices), as listas de 250 em
250 (/lexico/grego/1-250/) e uma página por palavra (/lexico/grego/26/, /lexico/hebraico/2617/).

Chamado pelo gerar_paginas.py (não rode sozinho). As páginas são HTML avulso e leve, sem o app (como a
/privacidade/): o Google lê definição, usos e versículos; o visitante segue para o capítulo no Sola pelos links.
Usam a folha /lexico.css (com a versão no endereço), e não o style.css: mudar o app não reescreve 14 mil páginas.

Fontes de cada página: data/strongs/{G,H}.json (defpt, usopt, def, kjv), data/interlinear/ (onde a palavra aparece,
a forma original e a glosa em cada versículo) e data/bibles/blivre/ (o texto do versículo)."""
import collections, hashlib, html, json, re, shutil
from pathlib import Path

e = html.escape
IDIOMA = {"G": ("grego", "Grego", "grc", "Léxico grego do Novo Testamento"),
          "H": ("hebraico", "Hebraico", "he", "Léxico hebraico do Antigo Testamento")}
VERSOS_COM_TEXTO = 25        # primeiros versículos mostrados por inteiro
MAIS_REFERENCIAS = 400       # depois deles, só a referência (até este número)
FAIXA = 250                  # tamanho das listas do índice
LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="3.4" r="1.7" fill="currentColor" stroke="none"/>'
        '<path d="M3 8c3-1.8 6-1.8 9 0c3-1.8 6-1.8 9 0v12c-3-1.8-6-1.8-9 0c-3-1.8-6-1.8-9 0z"/><path d="M12 8v12"/></svg>')
TEMA = ('<script>try{var t=JSON.parse(localStorage.getItem("logos_tema"));}catch(e){}'
        'if(t!=="claro"&&t!=="escuro")t=matchMedia("(prefers-color-scheme: dark)").matches?"escuro":"claro";'
        'document.documentElement.dataset.tema=t;</script>')


def mil(n):
    return f"{n:,}".replace(",", ".")


def url_de(codigo):
    return f"/lexico/{IDIOMA[codigo[0]][0]}/{int(codigo[1:])}/"


def limpa_forma(p):
    """forma original como está no interlinear, sem as barras e a pontuação ("אֱנֽוֹשׁ\\׃" -> "אֱנֽוֹשׁ")"""
    return re.sub(r"[\\׃׀,.;:·’“”?!]|\s+[ספ]$", "", p).strip()


def limpa_glosa(g):
    g = re.sub(r"\s+", " ", g).strip()
    return re.sub(r"[.,;:!?·]+$", "", g).strip()


def ocorrencias(raiz, livros):
    """{strong: [(livro, cap, v, forma, glosa)]} na ordem do cânon"""
    ordem = {b["id"]: i for i, b in enumerate(livros)}
    oc = collections.defaultdict(list)
    for arq in sorted((raiz / "data" / "interlinear").glob("*/*.json"), key=lambda a: (ordem[a.parent.name], int(a.stem))):
        livro, cap = arq.parent.name, int(arq.stem)
        for v, palavras in enumerate(json.loads(arq.read_text(encoding="utf-8")), 1):
            for p in palavras:
                if p[2]:
                    oc[p[2]].append((livro, cap, v, limpa_forma(p[0]), p[3]))
    return oc


def pagina(*, titulo, desc, css, corpo, seo=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(titulo)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#FAF7F0">
{TEMA}
<link rel="stylesheet" href="{css}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{seo}
</head>
<body>
<header class="topo"><a class="marca" href="/" aria-label="Sola — página inicial">{LOGO}Sola</a>
<nav aria-label="Seções"><a href="/biblia/joao/1/">Bíblia</a><a href="/lexico/">Léxico</a></nav></header>
<main class="lex">
{corpo}
</main>
<footer class="rodape"><em>Sola Scriptura</em> · Estudo bíblico gratuito e em português · <a href="/">solabiblia.com.br</a></footer>
</body>
</html>
"""


def gerar(raiz, site, livros, slug, cortar, cabeca_seo):
    """Grava /lexico/ e devolve a lista de endereços para o sitemap"""
    destino = raiz / "lexico"
    if destino.is_dir():
        shutil.rmtree(destino)
    css = "/lexico.css?v=" + hashlib.sha1((raiz / "lexico.css").read_bytes()).hexdigest()[:10]
    por_id = {b["id"]: b for b in livros}
    texto_bl = {b["id"]: json.loads((raiz / "data" / "bibles" / "blivre" / f"{b['id']}.json").read_text(encoding="utf-8"))
                for b in livros}
    oc = ocorrencias(raiz, livros)
    fonte = ('<p class="fonte">Léxico de Strong (1890), domínio público; definições e usos em tradução automática (Claude). '
             'Interlinear e morfologia: STEPBible/Tyndale House de Cambridge (CC BY). Texto bíblico: Bíblia Livre.</p>')
    urls = []

    def gravar(caminho, conteudo):
        arq = raiz / caminho.strip("/") / "index.html"
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(conteudo, encoding="utf-8")
        urls.append(site + caminho)

    def ref_html(livro, cap, v):
        b = por_id[livro]
        return f'<a class="ref" href="/biblia/{slug(b["pt"])}/{cap}/#v{v}">{e(b["pt"])} {cap}:{v}</a>'

    resumo_idioma = {}
    for L, (pasta, nome_idioma, lang, nome_lexico) in IDIOMA.items():
        dic = json.loads((raiz / "data" / "strongs" / f"{L}.json").read_text(encoding="utf-8"))
        codigos = sorted(dic, key=lambda k: int(k[1:]))
        resumo_idioma[L] = (codigos, dic)
        for n, cod in enumerate(codigos):
            ent = dic[cod]
            lista = oc.get(cod, [])
            defpt = ent.get("defpt") or ent.get("def") or ""
            curta = cortar(defpt, 38)
            versos = list(dict.fromkeys((l, c, v) for l, c, v, _, _ in lista))
            titulo = f"{ent['lemma']} ({ent['translit']}) — {cod}: {curta} | Léxico {pasta} | Sola"
            ponto = "" if defpt.rstrip().endswith((".", "!", "?")) else "."
            desc = cortar(f"{cod} {ent['lemma']} ({ent['translit']}): {defpt}{ponto}"
                          + (f" Aparece {mil(len(lista))} {'vez' if len(lista) == 1 else 'vezes'} na Bíblia." if lista else ""), 158)
            caminho = url_de(cod)
            migalhas = [("Sola", "/"), ("Léxico", "/lexico/"), (nome_idioma, f"/lexico/{pasta}/"), (cod, caminho)]
            termo = {"@context": "https://schema.org", "@type": "DefinedTerm", "name": ent["lemma"],
                     "alternateName": ent["translit"], "termCode": cod, "description": defpt,
                     "inDefinedTermSet": f"{site}/lexico/{pasta}/"}
            seo = cabeca_seo(site + caminho, f"{ent['lemma']} ({ent['translit']}) — {cod} | Sola", desc, "article", migalhas) + \
                f'\n<script type="application/ld+json">{json.dumps(termo, ensure_ascii=False)}</script>'
            corpo = [f'<p class="lex-sobre"><a href="/lexico/">Léxico de Strong</a> · <a href="/lexico/{pasta}/">{nome_idioma}</a> · {cod}</p>',
                     f'<h1><span class="lema" lang="{lang}">{e(ent["lemma"])}</span></h1>',
                     f'<p class="lex-translit">{e(ent["translit"])}<b>{cod}</b></p>',
                     f'<p class="lex-resumo">{e(defpt)}</p>']
            if ent.get("usopt"):
                corpo.append(f'<h2>Como a KJV traduz</h2><p>{e(ent["usopt"])}</p>')
            if lista:
                # "amor" e "Amor" contam juntas; aparece a grafia mais comum
                formas, glosas = collections.defaultdict(collections.Counter), collections.Counter()
                for g in (limpa_glosa(x[4]) for x in lista):
                    if g:
                        glosas[g.lower()] += 1
                        formas[g.lower()][g] += 1
                corpo.append('<h2>Como o interlinear do Sola traduz</h2><ul class="lex-glosas">' +
                             "".join(f"<li>{e(formas[g].most_common(1)[0][0])}<b>{mil(q)}</b></li>"
                                     for g, q in glosas.most_common(14)) + "</ul>")
                por_livro = collections.Counter(l for l, _, _, _, _ in lista)
                vezes = f"{mil(len(lista))} {'vez' if len(lista) == 1 else 'vezes'}"
                em = f"{mil(len(versos))} {'versículo' if len(versos) == 1 else 'versículos'}"
                corpo.append(f'<h2>Onde aparece</h2><p>{vezes} em {em}, em {len(por_livro)} '
                             f'{"livro" if len(por_livro) == 1 else "livros"}.</p>')
                if len(por_livro) > 1:
                    corpo.append('<ul class="lex-livros">' + "".join(
                        f'<li>{e(por_id[l]["pt"])}<span>{q}</span></li>' for l, q in por_livro.items()) + "</ul>")
                primeira = {}
                for l, c, v, forma, glosa in lista:
                    primeira.setdefault((l, c, v), (forma, glosa))
                itens = []
                for l, c, v in versos[:VERSOS_COM_TEXTO]:
                    forma, glosa = primeira[(l, c, v)]
                    try:
                        txt = texto_bl[l][c - 1][v - 1]
                    except IndexError:
                        txt = ""
                    itens.append(f'<li>{ref_html(l, c, v)}<span class="forma" lang="{lang}">{e(forma)}</span>'
                                 f'<span class="glosa">{e(limpa_glosa(glosa))}</span><p>{e(txt)}</p></li>')
                corpo.append('<ol class="lex-versos">' + "".join(itens) + "</ol>")
                resto = versos[VERSOS_COM_TEXTO:]
                if resto:
                    links = ", ".join(ref_html(l, c, v) for l, c, v in resto[:MAIS_REFERENCIAS])
                    sobra = len(resto) - MAIS_REFERENCIAS
                    fim = f" e mais {mil(sobra)} versículos." if sobra > 0 else "."
                    corpo.append(f'<p class="lex-mais"><strong>Outros versículos:</strong> {links}{fim}</p>')
                l, c, v = versos[0]
                corpo.append(f'<a class="lex-abrir" href="/biblia/{slug(por_id[l]["pt"])}/{c}/#v{v}">'
                             f'Estudar no Sola: {e(por_id[l]["pt"])} {c}:{v}</a>')
            else:
                corpo.append('<h2>Onde aparece</h2><p>Esta entrada não está marcada no interlinear do Sola (o Strong pode '
                             'ser só uma variante ou uma raiz que aparece apenas em palavras derivadas).</p>')
            if ent.get("def"):
                corpo.append(f'<h2>Definição original (inglês)</h2><p class="lex-ingles">{e(ent["def"])}'
                             + (f'<br><strong>KJV:</strong> {e(ent["kjv"])}' if ent.get("kjv") else "") + "</p>")
            ant = codigos[n - 1] if n else None
            pro = codigos[n + 1] if n + 1 < len(codigos) else None
            corpo.append('<nav class="lex-viz">' +
                         (f'<a href="{url_de(ant)}">‹ {ant} <span lang="{lang}">{e(dic[ant]["lemma"])}</span></a>' if ant else "<span></span>") +
                         (f'<a href="{url_de(pro)}">{pro} <span lang="{lang}">{e(dic[pro]["lemma"])}</span> ›</a>' if pro else "<span></span>") +
                         "</nav>")
            corpo.append(fonte)
            gravar(caminho, pagina(titulo=titulo, desc=desc, css=css, corpo="\n".join(corpo), seo=seo))

        # listas de 250 em 250 e o índice do idioma
        faixas = [codigos[i:i + FAIXA] for i in range(0, len(codigos), FAIXA)]
        nomes = [f"{int(f[0][1:])}-{int(f[-1][1:])}" for f in faixas]
        for f, nome in zip(faixas, nomes):
            caminho = f"/lexico/{pasta}/{nome}/"
            itens = "".join(f'<li><a href="{url_de(c)}">{c}<span class="lema" lang="{lang}">{e(dic[c]["lemma"])}</span></a> '
                            f'<small>{e(cortar(dic[c].get("defpt") or dic[c].get("def") or "", 60))}</small></li>' for c in f)
            desc = f"{nome_lexico}: entradas {f[0]} a {f[-1]} do léxico de Strong, com definição em português."
            corpo = (f'<p class="lex-sobre"><a href="/lexico/">Léxico de Strong</a> · <a href="/lexico/{pasta}/">{nome_idioma}</a></p>'
                     f'<h1>{nome_idioma}: {f[0]} a {f[-1]}</h1><ul class="lex-lista">{itens}</ul>{fonte}')
            gravar(caminho, pagina(titulo=f"{nome_lexico}: {f[0]}–{f[-1]} | Sola", desc=desc, css=css,
                                   corpo=corpo, seo=cabeca_seo(site + caminho, f"{nome_lexico}: {f[0]}–{f[-1]}", desc, "website",
                                                               [("Sola", "/"), ("Léxico", "/lexico/"), (nome_idioma, f"/lexico/{pasta}/"),
                                                                (f"{f[0]}–{f[-1]}", caminho)])))
        frequentes = sorted((c for c in codigos if oc.get(c)), key=lambda c: -len(oc[c]))[:40]
        caminho = f"/lexico/{pasta}/"
        desc = (f"{nome_lexico}: as {mil(len(codigos))} entradas do léxico de Strong em português, com definição, "
                f"usos e todos os versículos.")
        corpo = (f'<p class="lex-sobre"><a href="/lexico/">Léxico de Strong</a></p><h1>{nome_lexico}</h1>'
                 f'<p>{mil(len(codigos))} entradas, de {codigos[0]} a {codigos[-1]}.</p>' +
                 '<h2>Entradas</h2><ul class="lex-faixas">' +
                 "".join(f'<li><a href="/lexico/{pasta}/{nm}/">{nm.replace("-", "–")}</a></li>' for nm in nomes) + "</ul>" +
                 '<h2>Palavras mais frequentes</h2><ul class="lex-lista">' +
                 "".join(f'<li><a href="{url_de(c)}">{c}<span class="lema" lang="{lang}">{e(dic[c]["lemma"])}</span></a> '
                         f'<small>{mil(len(oc[c]))}× · {e(cortar(dic[c].get("defpt") or "", 40))}</small></li>'
                         for c in frequentes) + "</ul>" + fonte)
        gravar(caminho, pagina(titulo=f"{nome_lexico} (Strong) em português | Sola", desc=desc, css=css,
                               corpo=corpo, seo=cabeca_seo(site + caminho, nome_lexico, desc, "website",
                                                           [("Sola", "/"), ("Léxico", "/lexico/"), (nome_idioma, caminho)])))

    # /lexico/
    desc = ("Léxico de Strong em português: as palavras gregas e hebraicas da Bíblia com definição, como a KJV traduz, "
            "como o interlinear traduz e todos os versículos.")
    destaques = ["G26", "G5485", "G4102", "G3056", "G1343", "H2617", "H7965", "H3068", "H6662", "H530"]
    destaques = [c for c in destaques if c in resumo_idioma[c[0]][1]]
    corpo = ('<h1>Léxico de Strong</h1><p class="lex-resumo">As palavras do texto original da Bíblia, cada uma com a '
             'definição em português, como a King James a traduz, como o interlinear do Sola a traduz e os versículos onde '
             'aparece.</p><ul class="lex-faixas">' +
             "".join(f'<li><a href="/lexico/{IDIOMA[L][0]}/">{IDIOMA[L][3]} · {mil(len(resumo_idioma[L][0]))} entradas</a></li>'
                     for L in IDIOMA) + '</ul><h2>Para começar</h2><ul class="lex-lista">' +
             "".join(f'<li><a href="{url_de(c)}">{c}<span class="lema" lang="{IDIOMA[c[0]][2]}">'
                     f'{e(resumo_idioma[c[0]][1][c]["lemma"])}</span></a> '
                     f'<small>{e(cortar(resumo_idioma[c[0]][1][c].get("defpt", ""), 50))}</small></li>' for c in destaques) +
             "</ul>" + fonte)
    gravar("/lexico/", pagina(titulo="Léxico de Strong em português — grego e hebraico | Sola", desc=desc,
                              css=css, corpo=corpo,
                              seo=cabeca_seo(site + "/lexico/", "Léxico de Strong em português", desc, "website",
                                             [("Sola", "/"), ("Léxico", "/lexico/")])))
    return urls
