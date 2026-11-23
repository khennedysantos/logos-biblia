# AGENTS.md — Guia e Regras do Projeto Sola

Este documento é a **fonte única de verdade** para agentes de IA (Antigravity, Claude Code, Codex, Cursor e similares) que trabalham neste repositório.

Mantenedor: **Khennedy** (presbiteriano reformado, formado em ADS; usa **Windows 11** sem ambiente Linux local, com Firefox/Chrome). Comunique-se sempre em **português brasileiro**, de forma direta, clara e sem rodeios.

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
  - **Temas e símbolos de fé**: índice temático de Nave + os **credos da Igreja antiga** (Apostólico, Niceno, Atanásio e Calcedônia) + a **Confissão de Fé de Westminster**, o **Catecismo Maior** e o **Breve Catecismo** (1647) e as **Três Formas de Unidade** — **Confissão Belga** (1561), **Catecismo de Heidelberg** (1563) e **Cânones de Dort** (1619) —, no texto de domínio público traduzido pelo Sola, com os textos de prova (os da própria Assembleia de Westminster nos Padrões) (páginas em `/confissoes/`; os 33 capítulos da Confissão são as "doutrinas" da busca de Temas, da doutrina do dia e da aba CFW & Refs).
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
   - Fontes e bibliotecas ficam auto-hospedadas no próprio repositório (`fontes/`, `vendor/`). Não adicione Google Fonts nem CDNs externos (`unpkg`, `jsdelivr`). A única conexão externa no cliente é o Supabase (apenas se o visitante optar por entrar na conta, ou ao abrir a página pública de um perfil em `/perfil/<apelido>/`, que lê o cartão por `fetch` com a chave pública); o mapa do Atlas é desenhado pelo próprio site, sem *tiles* de fora.
3. **Não alterar o arquivo `CNAME` nem os dados já traduzidos**:
   - **Nunca apague, renomeie ou edite o arquivo `CNAME`** (`solabiblia.com.br`) nem o `google04e0bb96435230dc.html` (verificação do Google Search Console).
   - **Não altere, sobrescreva nem regere por cima os dados já traduzidos** (`data/commentaries/calvin/pt/`, `data/commentaries/henry/pt/`, `data/dictionary/pt/`, `data/topics/pt/`, o campo `defpt` em `data/strongs/{G,H}.json`, os arquivos `titulos_pt.json`, as glosas já traduzidas/revisadas em `data/interlinear/` e `ferramentas/glosas_pt.json`), nem apague ou sobrescreva os textos originais em inglês em `data/`, salvo pedido explícito do mantenedor.
4. **O pipeline de tradução em Python é separado do site**:
   - `ferramentas/tradutor/` (e os demais scripts em `ferramentas/`) funciona offline/em lote, separado da aplicação web. O site em produção lê apenas os JSONs estáticos em `/data/...` e não executa Python.
   - Ambientes virtuais, modelos baixados e pastas temporárias (`venv/`, `modelo/`, `modelo-*`, `trabalho/`, `ferramentas/fontes/`, `ferramentas/video/{telas,quadros,saida}/`) ficam fora do controle de versão (`.gitignore`).
   - Não rode traduções longas (dezenas de minutos) dentro do ambiente interativo do agente: o trabalho pesado roda no GitHub Actions (`.github/workflows/traduzir.yml`), que publica o resultado em uma branch `traducao-<etapa>` para revisão via Pull Request.
5. **Nunca editar páginas geradas à mão**:
   - Não edite manualmente `biblia/`, `lexico/`, `dicionario/`, `temas/`, `confissoes/`, `privacidade/index.html`, `404.html`, `sitemap.xml` nem o bloco entre `<!--CONTEUDO-->` e `<!--/CONTEUDO-->` dentro de `index.html`.
   - **Sempre que modificar `index.html`, `app.js`, `style.css`, `lexico.css`, `sw.js`, qualquer coisa em `data/` ou qualquer arquivo em `ferramentas/paginas/*.html`, execute `python3 ferramentas/gerar_paginas.py`** e inclua os arquivos regenerados no commit. O CI (`.github/workflows/verificar.yml`) reprova qualquer PR em que as páginas geradas estejam defasadas.

---

## 3. Stack tecnológica

- **Aplicação web (SPA + HTML pré-renderizado para SEO)**:
  - **HTML5** (`index.html` + páginas estáticas pré-geradas por livro e capítulo em `biblia/`).
  - **CSS3 puro** (`style.css`, variáveis CSS para o modelo editorial *Bancada Genebra*: tema claro *Papel Linho & Rubrica* — papel `#FAF7F0`, carmim `#8C2D23` e ouro envelhecido — e tema escuro *Vigília* em grafite quente `#171613`).
  - **JavaScript puro** (`app.js`, `"use strict"`, ES2020+, roteamento via `history.pushState`, zero dependências de build).
  - **PWA / Offline**: Service Worker (`sw.js`) + `manifest.webmanifest`.
