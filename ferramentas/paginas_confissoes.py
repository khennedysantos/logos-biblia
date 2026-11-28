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
    "breve-catecismo": "As 107 perguntas e respostas do Breve Catecismo de Westminster (1647), com os textos de prova "
                       "da Assembleia, a começar por “Qual é o fim principal do homem?”.",
    "canones-de-dort": "Os Cânones do Sínodo de Dort (1619): os cinco pontos da doutrina reformada da graça, com a "
                       "rejeição dos erros.",
    "confissao-belga": "Os 37 artigos da Confissão Belga (1561), escrita por Guido de Brès e revista no Sínodo de Dort "
                       "(1619), com os textos de prova da edição francesa.",
    "heidelberg": "As 129 perguntas e respostas do Catecismo de Heidelberg (1563), nos 52 Domingos, a começar por "
                  "“Qual é o teu único consolo na vida e na morte?”.",
    "confissao-batista-1644": "Os 53 artigos da Primeira Confissão de Fé Batista de Londres (1644), das sete igrejas "
                              "batistas particulares de Londres, com as notas de margem do original (os textos de prova).",
    "catecismo-batista": "As 114 perguntas e respostas do Catecismo Batista de Benjamin Keach (1693), feito sobre o "
                         "Breve Catecismo de Westminster, com os textos de prova, na edição da Associação de "
                         "Charleston (1813).",
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
              "tradução da Confissão de Westminster nos trechos em comum (pode conter imprecisões). Textos de prova da "
              "edição original, reunidos no fim de cada parágrafo (transcrição do Wikisource), no texto da Bíblia Livre.")
AVISO_1644 = ("Texto de domínio público (Londres, 1644), na transcrição do The Reformed Reader; tradução do Sola, feita com "
              "IA (pode conter imprecisões). Textos de prova das notas de margem do original, no texto da Bíblia Livre; "
              "os títulos dos artigos são do Sola (o original não os tem).")
AVISOS = {"credos": AVISO_CREDOS,
          "heidelberg": AVISO_SCHAFF + " Textos de prova da edição de 1879 da Reformed Church in America (transcrição do "
                        "Wikisource), reunidos por pergunta, no texto da Bíblia Livre.", "confissao-batista-1689": AVISO_1689,
          "confissao-batista-1644": AVISO_1644,
          "catecismo-batista": "Texto de domínio público (edição da Associação Batista de Charleston, 1813), na "
                               "transcrição do The Reformed Reader; tradução do Sola, feita com IA a partir da tradução "
                               "do Breve Catecismo nas respostas em comum (pode conter imprecisões). Textos de prova da "
                               "edição de 1813, no texto da Bíblia Livre.",
          "confissao-belga": AVISO_SCHAFF + " Textos de prova da edição francesa, no texto da Bíblia Livre."}
# as páginas das confissões se vestem como o app (topo com a marca e botões, cartões por tradição); o estilo vai só nelas,
# num <style> no <head>, para não mudar o lexico.css (que reescreveria as ~55 mil páginas avulsas)
TRADICOES = [("Igreja antiga", "A fé comum dos primeiros séculos", ["credos"]),
             ("Padrões de Westminster", "Presbiterianos, 1647", ["westminster", "catecismo-maior", "breve-catecismo"]),
             ("Três Formas de Unidade", "Reformados continentais", ["confissao-belga", "heidelberg", "canones-de-dort"]),
             ("Batista reformada", "Batistas particulares, Londres", ["confissao-batista-1644", "confissao-batista-1689", "catecismo-batista"])]
RESUMO = {"credos": "Apostólico, Niceno, Atanásio e Calcedônia: a fé que toda a Igreja confessa.",
          "westminster": "O principal símbolo de fé presbiteriano, com os textos de prova da Assembleia.",
          "catecismo-maior": "Para o ensino na igreja: a doutrina e os deveres, com os textos de prova.",
          "breve-catecismo": "Para as famílias, a começar por “Qual é o fim principal do homem?”.",
          "confissao-belga": "Escrita por Guido de Brès e revista no Sínodo de Dort.",
          "heidelberg": "Dividido em 52 Domingos, a começar pelo único consolo na vida e na morte.",
          "canones-de-dort": "Os cinco pontos da doutrina da graça e a rejeição dos erros.",
          "confissao-batista-1644": "A Primeira Confissão de Londres, das sete igrejas batistas particulares.",
          "confissao-batista-1689": "A Segunda Confissão de Londres, feita sobre a de Westminster.",
          "catecismo-batista": "O catecismo de Benjamin Keach, feito sobre o Breve Catecismo, com o batismo dos que creem."}
