# Sola — memória do projeto

Site de estudo bíblico em português, publicado em **https://solabiblia.com.br**.
Dono: Khennedy (presbiteriano reformado, formado em ADS). Fale com ele em português brasileiro,
informal e direto. Ele usa Ubuntu e Firefox/Chrome.

## Visão e decisões já tomadas

- Posicionamento: "o BibleHub em português" — estudo profundo (originais, Strong, comentários) e gratuito.
- Nome **Sola** (de *Sola Scriptura*). O nome antigo era "Logos" e foi abandonado por conflito de marca
  com o Logos Bible Software. Não reintroduzir "Logos" na interface.
- Sem fins comerciais por enquanto: sem anúncios, sem cobrança. Isso mantém válidas as licenças gratuitas.
- Custo: ele prefere o caminho gratuito. Nada de IA chamada por visitante (custo por uso). Processamento
  pesado roda uma vez, offline, e o resultado vira arquivo estático.
- Próxima fase desejada: contas de usuário (Supabase), painel pessoal, e "aulas públicas → síntese"
  curadas por ele e ligadas ao acervo. Respeitar direitos: incorporar o vídeo, síntese própria com crédito.

## Arquitetura

Site 100% estático (HTML + CSS + JS puro, sem build), servido pelo GitHub Pages a partir da raiz do branch `main`.

- `index.html`, `style.css`, `app.js` — a aplicação inteira (SPA). Endereços: `/biblia/{livro}/{cap}/`
  (ex.: `/biblia/joao/3/`, `/biblia/1-corintios/13/`), via `history.pushState`. Links antigos `#/JHN/3`
  ainda funcionam e são convertidos. Dados sempre por caminho absoluto (`/data/...`).
- `biblia/` — 1.189 páginas estáticas GERADAS (uma por capítulo, com título, descrição e o texto no HTML
  para o Google). Mais `sitemap.xml`, `robots.txt` e `404.html`. **Sempre que mexer em `index.html`, `app.js` ou
  `style.css`, rode `python3 ferramentas/gerar_paginas.py`** — as páginas são cópias do index, e ele
  carimba `?v=<hash>` nos endereços do JS/CSS para o navegador não usar a versão velha em cache. Nunca edite `biblia/` à mão.
- `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `og.png` (preview no WhatsApp, 1200×630).
- `CNAME` — domínio personalizado. **Nunca apagar.**
- `data/books.json` — cânon (66 livros, ids USFM, nomes pt/en/es) e lista de traduções.
- `data/bibles/{blivre,kjv,rva,orig,byz}/{USFM}.json` — texto por livro: lista de capítulos → lista de versículos.
  `orig` = hebraico (WLC) no AT e grego (TR) no NT; `byz` = Bizantino (NT).
- `data/interlinear/{USFM}/{cap}.json` — palavra a palavra: `[original, transliteração, strong, glosa]`.
- `data/strongs/{G,H}.json` — léxico. Campo `def` (inglês) e `defpt` (português, tradução automática revisada).
- `data/commentaries/calvin/{USFM}/{cap}.json` — Calvino original (inglês), chave = versículo.
  `data/commentaries/calvin/pt/...` — tradução; o app sobrepõe o `pt/` ao original quando o idioma é Português.
  Calvino não comentou 20 livros (Juízes, Samuel, Reis, Atos, Apocalipse...). O app usa o comentário do
  versículo anterior (blocos) ou o primeiro do capítulo.
- `data/dictionary/` (Easton) e `data/topics/` (Nave): originais + `pt/` (tradução) + `titulos_pt.json`.
- `data/places.json` — atlas; campo `p` = nome em português. `data/journeys.json` — viagens de Paulo.
- `data/crossrefs/` (openbible.info), `data/context.json` (fichas dos 66 livros, escritas à mão),
  `data/timeline.json`, `data/plans.json`.
- Dados do usuário (marcações, notas, progresso dos planos) ficam só no localStorage do navegador,
  com backup/restauração manual em arquivo.

## Ferramentas de tradução (`ferramentas/tradutor/`)

Tradução offline e gratuita (modelo Argos en→pt-BR via CTranslate2). `./traduzir_tudo.sh [etapas]` e
`revisar.py` (refaz trechos com omissão). As pastas `venv/`, `modelo/` e `trabalho/` são locais (gitignore).
Qualidade: boa no Strong e nos títulos; legível mas com tropeços em Calvino e Easton — por isso o site
sempre mostra "Tradução automática". O modelo omite texto em listas longas e não conhece inglês arcaico;
o tradutor já moderniza ("thou", "ass") e refaz em pedaços frases que saem curtas demais.

## Como trabalhar neste repositório

- Teste antes de publicar: `python3 -m http.server` na raiz e Playwright com
  `executablePath: '/opt/pw-browsers/chromium'`. Verifique erros de console e tire prints nas larguras
  390, 1280 e 1600.
- `node --check app.js` depois de qualquer edição no JS.
- Correção pequena e segura: commit direto no `main`. Mudança grande: branch + pull request para ele aprovar.
- Antes de push num clone raso: `git fetch origin main` e rebase.
- Depois de publicar, lembre: o navegador dele guarda cache — `Ctrl+Shift+R` para ver a versão nova.
- Não rode tarefas de dezenas de minutos no ambiente do Claude (já travou uma vez). Trabalho pesado vai
  para o GitHub Actions ou para o notebook dele.
- Arquivos grandes de dados: gere por script e valide uma amostra; nunca edite à mão em massa.
- O Chrome descarta o nome de arquivo de download com acento: gere nomes sem acento.
- Teste sempre nos dois temas (claro e escuro). Botões não herdam cor por padrão: já existe a regra
  global `button{color:inherit}` — não a remova. Texto em português dentro do hebraico precisa de
  `unicode-bidi:isolate`, senão a pontuação se embaralha.
- Antes de dar uma atualização por concluída, confira se os arquivos chegaram ao repositório. A pasta
  `data/crossrefs` ficou de fora por semanas porque um zip nunca foi enviado (regerada com
  `ferramentas/gerar_crossrefs.py`).
- Créditos obrigatórios (já no painel "Fontes e licenças"): STEPBible/Tyndale House (CC BY),
  openbible.info (CC-BY), demais fontes em domínio público.

## Pendências conhecidas

- E-mail de contato no rodapé ainda é `contato@exemplo.com`.
- Ele precisa cadastrar o site no Google Search Console e enviar o `sitemap.xml` (só ele pode, é conta dele).
- Qualidade da tradução de Calvino/Easton pode ser elevada com a Batch API da Anthropic (~US$ 45, uma vez),
  se ele decidir pagar.