- **Hospedagem**: **GitHub Pages** servindo diretamente a raiz da branch `main` no domínio customizado `solabiblia.com.br` (`CNAME`).
- **Ativos auto-hospedados**:
  - `fontes/`: *Cormorant Garamond* (títulos), *Cardo* (Escritura, grego e hebraico) e *Inter* (interface) em `.woff2` sob SIL Open Font License.
  - `vendor/leaflet/`: biblioteca de mapas Leaflet (BSD) para o Atlas, que desenha a base própria de `data/mapa/base.json` (Natural Earth, domínio público) em vez de *tiles* de terceiros.
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
├── lexico.css                  # Folha leve das páginas avulsas (léxico, dicionário, temas, versículos); mudá-la reescreve ~55 mil páginas
├── app.js                      # Toda a lógica da aplicação no navegador (~2.880 linhas, JS puro)
├── sw.js                       # Service Worker (cache do app e cache offline de /data/)
├── manifest.webmanifest        # Manifesto PWA (instalação no celular/desktop)
├── CNAME                       # Domínio customizado (solabiblia.com.br) — NUNCA ALTERAR
├── google04e0bb96435230dc.html # Verificação do Google Search Console — NUNCA APAGAR
├── 404.html                    # Gerado por gerar_paginas.py (carrega o app em rotas desconhecidas)
├── robots.txt                  # Regras de indexação + referência ao sitemap.xml
├── sitemap.xml                 # Gerado: índice de sitemap-{biblia,lexico,acervo}.xml (máx. 50 mil endereços por arquivo)
├── favicon.svg / *.png / og.png # Ícones do site, PWA e imagem Open Graph (1200×630)
├── AGENTS.md                   # Este guia (fonte única de regras e arquitetura para agentes)
├── CLAUDE.md                   # Ponteiro (@AGENTS.md) para o Claude Code
├── LEIA-ME.md                  # Resumo humano do projeto
│
├── biblia/                     # GERADO (não editar): 66 páginas de livro + 1.189 de capítulo + 31.102 de versículo
│   └── <livro-slug>/[<cap>/[<v>/]]index.html
├── privacidade/                # GERADO (não editar): página avulsa a partir de ferramentas/paginas/
│   └── index.html
├── lexico/                     # GERADO (não editar): léxico de Strong, uma página por palavra (~14.258 páginas)
│   └── {grego,hebraico}/<n>/index.html + índices e listas de 250 em 250
├── dicionario/                 # GERADO (não editar): Easton, uma página por verbete (/dicionario/alianca/) + letras
├── temas/                      # GERADO (não editar): Nave, uma página por tema (/temas/fe/) + letras
├── confissoes/                 # GERADO (não editar): credos antigos, Padrões de Westminster e Três Formas de Unidade
│
├── fontes/                     # Fontes .woff2 locais (Cardo, Cormorant Garamond, Inter) + LICENCA-OFL.txt
├── mapa/relevo/                # GERADO por ferramentas/gerar_relevo.py: azulejos do relevo sombreado do Atlas ({z}/{x}/{y}.png, ~15 MB)
├── vendor/
│   ├── leaflet/                # Leaflet auto-hospedado (Atlas)
│   └── supabase/               # Cliente Supabase JS carregado sob demanda (contas opcionais)
│
├── data/                       # Todo o acervo bíblico estático consumido via fetch('/data/...')
│   ├── books.json              # Cânon (66 livros, códigos USFM, nomes pt/en/es) e lista de traduções
│   ├── versoes.json            # GERADO por gerar_paginas.py: versão (hash) de cada grupo de dados, usada no ?v= dos endereços
│   ├── bibles/                 # {blivre,kjv,rva,orig,byz}/{USFM}.json (capítulos → versículos)
│   ├── interlinear/            # {USFM}/{cap}.json → palavras [original, translit, strong, glosa_pt]
│   ├── strongs/                # G.json (grego) e H.json (hebraico): def (EN), defpt (PT) e usopt (usos da KJV em PT)
│   ├── palavras/               # indice.json + {USFM}.json (palavras-chave e vocabulário na Bíblia Livre)
│   ├── commentaries/
│   │   ├── calvin/             # manifest.json, {USFM}/{cap}.json (EN) e pt/{USFM}/{cap}.json (PT)
│   │   └── henry/              # manifest.json, {USFM}/{cap}.json (EN) e pt/{USFM}/{cap}.json (PT)
│   ├── dictionary/             # Easton: index.json, A..Z.json (EN), titulos_pt.json e pt/A..Z.json
│   ├── topics/                 # Nave: index.json, A..Z.json (EN), aliases_pt.json, titulos_pt.json,
│   │                           #       pt/A..Z.json e doutrinas.json (GERADO dos 33 capítulos da Confissão)
│   ├── confissoes/             # citacoes/<LIVRO>.json (GERADO: onde as confissões citam cada versículo, sem a CFW) +
│   │                           #       credos, westminster, catecismo-maior, breve-catecismo, canones-de-dort, confissao-belga,
│   │                           #       heidelberg .json (inglês de
│   │                           #       domínio público + português + textos de prova em USFM)
│   ├── crossrefs/              # {USFM}/{cap}.json (referências cruzadas do openbible.info)
│   ├── places.json             # 1.335 lugares bíblicos: coordenadas, n (nome em EN), p (PT), e (ES), t (tipo) e c (certeza)
│   ├── journeys.json           # Rotas das viagens de Paulo para o Atlas (nome_en/nome_es, paradas_en/paradas_es)
│   ├── mapa/base.json          # GERADO por gerar_mapa_base.py: terra, litoral, lagos e rios (Natural Earth) do Atlas
│   ├── mapa/relevo.json        # GERADO por gerar_relevo.py: quais azulejos de relevo existem em cada zoom
│   ├── context.json            # Fichas de contexto dos 66 livros (autor, época, tema; en/es em c.en e c.es)
│   ├── prateleira.json         # GERADO por gerar_prateleira.py: catálogo de clássicos da prateleira do perfil
│   ├── plans.json              # 5 planos: 4 de leitura (o de M'Cheyne, 1842, vem de gerar_plano_mcheyne.py) e o Heidelberg em 52 Domingos (gerar_plano_heidelberg.py)
│   └── timeline.json           # Eventos da linha do tempo bíblica (nome_en/nome_es nas eras, t_en/t_es nos eventos)
│
├── ferramentas/                # Scripts offline de geração, revisão e validação (Python 3 stdlib)
│   ├── gerar_paginas.py        # Gera biblia/, lexico/, privacidade/, index.html, 404.html, sitemap.xml e hashes
│   ├── paginas_versiculos.py   # Chamado pelo gerar_paginas.py: uma página por versículo em biblia/<livro>/<cap>/<v>/
│   ├── paginas_lexico.py       # Chamado pelo gerar_paginas.py: as páginas do léxico em lexico/
│   ├── paginas_acervo.py       # Chamado pelo gerar_paginas.py: dicionario/, temas/ e data/{dictionary,topics}/enderecos.json
│   ├── validar_dados.py        # Valida integridade estrutural e textual de todo o acervo em data/
│   ├── paginas/privacidade.html# Conteúdo-fonte da política de privacidade (/privacidade/)
│   ├── CONTAS.md               # Passo a passo da sincronização opcional com Supabase
│   ├── supabase.sql            # Schema SQL (tabelas public.itens e perfis_publicos, RLS, RPCs apagar_conta, publicar_perfil e despublicar_perfil)
│   ├── gerar_interlinear_at.py # Gera interlinear do AT (STEPBible TAHOT na numeração da Bíblia Livre)
│   ├── corrigir_interlinear_nt.py # Alinha interlinear do NT (STEPBible TAGNT)
│   ├── stepbible.py            # Leitor/alinhador das fontes STEPBible (em ferramentas/fontes/, fora do git)
│   ├── corrigir_glosas.py      # Revisão gramatical e lexical em lote das glosas do interlinear
│   ├── glosas_revisao.py       # ~2.000 glosas mais frequentes revisadas + regras por gramática/pessoa
│   ├── conjugar.py             # Conjugação tu/vós, imperativos e correções morfológicas em PT
│   ├── nomes_pt.py             # Extrai nomes próprios na grafia da Bíblia Livre → nomes_pt.json
│   ├── glosas_pt.json          # Dicionário base inglês→português das glosas — NÃO SOBRESCREVER
│   ├── glosas_llm.json         # Correções de sentido das glosas revisadas por LLM ({"LIVRO|cap|v|i": {de, para}})
│   ├── glosas_manuais.json     # Correções de glosas feitas à mão, no mesmo formato (valem por cima das do LLM)
│   ├── nomes_pt.json           # Mapa Strong → nome próprio em português
│   ├── substantivos_pt.json    # Substantivos para remontagem de sufixos hebraicos
│   ├── gerar_palavras.py       # Gera data/palavras/ (notas das palavras-chave + aplica vocabulário)
│   ├── vocabulario.py          # Definições dos +700 termos difíceis/técnicos sublinhados
│   ├── notas_fontes.json       # GERADO por tradutor/notas_llm.py: notas e vocabulário conferidos com fontes abertas
│   ├── confissoes.py           # Importa os símbolos de fé (Creeds.json, domínio público) para data/confissoes/
│   ├── confissoes_ccel.py      # Confissão Belga e Heidelberg (inglês de Schaff na CCEL, domínio público) → data/confissoes/
│   ├── credos.py               # Credos antigos (texto inglês de referência + tradução do Sola) → data/confissoes/credos.json
│   ├── paginas_confissoes.py   # Chamado pelo gerar_paginas.py: confissoes/ e o índice versículo → citações
│   ├── gerar_doutrinas.py      # Gera data/topics/doutrinas.json dos 33 capítulos da Confissão de Westminster
│   ├── gerar_atlas_pt.py       # Preenche nomes em português (campo p) em data/places.json
│   ├── gerar_atlas_es.py       # Nomes em espanhol (campo e) a partir do português, por regras + MANUAL
│   ├── gerar_mapa_base.py      # Base do Atlas sem nomes modernos (Natural Earth recortado e simplificado) → data/mapa/base.json
│   ├── atlas_openbible.py      # Tipo e certeza de cada lugar (dados do openbible.info, CC BY) → campos t e c de places.json
│   ├── gerar_relevo.py         # Relevo sombreado do Atlas (elevação do Terrain Tiles, AWS Open Data) → mapa/relevo/ (~2 min)
│   ├── gerar_crossrefs.py      # Converte referências cruzadas do openbible.info
│   ├── gerar_prateleira.py     # Catálogo da prateleira do perfil (teologia, filosofia, literatura...; tradição, grupo e ligações com páginas do Sola)
│   ├── gerar_plano_mcheyne.py  # Plano de M'Cheyne (365 dias × 4 leituras, domínio público) → data/plans.json
│   ├── gerar_plano_heidelberg.py # Plano do Catecismo de Heidelberg em 52 Domingos (campo domingo de heidelberg.json) → data/plans.json
│   ├── baixar_henry.py         # Baixa comentário de Matthew Henry (domínio público)
│   ├── tradutor/               # Pipeline isolado de tradução offline (Argos / NLLB / Batch LLM)
│   │   ├── etapas.py           # Prepara entradas de data/ e aplica traduções em data/.../pt/
│   │   ├── calvino_llm.py      # Teste A/B (30 trechos difíceis) + Batch API p/ Calvino → pt-v2/
│   │   ├── strong_llm.py       # Amostra + Batch API p/ o léxico de Strong (defpt e usopt, com validação)
│   │   ├── acervo_llm.py       # Amostra + Batch API p/ Matthew Henry, Easton e Nave (usa preparar/aplicar do etapas.py)
│   │   ├── glosas_llm.py       # Amostra + Batch API p/ revisar as glosas do interlinear → glosas_llm.json
│   │   ├── titulos_llm.py      # Títulos em PT que faltam no Easton/Nave (só acrescenta nos titulos_pt.json)
│   │   ├── confissoes_llm.py   # Tradução própria dos símbolos de fé (marcadores de prova [n] preservados)
│   │   ├── notas_llm.py        # Confere palavras-chave e vocabulário com léxicos abertos, CFW e Calvino → notas_fontes.json
│   │   ├── nllb.py             # Motor NLLB-200 1.3B (protege refs USFM, numerais romanos e latim)
│   │   ├── tradutor.py         # Motor Argos Translate (moderniza inglês arcaico e fatia frases)
│   │   ├── lote.py             # Execução particionada (--parte K/N) com retomada segura
│   │   ├── revisar.py          # Retraduz trechos em que o modelo omitiu conteúdo
│   │   ├── teste_refs.py       # Testa amostras antes de rodar uma etapa inteira no Actions
│   │   ├── traduzir_tudo.sh    # Script local para etapas rápidas com Argos
│   │   └── entradas/           # Entradas auxiliares versionadas (verbos e amostra_calvino_ab.json)
│   └── video/                  # Geração automatizada do vídeo vertical (1080×1920, 30 fps)
│       ├── capturar.cjs        # Captura telas mobile do site com Playwright
│       ├── video.html          # Animação em linha do tempo única
│       ├── renderizar.cjs      # Renderiza quadro a quadro e monta MP4 com ffmpeg
│       └── narrado/            # Vídeos narrados para o Instagram (voz + cenas + legendas + música)
│           ├── alinhar.py      # Casa o roteiro com as pausas da voz → episodios/<ep>/tempos.json
│           ├── renderizar.cjs  # Motor: cenas no tempo da voz, legendas, aceleração e mixagem → saida/<ep>.mp4
│           ├── episodios/<ep>/ # roteiro.txt, tempos.json e cenas.cjs de cada vídeo (ex.: heidelberg-01)
│           └── entrada/        # voz.mp3 e musica.mp3 (de terceiros, FORA do git)
│
└── .github/workflows/
    ├── verificar.yml           # CI em push/PR: node --check, validar_dados.py e gerar_paginas.py
    └── traduzir.yml            # Execução manual (workflow_dispatch) da tradução em matriz NLLB/Argos
