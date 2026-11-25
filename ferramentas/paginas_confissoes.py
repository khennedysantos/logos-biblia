"""Páginas estáticas dos símbolos de fé (data/confissoes/): /confissoes/, os credos antigos (/confissoes/credos/niceno/),
a Confissão de Westminster por capítulo
(/confissoes/westminster/11/), o Catecismo Maior e o Breve Catecismo por pergunta (/confissoes/catecismo-maior/71/)
os Cânones de Dort por capítulo (/confissoes/canones-de-dort/1/), a Confissão Belga por artigo
(/confissoes/confissao-belga/22/) e o Catecismo de Heidelberg por pergunta (/confissoes/heidelberg/1/).

Chamado pelo gerar_paginas.py (não rode sozinho). Mesmo esquema das outras páginas avulsas (HTML leve, /lexico.css).
Os marcadores dos textos de prova ([1], [2]…) viram números que levam às provas logo abaixo do parágrafo, cada uma
com o versículo da Bíblia Livre. Devolve também o índice inverso (versículo -> onde é citado), usado nas páginas de
versículo, e grava o mesmo índice em data/confissoes/citacoes/<LIVRO>.json ({cap: {v: [[rótulo, endereço,
trecho]]}}, sem a Confissão de Westminster, que o app mostra pelo doutrinas.json), usado na aba de referências da
estante."""
import json, re
from html import escape as e

from paginas_versiculos import pagina_versiculo

RE_MARCA = re.compile(r"\s?\[(\d+)\]")
DESCRICAO = {
    "credos": "Os credos da Igreja antiga: o Credo Apostólico, o Credo Niceno, o Credo de Atanásio e a Definição de "
              "Calcedônia, base comum da fé cristã que os Padrões de Westminster pressupõem.",
    "westminster": "Os 33 capítulos da Confissão de Fé de Westminster (1647), o principal símbolo de fé presbiteriano, "
                   "com os textos de prova da própria Assembleia.",
    "catecismo-maior": "As 196 perguntas e respostas do Catecismo Maior de Westminster (1647), com os textos de prova.",
    "breve-catecismo": "As 107 perguntas e respostas do Breve Catecismo de Westminster (1647), a começar por "
                       "“Qual é o fim principal do homem?”.",
    "canones-de-dort": "Os Cânones do Sínodo de Dort (1619): os cinco pontos da doutrina reformada da graça, com a "
                       "rejeição dos erros.",
    "confissao-belga": "Os 37 artigos da Confissão Belga (1561), escrita por Guido de Brès e revista no Sínodo de Dort "
                       "(1619), com os textos de prova da edição francesa.",
    "heidelberg": "As 129 perguntas e respostas do Catecismo de Heidelberg (1563), nos 52 Domingos, a começar por "
                  "“Qual é o teu único consolo na vida e na morte?”.",
    "confissao-batista-1689": "Os 32 capítulos da Segunda Confissão de Fé Batista de Londres (redigida em 1677 e "
                              "adotada em 1689), o principal símbolo de fé batista reformado, feita sobre a Confissão "
                              "de Westminster.",
}
AVISO_CREDOS = ("Textos antigos, em domínio público. Tradução do Sola, feita com IA a partir do latim e do grego e "
                "conferida com textos ingleses em domínio público (pode conter imprecisões).")
AVISO = ("Texto de domínio público; tradução automática do original inglês, feita pelo Sola (pode conter "
         "imprecisões). Textos de prova da Assembleia de Westminster, no texto da Bíblia Livre.")
AVISO_SCHAFF = ("Texto de domínio público, do inglês publicado por Philip Schaff (The Creeds of Christendom, 1877); "
                "tradução do Sola, feita com IA (pode conter imprecisões).")
AVISO_1689 = ("Texto de domínio público (edição inglesa de 1677/1689); tradução do Sola, feita com IA a partir da "
              "tradução da Confissão de Westminster nos trechos em comum (pode conter imprecisões). Esta edição não "
              "traz os textos de prova.")
AVISOS = {"credos": AVISO_CREDOS, "heidelberg": AVISO_SCHAFF, "confissao-batista-1689": AVISO_1689,
          "confissao-belga": AVISO_SCHAFF + " Textos de prova da edição francesa, no texto da Bíblia Livre."}
