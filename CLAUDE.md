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

- `index.html`, `style.css`, `app.js` — a aplicação inteira (SPA), três telas (`est.vista`): início (`/`),
  livro (`/biblia/joao/`) e capítulo (`/biblia/joao/3/`, com `#v16` para ir direto ao versículo), via
  `history.pushState`. Links antigos `#/JHN/3` ainda funcionam e são convertidos. Toda referência é um
  `<a href>` de verdade (função `linkRef`); um único ouvinte de clique em `iniciar()` navega sem recarregar.
  Dados sempre por caminho absoluto (`/data/...`).
- `biblia/` — páginas estáticas GERADAS: 66 de livro e 1.189 de capítulo (título, descrição, texto e
  trilha JSON-LD no HTML para o Google). A página inicial é gerada dentro do próprio `index.html`, entre
  `<!--CONTEUDO-->` e `<!--/CONTEUDO-->`. Mais `sitemap.xml`, `robots.txt` e `404.html` (abre o início).
  **Sempre que mexer em `index.html`, `app.js`, `style.css` ou `sw.js`, rode `python3 ferramentas/gerar_paginas.py`**
  — as páginas são cópias do index, e ele carimba `?v=<hash>` nos endereços do JS/CSS e a `VERSAO` do `sw.js`.
  Nunca edite `biblia/` à mão. Rodar duas vezes não muda nada; o workflow `verificar.yml` reprova o envio se
  as páginas estiverem desatualizadas, se `node --check` falhar ou se `ferramentas/validar_dados.py` achar erro.
- `sw.js` + `manifest.webmanifest` — uso sem internet (PWA). Páginas: rede primeiro, e sem rede a página
  inicial guardada (o app lê o endereço). `/data/`: responde do cache `sola-dados-v1` e atualiza por trás.
  O botão "Baixar a Bíblia" (painel Sobre) guarda a tradução inteira nesse mesmo cache.
- `fontes/` (Cardo, Cormorant Garamond, Inter) e `vendor/leaflet/` — servidos pelo próprio site; nada de
  Google Fonts nem unpkg. A única coisa de terceiros são as imagens do mapa (OpenStreetMap), só no Atlas.