```

### Detalhes importantes da arquitetura

- **Roteamento SPA e SEO (`app.js` + `gerar_paginas.py`)**:
  - Três vistas (`est.vista`): início (`/`), livro (`/biblia/joao/`) e capítulo (`/biblia/joao/3/`, com `#v16` rolando direto ao versículo) via `history.pushState`. Links antigos `#/JHN/3` continuam funcionando e são convertidos automaticamente.
  - Toda referência bíblica é um `<a href>` real gerado por `linkRef`; um único ouvinte de clique em `iniciar()` intercepta e navega sem recarregar. Todos os `fetch` usam caminhos absolutos (`/data/...`).
  - `gerar_paginas.py` cria uma página HTML real para cada livro e capítulo em `biblia/` (com `<title>`, meta description, texto do capítulo e `BreadcrumbList` JSON-LD para buscadores), uma página leve por versículo em `biblia/<livro>/<cap>/<v>/` (`ferramentas/paginas_versiculos.py`: Bíblia Livre, KJV e RVA, o original palavra por palavra com link para o léxico, os primeiros 420 caracteres do comentário de Calvino/Henry, 3 referências cruzadas com texto e mais 9 em link, anterior/próximo e o botão para o capítulo no app; HTML compacto, ~6 KB cada, ~187 MB no total; os números de versículo das páginas de capítulo linkam para elas e o `rotaDe` do app abre `/biblia/joao/3/16/` no capítulo), as páginas do léxico de Strong em `lexico/` (`ferramentas/paginas_lexico.py`: uma por palavra em `/lexico/grego/26/` e `/lexico/hebraico/2617/`, com definição, usos da KJV, como o interlinear traduz, ocorrências por livro e versículos — os 25 primeiros com o texto da Bíblia Livre, depois só as referências; HTML avulso e leve com `lexico.css` próprio, para que mudar `app.js`/`style.css` não reescreva as ~14 mil páginas; o cartão do léxico e a busca Strong do app linkam para elas via `urlLexico()`), as páginas do dicionário de Easton e dos temas de Nave em `dicionario/` e `temas/` (`ferramentas/paginas_acervo.py`: uma por verbete, endereço pelo título em português de `titulos_pt.json` ou pelo nome em inglês; referências viram links como no `linkarRefs` e remissões "Veja X" viram links para o outro verbete; quando dois verbetes caem no mesmo endereço, o mais completo fica com o simples e os outros vão para `data/{dictionary,topics}/enderecos.json`, que o app usa em `htmlLinkAcervo()` — esses dois arquivos são gerados, não edite) e páginas de texto avulsas sem o app a partir de `ferramentas/paginas/*.html` (como `/privacidade/`, cujo link está cadastrado no Branding do login Google — atualize a data no topo de `ferramentas/paginas/privacidade.html` se mudar o que o site armazena).
- **Service Worker (`sw.js`)**:
  - Páginas HTML usam estratégia *rede primeiro*, caindo para a página inicial em cache quando sem internet (o `app.js` lê `location.pathname` e abre o capítulo certo).
  - Arquivos em `/data/` usam o cache `sola-dados-v1` e são pedidos com a versão no endereço (`/data/topics/doutrinas.json?v=899a0846`): `gerar_paginas.py` grava `data/versoes.json` (hash de cada grupo — a pasta do arquivo, ou o próprio arquivo nos dois primeiros níveis), o app o lê ao iniciar (`carregarVersoes`/`urlDados`) e o `sw.js` serve do cache só a mesma versão, trocando a velha pela nova; sem rede, qualquer versão guardada serve. Assim um arquivo de dados que mudou de formato nunca chega velho junto com o app novo (sem a versão, cai no antigo *stale-while-revalidate*). O botão *"Baixar a Bíblia"* no painel Sobre salva todos os capítulos da tradução atual nesse mesmo cache.