# as páginas das confissões se vestem como o app (topo com a marca e botões, cartões por tradição); o estilo vai só nelas,
# num <style> no <head>, para não mudar o lexico.css (que reescreveria as ~55 mil páginas avulsas)
TRADICOES = [("Igreja antiga", "A fé comum dos primeiros séculos", ["credos"]),
             ("Padrões de Westminster", "Presbiterianos, 1647", ["westminster", "catecismo-maior", "breve-catecismo"]),
             ("Três Formas de Unidade", "Reformados continentais", ["confissao-belga", "heidelberg", "canones-de-dort"]),
             ("Batista reformada", "Batistas particulares, Londres", ["confissao-batista-1689"])]
RESUMO = {"credos": "Apostólico, Niceno, Atanásio e Calcedônia: a fé que toda a Igreja confessa.",
          "westminster": "O principal símbolo de fé presbiteriano, com os textos de prova da Assembleia.",
          "catecismo-maior": "Para o ensino na igreja: a doutrina e os deveres, com os textos de prova.",
          "breve-catecismo": "Para as famílias, a começar por “Qual é o fim principal do homem?”.",
          "confissao-belga": "Escrita por Guido de Brès e revista no Sínodo de Dort.",
          "heidelberg": "Dividido em 52 Domingos, a começar pelo único consolo na vida e na morte.",
          "canones-de-dort": "Os cinco pontos da doutrina da graça e a rejeição dos erros.",
          "confissao-batista-1689": "A Segunda Confissão de Londres, feita sobre a de Westminster."}
NAV_CONF = ('<nav aria-label="Seções"><a href="/biblia/joao/1/">Bíblia</a><a href="/confissoes/" class="ativa">Confissões</a>'
            '<a href="/lexico/">Léxico</a><a href="/dicionario/">Dicionário</a><a href="/temas/">Temas</a>'
            '<a href="/" class="cf-abrir">Abrir o Sola</a></nav>')
