"""Páginas estáticas dos Pais da Igreja (data/pais/<obra>.json, importadas por ferramentas/pais_ccel.py): /pais/, a obra
(/pais/agostinho/confissoes/) e um capítulo por página (/pais/agostinho/confissoes/1/1/), com o visual e o topo das
páginas de /confissoes/ (ESTILO e TOPO_CONF do paginas_confissoes.py).

Só ganham página os capítulos já traduzidos (todas as seções com "pt"); os outros aparecem no índice da obra como
"em tradução". Os marcadores [n] das citações bíblicas viram números que levam à lista logo abaixo da seção, com o
versículo da Bíblia Livre. Devolve as páginas e o índice inverso (versículo -> onde a obra o cita), usado nas páginas de
versículo ("Nos pais da Igreja"), e grava o mesmo índice em data/pais/citacoes/<LIVRO>.json ({cap: {v: [[rótulo,
endereço, trecho]]}}), que a Estante do app mostra.

Chamado pelo gerar_paginas.py (não rode sozinho)."""
import json, re, shutil
from html import escape as e

from paginas_confissoes import ESTILO, TOPO_CONF
from paginas_versiculos import pagina_versiculo

RE_MARCA = re.compile(r"\s?\[(\d+)\]")
ROMANOS = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"]
AVISO = ("Texto de domínio público (tradução inglesa do Nicene and Post-Nicene Fathers, 1886); tradução para o português "
         "feita pelo Sola com IA (pode conter imprecisões). As citações bíblicas indicadas são as das notas da edição "
         "inglesa, no texto da Bíblia Livre.")
SOBRE = {"agostinho-confissoes": "O livro em que Agostinho conta a Deus, em forma de oração, a história da sua vida — a "
                                 "infância, os erros da juventude, os maniqueus, a conversão no jardim de Milão e a morte "
                                 "de Mônica — e depois medita sobre a memória, o tempo e a criação."}
ESTILO_PAIS = ESTILO + """<style>
.cf-blocos li.pa-resumo{grid-column:1/-1;margin:-.1rem 0 .2rem;font:italic 400 1rem/1.55 var(--escritura);color:var(--tinta-2)}
.cf-blocos .pa-falta{display:flex;gap:.7rem;align-items:flex-start;padding:.65rem .8rem;border:1px dashed var(--borda);
  border-radius:.5rem;color:var(--suave);font-size:.92rem;line-height:1.4;height:100%}
.cf-blocos .pa-falta b{flex:0 0 auto;min-width:1.9rem;height:1.9rem;display:grid;place-items:center;border-radius:50%;
  background:var(--hover);font:700 .78rem/1 var(--ui)}
.cf-blocos .pa-falta small{font-style:italic}
</style>"""
DESC_PAIS = ("Os Pais da Igreja em português: as obras dos primeiros séculos do cristianismo, em tradução do Sola a partir "
             "de textos em domínio público, com as citações bíblicas ligadas à Bíblia.")


def traduzido(cap):
    return bool(cap.get("titulo")) and all(s.get("pt") for s in cap["secoes"])