- `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `icone-*.png`, `og.png` (preview no WhatsApp, 1200×630).
- `CNAME` — domínio personalizado. **Nunca apagar.**
- `data/books.json` — cânon (66 livros, ids USFM, nomes pt/en/es) e lista de traduções.
- `data/bibles/{blivre,kjv,rva,orig,byz}/{USFM}.json` — texto por livro: lista de capítulos → lista de versículos.
  `orig` = hebraico (WLC) no AT e grego (TR) no NT; `byz` = Bizantino (NT).
- `data/interlinear/{USFM}/{cap}.json` — palavra a palavra: `[original, transliteração, strong, glosa]`.
  Sempre na numeração de versículos da Bíblia Livre. O hebraico numera diferente em ~2.300 versículos
  (títulos dos Salmos, Gn 32, Nm 17, Jl 3, Ml 4) e o grego em ~50; a STEPBible traz as duas numerações e
  `ferramentas/gerar_interlinear_at.py` / `corrigir_interlinear_nt.py` escolhem a certa (a fonte fica em
  `ferramentas/fontes/`, fora do git). No AT o Strong é o da raiz; palavra feita só de prefixo/sufixo fica sem número.
- `data/strongs/{G,H}.json` — léxico. Campo `def` (inglês) e `defpt` (português, tradução automática revisada).
- `data/commentaries/calvin/{USFM}/{cap}.json` — Calvino original (inglês), chave = versículo.
  `data/commentaries/calvin/pt/...` — tradução; o app sobrepõe o `pt/` ao original quando o idioma é Português.
  Calvino não comentou 20 livros (Juízes, Samuel, Reis, Atos, Apocalipse...). Nesses o app carrega
  `data/commentaries/henry/` (Matthew Henry, domínio público, baixado por `ferramentas/baixar_henry.py`;
  18 livros — Cantares não existe na fonte, e 2Sm 23–24 também faltam). Cada pasta tem `manifest.json`
  com a lista de livros. O app usa o comentário do versículo anterior (blocos) ou o primeiro do capítulo.
- `data/dictionary/` (Easton) e `data/topics/` (Nave): originais + `pt/` (tradução) + `titulos_pt.json`.
- `data/places.json` — atlas; campo `p` = nome em português. `data/journeys.json` — viagens de Paulo.
- `data/crossrefs/` (openbible.info), `data/context.json` (fichas dos 66 livros, escritas à mão),
  `data/timeline.json`, `data/plans.json`.
- Dados do usuário (marcações, notas, planos, capítulos lidos `logos_lidos`, "onde parei" `logos_ultimo`) ficam
  no localStorage do navegador, com backup/restauração manual em arquivo. O painel "Meu estudo" (progresso
  por livro, dias seguidos, marcações) funciona só com isso, sem conta.
- Contas (opcionais, Supabase): `CONTA` no topo do `app.js`; com `url` vazio tudo de conta fica escondido.
  O cliente (`vendor/supabase/supabase.js`, 220 KB) só é carregado se houver sessão guardada, volta do login
  ou clique em "Entrar". Uma tabela só (`itens`, em `ferramentas/supabase.sql`, com RLS). Sincronização em
  `sincronizar()`: o aparelho é a fonte, `tocar(tipo, chave)` anota cada alteração em `est.sinc.pend`, e no
  mesmo item vale o `ts` mais recente (apagar também é alteração). `DADOS` descreve cada tipo (nota, marca,
  plano, lido, estado). Passo a passo de configuração e detalhes em `ferramentas/CONTAS.md`.

## Ferramentas de tradução (`ferramentas/tradutor/`)

Dois motores: Argos (rápido, mediano) e NLLB-200 1.3B (`nllb.py`, ~10x mais lento, bem melhor em prosa).
O NLLB roda no GitHub Actions: `.github/workflows/traduzir.yml` (Actions → "Traduzir (NLLB)" → etapa,
nº de partes). Divide em N máquinas, junta, grava em `data/.../pt/` e envia ao branch `traducao-<etapa>`
para virar PR. Se faltar algo, rodar de novo com `retomar` = run id anterior. `lote.py --motor nllb --parte K/N`.
A etapa `glosas` do mesmo workflow usa o Argos (palavras soltas, 1 máquina, poucos minutos): é o
`traduzir_tudo.sh glosas` sem precisar de computador (ele usa Windows 11 agora, sem ambiente Linux).
O `nllb.py` protege marcadores de tópico ("I.", "1.", "(2.)") e devolve "milhas" (o modelo troca por "quilômetros").

Glosas do interlinear: `ferramentas/glosas_pt.json` é o dicionário inglês→português, e `GLOSAS_FIXAS` em
`etapas.py` são as revisadas à mão (têm prioridade). `python3 etapas.py aplicar glosas` reaplica as duas.

Tradução offline e gratuita (modelo Argos en→pt-BR via CTranslate2). `./traduzir_tudo.sh [etapas]` e
`revisar.py` (refaz trechos com omissão). As pastas `venv/`, `modelo/` e `trabalho/` são locais (gitignore).
Qualidade: boa no Strong e nos títulos; legível mas com tropeços em Calvino e Easton — por isso o site
sempre mostra "Tradução automática". O modelo omite texto em listas longas e não conhece inglês arcaico;
o tradutor já moderniza ("thou", "ass") e refaz em pedaços frases que saem curtas demais.

## Como trabalhar neste repositório

- Teste antes de publicar: `python3 -m http.server` na raiz e Playwright com
  `executablePath: '/opt/pw-browsers/chromium'`. Verifique erros de console e tire prints nas larguras
  390, 1280 e 1600.
- `node --check app.js` depois de qualquer edição no JS; `python3 ferramentas/validar_dados.py` depois de mexer em `data/`.
- Nos testes com Playwright, use `serviceWorkers: 'block'` no contexto, senão o service worker responde no
  lugar das rotas simuladas; e `reducedMotion: 'reduce'`, senão a rolagem suave faz cliques falharem ao acaso.
- Para testar contas sem Supabase: interceptar `/vendor/supabase/supabase.js` com um cliente falso (mesma
  interface: `auth.getSession/onAuthStateChange/signInWithOAuth/signOut`, `from().select().gte().order().range()`,
  `upsert`, `rpc`) e trocar `CONTA` na resposta do `app.js`. Variáveis `const` do app (`est`) são visíveis em
  `page.evaluate`, mas não em `window.est`.
- No celular (≤560px) a barra do versículo fica no fluxo, entre o texto e a gaveta: flutuando ela cobria o
  botão Salvar. `font-variant-numeric:lining-nums` no `body` é obrigatório: sem ele o "1" da Cormorant parece "I".
- Visual: cores e fontes são variáveis no topo do `style.css` (marfim, azul-noite, ouro envelhecido; títulos em
  Cormorant Garamond, Escritura em Cardo, interface em Inter). `.verso > p` é só o texto do versículo — o que
  está dentro das gavetas tem estilo próprio. Textos da interface ficam no objeto `UI` (pt/en/es).
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
- Qualidade da tradução de Calvino/Easton: o caminho gratuito é o workflow "Traduzir (NLLB)" (já usado no
  Henry). A Batch API da Anthropic (~US$ 45, uma vez) daria mais qualidade, se ele decidir pagar; o script
  antigo foi removido (gravava por cima dos originais) — seria preciso um novo que leia `trabalho/<etapa>.json`.
- Contas: falta ele criar o projeto no Supabase e o login do Google (`ferramentas/CONTAS.md`) e mandar a URL e
  a chave publishable; aí preencher `CONTA` e testar de verdade (login e RLS nunca rodaram contra um projeto real).
- Glosas do interlinear: ~900 palavras ainda em inglês ou truncadas (as que o Argos traduziu mal e o filtro
  `glosa_confiavel` recusou, mais antigas como "and  you will do"). Corrigir à mão em `GLOSAS_FIXAS`.
- Só 372 dos 1.335 lugares do atlas têm nome em português (`p` em `data/places.json`).
- Inglês e espanhol: a interface está traduzida, mas atlas (rótulos do cartão do lugar), linha do tempo e
  fichas de contexto têm conteúdo só em português.
- Publicação pelo GitHub Actions (em vez de commitar `biblia/`, 35 MB): exige ele trocar a origem do Pages
  em Settings → Pages. Enquanto isso, `biblia/` continua no repositório e o `verificar.yml` confere.
