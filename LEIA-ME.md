# Sola — Estudo Bíblico

Site de estudo bíblico profundo, gratuito e em português: **https://solabiblia.com.br**

100% estático (HTML, CSS e JavaScript puro, sem build, sem servidor, sem banco de dados), publicado pelo
GitHub Pages a partir da raiz do branch `main`. Custo de operação: zero.

## O que tem

- **Bíblia completa** em três traduções de domínio público: Bíblia Livre (português), King James 1769
  (inglês) e Reina-Valera Antigua (espanhol), com comparação lado a lado.
- **Interlinear palavra por palavra** do grego (NT) e do hebraico (AT): transliteração, glosa em
  português e número de Strong; um toque abre o verbete do léxico (14.197 entradas).
- **Comentários**: João Calvino (47 livros) e Matthew Henry (18 livros), em português por tradução
  automática, sempre com o aviso na tela.
- **Referências cruzadas**, **temas** (Nave), **dicionário** (Easton), **atlas** com as viagens de
  Paulo, **linha do tempo**, **planos de leitura** e ficha de **contexto** de cada livro.
- Marcações em quatro cores, anotações, copiar e compartilhar versículo como imagem. Tudo fica só no
  navegador do visitante (com backup em arquivo); não há contas, cookies nem contadores.
- Página inicial, uma página por livro e uma por capítulo já escritas em HTML para o Google
  (`/biblia/joao/`, `/biblia/joao/3/`), e link direto para o versículo (`/biblia/joao/3/#v16`).
- Funciona sem internet depois da primeira visita (service worker) e pode ser instalado no celular.
- "Meu estudo": capítulos lidos, progresso por livro, dias seguidos e versículos marcados.
- Contas opcionais (Supabase) para continuar em qualquer aparelho — desligadas até o projeto ser criado;
  veja `ferramentas/CONTAS.md`.

## Como mexer

```
python3 -m http.server            # abre o site em http://localhost:8000
node --check app.js               # depois de editar o JavaScript
python3 ferramentas/validar_dados.py
python3 ferramentas/gerar_paginas.py   # SEMPRE depois de mexer em index.html, app.js, style.css ou sw.js
```

O `gerar_paginas.py` reescreve a pasta `biblia/`, a página inicial dentro do `index.html`, o
`sitemap.xml`, o `404.html` e carimba a versão do `app.js`, do `style.css` e do `sw.js`. Nunca edite
`biblia/` à mão. A cada envio, o GitHub Actions (`.github/workflows/verificar.yml`) confere o
JavaScript, os dados e se as páginas geradas estão em dia.

Correção pequena vai direto no `main`; mudança grande, em branch com pull request. O site atualiza em
cerca de dois minutos (no navegador, `Ctrl+Shift+R` para ver a versão nova).

## Pastas

| Pasta | Conteúdo |
|---|---|
| `index.html`, `app.js`, `style.css`, `sw.js` | O aplicativo inteiro |
| `biblia/` | Páginas geradas (não editar) |
| `data/` | Bíblias, interlinear, léxico, comentários, referências, temas, dicionário, atlas |
| `fontes/`, `vendor/leaflet/` | Tipografia e mapa, servidos pelo próprio site |
| `ferramentas/` | Geradores e validador (Python, sem dependências) |
| `ferramentas/tradutor/` | Tradução automática offline (Argos e NLLB) |

Os detalhes de cada arquivo de dados e as decisões do projeto estão em `CLAUDE.md`.

## Ferramentas

- `gerar_paginas.py` — páginas estáticas, sitemap e versões.
- `validar_dados.py` — confere a integridade de `data/`.
- `gerar_interlinear_at.py` e `corrigir_interlinear_nt.py` — interlinear a partir da STEPBible, na
  numeração de versículos das nossas traduções.
- `gerar_crossrefs.py`, `baixar_henry.py` — referências cruzadas e comentário de Matthew Henry.
- `tradutor/traduzir_tudo.sh [glosas temas dicionario calvino]` — tradução offline com o Argos.
  Para o NLLB (melhor em prosa), aba Actions → "Traduzir (NLLB)".

## Fontes e licenças

- Textos bíblicos: scrollmapper/bible_databases (domínio público).
- Interlinear e morfologia: STEPBible / Tyndale House, Cambridge (CC BY).
- Léxico de Strong (1890), comentários de Calvino e Matthew Henry, dicionário de Easton, Nave's
  Topical Bible: domínio público.
- Referências cruzadas e lugares: openbible.info (CC-BY).
- Traduções automáticas: Argos Translate e NLLB-200 (Meta, CC BY-NC — uso não comercial).
- Tipografia: Cardo, Cormorant Garamond e Inter (SIL Open Font License). Mapa: Leaflet (BSD) e
  OpenStreetMap.