# o topo é o mesmo do app, mas em HTML puro: cada botão é um link para o app com ?abrir=<botão> (o app abre o painel
# ao carregar, lerAbrir). No computador: marca, busca, Bíblia, "Estudar ▾" (um <details>), Confissões e Planos; no
# celular (< 760px): uma faixa só no alto, com o ⋯ (outro <details>), e as abas fixas embaixo, como no app
ESTUDAR = [  # (endereço, ícone, rótulo): o menu "Estudar" (no celular, o ⋯ leva os mesmos, menos "Meu estudo", que é aba)
    ("/?abrir=meu", "progresso", "Meu estudo"), ("/pais/", "pomba", "Pais da Igreja"),
    ("/leituras/", "estante", "Leituras"), ("/?abrir=temas", "temas", "Temas"),
    ("/?abrir=dicionario", "dicionario", "Dicionário"), ("/?abrir=atlas", "atlas", "Atlas"),
    ("/?abrir=tempo", "tempo", "Linha do tempo"), ("/?abrir=notas", "anotacoes", "Anotações"), ("/?abrir=ajuda", "ajuda", "Como usar")]
BARRA = [("/confissoes/", "ancora", "Confissões"), ("/planos/", "planos", "Planos")]
ABAS = [("/", "casa", "Início"), ("/?abrir=livros", "livro", "Bíblia"), ("/?abrir=buscar", "busca", "Buscar"),
        ("/?abrir=meu", "progresso", "Estudo"), ("/confissoes/", "ancora", "Confissões")]
# quantos itens de BARRA cabem ao lado do "Estudar" em cada largura (o resto vai para o menu); medido no app (764 e 890 px)
CABEM_MESA = [(760, 0), (780, 1), (900, 2)]


def _simbolos(ids):
    """os ícones do próprio index.html, para o topo ficar igual ao do app"""
    from pathlib import Path
    html = (Path(__file__).resolve().parents[1] / "index.html").read_text(encoding="utf-8")
    return ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">' +
            "".join(re.search(rf'<symbol id="i-{i}".*?</symbol>', html, re.S).group(0) for i in ids) + "</svg>")


def _ico(nome, classe="ico"):
    return f'<svg class="{classe}" aria-hidden="true"><use href="#i-{nome}"/></svg>'


def _link(end, ico, rot, cls=""):
    atual = end == "/confissoes/"
    cls = (cls + (" ativa" if atual else "")).strip()
    classe = ' class="%s"' % cls if cls else ""
    corrente = ' aria-current="page"' if atual else ""
    return f'<a{classe} href="{end}"{corrente}>{_ico(ico)}<span>{rot}</span></a>'