- **Navegação responsiva, bancada de leitura e painéis (`app.js`)**:
  - **Topo único (`.topo`), barra de comando (`#btnComando`, `/` ou `Ctrl+K`) e menu `#navMais` (`#menuMais`)**: no desktop (`>700px`), `.topo` opera em linha única (`54px`) e `ajustarNav()` esconde com `nav-fora` os últimos botões de `.navbar` que não cabem na largura disponível, exibindo o botão *"Mais"*. A prioridade segue a ordem no HTML (*Como usar* sai primeiro). Recalcula via `ResizeObserver` na própria barra, ao mudar de vista/idioma e após carregar fontes — nunca por evento `resize` da janela. Onde `.controles` fica oculto (`≤700px`), o menu *"Mais"* também exibe os seletores de idioma, tradução e comparação. Para adicionar um botão novo na barra, basta inseri-lo na posição de prioridade correta no HTML.
  - **Leitura estilo Bíblia de Genebra e Estante Exegética (`#colEstudo`, desktop `≥1060px`)**: em telas largas (`≥860px`, fora de comparação/leitura contínua), `renderizarCapitulo()` exibe até 2 referências cruzadas principais na margem esquerda de cada versículo (`.margem-refs`). Em `≥1060px` com `est.estudo` ativo (`bancadaAtiva()`), a estante lateral acompanha apenas cliques deliberados no versículo (sem saltar ao passar o mouse) e reúne 4 abas sincronizadas em `#abasEstante` (`atualizarEstudo`): *Léxico & Orig.* (`original`, incluindo notas de palavras sublinhadas abertas direto na estante sem cobrir o texto), *Comentário* (`comentario`), *CFW & Refs* (`referencias`, cruzando textos de prova de `doutrinas.json` com `crossrefs`, mais o cartão "Nos catecismos e confissões" com os Catecismos de Westminster, a Confissão Belga e os Cânones de Dort que citam o versículo — `citacoesDoVerso`, a partir de `data/confissoes/citacoes/<LIVRO>.json`, gerado pelo `paginas_confissoes.py`; também nas gavetas do celular) e *Nota* (`anotacao`). Em telas menores ou com a estante fechada, as ações abrem nas gavetas internas do versículo (`.gaveta`) e no balão `#cartaoPalavra`.
  - **Busca unificada (`#painelBusca`)**: quatro abas (`texto`, `strong`, `temas`, `dicionario`); digitar uma referência (`Jo 3:16`) navega direto (`parseRef`/`acharLivro` aceitam muitas grafias — `Sm 51`, `jo3.16`, `I Co 13`, `primeira coríntios 13`, `salmo 23 versículo 1`, nomes em pt/en/es, `APELIDOS_LIVRO` e erros de digitação por `distancia()`; Judas 3 e Filemom 4 viram versículos; o nome do livro sozinho não navega, mas `ligarDicaRef` mostra o botão "Ir para…" abaixo do campo enquanto se digita; no versículo de vida do perfil, faltando o versículo, aparecem os números para tocar) e digitar um código Strong (`G3056`, `H2617`) abre automaticamente a aba *Strong* (`buscarStrong()`), que pesquisa código, lema original (com ou sem massorá), transliteração e definição nas `14.197` entradas.
  - **Perfil personalizável** (nov/2026; `perfil()`, `salvarPerfil`, `htmlCartaoPerfil`, `htmlEditorPerfil`): nome de exibição, avatar (inicial ou ícone em uma das cores de `PERFIL_CORES`, ou foto do aparelho recortada e reduzida a 160 px em JPEG por `reduzirFoto`), capa (`PERFIL_CAPAS`, gradientes em CSS `.capa-*`), versículo de vida (`vers` = `"ROM.8.28"`, mostrado na Bíblia do idioma), bio, tamanho da letra (`--escala-texto` em `.verso > p`), confissão em destaque (`conf`: `westminster` ou `tres-formas`, que põe a Confissão Belga, o Heidelberg e Dort primeiro na estante) e as seções do painel (ordem e quais aparecem, `SECOES_PAINEL`). Fica em `logos_perfil` e sobe para a conta como item `estado|perfil` (validado por `perfilValido`). **Conquistas** (`conquistas()`): selos calculados dos dados que já existem (capítulos, livros inteiros, Pentateuco, Evangelhos, cartas de Paulo, AT, NT, Bíblia, sequências, planos, notas, marcações, prateleira). **Prateleira** (`htmlPrateleira`): livros de teologia, filosofia, apologética, vida cristã, literatura e biografias em lombadas coloridas pela tradição (o campo `g` de cada obra agrupa os filtros da busca do catálogo), em "Lendo", "Lidos" e "Quero ler"; catálogo de clássicos em `data/prateleira.json` (gerado por `ferramentas/gerar_prateleira.py`, que confere as ligações com páginas do Sola) e livros à mão (`u-<id>`); fica em `logos_prateleira` e sobe como `estado|livro:<id>`. O backup em arquivo (`v: 3`) leva perfil, prateleira e meta. **Imagem do perfil** (botão no canto da capa do cartão): `compartilharPerfil()` usa a mesma janela da imagem do versículo e `desenharPerfil()` desenha capa, avatar, nome, bio, versículo de vida, os números do estudo e as lombadas dos livros lidos/em leitura que couberem.
  - **Painel "Meu estudo"**: dividido em duas abas (`est.abaEstudo`): *Estudo* (o cartão do perfil no topo e as seções na ordem escolhida; a semana em barras de domingo a sábado com a meta semanal de capítulos em `logos_meta_semana`, sincronizada como `estado|meta` — `htmlSemana`; as últimas 12 semanas em quadradinhos — `htmlHistorico`; as leituras recentes — `htmlRecentes`; tudo a partir das datas de `logos_lidos`; progresso por livro, dias seguidos, marcações) e *Perfil* (conta, preferências, backup, privacidade, excluir conta), acessível também pelo botão `#btnPerfil` no topo.
  - **Imagem do versículo** (ação *Compartilhar* do versículo e da estante): `compartilharVerso()` abre, por `abrirImagem({titulo, desenhar, texto})` (a mesma janela da imagem do perfil), uma prévia e escolhe formato (*Feed* 1080×1350 ou *Stories* 1080×1920, com o conteúdo fora das faixas que o Instagram cobre) e tema (claro: papel linho e carmim; escuro: Vigília), lembrados em `logos_img_formato`/`logos_img_tema`; `desenharVerso()` desenha no canvas (fundo, molduras e faixa do endereço em `molduraImagem`, comum às duas imagens; números em Inter, porque o "1" da Cormorant parece "I") com as fontes do site (a fonte diminui até caber; aspas decorativas só se houver espaço) e a janela compartilha (Web Share com arquivo, no celular), baixa ou copia a imagem.
  - **Catecismo no dia a dia** (nov/2026): a página inicial tem 4 cartões em 2 × 2 (versículo, palavra, capítulo da Confissão e a **pergunta do dia** do Breve Catecismo, que percorre as 107 perguntas pela mesma conta de dias do versículo do dia e leva a `/confissoes/breve-catecismo/<n>/`). Um plano com `doc` em `data/plans.json` é de catecismo: cada dia é uma lista de números de perguntas do documento em `data/confissoes/` (o Heidelberg em 52 Domingos), e `montarPlanos` mostra "Domingo N" com as perguntas e respostas num `<details>`; o progresso e as conquistas contam como nos outros planos, e o `validar_dados.py` confere que os números cobrem o catecismo inteiro. O Breve Catecismo e o Heidelberg não têm textos de prova nos dados (a fonte não os trazia).
  - **Painel "Como usar" (`#painelAjuda`)**: montado por `montarAjuda()` a partir do objeto `AJUDA` (`pt`/`en`/`es`: grupos → `[ação, ícone, título, texto]`), com botões *"Experimentar"* ligados a `ACOES_AJUDA[ação]`. Ao criar funcionalidade nova no site, adicione-a em `AJUDA` nos três idiomas e registre a ação correspondente.
