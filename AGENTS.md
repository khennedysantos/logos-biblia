# AGENTS.md — Guia e Regras do Projeto Sola

Este documento é a **fonte única de verdade** para agentes de IA (Antigravity, Claude Code, Codex, Cursor e similares) que trabalham neste repositório.

Mantenedor: **Khennedy** (presbiteriano reformado, formado em ADS). Comunique-se sempre em **português brasileiro**, de forma direta, clara e sem rodeios.

---

## 1. O que é o projeto

O **Sola** (**https://solabiblia.com.br**, de *Sola Scriptura*) é um site de estudo bíblico profundo em português — posicionado como **"um BibleHub em português"**, gratuito, sem anúncios e sem fins comerciais.

- **Histórico de nome**: o projeto chamava-se *"Logos"* no início (por isso o repositório ainda se chama `logos-biblia` e chaves antigas do `localStorage` mantêm o prefixo `logos_*` por retrocompatibilidade), mas o nome foi abandonado por conflito de marca com o Logos Bible Software. **Nunca reintroduza "Logos" na interface visível.**
- **Princípio de operação e custo zero**: nenhuma funcionalidade pode gerar custo por visitante (nada de APIs pagas ou chamadas de IA em tempo de execução). Todo processamento pesado (tradução, geração de interlinear, vocabulário, páginas estáticas) roda antes, offline ou no GitHub Actions, e vira arquivo estático no repositório. Manter o site sem fins comerciais também preserva as licenças gratuitas do acervo (como CC BY-NC).
- **O que o Sola entrega hoje**:
  - **Bíblia completa** em três traduções de domínio público — Bíblia Livre (`blivre`, PT), King James 1769 (`kjv`, EN) e Reina-Valera Antigua (`rva`, ES) — além dos textos originais (`orig`: Hebraico WLC no AT e Grego *Textus Receptus* no NT; `byz`: Grego Bizantino no NT), com comparação lado a lado e modo de leitura contínua.
  - **Interlinear palavra por palavra** (AT em hebraico e NT em grego, base STEPBible / Tyndale House) com transliteração, glosa em português e número de Strong integrado ao léxico (`14.197` entradas).
  - **Palavras-chave sublinhadas** (traço dourado contínuo, com notas teológicas próprias do Sola) e **vocabulário explicado** (traço pontilhado para mais de `700` termos antigos, técnicos, medidas ou palavras que mudaram de sentido) na Bíblia Livre.
  - **Comentários clássicos versículo a versículo**: João Calvino (`47` livros) e Matthew Henry (`18` livros), com tradução automática em português sobreposta ao original inglês e aviso transparente na tela.
  - **Temas e doutrinas**: índice temático de Nave + `50` **doutrinas da fé reformada** (baseadas na Confissão de Fé de Westminster e nos Catecismos, com textos de prova da Bíblia Livre já embutidos).
  - **Dicionário bíblico** (Easton), **referências cruzadas** (`openbible.info`), **fichas de contexto** dos `66` livros, **linha do tempo**, **planos de leitura** e **atlas bíblico interativo** (`+1.300` lugares e viagens missionárias de Paulo).
  - **Estudo pessoal *local-first***: marcações em 4 cores, notas, capítulos lidos, ofensiva de dias seguidos e backup manual em arquivo `.json` direto no navegador, funcionamento offline via PWA (`sw.js`) e **contas opcionais via Supabase** para sincronizar entre aparelhos.
- **Próximos passos desejados na visão do projeto**: evolução do painel pessoal e curadoria de *"aulas públicas → síntese"* ligadas ao acervo (incorporando o vídeo oficial e escrevendo síntese própria com crédito, respeitando direitos autorais).

---

## 2. Regras inegociáveis para agentes

Qualquer agente que atue neste repositório **deve** cumprir rigorosamente estas cinco regras:

1. **Sempre trabalhar em branch nova e abrir Pull Request — nunca commitar direto na `main`**:
   - **Jamais faça commit ou push direto na branch `main`**, nem mesmo para correções pequenas ou ajustes de texto.
   - Sempre atualize a referência remota antes (`git fetch origin main`), crie uma branch nova a partir de `origin/main`, faça os commits nela e abra um Pull Request contra a `main` para revisão.
2. **O site é 100% estático no GitHub Pages, sem backend**:
   - Não introduza servidor de aplicação (Node/Python/PHP/etc.), SSR dinâmico, banco de dados obrigatório para leitura, frameworks JS (React, Vue, etc.) nem etapa de empacotamento/build (`npm run build`, Vite, Webpack).
   - Fontes e bibliotecas ficam auto-hospedadas no próprio repositório (`fontes/`, `vendor/`). Não adicione Google Fonts nem CDNs externos (`unpkg`, `jsdelivr`). As únicas conexões externas no cliente são os *tiles* do OpenStreetMap (apenas ao abrir o Atlas) e o Supabase (apenas se o visitante optar por entrar na conta).
3. **Não alterar o arquivo `CNAME` nem os dados já traduzidos**:
   - **Nunca apague, renomeie ou edite o arquivo `CNAME`** (`solabiblia.com.br`).
   - **Não altere, sobrescreva nem regere por cima os dados já traduzidos** (`data/commentaries/calvin/pt/`, `data/commentaries/henry/pt/`, `data/dictionary/pt/`, `data/topics/pt/`, o campo `defpt` em `data/strongs/{G,H}.json`, os arquivos `titulos_pt.json`, as glosas já traduzidas/revisadas em `data/interlinear/` e `ferramentas/glosas_pt.json`), nem apague ou sobrescreva os textos originais em inglês em `data/`, salvo pedido explícito do mantenedor.
4. **O pipeline de tradução em Python é separado do site**:
   - `ferramentas/tradutor/` (e os demais scripts em `ferramentas/`) funciona offline/em lote, separado da aplicação web. O site em produção lê apenas os JSONs estáticos em `/data/...` e não executa Python.
   - Ambientes virtuais, modelos baixados e pastas temporárias (`venv/`, `modelo/`, `modelo-*`, `trabalho/`, `ferramentas/fontes/`, `ferramentas/video/{telas,quadros,saida}/`) ficam fora do controle de versão (`.gitignore`).
   - Não rode traduções longas (dezenas de minutos) dentro do ambiente interativo do agente: o trabalho pesado roda no GitHub Actions (`.github/workflows/traduzir.yml`), que publica o resultado em uma branch `traducao-<etapa>` para revisão via Pull Request.
5. **Nunca editar páginas geradas à mão**:
   - Não edite manualmente `biblia/`, `privacidade/index.html`, `404.html`, `sitemap.xml` nem o bloco entre `<!--CONTEUDO-->` e `<!--/CONTEUDO-->` dentro de `index.html`.
   - **Sempre que modificar `index.html`, `app.js`, `style.css`, `sw.js` ou qualquer arquivo em `ferramentas/paginas/*.html`, execute `python3 ferramentas/gerar_paginas.py`** e inclua os arquivos regenerados no commit. O CI (`.github/workflows/verificar.yml`) reprova qualquer PR em que as páginas geradas estejam defasadas.

---

## 3. Stack tecnológica

- **Aplicação web (SPA + HTML pré-renderizado para SEO)**:
  - **HTML5** (`index.html` + páginas estáticas pré-geradas por livro e capítulo em `biblia/`).
  - **CSS3 puro** (`style.css`, variáveis CSS para temas claro/escuro: marfim, azul-noite e ouro envelhecido).
  - **JavaScript puro** (`app.js`, `"use strict"`, ES2020+, roteamento via `history.pushState`, zero dependências de build).
  - **PWA / Offline**: Service Worker (`sw.js`) + `manifest.webmanifest`.
- **Hospedagem**: **GitHub Pages** servindo diretamente a raiz da branch `main` no domínio customizado `solabiblia.com.br` (`CNAME`).
- **Ativos auto-hospedados**:
  - `fontes/`: *Cormorant Garamond* (títulos), *Cardo* (Escritura, grego e hebraico) e *Inter* (interface) em `.woff2` sob SIL Open Font License.
  - `vendor/leaflet/`: biblioteca de mapas Leaflet (BSD) para o Atlas.
  - `vendor/supabase/`: cliente JS do Supabase (~220 KB), carregado sob demanda apenas quando há sessão salva, retorno de login ou clique em "Entrar". Banco configurado com tabela única `public.itens` e RLS em `ferramentas/supabase.sql`.
- **Geradores e validação (`ferramentas/`)**: **Python 3** usando exclusivamente a biblioteca padrão (`json`, `re`, `hashlib`, `pathlib`, `urllib`, `unicodedata`, etc.).
- **Pipeline de tradução offline (`ferramentas/tradutor/`)**: **Python 3** + `ctranslate2` + `sentencepiece`, com dois motores:
  - **NLLB-200 distilled 1.3B** (`JustFrederik/nllb-200-distilled-1.3B-ct2-int8`, Meta, licença CC BY-NC) para prosa (Calvino, Henry, Easton, temas e verbos contextualizados).
  - **Argos Translate** (`translate-en_pb-1_9`) para glosas curtas/palavras soltas.
- **Vídeo de apresentação (`ferramentas/video/`)**: **Node.js** CommonJS (`.cjs`), **Playwright** e **ffmpeg**.
- **CI / Automação (`.github/workflows/`)**: **GitHub Actions** (Python 3.12 + Node 22 em `verificar.yml`; matriz paralela com cache de modelo em `traduzir.yml`).

---

## 4. Estrutura de pastas e arquitetura detalhada

```text
/
├── index.html                  # Casca principal da SPA (início pré-renderizado entre <!--CONTEUDO-->)
├── style.css                   # Estilos globais, variáveis de tema (claro/escuro) e responsividade
├── app.js                      # Toda a lógica da aplicação no navegador (~2.400 linhas, JS puro)
├── sw.js                       # Service Worker (cache do app e cache offline de /data/)
├── manifest.webmanifest        # Manifesto PWA (instalação no celular/desktop)
├── CNAME                       # Domínio customizado (solabiblia.com.br) — NUNCA ALTERAR
├── 404.html                    # Gerado por gerar_paginas.py (carrega o app em rotas desconhecidas)
├── robots.txt                  # Regras de indexação + referência ao sitemap.xml
├── sitemap.xml                 # Gerado por gerar_paginas.py (todas as URLs canônicas)
├── favicon.svg / *.png / og.png # Ícones do site, PWA e imagem Open Graph (1200×630)
├── AGENTS.md                   # Este guia (fonte única de regras e arquitetura para agentes)
├── CLAUDE.md                   # Ponteiro (@AGENTS.md) para o Claude Code
├── LEIA-ME.md                  # Resumo humano do projeto
│
├── biblia/                     # GERADO (não editar): 66 páginas de livro + 1.189 de capítulo
│   └── <livro-slug>/[<cap>/]index.html
├── privacidade/                # GERADO (não editar): página avulsa a partir de ferramentas/paginas/
│   └── index.html
│
├── fontes/                     # Fontes .woff2 locais (Cardo, Cormorant Garamond, Inter) + LICENCA-OFL.txt
├── vendor/
│   ├── leaflet/                # Leaflet auto-hospedado (Atlas)
│   └── supabase/               # Cliente Supabase JS carregado sob demanda (contas opcionais)
│
├── data/                       # Todo o acervo bíblico estático consumido via fetch('/data/...')
│   ├── books.json              # Cânon (66 livros, códigos USFM, nomes pt/en/es) e lista de traduções
│   ├── bibles/                 # {blivre,kjv,rva,orig,byz}/{USFM}.json (capítulos → versículos)
│   ├── interlinear/            # {USFM}/{cap}.json → palavras [original, translit, strong, glosa_pt]
│   ├── strongs/                # G.json (grego) e H.json (hebraico): campos def (EN) e defpt (PT)
│   ├── palavras/               # indice.json + {USFM}.json (palavras-chave e vocabulário na Bíblia Livre)
│   ├── commentaries/
│   │   ├── calvin/             # manifest.json, {USFM}/{cap}.json (EN) e pt/{USFM}/{cap}.json (PT)
│   │   └── henry/              # manifest.json, {USFM}/{cap}.json (EN) e pt/{USFM}/{cap}.json (PT)
│   ├── dictionary/             # Easton: index.json, A..Z.json (EN), titulos_pt.json e pt/A..Z.json
│   ├── topics/                 # Nave: index.json, A..Z.json (EN), aliases_pt.json, titulos_pt.json,
│   │                           #       pt/A..Z.json e doutrinas.json (50 doutrinas reformadas)
│   ├── crossrefs/              # {USFM}/{cap}.json (referências cruzadas do openbible.info)
│   ├── places.json             # 1.335 lugares bíblicos com coordenadas e campo p (nome em PT)
│   ├── journeys.json           # Rotas das viagens de Paulo para o Atlas
│   ├── context.json            # Fichas de contexto dos 66 livros (autor, época, tema, esboço)
│   ├── plans.json              # 3 planos de leitura bíblica
│   └── timeline.json           # Eventos da linha do tempo bíblica
│
├── ferramentas/                # Scripts offline de geração, revisão e validação (Python 3 stdlib)
│   ├── gerar_paginas.py        # Gera biblia/, privacidade/, index.html, 404.html, sitemap.xml e hashes
│   ├── validar_dados.py        # Valida integridade estrutural e textual de todo o acervo em data/
│   ├── paginas/privacidade.html# Conteúdo-fonte da política de privacidade (/privacidade/)
│   ├── CONTAS.md               # Passo a passo da sincronização opcional com Supabase
│   ├── supabase.sql            # Schema SQL (tabela public.itens, RLS e RPC apagar_conta)
│   ├── gerar_interlinear_at.py # Gera interlinear do AT (STEPBible TAHOT na numeração da Bíblia Livre)
│   ├── corrigir_interlinear_nt.py # Alinha interlinear do NT (STEPBible TAGNT)
│   ├── stepbible.py            # Leitor/alinhador das fontes STEPBible (em ferramentas/fontes/, fora do git)
│   ├── corrigir_glosas.py      # Revisão gramatical e lexical em lote das glosas do interlinear
│   ├── glosas_revisao.py       # ~2.000 glosas mais frequentes revisadas + regras por gramática/pessoa
│   ├── conjugar.py             # Conjugação tu/vós, imperativos e correções morfológicas em PT
│   ├── nomes_pt.py             # Extrai nomes próprios na grafia da Bíblia Livre → nomes_pt.json
│   ├── glosas_pt.json          # Dicionário base inglês→português das glosas — NÃO SOBRESCREVER
│   ├── nomes_pt.json           # Mapa Strong → nome próprio em português
│   ├── substantivos_pt.json    # Substantivos para remontagem de sufixos hebraicos
│   ├── gerar_palavras.py       # Gera data/palavras/ (notas das palavras-chave + aplica vocabulário)
│   ├── vocabulario.py          # Definições dos +700 termos difíceis/técnicos sublinhados
│   ├── doutrinas.py            # Fonte das 50 doutrinas reformadas (CFW e Catecismos)
│   ├── gerar_doutrinas.py      # Valida referências e gera data/topics/doutrinas.json
│   ├── gerar_atlas_pt.py       # Preenche nomes em português (campo p) em data/places.json
│   ├── gerar_crossrefs.py      # Converte referências cruzadas do openbible.info
│   ├── baixar_henry.py         # Baixa comentário de Matthew Henry (domínio público)
│   ├── tradutor/               # Pipeline isolado de tradução automática offline (Argos / NLLB)
│   │   ├── etapas.py           # Prepara entradas de data/ e aplica traduções em data/.../pt/
│   │   ├── nllb.py             # Motor NLLB-200 1.3B (protege refs USFM, numerais romanos e latim)
│   │   ├── tradutor.py         # Motor Argos Translate (moderniza inglês arcaico e fatia frases)
│   │   ├── lote.py             # Execução particionada (--parte K/N) com retomada segura
│   │   ├── revisar.py          # Retraduz trechos em que o modelo omitiu conteúdo
│   │   ├── teste_refs.py       # Testa amostras antes de rodar uma etapa inteira no Actions
│   │   ├── traduzir_tudo.sh    # Script local para etapas rápidas com Argos
│   │   └── entradas/           # Entradas auxiliares versionadas (ex.: verbos contextualizados)
│   └── video/                  # Geração automatizada do vídeo vertical (1080×1920, 30 fps)
│       ├── capturar.cjs        # Captura telas mobile do site com Playwright
│       ├── video.html          # Animação em linha do tempo única
│       └── renderizar.cjs      # Renderiza quadro a quadro e monta MP4 com ffmpeg
│
└── .github/workflows/
    ├── verificar.yml           # CI em push/PR: node --check, validar_dados.py e gerar_paginas.py
    └── traduzir.yml            # Execução manual (workflow_dispatch) da tradução em matriz NLLB/Argos
```

### Detalhes importantes da arquitetura

- **Roteamento SPA e SEO (`app.js` + `gerar_paginas.py`)**:
  - Três vistas (`est.vista`): início (`/`), livro (`/biblia/joao/`) e capítulo (`/biblia/joao/3/`, com `#v16` rolando direto ao versículo) via `history.pushState`. Links antigos `#/JHN/3` continuam funcionando e são convertidos automaticamente.
  - Toda referência bíblica é um `<a href>` real gerado por `linkRef`; um único ouvinte de clique em `iniciar()` intercepta e navega sem recarregar. Todos os `fetch` usam caminhos absolutos (`/data/...`).
  - `gerar_paginas.py` cria uma página HTML real para cada livro e capítulo em `biblia/` (com `<title>`, meta description, texto do capítulo e `BreadcrumbList` JSON-LD para buscadores) e páginas de texto avulsas sem o app a partir de `ferramentas/paginas/*.html` (como `/privacidade/`, cujo link está cadastrado no Branding do login Google — atualize a data no topo de `ferramentas/paginas/privacidade.html` se mudar o que o site armazena).
- **Service Worker (`sw.js`)**:
  - Páginas HTML usam estratégia *rede primeiro*, caindo para a página inicial em cache quando sem internet (o `app.js` lê `location.pathname` e abre o capítulo certo).
  - Arquivos em `/data/` usam o cache `sola-dados-v1` (*stale-while-revalidate*). O botão *"Baixar a Bíblia"* no painel Sobre salva todos os capítulos da tradução atual nesse mesmo cache.
- **Navegação responsiva e painéis (`app.js`)**:
  - **Barra `.navbar` e menu `#navMais` (`#menuMais`)**: `ajustarNav()` esconde com `nav-fora` os últimos botões que não cabem na largura disponível e exibe o botão *"Mais"*. A prioridade segue a ordem no HTML (*Como usar* sai primeiro). Recalcula via `ResizeObserver` na própria barra, ao mudar de vista/idioma e após carregar fontes — nunca por evento `resize` da janela. Onde `.controles` fica oculto (`≤700px`), o menu *"Mais"* também exibe os seletores de idioma, tradução e comparação. Para adicionar um botão novo na barra, basta inseri-lo na posição de prioridade correta no HTML.
  - **Painel "Meu estudo"**: dividido em duas abas (`est.abaEstudo`): *Estudo* (estatísticas, progresso por livro, dias seguidos, marcações) e *Perfil* (conta, preferências, backup, privacidade, excluir conta), acessível também pelo botão `#btnPerfil` no topo.
  - **Painel "Como usar" (`#painelAjuda`)**: montado por `montarAjuda()` a partir do objeto `AJUDA` (`pt`/`en`/`es`: grupos → `[ação, ícone, título, texto]`), com botões *"Experimentar"* ligados a `ACOES_AJUDA[ação]`. Ao criar funcionalidade nova no site, adicione-a em `AJUDA` nos três idiomas e registre a ação correspondente.
- **Contas opcionais (`CONTA` em `app.js` + `ferramentas/CONTAS.md`)**:
  - Sem conta, tudo funciona via `localStorage` (`logos_lidos`, `logos_ultimo`, notas, marcas, planos).
  - Se `CONTA.url` estiver vazio ou `google` e `email` estiverem `false`, toda a interface de conta desaparece.
  - A sincronização (`sincronizar()`) é *local-first*: `tocar(tipo, chave)` registra pendências em `est.sinc.pend`, e conflitos no mesmo item são resolvidos pelo maior `ts` (`apagar` também grava timestamp). O mapa `DADOS` descreve cada categoria (`nota`, `marca`, `plano`, `lido`, `estado`).
  - O convite discreto para criar conta (`convidar(motivo)` / `mostrarConvite`) aparece no máximo uma vez por visita após interações reais e respeita adiamentos progressivos de 3, 7, 30 e 90 dias (`logos_convite`).
- **Acervo em `data/` e scripts geradores**:
  - **Interlinear (`data/interlinear/`)**: sempre na numeração de versículos da Bíblia Livre (que difere do hebraico massorético em ~2.300 versículos e do grego em ~50; `gerar_interlinear_at.py` e `corrigir_interlinear_nt.py` fazem o alinhamento usando os dados da STEPBible em `ferramentas/fontes/`). No AT, o Strong é o da raiz; partículas feitas só de prefixo/sufixo ficam sem Strong. As glosas passam por `corrigir_glosas.py` (`preparar` / `aplicar`), auxiliado por `stepbible.py`, `nomes_pt.py` (`Yahweh` → `SENHOR`), `glosas_revisao.py` (`REVISAO`), `substantivos_pt.json` (sufixos pronominais hebraicos em 3ª pessoa `dele/dela/deles/delas`), concordância de artigos gregos pelo gênero léxico extraído da Bíblia Livre e `conjugar.py` (`você` → `tu/vós` conjugado). O comando `aplicar` é idempotente.
  - **Palavras sublinhadas (`data/palavras/`)**: exclusivas da Bíblia Livre (ocultas na leitura contínua e nas outras traduções; controladas por `logos_chave` e `logos_voc`), geradas por `ferramentas/gerar_palavras.py` (~75 s):
    - *Palavras-chave* (traço dourado cheio): definidas no próprio `gerar_palavras.py` via `lema(strong, tradução, formas, nota)` (primeira ocorrência no capítulo) e `contexto("PSA.51.10", "H1254", nota)` (recusa se o Strong não existir no versículo).
    - *Vocabulário* (traço pontilhado): definido em `ferramentas/vocabulario.py` via `t(palavra, formas, significado, nota, s=(strongs), exige)`. `exige=True` restringe o sublinhado aos versículos que contêm aquele Strong (evita falsos positivos de homônimos como *"funda"* arma × *"cova funda"*). Máximo de 5 marcas por versículo (até 3 de vocabulário), sem sobrepor palavras-chave. Use `--relatorio` para auditar cobertura e confirmação de Strong.
  - **Comentários (`data/commentaries/`)**: Calvino cobre 47 livros; nos livros restantes entra Matthew Henry (`18` livros, baixado por `baixar_henry.py`; Cantares e 2Sm 23–24 não existem na fonte). Quando o idioma da interface é Português, o app sobrepõe `pt/{USFM}/{cap}.json` ao original inglês e resolve comentários em bloco buscando o versículo anterior ou o primeiro do capítulo.
  - **Dicionário, Temas e Doutrinas (`data/dictionary/`, `data/topics/`)**: em Easton/Nave traduzidos, as referências ficam no padrão USFM (`GEN 3:15; 4:1`) convertidas por `refs_usfm` (`etapas.py`) e transformadas em links clicáveis por `linkarRefs` (`app.js`). Já `data/topics/doutrinas.json` traz as 50 doutrinas reformadas escritas em `ferramentas/doutrinas.py` e geradas por `python3 ferramentas/gerar_doutrinas.py` (`--texto` imprime tudo para leitura; `validar_dados.py` confere se os versículos batem exatamente com a Bíblia Livre).
- **Funcionamento do pipeline `ferramentas/tradutor/`**:
  - `nllb.py` protege marcadores de estrutura (`I.`, `1.`, `(2.)`), preserva `"milhas"` (evitando conversão indevida para `"quilômetros"`) e mascara referências USFM (`GEN 3:15`) durante a inferência para que abreviações como `JOS` não virem `"JOSÉ"`.
  - Antes de disparar uma etapa grande no workflow `.github/workflows/traduzir.yml`, é possível rodar com `amostra = N` (executa `teste_refs.py` no log sem gravar nada). Se uma execução atingir o tempo limite de 6h do GitHub, basta disparar novamente passando `retomar = <run_id>` (inclusive se o arquivo do workflow tiver mudado durante a execução anterior).
  - Para glosas do interlinear, `GLOSAS_FIXAS` em `etapas.py` tem prioridade sobre `ferramentas/glosas_pt.json`; `python3 etapas.py aplicar glosas` reaplica ambos.

---

## 5. Comandos de desenvolvimento, validação e testes

Execute os comandos a partir da raiz do repositório:

```bash
# 1. Servir o site localmente em http://localhost:8000
python3 -m http.server 8000

# 2. Validar sintaxe do JavaScript (OBRIGATÓRIO após editar JS)
node --check app.js && node --check sw.js

# 3. Validar integridade dos dados (OBRIGATÓRIO após tocar em data/ ou geradores)
python3 ferramentas/validar_dados.py

# 4. Regenerar páginas estáticas, sitemap e versões (OBRIGATÓRIO após tocar em index.html, app.js, style.css, sw.js ou ferramentas/paginas/)
python3 ferramentas/gerar_paginas.py
git status --short
```

### Diretrizes de teste visual no navegador (Playwright)

- Ao testar mudanças visuais ou de interação com Playwright:
  - Passe `serviceWorkers: 'block'` na criação do contexto (caso contrário o `sw.js` intercepta rotas simuladas e serve cache antigo) e `reducedMotion: 'reduce'` (evita falhas intermitentes de clique causadas por rolagem suave). Se estiver em container com Chromium pré-instalado em `/opt/pw-browsers/chromium`, passe `executablePath`.
  - Confira ausência de erros no console e inspecione nos dois temas (**claro** e **escuro**) e nas larguras **`390`**, **`1280`** e **`1600`** px.
  - Para testar contas sem bater no Supabase real, intercepte `/vendor/supabase/supabase.js` devolvendo um cliente simulado (`auth.getSession/onAuthStateChange/signInWithOAuth/signOut`, `from().select().gte().order().range()`, `upsert`, `rpc`) e ajuste `CONTA` na resposta interceptada de `app.js` (nota: variáveis `const` de topo como `est` são acessíveis em `page.evaluate`, mas não em `window.est`).
- Antes de encerrar qualquer tarefa, confira com `git status` se todos os arquivos novos ou regenerados entraram no controle de versão. Ao orientar testes manuais após o merge na `main`, lembre que o GitHub Pages leva ~2 minutos para publicar e pode exigir `Ctrl+Shift+R` no navegador.

---

## 6. Convenções de código, interface, CSS e licenças

- **Idioma do código e da UI**:
  - Nomes de variáveis, funções, classes CSS, scripts e comentários devem ser escritos em **português**.
  - Textos visíveis na interface ficam centralizados nos objetos `UI`, `NAV` e `AJUDA` (`pt`, `en`, `es`) em `app.js`.
- **Cuidados essenciais de layout, CSS e mobile (não regredir)**:
  - **Cabeçalho no celular (`≤560px`)**: a palavra `"Sola"` ao lado do símbolo só aparece se couber junto ao nome do livro (`.topo .marca` quebra internamente e esconde o excedente). Sempre teste o topo mobile abrindo **`1 Tessalonicenses 5`**. Cabeçalho em linha única só ocorre a partir de `1500px` (ou `1850px` na tela de leitura).
  - **Toque e foco no celular**: a barra de ações do versículo fica no fluxo do documento em `≤560px` (entre o texto e a gaveta; flutuando ela cobria o botão *Salvar*). Qualquer mudança de foco ou versículo ativo no meio do toque desloca o texto e faz o clique errar o alvo — por isso palavras sublinhadas usam `mousedown` com `preventDefault` e ignoram `mouseenter` vindo de toque. **Nunca use o evento `resize` da janela para fechar menus/painéis**, pois no celular ele dispara ao rolar a página.
  - **Regras globais obrigatórias em `style.css`**:
    - `font-variant-numeric: lining-nums` no `body` (sem isso, o algarismo `"1"` da fonte Cormorant Garamond parece `"I"`).
    - `button, input, select, textarea { color: inherit }` (botões não herdam cor por padrão nos navegadores).
    - `.verso > p` estiliza apenas o texto bíblico do versículo; o conteúdo das gavetas tem estilo próprio.
    - Texto em português ao lado de hebraico (RTL) exige `unicode-bidi: isolate`, senão a pontuação se embaralha.
- **Downloads e geração de dados**:
  - Gere nomes de arquivos de download **sem acentos** (o Chrome descarta nomes acentuados em downloads gerados no cliente).
  - Arquivos grandes de dados devem ser gerados/atualizados por script e verificados com `validar_dados.py`, nunca editados manualmente em massa.
- **Créditos e licenças (manter sempre visíveis no painel "Fontes e licenças")**:
  - Textos bíblicos: `scrollmapper/bible_databases` (domínio público).
  - Interlinear e morfologia: STEPBible / Tyndale House, Cambridge (**CC BY**).
  - Léxico de Strong, Calvino, Matthew Henry, Easton e Nave: domínio público.
  - Referências cruzadas e lugares do Atlas: `openbible.info` (**CC-BY**).
  - Traduções automáticas: Argos Translate e NLLB-200 da Meta (**CC BY-NC** — exige manutenção do caráter não comercial do site).
  - Fontes tipográficas: Cardo, Cormorant Garamond e Inter (**SIL Open Font License**). Mapa: Leaflet (**BSD**) + OpenStreetMap.

---

## 7. Estado atual e pendências conhecidas

- **Contato e indexação**: o e-mail no rodapé ainda está como `contato@exemplo.com`; o cadastro no Google Search Console e envio do `sitemap.xml` dependem da conta pessoal do mantenedor.
- **Traduções automáticas**: Calvino, Matthew Henry e Dicionário de Easton já estão traduzidos com NLLB-200; Nave (Temas) ainda usa tradução do Argos (composta quase só de títulos curtos).
- **Revisão teológica pendente pelo mantenedor**:
  - *Palavras-chave* (`124` lemas e `83` notas de contexto em `851` capítulos), *Vocabulário* (`701` termos / `10.056` ocorrências, especialmente termos teológicos e expressões de sentido sensível) e *Doutrinas reformadas* (`50` temas / `514` referências; pontos de divergência interna reformada como milênio, cessacionismo e salmodia exclusiva ficaram de fora de propósito) foram redigidos por IA e aguardam leitura/revisão autoral do Khennedy.
- **Refinamentos residuais nos dados**:
  - *Glosas do interlinear*: após duas grandes rodadas em `corrigir_glosas.py`, restam poucos casos raros de sentido do Argos, ~150 ocorrências de `"você"` com verbos fora da tabela, ~8% de substantivos hebraicos com sufixo fora de `substantivos_pt.json` e `327` nomes próprios raros (`nomes_pt.py --relatorio`). Para corrigir glosas pontuais, adicione em `REVISAO` (`glosas_revisao.py`) e rode `aplicar`.
  - *Atlas e idiomas*: `1.240` de `1.335` lugares têm nome em português; interface suporta `pt`/`en`/`es`, mas rótulos internos do Atlas, linha do tempo e fichas de contexto estão apenas em português.
- **Contas Supabase**: ativas (`google: true`) apontando para o projeto `rxmxxuyqvetbkjfilayc`; em caso de falha de autenticação, mudar `google: false` em `CONTA` oculta imediatamente a funcionalidade.
- **GitHub Pages**: enquanto a publicação continuar saindo direto da branch `main` (e não via GitHub Actions em *Settings → Pages*), a pasta `biblia/` permanece versionada no repositório e verificada pelo `verificar.yml`.