def _topo():
    estudar = "".join(_link(*x) for x in ESTUDAR)
    barra = "".join(_link(*x, cls=f"b{k}") for k, x in enumerate(BARRA, 1))
    no_menu = "".join(_link(*x, cls=f"m{k}") for k, x in enumerate(BARRA, 1))     # os da barra que não couberem
    cel = _link(*BARRA[1]) + "".join(_link(*x) for x in ESTUDAR[1:])
    abas = "".join(_link(*x) for x in ABAS)
    ids = {"sola", "livro", "chevron", "busca", "mais", "lua", "sol", "pessoa", "lampada", "coracao", "casa"} | {
        x[1] for x in ESTUDAR + BARRA + ABAS}
    return (_simbolos(sorted(ids)) +
            '<header class="topo cf-topo">'
            f'<a class="btn-livros" href="/?abrir=livros">{_ico("livro")} <span>Bíblia</span> {_ico("chevron", "ico ico-seta-baixo")}</a>'
            f'<a class="marca" href="/" aria-label="Sola — página inicial">{_ico("sola", "ico ico-marca")}<span class="nome">Sola</span></a>'
            f'<a class="busca-comando" href="/?abrir=buscar">{_ico("busca")}<span>Passagem, palavra, Strong (G3056) ou doutrina…</span><kbd>/</kbd></a>'
            '<nav class="cf-barra" aria-label="Recursos">'
            f'<details class="cf-menu cf-estudar"><summary><span>Estudar</span>{_ico("chevron", "ico ico-seta-baixo")}</summary>'
            f'<div class="menu-mais">{estudar}{no_menu}</div></details>{barra}</nav>'
            '<div class="topo-acoes"><a class="btn-apoiar" href="/apoiar/" title="Apoiar o projeto">'
            f'{_ico("coracao")}<span>Apoiar</span></a>'
            '<button class="btn-icone" id="cfTema" type="button" aria-label="Alternar tema claro e escuro">'
            f'{_ico("lua", "ico so-claro")}{_ico("sol", "ico so-escuro")}</button>'
            f'<a class="btn-icone" href="/?abrir=perfil" aria-label="Perfil">{_ico("pessoa")}</a>'
            f'<details class="cf-menu cf-mais-cel"><summary class="btn-icone" aria-label="Mais">{_ico("mais")}</summary>'
            f'<div class="menu-mais">{cel}</div></details></div></header>'
            f'<nav class="cf-abas" aria-label="Navegação principal">{abas}</nav>'
            '<script>(function(){var b=document.getElementById("cfTema"),ms=document.querySelectorAll(".cf-menu");'
            'b.onclick=function(){var t=document.documentElement.dataset.tema==="escuro"?"claro":"escuro";'
            'document.documentElement.dataset.tema=t;try{localStorage.setItem("logos_tema",JSON.stringify(t))}catch(e){}};'
            'document.addEventListener("click",function(e){ms.forEach(function(m){if(m.open&&!m.contains(e.target))m.open=false})});'
            'document.addEventListener("keydown",function(e){if(e.key==="Escape")ms.forEach(function(m){m.open=false});'
            'if(e.key==="/"&&!/INPUT|TEXTAREA/.test(e.target.tagName)){e.preventDefault();location.href="/?abrir=buscar"}});})();</script>')


def _regras_cabem():
    """no computador, mostra na barra só os primeiros N itens de BARRA (e esconde do menu "Estudar" esses mesmos N)"""
    regras = []
    for i, (de, cabem) in enumerate(CABEM_MESA):
        ate = CABEM_MESA[i + 1][0] if i + 1 < len(CABEM_MESA) else None
        cond = f"(min-width:{de}px)" + (f" and (max-width:{ate - 1}px)" if ate else "")
        fora = ",".join(f".cf-topo .cf-barra > a.b{k}" for k in range(cabem + 1, len(BARRA) + 1))
        dentro = ",".join(f".cf-menu.cf-estudar .menu-mais a.m{k}" for k in range(1, cabem + 1))
        regras.append(f"@media {cond}{{" + (f"{fora}{{display:none}}" if fora else "") + (f"{dentro}{{display:none}}" if dentro else "") + "}")
    return "\n".join(regras)


TOPO_CONF = _topo()
# modo memorizar nas perguntas dos catecismos (a mesma chave logos_memorizar do plano no app)
MEMO_BOTAO = ('<button type="button" class="cf-memo" aria-pressed="false" title="Esconder a resposta para tentar lembrar">'
              + _ico("lampada") + '<span>Memorizar</span></button>')
MEMO_VER = '<button type="button" class="cf-ver">Mostrar resposta</button>'
MEMO_JS = ('<script>(function(){var m=document.querySelector(".cf-memo");if(!m)return;var r=document.querySelector(".cf-resposta"),'
           'on=false;try{on=JSON.parse(localStorage.getItem("logos_memorizar"))===true}catch(e){}'
           'function por(v,salvar){on=v;document.body.classList.toggle("cf-memorizar",v);m.setAttribute("aria-pressed",v);'
           'r.classList.remove("vista");if(salvar)try{localStorage.setItem("logos_memorizar",JSON.stringify(v))}catch(e){}}'
           'por(on);m.onclick=function(){por(!on,1)};r.querySelector(".cf-ver").onclick=function(){r.classList.add("vista")};})();'
           '</script>')