- **Página pública do perfil (`/perfil/<apelido>/`, nov/2026)**: opcional e só com conta (aba Perfil → *Página pública*, `htmlPaginaPublica`/`ligarPaginaPublica`). A pessoa escolhe o apelido (`problemaApelido`: 3 a 30 letras minúsculas, números e hífens, fora `APELIDO_RESERVADOS`, `APELIDO_PROIBIDOS`, `APELIDO_RAIZES` e `APELIDO_SEMPRE` — as mesmas listas de `apelido_permitido()` no `ferramentas/supabase.sql`, e o `validar_dados.py` reprova se divergirem) e o que mostrar além do cartão (`perfil().pub`: `num`, `selos`, `prat`; `conta` = id de quem publicou, para não publicar o perfil de outra conta no mesmo aparelho). `dadosPublicos()` monta o retrato (nunca anotações, marcações, planos nem datas) e `publicarPerfil()` o grava pela RPC `publicar_perfil` (security definer; erros `apelido_em_uso`/`apelido_invalido`); `agendarPublicacao()` o refaz depois de cada sincronização, só quando mudou (`logos_pub_enviado`). O GitHub Pages serve o `404.html` (o próprio app, com `noindex`) nesse endereço; `rotaDe` devolve `{vista:"perfil", apelido}` e `renderizarPerfilPublico()` lê `perfis_publicos` por `fetch` com a chave pública (`lerPerfilPublico`, sem carregar o cliente do Supabase), passa tudo por `perfilValido` e mostra cartão, números, conquistas, prateleira e o convite para conhecer o Sola. Tirar do ar: RPC `despublicar_perfil`; excluir a conta apaga a linha (cascade). Ninguém grava direto na tabela e o visitante não vê o `user_id` (só `apelido`, `dados`, `atualizado_em`). Moderação: apagar a linha no Table Editor do Supabase.
- **Contas opcionais (`CONTA` em `app.js` + `ferramentas/CONTAS.md`)**:
  - Sem conta, tudo funciona via `localStorage` (`logos_lidos`, `logos_ultimo`, notas, marcas, planos).
  - Se `CONTA.url` estiver vazio ou `google` e `email` estiverem `false`, toda a interface de conta desaparece.
  - A sincronização (`sincronizar()`) é *local-first*: `tocar(tipo, chave)` registra pendências em `est.sinc.pend`, e conflitos no mesmo item são resolvidos pelo maior `ts` (`apagar` também grava timestamp). O mapa `DADOS` descreve cada categoria (`nota`, `marca`, `plano`, `lido`, `estado`).
  - Referências no texto dos comentários ("Romanos 8:28", "1 Cor. 13:4", "Sl 23:1"; "Jó" com acento é Jó, sem é João)
    viram link em `linkarRefsTexto` — só com capítulo E versículo, e só se o nome for de livro (`livroPorNome`). Todo
    link `.ref-pv` (comentários, temas, dicionário) abre a prévia flutuante do versículo (`abrirPrevia`): mouse no
    computador; no toque, o 1º toque mostra e o 2º (ou "Abrir") navega. O ouvinte fica na captura da janela, antes do
    que navega pelos links internos.
  - Cabeçalho da Estante: clicar na referência volta ao versículo; `#estudoAlvo` mostra a palavra aberta no léxico;
    `#estudoVolta` aparece quando o versículo sai da tela; `#estudoSegue` ("Acompanhar a leitura", `logos_estudo_segue`)
    faz a Estante seguir o versículo a 1/3 da altura da tela (`verificarEstante`, no scroll).
  - Busca universal (aba Texto): enquanto digita (`buscar(true)`, 320 ms), mostra acima dos versículos os grupos Temas e
    doutrinas, Dicionário e No original (`gruposBusca`, com `itensTemas`/`itensDic`, as mesmas das abas). Ao digitar, o
    léxico inteiro não é carregado: só o código Strong digitado e as palavras-chave do `indice.json`.
  - O convite discreto para criar conta (`convidar(motivo)` / `mostrarConvite`) aparece no máximo uma vez por visita após interações reais e respeita adiamentos progressivos de 3, 7, 30 e 90 dias (`logos_convite`).
- **Acervo em `data/` e scripts geradores**:
  - **Interlinear (`data/interlinear/`)**: sempre na numeração de versículos da Bíblia Livre (que difere do hebraico massorético em ~2.300 versículos e do grego em ~50; `gerar_interlinear_at.py` e `corrigir_interlinear_nt.py` fazem o alinhamento usando os dados da STEPBible em `ferramentas/fontes/`). No AT, o Strong é o da raiz; partículas feitas só de prefixo/sufixo ficam sem Strong. As glosas passam por `corrigir_glosas.py` (`preparar` / `aplicar`), auxiliado por `stepbible.py`, `nomes_pt.py` (`Yahweh` → `SENHOR`), `glosas_revisao.py` (`REVISAO`), `substantivos_pt.json` (sufixos pronominais hebraicos em 3ª pessoa `dele/dela/deles/delas`), concordância de artigos gregos pelo gênero léxico extraído da Bíblia Livre e `conjugar.py` (`você` → `tu/vós` conjugado). Por último entram as correções de sentido revisadas por LLM em `ferramentas/glosas_llm.json` (`tradutor/glosas_llm.py`): só trocam a glosa que ainda é igual à que o modelo viu (`de`), e a palavra já corrigida fica fora das regras. Por cima delas valem as correções à mão de `ferramentas/glosas_manuais.json`, no mesmo formato (`de` = a glosa que as regras deixaram; ficam à parte porque o `glosas_llm.py aplicar` regrava o `glosas_llm.json`). O comando `aplicar` é idempotente (depois de mexer no `glosas_llm.json`, rode até `--conferir` dar 0 capítulos, porque os artigos gregos vizinhos se ajustam na rodada seguinte).
  - **Palavras sublinhadas (`data/palavras/`)**: exclusivas da Bíblia Livre (ocultas na leitura contínua e nas outras traduções; controladas por `logos_chave` e `logos_voc`), geradas por `ferramentas/gerar_palavras.py` (~75 s):
    - *Palavras-chave* (traço dourado cheio): definidas no próprio `gerar_palavras.py` via `lema(strong, tradução, formas, nota)` (primeira ocorrência no capítulo) e `contexto("PSA.51.10", "H1254", nota)` (recusa se o Strong não existir no versículo).
    - *Vocabulário* (traço pontilhado): definido em `ferramentas/vocabulario.py` via `t(palavra, formas, significado, nota, s=(strongs), exige)`. `exige=True` restringe o sublinhado aos versículos que contêm aquele Strong (evita falsos positivos de homônimos como *"funda"* arma × *"cova funda"*). Máximo de 5 marcas por versículo (até 3 de vocabulário), sem sobrepor palavras-chave. Use `--relatorio` para auditar cobertura e confirmação de Strong.
    - *Fontes das notas*: `gerar_palavras.py` sobrepõe aos textos escritos à mão o `ferramentas/notas_fontes.json` (gerado por `tradutor/notas_llm.py`, não edite à mão), em que cada nota e definição foi reescrita só com o que as fontes abertas dão — léxico grego Abbott-Smith da STEPBible (TBESG, CC BY), glosa da STEPBible (TBESH, CC BY) + Strong no hebraico (as definições do BDB resumido da TBESH exigem permissão da Online Bible e NÃO são usadas), parágrafos da Confissão de Westminster e do Catecismo Maior com textos de prova onde o Strong aparece, o comentário de Calvino/Henry no versículo e os versículos citados — e guarda a lista `f` das fontes, que o cartão mostra em "Fontes: …" no lugar do aviso de texto do Sola. Sem o arquivo, a saída volta a ser a dos textos à mão. Comandos: `preparar|amostra|conferir|aplicar [--modelo M] [--so lema,contexto|termo]`; o `conferir` retoma de onde parou em `trabalho/notas_llm_saida.json`, e o `aplicar` passa antes pela leitura humana versionada em `tradutor/entradas/notas_revisao.json` (`reverter`: itens que ficam com o texto à mão, sem fontes; `editar`: correções sobre a resposta do modelo). Rodada de nov/2026: notas das palavras-chave no `claude-sonnet-5-5` (151 itens, ~US$ 0,70) e vocabulário no `claude-haiku-5-5` (701 itens, ~US$ 0,10); o Haiku tirava medidas (cm, litros, gramas) e as formas derivadas que o sublinhado usa, por isso 72 termos voltaram ao texto à mão. Ao refazer, só aceite resposta que não perca números, formas entre aspas e referências do texto à mão.
  - **Comentários (`data/commentaries/`)**: Calvino cobre 47 livros; nos livros restantes entra Matthew Henry (`18` livros, baixado por `baixar_henry.py`; Cantares e 2Sm 23–24 não existem na fonte). Quando o idioma da interface é Português, o app sobrepõe `pt/{USFM}/{cap}.json` ao original inglês e resolve comentários em bloco buscando o versículo anterior ou o primeiro do capítulo.
  - **Dicionário, Temas e Doutrinas (`data/dictionary/`, `data/topics/`)**: em Easton/Nave traduzidos, as referências ficam no padrão USFM (`GEN 3:15; 4:1`) convertidas por `refs_usfm` (`etapas.py`) e transformadas em links clicáveis por `linkarRefs` (`app.js`). Já `data/topics/doutrinas.json` é gerado por `python3 ferramentas/gerar_doutrinas.py` a partir dos 33 capítulos da Confissão de Westminster em `data/confissoes/westminster.json` (cada parágrafo com as provas `[l, c, a, b]`, `b = 999` = até o fim do capítulo; em inglês o app mostra o original de 1647). As 50 "doutrinas" escritas por IA (`doutrinas.py`) foram retiradas em nov/2026 porque o mantenedor não as podia revisar.
  - **Símbolos de fé (`data/confissoes/`)**: importados por `ferramentas/confissoes.py` do repositório `NonlinearFruit/Creeds.json` (estrutura sob Unlicense; só textos marcados como domínio público — o Heidelberg e a Confissão Belga de lá estão em traduções inglesas modernas, com direitos, e NÃO foram importados de lá). Traduzidos por `tradutor/confissoes_llm.py` (`claude-opus-5-5`, ~US$ 3, nov/2026): tradução própria, sem reproduzir traduções portuguesas publicadas (que têm direitos), com os marcadores `[n]` validados. `paginas_confissoes.py` gera `/confissoes/<doc>/<n>/` e o índice inverso que as páginas de versículo usam ("Nas confissões de fé"). A **Confissão Belga** e o **Catecismo de Heidelberg** vêm de `ferramentas/confissoes_ccel.py`, que lê o `creeds3.xml` de Philip Schaff, *The Creeds of Christendom*, vol. 3 (1877), na CCEL (baixado para `ferramentas/fontes/ccel/`; o host `ccel.org` precisa estar liberado na rede do ambiente): o inglês do tricentenário (1863) no Heidelberg, com a divisão nos 52 Domingos, e o inglês da Reformed (Dutch) Church in America na Belga, com os textos de prova tirados das notas da coluna francesa (os capítulos em romano são lidos do texto, porque a CCEL erra alguns; os versículos dos Salmos são passados da numeração hebraica para a da Bíblia Livre com `TITULO_SALMO`; `CORRECOES` e `ERRATA` consertam erros de impressão e de digitalização). A tradução foi feita na própria sessão do agente, sem API, em nov/2026, e o importador a preserva quando roda de novo. Os **credos antigos** (`/confissoes/credos/<apostolico|niceno|atanasio|calcedonia>/`) vêm de `ferramentas/credos.py`, que guarda o texto inglês de referência em domínio público (Livro de Oração Comum de 1662 no Apostólico e no Atanásio, Schaff 1877 em Calcedônia — as versões do Creeds.json para esses dois têm direitos) e a tradução do Sola feita na própria sessão (sem API), com notas que só remetem aos Padrões de Westminster; a busca de Temas do app os lista (`CREDOS_ANTIGOS`).
