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
- `privacidade/` — página de texto avulsa (sem o app), também GERADA: o conteúdo fica em
  `ferramentas/paginas/privacidade.html` e cada arquivo dessa pasta vira `/nome/`. Atualize a data no topo
  do texto quando mudar o que o site guarda. O link dela está no cadastro do login do Google (Branding).
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
  As glosas são revisadas por `ferramentas/corrigir_glosas.py` (`preparar` / `aplicar`): `stepbible.py` alinha cada
  palavra do site com a da fonte (447.704 palavras), que traz a glosa inglesa e a gramática. Corrige nomes próprios
  (`nomes_pt.py` grava `nomes_pt.json`, Strong → nome na grafia da Bíblia Livre; "Yahweh" vira SENHOR), verbos com
  concordância quebrada (retraduzidos pelo NLLB na etapa "verbos" do workflow, numa moldura tirada da gramática:
  "sent" 3P → "they sent" → "enviaram"), concordância pela gramática (`GRAMATICA`) e termos que ficaram em inglês
  (`TABELA`). Segunda rodada, no mesmo script: `glosas_revisao.py` (`REVISAO`: as ~2.000 glosas mais frequentes lidas
  com o inglês ao lado; a chave pode limitar à gramática, `("praise", "HVpv")`, e o valor pode depender da pessoa,
  `{"2S": "sobe", "2P": "subi"}`); sufixo hebraico remontado parte por parte (preposição + `substantivos_pt.json` +
  pronome pela gramática: "mão  dele", "olhos  teus", "terra  vossa", "a  ele", "<obj.>  nós"; 3ª pessoa é
  dele/dela/deles/delas); artigo grego concordando com o gênero e o número da palavra portuguesa ("a palavra", "as
  obras", "da vida"; antes "of the" virava "fazer"), pelo léxico de gênero tirado da Bíblia Livre (`lexico()`);
  formas (`conjugar.py`): "você" → tu/vós com o verbo conjugado, "eu têm falado" → "eu falei", "eu vou cortar" →
  "eu cortarei", imperativo ("buscar" → "busca"/"buscai"), adjetivo plural ("os pobre" → "os pobres"), maiúscula
  indevida. O `aplicar` repete as etapas até nada mudar, então rodar de novo não muda nada. Glosa nova errada:
  acrescente em `REVISAO` (ou `GRAMATICA`/`TABELA`) e rode `aplicar` (~1 min).
- `data/strongs/{G,H}.json` — léxico. Campo `def` (inglês) e `defpt` (português, tradução automática revisada).
- `data/commentaries/calvin/{USFM}/{cap}.json` — Calvino original (inglês), chave = versículo.
  `data/commentaries/calvin/pt/...` — tradução; o app sobrepõe o `pt/` ao original quando o idioma é Português.
  Calvino não comentou 20 livros (Juízes, Samuel, Reis, Atos, Apocalipse...). Nesses o app carrega
  `data/commentaries/henry/` (Matthew Henry, domínio público, baixado por `ferramentas/baixar_henry.py`;
  18 livros — Cantares não existe na fonte, e 2Sm 23–24 também faltam). Cada pasta tem `manifest.json`
  com a lista de livros. O app usa o comentário do versículo anterior (blocos) ou o primeiro do capítulo.
- `data/palavras/` — palavras sublinhadas no texto (só na Bíblia Livre), em duas camadas, GERADAS por
  `ferramentas/gerar_palavras.py`:
  - palavras-chave (traço cheio dourado): as notas são escritas no próprio script. `lema(strong, tradução, formas,
    nota)` sublinha a palavra na primeira vez em que aparece em cada capítulo; `contexto("PSA.51.10", "H1254", nota)`
    é a nota própria de um versículo. O script acha a palavra no interlinear e a forma em português no versículo, e
    recusa nota de contexto cujo Strong não esteja no versículo (proteção contra número errado).
  - vocabulário (traço pontilhado): palavras difíceis, antigas ou técnicas (côvado, éfode, holocausto, filisteus,
    porquanto...), palavras que mudaram de sentido (aborrecer, constranger, príncipe, alma, dote), deuses vizinhos,
    meses hebraicos, títulos (Faraó, Herodes, SENHOR dos exércitos) e expressões ("descansou com seus pais"),
    escritas em `ferramentas/vocabulario.py` com `t(palavra, formas, significado, nota, s=(strongs),
    exige)`. `exige=True` só sublinha onde o Strong está no versículo — use quando a palavra tem outro sentido
    ("funda" arma × "cova funda"; "dízimas" medida × dízimo; "Selá" nome × pausa dos Salmos). Entra depois das
    palavras-chave, sem sobrepor e sem repetir no capítulo uma palavra que já é palavra-chave nele. Máximo de 5
    marcas por versículo (3 de vocabulário). Duas entradas sem `exige` não podem casar a mesma forma: a segunda
    sublinharia a mesma palavra mais adiante no capítulo com outro sentido. `--relatorio` mostra onde cada termo
    caiu e quantas vezes o Strong confirmou: porcentagem baixa costuma ser sentido errado. Leva cerca de 75 s.
  `indice.json` traz `lemas`, `termos`, `orig` (lema do Strong citado pelo vocabulário) e `livros`; `{LIVRO}.json`
  traz capítulo → versículo → `[início, fim, "H1254", nota?]` ou `[início, fim, "v:covado", strong?]`.
  No app: `carregarPalavras`, `textoVerso`, `abrirPalavra` (cartão `#cartaoPalavra`); preferências `logos_chave` e
  `logos_voc` no Perfil. Não aparece na leitura contínua nem nas outras traduções.
- `data/dictionary/` (Easton) e `data/topics/` (Nave): originais + `pt/` (tradução) + `titulos_pt.json`. No Easton em
  português as referências estão no formato dos dados ("GEN 3:15; GEN 4:1"), convertidas por `refs_usfm` (etapas.py)
  antes da tradução; `linkarRefs` (app.js) transforma em link essas referências, as só de capítulo ("ISA 53") e as
  continuações da mesma lista ("1TI 1:4; 4:7"), no dicionário e nos Temas.
- `data/topics/doutrinas.json` — doutrinas da fé reformada (pedobatismo, Trindade, TULIP, cinco solas, governo
  presbiteriano...) que aparecem primeiro na busca de Temas, com selo "Doutrina reformada": resumo, fonte (CFW,
  Catecismos) e os versículos de prova agrupados, com o texto da Bíblia Livre já embutido. Escritas em
  `ferramentas/doutrinas.py` (`D(id, título, sinônimos, fonte, resumo, [(seção, "GEN 17:7; ACT 2:38-39")])`);
  `python3 ferramentas/gerar_doutrinas.py` confere as referências e grava o JSON (`--texto` imprime tudo para revisar).
  `validar_dados.py` reprova se o texto guardado ficar diferente da Bíblia Livre. Com o campo vazio, a aba Temas
  lista todas; buscar "reformada", "westminster", "calvinismo" etc. também lista todas.
- `data/places.json` — atlas; campo `p` = nome em português, gerado por `ferramentas/gerar_atlas_pt.py` (o nome do
  Strong do lugar em `nomes_pt.json`, ou a expressão do texto: "monte das Oliveiras"; portas e construções em
  `MANUAL`). `data/journeys.json` — viagens de Paulo.
- `data/crossrefs/` (openbible.info), `data/context.json` (fichas dos 66 livros, escritas à mão),
  `data/timeline.json`, `data/plans.json`.
- Dados do usuário (marcações, notas, planos, capítulos lidos `logos_lidos`, "onde parei" `logos_ultimo`) ficam
  no localStorage do navegador, com backup/restauração manual em arquivo. O painel "Meu estudo" (progresso
  por livro, dias seguidos, marcações) funciona só com isso, sem conta.
- Contas (opcionais, Supabase): `CONTA` no topo do `app.js`; com `url` vazio, ou com `google` e `email`
  desligados, tudo de conta fica escondido.
  O cliente (`vendor/supabase/supabase.js`, 220 KB) só é carregado se houver sessão guardada, volta do login
  ou clique em "Entrar". Uma tabela só (`itens`, em `ferramentas/supabase.sql`, com RLS). Sincronização em
  `sincronizar()`: o aparelho é a fonte, `tocar(tipo, chave)` anota cada alteração em `est.sinc.pend`, e no
  mesmo item vale o `ts` mais recente (apagar também é alteração). `DADOS` descreve cada tipo (nota, marca,
  plano, lido, estado). Passo a passo de configuração e detalhes em `ferramentas/CONTAS.md`.
- Painel "Meu estudo" tem duas abas (`est.abaEstudo`): Estudo (números, progresso, marcações) e Perfil (conta,
  preferências, backup, privacidade, excluir conta). O botão de perfil no topo (`#btnPerfil`, inicial do nome de
  quem entrou) abre direto no Perfil; substituiu o antigo botão de ajustes. Os seletores do Perfil espelham os da
  barra `.controles`, que só aparece na leitura em tela larga (acima de 700 px); no celular eles também ficam no "Mais".
- Barra de recursos (`.navbar`) e menu "Mais" (`#navMais` / `#menuMais`): `ajustarNav()` esconde (classe `nav-fora`)
  os últimos botões que não cabem na linha e mostra o "Mais", que lista os escondidos. A ordem do HTML é a
  prioridade (Como usar é o primeiro a sair). Recalcula por `ResizeObserver` na própria barra, ao trocar de tela ou
  de idioma e quando as fontes carregam — nunca por `resize`. Onde a barra `.controles` está escondida, o menu traz
  também os seletores de idioma, tradução e comparação. No celular cabem Meu estudo, Buscar e Temas (a partir de
  360 px). Cabeçalho numa linha só a partir de 1500 px; na leitura, só a partir de 1850 px (Contexto, Modo estudo e
  "1 Tessalonicenses 5" não cabem antes). Botão novo na barra: é só pôr no lugar certo da ordem.
- Painel "Como usar" (`#painelAjuda`): aberto pelo botão "Como usar" da barra de navegação, pelo link na página
  inicial (`#btnAjudaInicio`) e no rodapé. O conteúdo fica no objeto `AJUDA` (pt/en/es: grupos → itens
  `[ação, ícone, título, texto]`), montado por `montarAjuda()`; o botão "Experimentar" de cada item chama
  `ACOES_AJUDA[ação]`. Funcionalidade nova no site: acrescente o item em `AJUDA` (nas três línguas) e a ação.
- Convite para entrar (`convidar(motivo)` / `mostrarConvite`): cartão no canto, no máximo uma vez por visita,
  depois de anotar, marcar, marcar capítulo lido ou abrir o 3º capítulo. "Agora não" adia 3, 7, 30 e 90 dias
  (`logos_convite`). Não aparece para quem está logado, sem rede ou com painel aberto.

## Ferramentas de tradução (`ferramentas/tradutor/`)

Dois motores: Argos (rápido, mediano) e NLLB-200 1.3B (`nllb.py`, ~10x mais lento, bem melhor em prosa).
O NLLB roda no GitHub Actions: `.github/workflows/traduzir.yml` (Actions → "Traduzir (NLLB)" → etapa,
nº de partes). Divide em N máquinas, junta, grava em `data/.../pt/` e envia ao branch `traducao-<etapa>`
para virar PR. Se faltar algo, rodar de novo com `retomar` = run id anterior. `lote.py --motor nllb --parte K/N`.
A etapa `glosas` do mesmo workflow usa o Argos (palavras soltas, 1 máquina, poucos minutos): é o
`traduzir_tudo.sh glosas` sem precisar de computador (ele usa Windows 11 agora, sem ambiente Linux).
O `nllb.py` protege marcadores de tópico ("I.", "1.", "(2.)"), devolve "milhas" (o modelo troca por "quilômetros") e
protege referências no formato USFM ("GEN 3:15"): cada grupo vira só os números durante a tradução e volta ao lugar
(sem isso, "JOS" virava "JOSÉ"). Antes de uma etapa inteira, rode o workflow com `amostra` = N: traduz N trechos, com e
sem a proteção, mostra no log e não grava nada (`teste_refs.py`). O robô do Actions não consegue criar o branch
`traducao-<etapa>` se o arquivo do workflow mudou depois do commit em que a execução começou: aí rode de novo com
`retomar` = número da execução (aproveita tudo o que já foi traduzido).

Glosas do interlinear: `ferramentas/glosas_pt.json` é o dicionário inglês→português, e `GLOSAS_FIXAS` em
`etapas.py` são as revisadas à mão (têm prioridade). `python3 etapas.py aplicar glosas` reaplica as duas.

Tradução offline e gratuita (modelo Argos en→pt-BR via CTranslate2). `./traduzir_tudo.sh [etapas]` e
`revisar.py` (refaz trechos com omissão). As pastas `venv/`, `modelo/` e `trabalho/` são locais (gitignore).
Qualidade: boa no Strong e nos títulos; legível mas com tropeços em Calvino e Easton — por isso o site
sempre mostra "Tradução automática". O modelo omite texto em listas longas e não conhece inglês arcaico;
o tradutor já moderniza ("thou", "ass") e refaz em pedaços frases que saem curtas demais.

## Vídeo de apresentação (`ferramentas/video/`)

Vídeo vertical (1080×1920, 30 qps, ~33 s) para ele postar. Tudo gerado, sem editor de vídeo:
`capturar.cjs` fotografa o site em tamanho de celular (grava em `telas/`, com `medidas.js`), `video.html` é a
animação (uma linha do tempo só, função `trilha(alvo, propriedade, [[segundo, valor], ...])`; aberta no
navegador ela toca sozinha) e `renderizar.cjs` fotografa quadro a quadro e junta com o ffmpeg em
`saida/sola-apresentacao.mp4` (`--fotos 2,13.5` só confere instantes). Precisa do site servido
(`SITE=http://localhost:8000`), do Playwright e do ffmpeg. `telas/`, `quadros/` e `saida/` ficam fora do git.
O interlinear do vídeo é João 1:14 e Salmo 23:1 porque João 3:16 tem glosas ruins ("amado", "possa têm").

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
- No celular (≤560px) a palavra "Sola" do topo só aparece se couber ao lado do nome do livro (senão fica só o
  símbolo): `.topo .marca` quebra a linha por dentro e esconde a sobra. Teste o topo com "1 Tessalonicenses 5".
- No celular, qualquer coisa que mude o foco ou o versículo ativo no meio de um toque desloca o texto (a barra
  do versículo está no fluxo) e o clique cai em outro lugar. Por isso a palavra-chave não recebe foco pelo toque
  (`mousedown` com `preventDefault`) e o `mouseenter` não ativa o versículo quando o dedo está nela. Não use
  `resize` para fechar coisas: no celular ele dispara ao rolar.
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
- Calvino (PR #7), Henry e Easton já foram traduzidos pelo NLLB; Nave (Temas) ainda é do Argos, mas é quase só
  títulos curtos. A Batch API da Anthropic (~US$ 45, uma vez) daria mais qualidade, se ele decidir pagar; o script
  antigo foi removido (gravava por cima dos originais) — seria preciso um novo que leia `trabalho/<etapa>.json`.
- Contas: ligadas (`google:true`) contra o projeto `rxmxxuyqvetbkjfilayc`. O login real e as regras do banco (RLS)
  só foram testados por ele, no navegador; daqui só rodou o teste com servidor falso. Se o login quebrar, voltar
  para `google:false` esconde tudo. O ambiente de nuvem "logos-biblia" libera `rxmxxuyqvetbkjfilayc.supabase.co`
  e `solabiblia.com.br`: sessões iniciadas nele conseguem conferir o projeto e o site publicado; no Default não.
- Palavras-chave: 124 palavras originais e 83 notas de contexto, escritas pelo Claude e ainda NÃO revisadas pelo
  Khennedy (são afirmações teológicas com o nome do site: ele precisa ler). Cobrem 851 dos 1.189 capítulos, mas
  nota própria de versículo só nas passagens mais conhecidas; ampliar é acrescentar `contexto(...)` no script.
  `--relatorio` mostra, por palavra, onde a forma em português não foi encontrada.
- Vocabulário: 701 termos (10.056 sublinhados, cerca de 8 por capítulo), também escritos pelo Claude e não
  revisados; as medidas e pesos são aproximados ("cerca de"). Os que ele mais precisa ler: os de teologia (anjo do
  SENHOR, alma, presbítero e bispo, Filho do Homem, santos, Renovo) e os de sentido sexual (conhecer, descobrir a
  nudez, sodomitas). A Bíblia Livre já é modernizada ("outrossim", "debalde", "mister" nem aparecem): a lista de
  palavras difíceis praticamente se esgota aqui, e ampliar mais seria sublinhar palavras comuns.
- Doutrinas reformadas: 50 temas (514 referências), escritos pelo Claude a partir da CFW e dos seus textos de prova,
  ainda NÃO revisados pelo Khennedy. Ficaram de fora, de propósito, pontos em que reformados divergem entre si
  (cessacionismo, milênio, salmodia exclusiva); acrescentar é só escrever `D(...)`.
- Glosas do interlinear: duas rodadas em `corrigir_glosas.py` (a segunda mexeu em 110 mil das 447 mil palavras: artigos,
  sufixos hebraicos, tu/vós, revisão das ~2.000 mais frequentes). Ainda há: glosas raras com erro de sentido do Argos
  (Rute 1:16 "Vou alojar", "as pessoas serão minhas"), cerca de 150 "você" com verbo que o script não reconhece,
  substantivo hebraico com sufixo fora de `substantivos_pt.json` (8% dessas palavras: só a concordância foi acertada)
  e 327 nomes raros duvidosos em inglês (`nomes_pt.py --relatorio`). Ampliar é acrescentar em `REVISAO`.
- Atlas: 1.240 dos 1.335 lugares com nome em português; os outros são quase todos de fora da Bíblia (Eridu, Punt).
- Inglês e espanhol: a interface está traduzida, mas atlas (rótulos do cartão do lugar), linha do tempo e
  fichas de contexto têm conteúdo só em português.
- Publicação pelo GitHub Actions (em vez de commitar `biblia/`, 35 MB): exige ele trocar a origem do Pages
  em Settings → Pages. Enquanto isso, `biblia/` continua no repositório e o `verificar.yml` confere.
