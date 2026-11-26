"""Páginas estáticas do Dicionário Bíblico de Easton (/dicionario/<verbete>/) e do índice temático de Nave
(/temas/<tema>/), com índices por letra (/dicionario/letra/a/, /temas/letra/a/).

Chamado pelo gerar_paginas.py (não rode sozinho). Mesmo esquema das páginas do léxico (paginas_lexico.py): HTML avulso
e leve, sem o app, com a folha /lexico.css; as referências bíblicas ("GEN 3:15; 4:1") viram links para o capítulo no
Sola, como o linkarRefs do app.js, e as remissões ("Veja FERRO") viram links para a página do outro verbete.

Endereço: o título em português (titulos_pt.json), ou o nome em inglês quando não há título. Se dois verbetes caem no
mesmo endereço, o mais completo fica com o endereço simples e os outros ganham o nome em inglês no fim; essas exceções
vão para data/dictionary/enderecos.json e data/topics/enderecos.json ({nome em inglês: endereço}), que o app
consulta (gerados aqui, não edite)."""
import json, re, shutil, unicodedata
from html import escape as e

from paginas_lexico import mil, pagina

RE_REF = re.compile(r"(?:\b([1-3]?[A-Z]{2,3}) )?(\d+)(?::(\d+))?((?:[-–]\d+(?::\d+)?)?(?:, ?\d+(?:[-–]\d+)?(?![\dA-Z]))*)")
RE_VEJA = re.compile(r"\b(Veja(?: também)?,? )([A-ZÀ-Ú][A-ZÀ-Ú0-9 ,'()\-]*[A-ZÀ-Ú)])")
ACERVOS = {
    # pasta de dados, endereço, nome, nome curto, fonte, maiúsculas nos nomes em inglês
    "dictionary": ("dicionario", "Dicionário Bíblico", "Dicionário",
                   "Dicionário Bíblico de Easton (1897), domínio público. Tradução automática do original em inglês (Claude); "
                   "pode conter imprecisões. Texto bíblico: Bíblia Livre."),
    "topics": ("temas", "Temas bíblicos", "Temas",
               "Índice temático de Nave (Nave's Topical Bible, 1897), domínio público. Tradução automática do original em "
               "inglês (Claude); pode conter imprecisões."),
}


def slug_url(nome):
    """o mesmo do app.js (slugAcervo): sem acento, minúsculas, o resto vira hífen"""
    s = unicodedata.normalize("NFD", nome)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def titulo_de(chave, tit):
    if tit.get(chave):
        return tit[chave]
    return chave.title() if chave.isupper() else chave       # "BATH-SHEBA" -> "Bath-Sheba"


def linkar(txt, livros_info, slug_livro):
    """port do linkarRefs do app.js: "GEN 3:15; 4:1" -> links com o nome do livro em português"""
    saida, fim, livro = [], 0, None
    for m in RE_REF.finditer(txt):
        cod, c, v, resto = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        seguida = livro and re.fullmatch(r"\s*;\s*", txt[fim:m.start()])
        l = (cod if cod in livros_info else None) if cod else (livro if seguida else None)
        if not l or not 1 <= int(c) <= livros_info[l]["ch"]:
            if cod:
                livro = None
            continue
        nome = livros_info[l]["pt"] + " " if cod and not (seguida and cod == livro) else ""
        alvo = f"/biblia/{slug_livro(livros_info[l]['pt'])}/{int(c)}/" + (f"#v{int(v)}" if v else "")
        saida += [e(txt[fim:m.start()]), f'<a href="{alvo}">{e(nome + c + (":" + v if v else "") + resto)}</a>']
        fim, livro = m.end(), l
    return "".join(saida) + e(txt[fim:])


def refs_por_extenso(txt, info):
    """ "GEN 1:1; 2" -> "Gênesis 1:1; 2": para a descrição que o Google mostra, onde link não existe."""
    return re.sub(r"\b([1-3]?[A-Z]{2,3})(?= \d)", lambda m: info[m.group(1)]["pt"] if m.group(1) in info else m.group(0), txt)


def descricao_tema(titulo, linhas, info):
    """Descrição do tema para buscadores: os subtemas com as referências por extenso e, no fim, as remissões
    ("Veja ANIMAIS") como "Veja também: Animais, …" — em vez das linhas cruas, que o Google ignorava."""
    partes, vejas = [], []
    for x in linhas:
        m = re.match(r"(?i)veja(?: também)?\s+(.+)", x)
        if m:
            vejas.append(m.group(1).strip(" .,;").capitalize())
        else:
            partes.append(refs_por_extenso(x.rstrip(" .;"), info))
    corpo = "; ".join(p[:1].lower() + p[1:] if p[:2] != p[:2].upper() else p for p in partes)
    txt = f"{titulo} na Bíblia" + (f": {corpo}." if corpo else ".")
    if vejas:
        txt += " Veja também: " + ", ".join(vejas[:8]) + "."
    return txt