ESTILO = """<style>
.cf-pag .topo{position:sticky;top:0;z-index:5;padding:.6rem clamp(1rem,3.5vw,2.4rem);gap:.8rem;flex-wrap:wrap;
  background:color-mix(in srgb,var(--papel) 92%,transparent);backdrop-filter:blur(8px)}
.cf-pag .marca{font-size:1.25rem;letter-spacing:.42em;text-transform:uppercase}
.cf-pag .topo nav{gap:.4rem;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;max-width:100%}
.cf-pag .topo nav::-webkit-scrollbar{display:none}
.cf-pag .topo nav a{white-space:nowrap;padding:.38rem .8rem;border:1px solid var(--borda);border-radius:999px;background:var(--painel);
  font-size:.8rem;font-weight:500;color:var(--tinta-2)}
.cf-pag .topo nav a:hover{border-color:var(--rubrica);color:var(--rubrica)}
.cf-pag .topo nav a.ativa{background:var(--rubrica-suave);border-color:var(--rubrica);color:var(--rubrica)}
.cf-pag .topo nav a.cf-abrir{background:var(--rubrica);border-color:var(--rubrica);color:#FAF7F0;font-weight:600}
[data-tema="escuro"] .cf-pag .topo nav a.cf-abrir{color:#171613}
.cf-pag .lex{max-width:58rem}
.cf-heroi{margin:.6rem 0 1.6rem;padding:1.6rem clamp(1.1rem,4vw,2.2rem);border-radius:.7rem;background:var(--noite);color:var(--marfim);
  border:1px solid rgba(212,174,106,.25);box-shadow:0 18px 40px rgba(30,22,10,.16);position:relative;overflow:hidden}
.cf-heroi::after{content:"";position:absolute;inset:.45rem;border:1px solid rgba(212,174,106,.18);border-radius:.5rem;pointer-events:none}
.cf-heroi .lex-sobre,.cf-heroi .lex-sobre a{color:var(--ouro-noite)}
.cf-heroi h1{color:var(--marfim);margin:.3rem 0 .5rem}
.cf-heroi h1 em{font-style:italic;color:var(--ouro-noite);font-weight:500}
.cf-heroi p.cf-sub{margin:0;max-width:40rem;font:400 1.08rem/1.6 var(--escritura);color:rgba(244,239,228,.82)}
.cf-heroi .cf-meta{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:1rem}
.cf-heroi .cf-meta span{font:600 .72rem/1 var(--ui);letter-spacing:.08em;text-transform:uppercase;padding:.45rem .7rem;border-radius:999px;
  border:1px solid rgba(212,174,106,.35);color:var(--ouro-noite)}
.cf-trad{margin:1.8rem 0 .7rem;display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap;padding:0;border:0}
.cf-trad b{font:700 .7rem/1 var(--ui);letter-spacing:.2em;text-transform:uppercase;color:var(--rubrica)}
.cf-trad span{font-size:.8rem;color:var(--suave)}
.cf-cartoes{display:grid;grid-template-columns:repeat(auto-fill,minmax(16rem,1fr));gap:.8rem}
.cf-cartao{display:flex;flex-direction:column;gap:.35rem;padding:1rem 1.1rem;border:1px solid var(--borda);border-radius:.6rem;
  background:var(--painel);text-decoration:none;color:var(--tinta);transition:border-color .15s,transform .15s}
.cf-cartao:hover{border-color:var(--rubrica);transform:translateY(-1px)}
.cf-cartao .cf-topo{display:flex;justify-content:space-between;align-items:baseline;gap:.6rem}
.cf-cartao h3{margin:0;font:600 1.3rem/1.15 var(--titulo);color:var(--tinta)}
.cf-cartao .cf-ano{font:600 .72rem/1 var(--ui);color:var(--ouro);white-space:nowrap}
.cf-cartao p{margin:0;font-size:.86rem;line-height:1.5;color:var(--tinta-2)}
.cf-cartao .cf-ler{margin-top:auto;padding-top:.3rem;font:600 .78rem/1 var(--ui);color:var(--rubrica)}
.cf-blocos{list-style:none;padding:0;margin:.4rem 0 1.2rem;display:grid;grid-template-columns:repeat(auto-fill,minmax(15rem,1fr));gap:.5rem}
.cf-blocos li.cf-domingo{grid-column:1/-1;margin:.9rem 0 .1rem;font:700 .7rem/1 var(--ui);letter-spacing:.18em;text-transform:uppercase;color:var(--ouro)}
.cf-blocos a{display:flex;gap:.7rem;align-items:flex-start;padding:.65rem .8rem;border:1px solid var(--borda);border-radius:.5rem;
  background:var(--painel);text-decoration:none;color:var(--tinta);font-size:.92rem;line-height:1.4;height:100%}
.cf-blocos a:hover{border-color:var(--rubrica);color:var(--rubrica)}
.cf-blocos a b{flex:0 0 auto;min-width:1.9rem;height:1.9rem;display:grid;place-items:center;border-radius:50%;background:var(--rubrica-suave);
  color:var(--rubrica);font:700 .78rem/1 var(--ui)}
.cf-pag .lex-viz a{display:inline-block;padding:.4rem .85rem;border:1px solid var(--borda);border-radius:999px;background:var(--painel);text-decoration:none}
.cf-pag .lex-viz a:hover{border-color:var(--rubrica)}
.cf-pag main.lex>h1{margin-bottom:.35rem}
.cf-pag main.lex>.lex-translit{padding-bottom:1.1rem;margin-bottom:1.5rem;border-bottom:1px solid var(--borda);
  box-shadow:0 3px 0 -2px var(--ouro)}
.cf-pag .lex-viz span{flex:1 1 0}
.cf-pag .lex-viz span+span{text-align:right}
@media (max-width:560px){.cf-pag .marca{letter-spacing:.3em}.cf-pag .topo{gap:.5rem;position:sticky}
  .cf-pag .topo nav a.cf-abrir{position:absolute;top:.6rem;right:1rem;padding:.32rem .7rem}}
</style>"""
CURTO = {"breve-catecismo": "Breve Catecismo de Westminster", "catecismo-maior": "Catecismo Maior de Westminster",
         "heidelberg": "Catecismo de Heidelberg"}


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
            return f"{info[l]['pt']} {c}" + (f"-{r[4]}" if len(r) > 4 else "")
        fim = f"-{r[4]}:{b}" if len(r) > 4 else (f"-{b}" if b != a else "")
        return f"{info[l]['pt']} {c}:{a}{fim}"

    def link(r):
        l, c, a = r[:3]
        alvo = f"/biblia/{slug_livro(info[l]['pt'])}/{c}/" + (f"{a}/" if a else "")
        return f'<a href="{alvo}">{e(rotulo(r))}</a>'

    def paragrafo(txt, provas, ancora):
        """texto com os marcadores [n] como números que levam à lista de provas logo abaixo"""
        corpo = RE_MARCA.sub(lambda m: f'<sup><a href="#{ancora}-{m.group(1)}">{m.group(1)}</a></sup>', e(txt))
        corpo = corpo.replace("\n", "<br>")                # o Credo e os Dez Mandamentos no Heidelberg, linha a linha
        lista = ""
        if provas:
            itens = []
            for n in sorted(provas, key=int):
                refs = provas[n]
                if not refs:
                    continue
                primeira = refs[0]
                trecho = texto(primeira[0], primeira[1], primeira[2] or 1)
                itens.append(f'<li id="{ancora}-{n}"><b>{n}</b> ' + "; ".join(link(r) for r in refs) +
                             (f'<span>{e(cortar(trecho, 160))}</span>' if trecho else "") + "</li>")
            lista = f'<ol class="cf-provas">{"".join(itens)}</ol>'
        return f'<p class="cf-texto">{corpo}</p>{lista}'

    urls, citacoes = [], {}

    def citar(provas, rot, url, trecho=""):
        item = (rot, url, cortar(re.sub(r"\s+", " ", RE_MARCA.sub("", trecho)).strip(), 240))
        for refs in provas.values():
            for r in refs:
                l, c, a, b = r[:4]
                if not a:
                    continue
                fim = len(biblia[l][c - 1]) if len(r) > 4 else b       # de um capítulo a outro: até o fim do primeiro
                for v in range(a, fim + 1):
                    lista = citacoes.setdefault((l, c, v), [])
                    if not any(c[:2] == item[:2] for c in lista):
                        lista.append(item)

    def gravar(caminho, titulo, desc, corpo, migalhas):
        seo = cabeca_seo(site + caminho, titulo.split(" | ")[0], desc, "article", migalhas)
        arq = raiz / caminho.strip("/") / "index.html"
        arq.parent.mkdir(parents=True, exist_ok=True)
        arq.write_text(pagina_versiculo(titulo, desc, css, corpo, seo, ESTILO, NAV_CONF, "cf-pag"), encoding="utf-8")
        urls.append(site + caminho)

    docs = [json.loads((raiz / "data" / "confissoes" / f"{d}.json").read_text(encoding="utf-8"))
            for d in ("credos", "westminster", "catecismo-maior", "breve-catecismo", "confissao-belga", "heidelberg",
                      "canones-de-dort", "confissao-batista-1689")]
    for l in info:                                       # carrega a Bíblia Livre (para o fim dos capítulos)
        texto(l, 1, 1)
    tamanhos = {}
    for doc in docs:
        d, nome = doc["id"], doc["titulo"]
        base = f"/confissoes/{d}/"
        fonte = f'<p class="fonte">{AVISOS.get(d, AVISO)}</p>'
        topo = f'<p class="lex-sobre"><a href="/confissoes/">Confissões e catecismos</a> · <a href="{base}">{e(nome)}</a></p>'
        if doc["tipo"] == "credos":
            itens = doc["itens"]
            for i, c in enumerate(itens):
                caminho = f"{base}{c['id']}/"
                notas = "".join(f'<p class="cf-nota"><b>“{e(trecho)}”</b> — {e(texto)} <a href="{url}">{e(rot)}</a></p>'
                                for trecho, texto, url, rot in c["notas"])
                ant = f'<span>‹ <a href="{base}{itens[i - 1]["id"]}/">{e(itens[i - 1]["titulo"])}</a></span>' if i else "<span></span>"
                pro = f'<span><a href="{base}{itens[i + 1]["id"]}/">{e(itens[i + 1]["titulo"])}</a> ›</span>' if i + 1 < len(itens) else "<span></span>"
                corpo = (f'{topo}<h1>{e(c["titulo"])}</h1><p class="lex-translit">{e(c["quando"][:1].upper() + c["quando"][1:])}; original em {e(c["lingua"])}</p>'
                         f'<p class="lex-resumo">{e(c["sobre"])}</p>'
                         + "".join(f'<p class="cf-texto">{e(par)}</p>' for par in c["texto"])
                         + (f'<h2 class="cf-n">Notas</h2>{notas}' if notas else "")
                         + f'<details class="acv-original"><summary>Texto inglês de referência — {e(c["fonte_en"])}</summary>'
                         + "".join(f"<p>{e(par)}</p>" for par in c["texto_en"]) + "</details>"
                         + f'<nav class="lex-viz">{ant}{pro}</nav>{fonte}')
                gravar(caminho, f"{c['titulo']} em português: texto completo | Sola", cortar(f"{c['titulo']}: {' '.join(c['texto'])}", 158),
                       corpo, [("Sola", "/"), ("Confissões", "/confissoes/"), (nome, base), (c["titulo"], caminho)])
            lista = "".join(f'<li><a href="{base}{c["id"]}/"><b>{i + 1}</b><span>{e(c["titulo"])} <small>{e(c["quando"])}</small></span></a></li>'
                            for i, c in enumerate(itens))
            tamanho = [f"{len(itens)} credos"]
        elif doc["tipo"] == "catecismo":
            itens = doc["itens"]
            for i, q in enumerate(itens):
                p, r = q.get("p") or q["p_en"], q.get("r") or q["r_en"]
                caminho = f"{base}{q['n']}/"
                curto = CURTO[d]
                citar(q["provas"], f"{curto.removesuffix(' de Westminster')}, pergunta {q['n']}", caminho, f"{p} {r}")
                ant = f'<span>‹ <a href="{base}{itens[i - 1]["n"]}/">Pergunta {itens[i - 1]["n"]}</a></span>' if i else "<span></span>"
                pro = f'<span><a href="{base}{itens[i + 1]["n"]}/">Pergunta {itens[i + 1]["n"]}</a> ›</span>' if i + 1 < len(itens) else "<span></span>"
                domingo = f'<p class="lex-translit">{e(nome)}, Domingo {q["domingo"]}</p>' if "domingo" in q else ""
                original = "Texto inglês (1863)" if d == "heidelberg" else "Original inglês (1647)"
                corpo = (f'{topo}<h1>Pergunta {q["n"]}</h1>{domingo}<p class="lex-resumo">{e(p)}</p>' +
                         paragrafo(r, q["provas"], f"p{q['n']}") +
                         f'<details class="acv-original"><summary>{original}</summary><p>{e(q["p_en"])}</p>'
                         f'<p>{e(RE_MARCA.sub("", q["r_en"])).replace(chr(10), "<br>")}</p></details>'
                         f'<nav class="lex-viz">{ant}{pro}</nav>{fonte}')
                gravar(caminho, f"{curto}, pergunta {q['n']}: {cortar(p, 60)} | Sola",
                       cortar(f"{p} {RE_MARCA.sub('', r)}", 158), corpo,
                       [("Sola", "/"), ("Confissões", "/confissoes/"), (nome, base), (f"Pergunta {q['n']}", caminho)])
            lista = "".join((f'<li class="cf-domingo">Domingo {q["domingo"]}</li>'
                             if q.get("domingo") and (i == 0 or itens[i - 1]["domingo"] != q["domingo"]) else "") +
                            f'<li><a href="{base}{q["n"]}/"><b>{q["n"]}</b><span>{e(q.get("p") or q["p_en"])}</span></a></li>'
                            for i, q in enumerate(itens))
            tamanho = [f"{len(itens)} perguntas"] + ([f"{itens[-1]['domingo']} Domingos"] if "domingo" in itens[-1] else [])
        else:
            partes = doc["partes"]
            nums = [p["n"] for p in partes] if d != "canones-de-dort" else ["1", "2", "3-4", "5"]
            for i, (parte, n) in enumerate(zip(partes, nums)):
                titulo = parte.get("titulo") or parte["titulo_en"]
                caminho = f"{base}{n}/"
                blocos = []
                for it in parte["itens"]:
                    rot_it = it["n"]
                    if d == "canones-de-dort":
                        rot_it = ("Artigo " if it["n"].startswith("A") else "Rejeição dos erros ") + it["n"][1:]
                    elif d == "confissao-belga":
                        rot_it = f"artigo {n}"
                    else:
                        rot_it = f"{n}.{it['n']}"
                    rot_cit = {"westminster": f"Confissão de Westminster {rot_it}", "confissao-belga": f"{nome}, {rot_it}",
                               "canones-de-dort": f"{nome}, capítulo {n}, {rot_it[:1].lower() + rot_it[1:]}"}.get(d, f"{nome} {rot_it}")
                    citar(it["provas"], rot_cit, caminho,
                          it.get("pt") or it["en"])
                    texto_it = paragrafo(it.get("pt") or it["en"], it["provas"], f"s{it['n']}")
                    if d == "confissao-belga":                   # os parágrafos de um artigo, sem título cada um
                        blocos.append(f'<div id="s{it["n"]}">{texto_it}</div>')
                    else:
                        blocos.append(f'<h2 class="cf-n" id="s{it["n"]}">{e(rot_it)}</h2>{texto_it}')
                rot_doc = {"westminster": "Capítulo", "confissao-batista-1689": "Capítulo", "confissao-belga": "Artigo"}.get(d, "Capítulo de doutrina")
                ant = f'<span>‹ <a href="{base}{nums[i - 1]}/">{rot_doc} {nums[i - 1]}</a></span>' if i else "<span></span>"
                pro = f'<span><a href="{base}{nums[i + 1]}/">{rot_doc} {nums[i + 1]}</a> ›</span>' if i + 1 < len(nums) else "<span></span>"
                corpo = (f'{topo}<h1>{e(titulo)}</h1><p class="lex-translit">{e(nome)}, {rot_doc.lower()} {n}</p>'
                         + "".join(blocos) + f'<nav class="lex-viz">{ant}{pro}</nav>{fonte}')
                primeiro = RE_MARCA.sub("", parte["itens"][0].get("pt") or parte["itens"][0]["en"]) if parte["itens"] else ""
                gravar(caminho, f"{nome}, {rot_doc.lower()} {n}: {titulo} | Sola", cortar(f"{titulo}. {primeiro}", 158),
                       corpo, [("Sola", "/"), ("Confissões", "/confissoes/"), (nome, base), (titulo, caminho)])
            lista = "".join(f'<li><a href="{base}{n}/"><b>{n}</b><span>{e(p.get("titulo") or p["titulo_en"])}</span></a></li>'
                            for p, n in zip(partes, nums))
            tamanho = (["5 capítulos de doutrina"] if d == "canones-de-dort" else
                       [f"{len(partes)} artigos" if d == "confissao-belga" else f"{len(partes)} capítulos"])
        tamanhos[d] = tamanho[0]
        tradicao = next(t for t, _, ds in TRADICOES if d in ds)
        gravar(base, f"{nome} ({doc['ano']}) em português | Sola", DESCRICAO[d],
               f'<header class="cf-heroi"><p class="lex-sobre"><a href="/confissoes/">Confissões e catecismos</a> · {e(tradicao)}</p>'
               f'<h1>{e(nome)}</h1><p class="cf-sub">{e(DESCRICAO[d])}</p><div class="cf-meta">'
               + "".join(f"<span>{e(str(x))}</span>" for x in [doc["ano"], *tamanho]) +
               f'</div></header><ol class="cf-blocos">{lista}</ol>{fonte}',
               [("Sola", "/"), ("Confissões", "/confissoes/"), (nome, base)])
    desc = ("Os símbolos de fé em português: os credos da Igreja antiga e, da tradição reformada, os Padrões de "
            "Westminster (a Confissão de Fé, o Catecismo Maior e o Breve Catecismo) e as Três Formas de Unidade (a "
            "Confissão Belga, o Catecismo de Heidelberg e os Cânones de Dort), com os textos de prova, e a Confissão "
            "Batista de Londres de 1689.")
    gravar("/confissoes/", "Confissões e catecismos reformados em português | Sola", desc,
           '<header class="cf-heroi"><p class="lex-sobre">Símbolos de fé</p><h1>Confissões e <em>catecismos</em></h1>'
           f'<p class="cf-sub">{e(desc)}</p></header>' +
           "".join(f'<h2 class="cf-trad"><b>{e(t)}</b><span>{e(sub)}</span></h2><div class="cf-cartoes">' +
                   "".join(f'<a class="cf-cartao" href="/confissoes/{x["id"]}/"><div class="cf-topo"><h3>{e(x["titulo"])}</h3>'
                           f'<span class="cf-ano">{e(str(x["ano"]))}</span></div><p>{e(RESUMO[x["id"]])}</p>'
                           f'<span class="cf-ler">{e(tamanhos[x["id"]])} · Ler ›</span></a>'
                           for x in docs if x["id"] in ds) + "</div>"
                   for t, sub, ds in TRADICOES) +
           f'<p class="fonte">{AVISO}</p>', [("Sola", "/"), ("Confissões", "/confissoes/")])
    # o índice também em data/, por livro, para a estante do app
    pasta = raiz / "data" / "confissoes" / "citacoes"
    if pasta.exists():
        for f in pasta.glob("*.json"):
            f.unlink()
    pasta.mkdir(parents=True, exist_ok=True)
    por_livro = {}
    for (l, c, v), lista in sorted(citacoes.items()):
        outras = [list(x) for x in lista if not x[1].startswith("/confissoes/westminster/")]   # a CFW o app já tem
        if outras:
            por_livro.setdefault(l, {}).setdefault(str(c), {})[str(v)] = outras
    for l, caps in por_livro.items():
        (pasta / f"{l}.json").write_text(json.dumps(caps, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return urls, citacoes