- **Funcionamento e qualidade do pipeline `ferramentas/tradutor/`**:
  - `nllb.py` protege marcadores de estrutura (`I.`, `1.`, `(2.)`), preserva `"milhas"` (evitando conversão indevida para `"quilômetros"`) e mascara referências USFM (`GEN 3:15`) durante a inferência para que abreviações como `JOS` não virem `"JOSÉ"`.
  - Antes de disparar uma etapa grande no workflow `.github/workflows/traduzir.yml`, é possível rodar com `amostra = N` (executa `teste_refs.py` no log sem gravar nada). Se uma execução atingir o tempo limite de 6h do GitHub — ou se o robô não conseguir criar a branch `traducao-<etapa>` porque o arquivo do workflow mudou após o commit inicial — basta disparar novamente passando `retomar = <run_id>` (reaproveita tudo o que já foi traduzido).
  - A etapa `glosas` do workflow usa o Argos em 1 máquina (poucos minutos): equivale ao `traduzir_tudo.sh glosas` sem exigir ambiente Linux local no computador do mantenedor (Windows 11). Para glosas do interlinear, `GLOSAS_FIXAS` em `etapas.py` tem prioridade sobre `ferramentas/glosas_pt.json`; `python3 etapas.py aplicar glosas` reaplica ambos.
  - **Qualidade e limitações conhecidas dos modelos**: boa no Strong e nos títulos; legível, mas ainda com tropeços em prosa densa como Calvino e Easton — por isso o site sempre exibe o aviso transparente de *"Tradução automática"*. Os modelos tendem a omitir texto em listas longas e desconhecem inglês arcaico; o pipeline já moderniza termos arcaicos (`"thou"`, `"ass"` etc.) e fatia/retrabalha frases que saem curtas demais (`revisar.py` refaz trechos com omissão).
- **Vídeo de apresentação (`ferramentas/video/`)**:
  - Gera vídeo vertical (`1080×1920`, 30 qps, ~33 s) sem editor externo: `capturar.cjs` fotografa o site mobile em `SITE=http://localhost:8000`, `video.html` anima numa linha do tempo única (`trilha(...)`) e `renderizar.cjs` junta quadro a quadro com `ffmpeg` em `saida/sola-apresentacao.mp4` (`--fotos 2,13.5` confere instantes). Usa João 1:14 e Salmo 23:1 no interlinear (evitando João 3:16 por glosas imperfeitas).
  - **Vídeos narrados (`ferramentas/video/narrado/`, nov/2026)** — a receita aprovada pelo mantenedor para os Reels: (1) escrever `episodios/<ep>/roteiro.txt` (um bloco por cena, separados por linha em branco; `{mostrado|falado}` para números e endereços, ex. `{1563|mil quinhentos e sessenta e três}`, `{solabiblia.com.br|sola bíblia ponto com ponto bê erre}`); (2) `python3 ferramentas/video/narrado/alinhar.py <ep> --texto` dá o texto para colar no **ElevenLabs** (voz *"Carlos – Resonant, Majestic Storyteller"*, modelo *Multilingual v2*, plano gratuito; créditos renovam por mês), e o mp3 vai para `entrada/<ep>/voz.mp3`; (3) a música de fundo é um piano calmo do **Pixabay Music** (licença livre, sem atribuição obrigatória) em `entrada/musica.mp3` — música sintetizada no próprio script ficou ruim e foi descartada; (4) `alinhar.py <ep>` acha as pausas (ffmpeg `silencedetect`) e grava `tempos.json` com blocos, frases e legendas (confira a tabela; dá para ajustar à mão); (5) `episodios/<ep>/cenas.cjs` monta as cenas a partir desses tempos (veja o `heidelberg-01`, Domingo 1 do Heidelberg); (6) com `python3 -m http.server 8000` rodando, `node ferramentas/video/narrado/renderizar.cjs <ep> --previa 2,11,30` tira fotos de instantes e sem `--previa` gera `ferramentas/video/saida/<ep>.mp4` (~2 min). O motor acelera tudo **12%** (`--vel 1.12`: vídeo por `setpts`, voz por `atempo`, sem mudar o tom — no ritmo original ficava lento), põe a música ~12 dB abaixo da voz e a abaixa ainda mais sob a fala (`sidechaincompress`), com entrada e saída suaves. O cartão final (`cartaoFinal`) traz o endereço, "Gratuito e sem anúncios", *Sola Scriptura*, `@projetosolabiblia` e o crédito "Voz: ElevenLabs". Os áudios são de terceiros: nunca entram no repositório.

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
- Em clones rasos, antes de enviar branch, rode `git fetch origin main` e faça rebase se necessário. Confira sempre com `git status` se todos os arquivos novos ou regenerados entraram no repositório. Ao orientar testes manuais após o merge na `main`, lembre que o GitHub Pages leva ~2 minutos para publicar e pode exigir `Ctrl+Shift+R` no navegador.