def gerar(raiz, site, livros, slug_livro, cortar, cabeca_seo):
    css = re.search(r'href="(/lexico\.css\?v=[0-9a-f]+)"', (raiz / "lexico" / "index.html").read_text(encoding="utf-8")).group(1)
    info = {b["id"]: b for b in livros}
    urls = []

    def gravar(caminho, conteudo):
        arq = raiz / caminho.strip("/") / "index.html"
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(conteudo, encoding="utf-8")
        urls.append(site + caminho)

    for pasta_dados, (pasta, nome_acervo, curto, fonte_txt) in ACERVOS.items():
        destino = raiz / pasta
        if destino.is_dir():
            shutil.rmtree(destino)
        tit = json.loads((raiz / "data" / pasta_dados / "titulos_pt.json").read_text(encoding="utf-8"))
        pt, en = {}, {}
        for arq in sorted((raiz / "data" / pasta_dados / "pt").glob("[A-Z].json")):     # só as letras (A.json…Z.json)
            pt.update({k: v for k, v in json.loads(arq.read_text(encoding="utf-8")).items() if k != "__pt"})
            en.update(json.loads((raiz / "data" / pasta_dados / arq.name).read_text(encoding="utf-8")))
        # endereços: o verbete mais completo fica com o endereço simples
        grupos = {}
        for k in pt:
            grupos.setdefault(slug_url(titulo_de(k, tit)) or slug_url(k), []).append(k)
        enderecos, excecoes = {}, {}
        for s, ks in grupos.items():
            ks.sort(key=lambda k: (-sum(len(x) for x in pt[k]), k))
            for i, k in enumerate(ks):
                final = s if i == 0 else f"{s}-{slug_url(k)}"
                n = 2
                while final in enderecos.values() or final == "letra":
                    final, n = f"{s}-{slug_url(k)}-{n}", n + 1
                enderecos[k] = final
                if final != s:
                    excecoes[k] = final
        assert len(set(enderecos.values())) == len(enderecos)
        # remissões "Veja FERRO": pelo título em português ou pelo nome em inglês, em maiúsculas
        por_nome = {}
        for k in pt:
            por_nome.setdefault(k.upper(), k)
        for k in pt:
            por_nome.setdefault(titulo_de(k, tit).upper(), k)

        def remissoes(html_txt):
            def troca(m):
                alvo = m.group(2).rstrip(" ,")
                k = por_nome.get(alvo) or por_nome.get(alvo.split(",")[0].strip())
                if not k:
                    return m.group(0)
                return f'{m.group(1)}<a href="/{pasta}/{enderecos[k]}/">{alvo}</a>' + m.group(2)[len(alvo):]
            return RE_VEJA.sub(troca, html_txt)

        ordem = sorted(pt, key=lambda k: (slug_url(titulo_de(k, tit)), k))
        fonte = f'<p class="fonte">{e(fonte_txt)}</p>'
        for n, k in enumerate(ordem):
            titulo = titulo_de(k, tit)
            caminho = f"/{pasta}/{enderecos[k]}/"
            linhas = [x.lstrip("-").strip() for x in pt[k] if x.strip()]
            texto_plano = re.sub(r"\s+", " ", " ".join(linhas))
            nome_en = f' · em inglês: {e(k.title() if k.isupper() else k)}' if titulo.lower() != k.lower() else ""
            corpo = [f'<p class="lex-sobre"><a href="/{pasta}/">{nome_acervo}</a> · '
                     f'<a href="/{pasta}/letra/{slug_url(titulo)[:1] or "outros"}/">{e(titulo[:1].upper())}</a></p>',
                     f'<h1>{e(titulo)}</h1>',
                     f'<p class="lex-translit">{"Easton" if pasta_dados == "dictionary" else "Nave"}{nome_en}</p>']
            if pasta_dados == "dictionary":
                corpo += [f'<p class="acv-def">{remissoes(linkar(x, info, slug_livro))}</p>' for x in linhas]
                originais = [x for x in en.get(k, []) if x.strip()]
                if originais:
                    corpo.append('<details class="acv-original"><summary>Texto original (inglês)</summary>' +
                                 "".join(f"<p>{e(x)}</p>" for x in originais) + "</details>")
                desc = cortar(f"{titulo}: {refs_por_extenso(texto_plano, info)}", 158)
                tipo_titulo = f"{titulo} — significado e referências bíblicas | Dicionário Bíblico | Sola"
                termo = {"@context": "https://schema.org", "@type": "DefinedTerm", "name": titulo,
                         "description": cortar(texto_plano, 300), "inDefinedTermSet": f"{site}/{pasta}/"}
                extra = f'\n<script type="application/ld+json">{json.dumps(termo, ensure_ascii=False)}</script>'
            else:
                corpo.append('<ul class="acv-linhas">' +
                             "".join(f"<li>{remissoes(linkar(x, info, slug_livro))}</li>" for x in linhas) + "</ul>")
                desc = cortar(descricao_tema(titulo, linhas, info), 158)
                tipo_titulo = f"{titulo} na Bíblia — versículos e referências | Temas bíblicos | Sola"
                extra = ""
            ant, pro = (ordem[n - 1] if n else None), (ordem[n + 1] if n + 1 < len(ordem) else None)
            corpo.append('<nav class="lex-viz">' +
                         (f'<a href="/{pasta}/{enderecos[ant]}/">‹ {e(titulo_de(ant, tit))}</a>' if ant else "<span></span>") +
                         (f'<a href="/{pasta}/{enderecos[pro]}/">{e(titulo_de(pro, tit))} ›</a>' if pro else "<span></span>") +
                         "</nav>")
            corpo.append(fonte)
            seo = cabeca_seo(site + caminho, f"{titulo} — {nome_acervo} | Sola", desc, "article",
                             [("Sola", "/"), (curto, f"/{pasta}/"), (titulo, caminho)]) + extra
            gravar(caminho, pagina(titulo=tipo_titulo, desc=desc, css=css, corpo="\n".join(corpo), seo=seo))

        # índices: por letra e geral
        letras = {}
        for k in ordem:
            letras.setdefault(slug_url(titulo_de(k, tit))[:1] or "outros", []).append(k)
        nav_letras = '<ul class="lex-faixas">' + "".join(
            f'<li><a href="/{pasta}/letra/{l}/">{l.upper()}</a></li>' for l in letras) + "</ul>"
        for l, ks in letras.items():
            caminho = f"/{pasta}/letra/{l}/"
            itens = "".join(f'<li><a href="/{pasta}/{enderecos[k]}/">{e(titulo_de(k, tit))}</a></li>' for k in ks)
            desc = f"{nome_acervo}: os {mil(len(ks))} verbetes com a letra {l.upper()}, em português, com as referências bíblicas."
            gravar(caminho, pagina(titulo=f"{nome_acervo}: letra {l.upper()} | Sola", desc=desc, css=css,
                                   corpo=f'<p class="lex-sobre"><a href="/{pasta}/">{nome_acervo}</a></p><h1>{curto}: {l.upper()}</h1>'
                                         f'{nav_letras}<ul class="lex-lista">{itens}</ul>{fonte}',
                                   seo=cabeca_seo(site + caminho, f"{nome_acervo}: {l.upper()}", desc, "website",
                                                  [("Sola", "/"), (curto, f"/{pasta}/"), (l.upper(), caminho)])))
        if pasta_dados == "dictionary":
            intro = (f"Os {mil(len(pt))} verbetes do Dicionário Bíblico de Easton em português: pessoas, lugares, objetos, "
                     "costumes e termos da Bíblia, com as referências que levam direto ao texto.")
            destaques = ["Covenant", "Atonement", "Justification", "Grace", "Elijah", "Jerusalem", "Passover", "Tabernacle"]
        else:
            intro = (f"Os {mil(len(pt))} temas do índice temático de Nave em português: cada assunto da Bíblia com os "
                     "versículos que tratam dele, organizados por tópico.")
            destaques = ["FAITH", "GRACE", "PRAYER", "JESUS, THE CHRIST", "LOVE", "REPENTANCE", "SIN", "HOLY SPIRIT"]
        destaques = [k for k in destaques if k in pt]
        caminho = f"/{pasta}/"
        gravar(caminho, pagina(titulo=f"{nome_acervo} em português — {mil(len(pt))} verbetes | Sola", desc=intro, css=css,
                               corpo=f'<h1>{nome_acervo}</h1><p class="lex-resumo">{e(intro)}</p><h2>Por letra</h2>{nav_letras}'
                                     '<h2>Para começar</h2><ul class="lex-lista">' +
                                     "".join(f'<li><a href="/{pasta}/{enderecos[k]}/">{e(titulo_de(k, tit))}</a></li>' for k in destaques)
                                     + f"</ul>{fonte}",
                               seo=cabeca_seo(site + caminho, nome_acervo, intro, "website", [("Sola", "/"), (curto, caminho)])))
        (raiz / "data" / pasta_dados / "enderecos.json").write_text(json.dumps(excecoes, ensure_ascii=False, sort_keys=True, indent=0) + "\n",
                                                encoding="utf-8")
    return urls