ESTILO = """<style>
.cf-pag .ico{width:1.05em;height:1.05em;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;
  vertical-align:-.16em;flex:0 0 auto}
[data-tema="escuro"] .so-claro,:root:not([data-tema="escuro"]) .so-escuro{display:none}
.cf-topo{position:sticky;top:0;z-index:30;display:flex;flex-wrap:wrap;align-items:center;justify-content:flex-start;gap:.42rem .55rem;
  padding:.55rem .85rem .4rem;background:color-mix(in srgb,var(--papel) 92%,transparent);
  -webkit-backdrop-filter:saturate(1.3) blur(12px);backdrop-filter:saturate(1.3) blur(12px);border-bottom:1px solid var(--borda)}
.cf-topo .marca{display:flex;align-items:center;gap:.48rem;margin:0 auto;color:var(--tinta);text-decoration:none;font:inherit;letter-spacing:0}
.cf-topo .ico-marca{width:1.38rem;height:1.38rem;color:var(--rubrica);stroke-width:1.6}
.cf-topo .marca .nome{font-family:var(--titulo);font-weight:600;font-size:1.38rem;letter-spacing:.28em;text-transform:uppercase;
  margin-right:-.28em;line-height:1}
.cf-topo .btn-livros,.cf-topo .btn-icone{display:inline-flex;align-items:center;justify-content:center;gap:.4rem;border:1px solid var(--borda);
  background:var(--painel);color:var(--tinta);border-radius:.32rem;cursor:pointer;text-decoration:none;font-family:var(--ui);
  transition:border-color .16s,background .16s}
.cf-topo .btn-livros{padding:.42rem .72rem;font-size:.8rem;font-weight:600}
.cf-topo .btn-livros .ico{color:var(--rubrica)}
.cf-topo .btn-livros .ico-seta-baixo{width:.85em;height:.85em;color:var(--suave);margin-left:-.1rem}
.cf-topo .btn-icone{width:2.1rem;height:2.1rem;padding:0;font-size:.96rem}
.cf-topo .btn-livros:hover,.cf-topo .btn-icone:hover{border-color:var(--suave);background:var(--hover)}
.cf-topo .topo-acoes{display:flex;align-items:center;gap:.35rem}
.cf-topo .btn-apoiar{display:inline-flex;align-items:center;gap:.38rem;height:2.1rem;padding:0 .72rem;border-radius:.32rem;
  border:1px solid color-mix(in srgb,var(--rubrica) 45%,var(--borda));background:var(--rubrica-suave);color:var(--rubrica);
  font:600 .73rem/1 var(--ui);letter-spacing:.03em;white-space:nowrap;text-decoration:none}
.cf-topo .btn-apoiar .ico{fill:currentColor;stroke:none;font-size:.92rem}
.cf-topo .btn-apoiar:hover{border-color:var(--rubrica)}
.cf-topo .busca-comando{display:none;align-items:center;gap:.5rem;height:2.1rem;padding:0 .5rem 0 .7rem;border:1px solid var(--borda);
  border-radius:.32rem;background:var(--mesa);color:var(--suave);font:400 .78rem/1 var(--ui);text-decoration:none}
.cf-topo .busca-comando span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.cf-topo .busca-comando kbd{font:600 .66rem/1.2 var(--ui);color:var(--suave);background:var(--papel);border:1px solid var(--borda);
  border-radius:.22rem;padding:.08rem .36rem}
.cf-topo .busca-comando:hover{border-color:var(--suave);background:var(--painel);color:var(--tinta)}
.cf-topo .btn-livros{max-width:46vw;overflow:hidden;white-space:nowrap}
.cf-topo .cf-barra{display:none;align-items:center;gap:.1rem}
.cf-barra > a,.cf-estudar summary{flex:0 0 auto;display:inline-flex;align-items:center;gap:.3rem;color:var(--tinta-2);
  padding:.42rem .55rem;font:500 .8rem/1.2 var(--ui);letter-spacing:.01em;white-space:nowrap;border-radius:.32rem;text-decoration:none;cursor:pointer}
.cf-barra > a .ico{display:none}
.cf-estudar summary .ico-seta-baixo{width:.85em;height:.85em;color:var(--suave);margin-left:-.1rem}
.cf-barra > a:hover,.cf-barra > a.ativa,.cf-estudar summary:hover,.cf-estudar[open] summary{color:var(--rubrica);background:var(--rubrica-suave)}
.cf-menu{position:relative}
.cf-menu summary{list-style:none}
.cf-menu summary::-webkit-details-marker{display:none}
.cf-menu .menu-mais{position:absolute;top:calc(100% + .35rem);z-index:35;display:flex;flex-direction:column;min-width:15rem;
  padding:.35rem;background:var(--painel);border:1px solid var(--borda);border-radius:.45rem;box-shadow:0 14px 36px rgba(30,22,10,.18)}
.cf-estudar .menu-mais{left:0}
.cf-mais-cel .menu-mais{right:0}
.cf-menu .menu-mais a{display:flex;align-items:center;gap:.7rem;padding:.62rem .78rem;border-radius:.32rem;font:400 .86rem/1.3 var(--ui);
  color:var(--tinta);text-decoration:none}
.cf-menu .menu-mais .ico{font-size:1rem;color:var(--ouro)}
.cf-menu .menu-mais a:hover{background:var(--hover)}
.cf-menu .menu-mais a.ativa{color:var(--rubrica);font-weight:600}
.cf-mais-cel summary{cursor:pointer}
.cf-abas{display:none}
@media (max-width:759px){
  .cf-abas{position:fixed;left:0;right:0;bottom:0;z-index:25;display:flex;justify-content:space-around;
    padding:.3rem .25rem calc(.3rem + env(safe-area-inset-bottom));background:var(--painel);
    border-top:1px solid var(--borda);box-shadow:0 -6px 18px rgba(29,27,24,.05)}
  .cf-abas a{flex:1 1 0;min-width:0;display:flex;flex-direction:column;align-items:center;gap:.18rem;padding:.38rem .1rem .32rem;
    color:var(--suave);font:500 .64rem/1.2 var(--ui);text-decoration:none;border-radius:.32rem}
  .cf-abas span{max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .cf-abas .ico{font-size:1.32rem}
  .cf-abas a.ativa{color:var(--rubrica);font-weight:600}
  body.cf-pag{padding-bottom:calc(3.65rem + env(safe-area-inset-bottom))}
}
@media (max-width:560px){.cf-topo .marca{flex:1 1 1.45rem;min-width:1.45rem;margin:0;justify-content:center;flex-wrap:wrap;
    align-content:flex-start;height:1.45rem;overflow:hidden}
  .cf-topo .btn-livros .ico:first-child{display:none}
  .cf-topo .btn-apoiar{width:2.1rem;padding:0;justify-content:center}
  .cf-topo .btn-apoiar span{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
@media (min-width:760px){
  .cf-topo{flex-wrap:nowrap;height:3.4rem;padding:0 1.2rem;gap:.55rem}
  .cf-topo .marca{order:1;margin:0 .5rem 0 0;flex:0 0 auto}
  .cf-topo .busca-comando{order:2;display:inline-flex;flex:1 100 26rem;max-width:30rem;min-width:10rem;margin-right:auto;
    border-radius:99px;padding:0 .45rem 0 .95rem}
  .cf-topo .btn-livros{order:3;flex:0 0 auto;border:0;background:none;color:var(--tinta-2);font-size:.8rem;font-weight:500;
    padding:.42rem .55rem;letter-spacing:.01em}
  .cf-topo .btn-livros > .ico:first-child{display:none}
  .cf-topo .btn-livros:hover{background:var(--rubrica-suave);color:var(--rubrica)}
  .cf-topo .cf-barra{order:4;display:flex;flex:0 1 auto}
  .cf-topo .topo-acoes{order:5;flex:0 0 auto;padding-left:.75rem;margin-left:.2rem;border-left:1px solid var(--borda)}
  .cf-topo .btn-apoiar{border:0;background:none;padding:0 .45rem;font-size:.8rem;letter-spacing:.01em}
  .cf-topo .btn-apoiar:hover{background:var(--rubrica-suave)}
  .cf-mais-cel{display:none}
}
""" + _regras_cabem() + """
.cf-pag *{font-variant-numeric:lining-nums}   /* o "font" do lexico.css zera isto; sem ele o "1" da Cormorant parece "I" ("Pergunta I") */
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
.cf-perg{display:flex;align-items:flex-start;gap:.8rem}
.cf-perg .lex-resumo{flex:1 1 auto}
.cf-memo{flex:0 0 auto;display:inline-flex;align-items:center;gap:.35rem;margin-top:.2rem;border:1px solid var(--borda);background:var(--painel);
  border-radius:999px;padding:.35rem .75rem;font:600 .78rem/1 var(--ui);color:var(--tinta-2);cursor:pointer}
.cf-memo .ico{color:var(--ouro)}
.cf-memo[aria-pressed="true"]{border-color:var(--rubrica);color:var(--rubrica);background:var(--rubrica-suave)}
.cf-resposta{position:relative}
.cf-ver{display:none}
.cf-memorizar .cf-resposta:not(.vista)>*:not(.cf-ver){filter:blur(7px);user-select:none;pointer-events:none}
.cf-memorizar .cf-resposta:not(.vista) .cf-ver{display:block;position:absolute;z-index:2;top:1.2rem;left:50%;transform:translateX(-50%);
  border:1px solid var(--rubrica);background:var(--painel);color:var(--rubrica);border-radius:999px;padding:.6rem 1.2rem;
  font:600 .9rem/1 var(--ui);cursor:pointer;box-shadow:0 8px 24px rgba(30,22,10,.18)}
.cf-pag .lex-viz span+span{text-align:right}
</style>"""
CURTO = {"breve-catecismo": "Breve Catecismo de Westminster", "catecismo-maior": "Catecismo Maior de Westminster",
         "heidelberg": "Catecismo de Heidelberg", "catecismo-batista": "Catecismo Batista"}


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
        sem_marcas = not RE_MARCA.search(txt)             # provas reunidas no fim (Heidelberg, 1689): sem número
        if provas:
            itens = []
            for n in sorted(provas, key=int):
                refs = provas[n]
                if not refs:
                    continue
                primeira = refs[0]
                trecho = texto(primeira[0], primeira[1], primeira[2] or 1)
                rotulo = "Textos de prova:" if sem_marcas else n
                itens.append(f'<li id="{ancora}-{n}"><b>{rotulo}</b> ' + "; ".join(link(r) for r in refs) +
                             (f'<span>{e(cortar(trecho, 160))}</span>' if trecho else "") + "</li>")
            lista = f'<ol class="cf-provas">{"".join(itens)}</ol>'
        return f'<p class="cf-texto">{corpo}</p>{lista}'

    urls, citacoes = [], {}
    busca = []                                           # [documento, rótulo, endereço, texto] para a busca do app

    def indexar(d, rot, url, texto):
        busca.append([d, rot, url, re.sub(r"\s+", " ", RE_MARCA.sub("", texto)).strip()])

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
        seo = seo.replace("/og.png", "/og-confissoes.png")   # a imagem ao compartilhar (WhatsApp, Twitter): própria das confissões
        arq = raiz / caminho.strip("/") / "index.html"
        arq.parent.mkdir(parents=True, exist_ok=True)
        js = MEMO_JS if "cf-memo" in corpo else ""
        arq.write_text(pagina_versiculo(titulo, desc, css, corpo + js, seo, ESTILO, TOPO_CONF, "cf-pag"), encoding="utf-8")
        urls.append(site + caminho)

    docs = [json.loads((raiz / "data" / "confissoes" / f"{d}.json").read_text(encoding="utf-8"))
            for d in ("credos", "westminster", "catecismo-maior", "breve-catecismo", "confissao-belga", "heidelberg",
                      "canones-de-dort", "confissao-batista-1644", "confissao-batista-1689", "catecismo-batista")]
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
                indexar(d, c["titulo"], caminho, " ".join(c["texto"]))
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
                indexar(d, f"Pergunta {q['n']}", caminho, f"{p} {r}")
                ant = f'<span>‹ <a href="{base}{itens[i - 1]["n"]}/">Pergunta {itens[i - 1]["n"]}</a></span>' if i else "<span></span>"
                pro = f'<span><a href="{base}{itens[i + 1]["n"]}/">Pergunta {itens[i + 1]["n"]}</a> ›</span>' if i + 1 < len(itens) else "<span></span>"
                domingo = f'<p class="lex-translit">{e(nome)}, Domingo {q["domingo"]}</p>' if "domingo" in q else ""
                original = {"heidelberg": "Texto inglês (1863)",
                            "catecismo-batista": "Texto inglês (edição de 1813)"}.get(d, "Original inglês (1647)")
                # modo memorizar: a resposta (e o inglês, que a entregaria) fica embaçada até tocar em "Mostrar resposta"
                corpo = (f'{topo}<h1>Pergunta {q["n"]}</h1>{domingo}<div class="cf-perg"><p class="lex-resumo">{e(p)}</p>'
                         f'{MEMO_BOTAO}</div><div class="cf-resposta">{MEMO_VER}' +
                         paragrafo(r, q["provas"], f"p{q['n']}") +
                         f'<details class="acv-original"><summary>{original}</summary><p>{e(q["p_en"])}</p>'
                         f'<p>{e(RE_MARCA.sub("", q["r_en"])).replace(chr(10), "<br>")}</p></details></div>'
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
                    elif d in ("confissao-belga", "confissao-batista-1644"):
                        rot_it = f"artigo {n}"
                    else:
                        rot_it = f"{n}.{it['n']}"
                    rot_cit = {"westminster": f"Confissão de Westminster {rot_it}", "confissao-belga": f"{nome}, {rot_it}",
                               "confissao-batista-1644": f"Confissão Batista de 1644, {rot_it}",
                               "canones-de-dort": f"{nome}, capítulo {n}, {rot_it[:1].lower() + rot_it[1:]}"}.get(d, f"{nome} {rot_it}")
                    rot_busca = (f"Capítulo {n}, {rot_it[:1].lower()}{rot_it[1:]}" if d == "canones-de-dort"
                                 else f"{rot_it[:1].upper()}{rot_it[1:]}")
                    indexar(d, f"{rot_busca} · {titulo}", f"{caminho}#s{it['n']}", it.get("pt") or it["en"])
                    citar(it["provas"], rot_cit, caminho,
                          it.get("pt") or it["en"])
                    texto_it = paragrafo(it.get("pt") or it["en"], it["provas"], f"s{it['n']}")
                    if d in ("confissao-belga", "confissao-batista-1644"):   # os parágrafos de um artigo, sem título cada um
                        blocos.append(f'<div id="s{it["n"]}">{texto_it}</div>')
                    else:
                        blocos.append(f'<h2 class="cf-n" id="s{it["n"]}">{e(rot_it)}</h2>{texto_it}')
                rot_doc = {"westminster": "Capítulo", "confissao-batista-1689": "Capítulo", "confissao-belga": "Artigo",
                           "confissao-batista-1644": "Artigo"}.get(d, "Capítulo de doutrina")
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
                       [f"{len(partes)} artigos" if d in ("confissao-belga", "confissao-batista-1644") else f"{len(partes)} capítulos"])
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
            "Confissão Belga, o Catecismo de Heidelberg e os Cânones de Dort), com os textos de prova, e, da tradição "
            "batista reformada, as Confissões de Londres de 1644 e de 1689 e o Catecismo Batista.")
    gravar("/confissoes/", "Confissões e catecismos reformados em português | Sola", desc,
           '<header class="cf-heroi"><p class="lex-sobre">Símbolos de fé</p><h1>Confissões e <em>catecismos</em></h1>'
           f'<p class="cf-sub">{e(desc)}</p></header>' +
           "".join(f'<h2 class="cf-trad"><b>{e(t)}</b><span>{e(sub)}</span></h2><div class="cf-cartoes">' +
                   "".join(f'<a class="cf-cartao" href="/confissoes/{x["id"]}/"><div class="cf-topo"><h3>{e(x["titulo"])}</h3>'
                           f'<span class="cf-ano">{e(str(x["ano"]))}</span></div><p>{e(RESUMO[x["id"]])}</p>'
                           f'<span class="cf-ler">{e(tamanhos[x["id"]])} · Ler ›</span></a>'
                           for x in docs if x["id"] in ds) + "</div>"
                   for t, sub, ds in TRADICOES) +
           '<h2 class="cf-trad"><b>Pais da Igreja</b><span>Os escritos dos primeiros séculos</span></h2><div class="cf-cartoes">'
           '<a class="cf-cartao" href="/pais/agostinho/confissoes/"><div class="cf-topo"><h3>Confissões de Agostinho</h3>'
           '<span class="cf-ano">c. 400</span></div><p>A vida de Agostinho contada a Deus em forma de oração, da infância à '
           'conversão, e suas meditações sobre a memória, o tempo e a criação.</p><span class="cf-ler">Ler ›</span></a>'
           '</div>'
           f'<p class="fonte">{AVISO}</p>', [("Sola", "/"), ("Confissões", "/confissoes/")])
    # o texto de todos os documentos, para a busca do app (aba Confissões e o grupo da busca universal)
    nomes = {doc["id"]: doc["titulo"] for doc in docs}
    (raiz / "data" / "confissoes" / "busca.json").write_text(
        json.dumps({"docs": nomes, "itens": busca}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
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