---

## 6. Convenções de código, interface, CSS e licenças

- **Idioma do código e da UI**:
  - Nomes de variáveis, funções, classes CSS, scripts e comentários devem ser escritos em **português**.
  - Textos visíveis na interface ficam centralizados nos objetos `UI`, `NAV` e `AJUDA` (`pt`, `en`, `es`) em `app.js`.
- **Cuidados essenciais de layout, CSS e mobile (não regredir)**:
  - **Cabeçalho no celular (`≤560px`) e no desktop (`>700px`)**: em `≤560px`, a palavra `"Sola"` é ocultada para que o ícone da marca caiba junto a nomes longos de livros sem quebrar linha (sempre teste o topo mobile abrindo **`1 Tessalonicenses 5`**); em `≤700px`, `.topo` divide-se em duas faixas compactas (identidade/ações em cima e `.navbar` embaixo), enquanto acima de `700px` permanece sempre em linha única (`3.4rem`) apoiado pelo botão `#navMais`.
  - **Toque e foco no celular**: a barra de ações do versículo fica no fluxo do documento em `≤560px` (entre o texto e a gaveta; flutuando ela cobria o botão *Salvar*). Qualquer mudança de foco ou versículo ativo no meio do toque desloca o texto e faz o clique errar o alvo — por isso palavras sublinhadas usam `mousedown` com `preventDefault` e ignoram `mouseenter` vindo de toque. **Nunca use o evento `resize` da janela para fechar menus/painéis**, pois no celular ele dispara ao rolar a página.
  - **Regras globais obrigatórias em `style.css`**:
    - `font-variant-numeric: lining-nums` no `body` (sem isso, o algarismo `"1"` da fonte Cormorant Garamond parece `"I"`).
    - `button, input, select, textarea { color: inherit }` (botões não herdam cor por padrão nos navegadores).
    - `.verso > p` estiliza apenas o texto bíblico do versículo (com `display: flow-root` para que a capitular `.capitular` do v. 1 nunca invada o v. 2 em versículos curtos); o conteúdo das gavetas tem estilo próprio.
    - Texto em português ao lado de hebraico (RTL) exige `unicode-bidi: isolate`, senão a pontuação se embaralha.
    - As cores do tema escuro valem só em `:root[data-tema="escuro"]`: nunca use o atributo `data-tema` em outro elemento (um botão com `data-tema="escuro"` herdaria as cores escuras e ficaria esmaecido no tema claro) — para opções de tema use outro nome, como `data-img-tema`.
- **Downloads e geração de dados**:
  - Gere nomes de arquivos de download **sem acentos** (o Chrome descarta nomes acentuados em downloads gerados no cliente).
  - Arquivos grandes de dados devem ser gerados/atualizados por script e verificados com `validar_dados.py`, nunca editados manualmente em massa.
- **Créditos e licenças (manter sempre visíveis no painel "Fontes e licenças")**:
  - Textos bíblicos: `scrollmapper/bible_databases` (domínio público).
  - Interlinear e morfologia: STEPBible / Tyndale House, Cambridge (**CC BY**).
  - Léxico de Strong, Calvino, Matthew Henry, Easton e Nave: domínio público.
  - Referências cruzadas e lugares do Atlas: `openbible.info` (**CC-BY**).
  - Traduções automáticas: Claude (Anthropic) em Calvino, Henry, Strong, Easton, Nave e revisão das glosas; Argos Translate e NLLB-200 da Meta na base das glosas (**CC BY-NC** — exige manutenção do caráter não comercial do site).
  - Fontes tipográficas: Cardo, Cormorant Garamond e Inter (**SIL Open Font License**). Mapa: Leaflet (**BSD**) + Natural Earth (domínio público) + relevo do Terrain Tiles (AWS Open Data: SRTM, GMTED, ETOPO1, EU-DEM/Copernicus).

---

## 7. Estado atual e pendências conhecidas