def gerar(raiz, site, livros, slug_livro, cortar, cabeca_seo, css):
    info = {b["id"]: b for b in livros}
    biblia = {}

    def texto(l, c, a):
        if l not in biblia:
            biblia[l] = json.loads((raiz / "data" / "bibles" / "blivre" / f"{l}.json").read_text(encoding="utf-8"))
        try:
            return biblia[l][c - 1][a - 1] or ""
        except IndexError:
            return ""

    def rotulo(r):
        l, c, a, b = r[:4]
        if not a:
            return f"{info[l]['pt']} {c}"
        fim = f"-{r[4]}:{b}" if len(r) > 4 else (f"-{b}" if b != a else "")
        return f"{info[l]['pt']} {c}:{a}{fim}"

    def link(r):
        l, c, a = r[:3]
        return f'<a href="/biblia/{slug_livro(info[l]["pt"])}/{c}/{f"{a}/" if a else ""}">{e(rotulo(r))}</a>'

    def secao(sec, ancora):
        corpo = RE_MARCA.sub(lambda m: f'<sup><a href="#{ancora}-{m.group(1)}">{m.group(1)}</a></sup>', e(sec["pt"]))
        pars = "".join(f'<p class="cf-texto">{p}</p>' for p in corpo.split("\n\n"))
        itens = []
        for n in sorted(sec["provas"], key=int):
            refs = sec["provas"][n]
            r0 = refs[0]
            trecho = texto(r0[0], r0[1], r0[2]) if r0[2] else ""
            itens.append(f'<li id="{ancora}-{n}"><b>{n}</b> ' + "; ".join(link(r) for r in refs) +
                         (f'<span>{e(cortar(trecho, 160))}</span>' if trecho else "") + "</li>")
        return pars + (f'<ol class="cf-provas">{"".join(itens)}</ol>' if itens else "")

    urls, citacoes = [], {}

    def frase(txt, n):
        """a frase que termina no marcador [n] (a que faz a citação)"""
        m = re.search(rf"\[{n}\]", txt)
        if not m:
            return txt
        ini = max(txt.rfind(x, 0, m.start() - 1) for x in (". ", "? ", "! ", "; ", "\n"))
        fim = m.start()
        trecho = txt[ini + 1:fim].strip(" —\n")
        if len(trecho) < 40:                             # frase curta: junta a anterior
            ini2 = max(txt.rfind(x, 0, max(ini, 0)) for x in (". ", "? ", "! ", "\n"))
            trecho = txt[ini2 + 1:fim].strip(" —\n")
        return trecho

    def citar(provas, rot, url, txt):
        for n, refs in provas.items():
            item = (rot, url, cortar(re.sub(r"\s+", " ", RE_MARCA.sub("", frase(txt, n))).strip(), 240))
            for r in refs:
                l, c, a, b = r[:4]
                if not a:
                    continue
                texto(l, 1, 1)
                fim = len(biblia[l][c - 1]) if len(r) > 4 else b
                for v in range(a, fim + 1):
                    lista = citacoes.setdefault((l, c, v), [])
                    if not any(x[:2] == item[:2] for x in lista):
                        lista.append(item)

    def gravar(caminho, titulo, desc, corpo, migalhas):
        seo = cabeca_seo(site + caminho, titulo.split(" | ")[0], desc, "article", migalhas)
        seo = seo.replace("/og.png", "/og-confissoes.png")
        arq = raiz / caminho.strip("/") / "index.html"
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(pagina_versiculo(titulo, desc, css, corpo, seo, ESTILO_PAIS, TOPO_CONF, "cf-pag"), encoding="utf-8")
        urls.append(site + caminho)

    if (raiz / "pais").is_dir():                         # capítulo que deixou de existir não fica para trás
        shutil.rmtree(raiz / "pais")
    obras = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((raiz / "data" / "pais").glob("*.json"))]
    cartoes = []
    for obra in obras:
        base = f"/pais/{obra['autor_id']}/{obra['obra_id']}/"
        nome = f"{obra['titulo']}, de {obra['autor'].split(' de ')[0]}"
        fonte = f'<p class="fonte">{AVISO}</p>'
        topo = (f'<p class="lex-sobre"><a href="/pais/">Pais da Igreja</a> · <a href="{base}">{e(obra["titulo"])}</a></p>')
        prontos = [(l, c) for l in obra["livros"] for c in l["caps"] if traduzido(c)]
        for i, (l, c) in enumerate(prontos):
            caminho = f"{base}{l['n']}/{c['n']}/"
            blocos = []
            for s in c["secoes"]:
                blocos.append(f'<h2 class="cf-n" id="s{s["n"]}">§ {s["n"]}</h2>' + secao(s, f"s{s['n']}"))
                citar(s["provas"], f"{obra['autor'].split(' de ')[0]}, {obra['titulo']} {ROMANOS[l['n']]}.{c['n']}",
                      f"{caminho}#s{s['n']}", s["pt"])
            ant = (f'<span>‹ <a href="{base}{prontos[i - 1][0]["n"]}/{prontos[i - 1][1]["n"]}/">'
                   f'{ROMANOS[prontos[i - 1][0]["n"]]}.{prontos[i - 1][1]["n"]}</a></span>') if i else "<span></span>"
            pro = (f'<span><a href="{base}{prontos[i + 1][0]["n"]}/{prontos[i + 1][1]["n"]}/">'
                   f'{ROMANOS[prontos[i + 1][0]["n"]]}.{prontos[i + 1][1]["n"]}</a> ›</span>') if i + 1 < len(prontos) else "<span></span>"
            original = (f'<details class="acv-original"><summary>Texto inglês (Nicene and Post-Nicene Fathers, 1886)</summary>'
                        f'<p><b>{e(c["titulo_en"])}</b></p>' +
                        "".join(f"<p>{e(RE_MARCA.sub('', p))}</p>" for s in c["secoes"] for p in s["en"].split("\n\n")) +
                        "</details>")
            corpo = (f'{topo}<h1>{e(c["titulo"])}</h1><p class="lex-translit">{e(obra["autor"])}, {e(obra["titulo"])}, '
                     f'livro {ROMANOS[l["n"]]}, capítulo {c["n"]}</p>' + "".join(blocos) + original +
                     f'<nav class="lex-viz">{ant}{pro}</nav>{fonte}')
            gravar(caminho, f"{c['titulo']} — {nome}, {ROMANOS[l['n']]}.{c['n']} | Sola",
                   cortar(f"{nome}, livro {ROMANOS[l['n']]}, cap. {c['n']}: {RE_MARCA.sub('', c['secoes'][0]['pt'])}", 158),
                   corpo, [("Sola", "/"), ("Pais da Igreja", "/pais/"), (obra["titulo"], base),
                           (f"Livro {ROMANOS[l['n']]}, capítulo {c['n']}", caminho)])
        # índice da obra: os livros com o resumo e os capítulos (os ainda sem tradução, sem link)
        lista = []
        for l in obra["livros"]:
            lista.append(f'<li class="cf-domingo">Livro {ROMANOS[l["n"]]}</li>')
            if l.get("resumo"):
                lista.append(f'<li class="pa-resumo">{e(l["resumo"])}</li>')
            for c in l["caps"]:
                if traduzido(c):
                    lista.append(f'<li><a href="{base}{l["n"]}/{c["n"]}/"><b>{c["n"]}</b><span>{e(c["titulo"])}</span></a></li>')
                else:
                    lista.append(f'<li><span class="pa-falta"><b>{c["n"]}</b><span>{e(c.get("titulo") or c["titulo_en"])}'
                                 f' <small>(em tradução)</small></span></span></li>')
        n_caps = sum(len(l["caps"]) for l in obra["livros"])
        meta = [obra["ano"], f"{len(obra['livros'])} livros", f"{n_caps} capítulos"]
        if len(prontos) < n_caps:
            meta.append(f"{len(prontos)} traduzidos")
        sobre = SOBRE.get(obra["id"], "")
        gravar(base, f"{nome}, em português | Sola", cortar(f"{nome} em português. {sobre}", 158),
               f'<header class="cf-heroi"><p class="lex-sobre"><a href="/pais/">Pais da Igreja</a> · {e(obra["autor"])}</p>'
               f'<h1>{e(obra["titulo"])}</h1><p class="cf-sub">{e(sobre)}</p><div class="cf-meta">' +
               "".join(f"<span>{e(str(x))}</span>" for x in meta) +
               f'</div></header><ol class="cf-blocos">{"".join(lista)}</ol>{fonte}',
               [("Sola", "/"), ("Pais da Igreja", "/pais/"), (obra["titulo"], base)])
        cartoes.append(f'<a class="cf-cartao" href="{base}"><div class="cf-topo"><h3>{e(obra["titulo"])}</h3>'
                       f'<span class="cf-ano">{e(obra["ano"])}</span></div><p>{e(obra["autor"])}. {e(sobre)}</p>'
                       f'<span class="cf-ler">{len(prontos)} de {n_caps} capítulos · Ler ›</span></a>')
    gravar("/pais/", "Pais da Igreja em português | Sola", DESC_PAIS,
           '<header class="cf-heroi"><p class="lex-sobre">Os primeiros séculos</p><h1>Pais da <em>Igreja</em></h1>'
           f'<p class="cf-sub">{e(DESC_PAIS)}</p></header><div class="cf-cartoes">{"".join(cartoes)}</div>'
           f'<p class="fonte">{AVISO}</p>', [("Sola", "/"), ("Pais da Igreja", "/pais/")])
    # o índice também em data/, por livro, para a Estante do app
    pasta = raiz / "data" / "pais" / "citacoes"
    if pasta.exists():
        for f in pasta.glob("*.json"):
            f.unlink()
    pasta.mkdir(parents=True, exist_ok=True)
    por_livro = {}
    for (l, c, v), lista in sorted(citacoes.items()):
        por_livro.setdefault(l, {}).setdefault(str(c), {})[str(v)] = [list(x) for x in lista]
    for l, caps in por_livro.items():
        (pasta / f"{l}.json").write_text(json.dumps(caps, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return urls, citacoes