- **Contato e indexação**: o link "Contato" do rodapé é o e-mail do projeto (`projetosolabiblia@gmail.com`, nov/2026) e o Instagram oficial é **@projetosolabiblia** (`https://www.instagram.com/projetosolabiblia/`, na coluna Comunidade do rodapé; YouTube e "Apoiar o projeto" ainda aparecem como "em breve"). Para mudar, edite o rodapé do `index.html` (fora do bloco `<!--CONTEUDO-->`) e rode o `gerar_paginas.py`. No Google Search Console, a propriedade do tipo prefixo do URL (`https://solabiblia.com.br/`) foi verificada em 19/nov/2026 pelo arquivo HTML `google04e0bb96435230dc.html` na raiz — **nunca apague nem renomeie esse arquivo** (o Google confere de tempos em tempos; a tentativa de verificar a propriedade de domínio por registro TXT no Registro.br não encontrou o token). No mesmo dia o `sitemap.xml` (índice de `sitemap-{biblia,lexico,acervo}.xml`, ~56 mil endereços) foi enviado em *Sitemaps*; a indexação é gradual (semanas a meses).
- **Traduções automáticas e opção via Batch API (`calvino_llm.py`)**: Calvino foi retraduzido via LLM em nov/2026 (`claude-haiku-5-5` em Batch + `claude-sonnet-5-5` nos trechos sinalizados pelas checagens automáticas; PRs #20 e #21) e substituiu a versão NLLB em `pt/`. Matthew Henry, Dicionário de Easton e Nave (Temas) foram retraduzidos em nov/2026 por `ferramentas/tradutor/acervo_llm.py` (`claude-haiku-5-5` em Batch; as partes do Henry e do Easton recusadas pela validação foram refeitas com o `claude-sonnet-5-5`); os 3 blocos do Henry (2SA 6:12, ACT 9:36, ACT 21:1) e as 59 linhas do Nave que a validação recusou foram traduzidos na própria sessão do agente (sem API) em nov/2026 — as do Nave entraram em `trabalho/temas_llm_saida.json` e passaram pelo `acervo_llm.py aplicar temas`, que também refez as remissões "Veja X" com os títulos em português atuais. Os títulos que faltavam (2.214 do Easton e 2.978 do Nave, quase todos nomes próprios na grafia inglesa) foram traduzidos em nov/2026 por `ferramentas/tradutor/titulos_llm.py` (`claude-sonnet-5-5`, ~US$ 2,20; cada título vai com o começo do verbete, e o script confere os nomes no texto da Bíblia Livre — 3.724 confirmados) e acrescentados aos `titulos_pt.json` sem trocar os existentes; agora todo verbete tem título em português. Comandos do `acervo_llm.py`: `amostra|preparar|enviar|status|baixar|reenviar|revalidar|aplicar <henry|dicionario|temas>`; a entrada vem de `etapas.py preparar` e a saída vai para `etapas.py aplicar`, então as regras de cada etapa continuam valendo (referências USFM no Easton, códigos de livro do Henry convertidos para abreviações em português antes do envio, subtítulos do Nave agrupados por verbete). Para retraduzir Calvino com qualidade superior via LLM sem tocar em `pt/` nem nos originais em inglês, `ferramentas/tradutor/calvino_llm.py` roda primeiro um teste A/B em `30` trechos difíceis (`entradas/amostra_calvino_ab.json` → `trabalho/relatorio_ab_calvino.html`) e, se aprovado, envia os `10.349` textos únicos deduplicados na Batch API da Anthropic ou OpenAI (~US$ 3,80 no `claude-haiku-5-5`, ~US$ 75 no `claude-sonnet-5-5` ou ~US$ 3 no `gpt-6-luna`; ou modo `direto` a preço cheio no `gemini-3.5-flash`), gravando exclusivamente em `data/commentaries/calvin/pt-v2/` e proibindo substituição de citações bíblicas pela ARA (direitos da SBB).
- **Palavras-chave e vocabulário conferidos com fontes abertas** (nov/2026, `tradutor/notas_llm.py`): as `68` notas de lema e `83` notas de contexto foram reescritas só com o que dizem o léxico (Abbott-Smith/Strong), a Confissão de Westminster e o Catecismo Maior, Calvino/Henry e os versículos; `629` dos `701` termos do vocabulário foram conferidos do mesmo modo, quase todos confirmados sem mudança ou com pequenos ajustes (os outros `72` ficaram com o texto à mão, sobretudo medidas, pesos e formas derivadas). O cartão mostra as fontes de cada nota em "Fontes: …"; o que ainda é texto do Sola continua com o aviso de sempre. As palavras-chave sem nota (`56` dos `124` lemas) mostram só o léxico.
- **Léxico de Strong (`strong_llm.py`)**: `defpt` retraduzido em nov/2026 com o `claude-haiku-5-5` pela Batch API (~US$ 0,50; a amostra de 40 entradas difíceis saiu praticamente igual à do Sonnet 5.5), mais o campo novo `usopt` (lista de usos da KJV em português, mostrada em "Como a KJV traduz" no cartão do léxico). O script valida cada resposta (números G/H e palavras gregas/hebraicas preservados, sem inglês, tamanho razoável); as 3 entradas recusadas (G5352, G4577, G1744) foram traduzidas à mão na sessão do agente em nov/2026. Para refazer: `amostra`, `preparar`, `enviar`, `status`, `baixar`, `reenviar`, `aplicar` (idempotente).
- **Refinamentos residuais nos dados**:
  - *Glosas do interlinear*: depois das duas rodadas em `corrigir_glosas.py`, `glosas_llm.py` (nov/2026, `claude-haiku-5-5` em Batch, ~US$ 1,60) revisou os 31.103 versículos com Strong, gramática, glosa inglesa e texto da Bíblia Livre e gerou `38.779` correções aceitas (a validação recusa as que só apagam palavras, inventam negação, mexem nas marcações `[ ]`/`< >` ou reescrevem o versículo inteiro). Numa auditoria por amostragem, ~9 em 10 corrigiam erros reais; o restante é discutível — para corrigir uma correção ruim, adicione a glosa certa em `REVISAO` ou troque o `para` dela em `glosas_llm.json` (apagar a chave não restaura a glosa antiga, que precisa vir do histórico do git). Antes disso restavam poucos casos raros de sentido do Argos, ~150 ocorrências de `"você"` com verbos fora da tabela (as 66 que sobraram depois do LLM foram corrigidas à mão em nov/2026 em `glosas_manuais.json`: tu/vós, com o subjuntivo depois de "não" nos jussivos hebraicos), ~8% de substantivos hebraicos com sufixo fora de `substantivos_pt.json` e `327` nomes próprios raros (`nomes_pt.py --relatorio`). Para corrigir glosas pontuais, adicione em `REVISAO` (`glosas_revisao.py`) e rode `aplicar`.
  - *Mapa do Atlas* (nov/2026): os *tiles* do OpenStreetMap (que escreviam os nomes em árabe e hebraico) deram lugar a uma base própria — `ferramentas/gerar_mapa_base.py` recorta e simplifica o Natural Earth (níveis `geral` 1:50m, da Espanha à Índia, e `detalhe` 1:10m, do Mediterrâneo à Mesopotâmia, ~670 KB) e o app a desenha em canvas com as cores do tema (`--mapa-mar/-terra/-costa/-rio` no `style.css`; `montarBaseMapa`, `trocarNivelMapa`, `colorirMapa`). Os únicos nomes são os bíblicos em português: `atualizarRotulos()` mostra os mais citados que cabem sem se encostar, mais os mares fixos de `MARES_MAPA`, e ignora direções genéricas do geocódigo (`NOMES_GENERICOS`); clicar no nome abre a ficha do lugar. Por cima da base vai o **relevo sombreado** (`mapa/relevo/{z}/{x}/{y}.png`, gerado por `ferramentas/gerar_relevo.py` só com Python padrão a partir da elevação aberta do Terrain Tiles no AWS Open Data — SRTM/GMTED/ETOPO1/EU-DEM): luz do noroeste, sombra em preto translúcido e luz em branco translúcido, mar e terra plana transparentes, então serve aos dois temas (`--mapa-relevo` regula a opacidade); zooms 3–5 da Espanha à Índia, 6–7 do Mediterrâneo à Mesopotâmia e 8 na Terra Santa (`data/mapa/relevo.json` lista os azulejos que existem; `montarRelevo`/`trocarRelevo`); o vale do Jordão, abaixo do nível do mar, é tratado como terra (`DEPRESSOES`). O estilo segue o tipo do lugar (`t`, de `ferramentas/atlas_openbible.py`, a partir do Bible Geocoding Data do openbible.info, CC BY): cidades com ponto, regiões em versalete espaçado, montes com ▲, águas em azul itálico; portas, salas e altares (`outro`) e as localizações incertas (`c` < 300, inclusive as que são só uma área de 50 km ou mais) ficam fora do mapa, continuam na busca e a ficha avisa "Localização incerta".
  - *Atlas e idiomas*: os `1.335` lugares têm nome em português (os 95 que o `gerar_atlas_pt.py` não achava estão no `MANUAL` dele, na grafia da Bíblia Livre ou na forma usual em português); o Atlas, a linha do tempo e as fichas de contexto seguem o idioma da interface (nov/2026): em inglês o nome do lugar é o do openbible.info (`n`) e em espanhol o campo `e`, gerado por `ferramentas/gerar_atlas_es.py` a partir do português (regras de grafia + `MANUAL` com a forma usual dos nomes mais citados, como Galaad, Egipto, Neguev — não há Bíblia espanhola moderna em domínio público alinhada para tirar os nomes do texto); os textos da linha do tempo, das fichas e das viagens têm os campos `_en`/`_es` (ou `en`/`es` nas fichas) escritos à mão, e as datas são convertidas por `dataLocal()` no app (a.C./d.C. → BC/AD em inglês).
- **Contas Supabase e ambiente de nuvem do Claude Code**: contas ativas (`google: true`) contra o projeto `rxmxxuyqvetbkjfilayc` (login real e RLS testados pelo mantenedor no navegador; em ambiente de agente usa-se servidor falso nos testes, e mudar `google: false` em `CONTA` esconde tudo se algo quebrar). No **Claude Code**, o ambiente de nuvem **`"logos-biblia"`** libera rede para `rxmxxuyqvetbkjfilayc.supabase.co` e `solabiblia.com.br` (sessões iniciadas nele conseguem conferir o projeto Supabase e o site publicado; no ambiente *Default*, não).
- **GitHub Pages**: enquanto a publicação continuar saindo direto da branch `main` (e não via GitHub Actions em *Settings → Pages*), as pastas `biblia/` (incluindo as páginas de versículo), `lexico/`, `dicionario/`, `temas/` e `confissoes/` permanecem versionadas no repositório e verificada pelo `verificar.yml`.
