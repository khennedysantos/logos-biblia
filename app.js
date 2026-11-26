/* Sola — Estudo Bíblico. SPA em JS puro, sem dependências. */
"use strict";

/* ---------- textos da interface ---------- */
const UI = {
  pt: { idioma:"Idioma", traducao:"Tradução", comparar:"Comparar com…", semComparar:"Sem comparação",
    livros:"Livros", buscar:"Buscar", notas:"Minhas anotações", marcar:"Marcar",
    cores:{ouro:"ouro", verde:"verde", azul:"azul", rosa:"rosa"},
    original:"Original", comentario:"Comentário", anotacao:"Anotação", copiar:"Copiar", copiado:"Copiado!",
    grego:"Grego — Textus Receptus", hebraico:"Hebraico — Códice de Leningrado",
    sugerir:"Sugerir correção", lexDef:"Definição (Strong)", lexKjv:"Como a KJV traduz", lexPagina:"Página completa, com todos os versículos", lexFonte:"Léxico de Strong (1890), definições em tradução automática (Claude) · Texto marcado: STEPBible/Tyndale House (CC BY)",
    referencias:"Referências", semRefs:"Sem referências para este versículo.", refFonte:"Referências: openbible.info (CC-BY)",
    leituraCorrida:"Leitura contínua",
    prefChave:"Palavras-chave sublinhadas", chaveTrad:"Tradução", chaveAqui:"Neste versículo", chavePalavra:"A palavra",
    chaveVer:"Ver o versículo no original", chaveFonte:"Nota de estudo do Sola", fontesRot:"Fontes", chaveDica:"palavra-chave: ver o original e a explicação",
    prefVoc:"Significado das palavras difíceis", vocSig:"Significado", vocOrig:"No original", vocFonte:"Vocabulário do Sola",
    abaTexto:"Texto", abaStrong:"Strong", abaTemas:"Temas", abaDic:"Dicionário", abaConf:"Confissões",
    exConf:"ex.: único consolo, batismo, fim principal", bgConf:"Nas confissões e catecismos",
    exStrong:"ex.: G3056, H2617, logos, hesed, graça", exTema:"ex.: fé, batismo infantil, Trindade", exDic:"ex.: Abraão, altar, aliança",
    comandoBusca:"Passagem, palavra, Strong (G3056) ou doutrina…",
    emEstudo:"Em estudo", eabaOrig:"Léxico & Orig.", eabaCom:"Comentário", eabaRefs:"CFW & Refs", eabaNota:"Nota",
    refAbrir:"Abrir", estudoSegue:"Acompanhar a leitura", estudoFixo:"Fixar neste versículo", estudoVolta:"Voltar ao v.",
    irVerso:"Ir ao versículo", bgTemas:"Temas e doutrinas", bgDic:"Dicionário", bgOrig:"No original", bgVersos:"Versículos", bgTodos:"ver todos",
    verDoutrina:"Ler o capítulo da Confissão", chavesNoVerso:"Palavras destacadas", notaSalva:"Salvo!",
    palavraDia:"Palavra no original", examinarVerso:"Examinar no interlinear", iniciarPlano:"Iniciar plano de leitura",
    indiceCanonico:"Índice canônico", todosLivros:"Todos",
    citSelo:"Nos catecismos e confissões", citMais:"e mais {n} na página do versículo", citFonte:"Textos de prova dos Catecismos de Westminster, da Confissão Belga, do Heidelberg e dos Cânones de Dort; tradução do Sola.",
    doutSelo:"Confissão de Westminster", doutLista:"Confissão de Fé de Westminster (1647) — ou digite um tema", doutPagina:"Página do capítulo, com o texto das provas", doutMais:"continua no capítulo", doutTodos:"Todas as confissões e catecismos", credoSelo:"Credo antigo", credoLer:"Ler o texto completo, com notas",
    doutFonte:"Confissão de Fé de Westminster (1647), domínio público, com os textos de prova da Assembleia; tradução automática do original inglês.",
    conteudoEN:"Conteúdo no original em inglês — tradução em andamento.",
    tradAuto:"Tradução automática do original em inglês.", lerMais:"Ler mais", lerMenos:"Recolher", compartilhar:"Compartilhar", gerandoImagem:"Gerando…", imgTitulo:"Imagem do versículo", imgFormato:"Formato", imgTema:"Tema", imgFeed:"Feed (4:5)", imgStories:"Stories (9:16)", imgClaro:"Claro", imgEscuro:"Escuro", imgBaixar:"Baixar", imgCopiar:"Copiar imagem", imgCopiada:"Imagem copiada.", imgSemCopiar:"Este navegador não deixou copiar; use Baixar.",
    comRef:"Comentário referente ao v.", comBloco:"(o comentário cobre um bloco de versículos)",
    comInicio:"Neste capítulo, o comentário começa no v.",
    semLivroCalvin:"Ainda não há comentário para este livro.",
    autorCalvin:"João Calvino (1509–1564), domínio público", autorHenry:"Matthew Henry (1662–1714), domínio público",
    notaHenry:"Calvino não comentou este livro; aqui, o comentário é de Matthew Henry, pastor puritano.",
    fonteNave:"Nave's Topical Bible (1897), domínio público", acvPagina:"Página do verbete", fonteEaston:"Dicionário Bíblico de Easton (1897), domínio público",
    semOriginal:"Texto original indisponível para este versículo.",
    semComentario:"Ainda não há comentário para este versículo.",
    avisoIdiomaComentario:"Comentário exibido no original em inglês — tradução em andamento.",
    fonte:"Fonte", salvar:"Salvar", cancelar:"Cancelar", excluir:"Excluir", fechar:"Fechar", outrosLugares:"Outros lugares achados",
    escrevaNota:"Escreva sua reflexão sobre este versículo…",
    semNotas:"Você ainda não tem anotações. Toque em um versículo e escolha “Anotação”.",
    bibliaToda:"Buscar na Bíblia toda", carregando:"Carregando…",
    buscando:"Buscando…", resultados:"resultado(s)", nadaEncontrado:"Nada encontrado.", mostrando:"mostrando os primeiros",
    digiteBusca:"Digite ao menos 3 letras, ou uma referência como “João 3:16”.", digiteStrong:"Digite um código (ex.: G3056, H2617) ou ao menos 2 letras.",
    at:"Antigo Testamento", nt:"Novo Testamento",
    exPlaceholder:"ex.: graça e verdade, G3056 ou João 3:16",
    contexto:"Contexto", voltar:"Voltar", dia:"Dia", dias:"dias", capitulos:"capítulos", todosCaps:"Todos os capítulos",
    autor:"Autor", data:"Data", local:"Local", publico:"Público", tema:"Tema", paralelos:"Paralelos",
    escala:["Criação","Êxodo","Davi","Exílio","Cristo","Igreja"],
    erroCarregar:"Não foi possível carregar este texto. Verifique a conexão.", tentar:"Tentar de novo",
    erroIniciar:"Não foi possível carregar o Sola. Verifique a conexão.", recarregar:"Recarregar",
    heroiSobre:"Sola Scriptura", heroiTitulo:"A Escritura, <em>em profundidade</em>",
    heroiTexto:"A Bíblia completa com o grego e o hebraico palavra por palavra, léxico de Strong, comentários de Calvino e Matthew Henry, doutrinas reformadas, referências cruzadas e atlas. Gratuito, sem anúncios, em português.",
    heroiCampo:"João 3:16, Sl 23, G3056 ou uma palavra…", continuar:"Continuar em", comecar:"Começar por João",
    versoDia:"Versículo do dia",
    grupos:{pentateuco:"Pentateuco", historicos:"Históricos", poeticos:"Poéticos e sapienciais", maiores:"Profetas maiores",
      menores:"Profetas menores", evangelhos:"Evangelhos e Atos", paulo:"Cartas de Paulo", gerais:"Cartas gerais e Apocalipse"},
    confTit:"Confissões e catecismos", confTexto:"Os símbolos de fé da Igreja, em português, por tradição.", confTodas:"Todas as confissões",
    confGrupos:["Igreja antiga","Padrões de Westminster","Três Formas de Unidade","Batista reformada"],
    confNomes:{credos:"Credos antigos",westminster:"Confissão de Fé","catecismo-maior":"Catecismo Maior","breve-catecismo":"Breve Catecismo","confissao-belga":"Confissão Belga",heidelberg:"Catecismo de Heidelberg","canones-de-dort":"Cânones de Dort","confissao-batista-1644":"1ª Confissão de Londres","confissao-batista-1689":"2ª Confissão de Londres","catecismo-batista":"Catecismo Batista"},
    recursos:[["Original e Strong","Cada palavra do grego e do hebraico com transliteração, tradução literal e o verbete do léxico."],
      ["Comentários clássicos","João Calvino em 47 livros e Matthew Henry em outros 18, versículo por versículo."],
      ["Referências cruzadas","A Escritura interpreta a Escritura: as passagens paralelas de cada versículo."],
      ["Temas e dicionário","Confissão de Westminster, mais de 5.000 temas de Nave e 3.900 verbetes de Easton."],
      ["Atlas bíblico","1.300 lugares no mapa, com as viagens missionárias de Paulo."],
      ["Planos de leitura","A Bíblia em um ano, o clássico plano de M'Cheyne, o Novo Testamento em 90 dias, Salmos e Provérbios e o Heidelberg em 52 Domingos."]],
    sobreLivro:"Sobre o livro", comentarioDe:"Comentário",
    backup:"Backup", restaurar:"Restaurar", restaurado:"Restaurado deste arquivo:", arquivoInvalido:"Este arquivo não é um backup do Sola.",
    nAnot:"anotação(ões)", nMarc:"marcação(ões)",
    offBaixando:"Baixando…", offPronto:"Pronto: esta tradução inteira está guardada neste aparelho.",
    offErro:"Não deu para baixar tudo. Verifique a conexão e tente de novo.", offSem:"Este navegador não permite guardar o site para uso sem internet.",
    meuEstudo:"Meu estudo", lidoMarcar:"Marcar capítulo como lido", lido:"Capítulo lido", capsLidos:"capítulos lidos", capLido1:"capítulo lido", de:"de",
    pubTit:"Página pública", pubNoAr:"no ar", pubSemConta:"Entre na conta para ter uma página pública do seu perfil, com endereço próprio para compartilhar.",
    pubTexto:"Quem tiver o link vê o seu cartão (nome, foto ou avatar, capa, bio e versículo de vida) e o que você marcar abaixo. Anotações, marcações e o histórico de leitura nunca aparecem.",
    pubEndereco:"Endereço", pubMostrar:"Mostrar também", pubOpcoes:{ num:"Números do estudo (capítulos, livros, dias seguidos)", selos:"Conquistas", prat:"Prateleira de livros" },
    pubPublicar:"Publicar perfil", pubAtualizar:"Atualizar página", pubVer:"Ver página", pubCopiar:"Copiar link", pubCopiado:"Copiado!", pubCopieAMao:"Não deu para copiar sozinho; o link é:", pubTirar:"Tirar do ar",
    pubTirarConfirma:"Tirar sua página pública do ar? O endereço fica livre para outra pessoa.", pubEnviando:"Publicando…",
    pubOk:"Publicado! Seu perfil está em", pubFora:"Sua página pública saiu do ar.", pubErro:"Não deu para publicar agora. Confira a conexão e tente de novo.",
    pubLinkCopiado:"Link copiado.", apelidoLivre:"Disponível.",
    apelidoErros:{ formato:"Use de 3 a 30 letras minúsculas sem acento, números ou hífens (sem hífen no começo ou no fim).", reservado:"Esse endereço é reservado. Escolha outro.",
      improprio:"Esse endereço não é permitido. Escolha outro.", emUso:"Esse endereço já está em uso. Escolha outro." },
    pubCarregando:"Carregando o perfil…", pubNaoAchou:"Perfil não encontrado", pubNaoAchouTexto:"Não há perfil publicado neste endereço. Talvez a pessoa tenha mudado o endereço ou tirado a página do ar.",
    pubSemRedeTit:"Não foi possível abrir o perfil", pubSemRede:"Confira a conexão e tente de novo.", pubLivrosBiblia:"livros da Bíblia completos", pubMaiorSeq:"maior sequência de dias",
    pubAtualizado:"Atualizado em", pubCompartilhar:"Compartilhar", pubEditar:"Editar meu perfil", pubConvite:"Estude a Bíblia com o Sola",
    pubConviteTexto:"Bíblia de estudo gratuita e sem anúncios: texto original palavra por palavra, léxico, comentários de Calvino e Matthew Henry, confissões de fé, atlas e o seu próprio perfil de estudo.",
    pubComecar:"Começar a ler",
    imgPerfilTit:"Imagem do perfil", imgPerfilTexto:"meu estudo bíblico no Sola:", compartilharPerfil:"Compartilhar perfil", imgLivrosLidos:"livros lidos",
    personalizar:"Personalizar perfil", pfNome:"Nome no perfil", pfAvatar:"Avatar", pfAv_letra:"Inicial", pfAv_icone:"Ícone", pfAv_foto:"Foto",
    pfFotoEscolher:"Escolher foto", pfFotoOk:"Foto salva (reduzida a 160 px).", pfFotoDica:"A foto fica pequena e recortada no centro.", pfFotoErro:"Não deu para ler essa imagem.",
    pfCapa:"Capa", capas:{linho:"Linho", carmim:"Carmim", ouro:"Ouro", oliva:"Oliveira", mar:"Mar da Galileia", vigilia:"Vigília"},
    pfVers:"Versículo de vida", pfVersDica:"ex.: Rm 8:28", pfVersErro:"Não reconheci o livro. Tente “Sl 23:1”, “Salmo 23 1” ou “Romanos 8:28”.", pfVersFaltaCap:"falta o capítulo e o versículo (ex.: Sl 23:1).", pfVersEscolha:"toque no versículo:", irPara:"Ir para",
    pfBio:"Sobre você", pfBioDica:"Igreja, tradição, o que você gosta de estudar…", pfEstudo:"Estudo do meu jeito", pfLetra:"Tamanho da letra",
    pfConf:"Confissão em destaque", pfConfW:"Padrões de Westminster", pfConf3:"Três Formas de Unidade", pfSecoes:"Seções do painel (marque as que aparecem)",
    pfSobe:"Subir", pfDesce:"Descer",
    secoesNomes:{semana:"Esta semana", historico:"Últimas 12 semanas", recentes:"Leituras recentes", conquistas:"Conquistas", prateleira:"Minha prateleira",
      livros:"Progresso por livro", planos:"Planos de leitura", marcacoes:"Marcações", notas:"Anotações"},
    conquistasTit:"Conquistas", conquistado:"Conquistado!",
    selos:{primeiro:"Primeiro capítulo", cem:"100 capítulos", quinhentos:"500 capítulos", livroInteiro:"Um livro inteiro", dezLivros:"10 livros inteiros",
      salmos:"Todos os Salmos", pentateuco:"O Pentateuco", evangelhos:"Os quatro Evangelhos", paulo:"As cartas de Paulo", nt:"O Novo Testamento",
      at:"O Antigo Testamento", biblia:"A Bíblia toda", seq7:"7 dias seguidos", seq30:"30 dias seguidos", seq100:"100 dias seguidos",
      plano:"Um plano concluído", notas10:"10 anotações", marcas50:"50 versículos marcados", prateleira5:"5 livros na prateleira"},
    prateleiraTit:"Minha prateleira", stLivro:{lendo:"Lendo", lido:"Lidos", quero:"Quero ler"}, ligaSola:"No Sola", tirarLivro:"Tirar da prateleira",
    pratGrupoRot:"Tipo de livro", pratGrupos:{todos:"Todos", teologia:"Teologia", filosofia:"Filosofia", apologetica:"Apologética", devocional:"Vida cristã", literatura:"Literatura", biografia:"Biografias e história"}, pratBuscaDica:"Buscar: Calvino, Agostinho, Pascal, Lewis…", pratComo:"Pôr como", pratOutro:"Outro livro:", pratTitulo:"Título", pratAutor:"Autor",
    pratPor:"Pôr na prateleira", pratAdicionar:"Adicionar livro", pratVazia:"Monte a sua prateleira com os livros de teologia, filosofia, vida cristã e literatura que você leu, está lendo ou quer ler — há um catálogo de clássicos ligados ao Sola, e dá para pôr qualquer outro.",
    semanaTit:"Esta semana", semanaCaps:"capítulo(s) nesta semana", semanaDias:"dia(s) com leitura", semanaAntes:"semana passada",
    metaRot:"Meta semanal", metaSem:"Sem meta", metaCaps:"capítulos", metaFeita:"Meta da semana cumprida!", metaFalta:"faltam {n} para a meta",
    diasSem:["D","S","T","Q","Q","S","S"], historicoTit:"Últimas 12 semanas", menos:"menos", mais:"mais",
    recentesTit:"Leituras recentes", hoje:"hoje", ontem:"ontem", haDias:"há {n} dias", capsNoDia:"{n} capítulo(s) em {d}",
    diasSeguidos:"dia(s) seguidos", nNotasRot:"anotações", nMarcasRot:"versículos marcados", progLivros:"Progresso por livro",
    marcacoes:"Versículos marcados", semMarcas:"Nenhum versículo marcado ainda. Toque em um versículo e escolha uma cor.", verTodas:"Ver todas",
    perguntaDia:"Pergunta do dia", breveCat:"Breve Catecismo (1647)", lerCatecismo:"Ver no catecismo", pergAbrev:"P.", domingo:"Domingo", domingos:"Domingos", memorizar:"Memorizar", verResposta:"Mostrar resposta",
    planosTit:"Planos de leitura", tempoTit:"Linha do tempo", atlasTit:"Atlas bíblico", atlasDica:"ex.: Jericó, Betel, Corinto",
    atlasFonte:"Lugares: openbible.info Bible Geocoding (CC-BY) · Mapa: desenhado pelo Sola com dados do Natural Earth (domínio público) e relevo do Terrain Tiles (AWS Open Data)",
    lugarIncerto:"Localização incerta: os estudiosos não concordam onde ficava (openbible.info).", ocorrencias:"ocorrência(s) na Bíblia",
    primeira:"Primeira", ultima:"Última", distancias:"Distâncias aproximadas", verFoto:"Ver foto (Wikimedia Commons)", semLeitura:"Marque os capítulos como lidos ao terminar e acompanhe aqui o seu progresso.",
    contaLocal:"Seu estudo fica guardado só neste aparelho. Para levar a outro, use Backup e Restaurar em “Minhas anotações”.",
    contaTitulo:"Continue em qualquer aparelho", contaTexto:"Entre para guardar anotações, marcações, capítulos lidos e planos na sua conta. É gratuito e opcional.",
    entrarGoogle:"Entrar com Google", entrarEmail:"Receber link por e-mail", linkEnviado:"Enviamos um link de acesso para", seuEmail:"seu e-mail",
    sair:"Sair", sincAgora:"Sincronizar agora", sincIndo:"Sincronizando…", sincOk:"Tudo guardado na sua conta",
    sincErro:"Sem conexão com a conta: o que você fizer fica neste aparelho e sobe depois", entrou:"Você entrou como", erroConta:"Não foi possível conectar à conta agora. Tente de novo.",
    contaOutra:"Este aparelho tem o estudo de outra conta. Trocar pelo estudo da conta em que você entrou agora? O que ainda não tinha sido sincronizado da outra conta será perdido.",
    excluirConta:"Excluir minha conta", excluirConfirma:"Excluir a sua conta e tudo o que está guardado nela no servidor? Isso não pode ser desfeito. O que está neste aparelho continua aqui.",
    contaExcluida:"Conta excluída. O que estava neste aparelho continua aqui.",
    abaEstudo:"Estudo", abaPerfil:"Perfil", visitante:"Visitante", visitanteTexto:"Sem conta: seu estudo fica só neste aparelho.",
    desde:"No Sola desde", preferencias:"Preferências", temaRot:"Aparência", claro:"Claro", escuro:"Escuro",
    seusDados:"Seus dados", lerOffline:"Ler sem internet", privacidade:"Privacidade", faixaTexto:"Entre para guardar seu estudo.",
    vantagens:["Anotações e versículos marcados em todos os seus aparelhos","Capítulos lidos e planos de leitura sempre em dia","Continue exatamente de onde parou"],
    conviteSobre:"Seu estudo, sempre com você", agoraNao:"Agora não",
    instSobre:"Sola no celular", instTit:"Instale o Sola na tela inicial", instTexto:"Abre como um aplicativo, sem a barra do navegador, e os capítulos que você já leu funcionam sem internet.", instBotao:"Instalar", instEntendi:"Entendi", instIos:"No Safari, toque em <b>Compartilhar</b> (o quadrado com a seta para cima) e depois em <b>Adicionar à Tela de Início</b>.", instOutro:"No menu do navegador (⋮ ou ⋯), procure <b>Instalar aplicativo</b> ou <b>Adicionar à tela inicial</b>.", instJa:"O Sola já está instalado neste aparelho.",
    convites:{nota:"Sua anotação está só neste aparelho", marca:"Suas marcações estão só neste aparelho", lido:"Guarde o seu progresso", padrao:"Continue de onde parou"},
    conviteTexto:"Entre com o Google para guardar anotações, marcações e capítulos lidos e continuar em qualquer aparelho. É gratuito." },
  en: { idioma:"Language", traducao:"Translation", comparar:"Compare with…", semComparar:"No comparison",
    livros:"Books", buscar:"Search", notas:"My notes", marcar:"Highlight",
    cores:{ouro:"gold", verde:"green", azul:"blue", rosa:"pink"},
    original:"Original", comentario:"Commentary", anotacao:"Note", copiar:"Copy", copiado:"Copied!",
    grego:"Greek — Textus Receptus", hebraico:"Hebrew — Leningrad Codex",
    sugerir:"Suggest a correction", lexDef:"Definition (Strong)", lexKjv:"KJV renderings", lexPagina:"Full page with every verse (in Portuguese)", lexFonte:"Strong's Lexicon (1890) · Tagged text: STEPBible/Tyndale House (CC BY)",
    referencias:"Cross-refs", semRefs:"No cross-references for this verse.", refFonte:"Cross-references: openbible.info (CC-BY)",
    leituraCorrida:"Continuous reading",
    prefChave:"Underlined key words", chaveTrad:"Translation", chaveAqui:"In this verse", chavePalavra:"The word",
    chaveVer:"See the verse in the original", chaveFonte:"Sola study note", fontesRot:"Sources", chaveDica:"key word: see the original and the explanation",
    prefVoc:"Meaning of hard words", vocSig:"Meaning", vocOrig:"In the original", vocFonte:"Sola glossary",
    abaTexto:"Text", abaStrong:"Strong", abaTemas:"Topics", abaDic:"Dictionary", abaConf:"Confessions",
    exConf:"in Portuguese, e.g. batismo, consolo", bgConf:"In the confessions and catechisms",
    exStrong:"e.g. G3056, H2617, logos, grace", exTema:"e.g. faith, covenant", exDic:"e.g. Abraham, altar",
    comandoBusca:"Passage, word, Strong (G3056) or doctrine…",
    emEstudo:"Studying", eabaOrig:"Lexicon & Orig.", eabaCom:"Commentary", eabaRefs:"WCF & Refs", eabaNota:"Note",
    refAbrir:"Open", estudoSegue:"Follow my reading", estudoFixo:"Pin to this verse", estudoVolta:"Back to v.",
    irVerso:"Go to the verse", bgTemas:"Topics and doctrines", bgDic:"Dictionary", bgOrig:"In the original", bgVersos:"Verses", bgTodos:"see all",
    verDoutrina:"Read the Confession chapter", chavesNoVerso:"Key words", notaSalva:"Saved!",
    palavraDia:"Word in the original", examinarVerso:"Inspect in interlinear", iniciarPlano:"Start a reading plan",
    indiceCanonico:"Canonical index", todosLivros:"All",
    citSelo:"In the catechisms and confessions", citMais:"and {n} more on the verse page", citFonte:"Proof texts of the Westminster Catechisms, the Belgic Confession, the Heidelberg Catechism and the Canons of Dort; Sola's Portuguese translation.",
    doutSelo:"Westminster Confession", doutLista:"Westminster Confession of Faith (1647) — or type a topic", doutPagina:"Chapter page with the proof texts (in Portuguese)", doutMais:"continues in the chapter", doutTodos:"All creeds, confessions and catechisms (in Portuguese)", credoSelo:"Ancient creed", credoLer:"Read the full text (in Portuguese)",
    doutFonte:"Westminster Confession of Faith (1647), public domain, with the Westminster Assembly's proof texts.",
    conteudoEN:"Content in the original English.",
    tradAuto:"", lerMais:"Read more", lerMenos:"Show less", compartilhar:"Share", gerandoImagem:"Creating…", imgTitulo:"Verse image", imgFormato:"Format", imgTema:"Theme", imgFeed:"Feed (4:5)", imgStories:"Stories (9:16)", imgClaro:"Light", imgEscuro:"Dark", imgBaixar:"Download", imgCopiar:"Copy image", imgCopiada:"Image copied.", imgSemCopiar:"This browser did not allow copying; use Download.",
    comRef:"Commentary on v.", comBloco:"(the commentary covers a block of verses)",
    comInicio:"In this chapter, the commentary begins at v.",
    semLivroCalvin:"No commentary available for this book yet.",
    autorCalvin:"John Calvin (1509–1564), public domain", autorHenry:"Matthew Henry (1662–1714), public domain",
    notaHenry:"Calvin did not comment on this book; this commentary is by Matthew Henry, Puritan pastor.",
    fonteNave:"Nave's Topical Bible (1897), public domain", acvPagina:"Entry page (in Portuguese)", fonteEaston:"Easton's Bible Dictionary (1897), public domain",
    semOriginal:"Original text unavailable for this verse.",
    semComentario:"No commentary available for this verse yet.",
    avisoIdiomaComentario:"Commentary shown in the original English.",
    fonte:"Source", salvar:"Save", cancelar:"Cancel", excluir:"Delete", fechar:"Close", outrosLugares:"Other places found",
    escrevaNota:"Write your reflection on this verse…",
    semNotas:"No notes yet. Tap a verse and choose “Note”.",
    bibliaToda:"Search the whole Bible", carregando:"Loading…",
    buscando:"Searching…", resultados:"result(s)", nadaEncontrado:"Nothing found.", mostrando:"showing the first",
    digiteBusca:"Type at least 3 letters, or a reference such as “John 3:16”.", digiteStrong:"Type a Strong code (e.g. G3056, H2617) or at least 2 letters.",
    at:"Old Testament", nt:"New Testament",
    exPlaceholder:"e.g. grace and truth, G3056 or John 3:16",
    contexto:"Context", voltar:"Back", dia:"Day", dias:"days", capitulos:"chapters", todosCaps:"All chapters",
    autor:"Author", data:"Date", local:"Place", publico:"Audience", tema:"Theme", paralelos:"Parallels",
    escala:["Creation","Exodus","David","Exile","Christ","Church"],
    erroCarregar:"Could not load this text. Check your connection.", tentar:"Try again",
    erroIniciar:"Could not load Sola. Check your connection.", recarregar:"Reload",
    heroiSobre:"Sola Scriptura", heroiTitulo:"Scripture, <em>in depth</em>",
    heroiTexto:"The whole Bible with Greek and Hebrew word by word, Strong's lexicon, commentaries by Calvin and Matthew Henry, cross-references and an atlas. Free, with no ads.",
    heroiCampo:"John 3:16, Ps 23, G3056 or a word…", continuar:"Continue in", comecar:"Start with John",
    versoDia:"Verse of the day",
    grupos:{pentateuco:"Pentateuch", historicos:"History", poeticos:"Poetry and wisdom", maiores:"Major prophets",
      menores:"Minor prophets", evangelhos:"Gospels and Acts", paulo:"Paul's letters", gerais:"General letters and Revelation"},
    confTit:"Confessions and catechisms", confTexto:"The Church’s creeds and confessions, in Portuguese, by tradition.", confTodas:"All confessions",
    confGrupos:["Early Church","Westminster Standards","Three Forms of Unity","Reformed Baptist"],
    confNomes:{credos:"Ancient creeds",westminster:"Confession of Faith","catecismo-maior":"Larger Catechism","breve-catecismo":"Shorter Catechism","confissao-belga":"Belgic Confession",heidelberg:"Heidelberg Catechism","canones-de-dort":"Canons of Dort","confissao-batista-1644":"First London Confession","confissao-batista-1689":"Second London Confession","catecismo-batista":"Baptist Catechism"},
    recursos:[["Original and Strong","Every Greek and Hebrew word with transliteration, literal gloss and its lexicon entry."],
      ["Classic commentaries","John Calvin on 47 books and Matthew Henry on another 18, verse by verse."],
      ["Cross-references","Scripture interprets Scripture: parallel passages for every verse."],
      ["Topics and dictionary","Over 5,000 topics from Nave and 3,900 entries from Easton's dictionary."],
      ["Bible atlas","1,300 places on the map, with Paul's missionary journeys."],
      ["Reading plans","The Bible in a year, the classic M'Cheyne plan, the New Testament in 90 days, Psalms and Proverbs, and Heidelberg in 52 Lord's Days."]],
    sobreLivro:"About the book", comentarioDe:"Commentary",
    backup:"Backup", restaurar:"Restore", restaurado:"Restored from this file:", arquivoInvalido:"This file is not a Sola backup.",
    nAnot:"note(s)", nMarc:"highlight(s)",
    offBaixando:"Downloading…", offPronto:"Done: this whole translation is stored on this device.",
    offErro:"Could not download everything. Check your connection and try again.", offSem:"This browser cannot store the site for offline use.",
    meuEstudo:"My study", lidoMarcar:"Mark chapter as read", lido:"Chapter read", capsLidos:"chapters read", capLido1:"chapter read", de:"of",
    pubTit:"Public page", pubNoAr:"online", pubSemConta:"Sign in to get a public page for your profile, with its own address to share.",
    pubTexto:"Anyone with the link sees your card (name, photo or avatar, cover, bio and life verse) and whatever you tick below. Notes, highlights and reading history never appear.",
    pubEndereco:"Address", pubMostrar:"Also show", pubOpcoes:{ num:"Study numbers (chapters, books, days in a row)", selos:"Achievements", prat:"Bookshelf" },
    pubPublicar:"Publish profile", pubAtualizar:"Update page", pubVer:"View page", pubCopiar:"Copy link", pubCopiado:"Copied!", pubCopieAMao:"Could not copy automatically; the link is:", pubTirar:"Unpublish",
    pubTirarConfirma:"Take your public page down? The address becomes free for someone else.", pubEnviando:"Publishing…",
    pubOk:"Published! Your profile is at", pubFora:"Your public page is no longer online.", pubErro:"Could not publish right now. Check your connection and try again.",
    pubLinkCopiado:"Link copied.", apelidoLivre:"Available.",
    apelidoErros:{ formato:"Use 3 to 30 lowercase letters without accents, numbers or hyphens (no hyphen at the start or end).", reservado:"That address is reserved. Choose another.",
      improprio:"That address is not allowed. Choose another.", emUso:"That address is already taken. Choose another." },
    pubCarregando:"Loading profile…", pubNaoAchou:"Profile not found", pubNaoAchouTexto:"There is no profile published at this address. The person may have changed the address or taken the page down.",
    pubSemRedeTit:"Could not open the profile", pubSemRede:"Check your connection and try again.", pubLivrosBiblia:"books of the Bible completed", pubMaiorSeq:"longest streak (days)",
    pubAtualizado:"Updated on", pubCompartilhar:"Share", pubEditar:"Edit my profile", pubConvite:"Study the Bible with Sola",
    pubConviteTexto:"A free Bible study site with no ads: the original text word by word, lexicon, commentaries by Calvin and Matthew Henry, confessions of faith, an atlas and your own study profile.",
    pubComecar:"Start reading",
    imgPerfilTit:"Profile image", imgPerfilTexto:"my Bible study on Sola:", compartilharPerfil:"Share profile", imgLivrosLidos:"books read",
    personalizar:"Customize profile", pfNome:"Profile name", pfAvatar:"Avatar", pfAv_letra:"Initial", pfAv_icone:"Icon", pfAv_foto:"Photo",
    pfFotoEscolher:"Choose photo", pfFotoOk:"Photo saved (reduced to 160 px).", pfFotoDica:"The photo is made small and cropped to the center.", pfFotoErro:"Couldn't read that image.",
    pfCapa:"Cover", capas:{linho:"Linen", carmim:"Crimson", ouro:"Gold", oliva:"Olive", mar:"Sea of Galilee", vigilia:"Vigil"},
    pfVers:"Life verse", pfVersDica:"e.g. Rom 8:28", pfVersErro:"I didn't recognize the book. Try “Ps 23:1”, “Psalm 23 1” or “Romans 8:28”.", pfVersFaltaCap:"add the chapter and verse (e.g. Ps 23:1).", pfVersEscolha:"tap the verse:", irPara:"Go to",
    pfBio:"About you", pfBioDica:"Church, tradition, what you like to study…", pfEstudo:"Study my way", pfLetra:"Text size",
    pfConf:"Featured confession", pfConfW:"Westminster Standards", pfConf3:"Three Forms of Unity", pfSecoes:"Panel sections (tick the ones shown)",
    pfSobe:"Move up", pfDesce:"Move down",
    secoesNomes:{semana:"This week", historico:"Last 12 weeks", recentes:"Recent reading", conquistas:"Achievements", prateleira:"My bookshelf",
      livros:"Progress by book", planos:"Reading plans", marcacoes:"Highlights", notas:"Notes"},
    conquistasTit:"Achievements", conquistado:"Earned!",
    selos:{primeiro:"First chapter", cem:"100 chapters", quinhentos:"500 chapters", livroInteiro:"A whole book", dezLivros:"10 whole books",
      salmos:"All the Psalms", pentateuco:"The Pentateuch", evangelhos:"The four Gospels", paulo:"Paul's letters", nt:"The New Testament",
      at:"The Old Testament", biblia:"The whole Bible", seq7:"7 days in a row", seq30:"30 days in a row", seq100:"100 days in a row",
      plano:"A plan completed", notas10:"10 notes", marcas50:"50 highlighted verses", prateleira5:"5 books on the shelf"},
    prateleiraTit:"My bookshelf", stLivro:{lendo:"Reading", lido:"Read", quero:"Want to read"}, ligaSola:"On Sola", tirarLivro:"Remove from shelf",
    pratGrupoRot:"Kind of book", pratGrupos:{todos:"All", teologia:"Theology", filosofia:"Philosophy", apologetica:"Apologetics", devocional:"Christian life", literatura:"Literature", biografia:"Biographies and history"}, pratBuscaDica:"Search: Calvin, Augustine, Pascal, Lewis…", pratComo:"Add as", pratOutro:"Another book:", pratTitulo:"Title", pratAutor:"Author",
    pratPor:"Add to shelf", pratAdicionar:"Add book", pratVazia:"Build your shelf with the theology, philosophy, Christian life and literature books you've read, are reading or want to read — there's a catalog of classics linked to Sola, and you can add any other.",
    semanaTit:"This week", semanaCaps:"chapter(s) this week", semanaDias:"day(s) with reading", semanaAntes:"last week",
    metaRot:"Weekly goal", metaSem:"No goal", metaCaps:"chapters", metaFeita:"Weekly goal reached!", metaFalta:"{n} to go",
    diasSem:["S","M","T","W","T","F","S"], historicoTit:"Last 12 weeks", menos:"less", mais:"more",
    recentesTit:"Recent reading", hoje:"today", ontem:"yesterday", haDias:"{n} days ago", capsNoDia:"{n} chapter(s) on {d}",
    diasSeguidos:"day(s) in a row", nNotasRot:"notes", nMarcasRot:"highlighted verses", progLivros:"Progress by book",
    marcacoes:"Highlighted verses", semMarcas:"No highlighted verses yet. Tap a verse and pick a colour.", verTodas:"See all",
    perguntaDia:"Question of the day", breveCat:"Shorter Catechism (1647)", lerCatecismo:"Open in the catechism", pergAbrev:"Q.", domingo:"Lord's Day", domingos:"Lord's Days", memorizar:"Memorize", verResposta:"Show answer",
    planosTit:"Reading plans", tempoTit:"Timeline", atlasTit:"Bible atlas", atlasDica:"e.g. Jericho, Bethel, Corinth",
    atlasFonte:"Places: openbible.info Bible Geocoding (CC-BY) · Map: drawn by Sola from Natural Earth data (public domain) with relief from Terrain Tiles (AWS Open Data)",
    lugarIncerto:"Uncertain location: scholars disagree on where it was (openbible.info).", ocorrencias:"occurrence(s) in the Bible",
    primeira:"First", ultima:"Last", distancias:"Approximate distances", verFoto:"See photo (Wikimedia Commons)", semLeitura:"Mark chapters as read when you finish them and follow your progress here.",
    contaLocal:"Your study is stored on this device only. To move it, use Backup and Restore under “My notes”.",
    contaTitulo:"Pick up on any device", contaTexto:"Sign in to keep your notes, highlights, chapters read and plans in your account. Free and optional.",
    entrarGoogle:"Sign in with Google", entrarEmail:"Email me a link", linkEnviado:"We sent a sign-in link to", seuEmail:"your email",
    sair:"Sign out", sincAgora:"Sync now", sincIndo:"Syncing…", sincOk:"Everything is saved to your account",
    sincErro:"Cannot reach your account: changes stay on this device and upload later", entrou:"Signed in as", erroConta:"Could not reach the account right now. Try again.",
    contaOutra:"This device holds another account's study. Replace it with the study from the account you just signed in to? Anything not yet synced from the other account will be lost.",
    excluirConta:"Delete my account", excluirConfirma:"Delete your account and everything stored in it on the server? This cannot be undone. What is on this device stays here.",
    contaExcluida:"Account deleted. What was on this device is still here.",
    abaEstudo:"Study", abaPerfil:"Profile", visitante:"Guest", visitanteTexto:"No account: your study stays on this device only.",
    desde:"On Sola since", preferencias:"Preferences", temaRot:"Appearance", claro:"Light", escuro:"Dark",
    seusDados:"Your data", lerOffline:"Read offline", privacidade:"Privacy", faixaTexto:"Sign in to keep your study.",
    vantagens:["Notes and highlighted verses on all your devices","Chapters read and reading plans always up to date","Pick up exactly where you left off"],
    conviteSobre:"Your study, always with you", agoraNao:"Not now",
    instSobre:"Sola on your phone", instTit:"Add Sola to your home screen", instTexto:"It opens like an app, without the browser bar, and the chapters you have read work offline.", instBotao:"Install", instEntendi:"Got it", instIos:"In Safari, tap <b>Share</b> (the square with an arrow) and then <b>Add to Home Screen</b>.", instOutro:"In the browser menu (⋮ or ⋯), look for <b>Install app</b> or <b>Add to home screen</b>.", instJa:"Sola is already installed on this device.",
    convites:{nota:"Your note is on this device only", marca:"Your highlights are on this device only", lido:"Keep your progress", padrao:"Pick up where you left off"},
    conviteTexto:"Sign in with Google to keep your notes, highlights and chapters read, and continue on any device. It's free." },
  es: { idioma:"Idioma", traducao:"Traducción", comparar:"Comparar con…", semComparar:"Sin comparación",
    livros:"Libros", buscar:"Buscar", notas:"Mis notas", marcar:"Resaltar",
    cores:{ouro:"oro", verde:"verde", azul:"azul", rosa:"rosa"},
    original:"Original", comentario:"Comentario", anotacao:"Nota", copiar:"Copiar", copiado:"¡Copiado!",
    grego:"Griego — Textus Receptus", hebraico:"Hebreo — Códice de Leningrado",
    sugerir:"Sugerir corrección", lexDef:"Definición (Strong)", lexKjv:"Traducciones en la KJV", lexPagina:"Página completa con todos los versículos (en portugués)", lexFonte:"Léxico de Strong (1890) · Texto marcado: STEPBible/Tyndale House (CC BY)",
    referencias:"Referencias", semRefs:"Sin referencias para este versículo.", refFonte:"Referencias: openbible.info (CC-BY)",
    leituraCorrida:"Lectura continua",
    prefChave:"Palabras clave subrayadas", chaveTrad:"Traducción", chaveAqui:"En este versículo", chavePalavra:"La palabra",
    chaveVer:"Ver el versículo en el original", chaveFonte:"Nota de estudio de Sola", fontesRot:"Fuentes", chaveDica:"palabra clave: ver el original y la explicación",
    prefVoc:"Significado de palabras difíciles", vocSig:"Significado", vocOrig:"En el original", vocFonte:"Vocabulario de Sola",
    abaTexto:"Texto", abaStrong:"Strong", abaTemas:"Temas", abaDic:"Diccionario", abaConf:"Confesiones",
    exConf:"en portugués, ej.: batismo, consolo", bgConf:"En las confesiones y catecismos",
    exStrong:"ej.: G3056, H2617, logos, gracia", exTema:"ej.: fe, pacto", exDic:"ej.: Abraham, altar",
    comandoBusca:"Pasaje, palabra, Strong (G3056) o doctrina…",
    emEstudo:"En estudio", eabaOrig:"Léxico y Orig.", eabaCom:"Comentario", eabaRefs:"CFW y Refs", eabaNota:"Nota",
    refAbrir:"Abrir", estudoSegue:"Seguir la lectura", estudoFixo:"Fijar en este versículo", estudoVolta:"Volver al v.",
    irVerso:"Ir al versículo", bgTemas:"Temas y doctrinas", bgDic:"Diccionario", bgOrig:"En el original", bgVersos:"Versículos", bgTodos:"ver todos",
    verDoutrina:"Leer el capítulo de la Confesión", chavesNoVerso:"Palabras clave", notaSalva:"¡Guardado!",
    palavraDia:"Palabra en el original", examinarVerso:"Examinar en interlineal", iniciarPlano:"Iniciar plan de lectura",
    indiceCanonico:"Índice canónico", todosLivros:"Todos",
    citSelo:"En los catecismos y confesiones", citMais:"y {n} más en la página del versículo", citFonte:"Textos de prueba de los Catecismos de Westminster, la Confesión Belga, el Catecismo de Heidelberg y los Cánones de Dort; traducción al portugués de Sola.",
    doutSelo:"Confesión de Westminster", doutLista:"Confesión de Fe de Westminster (1647) — o escribe un tema", doutPagina:"Página del capítulo (en portugués)", doutMais:"continúa en el capítulo", doutTodos:"Todas las confesiones y catecismos (en portugués)", credoSelo:"Credo antiguo", credoLer:"Leer el texto completo (en portugués)",
    doutFonte:"Confesión de Fe de Westminster (1647), dominio público, con los textos de prueba de la Asamblea; traducción automática al portugués del original inglés.",
    conteudoEN:"Contenido en el inglés original.",
    tradAuto:"", lerMais:"Leer más", lerMenos:"Ocultar", compartilhar:"Compartir", gerandoImagem:"Generando…", imgTitulo:"Imagen del versículo", imgFormato:"Formato", imgTema:"Tema", imgFeed:"Feed (4:5)", imgStories:"Stories (9:16)", imgClaro:"Claro", imgEscuro:"Oscuro", imgBaixar:"Descargar", imgCopiar:"Copiar imagen", imgCopiada:"Imagen copiada.", imgSemCopiar:"Este navegador no permitió copiar; usa Descargar.",
    comRef:"Comentario sobre el v.", comBloco:"(el comentario abarca un bloque de versículos)",
    comInicio:"En este capítulo, el comentario comienza en el v.",
    semLivroCalvin:"Aún no hay comentario para este libro.",
    autorCalvin:"Juan Calvino (1509–1564), dominio público", autorHenry:"Matthew Henry (1662–1714), dominio público",
    notaHenry:"Calvino no comentó este libro; aquí el comentario es de Matthew Henry, pastor puritano.",
    fonteNave:"Nave's Topical Bible (1897), dominio público", acvPagina:"Página de la entrada (en portugués)", fonteEaston:"Diccionario Bíblico de Easton (1897), dominio público",
    semOriginal:"Texto original no disponible para este versículo.",
    semComentario:"Aún no hay comentario para este versículo.",
    avisoIdiomaComentario:"Comentario mostrado en el inglés original.",
    fonte:"Fuente", salvar:"Guardar", cancelar:"Cancelar", excluir:"Eliminar", fechar:"Cerrar", outrosLugares:"Otros lugares encontrados",
    escrevaNota:"Escribe tu reflexión sobre este versículo…",
    semNotas:"Aún no tienes notas. Toca un versículo y elige “Nota”.",
    bibliaToda:"Buscar en toda la Biblia", carregando:"Cargando…",
    buscando:"Buscando…", resultados:"resultado(s)", nadaEncontrado:"No se encontró nada.", mostrando:"mostrando los primeros",
    digiteBusca:"Escribe al menos 3 letras, o una referencia como “Juan 3:16”.", digiteStrong:"Escribe un código (ej.: G3056, H2617) o al menos 2 letras.",
    at:"Antiguo Testamento", nt:"Nuevo Testamento",
    exPlaceholder:"ej.: gracia y verdad, G3056 o Juan 3:16",
    contexto:"Contexto", voltar:"Volver", dia:"Día", dias:"días", capitulos:"capítulos", todosCaps:"Todos los capítulos",
    autor:"Autor", data:"Fecha", local:"Lugar", publico:"Destinatarios", tema:"Tema", paralelos:"Paralelos",
    escala:["Creación","Éxodo","David","Exilio","Cristo","Iglesia"],
    erroCarregar:"No se pudo cargar este texto. Revisa la conexión.", tentar:"Reintentar",
    erroIniciar:"No se pudo cargar Sola. Revisa la conexión.", recarregar:"Recargar",
    heroiSobre:"Sola Scriptura", heroiTitulo:"La Escritura, <em>en profundidad</em>",
    heroiTexto:"La Biblia completa con el griego y el hebreo palabra por palabra, léxico de Strong, comentarios de Calvino y Matthew Henry, referencias cruzadas y atlas. Gratis y sin anuncios.",
    heroiCampo:"Juan 3:16, Sal 23, G3056 o una palabra…", continuar:"Continuar en", comecar:"Empezar por Juan",
    versoDia:"Versículo del día",
    grupos:{pentateuco:"Pentateuco", historicos:"Históricos", poeticos:"Poéticos y sapienciales", maiores:"Profetas mayores",
      menores:"Profetas menores", evangelhos:"Evangelios y Hechos", paulo:"Cartas de Pablo", gerais:"Cartas generales y Apocalipsis"},
    confTit:"Confesiones y catecismos", confTexto:"Los símbolos de fe de la Iglesia, en portugués, por tradición.", confTodas:"Todas las confesiones",
    confGrupos:["Iglesia antigua","Normas de Westminster","Tres Formas de Unidad","Bautista reformada"],
    confNomes:{credos:"Credos antiguos",westminster:"Confesión de Fe","catecismo-maior":"Catecismo Mayor","breve-catecismo":"Catecismo Menor","confissao-belga":"Confesión Belga",heidelberg:"Catecismo de Heidelberg","canones-de-dort":"Cánones de Dort","confissao-batista-1644":"1.ª Confesión de Londres","confissao-batista-1689":"2.ª Confesión de Londres","catecismo-batista":"Catecismo Bautista"},
    recursos:[["Original y Strong","Cada palabra del griego y del hebreo con transliteración, traducción literal y su entrada del léxico."],
      ["Comentarios clásicos","Juan Calvino en 47 libros y Matthew Henry en otros 18, versículo por versículo."],
      ["Referencias cruzadas","La Escritura interpreta la Escritura: pasajes paralelos de cada versículo."],
      ["Temas y diccionario","Más de 5.000 temas de Nave y 3.900 entradas del diccionario de Easton."],
      ["Atlas bíblico","1.300 lugares en el mapa, con los viajes misioneros de Pablo."],
      ["Planes de lectura","La Biblia en un año, el clásico plan de M'Cheyne, el Nuevo Testamento en 90 días, Salmos y Proverbios y Heidelberg en 52 domingos."]],
    sobreLivro:"Sobre el libro", comentarioDe:"Comentario",
    backup:"Copia", restaurar:"Restaurar", restaurado:"Restaurado de este archivo:", arquivoInvalido:"Este archivo no es una copia de Sola.",
    nAnot:"nota(s)", nMarc:"resaltado(s)",
    offBaixando:"Descargando…", offPronto:"Listo: esta traducción completa está guardada en este dispositivo.",
    offErro:"No se pudo descargar todo. Revisa la conexión e inténtalo de nuevo.", offSem:"Este navegador no permite guardar el sitio para usarlo sin conexión.",
    meuEstudo:"Mi estudio", lidoMarcar:"Marcar capítulo como leído", lido:"Capítulo leído", capsLidos:"capítulos leídos", capLido1:"capítulo leído", de:"de",
    pubTit:"Página pública", pubNoAr:"en línea", pubSemConta:"Inicia sesión para tener una página pública de tu perfil, con dirección propia para compartir.",
    pubTexto:"Quien tenga el enlace ve tu tarjeta (nombre, foto o avatar, portada, bio y versículo de vida) y lo que marques abajo. Notas, resaltados e historial de lectura nunca aparecen.",
    pubEndereco:"Dirección", pubMostrar:"Mostrar también", pubOpcoes:{ num:"Números del estudio (capítulos, libros, días seguidos)", selos:"Logros", prat:"Estantería de libros" },
    pubPublicar:"Publicar perfil", pubAtualizar:"Actualizar página", pubVer:"Ver página", pubCopiar:"Copiar enlace", pubCopiado:"¡Copiado!", pubCopieAMao:"No se pudo copiar solo; el enlace es:", pubTirar:"Retirar",
    pubTirarConfirma:"¿Retirar tu página pública? La dirección queda libre para otra persona.", pubEnviando:"Publicando…",
    pubOk:"¡Publicado! Tu perfil está en", pubFora:"Tu página pública ya no está en línea.", pubErro:"No se pudo publicar ahora. Revisa la conexión e inténtalo de nuevo.",
    pubLinkCopiado:"Enlace copiado.", apelidoLivre:"Disponible.",
    apelidoErros:{ formato:"Usa de 3 a 30 letras minúsculas sin tilde, números o guiones (sin guion al principio ni al final).", reservado:"Esa dirección está reservada. Elige otra.",
      improprio:"Esa dirección no está permitida. Elige otra.", emUso:"Esa dirección ya está en uso. Elige otra." },
    pubCarregando:"Cargando el perfil…", pubNaoAchou:"Perfil no encontrado", pubNaoAchouTexto:"No hay un perfil publicado en esta dirección. Tal vez la persona cambió la dirección o retiró la página.",
    pubSemRedeTit:"No se pudo abrir el perfil", pubSemRede:"Revisa la conexión e inténtalo de nuevo.", pubLivrosBiblia:"libros de la Biblia completos", pubMaiorSeq:"racha más larga (días)",
    pubAtualizado:"Actualizado el", pubCompartilhar:"Compartir", pubEditar:"Editar mi perfil", pubConvite:"Estudia la Biblia con Sola",
    pubConviteTexto:"Biblia de estudio gratuita y sin anuncios: texto original palabra por palabra, léxico, comentarios de Calvino y Matthew Henry, confesiones de fe, atlas y tu propio perfil de estudio.",
    pubComecar:"Empezar a leer",
    imgPerfilTit:"Imagen del perfil", imgPerfilTexto:"mi estudio bíblico en Sola:", compartilharPerfil:"Compartir perfil", imgLivrosLidos:"libros leídos",
    personalizar:"Personalizar perfil", pfNome:"Nombre en el perfil", pfAvatar:"Avatar", pfAv_letra:"Inicial", pfAv_icone:"Ícono", pfAv_foto:"Foto",
    pfFotoEscolher:"Elegir foto", pfFotoOk:"Foto guardada (reducida a 160 px).", pfFotoDica:"La foto queda pequeña y recortada al centro.", pfFotoErro:"No se pudo leer esa imagen.",
    pfCapa:"Portada", capas:{linho:"Lino", carmim:"Carmesí", ouro:"Oro", oliva:"Olivo", mar:"Mar de Galilea", vigilia:"Vigilia"},
    pfVers:"Versículo de vida", pfVersDica:"ej.: Ro 8:28", pfVersErro:"No reconocí el libro. Prueba “Sal 23:1”, “Salmo 23 1” o “Romanos 8:28”.", pfVersFaltaCap:"falta el capítulo y el versículo (ej.: Sal 23:1).", pfVersEscolha:"toca el versículo:", irPara:"Ir a",
    pfBio:"Sobre ti", pfBioDica:"Iglesia, tradición, lo que te gusta estudiar…", pfEstudo:"Estudio a mi manera", pfLetra:"Tamaño de letra",
    pfConf:"Confesión destacada", pfConfW:"Normas de Westminster", pfConf3:"Tres Formas de Unidad", pfSecoes:"Secciones del panel (marca las que aparecen)",
    pfSobe:"Subir", pfDesce:"Bajar",
    secoesNomes:{semana:"Esta semana", historico:"Últimas 12 semanas", recentes:"Lecturas recientes", conquistas:"Logros", prateleira:"Mi estantería",
      livros:"Progreso por libro", planos:"Planes de lectura", marcacoes:"Resaltados", notas:"Notas"},
    conquistasTit:"Logros", conquistado:"¡Logrado!",
    selos:{primeiro:"Primer capítulo", cem:"100 capítulos", quinhentos:"500 capítulos", livroInteiro:"Un libro entero", dezLivros:"10 libros enteros",
      salmos:"Todos los Salmos", pentateuco:"El Pentateuco", evangelhos:"Los cuatro Evangelios", paulo:"Las cartas de Pablo", nt:"El Nuevo Testamento",
      at:"El Antiguo Testamento", biblia:"Toda la Biblia", seq7:"7 días seguidos", seq30:"30 días seguidos", seq100:"100 días seguidos",
      plano:"Un plan completado", notas10:"10 notas", marcas50:"50 versículos resaltados", prateleira5:"5 libros en la estantería"},
    prateleiraTit:"Mi estantería", stLivro:{lendo:"Leyendo", lido:"Leídos", quero:"Quiero leer"}, ligaSola:"En Sola", tirarLivro:"Quitar de la estantería",
    pratGrupoRot:"Tipo de libro", pratGrupos:{todos:"Todos", teologia:"Teología", filosofia:"Filosofía", apologetica:"Apologética", devocional:"Vida cristiana", literatura:"Literatura", biografia:"Biografías e historia"}, pratBuscaDica:"Buscar: Calvino, Agustín, Pascal, Lewis…", pratComo:"Poner como", pratOutro:"Otro libro:", pratTitulo:"Título", pratAutor:"Autor",
    pratPor:"Poner en la estantería", pratAdicionar:"Añadir libro", pratVazia:"Arma tu estantería con los libros de teología, filosofía, vida cristiana y literatura que leíste, estás leyendo o quieres leer — hay un catálogo de clásicos enlazados con Sola, y puedes poner cualquier otro.",
    semanaTit:"Esta semana", semanaCaps:"capítulo(s) esta semana", semanaDias:"día(s) con lectura", semanaAntes:"semana pasada",
    metaRot:"Meta semanal", metaSem:"Sin meta", metaCaps:"capítulos", metaFeita:"¡Meta de la semana cumplida!", metaFalta:"faltan {n} para la meta",
    diasSem:["D","L","M","X","J","V","S"], historicoTit:"Últimas 12 semanas", menos:"menos", mais:"más",
    recentesTit:"Lecturas recientes", hoje:"hoy", ontem:"ayer", haDias:"hace {n} días", capsNoDia:"{n} capítulo(s) el {d}",
    diasSeguidos:"día(s) seguidos", nNotasRot:"notas", nMarcasRot:"versículos resaltados", progLivros:"Progreso por libro",
    marcacoes:"Versículos resaltados", semMarcas:"Aún no hay versículos resaltados. Toca un versículo y elige un color.", verTodas:"Ver todas",
    perguntaDia:"Pregunta del día", breveCat:"Catecismo Menor (1647)", lerCatecismo:"Ver en el catecismo", pergAbrev:"P.", domingo:"Domingo", domingos:"domingos", memorizar:"Memorizar", verResposta:"Mostrar respuesta",
    planosTit:"Planes de lectura", tempoTit:"Cronología", atlasTit:"Atlas bíblico", atlasDica:"ej.: Jericó, Betel, Corinto",
    atlasFonte:"Lugares: openbible.info Bible Geocoding (CC-BY) · Mapa: dibujado por Sola con datos de Natural Earth (dominio público) y relieve de Terrain Tiles (AWS Open Data)",
    lugarIncerto:"Ubicación incierta: los estudiosos no concuerdan dónde estaba (openbible.info).", ocorrencias:"aparición(es) en la Biblia",
    primeira:"Primera", ultima:"Última", distancias:"Distancias aproximadas", verFoto:"Ver foto (Wikimedia Commons)", semLeitura:"Marca los capítulos como leídos al terminar y sigue aquí tu progreso.",
    contaLocal:"Tu estudio se guarda solo en este dispositivo. Para llevarlo a otro, usa Copia y Restaurar en “Mis notas”.",
    contaTitulo:"Continúa en cualquier dispositivo", contaTexto:"Entra para guardar notas, resaltados, capítulos leídos y planes en tu cuenta. Gratis y opcional.",
    entrarGoogle:"Entrar con Google", entrarEmail:"Recibir enlace por correo", linkEnviado:"Enviamos un enlace de acceso a", seuEmail:"tu correo",
    sair:"Salir", sincAgora:"Sincronizar ahora", sincIndo:"Sincronizando…", sincOk:"Todo guardado en tu cuenta",
    sincErro:"Sin conexión con la cuenta: los cambios quedan en este dispositivo y se suben después", entrou:"Entraste como", erroConta:"No se pudo conectar con la cuenta ahora. Inténtalo de nuevo.",
    contaOutra:"Este dispositivo tiene el estudio de otra cuenta. ¿Cambiarlo por el de la cuenta con la que acabas de entrar? Lo que no se había sincronizado de la otra cuenta se perderá.",
    excluirConta:"Eliminar mi cuenta", excluirConfirma:"¿Eliminar tu cuenta y todo lo guardado en ella en el servidor? No se puede deshacer. Lo que está en este dispositivo sigue aquí.",
    contaExcluida:"Cuenta eliminada. Lo que estaba en este dispositivo sigue aquí.",
    abaEstudo:"Estudio", abaPerfil:"Perfil", visitante:"Invitado", visitanteTexto:"Sin cuenta: tu estudio queda solo en este dispositivo.",
    desde:"En Sola desde", preferencias:"Preferencias", temaRot:"Apariencia", claro:"Claro", escuro:"Oscuro",
    seusDados:"Tus datos", lerOffline:"Leer sin conexión", privacidade:"Privacidad", faixaTexto:"Entra para guardar tu estudio.",
    vantagens:["Notas y versículos resaltados en todos tus dispositivos","Capítulos leídos y planes de lectura siempre al día","Continúa exactamente donde lo dejaste"],
    conviteSobre:"Tu estudio, siempre contigo", agoraNao:"Ahora no",
    instSobre:"Sola en el celular", instTit:"Instala Sola en la pantalla de inicio", instTexto:"Se abre como una aplicación, sin la barra del navegador, y los capítulos que ya leíste funcionan sin internet.", instBotao:"Instalar", instEntendi:"Entendido", instIos:"En Safari, toca <b>Compartir</b> (el cuadrado con la flecha) y luego <b>Agregar a inicio</b>.", instOutro:"En el menú del navegador (⋮ o ⋯), busca <b>Instalar aplicación</b> o <b>Agregar a la pantalla de inicio</b>.", instJa:"Sola ya está instalado en este dispositivo.",
    convites:{nota:"Tu nota está solo en este dispositivo", marca:"Tus resaltados están solo en este dispositivo", lido:"Guarda tu progreso", padrao:"Continúa donde lo dejaste"},
    conviteTexto:"Entra con Google para guardar notas, resaltados y capítulos leídos y continuar en cualquier dispositivo. Es gratis." },
};
const NAV = {
  pt:{meu:"Meu estudo",buscar:"Buscar",temas:"Temas",confissoes:"Confissões",dicionario:"Dicionário",planos:"Planos",tempo:"Linha do tempo",atlas:"Atlas",contexto:"Contexto",notas:"Anotações",ajuda:"Como usar",estudo:"Estante",mais:"Mais",prefs:"Tradução e idioma"},
  en:{meu:"My study",buscar:"Search",temas:"Topics",confissoes:"Confessions",dicionario:"Dictionary",planos:"Plans",tempo:"Timeline",atlas:"Atlas",contexto:"Context",notas:"Notes",ajuda:"How to use",estudo:"Study pane",mais:"More",prefs:"Translation and language"},
  es:{meu:"Mi estudio",buscar:"Buscar",temas:"Temas",confissoes:"Confesiones",dicionario:"Diccionario",planos:"Planes",tempo:"Cronología",atlas:"Atlas",contexto:"Contexto",notas:"Notas",ajuda:"Cómo usar",estudo:"Estante",mais:"Más",prefs:"Traducción e idioma"}
};
/* Guia "Como usar": grupos → [ação, ícone, título, texto]. A ação (mesma nos três idiomas) está em ACOES_AJUDA. */
const AJUDA = {
  pt:{ titulo:"Como usar o Sola", experimentar:"Experimentar",
    intro:"Tudo o que o Sola faz, em poucas linhas. Toque em “Experimentar” para ir direto à função. No celular, o que não cabe na barra do alto fica no botão “Mais”.",
    grupos:[
      ["Ler a Bíblia", [
        ["livros","livro","Escolher livro e capítulo","Toque no nome do livro no alto da tela. Também dá para digitar uma referência na busca (tecla /) ou na página inicial, como “Jo 3:16” ou “Sl 23”. Para mudar de capítulo, use as setas no rodapé (no computador, as setas ← → do teclado)."],
        ["traducoes","dicionario","Traduções e comparação","Leia na Bíblia Livre, na King James ou na Reina-Valera, e compare com outra tradução ou com o grego e o hebraico lado a lado. No computador, os seletores ficam acima do texto; no celular, no botão “Mais” (ou no Perfil)."],
        ["corrida","corrida","Leitura contínua","O botão de linhas no alto junta os versículos num texto corrido, como num livro, sem números no meio."],
        ["tema","lua","Tema claro e escuro","O botão da lua (ou do sol) alterna entre Papel Linho (claro) e Vigília (escuro). A escolha fica guardada no aparelho."],
        ["modoEstudo","estudo","Estante exegética","No computador, a estante ao lado do texto reúne quatro abas sincronizadas ao versículo clicado: Léxico & Original, Comentário, Confissão de Westminster & Referências, e sua Nota pessoal. O botão de mira no topo faz a estante acompanhar a leitura enquanto você rola o texto."],
        ["lido","feito","Marcar capítulo como lido","No fim de cada capítulo há o botão “Marcar capítulo como lido”. Os capítulos lidos aparecem marcados na lista e contam no seu progresso."]]],
      ["Estudar um versículo", [
        ["original","original","Original e Strong","Clique num versículo e abra “Original”: cada palavra do grego ou do hebraico aparece com a transliteração e a tradução literal. Toque na palavra para abrir o verbete do léxico de Strong."],
        ["comentario","comentario","Comentário","“Comentário” mostra João Calvino no versículo (em 47 livros) ou Matthew Henry, nos livros que Calvino não comentou. As referências citadas no meio do comentário são links: passe o mouse (ou toque) para ler o versículo sem sair do texto."],
        ["referencias","refs","Referências e Confissão","Nas telas largas, as referências principais já aparecem na margem esquerda de cada versículo (como na Bíblia de Genebra); abrir “Referências” mostra os textos completos, as doutrinas da Confissão de Westminster e onde os Catecismos de Westminster e a Confissão Belga citam o versículo."],
        ["palavras","temas","Palavras sublinhadas","Na Bíblia Livre, o traço cheio marca palavras-chave: toque para ver a palavra original e por que ela importa ali. O traço pontilhado explica palavras difíceis ou antigas. As duas camadas podem ser desligadas em Perfil."],
        ["contexto","contexto","Contexto do livro","O botão “Contexto” mostra autor, data, local, destinatários, tema e passagens paralelas do livro que você está lendo."]]],
      ["Pesquisar", [
        ["buscar","busca","Buscar no texto","Procure uma palavra ou frase na Bíblia toda ou só no livro aberto (atalho / ou Ctrl+K). A frase exata aparece primeiro; depois, os versículos com todas as palavras. Enquanto você digita, aparecem acima os temas, os trechos das confissões e catecismos, os verbetes do dicionário e as palavras do original que batem com o termo; a aba Confissões busca só no texto de todas as confissões e catecismos."],
        ["strong","original","Léxico de Strong","Busque direto por código (como G3056 ou H2617), palavra original, transliteração ou significado em português nas 14.197 entradas do léxico."],
        ["lexicoPaginas","original","Uma página para cada palavra, verbete e tema","Cada entrada do léxico tem uma página própria (como /lexico/grego/26/, ἀγάπη) com a definição, como a KJV e o interlinear a traduzem e todos os versículos onde aparece; o dicionário e os temas também (como /dicionario/alianca/ e /temas/fe/). Cada versículo também tem a sua (como /biblia/joao/3/16/), com as três traduções, o original, o começo do comentário e as referências. Abra pelo link “Página completa” ou “Página do verbete”."],
        ["temas","temas","Temas e doutrinas","Mais de 5.000 temas bíblicos (Nave), os 33 capítulos da Confissão de Fé de Westminster (1647), cada um com os textos de prova da própria Assembleia, e os credos antigos (Apostólico, Niceno, Atanásio e Calcedônia). Em “Todas as confissões e catecismos” estão também os Catecismos de Westminster, a Confissão Belga, o Catecismo de Heidelberg, os Cânones de Dort, as Confissões Batistas de Londres de 1644 e de 1689 e o Catecismo Batista."],
        ["dicionario","dicionario","Dicionário","Os verbetes do dicionário bíblico de Easton: pessoas, lugares, objetos e costumes."],
        ["tempo","tempo","Linha do tempo","Os grandes acontecimentos da Bíblia em ordem, da criação à igreja."],
        ["atlas","atlas","Atlas","Mais de 1.300 lugares bíblicos no mapa e as viagens missionárias de Paulo."]]],
      ["Seu estudo", [
        ["marcar","anotacoes","Marcar, anotar e compartilhar","Toque num versículo para marcá-lo com uma das quatro cores de lápis seco, escrever uma anotação, copiar o texto ou compartilhá-lo como imagem."],
        ["notas","anotacoes","Minhas anotações","Todas as suas anotações e marcações num só lugar, com o versículo de cada uma."],
        ["planos","planos","Planos de leitura","A Bíblia em um ano, o plano de M'Cheyne (4 leituras por dia, com o Novo Testamento e os Salmos duas vezes), o Novo Testamento em 90 dias, Salmos e Provérbios e os catecismos: Heidelberg em 52 Domingos, Breve Catecismo e Catecismo Batista em 52 semanas (as perguntas e respostas abrem no próprio plano; o botão Memorizar esconde as respostas para você tentar lembrar antes de ver). O Sola lembra em que dia você está. Na página inicial, a pergunta do dia percorre o Breve Catecismo."],
        ["meu","progresso","Meu estudo","Seu perfil (nome, avatar, capa, versículo de vida), que você pode compartilhar como imagem, a semana de leitura com meta, as últimas 12 semanas, conquistas, a sua prateleira de livros (teologia, filosofia, vida cristã, literatura), o progresso por livro e as marcações. Em Perfil › Personalizar, escolha o tamanho da letra, a confissão em destaque e quais seções aparecem. Funciona sem conta; com conta, dá também para publicar uma página pública do perfil (solabiblia.com.br/perfil/seu-nome)."],
        ["conta","pessoa","Conta e backup","Entrar com o Google é opcional: serve para levar anotações, marcações e progresso para outros aparelhos. Sem conta, tudo fica neste aparelho, e você pode salvar um backup em arquivo em Perfil."],
        ["offline","baixar","Ler sem internet","Os capítulos que você abre ficam guardados. Em “Sobre o projeto” dá para baixar a Bíblia inteira para ler sem sinal."],
        ["instalar","baixar","Instalar como aplicativo","No celular, o Sola fica na tela inicial e abre como um aplicativo, sem a barra do navegador. No Android, toque em “Instalar”; no iPhone, em Compartilhar › Adicionar à Tela de Início."],
        ["sugerir","anotacoes","Achou um erro? Sugira a correção","No léxico, no interlinear e no comentário há o link “Sugerir correção”: ele abre um e-mail já com o lugar, para você dizer o que está errado e como deveria ficar."]]]]},
  en:{ titulo:"How to use Sola", experimentar:"Try it",
    intro:"Everything Sola does, in a few lines. Tap “Try it” to go straight to each feature. On a phone, whatever does not fit in the top bar is under “More”.",
    grupos:[
      ["Reading", [
        ["livros","livro","Choose a book and chapter","Tap the book name at the top. You can also type a reference in search (press /) or on the home page, like “John 3:16”. To change chapters, use the arrows at the bottom (on a computer, the ← → keys)."],
        ["traducoes","dicionario","Translations and comparison","Read the Bíblia Livre, the King James or the Reina-Valera, and compare with another translation or with the Greek and Hebrew side by side. On a computer the selectors are above the text; on a phone, under “More” (or in Profile)."],
        ["corrida","corrida","Continuous reading","The lines button at the top joins the verses into running text, like a book."],
        ["tema","lua","Light and dark theme","The moon (or sun) button switches colors. Your choice is saved on this device."],
        ["modoEstudo","estudo","Study pane","On desktop, the side study pane gathers four tabs synced to the verse you click: Lexicon & Original, Commentary, Westminster Confession & Cross-refs, and your personal Note. The target button at the top makes the pane follow your reading as you scroll."],
        ["lido","feito","Mark a chapter as read","At the end of each chapter there is a “Mark chapter as read” button. Read chapters are marked in the list and count toward your progress."]]],
      ["Studying a verse", [
        ["original","original","Original and Strong","Tap a verse and choose “Original”: every Greek or Hebrew word with transliteration and a literal gloss. Tap a word to open its Strong’s lexicon entry."],
        ["comentario","comentario","Commentary","“Commentary” shows John Calvin on the verse (47 books) or Matthew Henry where Calvin did not comment. References cited in the commentary are links: hover (or tap) to read the verse without leaving the text."],
        ["referencias","refs","Cross-references","Key parallel passages appear in the left margin on wide screens; opening “Cross-refs” shows full verse previews and connected Reformed doctrines."],
        ["palavras","temas","Underlined words","In the Bíblia Livre, a solid line marks key words: tap to see the original word and why it matters. A dotted line explains hard or old words. Both layers can be turned off in Profile (Portuguese only)."],
        ["contexto","contexto","Book context","The “Context” button shows author, date, place, audience, theme and parallels for the book you are reading."]]],
      ["Searching", [
        ["buscar","busca","Text search","Search a word or phrase in the whole Bible or only the open book (shortcut / or Ctrl+K). Exact phrases come first. While you type, matching topics, passages from the confessions and catechisms, dictionary entries and original words appear above the verses; the Confessions tab searches only the (Portuguese) text of all the confessions and catechisms."],
        ["strong","original","Strong's Lexicon","Search directly by Strong code (such as G3056 or H2617), original lemma, transliteration or definition across all 14,197 entries."],
        ["lexicoPaginas","original","A page for every word, entry and topic","Each lexicon entry has its own page (such as /lexico/grego/26/, ἀγάπη) with the definition, how the KJV and the interlinear render it and every verse where it occurs; so do the dictionary and the topics (such as /dicionario/alianca/ and /temas/fe/). Every verse has one too (such as /biblia/joao/3/16/), with the three translations, the original, the start of the commentary and the cross-references. All in Portuguese; open them from the “Full page” or “Entry page” link."],
        ["temas","temas","Topics and doctrines","Over 5,000 Bible topics (Nave), the 33 chapters of the Westminster Confession of Faith (1647), each with the Assembly's own proof texts, and the ancient creeds (Apostles', Nicene, Athanasian and Chalcedon). The confessions page also has the Westminster Catechisms, the Belgic Confession, the Heidelberg Catechism, the Canons of Dort, the 1644 and 1689 London Baptist Confessions and the Baptist Catechism (in Portuguese)."],
        ["dicionario","dicionario","Dictionary","Easton’s Bible Dictionary: people, places, objects and customs."],
        ["tempo","tempo","Timeline","The great events of the Bible in order, from creation to the church."],
        ["atlas","atlas","Atlas","Over 1,300 Bible places on the map and Paul’s missionary journeys."]]],
      ["Your study", [
        ["marcar","anotacoes","Highlight, note and share","Tap a verse to highlight it in one of four colors, write a note, copy it or share it as an image."],
        ["notas","anotacoes","My notes","All your notes and highlights in one place, each with its verse."],
        ["planos","planos","Reading plans","The Bible in a year, M'Cheyne's plan (4 readings a day, with the New Testament and the Psalms twice), the New Testament in 90 days, Psalms and Proverbs, and the catechisms: Heidelberg in 52 Lord's Days, the Shorter Catechism and the Baptist Catechism in 52 weeks (the questions and answers open right in the plan; the Memorize button hides the answers so you can try to recall them first). Sola remembers your day. On the home page, the question of the day goes through the Shorter Catechism."],
        ["meu","progresso","My study","Your profile (name, avatar, cover, life verse), your reading week with a goal, the last 12 weeks, achievements, your bookshelf (theology, philosophy, Christian life, literature), a shareable profile image, progress by book and highlights. In Profile › Customize, pick the text size, the featured confession and which sections show. Works without an account; with one, you can also publish a public profile page (solabiblia.com.br/perfil/your-name)."],
        ["conta","pessoa","Account and backup","Signing in with Google is optional: it carries notes, highlights and progress to your other devices. Without an account everything stays on this device, and you can save a backup file in Profile."],
        ["offline","baixar","Offline reading","Chapters you open are kept. In “About” you can download the whole Bible."],
        ["instalar","baixar","Install as an app","On your phone, Sola can sit on the home screen and open like an app, without the browser bar. On Android, tap “Install”; on iPhone, Share › Add to Home Screen."],
        ["sugerir","anotacoes","Found a mistake? Suggest a correction","In the lexicon, the interlinear and the commentary there is a “Suggest a correction” link: it opens an e-mail with the place already filled in, so you can say what is wrong."]]]]},
  es:{ titulo:"Cómo usar Sola", experimentar:"Probar",
    intro:"Todo lo que hace Sola, en pocas líneas. Toca “Probar” para ir directo a cada función. En el celular, lo que no cabe en la barra de arriba está en “Más”.",
    grupos:[
      ["Leer la Biblia", [
        ["livros","livro","Elegir libro y capítulo","Toca el nombre del libro arriba. También puedes escribir una referencia en la búsqueda (tecla /) o en el inicio, como “Juan 3:16”. Para cambiar de capítulo, usa las flechas de abajo (en la computadora, las teclas ← →)."],
        ["traducoes","dicionario","Traducciones y comparación","Lee la Bíblia Livre, la King James o la Reina-Valera, y compara con otra traducción o con el griego y el hebreo lado a lado. En la computadora los selectores están sobre el texto; en el celular, en el botón “Más” (o en Perfil)."],
        ["corrida","corrida","Lectura continua","El botón de líneas arriba une los versículos en texto corrido, como un libro."],
        ["tema","lua","Tema claro y oscuro","El botón de la luna (o del sol) cambia los colores. La elección queda guardada en el dispositivo."],
        ["modoEstudo","estudo","Estante de estudio","En computadora, el estante lateral reúne cuatro pestañas sincronizadas al versículo seleccionado: Léxico y Original, Comentario, Confesión de Westminster y Referencias, y tu Nota. El botón de mira arriba hace que el estante siga tu lectura mientras te desplazas."],
        ["lido","feito","Marcar capítulo como leído","Al final de cada capítulo está el botón “Marcar capítulo como leído”. Los capítulos leídos aparecen marcados y cuentan en tu progreso."]]],
      ["Estudiar un versículo", [
        ["original","original","Original y Strong","Toca un versículo y elige “Original”: cada palabra del griego o del hebreo con transliteración y traducción literal. Toca la palabra para abrir el léxico de Strong."],
        ["comentario","comentario","Comentario","“Comentario” muestra a Juan Calvino (47 libros) o a Matthew Henry donde Calvino no comentó. Las referencias citadas en el comentario son enlaces: pasa el ratón (o toca) para leer el versículo sin salir del texto."],
        ["referencias","refs","Referencias cruzadas","Las referencias principales aparecen en el margen izquierdo en pantallas anchas; abrir “Referencias” muestra los pasajes completos y las doctrinas conectadas."],
        ["palavras","temas","Palabras subrayadas","En la Bíblia Livre, la línea continua marca palabras clave y la punteada explica palabras difíciles (en portugués). Se pueden desactivar en Perfil."],
        ["contexto","contexto","Contexto del libro","El botón “Contexto” muestra autor, fecha, lugar, destinatarios, tema y paralelos del libro."]]],
      ["Buscar", [
        ["buscar","busca","Buscar en el texto","Busca una palabra o frase en toda la Biblia o solo en el libro abierto (atajo / o Ctrl+K). La frase exacta aparece primero. Mientras escribes, aparecen arriba los temas, pasajes de las confesiones y catecismos, entradas del diccionario y palabras del original que coinciden; la pestaña Confesiones busca solo en el texto (en portugués) de todas las confesiones y catecismos."],
        ["strong","original","Léxico de Strong","Busca directamente por código (como G3056 o H2617), lema original, transliteración o definición en las 14.197 entradas del léxico."],
        ["lexicoPaginas","original","Una página por palabra, entrada y tema","Cada entrada del léxico tiene su propia página (como /lexico/grego/26/, ἀγάπη) con la definición, cómo la traducen la KJV y el interlineal y todos los versículos donde aparece; también el diccionario y los temas (como /dicionario/alianca/ y /temas/fe/). Cada versículo también tiene la suya (como /biblia/joao/3/16/), con las tres traducciones, el original, el inicio del comentario y las referencias. Todo en portugués; ábrelas desde el enlace “Página completa” o “Página de la entrada”."],
        ["temas","temas","Temas y doctrinas","Más de 5.000 temas bíblicos (Nave), los 33 capítulos de la Confesión de Fe de Westminster (1647), con los textos de prueba de la propia Asamblea, y los credos antiguos (Apostólico, Niceno, Atanasio y Calcedonia), en portugués. En la página de confesiones están también los Catecismos de Westminster, la Confesión Belga, el Catecismo de Heidelberg, los Cánones de Dort, las Confesiones Bautistas de Londres de 1644 y de 1689 y el Catecismo Bautista."],
        ["dicionario","dicionario","Diccionario","El diccionario bíblico de Easton: personas, lugares, objetos y costumbres."],
        ["tempo","tempo","Cronología","Los grandes acontecimientos de la Biblia en orden, de la creación a la iglesia."],
        ["atlas","atlas","Atlas","Más de 1.300 lugares bíblicos en el mapa y los viajes misioneros de Pablo."]]],
      ["Tu estudio", [
        ["marcar","anotacoes","Resaltar, anotar y compartir","Toca un versículo para resaltarlo en uno de cuatro colores, anotar, copiarlo o compartirlo como imagen."],
        ["notas","anotacoes","Mis notas","Todas tus notas y resaltados en un solo lugar, con su versículo."],
        ["planos","planos","Planes de lectura","La Biblia en un año, el plan de M'Cheyne (4 lecturas por día, con el Nuevo Testamento y los Salmos dos veces), el Nuevo Testamento en 90 días, Salmos y Proverbios y los catecismos: Heidelberg en 52 domingos, Catecismo Menor y Catecismo Bautista en 52 semanas (las preguntas y respuestas se abren en el propio plan; el botón Memorizar oculta las respuestas para que intentes recordarlas antes). Sola recuerda tu día. En la página de inicio, la pregunta del día recorre el Catecismo Menor."],
        ["meu","progresso","Mi estudio","Tu perfil (nombre, avatar, portada, versículo de vida), tu semana de lectura con meta, las últimas 12 semanas, logros, tu estantería de libros (teología, filosofía, vida cristiana, literatura), una imagen del perfil para compartir, el progreso por libro y los resaltados. En Perfil › Personalizar, elige el tamaño de letra, la confesión destacada y qué secciones aparecen. Funciona sin cuenta; con cuenta, también puedes publicar una página pública del perfil (solabiblia.com.br/perfil/tu-nombre)."],
        ["conta","pessoa","Cuenta y copia de seguridad","Entrar con Google es opcional: lleva notas, resaltados y progreso a tus otros dispositivos. Sin cuenta todo queda en este dispositivo, y puedes guardar una copia en archivo en Perfil."],
        ["offline","baixar","Leer sin internet","Los capítulos que abres quedan guardados. En “Acerca de” puedes descargar la Biblia entera."],
        ["instalar","baixar","Instalar como aplicación","En el celular, Sola puede quedar en la pantalla de inicio y abrirse como una aplicación, sin la barra del navegador. En Android, toca “Instalar”; en iPhone, Compartir › Agregar a inicio."],
        ["sugerir","anotacoes","¿Encontraste un error? Sugiere la corrección","En el léxico, el interlineal y el comentario hay un enlace “Sugerir corrección”: abre un correo con el lugar ya indicado, para que digas qué está mal."]]]]}
};
const ACOES_AJUDA = {
  livros: ()=>{ montarListaLivros(); alternarPainel("painelLivros", true); },
  traducoes: ()=>innerWidth > 700 ? irPara("JHN", 1, 1) : abrirMais(),   // no celular os seletores ficam no "Mais"
  corrida: ()=>irPara("PSA", 23),
  tema: ()=>{ est.tema = est.tema==="escuro" ? "claro" : "escuro"; gravarLS("logos_tema", est.tema); aplicarTema(); },
  modoEstudo: ()=>{ fecharPaineis(); est.estudo = true; gravarLS("logos_estudo", true); aplicarEstudo(); if(est.vista!=="cap") irPara("JHN", 1, 1); else atualizarEstudo(est.versoEstudo || 1); },
  lido: ()=>irPara("PSA", 23),
  original: ()=>irPara("JHN", 1, 1, "original"),
  lexicoPaginas: ()=>{ location.href = "/lexico/grego/26/"; },
  comentario: ()=>irPara("ROM", 8, 28, "comentario"),
  referencias: ()=>irPara("JHN", 3, 16, "referencias"),
  palavras: ()=>irPara("PSA", 51, 10),
  contexto: ()=>abrirContexto(),
  buscar: ()=>abrirBusca("texto"),
  strong: ()=>abrirBusca("strong"),
  temas: ()=>abrirBusca("temas"),
  dicionario: ()=>abrirBusca("dicionario"),
  tempo: ()=>{ montarTempo(); alternarPainel("painelTempo", true); },
  atlas: ()=>abrirAtlas(),
  marcar: ()=>irPara("JHN", 3, 16),
  notas: ()=>{ montarNotas(); alternarPainel("painelNotas", true); },
  planos: ()=>{ montarPlanos(null); alternarPainel("painelPlanos", true); },
  meu: ()=>abrirMeuEstudo("estudo"),
  conta: ()=>abrirMeuEstudo("perfil"),
  offline: ()=>alternarPainel("painelSobre", true),
  instalar: ()=>mostrarInstalar(true),
  sugerir: ()=>irPara("MIC", 6, 8, "original"),
};
function montarAjuda(){
  const a = AJUDA[est.idioma] || AJUDA.pt;
  $("tituloAjuda").textContent = a.titulo;
  $("conteudoAjuda").innerHTML = `<p class="painel-texto">${a.intro}</p>` + a.grupos.map(([g, itens])=>
    `<h3 class="painel-sub">${g}</h3><div class="ajuda-grade">` + itens.map(([acao, icone, tit, txt])=>
      `<div class="ajuda-item">${ico(icone)}<div><h4>${tit}</h4><p>${txt}</p>` +
      (ACOES_AJUDA[acao] ? `<button class="ajuda-ir" data-acao="${acao}">${a.experimentar} ${ico("seta")}</button>` : "") +
      `</div></div>`).join("") + `</div>`).join("");
  $("conteudoAjuda").querySelectorAll(".ajuda-ir").forEach(b=>b.addEventListener("click", ()=>{
    alternarPainel("painelAjuda", false);
    ACOES_AJUDA[b.dataset.acao]();
  }));
}
function abrirAjuda(){ montarAjuda(); alternarPainel("painelAjuda", true); }
const CORES = ["ouro","verde","azul","rosa"];
/* Os mesmos grupos estão em ferramentas/gerar_paginas.py (página inicial que o Google lê). */
const GRUPOS = [
  ["AT","pentateuco",["GEN","EXO","LEV","NUM","DEU"]],
  ["AT","historicos",["JOS","JDG","RUT","1SA","2SA","1KI","2KI","1CH","2CH","EZR","NEH","EST"]],
  ["AT","poeticos",["JOB","PSA","PRO","ECC","SNG"]],
  ["AT","maiores",["ISA","JER","LAM","EZK","DAN"]],
  ["AT","menores",["HOS","JOL","AMO","OBA","JON","MIC","NAM","HAB","ZEP","HAG","ZEC","MAL"]],
  ["NT","evangelhos",["MAT","MRK","LUK","JHN","ACT"]],
  ["NT","paulo",["ROM","1CO","2CO","GAL","EPH","PHP","COL","1TH","2TH","1TI","2TI","TIT","PHM"]],
  ["NT","gerais",["HEB","JAS","1PE","2PE","1JN","2JN","3JN","JUD","REV"]],
];
const VERSOS_DIA = [["PSA",119,105],["JHN",3,16],["ROM",8,28],["PSA",23,1],["ISA",40,31],["PHP",4,6],["PRO",3,5],["MAT",11,28],
  ["ROM",5,8],["2TI",3,16],["HEB",4,12],["JOS",1,9],["PSA",46,1],["ISA",41,10],["JHN",14,6],["ROM",12,2],["EPH",2,8],["GAL",2,20],
  ["PSA",19,7],["LAM",3,22],["MIC",6,8],["MAT",6,33],["JHN",1,14],["1JN",4,19],["ROM",1,16],["PSA",1,2],["COL",3,16],["HEB",11,1],
  ["JAS",1,5],["1PE",1,25],["REV",21,4],["ISA",53,5],["PSA",27,1],["JHN",8,32],["2CO",5,17],["PHP",1,6],["PSA",34,8],["DEU",6,5],
  ["ROM",11,36],["JHN",17,17]];
/* Destaques diários do léxico original para a Mesa de Estudo inicial: [strong, usfm, cap, v, lema, translit, glosa, nota] */
const PALAVRAS_DIA = [
  ["G3056","JHN",1,1,"λόγος","lógos","Palavra, Verbo","No prólogo de João, não é uma força impessoal, mas a eterna autoexpressão pessoal de Deus que estava com Deus, é Deus e se fez carne em Cristo."],
  ["H2617","PSA",136,1,"חֶסֶד","ḥeseḏ","Amor leal, bondade","Mais que afeto passageiro, descreve a fidelidade firme de quem se comprometeu por aliança e jamais abandona a sua promessa."],
  ["H1254","GEN",1,1,"בָּרָא","bārāʾ","Criar","Em toda a Bíblia hebraica, este verbo no sentido de criar tem exclusivamente Deus como sujeito: fazer surgir o universo, um povo e um coração novo."],
  ["G4637","JHN",1,14,"σκηνόω","skēnóō","Habitar, armar tenda","Literalmente “armar tabernáculo”: assim como a glória do Senhor habitava na tenda no deserto, o Filho eterno veio morar entre nós."],
  ["H3722","LEV",16,30,"כָּפַר","kāpar","Fazer expiação","Cobrir a culpa pagando o preço que afasta o juízo por meio de um sacrifício substituto — cumprido de uma vez por todas na cruz."],
  ["G5485","EPH",2,8,"χάρις","cháris","Graça","O favor livre e imerecido de Deus concedido a quem merecia condenação — a fonte inteira da eleição, redenção e fé."],
  ["H1285","GEN",17,7,"בְּרִית","bᵉrîṯ","Aliança, pacto","Pacto solene firmado por Deus com promessas e juramento: o fio condutor que une Abraão, Moisés, Davi e o sangue da nova aliança."],
  ["G1343","ROM",3,21,"δικαιοσύνη","dikaiosýnē","Justiça","Em Paulo, tanto a retidão perfeita do caráter de Deus quanto a justiça de Cristo imputada pela fé ao pecador justificado."],
  ["H7965","ISA",53,5,"שָׁלוֹם","šālôm","Paz, plenitude","Não apenas ausência de guerra, mas integridade completa e reconciliação restaurada entre o pecador e o Deus santo."],
  ["G2435","ROM",3,25,"ἱλαστήριον","hilastḗrion","Propiciatório","O mesmo termo da Septuaginta para a tampa da arca onde o sangue era aspergido: Cristo satisfaz a justiça divina e afasta a ira."]
];
const ABREV_CURTA = {GEN:"Gn",EXO:"Êx",LEV:"Lv",NUM:"Nm",DEU:"Dt",JOS:"Js",JDG:"Jz",RUT:"Rt","1SA":"1Sm","2SA":"2Sm","1KI":"1Rs","2KI":"2Rs",
  "1CH":"1Cr","2CH":"2Cr",EZR:"Ed",NEH:"Ne",EST:"Et",JOB:"Jó",PSA:"Sl",PRO:"Pv",ECC:"Ec",SNG:"Ct",ISA:"Is",JER:"Jr",LAM:"Lm",EZK:"Ez",
  DAN:"Dn",HOS:"Os",JOL:"Jl",AMO:"Am",OBA:"Ob",JON:"Jn",MIC:"Mq",NAM:"Na",HAB:"Hc",ZEP:"Sf",HAG:"Ag",ZEC:"Zc",MAL:"Ml",MAT:"Mt",
  MRK:"Mc",LUK:"Lc",JHN:"Jo",ACT:"At",ROM:"Rm","1CO":"1Co","2CO":"2Co",GAL:"Gl",EPH:"Ef",PHP:"Fp",COL:"Cl","1TH":"1Ts","2TH":"2Ts",
  "1TI":"1Tm","2TI":"2Tm",TIT:"Tt",PHM:"Fm",HEB:"Hb",JAS:"Tg","1PE":"1Pe","2PE":"2Pe","1JN":"1Jo","2JN":"2Jo","3JN":"3Jo",JUD:"Jd",REV:"Ap"};
/* abreviações usuais em português, para "jo 3 16", "sl 23", "1co 13" na busca */
const ABREV = {gn:"GEN",ex:"EXO",lv:"LEV",nm:"NUM",dt:"DEU",js:"JOS",jz:"JDG",rt:"RUT","1sm":"1SA","2sm":"2SA","1rs":"1KI","2rs":"2KI",
  "1cr":"1CH","2cr":"2CH",ed:"EZR",ne:"NEH",et:"EST",sl:"PSA",sal:"PSA",pv:"PRO",ec:"ECC",ct:"SNG",is:"ISA",jr:"JER",lm:"LAM",ez:"EZK",
  dn:"DAN",os:"HOS",jl:"JOL",am:"AMO",ob:"OBA",jn:"JON",mq:"MIC",na:"NAM",hc:"HAB",sf:"ZEP",ag:"HAG",zc:"ZEC",ml:"MAL",mt:"MAT",
  mc:"MRK",lc:"LUK",jo:"JHN",at:"ACT",rm:"ROM","1co":"1CO","2co":"2CO",gl:"GAL",ef:"EPH",fp:"PHP",fl:"PHP",cl:"COL","1ts":"1TH","2ts":"2TH",
  "1tm":"1TI","2tm":"2TI",tt:"TIT",fm:"PHM",hb:"HEB",tg:"JAS","1pe":"1PE","2pe":"2PE","1jo":"1JN","2jo":"2JN","3jo":"3JN",jd:"JUD",ap:"REV",apoc:"REV"};
const CACHE_DADOS = "sola-dados-v1";   // o mesmo nome está no sw.js
/* Contas (opcionais): endereço e chave pública ("publishable"/anon) do projeto no Supabase — ver ferramentas/supabase.sql.
   `google` e `email` ligam cada forma de entrar (o link por e-mail exige SMTP próprio configurado no Supabase).
   Com `url` vazio, ou com as duas formas desligadas, nada de conta aparece e o site funciona como sempre,
   só neste aparelho. O Google fica desligado até o provedor estar configurado no painel do Supabase. */
const CONTA = { url:"https://rxmxxuyqvetbkjfilayc.supabase.co", chave:"sb_publishable_l4W4kfy9e24ajcdxKNtGFA_yIBhqbY-", google:true, email:false };

/* ---------- estado ---------- */
const est = {
  meta:null, idioma:"pt", traducao:"blivre", comparar:"",
  vista:"inicio", livro:"JHN", cap:1, alvoV:0, abrir:null, tema:"claro",
  marcas: lerLS("logos_marcas", {}), notas: lerLS("logos_notas", {}),
  corrida: lerLS("logos_corrida", false), estudo: lerLS("logos_estudo", true), progresso: lerLS("logos_planos", {}),
  metaSemana: +lerLS("logos_meta_semana", 0) || 0,
  perfil: lerLS("logos_perfil", {}), prateleira: lerLS("logos_prateleira", {}),         // perfil personalizável                       // meta de capítulos por semana (0 = sem meta)
  lidos: lerLS("logos_lidos", {}),                                       // capítulos lidos: {"JHN.3": quando}
  chave: lerLS("logos_chave", true), voc: lerLS("logos_voc", true),       // as duas camadas de palavras sublinhadas
  cachePalavras:{}, palavrasCap:null,
  sinc: Object.assign({ pend:{}, cursor:null, conta:null, ultima:0 }, lerLS("logos_sinc", null)),   // o que falta subir para a conta
  sb:null, sessao:null, sincEstado:"",
  cacheBiblia:{}, cacheComent:{}, cacheInter:{}, cacheLex:{}, cacheRefs:{}, cacheTemas:{}, cacheDic:{}, titulosPT:{}, enderecosAcervo:{}, doutrinas:null,
  livrosCom:null, idxTemas:null, idxDic:null, aliasPT:null, planos:null, tempo:null, ctx:null,
  lugares:null, mapa:null, marcadores:[], viagens:null, camadaViagem:[],
  versos:[], versoAtivo:null, versoEstudo:1, estudoAba:"original", chaveEstudo:null, filtroCanone:"todos",
  gaveta:null, buscaModo:"texto", vez:0, vezBusca:0, focoAntes:null,
};
function lerLS(k, padrao){ try{ return JSON.parse(localStorage.getItem(k)) ?? padrao; }catch(e){ return padrao; } }
function gravarLS(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){} }
function t(){ return UI[est.idioma]; }
const $ = (id)=>document.getElementById(id);
function esc(s){ return String(s ?? "").replace(/[&<>"']/g, (c)=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
const normStr = (s)=>s.normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();
const emPT = ()=>est.idioma==="pt";
const ico = (nome)=>`<svg class="ico" aria-hidden="true"><use href="#i-${nome}"/></svg>`;

/* ---------- dados ---------- */
/* Versão de cada grupo de dados (data/versoes.json, gerado por ferramentas/gerar_paginas.py). O endereço leva
   ?v=<versão>: quando um arquivo muda, o endereço muda, e nenhum cache (nem um service worker antigo) entrega a
   cópia velha junto com o app novo. Grupo = a pasta do arquivo, ou o próprio arquivo nos dois primeiros níveis. */
let VERSOES = {};
function urlDados(url){
  const rel = url.replace(/^\/?data\//, "");
  if(rel === url) return url;
  const p = rel.split("/"), v = VERSOES[p.length >= 3 ? p.slice(0, -1).join("/") : rel];
  return "/data/" + rel + (v ? "?v=" + v : "");
}
async function carregarVersoes(){
  try{ const r = await fetch("/data/versoes.json", { cache: "no-cache" }); if(r.ok) VERSOES = await r.json(); }catch(e){}
}
async function json(url){ const r = await fetch(urlDados(url)); if(!r.ok) throw new Error(url); return r.json(); }
/* Guarda no cache o que deu certo; o que falhou (sem rede) pode ser pedido de novo. */
async function comCache(cache, chave, url){
  if(!(chave in cache)){
    try{ cache[chave] = await json(url); }
    catch(e){ return null; }
  }
  return cache[chave];
}
const carregarLivro = (trad, usfm)=>comCache(est.cacheBiblia, trad+"/"+usfm, `data/bibles/${trad}/${usfm}.json`);
/* Palavras sublinhadas (data/palavras, gerado por ferramentas/gerar_palavras.py). As posições valem para o texto da
   Bíblia Livre, então só aparecem nela. Duas camadas: palavras-chave [início, fim, "H1254", nota de contexto?] e
   vocabulário [início, fim, "v:covado", strong?]. O índice traz "lemas", "termos", "orig" e os livros com arquivo. */
const ehVoc = (m)=>String(m[2]).startsWith("v:");
async function carregarPalavras(usfm, cap){
  if((!est.chave && !est.voc) || est.traducao !== "blivre" || est.corrida) return null;
  const idx = await comCache(est.cachePalavras, "indice", "data/palavras/indice.json");
  if(!idx || !idx.livros.includes(usfm)) return null;
  const livro = await comCache(est.cachePalavras, usfm, `data/palavras/${usfm}.json`);
  return (livro && livro[cap]) || null;
}
const carregarRefs = (usfm, cap)=>comCache(est.cacheRefs, usfm+"/"+cap, `data/crossrefs/${usfm}/${cap}.json`);
const carregarInterlinear = (usfm, cap)=>comCache(est.cacheInter, usfm+"/"+cap, `data/interlinear/${usfm}/${cap}.json`);
const carregarLexico = (letra)=>comCache(est.cacheLex, letra, `data/strongs/${letra}.json`);
/* Comentário do capítulo: Calvino nos livros que ele comentou; nos outros, Matthew Henry.
   Devolve {versículo: texto, __autor: "calvin"|"henry", __pt?: true} ou null. */
async function carregarComentario(usfm, cap){
  const pt = emPT();
  const chave = (pt?"pt/":"") + usfm+"/"+cap;
  if(!(chave in est.cacheComent)){
    const livros = await livrosComentario();
    const autor = autorDoLivro(livros, usfm);
    let base = null, trad = null;
    if(autor){
      try{ base = await json(`data/commentaries/${autor}/${usfm}/${cap}.json`); }catch(e){}
      if(pt){ try{ trad = await json(`data/commentaries/${autor}/pt/${usfm}/${cap}.json`); }catch(e){} }
    }
    const com = base && trad ? Object.assign({}, base, trad) : base;
    if(com) com.__autor = autor;
    est.cacheComent[chave] = com;
  }
  return est.cacheComent[chave];
}
async function livrosComentario(){
  if(!est.livrosCom){
    const ler = async (a)=>{ try{ return (await json(`data/commentaries/${a}/manifest.json`)).books; }catch(e){ return []; } };
    const [calvin, henry] = await Promise.all([ler("calvin"), ler("henry")]);
    est.livrosCom = { calvin, henry };
  }
  return est.livrosCom;
}
function autorDoLivro(livros, usfm){ return livros.calvin.includes(usfm) ? "calvin" : livros.henry.includes(usfm) ? "henry" : null; }
function autorComentario(com, x){ return com && com.__autor === "henry" ? x.autorHenry : x.autorCalvin; }
function comentarioProximo(com, v){
  if(!com) return null;
  if(com[String(v)]) return { v: v, texto: com[String(v)] };
  let antes = 0, depois = Infinity;
  for(const k of Object.keys(com)){
    const n = +k;
    if(k.startsWith("__") || isNaN(n)) continue;
    if(n < v && n > antes) antes = n;
    if(n > v && n < depois) depois = n;
  }
  if(antes) return { v: antes, texto: com[String(antes)] };
  if(depois < Infinity) return { v: depois, texto: com[String(depois)], seguinte: true };
  return null;
}
async function idxTemas(){ if(!est.idxTemas){ est.idxTemas = await json("data/topics/index.json"); } return est.idxTemas; }
async function doutrinas(){
  if(!est.doutrinas){ try{ est.doutrinas = await json("data/topics/doutrinas.json"); }catch(e){ est.doutrinas = []; } }
  return est.doutrinas;
}
/* Onde as confissões e os catecismos citam cada versículo (data/confissoes/citacoes/<LIVRO>.json, gerado pelo
   gerar_paginas.py com os textos de prova): {cap: {v: [[rótulo, endereço, trecho]]}}. A Confissão de Westminster
   fica de fora da lista porque já aparece completa no cartão da doutrina. */
async function citacoesDoVerso(usfm, cap, v){
  est.cacheCit = est.cacheCit || {};
  if(!(usfm in est.cacheCit)){ try{ est.cacheCit[usfm] = await json(`data/confissoes/citacoes/${usfm}.json`); }catch(e){ est.cacheCit[usfm] = {}; } }
  return ((est.cacheCit[usfm][String(cap)] || {})[String(v)] || []).filter(c=>!c[1].startsWith("/confissoes/westminster/"));
}
function htmlCitacoes(cits, x){
  if(!cits.length) return "";
  const mostrar = cits.slice(0, window.innerWidth < 1060 ? 4 : 6);
  return `<div class="estante-cartao confessional"><p class="dout-selo">${x.citSelo}</p>` +
    mostrar.map(([rot, url, trecho])=>`<div class="cit-item"><a class="cit-rot" href="${esc(url)}">${esc(rot)}</a>
      ${trecho ? `<p class="cm-nota">${esc(trecho)}</p>` : ""}</div>`).join("") +
    (cits.length > mostrar.length ? `<p class="estudo-vazio">${x.citMais.replace("{n}", cits.length - mostrar.length)}</p>` : "") +
    `<p class="fonte">${x.citFonte}</p></div>`;
}
async function idxDic(){ if(!est.idxDic){ est.idxDic = await json("data/dictionary/index.json"); } return est.idxDic; }
async function aliasPT(){ if(!est.aliasPT){ try{ est.aliasPT = await json("data/topics/aliases_pt.json"); }catch(e){ est.aliasPT = {}; } } return est.aliasPT; }
async function secaoPT(cache, pasta, letra){
  const k = (emPT()?"pt/":"") + letra;
  if(!cache[k]){
    try{ cache[k] = await json(`data/${pasta}/${k}.json`); }
    catch(e){ cache[k] = await json(`data/${pasta}/${letra}.json`); }
  }
  return cache[k];
}
const temaSecao = (letra)=>secaoPT(est.cacheTemas, "topics", letra);
const dicLetra = (letra)=>secaoPT(est.cacheDic, "dictionary", letra);
async function titulos(tipo){
  if(!(tipo in est.titulosPT)){
    try{ est.titulosPT[tipo] = await json(`data/${tipo}/titulos_pt.json`); }
    catch(e){ est.titulosPT[tipo] = {}; }
  }
  return est.titulosPT[tipo];
}
async function contextos(){ if(!est.ctx){ est.ctx = await json("data/context.json"); } return est.ctx; }

/* ---------- livros, endereços e rotas ---------- */
function infoLivro(usfm){ return est.meta.books.find(b=>b.id===usfm); }
function nomeLivro(usfm){ const b = infoLivro(usfm); return b ? (b[est.idioma] || b.pt) : usfm; }
function refStr(usfm, cap, v){ return `${nomeLivro(usfm)} ${cap}:${v}`; }
function slugLivro(usfm){ return normStr(infoLivro(usfm).pt).replace(/\s+/g,"-"); }
function livroPorSlug(slug){ return est.meta.books.find(b=>slugLivro(b.id)===slug); }
function urlLivro(usfm){ return `/biblia/${slugLivro(usfm)}/`; }
function urlCapitulo(usfm, cap, v){ return `/biblia/${slugLivro(usfm)}/${cap}/` + (v ? "#v"+v : ""); }
function grupoDe(usfm){ return GRUPOS.find(g=>g[2].includes(usfm)); }
/* Link para um capítulo ou versículo: é um <a> de verdade (abre em nova aba, funciona sem o app)
   e, dentro do app, o clique é interceptado em iniciar() para navegar sem recarregar. */
function linkRef(usfm, cap, v, rotulo, classe){
  return `<a class="${classe ?? "tema-ref"}" href="${urlCapitulo(usfm, cap, v)}">${rotulo ?? esc(nomeLivro(usfm)+" "+cap+(v ? ":"+v : ""))}</a>`;
}
/* Lê um endereço e devolve a rota: {vista:"inicio"} | {vista:"livro",livro} | {vista:"cap",livro,cap,v} | {vista:"perfil",apelido}
   | {vista:"inicio", plano, dia} (/planos/...)
   | null (não é do app). */
function rotaDe(caminho, hash){
  const h = (hash||"").match(/^#\/([A-Z0-9]{3})\/(\d+)(?:\/(\d+))?/);   // links antigos: #/JHN/3
  if(h && infoLivro(h[1])) return { vista:"cap", livro:h[1], cap:Math.min(Math.max(+h[2],1), infoLivro(h[1]).ch), v:+h[3]||0 };
  const v = +((hash||"").match(/^#v(\d+)$/)||[])[1] || 0;
  let m = caminho.match(/^\/biblia\/([a-z0-9-]+)\/(\d+)\/?$/);
  if(m){ const b = livroPorSlug(m[1]); if(b && +m[2] >= 1 && +m[2] <= b.ch) return { vista:"cap", livro:b.id, cap:+m[2], v }; }
  // página de um versículo (/biblia/joao/3/16/): no app, abre o capítulo nele
  m = caminho.match(/^\/biblia\/([a-z0-9-]+)\/(\d+)\/(\d+)\/?$/);
  if(m){ const b = livroPorSlug(m[1]); if(b && +m[2] >= 1 && +m[2] <= b.ch) return { vista:"cap", livro:b.id, cap:+m[2], v:+m[3] }; }
  m = caminho.match(/^\/biblia\/([a-z0-9-]+)\/?$/);
  if(m){ const b = livroPorSlug(m[1]); if(b) return { vista:"livro", livro:b.id }; }
  m = caminho.match(/^\/perfil\/([a-z0-9][a-z0-9-]{1,28}[a-z0-9])\/?$/);   // página pública de um perfil
  if(m) return { vista:"perfil", apelido:m[1] };
  // planos: /planos/ (a lista), /planos/heidelberg/ e /planos/heidelberg/2/ (já no Domingo 2): o início com o painel aberto
  m = caminho.match(/^\/planos\/?(?:([a-z0-9-]+)\/?(?:(\d{1,3})\/?)?)?$/);
  if(m) return { vista:"inicio", plano: m[1] || "", dia: +m[2] || 0 };
  return caminho === "/" || caminho === "/index.html" ? { vista:"inicio" } : null;
}
function lerRota(){ return rotaDe(location.pathname, location.hash) || { vista:"inicio" }; }   // endereço desconhecido (404): início
function urlAtual(){
  return est.vista==="inicio" ? "/" : est.vista==="livro" ? urlLivro(est.livro) : est.vista==="perfil" ? urlPerfilPublico(est.apelidoPub)
    : urlCapitulo(est.livro, est.cap, est.alvoV);
}
function atualizarURL(substituir){
  const url = urlAtual();
  const primeira = !est.urlPronta;
  est.urlPronta = true;   // a partir da primeira renderização, cada página nova entra no histórico
  if(location.pathname + location.hash === url) return;
  history[primeira || substituir ? "replaceState" : "pushState"]({}, "", url);
}
function navegar(r, op){
  est.vista = r.vista;
  if(r.livro) est.livro = r.livro;
  if(r.vista==="perfil") est.apelidoPub = r.apelido;
  if(r.vista==="cap"){ est.cap = r.cap; est.alvoV = r.v || 0; est.abrir = r.abrir || null; }
  else { est.alvoV = 0; est.abrir = null; }
  const feito = renderizar(Object.assign({ nav:true }, op));
  if(r.plano !== undefined) feito.then(()=>abrirPlano(r.plano, r.dia));
  return feito;
}
function irPara(usfm, cap, v, abrir){ return navegar({ vista:"cap", livro:usfm, cap, v, abrir }); }

/* ---------- interface base ---------- */
const EABAS = { original:"eabaOrig", comentario:"eabaCom", referencias:"eabaRefs", anotacao:"eabaNota" };
function aplicarTextos(){
  const x = t();
  document.documentElement.lang = est.idioma==="pt" ? "pt-BR" : est.idioma;
  document.querySelectorAll("[data-nav] [data-label]").forEach(sp=>{
    const chave = sp.parentNode.dataset.nav;
    if(NAV[est.idioma][chave]) sp.textContent = NAV[est.idioma][chave];
  });
  $("lblComando").textContent = x.comandoBusca;
  $("estudoSelo").textContent = x.emEstudo;
  $("estudoCopiar").title = x.copiar;
  $("estudoCopiar").setAttribute("aria-label", x.copiar);
  $("estudoCompartilhar").title = x.compartilhar;
  $("estudoCompartilhar").setAttribute("aria-label", x.compartilhar);
  document.querySelectorAll("#abasEstante .eaba").forEach(b=>{
    const p = b.querySelector(".ponto");
    b.textContent = x[EABAS[b.dataset.eaba]];
    if(p) b.appendChild(p);
  });
  $("lblIdioma").textContent = x.idioma;
  $("lblTraducao").textContent = x.traducao;
  $("lblComparar").textContent = x.comparar;
  $("tituloLivros").textContent = x.livros;
  $("tituloBusca").textContent = x.buscar;
  $("tituloNotas").textContent = x.notas;
  $("lblBibliaToda").textContent = x.bibliaToda;
  $("tituloPlanos").textContent = x.planosTit;
  $("tituloTempo").textContent = x.tempoTit;
  $("tituloAtlas").textContent = x.atlasTit;
  $("campoAtlas").placeholder = x.atlasDica;
  $("atlasFonte").textContent = x.atlasFonte;
  $("btnCorrida").title = x.leituraCorrida;
  document.querySelectorAll(".fechar").forEach(b=>b.setAttribute("aria-label", x.fechar));
  prepararAbas();
  ajustarNav();
}
function preencherTraducoes(){
  const doIdioma = est.meta.translations.filter(tr=>tr.lang===est.idioma);
  if(!doIdioma.find(tr=>tr.id===est.traducao)) est.traducao = doIdioma[0].id;
  $("selTraducao").innerHTML = doIdioma.map(tr=>`<option value="${tr.id}">${esc(tr.name)}</option>`).join("");
  $("selTraducao").value = est.traducao;
  const outras = est.meta.translations.filter(tr=>tr.id!==est.traducao);
  $("selComparar").innerHTML = `<option value="">${t().semComparar}</option>` +
    outras.map(tr=>`<option value="${tr.id}">${esc(tr.name)}</option>`).join("");
  if(!outras.find(tr=>tr.id===est.comparar)) est.comparar = "";
  $("selComparar").value = est.comparar;
}
const nomeTraducao = (id)=>est.meta.translations.find(tr=>tr.id===id).name;
const ornamento = `<div class="ornamento" aria-hidden="true"><i></i></div>`;

/* Desenha a página pedida. op: {substituir} troca o endereço sem criar histórico; {manter} não mexe na rolagem;
   {nav} = a pessoa navegou até aqui (vem de navegar()), e não um redesenho da mesma página. */
async function renderizar(op){
  op = op || {};
  const x = t();
  document.body.dataset.vista = est.vista;
  document.body.classList.toggle("corrida-ativa", est.corrida);
  if(!op.manter) fecharMais();   // mesma página (tradução, idioma): o menu "Mais" continua aberto
  ajustarNav();                  // Contexto e Modo estudo só existem na leitura: muda o que cabe na barra
  fecharPalavra();
  est.versoAtivo = null; est.gaveta = null;
  if(est.vista==="inicio"){
    renderizarInicio();
    $("lblLivroAtual").textContent = x.livros;
    document.title = "Sola — Estudo Bíblico";
  } else if(est.vista==="livro"){
    await renderizarLivro();
    $("lblLivroAtual").textContent = nomeLivro(est.livro);
    document.title = `${nomeLivro(est.livro)} — Sola`;
  } else if(est.vista==="perfil"){
    $("lblLivroAtual").textContent = x.livros;
    await renderizarPerfilPublico();
  } else {
    await renderizarCapitulo(op);
    $("lblLivroAtual").textContent = `${nomeLivro(est.livro)} ${est.cap}`;
    document.title = `${nomeLivro(est.livro)} ${est.cap} — Sola`;
    // "onde parei" só muda quando a pessoa vai a um capítulo, não quando a tela é redesenhada (senão um aparelho
    // parado numa página desfaria o "continuar" que acabou de chegar de outro aparelho)
    const ult = lerLS("logos_ultimo", null);
    if(op.nav && (!ult || ult.livro !== est.livro || ult.cap !== est.cap)){
      gravarLS("logos_ultimo", { livro: est.livro, cap: est.cap });
      tocar("estado", "ultimo");
      est.capsVisita = (est.capsVisita || 0) + 1;
      if(est.capsVisita >= 3) convidar("padrao");   // terceiro capítulo da visita
      if(est.capsVisita >= 2) convidarInstalar();   // não aparece se o da conta já apareceu nesta visita
    }
  }
  atualizarURL(op.substituir);
  if(est.vista!=="cap" && !op.manter && est.pronto) window.scrollTo({ top:0, behavior:"instant" });
  est.pronto = true;
}

/* ---------- página inicial: Mesa de Estudo ---------- */
/* Atalho para os símbolos de fé na página inicial, por tradição (as mesmas páginas de /confissoes/; o mesmo bloco está no
   gerar_paginas.py, na página inicial que o Google lê). */
const CONF_INICIO = [[["credos", "IV–VIII"]], [["westminster", "1647"], ["catecismo-maior", "1647"], ["breve-catecismo", "1647"]],
  [["confissao-belga", "1561"], ["heidelberg", "1563"], ["canones-de-dort", "1619"]], [["confissao-batista-1644", "1644"], ["confissao-batista-1689", "1689"], ["catecismo-batista", "1693"]]];
function htmlConfInicio(x){
  return `<section class="conf-inicio"><div class="conf-cabeca"><div><h2>${x.confTit}</h2><p>${x.confTexto}</p></div>
    <a class="cm-acao" href="/confissoes/">${x.confTodas} ${ico("seta")}</a></div><div class="conf-grupos">` +
    CONF_INICIO.map((docs, i)=>`<div class="conf-grupo"><h3>${x.confGrupos[i]}</h3>` + docs.map(([id, ano])=>
      `<a href="/confissoes/${id}/">${esc(x.confNomes[id])}<span>${ano}</span></a>`).join("") + `</div>`).join("") + `</div></section>`;
}
function renderizarInicio(){
  const x = t(), ult = lerLS("logos_ultimo", null);
  const temUlt = ult && infoLivro(ult.livro) && ult.cap >= 1 && ult.cap <= infoLivro(ult.livro).ch;
  const icones = ["original","comentario","refs","temas","atlas","planos"];
  const resumo = resumoEstudo(), nLidos = resumo.lidos;
  const hoje = new Date(), dia = Math.floor(Date.UTC(hoje.getFullYear(), hoje.getMonth(), hoje.getDate()) / 864e5);
  const [l, c, v] = VERSOS_DIA[dia % VERSOS_DIA.length];
  const [pStrong, pl, pc, pv, pLema, pTranslit, pGlosa, pNota] = PALAVRAS_DIA[dia % PALAVRAS_DIA.length];
  const pDir = pStrong[0] === "H" ? 'dir="rtl" lang="he"' : 'lang="grc"';
  const testamento = (tst)=>`<section class="testamento${est.filtroCanone!=="todos" && est.filtroCanone!==tst ? " oculto" : ""}" data-tst="${tst}"><h2>${tst==="AT" ? x.at : x.nt}</h2>${ornamento}
    <div class="grupos">` + GRUPOS.filter(g=>g[0]===tst).map(g=>
      `<div class="grupo-livros"><h3>${x.grupos[g[1]]}</h3>` + g[2].map(id=>
        `<a href="${urlLivro(id)}">${esc(nomeLivro(id))}<span>${infoLivro(id).ch}</span></a>`).join("") + `</div>`).join("") +
    `</div></section>`;
  $("leitor").innerHTML = `<div class="inicio">
    <section class="mesa-cabeca">
      <div class="mesa-topo">
        <div>
          <p class="mesa-sobre">${x.heroiSobre}</p>
          <h1>${x.heroiTitulo}</h1>
          <p class="mesa-texto">${x.heroiTexto}</p>
        </div>
        <div class="mesa-acao-col">
          <form class="mesa-busca" id="formInicio" role="search">
            <input id="campoInicio" type="search" placeholder="${x.heroiCampo}" aria-label="${x.buscar}" autocomplete="off">
            <button type="submit">${x.buscar}</button>
          </form>
          <div class="mesa-acoes">
            ${temUlt ? `<a class="btn-ouro" href="${urlCapitulo(ult.livro, ult.cap)}">${x.continuar} ${esc(nomeLivro(ult.livro))} ${ult.cap} ${ico("seta")}</a>` : ""}
            <a class="${temUlt ? "btn-linha" : "btn-ouro"}" href="${urlCapitulo("JHN", 1)}">${x.comecar}</a>
          </div>
          <div class="mesa-atalhos">
            <button type="button" id="btnAjudaInicio">${ico("ajuda")} ${(AJUDA[est.idioma] || AJUDA.pt).titulo}</button>
            ${nLidos ? `<button type="button" id="btnEstudoInicio">${ico("progresso")} ${x.meuEstudo}: ${nLidos} ${nLidos === 1 ? x.capLido1 : x.capsLidos}${resumo.seq > 1 ? ` · ${resumo.seq} ${x.diasSeguidos}` : ""}</button>` : ""}
          </div>
        </div>
      </div>
    </section>
    <section class="mesa-grade">
      <article class="cartao-mesa">
        <div>
          <p class="cm-rotulo">${x.versoDia}</p>
          <blockquote id="versoDia"></blockquote>
          <div id="versoDiaRef"></div>
        </div>
        <div class="cm-rodape">
          <span>${nLidos ? `${nLidos} ${nLidos === 1 ? x.capLido1 : x.capsLidos}${resumo.seq > 1 ? ` · ${resumo.seq} ${x.diasSeguidos}` : ""}` : esc(nomeTraducao(est.traducao))}</span>
          <button type="button" class="cm-acao" id="btnPlanoInicio">${x.iniciarPlano} ${ico("seta")}</button>
        </div>
      </article>
      <article class="cartao-mesa">
        <div>
          <p class="cm-rotulo">${x.palavraDia} <span>${pStrong[0] === "H" ? "HEBRAICO" : "GREGO"}</span></p>
          <div class="cm-palavra-topo">
            <span class="cm-lemma" ${pDir}>${esc(pLema)}</span>
            <span class="cm-translit">${esc(pTranslit)}</span>
            <span class="cm-strong">${esc(pStrong)}</span>
          </div>
          <h3 class="cm-glosa">${esc(pGlosa)}</h3>
          <p class="cm-nota">${esc(pNota)}</p>
        </div>
        <div class="cm-rodape">
          <span>${esc(refStr(pl, pc, pv))}</span>
          <button type="button" class="cm-acao" id="btnPalavraDia">${x.examinarVerso} ${ico("seta")}</button>
        </div>
      </article>
      <article class="cartao-mesa">
        <div>
          <p class="cm-rotulo">${x.doutSelo} <span id="doutDiaFonte">CFW 1</span></p>
          <h3 class="cm-titulo" id="doutDiaTit">Somente a Escritura (Sola Scriptura)</h3>
          <p class="cm-nota" id="doutDiaRes">A Bíblia é a Palavra de Deus escrita e a única regra infalível de fé e de vida; tudo o que é necessário para a salvação e para agradar a Deus está nela.</p>
        </div>
        <div class="cm-rodape">
          <span id="doutDiaRef">${esc(refStr("2TI", 3, 16))}</span>
          <button type="button" class="cm-acao" id="btnDoutDia">${x.verDoutrina} ${ico("seta")}</button>
        </div>
      </article>
      <article class="cartao-mesa">
        <div>
          <p class="cm-rotulo">${x.perguntaDia} <span id="catDiaN"></span></p>
          <h3 class="cm-titulo" id="catDiaP"></h3>
          <p class="cm-nota" id="catDiaR"></p>
        </div>
        <div class="cm-rodape">
          <span>${x.breveCat}</span>
          <a class="cm-acao" id="catDiaLink" href="/confissoes/breve-catecismo/">${x.lerCatecismo} ${ico("seta")}</a>
        </div>
      </article>
    </section>
    <section class="recursos">` + x.recursos.map((r,i)=>
      `<button type="button" class="recurso" data-recurso="${i}">${ico(icones[i])}<div><h3>${r[0]}</h3><p>${r[1]}</p></div></button>`).join("") +
    `</section>
    ${htmlConfInicio(x)}
    <section class="canone">
      <div class="canone-cabeca">
        <h2>${x.indiceCanonico}</h2>
        <div class="canone-abas" role="tablist">
          <button type="button" data-canone="todos" class="${est.filtroCanone==="todos"?"ativa":""}">${x.todosLivros} (66)</button>
          <button type="button" data-canone="AT" class="${est.filtroCanone==="AT"?"ativa":""}">${x.at} (39)</button>
          <button type="button" data-canone="NT" class="${est.filtroCanone==="NT"?"ativa":""}">${x.nt} (27)</button>
        </div>
      </div>
      ${testamento("AT")}${testamento("NT")}
    </section></div>`;
  const dicaInicio = document.createElement("div");
  dicaInicio.className = "dica-ref-linha"; dicaInicio.setAttribute("aria-live", "polite");
  $("formInicio").after(dicaInicio);
  ligarDicaRef($("campoInicio"), dicaInicio);
  $("formInicio").addEventListener("submit", (e)=>{
    e.preventDefault();
    const termo = $("campoInicio").value.trim();
    if(!termo) return;
    const r = parseRef(termo);
    if(r && r.cap) return irParaRef(r);
    if(parseStrong(termo)){ abrirBusca("strong"); $("campoBusca").value = termo; return buscar(); }
    abrirBusca("texto"); $("chkBibliaToda").checked = true; $("campoBusca").value = termo; buscar();
  });
  if($("btnEstudoInicio")) $("btnEstudoInicio").addEventListener("click", ()=>abrirMeuEstudo("estudo"));
  $("btnAjudaInicio").addEventListener("click", abrirAjuda);
  $("btnPlanoInicio").addEventListener("click", ()=>{ montarPlanos(null); alternarPainel("painelPlanos", true); });
  $("btnPalavraDia").addEventListener("click", ()=>irPara(pl, pc, pv, "original"));
  let doutDia = null;
  $("btnDoutDia").addEventListener("click", ()=>doutDia ? abrirDoutrina(doutDia) : abrirBusca("temas"));
  document.querySelectorAll(".canone-abas button").forEach(b=>b.addEventListener("click", ()=>{
    est.filtroCanone = b.dataset.canone;
    document.querySelectorAll(".canone-abas button").forEach(o=>o.classList.toggle("ativa", o===b));
    document.querySelectorAll(".canone .testamento").forEach(sec=>{
      sec.classList.toggle("oculto", est.filtroCanone !== "todos" && sec.dataset.tst !== est.filtroCanone);
    });
  }));
  const acoes = [()=>irPara("JHN",1,1,"original"), ()=>irPara("ROM",8,28,"comentario"), ()=>irPara("JHN",3,16,"referencias"),
    ()=>abrirBusca("temas"), abrirAtlas, ()=>{ montarPlanos(null); alternarPainel("painelPlanos", true); }];
  document.querySelectorAll(".recurso").forEach(b=>b.addEventListener("click", acoes[+b.dataset.recurso]));
  // versículo e doutrina do dia: os mesmos para todos, mudam à meia-noite
  const vez = ++est.vez;
  carregarLivro(est.traducao, l).then(livro=>{
    if(vez !== est.vez || !$("versoDia")) return;
    const texto = livro && livro[c-1] && livro[c-1][v-1];
    if(!texto) return;
    $("versoDia").textContent = `“${texto}”`;
    $("versoDiaRef").innerHTML = linkRef(l, c, v, `${esc(refStr(l, c, v))} ${ico("seta")}`, "cm-ref");
  });
  // pergunta do dia: o Breve Catecismo inteiro (107 perguntas) volta ao começo a cada 107 dias
  json("data/confissoes/breve-catecismo.json").then(doc=>{
    if(vez !== est.vez || !$("catDiaP") || !doc.itens.length) return;
    const q = doc.itens[dia % doc.itens.length], en = est.idioma === "en";
    $("catDiaN").textContent = `${x.pergAbrev} ${q.n}`;
    $("catDiaP").textContent = en ? q.p_en : q.p;
    $("catDiaR").textContent = encurtar((en ? q.r_en : q.r).replace(/\s*\[\d+\]/g, ""), 280);
    $("catDiaLink").href = `/confissoes/breve-catecismo/${q.n}/`;
  }).catch(()=>{});
  doutrinas().then(douts=>{
    if(vez !== est.vez || !douts.length || !$("doutDiaTit")) return;
    const d = doutDia = douts[dia % douts.length];
    $("doutDiaFonte").textContent = d.f.split(";")[0].trim();
    $("doutDiaTit").textContent = doutTitulo(d);
    $("doutDiaRes").textContent = encurtar(doutResumo(d), 260);
    const v0 = d.sec && d.sec[0] && d.sec[0].v && d.sec[0].v[0];
    if(v0) $("doutDiaRef").textContent = refStr(v0[0], v0[1], v0[2]);
  });
}

/* ---------- página do livro ---------- */
async function renderizarLivro(){
  const x = t(), vez = ++est.vez, info = infoLivro(est.livro), g = grupoDe(est.livro);
  const idx = est.meta.books.indexOf(info), ant = est.meta.books[idx-1], pro = est.meta.books[idx+1];
  const [ctx, livros] = await Promise.all([contextos().catch(()=>({})), livrosComentario()]);
  if(vez !== est.vez) return;
  const c = ctx[est.livro], autor = autorDoLivro(livros, est.livro);
  const caps = Array.from({length:info.ch}, (_,i)=>`<a href="${urlCapitulo(est.livro, i+1)}"${foiLido(est.livro, i+1) ? ` class="lido" title="${x.lido}"` : ""}>${i+1}</a>`).join("");
  $("leitor").innerHTML = `<div class="livro-pagina">
    <header class="cap-cabeca">
      <p class="cap-sobre"><a href="/">${info.t==="AT" ? x.at : x.nt}</a> · ${x.grupos[g[1]]}</p>
      <h1 class="titulo-cap">${esc(nomeLivro(est.livro))}</h1>${ornamento}
      <p class="sub-cap">${info.ch} ${x.capitulos}${autor ? ` · ${x.comentarioDe}: ${autorComentario({__autor:autor}, x).split(" (")[0]}` : ""}</p>
    </header>
    ${c ? `<div class="livro-ficha">${fichaContexto(c)}</div>` : ""}
    <h2>${x.capitulos}</h2>
    <nav class="caps" aria-label="${x.capitulos}">${caps}</nav>
    <div class="livro-vizinhos">
      ${ant ? `<a href="${urlLivro(ant.id)}">‹ ${esc(nomeLivro(ant.id))}</a>` : "<span></span>"}
      ${pro ? `<a href="${urlLivro(pro.id)}">${esc(nomeLivro(pro.id))} ›</a>` : "<span></span>"}
    </div></div>`;
}
function fichaContexto(c){
  const x = t();
  c = Object.assign({}, c, (!emPT() && c[est.idioma]) || {});
  const par = (c.par||[]).map(([l,ch])=>linkRef(l, ch)).join(" · ");
  return `<dl class="ctx-grade">
    <dt>${x.autor}</dt><dd>${esc(c.a)}</dd>
    <dt>${x.data}</dt><dd>${esc(dataLocal(c.d))}</dd>
    <dt>${x.local}</dt><dd>${esc(c.l)}</dd>
    <dt>${x.publico}</dt><dd>${esc(c.p)}</dd>
    <dt>${x.tema}</dt><dd>${esc(c.t)}</dd>
    ${par ? `<dt>${x.paralelos}</dt><dd>${par}</dd>` : ""}
  </dl>
  <div class="ctx-barra"><i style="left:${+c.pos||0}%"></i></div>
  <div class="ctx-escala">${x.escala.map(e=>`<span>${e}</span>`).join("")}</div>`;
}

/* ---------- leitura ---------- */
const bancadaAtiva = ()=>est.vista === "cap" && est.estudo && !est.corrida && window.innerWidth >= 1060;
const abrevLivro = (u)=>(emPT() && ABREV_CURTA[u]) || nomeLivro(u).slice(0, 3);

async function renderizarCapitulo(op){
  op = op || {};
  const x = t(), leitor = $("leitor"), vez = ++est.vez;
  const info = infoLivro(est.livro);
  if(est.cap > info.ch || est.cap < 1) est.cap = 1;
  leitor.classList.add("carregando");
  const [livro, livroComp, palavras, refsCap] = await Promise.all([
    carregarLivro(est.traducao, est.livro),
    est.comparar ? carregarLivro(est.comparar, est.livro) : null,
    carregarPalavras(est.livro, est.cap),
    est.corrida ? null : carregarRefs(est.livro, est.cap),
  ]);
  if(vez !== est.vez) return;   // o leitor já pediu outra página enquanto esta carregava
  leitor.classList.remove("carregando");
  const g = grupoDe(est.livro);
  let html = `<header class="cap-cabeca">
      <p class="cap-sobre"><a href="/">${info.t==="AT" ? x.at : x.nt}</a> · <a href="${urlLivro(est.livro)}">${x.grupos[g[1]]}</a></p>
      <h1 class="titulo-cap">${esc(nomeLivro(est.livro))} ${est.cap}</h1>${ornamento}
      <p class="sub-cap"><span>${esc(nomeTraducao(est.traducao))}${est.comparar ? " · " + esc(nomeTraducao(est.comparar)) : ""}</span>
        <button class="btn-contexto" id="btnCtxCap">${x.contexto}</button>
        <a class="btn-contexto" href="${urlLivro(est.livro)}">${x.todosCaps}</a></p>
    </header>`;
  if(!livro){
    leitor.innerHTML = html + `<p class="erro-leitura">${x.erroCarregar}<br><br><button class="btn-ouro" id="btnTentar">${x.tentar}</button></p>`;
    $("btnTentar").addEventListener("click", ()=>renderizar({ manter:true }));
    $("btnCtxCap").addEventListener("click", abrirContexto);
    atualizarNav();
    return;
  }
  const versos = est.versos = livro[est.cap-1] || [];
  est.palavrasCap = palavras;
  const versosComp = livroComp ? (livroComp[est.cap-1]||[]) : null;
  if(!(op.manter && est.versoEstudo >= 1 && est.versoEstudo <= versos.length)){
    est.versoEstudo = (est.alvoV >= 1 && est.alvoV <= versos.length) ? est.alvoV : 1;
    est.chaveEstudo = null;
  }
  if(est.corrida){
    html += `<p class="escritura corrida">` + versos.filter(Boolean).map(esc).join(" ") + `</p>`;
  } else {
    const ltr = !(est.traducao === "orig" && info.t === "AT");
    versos.forEach((texto, i)=>{
      if(!texto && !(versosComp && versosComp[i])) return;
      const v = i+1, chave = `${est.livro}.${est.cap}.${v}`;
      const marca = CORES.includes(est.marcas[chave]) ? " m-"+est.marcas[chave] : "";
      const comMargem = refsCap ? " com-margem" : "";
      const emEst = v === est.versoEstudo ? " em-estudo" : "";
      const temNota = est.notas[chave] ? `<span class="indicadores" title="${x.anotacao}">✎</span>` : "";
      let margem = "";
      if(refsCap){
        const lista = refsCap[String(v)] || [];
        const links = lista.slice(0, 2).map(r=>linkRef(r[0], r[1], r[2], esc(`${abrevLivro(r[0])} ${r[1]}:${r[2]}`), "mref")).join("") +
          (lista.length > 2 ? `<button type="button" class="mref-mais" data-v="${v}">+${lista.length - 2}</button>` : "");
        margem = `<aside class="margem-refs" aria-label="${x.referencias}">${links}</aside>`;
      }
      let corpoVerso;
      if(v === 1 && texto && ltr){
        const ini = /^["“«'‘¡¿]/.test(texto) ? 2 : 1;
        const conflito = (palavras && palavras[1] || []).some(m => (ehVoc(m) ? est.voc : est.chave) && m[0] < ini);
        corpoVerso = !conflito && texto.length > ini
          ? `<span class="capitular">${esc(texto.slice(0, ini))}</span>${textoVerso(texto, palavras && palavras[1], 1, ini)}`
          : `<sup>${v}</sup>${textoVerso(texto, palavras && palavras[v], v, 0)}`;
      } else {
        corpoVerso = `<sup>${v}</sup>${textoVerso(texto, palavras && palavras[v], v, 0)}`;
      }
      html += `<div class="verso${comMargem}${emEst}${marca}" id="v${v}" data-v="${v}" tabindex="0">
        ${margem}<p class="escritura">${corpoVerso}${temNota}</p>
        ${versosComp && versosComp[i] ? `<p class="comparado escritura">${esc(versosComp[i])}</p>` : ""}
        <div class="barra" role="toolbar" aria-label="${esc(refStr(est.livro, est.cap, v))}"></div>
        <div class="gavetas"></div>
      </div>`;
    });
  }
  leitor.innerHTML = html + botaoLido();
  ligarBotaoLido();
  if(est.capAberto !== est.livro + "." + est.cap){ est.capAberto = est.livro + "." + est.cap; est.capAbertoEm = Date.now(); }
  $("btnCtxCap").addEventListener("click", abrirContexto);
  leitor.querySelectorAll(".mref-mais").forEach(b=>b.addEventListener("click", (e)=>{
    e.stopPropagation();
    const v = +b.dataset.v, el = leitor.querySelector(`.verso[data-v="${v}"]`);
    if(el) acaoVerso(el, v, "referencias");
  }));
  leitor.querySelectorAll(".verso").forEach(el=>{
    // com uma gaveta aberta, passar o mouse por outro versículo não troca o ativo (senão a gaveta fecha sozinha)
    // logo depois de chegar por um link, o mouse parado em cima de outro versículo também não rouba o destaque
    el.addEventListener("mouseenter", (e)=>{
      montarBarra(el);
      // no toque, o navegador manda este evento antes do clique: se o dedo está numa palavra-chave, ativar o
      // versículo aqui mexeria na página e o clique cairia fora da palavra
      if(matchMedia("(hover:none)").matches && (document.elementFromPoint(e.clientX, e.clientY) || el).closest(".chave")) return;
      if(!est.gaveta && Date.now() > (est.semHover||0)) ativarVerso(el, false);
    });
    el.addEventListener("focus", ()=>montarBarra(el));
    // tocar numa palavra-chave não leva o foco para ela: no celular a barra do versículo que tinha o foco sumiria
    // no meio do toque, o texto subiria e o clique cairia em outro lugar (pelo teclado, Tab continua chegando nela)
    el.addEventListener("mousedown", (e)=>{ if(e.target.closest(".chave")) e.preventDefault(); });
    el.addEventListener("click", (e)=>{
      if(e.target.closest(".barra,.gavetas,.margem-refs")) return;
      const chave = e.target.closest(".chave");
      if(chave) return bancadaAtiva() ? abrirPalavraEstante(chave) : abrirPalavra(chave);
      ativarVerso(el, true);
    });
    el.addEventListener("keydown", (e)=>{
      if(e.key !== "Enter" && e.key !== " ") return;
      if(e.target === el){ e.preventDefault(); ativarVerso(el, true); }
      else if(e.target.classList.contains("chave")){
        e.preventDefault();
        bancadaAtiva() ? abrirPalavraEstante(e.target) : abrirPalavra(e.target, true);
      }
    });
  });
  atualizarNav();
  const alvo = est.alvoV && leitor.querySelector(`.verso[data-v="${est.alvoV}"]`);
  if(alvo) irAoVerso(alvo, est.abrir);
  else {
    if(bancadaAtiva()) atualizarEstudo(est.versoEstudo);
    if(!op.manter && est.pronto) window.scrollTo({ top:0, behavior:"instant" });
  }
  est.abrir = null;
}
/* Texto do versículo com as palavras-chave sublinhadas. `inicio` permite destacar a capitular no v. 1 sem deslocar offsets. */
function textoVerso(texto, marcas, v, inicio){
  inicio = inicio || 0;
  if(!marcas) return esc(texto.slice(inicio));
  let html = "", pos = inicio;
  marcas.forEach((m, i)=>{
    if(m[0] < pos || m[1] > texto.length) return;    // arquivo fora de sincronia com o texto: fica sem sublinhado
    if(ehVoc(m) ? !est.voc : !est.chave) return;     // camada desligada no Perfil
    html += esc(texto.slice(pos, m[0])) +
      `<span class="chave${ehVoc(m) ? " voc" : ""}" role="button" tabindex="0" aria-haspopup="dialog" data-v="${v}" data-i="${i}">${esc(texto.slice(m[0], m[1]))}</span>`;
    pos = m[1];
  });
  return html + esc(texto.slice(pos));
}
function fecharPalavra(devolverFoco){
  const c = $("cartaoPalavra");
  const dona = document.querySelector(".chave.aberta");
  if(!c){
    if(dona && !bancadaAtiva()) dona.classList.remove("aberta");
    return false;
  }
  c.remove();
  if(dona){ dona.classList.remove("aberta"); if(devolverFoco) dona.focus({ preventScroll:true }); }
  return true;
}
function htmlOriginalBadge(num, o, tr){
  return `<span class="escritura lex-lemma" ${num[0] === "H" ? 'dir="rtl" lang="he"' : 'lang="grc"'}>${esc(o)}</span>
      <span class="lex-translit">${esc(tr)}</span><span class="lex-num">${esc(num)}</span>`;
}
/* De onde vem a nota (notas_fontes.json, via gerar_palavras.py): "Fontes: léxico…; CFW 11.1"; sem lista, o rótulo antigo. */
function htmlFontesNota(listas, padrao){
  const f = [...new Set(listas.flat().filter(Boolean))];
  return f.length ? `${t().fontesRot}: ${esc(f.join("; "))}` : padrao;
}
/* Cartão da palavra-chave (celular ou quando a estante lateral está fechada). */
function abrirPalavra(el, peloTeclado){
  const jaAberta = el.classList.contains("aberta") && !!$("cartaoPalavra");
  fecharPalavra();
  document.querySelectorAll(".chave.aberta").forEach(o=>o.classList.remove("aberta"));
  if(jaAberta) return;
  const idx = est.cachePalavras.indice, doVerso = est.palavrasCap && est.palavrasCap[el.dataset.v];
  const m = doVerso && doVerso[+el.dataset.i], voc = m && ehVoc(m);
  const lema = idx && m && (voc ? idx.termos && idx.termos[m[2]] : idx.lemas[m[2]]);
  if(!lema) return;
  const x = t(), verso = el.closest(".verso");
  const botaoOriginal = `<button class="btn-linha" id="cpOriginal">${ico("original")} ${x.chaveVer}</button>`;
  const c = document.createElement("aside");
  c.id = "cartaoPalavra"; c.className = "cartao-palavra" + (voc ? " voc" : "");
  c.setAttribute("role", "dialog");
  if(voc){
    const o = m[3] && idx.orig && idx.orig[m[3]];
    c.setAttribute("aria-label", `${el.textContent} — ${lema.s}`);
    c.innerHTML = `
      <div class="voc-topo"><span class="voc-palavra">${esc(lema.p || el.textContent)}</span>
        <button class="fechar" aria-label="${x.fechar}">×</button></div>
      <h4>${x.vocSig}</h4><p class="voc-sig">${esc(lema.s)}</p>
      ${lema.n ? `<p class="voc-nota">${esc(lema.n)}</p>` : ""}
      ${o ? `<div class="voc-orig"><span class="voc-rot">${x.vocOrig}</span> ${htmlOriginalBadge(m[3], o[0], o[1])}</div>` : ""}
      <div class="cp-pe">${o ? botaoOriginal : ""}<span class="fonte">${htmlFontesNota([lema.f || []], x.vocFonte)}</span></div>`;
  } else {
    c.setAttribute("aria-label", `${el.textContent} — ${lema.pt}`);
    c.innerHTML = `
      <div class="lex-topo">${htmlOriginalBadge(m[2], lema.o, lema.t)}
        <button class="fechar" aria-label="${x.fechar}">×</button></div>
      <p class="cp-trad"><span>${x.chaveTrad}</span> ${esc(lema.pt)}</p>
      ${m[3] ? `<h4>${x.chaveAqui}</h4><p>${esc(m[3])}</p>` : ""}
      ${lema.nota ? `<h4>${x.chavePalavra}</h4><p>${esc(lema.nota)}</p>` : ""}
      <div class="cp-pe">${botaoOriginal}<span class="fonte">${htmlFontesNota([m[4] || [], lema.nota ? lema.f || [] : []], x.chaveFonte)}</span></div>`;
  }
  document.body.appendChild(c);
  el.classList.add("aberta");
  const r = el.getBoundingClientRect(), alt = c.offsetHeight;
  if(matchMedia("(max-width:560px)").matches){
    const sobra = r.bottom + 16 - (innerHeight - alt - 12);
    if(sobra > 0) window.scrollBy({ top: sobra, behavior:"instant" });
  } else {
    const cabeAbaixo = r.bottom + alt + 18 < innerHeight || r.top - alt - 12 < document.querySelector(".topo").getBoundingClientRect().bottom;
    c.style.left = Math.max(12, Math.min(r.left, innerWidth - c.offsetWidth - 24)) + scrollX + "px";
    c.style.top = (cabeAbaixo ? r.bottom + 10 : r.top - alt - 10) + scrollY + "px";
    const passa = c.getBoundingClientRect().bottom + 12 - innerHeight;
    if(passa > 0) window.scrollBy({ top: passa, behavior:"instant" });
  }
  c.querySelector(".fechar").addEventListener("click", (e)=>fecharPalavra(e.detail === 0));
  if($("cpOriginal")) $("cpOriginal").addEventListener("click", ()=>{ fecharPalavra(); irAoVerso(verso, "original"); });
  if(peloTeclado) c.querySelector(".fechar").focus({ preventScroll:true });
}
/* Na bancada desktop, clicar numa palavra sublinhada abre a explicação dela direto na Estante Exegética, sem cobrir o texto. */
function abrirPalavraEstante(el){
  fecharPalavra();
  document.querySelectorAll(".chave.aberta").forEach(o=>o.classList.remove("aberta"));
  el.classList.add("aberta");
  const v = +el.dataset.v, i = +el.dataset.i;
  est.estudoAba = "original";
  est.versoEstudo = v;
  est.chaveEstudo = i;
  focarEstudo(v, true);
}
/* Rola até o versículo pedido (busca, referência cruzada, link com #v16), destaca e abre as ferramentas dele. */
function irAoVerso(el, abrir){
  est.semHover = Date.now() + 900;
  el.scrollIntoView({ block:"center", behavior:"instant" });
  el.classList.remove("destino"); void el.offsetWidth; el.classList.add("destino");
  if(abrir && bancadaAtiva() && ["original","comentario","referencias","anotacao"].includes(abrir)) est.estudoAba = abrir;
  ativarVerso(el, true);
  if(abrir && !bancadaAtiva()) acaoVerso(el, +el.dataset.v, abrir);
}

function focarEstudo(v, forcar, focarNota){
  const mudou = est.versoEstudo !== v;
  est.versoEstudo = v;
  if(mudou){
    est.chaveEstudo = null;
    document.querySelectorAll(".chave.aberta").forEach(o=>o.classList.remove("aberta"));
  }
  document.querySelectorAll(".verso.em-estudo").forEach(o=>o.classList.remove("em-estudo"));
  const alvo = document.querySelector(`.verso[data-v="${v}"]`);
  if(alvo) alvo.classList.add("em-estudo");
  if(bancadaAtiva() && (mudou || forcar || est.estudoAtual !== `${est.livro}.${est.cap}.${v}.${est.estudoAba}`))
    atualizarEstudo(v, focarNota);
}
function ativarVerso(el, toque){
  if(est.versoAtivo && est.versoAtivo!==el){ est.versoAtivo.classList.remove("ativo"); fecharGavetas(est.versoAtivo); }
  est.versoAtivo = el;
  el.classList.add("ativo");
  const topoFixo = document.querySelector(".topo").getBoundingClientRect().bottom;
  el.classList.toggle("barra-baixo", el.getBoundingClientRect().top < topoFixo + 28);
  montarBarra(el);
  if(toque) focarEstudo(+el.dataset.v);
}
function fecharGavetas(el){ const g = el.querySelector(".gavetas"); if(g) g.innerHTML=""; est.gaveta=null; }

function alternarMarcaVerso(v, cor){
  const chave = `${est.livro}.${est.cap}.${v}`;
  if(est.marcas[chave]===cor) delete est.marcas[chave]; else est.marcas[chave] = cor;
  gravarLS("logos_marcas", est.marcas); tocar("marca", chave);
  if(est.marcas[chave]) convidar("marca");
  const el = document.querySelector(`.verso[data-v="${v}"]`);
  if(el){
    CORES.forEach(o=>el.classList.toggle("m-"+o, est.marcas[chave]===o));
    el.querySelectorAll(".barra .cor").forEach(o=>{
      o.classList.toggle("sel", est.marcas[chave]===o.dataset.cor);
      o.setAttribute("aria-pressed", est.marcas[chave]===o.dataset.cor);
    });
  }
  if(v === est.versoEstudo){
    document.querySelectorAll("#estudoCores .cor").forEach(o=>{
      o.classList.toggle("sel", est.marcas[chave]===o.dataset.cor);
      o.setAttribute("aria-pressed", est.marcas[chave]===o.dataset.cor);
    });
  }
}
function salvarNotaVerso(v, texto){
  const x = t(), chave = `${est.livro}.${est.cap}.${v}`, valor = texto.trim();
  if(valor) est.notas[chave] = valor; else delete est.notas[chave];
  gravarLS("logos_notas", est.notas); tocar("nota", chave);
  const el = document.querySelector(`.verso[data-v="${v}"]`);
  if(el){
    let sinal = el.querySelector(".indicadores");
    if(valor && !sinal){
      sinal = document.createElement("span");
      sinal.className = "indicadores"; sinal.title = x.anotacao; sinal.textContent = "✎";
      el.querySelector("p.escritura").appendChild(sinal);
    } else if(!valor && sinal) sinal.remove();
  }
  if(valor) convidar("nota");
  if(v === est.versoEstudo) sinalizarAbasEstante(v);
}

function montarBarra(el){
  const v = +el.dataset.v, chave = `${est.livro}.${est.cap}.${v}`, x = t();
  const barra = el.querySelector(".barra");
  if(barra.dataset.pronta) return;
  barra.dataset.pronta = "1";
  barra.innerHTML =
    CORES.map(c=>`<button class="cor" data-cor="${c}" title="${x.marcar}: ${x.cores[c]}" aria-label="${x.marcar}: ${x.cores[c]}" style="background:var(--m-${c})"></button>`).join("") +
    `<span class="sep"></span>` +
    ["original","comentario","referencias","anotacao","copiar","compartilhar"].map(a=>
      `<button class="acao" data-acao="${a}">${x[a]}</button>`).join("");
  barra.querySelectorAll(".cor").forEach(b=>{
    b.classList.toggle("sel", est.marcas[chave]===b.dataset.cor);
    b.setAttribute("aria-pressed", est.marcas[chave]===b.dataset.cor);
    b.addEventListener("click", ()=>alternarMarcaVerso(v, b.dataset.cor));
  });
  barra.querySelectorAll(".acao").forEach(b=>b.addEventListener("click", ()=>acaoVerso(el, v, b.dataset.acao, b)));
}

async function copiarTexto(texto){
  try{ await navigator.clipboard.writeText(texto); return true; }
  catch(e){   // sem permissão ou navegador antigo: o jeito clássico
    const ta = document.createElement("textarea");
    ta.value = texto; ta.style.cssText = "position:fixed;opacity:0";
    document.body.appendChild(ta); ta.select();
    let ok = false; try{ ok = document.execCommand("copy"); }catch(e2){}
    ta.remove(); return ok;
  }
}
/* Grade palavra por palavra (gaveta "Original" e Estante Exegética). */
function gradeInterlinear(palavras, ehAT){
  return `<div class="inter-grid" ${ehAT?'dir="rtl"':''}>` + palavras.map(p=>
    `<button type="button" class="inter-palavra" data-strong="${esc(p[2]||"")}">
       <span class="ip-surf escritura" ${ehAT?'dir="rtl" lang="he"':'lang="grc"'}>${esc(p[0].replace(/\\/g, ""))}</span>
       <span class="ip-translit">${esc(p[1])}</span>
       <span class="ip-gloss">${esc(p[3])}</span>
       <span class="ip-strong">${esc(p[2]||"")}</span>
     </button>`).join("") + `</div><div class="lex-caixa oculto" aria-live="polite"></div>`;
}
function ligarLexico(alvo, completo, strongInicial){
  const x = t(), caixa = alvo.querySelector(".lex-caixa");
  if(!caixa) return;
  const mostrar = async (btn, rolar)=>{
    const strong = btn.dataset.strong;
    alvo.querySelectorAll(".inter-palavra").forEach(o=>o.classList.remove("sel"));
    const naEstante = !!alvo.closest("#estudoCorpo");
    if(!strong || (rolar && caixa.dataset.atual===strong && !caixa.classList.contains("oculto"))){
      caixa.classList.add("oculto"); caixa.dataset.atual="";
      if(naEstante) alvoEstudo(null);
      return;
    }
    btn.classList.add("sel");
    caixa.dataset.atual = strong;
    caixa.classList.remove("oculto");
    caixa.innerHTML = `<em>${x.carregando}</em>`;
    const lex = await carregarLexico(strong[0]);
    const ent = lex && lex[strong];
    if(caixa.dataset.atual !== strong) return;
    if(!ent){ caixa.innerHTML = ""; caixa.classList.add("oculto"); return; }
    if(naEstante) alvoEstudo(strong, ent.lemma);
    caixa.innerHTML = `
      <div class="lex-topo"><span class="escritura lex-lemma" ${strong[0]==="H"?'dir="rtl" lang="he"':'lang="grc"'}>${esc(ent.lemma)}</span>
        <span class="lex-translit">${esc(ent.translit)}</span>
        <span class="lex-num">${esc(strong)}</span></div>
      <p class="lex-def">${completo ? `<strong>${x.lexDef}:</strong> ` : ""}${esc((emPT() && ent.defpt) || ent.def)}</p>
      ${completo ? htmlUsosKjv(ent, x) : ""}
      ${htmlLinkLexico(strong, x)}
      <p class="lex-correcao">${linkCorrecao(`Léxico ${strong} (${ent.translit})`, x)}</p>`;
    if(rolar) caixa.scrollIntoView({ block:"nearest" });
  };
  alvo.querySelectorAll(".inter-palavra").forEach(btn=>btn.addEventListener("click", ()=>mostrar(btn, true)));
  if(strongInicial){
    const inicial = alvo.querySelector(`.inter-palavra[data-strong="${CSS.escape(strongInicial)}"]`);
    if(inicial) mostrar(inicial, false);
  }
}
function htmlMss(ehAT){
  return ehAT ? "" : `<div class="mss-abas">
      <button type="button" data-mss="tr">Textus Receptus</button>
      <button type="button" data-mss="byz">Bizantino</button>
      <button type="button" data-mss="diff">Diferenças</button>
    </div><div class="mss-alvo"></div>`;
}
function ligarMss(raiz, v){
  raiz.querySelectorAll(".mss-abas button").forEach(b=>b.addEventListener("click", async ()=>{
    const alvo = raiz.querySelector(".mss-alvo");
    const ativa = b.classList.contains("ativa");
    raiz.querySelectorAll(".mss-abas button").forEach(o=>o.classList.remove("ativa"));
    if(ativa){ alvo.innerHTML = ""; return; }
    b.classList.add("ativa");
    const [tr, byz] = await Promise.all([carregarLivro("orig", est.livro), carregarLivro("byz", est.livro)]);
    const tTR = tr && tr[est.cap-1] ? (tr[est.cap-1][v-1]||"") : "";
    const tBZ = byz && byz[est.cap-1] ? (byz[est.cap-1][v-1]||"") : "";
    const modo = b.dataset.mss;
    if(modo==="tr") alvo.innerHTML = `<p class="mss-texto" lang="grc"><span class="rot">Textus Receptus (1550)</span>${esc(tTR)}</p>`;
    else if(modo==="byz") alvo.innerHTML = `<p class="mss-texto" lang="grc"><span class="rot">Texto Bizantino (Robinson-Pierpont)</span>${esc(tBZ)}</p>`;
    else {
      const A = tTR.split(/\s+/), B = tBZ.split(/\s+/);
      const sA = new Set(B), sB = new Set(A);
      const marcar = (toks, outro)=>toks.map(w=>outro.has(w.replace(/[.,;·]/g,"")) || outro.has(w) ? esc(w) : `<mark>${esc(w)}</mark>`).join(" ");
      alvo.innerHTML = `<p class="mss-texto" lang="grc"><span class="rot">Textus Receptus</span>${marcar(A,sA)}</p>
        <p class="mss-texto" lang="grc"><span class="rot">Bizantino</span>${marcar(B,sB)}</p>`;
    }
  }));
}
/* "Sugerir correção": abre um e-mail já endereçado ao projeto, com o que é e onde está (o site não tem servidor;
   quem lê vira revisor). oQue vai no assunto; o corpo leva também o endereço da página. */
const EMAIL_PROJETO = "projetosolabiblia@gmail.com";
function linkCorrecao(oQue, x){
  const corpo = `${oQue}\n${location.href}\n\nO que está errado e como deveria ficar:\n\n`;
  return `<a class="sugerir" href="mailto:${EMAIL_PROJETO}?subject=${encodeURIComponent("Correção no Sola: " + oQue)}&body=${encodeURIComponent(corpo)}">${ico("anotacoes")} ${x.sugerir}</a>`;
}
function htmlComentarioCorpo(com, v, x, resumir){
  const achado = comentarioProximo(com, v);
  if(!achado){
    const lv = est.livrosCom || {calvin:[], henry:[]};
    return `<p class="comentario-texto">${autorDoLivro(lv, est.livro) ? x.semComentario : x.semLivroCalvin}</p>`;
  }
  const nota = achado.v !== v
    ? `<p class="aviso-idioma">${achado.seguinte ? x.comInicio : x.comRef} ${achado.v} ${achado.seguinte ? "" : x.comBloco}</p>` : "";
  const longo = resumir && achado.texto.length > 1400;
  const aviso = est.idioma==="en" ? "" : (com.__pt ? x.tradAuto : x.avisoIdiomaComentario);
  const henry = com.__autor === "henry" ? `<p class="aviso-idioma">${x.notaHenry}</p>` : "";
  return `${henry}${nota}<p class="comentario-texto${longo ? " recolhido" : ""}">${linkarRefsTexto(achado.texto)}</p>
    ${longo ? `<button type="button" class="ler-mais" aria-expanded="false">${x.lerMais}</button>` : ""}
    <p class="fonte">${x.fonte}: ${autorComentario(com, x)} · ${linkCorrecao(`Comentário, ${refStr(est.livro, est.cap, achado.v)}`, x)}</p>
    ${aviso ? `<p class="aviso-idioma">${aviso}</p>` : ""}`;
}
function ligarLerMais(raiz, x){
  const lm = raiz.querySelector(".ler-mais");
  if(lm) lm.addEventListener("click", ()=>{
    const antes = lm.getBoundingClientRect().top;
    const abrir = raiz.querySelector(".comentario-texto").classList.toggle("recolhido") === false;
    lm.textContent = abrir ? x.lerMenos : x.lerMais;
    lm.setAttribute("aria-expanded", abrir);
    // ao recolher, o texto encolhe acima do botão e a página "cai" lá para baixo: mantém o botão onde estava
    if(!abrir) window.scrollBy({ top: lm.getBoundingClientRect().top - antes, behavior: "instant" });
  });
}
function htmlRefsLista(lista, x){
  return `<div class="refs">` + lista.map((r,ri)=>{
    const rot = esc(`${nomeLivro(r[0])} ${r[1]}:${r[2]}${r[3]>r[2] ? "-"+r[3] : ""}`);
    return `<div class="ref-item">${linkRef(r[0], r[1], r[2], rot, "ref-ir")}<span class="ref-previa" data-ri="${ri}"></span></div>`;
  }).join("") + `</div><p class="fonte">${x.refFonte}</p>`;
}
function carregarPreviasRefs(raiz, lista){
  lista.forEach(async (r,ri)=>{
    const livro = await carregarLivro(est.traducao, r[0]);
    const alvo = raiz.querySelector(`.ref-previa[data-ri="${ri}"]`);
    if(alvo && livro && livro[r[1]-1] && livro[r[1]-1][r[2]-1]) alvo.textContent = livro[r[1]-1][r[2]-1];
  });
}

async function acaoVerso(el, v, acao, botao){
  const x = t(), chave = `${est.livro}.${est.cap}.${v}`;
  const gavetas = el.querySelector(".gavetas");
  if(acao==="compartilhar"){
    const rot = botao ? botao.textContent : "";
    if(botao) botao.textContent = x.gerandoImagem;
    try{ await compartilharVerso(v); } catch(e){ console.warn(e); }
    if(botao) botao.textContent = rot;
    return;
  }
  if(acao==="copiar"){
    const ok = await copiarTexto(`“${est.versos[v-1] || ""}” — ${refStr(est.livro, est.cap, v)} (${nomeTraducao(est.traducao)})`);
    if(ok && botao){ const rot = botao.textContent; botao.textContent = x.copiado; setTimeout(()=>{ botao.textContent = rot; }, 1400); }
    return;
  }
  if(bancadaAtiva() && ["original","comentario","referencias","anotacao"].includes(acao)){
    fecharGavetas(el);
    est.estudoAba = acao;
    est.chaveEstudo = null;
    focarEstudo(v, true, acao === "anotacao");
    return;
  }
  if(est.gaveta && est.gaveta.tipo===acao && est.gaveta.verso===v){ fecharGavetas(el); return; }
  est.gaveta = {tipo:acao, verso:v};
  const aberta = ()=>est.gaveta && est.gaveta.tipo===acao && est.gaveta.verso===v && el.isConnected;

  if(acao==="original"){
    const ehAT = infoLivro(est.livro).t==="AT";
    const rotulo = ehAT ? x.hebraico : x.grego;
    const inter = await carregarInterlinear(est.livro, est.cap);
    if(!aberta()) return;
    const palavras = inter && inter[v-1] && inter[v-1].length ? inter[v-1] : null;
    if(palavras){
      gavetas.innerHTML = gaveta(rotulo, gradeInterlinear(palavras, ehAT) + htmlMss(ehAT) + `<p class="fonte">${x.lexFonte} · ${linkCorrecao(`Interlinear, ${refStr(est.livro, est.cap, v)}`, x)}</p>`);
      ligarLexico(gavetas, true);
      ligarMss(gavetas, v);
    } else {
      const orig = await carregarLivro("orig", est.livro);
      if(!aberta()) return;
      const texto = orig && orig[est.cap-1] ? orig[est.cap-1][v-1] : "";
      gavetas.innerHTML = gaveta(rotulo,
        texto ? `<p class="original-texto" dir="${ehAT?"rtl":"ltr"}" lang="${ehAT?"he":"grc"}">${esc(texto)}</p>`
              : `<p class="comentario-texto">${x.semOriginal}</p>`);
    }
  }
  if(acao==="comentario"){
    const com = await carregarComentario(est.livro, est.cap);
    if(!aberta()) return;
    gavetas.innerHTML = gaveta(x.comentario, htmlComentarioCorpo(com, v, x, true));
    ligarLerMais(gavetas, x);
  }
  if(acao==="referencias"){
    const [refs, cits] = await Promise.all([carregarRefs(est.livro, est.cap), citacoesDoVerso(est.livro, est.cap, v)]);
    if(!aberta()) return;
    const lista = refs ? refs[String(v)] : null;
    const confs = htmlCitacoes(cits, x);
    if(!lista || !lista.length){
      gavetas.innerHTML = gaveta(x.referencias, confs + (confs ? "" : `<p class="comentario-texto">${x.semRefs}</p>`));
    } else {
      gavetas.innerHTML = gaveta(x.referencias, confs + htmlRefsLista(lista, x));
      carregarPreviasRefs(gavetas, lista);
    }
  }
  if(acao==="anotacao"){
    gavetas.innerHTML = gaveta(x.anotacao,
      `<textarea id="campoNota" placeholder="${x.escrevaNota}" aria-label="${x.anotacao}">${esc(est.notas[chave]||"")}</textarea>
       <div class="acoes">
         <button class="cancelar">${x.cancelar}</button>
         <button class="salvar">${x.salvar}</button>
       </div>`, true);
    gavetas.querySelector(".cancelar").addEventListener("click", ()=>fecharGavetas(el));
    gavetas.querySelector(".salvar").addEventListener("click", ()=>{
      salvarNotaVerso(v, gavetas.querySelector("#campoNota").value);
      fecharGavetas(el);
    });
    gavetas.querySelector("#campoNota").focus({ preventScroll:true });
    gavetas.firstElementChild.scrollIntoView({ block:"nearest" });
  }
  const fechaBtn = gavetas.querySelector(".rotulo button");
  if(fechaBtn) fechaBtn.addEventListener("click", ()=>fecharGavetas(el));
}
function gaveta(rotulo, corpo, destaque){
  return `<div class="gaveta${destaque?" destaque":""}">
    <div class="rotulo"><span>${rotulo}</span><button>✕ ${t().fechar}</button></div>${corpo}</div>`;
}

/* ---------- navegação ---------- */
function vizinhos(){
  const idx = est.meta.books.findIndex(b=>b.id===est.livro), info = est.meta.books[idx];
  return {
    ant: est.cap>1 ? {l:est.livro, c:est.cap-1} : idx>0 ? {l:est.meta.books[idx-1].id, c:est.meta.books[idx-1].ch} : null,
    pro: est.cap<info.ch ? {l:est.livro, c:est.cap+1} : idx<est.meta.books.length-1 ? {l:est.meta.books[idx+1].id, c:1} : null,
  };
}
function atualizarNav(){
  const { ant, pro } = vizinhos();
  const bA = $("btnAnterior"), bP = $("btnProximo");
  bA.disabled = !ant; bP.disabled = !pro;
  if(ant){ bA.querySelector("span").textContent = `${nomeLivro(ant.l)} ${ant.c}`; bA.onclick = ()=>irPara(ant.l, ant.c); }
  if(pro){ bP.querySelector("span").textContent = `${nomeLivro(pro.l)} ${pro.c}`; bP.onclick = ()=>{ leuAoAvancar(); irPara(pro.l, pro.c); }; }
}

function montarListaLivros(){
  const x = t();
  let html = `<div class="grupo">${x.at}</div>`;
  est.meta.books.forEach(b=>{
    if(b.id==="MAT") html += `<div class="grupo">${x.nt}</div>`;
    html += `<button data-livro="${b.id}">${esc(b[est.idioma]||b.pt)}</button>`;
  });
  $("listaLivros").innerHTML = html;
  $("listaLivros").classList.remove("oculto");
  $("listaCapitulos").classList.add("oculto");
  $("tituloLivros").textContent = x.livros;
  $("listaLivros").querySelectorAll("button").forEach(btn=>btn.addEventListener("click", ()=>{
    const info = infoLivro(btn.dataset.livro);
    $("listaLivros").classList.add("oculto");
    $("tituloLivros").textContent = nomeLivro(info.id);
    $("listaCapitulos").innerHTML = `<button class="voltar-livros">‹ ${x.livros}</button>` +
      Array.from({length:info.ch},(_,i)=>`<button data-cap="${i+1}"${foiLido(info.id, i+1) ? ' class="lido"' : ""}>${i+1}</button>`).join("") +
      `<button class="livro-inteiro">${x.sobreLivro} →</button>`;
    $("listaCapitulos").classList.remove("oculto");
    $("listaCapitulos").querySelector(".voltar-livros").addEventListener("click", montarListaLivros);
    $("listaCapitulos").querySelector(".livro-inteiro").addEventListener("click", ()=>{
      alternarPainel("painelLivros", false); navegar({ vista:"livro", livro:info.id });
    });
    $("listaCapitulos").querySelectorAll("[data-cap]").forEach(cb=>cb.addEventListener("click", ()=>{
      alternarPainel("painelLivros", false);
      irPara(info.id, +cb.dataset.cap);
    }));
    const primeiro = $("listaCapitulos").querySelector("[data-cap]");
    if(primeiro) primeiro.focus();
  }));
}

/* ---------- busca ---------- */
/* Outros nomes e abreviações dos livros (além de ABREV e dos nomes em pt/en/es), já sem acento e sem espaço. */
const APELIDOS_LIVRO = { PSA:["sm","slm","salmo","ps","psa","psalm","salterio"], SNG:["canticos","canticodoscanticos","canticodesalomao","cantaresdesalomao","songofsongs","songofsolomon","cant"],
  JOB:["jb"], PRO:["pr","prov"], ECC:["ecl","qoelet"], EZR:["esd"], OBA:["abd","abdias"], ZEP:["sof"], ZEC:["zac"], MIC:["miq"],
  HAB:["hab"], MRK:["mr","mar"], LUK:["lu"], ACT:["atos","atosdosapostolos","hch","hechos"], PHP:["filip"], PHM:["flm","filem"],
  JAS:["tiago","sant","stg"], REV:["apc","apocalipse","revelacao","revelation"], JHN:["joao"], JON:["jonas"],
  "1SA":["1sa","1sam"], "2SA":["2sa","2sam"], "1KI":["1re","1reis","1reyes","1kings"], "2KI":["2re","2reis","2reyes","2kings"],
  "1TH":["1tes","1tess"], "2TH":["2tes","2tess"], "1TI":["1tim"], "2TI":["2tim"], "1PE":["1pd","1ped"], "2PE":["2pd","2ped"],
  "1JN":["1joao"], "2JN":["2joao"], "3JN":["3joao"] };
/* distância de edição (letras trocadas, a mais ou a menos), para aceitar "genisis" e "apocalipce" */
function distancia(a, b){
  if(Math.abs(a.length - b.length) > 2) return 9;
  let ant = [...Array(b.length + 1).keys()];
  for(let i = 1; i <= a.length; i++){
    const atual = [i];
    for(let j = 1; j <= b.length; j++) atual[j] = Math.min(ant[j] + 1, atual[j - 1] + 1, ant[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    ant = atual;
  }
  return ant[b.length];
}
/* Acha o livro por um nome já normalizado ("1corintios", "sl", "apocalipce"). solto = sem capítulo: só nome inteiro. */
function acharLivro(nome, solto){
  if(!nome) return null;
  const livros = est.meta.books, limpo = (n)=>normStr(n).replace(/[^a-z0-9]/g, "");
  const nomes = (b)=>[b.pt, b.en, b.es].map(limpo);
  const exato = nome.length >= 3 && livros.find(b=>nomes(b).includes(nome));          // "jo" (Jó sem acento) fica para João
  if(exato) return exato;
  const apelido = Object.keys(APELIDOS_LIVRO).find(id=>APELIDOS_LIVRO[id].includes(nome));
  if(solto) return apelido && nome.length >= 5 ? infoLivro(apelido) : null;            // sozinho, "os" ou "at" são palavras
  if(ABREV[nome]) return infoLivro(ABREV[nome]);
  if(apelido) return infoLivro(apelido);
  if(livros.find(b=>b.id.toLowerCase() === nome)) return infoLivro(nome.toUpperCase());
  if(nome.length >= 2){                                                                  // começo do nome: "gen", "filip", "jud"
    const comeco = (lng)=>livros.find(b=>limpo(b[lng]).startsWith(nome));
    const b = comeco("pt") || comeco("es") || comeco("en");
    if(b) return b;
  }
  // erro de digitação: o nome mais parecido (até 1 letra nos curtos, 2 nos longos)
  let melhor = null, menor = 9;
  for(const l of livros) for(const n of nomes(l)){
    const d = distancia(nome, n);
    if(d < menor){ menor = d; melhor = l; }
  }
  return melhor && menor <= (nome.length >= 7 ? 2 : nome.length >= 4 ? 1 : 0) ? melhor : null;
}
/* Lê uma referência escrita de muitos jeitos: "João 3:16", "jo 3 16", "Jo3.16", "1 co 13", "I Coríntios 13:4",
   "primeira coríntios 13", "Sm 51", "salmo 23 versículo 1", "apocalipce 21", "Judas 3", "Salmos".
   Devolve {livro, cap, v} (cap 0 = só o livro; v 0 = o capítulo inteiro) ou null. */
function parseRef(txt){
  const cru = String(txt || "").trim().toLowerCase();
  let s = normStr(cru).replace(/[ºª°]/g, "").replace(/\s+/g, " ").trim();
  s = s.replace(/^(livro de |evangelho (de |segundo )?|sao |s\. ?|st\.? |saint )/, "");
  s = s.replace(/^(terceir[oa]|tercer[oa]?|third|3rd|iii)\s+(?=[a-z])/, "3").replace(/^(segund[oa]|second|2nd|ii)\s+(?=[a-z])/, "2")
       .replace(/^(primeir[oa]|primer[oa]?|first|1st|i)\s+(?=[a-z])/, "1").replace(/^([1-3])[oa]\s*(?=[a-z])/, "$1");
  const m = s.match(/^([1-3]?)\s*([a-z][a-z.\s]*?)\.?\s*(\d.*)?$/);
  if(!m) return null;
  const nome = (m[1] + m[2]).replace(/[.\s]/g, "").replace(/(capitulo|cap|chapter|cp)$/, "");
  const resto = (m[3] || "").trim();
  const mn = resto.match(/^(\d+)(?:\s*(?:[:.,;]|\s|v|vs|vv|vers|versiculo|verso|verse)\.?\s*(\d+))?(?:\s*[-–]\s*\d+)?$/);   // o fim de um intervalo fica de fora
  if(resto && !mn) return null;
  const nums = mn ? [+mn[1]].concat(mn[2] ? [+mn[2]] : []) : [];
  let livro = /^jó/.test(cru) ? infoLivro("JOB") : acharLivro(nome, !nums.length);   // sem o acento, "jo" é João
  if(!livro && !m[1] && nums.length) livro = acharLivro("1" + nome, false);              // "coríntios 13": a primeira
  if(!livro) return null;
  if(!nums.length) return { livro: livro.id, cap: 0, v: 0 };
  let [cap, v] = nums;
  if(livro.ch === 1 && nums.length === 1){ v = cap; cap = 1; }                            // Judas 3, Filemom 4: versículo
  if(cap < 1 || cap > livro.ch) return null;
  return { livro: livro.id, cap, v: v || 0 };
}
const nomeRef = (r)=>r.cap ? (r.v ? refStr(r.livro, r.cap, r.v) : `${nomeLivro(r.livro)} ${r.cap}`) : nomeLivro(r.livro);
function irParaRef(r){ return r.cap ? irPara(r.livro, r.cap, r.v) : navegar({ vista:"livro", livro:r.livro }); }
/* Enquanto a pessoa digita numa busca: se o texto é uma referência, um botão "Ir para Salmos 51" logo abaixo. */
function ligarDicaRef(campo, dica, antes){
  const atualizar = ()=>{
    const r = (!antes || antes()) && campo.value.trim() ? parseRef(campo.value) : null;
    dica.innerHTML = r ? `<button type="button" class="dica-ref">${ico("seta")} ${t().irPara} <b>${esc(nomeRef(r))}</b></button>` : "";
    if(r) dica.querySelector("button").addEventListener("click", ()=>{ fecharPaineis(); irParaRef(r); });
  };
  campo.addEventListener("input", atualizar);
  return atualizar;
}
/* Marca os termos no texto ignorando acentos e maiúsculas ("graca" destaca "graça"). */
function destacar(texto, termos){
  let norm = "";
  const pos = [];
  for(let i = 0; i < texto.length; i++){
    for(const ch of normStr(texto[i])){ norm += ch; pos.push(i); }
  }
  const trechos = [];
  for(const termo of termos){
    for(let k = norm.indexOf(termo); k !== -1; k = norm.indexOf(termo, k + termo.length))
      trechos.push([pos[k], pos[k + termo.length - 1] + 1]);
  }
  trechos.sort((a,b)=>a[0]-b[0]);
  let saida = "", fim = 0;
  for(const [a, b] of trechos){
    if(a < fim) continue;
    saida += esc(texto.slice(fim, a)) + "<mark>" + esc(texto.slice(a, b)) + "</mark>";
    fim = b;
  }
  return saida + esc(texto.slice(fim));
}
function parseStrong(txt){
  const m = String(txt || "").trim().match(/^([gh])\s*0*([1-9]\d{0,3})$/i);
  return m ? m[1].toUpperCase() + m[2] : null;
}
// "Como a KJV traduz": a lista original em inglês; em português, a tradução dela (usopt), quando existe
function htmlUsosKjv(ent, x){
  const usos = est.idioma==="en" ? ent.kjv : (emPT() ? ent.usopt : "");
  return usos ? `<p class="lex-def"><strong>${x.lexKjv}:</strong> ${esc(usos)}</p>` : "";
}
// página estática do verbete (/lexico/grego/26/), gerada por ferramentas/paginas_lexico.py
function urlLexico(cod){
  const m = /^([GH])(\d+)$/.exec(cod || "");
  return m ? `/lexico/${m[1]==="G" ? "grego" : "hebraico"}/${+m[2]}/` : "";
}
function htmlLinkLexico(cod, x){
  const url = urlLexico(cod);
  return url ? `<a class="lex-pagina" href="${url}">${x.lexPagina} ›</a>` : "";
}
function htmlStrongItem(k, ent, idxPal, x){
  const lema = idxPal && idxPal.lemas && idxPal.lemas[k];
  return `<div class="strong-item">
    <div class="lex-topo">${htmlOriginalBadge(k, ent.lemma, ent.translit)}</div>
    <p class="lex-def">${esc((emPT() && ent.defpt) || ent.def)}</p>
    ${htmlUsosKjv(ent, x)}
    ${emPT() && lema && lema.nota ? `<p class="strong-nota"><strong>${esc(lema.pt)}:</strong> ${esc(lema.nota)}</p>` : ""}
    ${htmlLinkLexico(k, x)}
  </div>`;
}
async function buscarStrong(){
  const x = t(), termo = $("campoBusca").value.trim();
  const res = $("buscaResultados"), status = $("buscaStatus");
  res.innerHTML = "";
  const cod = parseStrong(termo);
  const vez = ++est.vezBusca;
  if(cod){
    status.textContent = x.buscando;
    const [lex, idxPal] = await Promise.all([carregarLexico(cod[0]), emPT() ? comCache(est.cachePalavras, "indice", "data/palavras/indice.json") : null]);
    if(vez !== est.vezBusca) return;
    const ent = lex && lex[cod];
    if(!ent){ status.textContent = x.nadaEncontrado; return; }
    status.textContent = `1 ${x.resultados}`;
    res.innerHTML = htmlStrongItem(cod, ent, idxPal, x) + `<p class="fonte">${x.lexFonte}</p>`;
    return;
  }
  if(termo.length < 2){ status.textContent = x.digiteStrong; return; }
  status.textContent = x.buscando;
  const [g, h, idxPal] = await Promise.all([
    carregarLexico("G"), carregarLexico("H"),
    emPT() ? comCache(est.cachePalavras, "indice", "data/palavras/indice.json") : null
  ]);
  if(vez !== est.vezBusca) return;
  const normLex = (s)=>normStr(String(s || "")).replace(/[\u0591-\u05c7]/g, "");
  const alvo = normLex(termo), LIMITE = 40;
  const pri = [], sec = [];
  for(const dic of [g, h]){
    if(!dic) continue;
    for(const [k, ent] of Object.entries(dic)){
      const lemaPt = emPT() && idxPal && idxPal.lemas && idxPal.lemas[k] ? normLex(idxPal.lemas[k].pt) : "";
      const tr = normLex(ent.translit), lm = normLex(ent.lemma);
      const def = normLex((emPT() && ent.defpt) || ent.def);
      if(lm === alvo || tr === alvo || ent.lemma === termo || (lemaPt && lemaPt.split(/[,;]/).some(s=>s.trim() === alvo))) pri.push([k, ent]);
      else if(lm.includes(alvo) || tr.includes(alvo) || (lemaPt && lemaPt.includes(alvo)) || def.includes(alvo)) sec.push([k, ent]);
    }
  }
  const achados = pri.concat(sec);
  status.textContent = !achados.length ? x.nadaEncontrado
    : `${achados.length.toLocaleString(est.idioma)} ${x.resultados}` + (achados.length > LIMITE ? ` — ${x.mostrando} ${LIMITE}` : "");
  if(achados.length) res.innerHTML = achados.slice(0, LIMITE).map(([k, ent])=>htmlStrongItem(k, ent, idxPal, x)).join("") + `<p class="fonte">${x.lexFonte}</p>`;
}
async function buscar(aoDigitar){
  aoDigitar = aoDigitar === true;   // pelo botão chega um evento de clique
  if(est.buscaModo==="strong") return buscarStrong();
  if(est.buscaModo==="temas") return buscarTemas();
  if(est.buscaModo==="dicionario") return buscarDic();
  if(est.buscaModo==="confissoes") return buscarConf();
  const x = t(), termo = $("campoBusca").value.trim();
  const res = $("buscaResultados"), status = $("buscaStatus");
  res.innerHTML = "";
  const ref = parseRef(termo);
  if(ref && ref.cap){
    if(aoDigitar){ ++est.vezBusca; status.textContent = ""; return; }   // o botão "Ir para" já aparece logo abaixo
    alternarPainel("painelBusca", false); return irParaRef(ref);
  }
  if(parseStrong(termo) && !aoDigitar){ abrirBusca("strong"); $("campoBusca").value = termo; return buscarStrong(); }
  const vezG = ++est.vezBusca, grupos = gruposBusca(termo);
  if(termo.length < 3 || parseStrong(termo)){
    const g = await grupos;
    if(vezG !== est.vezBusca) return;
    res.innerHTML = g.html; g.ligar(res);
    status.textContent = g.html ? "" : x.digiteBusca;
    return;
  }
  const frase = normStr(termo).replace(/\s+/g, " ");
  const palavras = frase.split(" ").filter(p=>p.length > 1);
  const ids = $("chkBibliaToda").checked || est.vista==="inicio" ? est.meta.books.map(b=>b.id) : [est.livro];
  status.textContent = x.buscando;
  const vez = vezG;
  const livros = await Promise.all(ids.map(id=>carregarLivro(est.traducao, id)));
  if(vez !== est.vezBusca) return;
  const exatos = [], soltos = [];
  livros.forEach((livro, li)=>{
    if(!livro) return;
    livro.forEach((capversos, ci)=>capversos.forEach((texto, vi)=>{
      if(!texto) return;
      const n = normStr(texto);
      if(n.includes(frase)) exatos.push({usfm:ids[li], cap:ci+1, v:vi+1, texto, termos:[frase]});
      else if(palavras.length > 1 && palavras.every(p=>n.includes(p))) soltos.push({usfm:ids[li], cap:ci+1, v:vi+1, texto, termos:palavras});
    }));
  });
  const achados = exatos.concat(soltos), LIMITE = 300;   // a frase exata vem primeiro; depois, versículos com todas as palavras
  status.textContent = !achados.length ? x.nadaEncontrado
    : `${achados.length.toLocaleString(est.idioma)} ${x.resultados}` + (achados.length > LIMITE ? ` — ${x.mostrando} ${LIMITE}` : "");
  const g = await grupos;
  if(vez !== est.vezBusca) return;
  res.innerHTML = g.html + (g.html && achados.length ? `<h4 class="bg-sec">${x.bgVersos}</h4>` : "") + achados.slice(0, LIMITE).map(a=>
    `<a class="res" href="${urlCapitulo(a.usfm, a.cap, a.v)}" style="display:block;text-decoration:none;color:inherit">
       <div class="ref">${esc(refStr(a.usfm,a.cap,a.v))}</div><p>${destacar(a.texto, a.termos)}</p></a>`).join("");
  g.ligar(res);
  if(!achados.length && g.html) status.textContent = "";
}

function avisoConteudo(x, temPT){ return !emPT() ? "" : `<p class="aviso-en">${temPT ? x.tradAuto : x.conteudoEN}</p>`; }
function rotuloDuplo(tit, n){
  return tit[n] && tit[n].toLowerCase() !== n.toLowerCase()
    ? `${esc(tit[n])} <span style="opacity:.55;font-weight:400">(${esc(n)})</span>` : esc(n);
}
/* Referências no formato dos dados (Nave e Easton traduzido): "GEN 3:15", "TIT 1:7,14", "ISA 53", "PSA 23, 24",
   "1TI 1:4; 4:7". Cada uma vira link; depois de uma referência, "; 4:7" é do mesmo livro, e o livro repetido logo em
   seguida não é escrito de novo ("Ezequiel 29:10; 30:6"). Número solto no texto ("40 dias") fica como está. */
const RE_REF = /(?:\b([1-3]?[A-Z]{2,3}) )?(\d+)(?::(\d+))?((?:[-–]\d+(?::\d+)?)?(?:, ?\d+(?:[-–]\d+)?(?![\dA-Z]))*)/g;
/* Referências escritas por extenso no texto corrido dos comentários: "Romanos 8:28", "1 Coríntios 11:10", "Sl 23:1",
   "Jó 1:21" (com acento é Jó; sem, João), "Romans 8:28", "1 Cor. 13:4", "Ps. 23:1". Logo depois de uma, "; 14:44" é do
   mesmo livro. Só vale com capítulo E versículo (evita "3 vezes"), e só se o nome for de um livro mesmo ("em 3:4" fica
   como está). Cada uma vira link com prévia (classe ref-pv, data-pv="ROM.8.28.30"). */
const ABREV_EN = {gen:"GEN",exod:"EXO",lev:"LEV",num:"NUM",deut:"DEU",josh:"JOS",judg:"JDG",neh:"NEH",esth:"EST",ps:"PSA",psa:"PSA",
  psalm:"PSA",prov:"PRO",eccl:"ECC",eccles:"ECC",isa:"ISA",jer:"JER",lam:"LAM",ezek:"EZK",dan:"DAN",hos:"HOS",obad:"OBA",mic:"MIC",
  nah:"NAM",hab:"HAB",zeph:"ZEP",hag:"HAG",zech:"ZEC",mal:"MAL",matt:"MAT",mk:"MRK",lk:"LUK",jn:"JHN",rom:"ROM",gal:"GAL",eph:"EPH",
  phil:"PHP",col:"COL",tit:"TIT",philem:"PHM",heb:"HEB",jas:"JAS",jude:"JUD",rev:"REV",salmo:"PSA",
  // estas só valem com o número antes ("1 Cor", "2 Sam")
  sam:"SA",kgs:"KI",chron:"CH",cor:"CO",thess:"TH",tim:"TI",pet:"PE"};
const RE_REF_TEXTO = /(?<![\p{L}\d])(?:([1-3]|I{1,3})\s?)?(\p{Lu}\p{L}{1,13}|\p{Ll}{2,4})\.?\s(\d{1,3}):(\d{1,3})((?:\s?[-–]\s?\d{1,3}(?!:))?(?:,\s?\d{1,3}(?:[-–]\d{1,3})?(?![\d:]))*)|(?<=;\s?)(\d{1,3}):(\d{1,3})((?:[-–]\d{1,3}(?!:))?)/gu;
let mapaNomesLivros = null;
function livroPorNome(num, nome){
  const n = normStr(nome);
  if(!num && n === "jo") return /ó/i.test(nome) ? "JOB" : "JHN";
  if(!mapaNomesLivros){
    mapaNomesLivros = {};
    const pon = (k, id)=>{ if(k && !(k in mapaNomesLivros)) mapaNomesLivros[k] = id; };
    for(const b of est.meta.books) for(const l of ["pt", "en", "es"]) if(b[l]) pon(normStr(b[l]).replace(/\s+/g, ""), b.id);
    for(const [k, id] of Object.entries(ABREV)) pon(k, id);
    for(const [k, id] of Object.entries(ABREV_EN)) if(id.length === 3) pon(k, id);
  }
  const id = mapaNomesLivros[num + n] || (num && ABREV_EN[n] && ABREV_EN[n].length === 2 ? num + ABREV_EN[n] : null);
  return id && infoLivro(id) ? id : null;
}
function linkarRefsTexto(txt){
  const s = String(txt ?? "");
  let saida = "", fim = 0, ultimo = null;
  for(const m of s.matchAll(RE_REF_TEXTO)){
    let id, cap, v, resto;
    if(m[3] !== undefined){
      id = livroPorNome(m[1] ? ({ I:"1", II:"2", III:"3" }[m[1]] || m[1]) : "", m[2]);
      if(!id){ ultimo = null; continue; }
      [cap, v, resto] = [+m[3], +m[4], m[5] || ""];
    } else {
      if(!ultimo || !/^\s*;\s*$/.test(s.slice(fim, m.index))) continue;
      [id, cap, v, resto] = [ultimo, +m[6], +m[7], m[8] || ""];
    }
    if(cap < 1 || cap > infoLivro(id).ch || v < 1) continue;
    const ate = +((resto.match(/^\s?[-–]\s?(\d+)/) || [])[1] || 0);
    saida += esc(s.slice(fim, m.index)) +
      `<a class="ref-com ref-pv" href="${urlCapitulo(id, cap, v)}" data-pv="${id}.${cap}.${v}.${ate > v ? ate : v}">${esc(m[0])}</a>`;
    fim = m.index + m[0].length; ultimo = id;
  }
  return saida + esc(s.slice(fim));
}
/* Prévia de referência: passar o mouse num link .ref-pv (ou tocar nele, no celular) mostra o versículo num cartão
   flutuante, sem sair do que se está lendo. No toque, o primeiro toque abre a prévia e o segundo (ou "Abrir") navega. */
const tocavel = ()=>matchMedia("(hover:none)").matches;
const prv = { timer:null, fechar:null, link:null };
function cartaoPrevia(){
  let c = $("refPrevia");
  if(!c){
    c = document.createElement("div");
    c.id = "refPrevia"; c.className = "ref-previa-flut"; c.setAttribute("role", "tooltip"); c.hidden = true;
    c.addEventListener("mouseenter", ()=>clearTimeout(prv.fechar));
    c.addEventListener("mouseleave", ()=>fecharPrevia(220));
    document.body.appendChild(c);
  }
  return c;
}
function fecharPrevia(ms){
  clearTimeout(prv.timer); clearTimeout(prv.fechar);
  prv.fechar = setTimeout(()=>{ const c = $("refPrevia"); if(c) c.hidden = true; prv.link = null; }, ms || 0);
}
function posicionarPrevia(c, a){
  const r = a.getBoundingClientRect(), w = Math.min(360, innerWidth - 24);
  c.style.width = w + "px";
  c.style.left = Math.min(Math.max(12, r.left + r.width / 2 - w / 2), innerWidth - w - 12) + "px";
  const h = c.offsetHeight;
  c.style.top = (r.bottom + 8 + h > innerHeight - 8 && r.top - h - 8 > 8 ? r.top - h - 8 : r.bottom + 8) + "px";
}
async function abrirPrevia(a){
  let id, cap, v1, v2;
  if(a.dataset.pv) [id, cap, v1, v2] = a.dataset.pv.split(".").map((p, i)=>i ? +p : p);
  else {
    const r = rotaDe(a.pathname, a.hash);
    if(!r || r.vista !== "cap") return;
    [id, cap, v1, v2] = [r.livro, r.cap, r.v || 1, r.v || 3];
  }
  const x = t(), c = cartaoPrevia();
  clearTimeout(prv.fechar); prv.link = a;
  const trad = ["orig", "byz"].includes(est.traducao) ? (emPT() ? "blivre" : est.idioma === "es" ? "rva" : "kjv") : est.traducao;
  const titulo = refStr(id, cap, v1) + (v2 > v1 ? "-" + v2 : "");
  c.innerHTML = `<div class="rp-topo"><b>${esc(titulo)}</b><a href="${esc(a.getAttribute("href"))}">${x.refAbrir} ›</a></div>
    <p class="rp-texto">${x.carregando}</p>`;
  c.hidden = false; posicionarPrevia(c, a);
  const livro = await carregarLivro(trad, id);
  if(prv.link !== a) return;
  const versos = [];
  for(let v = v1; v <= Math.min(v2, v1 + 4); v++){
    const tx = livro && livro[cap - 1] && livro[cap - 1][v - 1];
    if(tx) versos.push(`${v2 > v1 ? `<sup>${v}</sup>` : ""}${esc(tx)}`);
  }
  c.querySelector(".rp-texto").innerHTML = versos.join(" ") || "—";
  c.insertAdjacentHTML("beforeend", `<p class="rp-trad">${esc(nomeTraducao(trad))}${v2 > v1 + 4 ? " · …" : ""}</p>`);
  posicionarPrevia(c, a);
}
function ligarPrevias(){
  document.addEventListener("mouseover", (e)=>{
    if(tocavel() || !e.target.closest) return;
    const a = e.target.closest("a.ref-pv");
    if(!a) return;
    if(a === prv.link){ clearTimeout(prv.fechar); return; }
    clearTimeout(prv.timer);
    prv.timer = setTimeout(()=>abrirPrevia(a), 260);
  });
  document.addEventListener("mouseout", (e)=>{
    const a = e.target.closest && e.target.closest("a.ref-pv");
    if(!a || (e.relatedTarget && a.contains(e.relatedTarget))) return;
    clearTimeout(prv.timer);
    if(prv.link === a) fecharPrevia(220);
  });
  // na captura da janela: roda antes do ouvinte que navega pelos links internos
  window.addEventListener("click", (e)=>{
    const a = e.target.closest && e.target.closest("a.ref-pv");
    if(a && tocavel() && prv.link !== a){ e.preventDefault(); e.stopPropagation(); abrirPrevia(a); return; }
    if(!(e.target.closest && e.target.closest("#refPrevia")) || (e.target.closest && e.target.closest("#refPrevia a"))) fecharPrevia(0);
  }, true);
  addEventListener("scroll", ()=>{ const c = $("refPrevia"); if(c && !c.hidden) fecharPrevia(0); }, { passive:true, capture:true });
  addEventListener("keydown", (e)=>{ if(e.key === "Escape") fecharPrevia(0); });
}
function linkarRefs(txt){
  const s = String(txt ?? "");
  let saida = "", fim = 0, livro = null;
  for(const m of s.matchAll(RE_REF)){
    const [todo, cod, c, v, resto] = m;
    const seguida = livro && /^\s*;\s*$/.test(s.slice(fim, m.index));
    const l = cod ? (infoLivro(cod) ? cod : null) : (seguida ? livro : null);
    if(!l || +c < 1 || +c > infoLivro(l).ch){ if(cod) livro = null; continue; }
    const nome = cod && !(seguida && cod === livro) ? esc(nomeLivro(l)) + " " : "";
    saida += esc(s.slice(fim, m.index)) + linkRef(l, +c, +v || 0, nome + c + (v ? ":" + v : "") + esc(resto), "tema-ref ref-pv");
    fim = m.index + todo.length; livro = l;
  }
  return saida + esc(s.slice(fim));
}
/* Lista de resultados ({html, titulo, abrir}) e, ao escolher um, o conteúdo dele. */
function listarItens(itens){
  const x = t(), res = $("buscaResultados"), status = $("buscaStatus");
  if(!itens.length){ status.textContent = x.nadaEncontrado; return; }
  status.textContent = `${itens.length} ${x.resultados}`;
  res.innerHTML = itens.map((it,i)=>`<div class="res" data-n="${i}" tabindex="0" role="button"><div class="ref">${it.html}</div></div>`).join("");
  res.querySelectorAll(".res").forEach(el=>{
    const ir = async ()=>{
      const it = itens[+el.dataset.n];
      res.innerHTML = `<h3 class="res-titulo">${it.titulo}</h3>` + await it.abrir();
      status.textContent = "";
    };
    el.addEventListener("click", ir);
    el.addEventListener("keydown", (e)=>{ if(e.key==="Enter"){ ir(); } });
  });
}
/* Página estática do verbete (/dicionario/elias/, /temas/paulo/), gerada por ferramentas/paginas_acervo.py: o endereço
   vem do título em português (ou do nome em inglês), como o slug_url de lá; as exceções estão em enderecos.json. */
function slugAcervo(nome){
  return nome.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");
}
async function htmlLinkAcervo(tipo, nome, x){
  const pasta = tipo==="dictionary" ? "dicionario" : "temas";
  const [tit, exc] = await Promise.all([titulos(tipo), comCache(est.enderecosAcervo, tipo, `data/${tipo}/enderecos.json`)]);
  const s = (exc && exc[nome]) || slugAcervo(tit[nome] || nome);
  return s ? `<a class="lex-pagina" href="/${pasta}/${s}/">${x.acvPagina} ›</a>` : "";
}
function listarVerbetes(nomes, tit, abrir){
  listarItens(nomes.map(n=>({ html: rotuloDuplo(tit, n), titulo: rotuloDuplo(tit, n), abrir: ()=>abrir(n) })));
}
/* Capítulo da Confissão de Westminster (doutrinas.json, gerado por ferramentas/gerar_doutrinas.py): cada parágrafo
   com os seus textos de prova; em inglês, o original de 1647. */
const doutTitulo = (d)=>est.idioma==="en" && d.te ? d.te : d.t;
const doutTexto = (s)=>est.idioma==="en" && s.pe ? s.pe : s.p;
const doutResumo = (d)=>est.idioma==="en" && d.sec && d.sec[0] ? d.sec[0].pe.split(/(?<=[.;:])\s/)[0] : d.r;
function encurtar(txt, n){ return txt.length > n ? txt.slice(0, n).replace(/\s+\S*$/, "") + "…" : txt; }
function htmlDoutrina(d){
  const x = t();
  const refs = (lista)=>lista.map(([l, c, a, b])=>linkRef(l, c, b===999 && a===1 ? 0 : a,
    esc(`${nomeLivro(l)} ${c}` + (b===999 && a===1 ? "" : `:${a}${b!==a && b!==999 ? "-" + b : ""}`)))).join("; ");
  return `<p class="dout-selo">${x.doutSelo} · ${esc(d.f)}</p>` +
    d.sec.map(s=>`<div class="dout-par"><p><b>${esc(s.t)}</b> ${esc(doutTexto(s))}</p>` +
      (s.v.length ? `<p class="dout-provas">${refs(s.v)}</p>` : "") + `</div>`).join("") +
    (d.u ? `<a class="lex-pagina" href="${d.u}">${x.doutPagina} ›</a>` : "") +
    `<a class="lex-pagina" href="/confissoes/">${x.doutTodos} ›</a><p class="fonte">${x.doutFonte}</p>`;
}
async function abrirDoutrina(dOuId){
  abrirBusca("temas");
  const d = typeof dOuId === "string" ? (await doutrinas()).find(o=>o.id===dOuId) : dOuId;
  if(!d) return;
  $("buscaStatus").textContent = "";
  $("buscaResultados").innerHTML = `<h3 class="res-titulo">${esc(doutTitulo(d))}</h3>` + htmlDoutrina(d);
}
const itemDoutrina = (d)=>({ html: `${esc(doutTitulo(d))} <span class="dout-tag">${t().doutSelo}</span>`, titulo: esc(doutTitulo(d)), abrir: async ()=>htmlDoutrina(d) });
const RE_DOUT_GERAL = /reformad|doutrin|westminster|presbiterian|confiss|catecism|calvin/;
/* Credos da Igreja antiga: páginas em /confissoes/credos/<id>/ (ferramentas/credos.py). */
const CREDOS_ANTIGOS = [
  ["apostolico", "Credo Apostólico", "apostolico apostolos simbolo creio"],
  ["niceno", "Credo Niceno", "niceno niceia nicea constantinopla trindade filho"],
  ["atanasio", "Credo de Atanásio", "atanasio quicumque trindade encarnacao"],
  ["calcedonia", "Definição de Calcedônia", "calcedonia duas naturezas encarnacao cristo"]];
const itemCredo = ([id, nome])=>({ html: `${esc(nome)} <span class="dout-tag">${t().credoSelo}</span>`, titulo: esc(nome),
  abrir: async ()=>`<a class="lex-pagina" href="/confissoes/credos/${id}/">${t().credoLer} ›</a>` });
async function itensTemas(termo){
  const x = t();
  const [douts, idx, alias, tit] = await Promise.all([doutrinas(), idxTemas(), aliasPT(), emPT() ? titulos("topics") : {}]);
  const alvo = normStr(termo), geral = RE_DOUT_GERAL.test(alvo);
  const dz = douts.filter(d=>geral || normStr(d.t).includes(alvo) || normStr(d.te || "").includes(alvo) || d.s.some(s=>normStr(s).includes(alvo)));
  const credos = CREDOS_ANTIGOS.filter(([, nome, chaves])=>geral || /credo|creed|simbolo/.test(alvo) || normStr(nome + " " + chaves).includes(alvo));
  const diretos = idx.filter(s=>normStr(s).includes(alvo) || (tit[s] && normStr(tit[s]).includes(alvo)));
  const viaAlias = Object.entries(alias).filter(([pt])=>normStr(pt).includes(alvo)).map(([,en])=>en);
  const nave = [...new Set([...viaAlias, ...diretos])].slice(0, 40).map(nome=>({
    html: rotuloDuplo(tit, nome), titulo: rotuloDuplo(tit, nome), abrir: async ()=>{
      const secao = await temaSecao(nome[0].toUpperCase());
      return (secao[nome] || []).map(l=>`<p class="tema-linha">${linkarRefs(l.replace(/^-/, ""))}</p>`).join("") +
        (await htmlLinkAcervo("topics", nome, x)) + `<p class="fonte">${x.fonteNave}</p>` + avisoConteudo(x, !!secao.__pt);
    }}));
  return [...dz.map(itemDoutrina), ...credos.map(itemCredo), ...nave];
}
async function buscarTemas(){
  const x = t(), termo = $("campoBusca").value.trim(), vez = ++est.vezBusca;
  $("buscaResultados").innerHTML = ""; $("buscaStatus").textContent = "";
  if(termo.length < 2){
    const douts = await doutrinas();
    if(vez !== est.vezBusca) return;
    if(douts.length){ listarItens(douts.map(itemDoutrina)); $("buscaStatus").textContent = x.doutLista; }
    else $("buscaStatus").textContent = x.digiteBusca;
    return;
  }
  const itens = await itensTemas(termo);
  if(vez === est.vezBusca) listarItens(itens);
}
async function itensDic(termo){
  const x = t(), [idx, tit] = await Promise.all([idxDic(), emPT() ? titulos("dictionary") : {}]);
  const alvo = normStr(termo);
  return idx.filter(s=>normStr(s).includes(alvo) || (tit[s] && normStr(tit[s]).includes(alvo))).slice(0, 40).map(nome=>({
    html: rotuloDuplo(tit, nome), titulo: rotuloDuplo(tit, nome), abrir: async ()=>{
      const dic = await dicLetra(nome[0].toUpperCase());
      return (dic[nome]||[]).map(d=>`<p class="dic-def">${linkarRefs(d)}</p>`).join("") +
        (await htmlLinkAcervo("dictionary", nome, x)) + `<p class="fonte">${x.fonteEaston}</p>` + avisoConteudo(x, !!dic.__pt);
    }}));
}
async function buscarDic(){
  const x = t(), termo = $("campoBusca").value.trim(), vez = ++est.vezBusca;
  $("buscaResultados").innerHTML = ""; $("buscaStatus").textContent = "";
  if(termo.length < 2){ $("buscaStatus").textContent = x.digiteBusca; return; }
  const itens = await itensDic(termo);
  if(vez === est.vezBusca) listarItens(itens);
}
/* Busca nas confissões e catecismos (aba Confissões e o grupo da busca universal): o texto em português de todos os
   documentos de /confissoes/, num índice só (data/confissoes/busca.json, gerado pelo paginas_confissoes.py:
   {docs: {id: nome}, itens: [[id, rótulo, endereço, texto]]}), carregado na primeira busca. A frase exata vem
   primeiro; depois, os trechos com todas as palavras. Cada resultado é um link para a página do documento. */
const idxConf = ()=>comCache(est.cachePalavras, "confissoes", "data/confissoes/busca.json");
async function itensConf(termo){
  const idx = await idxConf(), frase = normStr(termo).replace(/\s+/g, " ").trim();
  if(!idx || frase.length < 3) return [];
  const palavras = frase.split(" ").filter(p=>p.length > 2), exatos = [], soltos = [];
  for(const [doc, rot, url, texto] of idx.itens){
    const n = normStr(texto);
    if(n.includes(frase)) exatos.push({doc, rot, url, texto, termos:[frase], pos:n.indexOf(frase)});
    else if(palavras.length > 1 && palavras.every(p=>n.includes(p))) soltos.push({doc, rot, url, texto, termos:palavras, pos:n.indexOf(palavras[0])});
  }
  return exatos.concat(soltos).map(a=>({ ...a, nome: idx.docs[a.doc] || a.doc,
    html: `<b>${esc(idx.docs[a.doc] || a.doc)}</b> · ${esc(a.rot)}` }));
}
function trechoConf(a){                                  // ~220 caracteres em volta da primeira ocorrência
  const ini = Math.max(0, a.pos - 80), fim = Math.min(a.texto.length, ini + 220);
  const s = (ini ? "…" : "") + a.texto.slice(ini, fim) + (fim < a.texto.length ? "…" : "");
  return destacar(s, a.termos);
}
async function buscarConf(){
  const x = t(), termo = $("campoBusca").value.trim(), vez = ++est.vezBusca;
  const res = $("buscaResultados"), status = $("buscaStatus");
  res.innerHTML = ""; status.textContent = "";
  if(termo.length < 3){ status.textContent = x.digiteBusca; return; }
  status.textContent = x.buscando;
  const itens = await itensConf(termo);
  if(vez !== est.vezBusca) return;
  const LIMITE = 150;
  status.textContent = !itens.length ? x.nadaEncontrado
    : `${itens.length.toLocaleString(est.idioma)} ${x.resultados}` + (itens.length > LIMITE ? ` — ${x.mostrando} ${LIMITE}` : "");
  res.innerHTML = itens.slice(0, LIMITE).map(a=>`<a class="res" href="${a.url}" style="display:block;text-decoration:none;color:inherit">
    <div class="ref">${a.html}</div><p>${trechoConf(a)}</p></a>`).join("");
}
/* Busca universal (aba Texto): acima dos versículos, os temas e doutrinas, os verbetes do dicionário e as palavras do
   original que batem com o termo. Cada item abre na aba dele já aberto; "ver todos" leva à aba com a busca feita.
   O léxico inteiro (3 MB) não é carregado aqui: só o código Strong digitado e as palavras-chave (indice.json). */
async function gruposBusca(termo){
  const x = t(), alvo = normStr(termo), vazio = { html:"", ligar(){} };
  if(alvo.length < 2) return vazio;
  const cod = parseStrong(termo);
  const [temas, dic, idxPal, conf] = await Promise.all([
    cod ? [] : itensTemas(termo), cod ? [] : itensDic(termo),
    emPT() ? comCache(est.cachePalavras, "indice", "data/palavras/indice.json").catch(()=>null) : null,
    cod || alvo.length < 3 ? [] : itensConf(termo).catch(()=>[])]);
  const orig = [];
  if(cod){
    const lex = await carregarLexico(cod[0]), ent = lex && lex[cod];
    if(ent) orig.push({ cod, html: `<span class="bg-cod">${esc(cod)}</span> ${esc(ent.lemma)} · ${esc(ent.translit)}` });
  } else if(idxPal && idxPal.lemas && alvo.length >= 3){
    for(const [k, l] of Object.entries(idxPal.lemas)){
      const formas = normStr(l.pt || "").split(/[,;/]/).map(f=>f.trim());
      if(formas.some(f=>f === alvo || (alvo.length >= 4 && f.startsWith(alvo))))
        orig.push({ cod: k, html: `<span class="bg-cod">${esc(k)}</span> ${esc(l.o || "")} · ${esc(l.pt)}` });
      if(orig.length >= 4) break;
    }
  }
  const grupos = [["temas", x.bgTemas, temas], ["confissoes", x.bgConf, conf], ["dicionario", x.bgDic, dic],
    ["strong", x.bgOrig, orig]].filter(g=>g[2].length);
  if(!grupos.length) return vazio;
  const html = `<div class="busca-grupos">` + grupos.map(([modo, rot, itens])=>`<div class="bg-grupo"><h4>${rot}</h4><div class="bg-itens">` +
    itens.slice(0, 4).map((it, i)=>it.url ? `<a class="bg-item" href="${it.url}">${it.html}</a>`     // confissões: link direto
      : `<button type="button" class="bg-item" data-modo="${modo}" data-n="${i}">${it.html}</button>`).join("") +
    (itens.length > 4 ? `<button type="button" class="bg-mais" data-modo="${modo}">${x.bgTodos} (${itens.length})</button>` : "") +
    `</div></div>`).join("") + `</div>`;
  const porModo = Object.fromEntries(grupos.map(g=>[g[0], g[2]]));
  return { html, ligar(raiz){
    raiz.querySelectorAll("button.bg-item, .bg-mais").forEach(b=>b.addEventListener("click", async ()=>{
      const modo = b.dataset.modo, it = b.classList.contains("bg-item") ? porModo[modo][+b.dataset.n] : null;
      abrirBusca(modo);
      if(modo === "strong"){ if(it) $("campoBusca").value = it.cod; return buscarStrong(); }
      if(!it) return modo === "confissoes" ? buscarConf() : buscar();
      ++est.vezBusca;
      $("buscaStatus").textContent = "";
      $("buscaResultados").innerHTML = `<h3 class="res-titulo">${it.titulo}</h3>` + await it.abrir();
    }));
  }};
}
function abrirBusca(modo){
  alternarPainel("painelBusca", true);
  const alvo = document.querySelector(`.busca-abas .aba[data-modo="${modo}"]`);
  if(alvo) alvo.onclick();
  $("campoBusca").focus();
}
function prepararAbas(){
  const x = t();
  const exemplo = ()=>est.buscaModo==="texto" ? x.exPlaceholder : est.buscaModo==="strong" ? x.exStrong : est.buscaModo==="temas" ? x.exTema
    : est.buscaModo==="confissoes" ? x.exConf : x.exDic;
  document.querySelectorAll(".busca-abas .aba").forEach(b=>{
    b.textContent = b.dataset.modo==="texto" ? x.abaTexto : b.dataset.modo==="strong" ? x.abaStrong : b.dataset.modo==="temas" ? x.abaTemas
      : b.dataset.modo==="confissoes" ? x.abaConf : x.abaDic;
    b.onclick = ()=>{
      est.buscaModo = b.dataset.modo;
      document.querySelectorAll(".busca-abas .aba").forEach(o=>{ o.classList.toggle("ativa", o===b); o.setAttribute("aria-selected", o===b); });
      document.querySelector(".busca-escopo").style.display = est.buscaModo==="texto" ? "" : "none";
      $("campoBusca").placeholder = exemplo();
      $("buscaResultados").innerHTML = ""; $("buscaStatus").textContent = "";
      if(est.dicaBusca) est.dicaBusca();
      if(est.buscaModo==="temas" && !$("campoBusca").value.trim()) buscarTemas();
      else if(est.buscaModo==="strong" && $("campoBusca").value.trim()) buscarStrong();
      else if(est.buscaModo==="confissoes" && $("campoBusca").value.trim()) buscarConf();
    };
  });
  $("campoBusca").placeholder = exemplo();
}

/* ---------- planos de leitura ---------- */
async function planos(){ if(!est.planos){ est.planos = await json("data/plans.json"); } return est.planos; }
function pctPlano(pl){
  const pr = est.progresso[pl.id] || {};
  const feitos = Object.values(pr).filter(Boolean).length;
  return Math.round(feitos / pl.dias.length * 100);
}
/* As leituras de um dia: cada item é [livro, cap] ou, parte de um capítulo, [livro, cap, v1, v2]. "grupos" diz
   quantos itens formam cada leitura (M'Cheyne: 4 por dia); sem ele, os capítulos seguidos do mesmo livro são uma
   leitura. Dentro da leitura o livro aparece uma vez: "Gênesis 9, 10", "Lucas 1:1–38", "Zacarias 12, 13:1". */
function leiturasDoDia(caps, grupos){
  const leituras = [];
  if(grupos){ let i = 0; for(const n of grupos){ leituras.push(caps.slice(i, i + n)); i += n; } }
  else for(const it of caps){
    const ult = leituras[leituras.length - 1], ant = ult && ult[ult.length - 1];
    if(ant && ant[0] === it[0] && ant.length === 2 && it.length === 2 && it[1] === ant[1] + 1) ult.push(it);
    else leituras.push([it]);
  }
  return leituras.map(itens=>itens.map(([l, c, a, b], k)=>{
    const rotulo = (k ? "" : nomeLivro(l) + " ") + c + (a ? ":" + a + (b > a ? "–" + b : "") : "");
    return linkRef(l, c, a || 0, esc(rotulo), "");
  }).join(", ")).join("; ");
}
/* Abre o painel de planos (do link /planos/<id>/<dia>/): sem plano, a lista; plano desconhecido, a lista também. */
async function abrirPlano(id, dia){
  const ps = await planos();
  await montarPlanos(ps.find(p=>p.id===id) ? id : null, dia);
  alternarPainel("painelPlanos", true);
}
/* A série do Heidelberg no Instagram (@projetosolabiblia) começou no Domingo 1 em 22/11/2026: quem chega pelo link e
   ainda não marcou nada cai no Domingo da semana. */
const SERIE_HEIDELBERG = Date.UTC(2026, 10, 22);
function domingoDaSerie(){
  const semanas = Math.floor((Date.now() - SERIE_HEIDELBERG) / (7 * 864e5));
  return semanas < 0 ? 0 : semanas % 52;
}
async function montarPlanos(planoAberto, diaAbrir){
  const alvo = $("conteudoPlanos"), x = t();
  const ps = await planos();
  if(!planoAberto){
    alvo.innerHTML = ps.map(pl=>{
      const pct = pctPlano(pl);
      return `<div class="plano-card" data-id="${esc(pl.id)}" tabindex="0" role="button">
        <h3>${esc(pl.nome[est.idioma]||pl.nome.pt)}</h3>
        ${pl.desc ? `<p class="plano-desc">${esc(pl.desc[est.idioma]||pl.desc.pt)}</p>` : ""}
        <div class="plano-barra"><i style="width:${pct}%"></i></div>
        <div class="plano-pct">${pct}% · ${pl.dias.length} ${pl.doc ? (pl.rots ? pl.rots[est.idioma] || pl.rots.pt : x.domingos) : x.dias}</div></div>`;
    }).join("");
    alvo.querySelectorAll(".plano-card").forEach(c=>{
      c.addEventListener("click", ()=>montarPlanos(c.dataset.id));
      c.addEventListener("keydown", (e)=>{ if(e.key==="Enter") montarPlanos(c.dataset.id); });
    });
    return;
  }
  const pl = ps.find(p=>p.id===planoAberto);
  const pr = est.progresso[pl.id] || {};
  let doc = null;
  if(pl.doc){ try{ doc = await json(`data/confissoes/${pl.doc}.json`); }catch(e){ alvo.innerHTML = `<p class="erro-leitura">${x.erroCarregar}</p>`; return; } }
  const en = est.idioma === "en", rotDia = pl.doc ? (pl.rot ? pl.rot[est.idioma] || pl.rot.pt : x.domingo) : x.dia;
  // plano de catecismo: cada dia é um Domingo, com as perguntas e respostas abertas ali mesmo
  const perguntas = (nums)=>{
    const itens = nums.map(n=>doc.itens.find(q=>+q.n === n)).filter(Boolean);
    const faixa = `${x.pergAbrev} ${nums[0]}${nums.length > 1 ? "–" + nums[nums.length - 1] : ""}`;
    return `<details class="dia-cat"><summary><b>${faixa}</b> ${esc(en ? itens[0].p_en : itens[0].p)}</summary>${itens.map(q=>
      `<div class="dia-perg"><p class="dia-p"><a href="/confissoes/${esc(pl.doc)}/${q.n}/">${x.pergAbrev} ${q.n}.</a> ${esc(en ? q.p_en : q.p)}</p>
        <button type="button" class="ver-resposta">${x.verResposta}</button><p class="dia-r">${esc((en ? q.r_en : q.r).replace(/\s*\[\d+\]/g, ""))}</p></div>`).join("")}</details>`;
  };
  // modo memorizar (planos de catecismo): as respostas ficam escondidas até tocar em "Mostrar resposta"; a escolha
  // vale também nas páginas de cada pergunta em /confissoes/ (a mesma chave logos_memorizar)
  const memo = !!pl.doc && lerLS("logos_memorizar", false) === true;
  alvo.classList.toggle("memorizar", memo);
  alvo.innerHTML = `<div class="plano-topo"><button class="voltar-planos">‹ ${x.voltar}</button><span class="plano-acoes">
    ${pl.doc ? `<button type="button" class="plano-memo" aria-pressed="${memo}">${ico("lampada")} <span>${x.memorizar}</span></button>` : ""}
    <button type="button" class="plano-link" data-url="https://solabiblia.com.br/planos/${esc(pl.id)}/">${ico("copiar")} <span>${x.pubCopiar}</span></button></span></div>
    <h3 class="plano-titulo">${esc(pl.nome[est.idioma]||pl.nome.pt)}</h3>` +
    (pl.desc ? `<p class="plano-desc">${esc(pl.desc[est.idioma]||pl.desc.pt)}</p>` : "") +
    pl.dias.map((caps,i)=>
      `<div class="dia-linha${pl.doc ? " dia-linha-cat" : ""}"><span class="dia-num">${rotDia} ${i+1}</span>
        <span class="dia-caps">${pl.doc ? perguntas(caps) : leiturasDoDia(caps, pl.grupos && pl.grupos[i])}</span>
        <input type="checkbox" class="dia-check" data-i="${i}" aria-label="${rotDia} ${i+1}" ${pr[i]?"checked":""}></div>`).join("");
  alvo.querySelector(".voltar-planos").addEventListener("click", ()=>{ alvo.classList.remove("memorizar"); montarPlanos(null); });
  const bm = alvo.querySelector(".plano-memo");
  if(bm) bm.addEventListener("click", ()=>{
    const liga = !alvo.classList.contains("memorizar");
    alvo.classList.toggle("memorizar", liga); bm.setAttribute("aria-pressed", liga); gravarLS("logos_memorizar", liga);
    alvo.querySelectorAll(".dia-perg.vista").forEach(p=>p.classList.remove("vista"));
  });
  alvo.querySelectorAll(".ver-resposta").forEach(b=>b.addEventListener("click", ()=>b.closest(".dia-perg").classList.add("vista")));
  const bl = alvo.querySelector(".plano-link");
  bl.addEventListener("click", async ()=>{
    const rot = bl.querySelector("span");
    if(await copiarTexto(bl.dataset.url)){
      rot.textContent = x.pubCopiado; clearTimeout(est.timerCopiado);
      est.timerCopiado = setTimeout(()=>{ if(rot.isConnected) rot.textContent = x.pubCopiar; }, 2000);
    } else prompt(x.pubCopieAMao, bl.dataset.url);
  });
  alvo.querySelectorAll(".dia-check").forEach(ch=>ch.addEventListener("change", ()=>{
    est.progresso[pl.id] = est.progresso[pl.id] || {};
    est.progresso[pl.id][ch.dataset.i] = ch.checked;
    gravarLS("logos_planos", est.progresso); tocar("plano", pl.id + "." + ch.dataset.i);
  }));
  // onde abrir: o dia pedido no link; senão o primeiro não lido; no Heidelberg sem nada marcado, o Domingo da semana da série
  const linhas = alvo.querySelectorAll(".dia-linha"), primeiro = pl.dias.findIndex((_,i)=>!pr[i]);
  const nada = !Object.values(pr).some(Boolean);
  let i = diaAbrir >= 1 && diaAbrir <= pl.dias.length ? diaAbrir - 1 : pl.id === "heidelberg" && nada ? domingoDaSerie() : primeiro;
  const el = linhas[i];
  if(!el) return;
  if(pl.doc){ const d = el.querySelector("details"); if(d) d.open = true; }   // a semana (ou o Domingo) de agora já aberta
  if(i > 3 || diaAbrir) requestAnimationFrame(()=>el.scrollIntoView({ block: diaAbrir ? "start" : "center" }));
}

/* ---------- linha do tempo ---------- */
/* As datas são escritas em português nos dados; em inglês e espanhol, algumas palavras mudam e, em inglês, a.C./d.C.
   viram BC/AD ("c. 1446 a.C." -> "c. 1446 BC", "30–95 d.C." -> "AD 30–95"). */
const DATAS_TRAD = {
  en: [["No princípio","In the beginning"],["Incerta","Uncertain"],["ambientação patriarcal","patriarchal setting"],
       ["(debatida)","(debated)"],["(provável)","(probable)"],[" ou "," or "]],
  es: [["No princípio","En el principio"],["Incerta","Incierta"],["ambientação patriarcal","ambientación patriarcal"],
       ["(debatida)","(debatida)"],["(provável)","(probable)"],[" ou "," o "]]
};
function dataLocal(d){
  if(emPT() || !d) return d;
  for(const [a, b] of DATAS_TRAD[est.idioma] || []) d = d.split(a).join(b);
  if(est.idioma === "en") d = d.replace(/a\.C\./g, "BC").replace(/(c\. )?([\d–]+) d\.C\./g, (_, c, n)=>`${c || ""}AD ${n}`);
  return d;
}
/* texto de um campo no idioma da interface: campo_en / campo_es, ou o português */
const local = (o, campo)=> (!emPT() && o[campo + "_" + est.idioma]) || o[campo];
async function montarTempo(){
  if(!est.tempo){ est.tempo = await json("data/timeline.json"); }
  $("conteudoTempo").innerHTML = est.tempo.eras.map(era=>
    `<div class="era"><h3>${esc(local(era, "nome"))}</h3>` + era.eventos.map(ev=>
      `<div class="evento"><span class="data">${esc(dataLocal(ev.d))}</span>
       <span class="corpo">${esc(local(ev, "t"))} — ` + ev.r.map(([l,c])=>linkRef(l, c)).join(", ") +
      `</span></div>`).join("") + `</div>`).join("");
}

/* ---------- atlas ---------- */
function carregarLeaflet(){
  return new Promise((res, rej)=>{
    if(window.L) return res();
    const css = document.createElement("link");
    css.rel = "stylesheet"; css.href = "/vendor/leaflet/leaflet.css";
    document.head.appendChild(css);
    const js = document.createElement("script");
    js.src = "/vendor/leaflet/leaflet.js";
    js.onload = ()=>res(); js.onerror = rej;
    document.head.appendChild(js);
  });
}
async function abrirAtlas(){
  alternarPainel("painelAtlas", true);
  try{
    await carregarLeaflet();
    if(!est.lugares){ est.lugares = await json("data/places.json"); }
  }catch(e){ $("atlasResultados").innerHTML = `<p class="erro-leitura">${t().erroCarregar}</p>`; return; }
  montarViagens();
  if(!est.mapa){
    let base, relevo;
    try{ [base, relevo] = await Promise.all([json("data/mapa/base.json"), json("data/mapa/relevo.json").catch(()=>null)]); }
    catch(e){ $("atlasResultados").innerHTML = `<p class="erro-leitura">${t().erroCarregar}</p>`; return; }
    est.mapa = L.map("mapa", { minZoom: 3, maxZoom: 10, maxBounds: [[-6, -26], [60, 104]], maxBoundsViscosity: .8 })
      .setView([31.77, 35.21], 6);
    est.mapa.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
    est.mapa.attributionControl.addAttribution('<a href="https://www.naturalearthdata.com" target="_blank" rel="noopener">Natural Earth</a>');
    est.mapa.createPane("base").style.zIndex = 250;      // abaixo das rotas, marcadores e nomes
    est.mapa.createPane("relevo").style.zIndex = 260;    // o sombreado, misturado à base (mix-blend-mode no CSS)
    montarBaseMapa(base);
    if(relevo) montarRelevo(relevo);
    est.mapa.on("moveend", ()=>{ trocarNivelMapa(); trocarRelevo(); atualizarRotulos(); });
    atualizarRotulos();
  }
  setTimeout(()=>{ est.mapa.invalidateSize(); atualizarRotulos(); }, 150);
}
/* Base do Atlas sem azulejos de fora: terra, litoral, lagos e rios do Natural Earth (data/mapa/base.json, gerado por
   ferramentas/gerar_mapa_base.py), desenhados com as cores do tema; os únicos nomes são os bíblicos, em português.
   Dois níveis: "geral" de longe e "detalhe" de perto (só dentro da caixa dele, do Mediterrâneo à Mesopotâmia). */
const ZOOM_DETALHE = 6;
const corMapa = (v)=>getComputedStyle(document.documentElement).getPropertyValue(v).trim();
function pontosMapa(plano){ const r = []; for(let i = 0; i < plano.length; i += 2) r.push([plano[i + 1], plano[i]]); return r; }
function montarBaseMapa(base){
  const rend = L.canvas({ pane: "base", padding: .3 }), sem = { renderer: rend, interactive: false };
  est.baseMapa = { niveis: {}, atual: null };
  for(const [nome, n] of Object.entries(base.niveis)){
    est.baseMapa.niveis[nome] = { caixa: n.caixa, camadas: [
      ["terra", L.polygon(n.terra.map(p=>p.map(pontosMapa)), { ...sem, stroke: false, fillOpacity: 1 })],
      ["lagos", L.polygon(n.lagos.map(p=>p.map(pontosMapa)), { ...sem, weight: .8, fillOpacity: 1 })],
      ["rios", L.polyline(n.rios.map(pontosMapa), { ...sem, weight: 1.2 })],
      ["costa", L.polyline(n.costa.map(pontosMapa), { ...sem, weight: 1 })]] };
  }
  colorirMapa(); trocarNivelMapa();
}
function colorirMapa(){
  if(!est.baseMapa) return;
  const terra = corMapa("--mapa-terra"), mar = corMapa("--mapa-mar"), costa = corMapa("--mapa-costa"), rio = corMapa("--mapa-rio");
  const estilo = { terra: { fillColor: terra }, lagos: { color: costa, fillColor: mar }, rios: { color: rio }, costa: { color: costa } };
  Object.values(est.baseMapa.niveis).forEach(n=>n.camadas.forEach(([tipo, c])=>c.setStyle(estilo[tipo])));
  if(est.camadaRotulos) atualizarRotulos();
}
function trocarNivelMapa(){
  const mapa = est.mapa, c = mapa.getCenter(), cx = est.baseMapa.niveis.detalhe.caixa;
  const nome = mapa.getZoom() >= ZOOM_DETALHE && c.lng >= cx[0] && c.lat >= cx[1] && c.lng <= cx[2] && c.lat <= cx[3] ? "detalhe" : "geral";
  if(est.baseMapa.atual === nome) return;
  if(est.baseMapa.atual) est.baseMapa.niveis[est.baseMapa.atual].camadas.forEach(([, c])=>mapa.removeLayer(c));
  est.baseMapa.niveis[nome].camadas.forEach(([, c])=>c.addTo(mapa));
  est.baseMapa.atual = nome;
}
/* Relevo sombreado: azulejos em cinza do próprio site (mapa/relevo/{z}/{x}/{y}.png, gerados por
   ferramentas/gerar_relevo.py a partir da elevação aberta do Terrain Tiles). data/mapa/relevo.json diz quais azulejos
   existem em cada zoom: 3–5 da Espanha à Índia, 6–7 do Mediterrâneo à Mesopotâmia e 8 na Terra Santa; de perto, fora
   da Terra Santa, o zoom 7 é ampliado. */
function montarRelevo(indice){
  const limites = (z)=>{
    const [x0, y0, x1, y1] = indice[z], n = 2 ** z, e = 1e-6;
    const lon = (x)=>x / n * 360 - 180, lat = (y)=>Math.atan(Math.sinh(Math.PI * (1 - 2 * y / n))) * 180 / Math.PI;
    return L.latLngBounds([lat(y1 + 1) + e, lon(x0) + e], [lat(y0) - e, lon(x1 + 1) - e]);
  };
  const camada = (zmin, zmax, nativo, z)=>L.tileLayer("/mapa/relevo/{z}/{x}/{y}.png",
    { pane: "relevo", minZoom: zmin, maxZoom: zmax, minNativeZoom: zmin, maxNativeZoom: nativo, bounds: limites(z), attribution: "" });
  // cada camada só pede azulejos dentro da área do seu zoom mais detalhado (os de cima cobrem a mesma área ou mais)
  est.relevo = { longe: indice[5] ? camada(3, 5, 5, 5) : null, meio: indice[7] ? camada(6, 10, 7, 7) : null,
    perto: indice[8] ? camada(8, 10, 8, 8) : null, caixaPerto: indice[8] ? limites(8) : null };
  est.mapa.attributionControl.addAttribution('Relevo: <a href="https://registry.opendata.aws/terrain-tiles/" target="_blank" rel="noopener">Terrain Tiles</a>');
  trocarRelevo();
}
function trocarRelevo(){
  const r = est.relevo, mapa = est.mapa;
  if(!r) return;
  const perto = !!(r.perto && mapa.getZoom() >= 8 && r.caixaPerto.contains(mapa.getCenter()));
  const quer = [r.longe, perto ? r.perto : r.meio].filter(Boolean);
  [r.longe, r.meio, r.perto].filter(Boolean).forEach(c=>{
    if(quer.includes(c)) { if(!mapa.hasLayer(c)) c.addTo(mapa); } else if(mapa.hasLayer(c)) mapa.removeLayer(c);
  });
}
/* Nomes no mapa: os mares (fixos, em itálico) e os lugares mais citados na Bíblia que cabem na tela sem se encostar
   (mais nomes quanto mais perto). Ficam de fora as direções e águas genéricas do geocódigo ("Rio", "Sul", "Oriente"). */
const MARES_MAPA = [   // [nome, lat, lon, zoom mínimo, zoom máximo]
  ["Mar Grande (Mediterrâneo)", 34.3, 19.5, 3, 7], ["Mar Grande", 33.4, 33.2, 6, 8], ["Mar Egeu", 38.4, 25.1, 5, 9], ["Mar Adriático", 42.6, 16.2, 5, 9],
  ["Mar Vermelho", 21.2, 38.6, 3, 7], ["Golfo Pérsico", 27.3, 51.2, 4, 8], ["Mar Negro", 43.3, 34.2, 3, 7],
  ["Mar Cáspio", 41.8, 50.8, 3, 7], ["Mar Salgado (Morto)", 31.52, 35.49, 8, 10], ["Mar da Galileia", 32.83, 35.59, 9, 10]];
const MARES_TRAD = {
  "Mar Grande (Mediterrâneo)": {en:"Great Sea (Mediterranean)", es:"Mar Grande (Mediterráneo)"}, "Mar Grande": {en:"Great Sea", es:"Mar Grande"},
  "Mar Egeu": {en:"Aegean Sea", es:"Mar Egeo"}, "Mar Adriático": {en:"Adriatic Sea", es:"Mar Adriático"},
  "Mar Vermelho": {en:"Red Sea", es:"Mar Rojo"}, "Golfo Pérsico": {en:"Persian Gulf", es:"Golfo Pérsico"},
  "Mar Negro": {en:"Black Sea", es:"Mar Negro"}, "Mar Cáspio": {en:"Caspian Sea", es:"Mar Caspio"},
  "Mar Salgado (Morto)": {en:"Salt Sea (Dead Sea)", es:"Mar Salado (Muerto)"}, "Mar da Galileia": {en:"Sea of Galilee", es:"Mar de Galilea"}};
const NOMES_GENERICOS = /^(Rio|Sul|Norte|Oriente|Mar (Grande|Salgado|Vermelho|do Egito|da Galileia|Adriático))$/;
function atualizarRotulos(){
  const mapa = est.mapa;
  if(!mapa || !est.lugares) return;
  if(!est.camadaRotulos) est.camadaRotulos = L.layerGroup().addTo(mapa);
  est.camadaRotulos.clearLayers();
  const z = mapa.getZoom(), lim = mapa.getBounds();
  const max = Math.round((mapa.getSize().x < 500 ? .55 : 1) * (z <= 4 ? 16 : z === 5 ? 26 : z === 6 ? 38 : z === 7 ? 50 : 64));
  const ocupados = [], usados = new Set();
  for(const [nomePT, la, lo, zmin, zmax] of MARES_MAPA){
    const nome = emPT() ? nomePT : (MARES_TRAD[nomePT] || {})[est.idioma] || nomePT;
    if(z < zmin || z > zmax || !lim.contains([la, lo])) continue;
    const pt = mapa.latLngToContainerPoint([la, lo]), meia = nome.length * 3.4;
    ocupados.push([pt.x - meia, pt.y - 9, pt.x + meia, pt.y + 9]);
    L.marker([la, lo], { interactive: false, keyboard: false,
      icon: L.divIcon({ className: "rotulo-mar", html: `<span>${esc(nome)}</span>`, iconSize: [0, 0] }) }).addTo(est.camadaRotulos);
  }
  const limite = ocupados.length + max;
  // fora do mapa: portas, salas e altares (t "outro") e as localizações incertas (c < 300, dados do openbible.info)
  const cand = est.lugares.filter(l=>l.tot > 0 && l.t !== "outro" && !(l.c < 300) && lim.contains([l.la, l.lo]))
    .sort((a, b)=>b.tot - a.tot);
  for(const l of cand){
    if(ocupados.length >= limite) break;
    const nome = nomeLugar(l);
    if(usados.has(nome) || NOMES_GENERICOS.test((l.p || "").replace(/ \d+$/, ""))) continue;
    const pt = mapa.latLngToContainerPoint([l.la, l.lo]), maior = l.tot >= 150, regiao = l.t === "regiao";
    const larg = nome.length * (regiao ? 8.5 : maior ? 8 : 7);
    const caixa = regiao ? [pt.x - larg / 2, pt.y - 9, pt.x + larg / 2, pt.y + 9] : [pt.x - 6, pt.y - 10, pt.x + 12 + larg, pt.y + 10];
    if(ocupados.some(o=>caixa[0] < o[2] && o[0] < caixa[2] && caixa[1] < o[3] && o[1] < caixa[3])) continue;
    ocupados.push(caixa); usados.add(nome);
    L.marker([l.la, l.lo], { keyboard: false, title: nome, riseOnHover: true,
      icon: L.divIcon({ className: `rotulo rotulo-${l.t || "cidade"}${maior ? " maior" : ""}`, html: `<span>${esc(nome)}</span>`, iconSize: [0, 0] }) })
      .on("click", ()=>mostrarLugar(l))
      .addTo(est.camadaRotulos);
  }
}
/* A busca não lista nada acima do mapa: marca no mapa os lugares achados e abre a ficha do primeiro; os outros
   (homônimos como os três "Jezreel", ou "Vale de Jezreel") ficam como marcadores e como atalhos dentro da ficha. */
function buscarAtlas(){
  const termo = normStr($("campoAtlas").value.trim());
  const res = $("atlasResultados");
  res.innerHTML = "";
  if(termo.length < 2 || !est.lugares || !est.mapa) return;
  // primeiro o nome exato, e entre os homônimos o mais citado ("Jezreel" abre na cidade de Acabe, não na de Judá)
  const exato = (l)=> normStr(nomeLugar(l)) === termo || normStr(l.n.replace(/ \d+$/, "")) === termo;
  const achados = est.lugares.filter(l=>normStr(l.n).includes(termo) || (l.p && normStr(l.p).includes(termo)) || (l.e && normStr(l.e).includes(termo)))
    .sort((a, b)=>(exato(b) - exato(a)) || (b.tot - a.tot)).slice(0, 12);
  fecharLugar();
  est.marcadores.forEach(m=>est.mapa.removeLayer(m)); est.marcadores = [];
  if(!achados.length){ res.innerHTML = `<p class="busca-status">${t().nadaEncontrado}</p>`; return; }
  achados.forEach(l=>{
    const m = L.marker([l.la, l.lo], { title: nomeLugar(l), alt: nomeLugar(l) }).addTo(est.mapa).on("click", ()=>mostrarLugar(l, achados));
    est.marcadores.push(m);
  });
  mostrarLugar(achados[0], achados);
}
const CIDADES_CHAVE = [[{pt:"Jerusalém",en:"Jerusalem",es:"Jerusalén"},31.7784,35.2354],[{pt:"Babilônia",en:"Babylon",es:"Babilonia"},32.5364,44.4208],
  [{pt:"Roma",en:"Rome",es:"Roma"},41.8919,12.5113],[{pt:"Éfeso",en:"Ephesus",es:"Éfeso"},37.9411,27.3419],
  [{pt:"Alexandria",en:"Alexandria",es:"Alejandría"},31.2001,29.9187],[{pt:"Damasco",en:"Damascus",es:"Damasco"},33.5132,36.2919]];
function distKm(a1,o1,a2,o2){
  const R=6371, r=Math.PI/180;
  const dA=(a2-a1)*r, dO=(o2-o1)*r;
  const h=Math.sin(dA/2)**2 + Math.cos(a1*r)*Math.cos(a2*r)*Math.sin(dO/2)**2;
  return Math.round(2*R*Math.asin(Math.sqrt(h)));
}
/* nome em português, sem o número que separa os lugares homônimos ("Jezreel 2", "Afeque 3") */
function nomeLugar(l){ return ((est.idioma === "pt" ? l.p : est.idioma === "es" ? l.e : l.n) || l.p || l.n).replace(/ \d+$/, ""); }
function fecharLugar(){ const f = $("fichaLugar"); if(f){ f.hidden = true; f.innerHTML = ""; } }
function mostrarLugar(l, achados){
  const res = $("fichaLugar");
  const outros = (achados || []).filter(o=>o !== l);
  const refs = l.r.map(([b,c,v])=>linkRef(b, c, v)).join(" · ");
  const primeira = l.r[0], ultima = l.ult || l.r[l.r.length-1];
  const x = t();
  const dists = CIDADES_CHAVE.filter(c=>c[0].en.toLowerCase()!==l.n.toLowerCase() && c[0].pt !== l.p)
    .map(c=>`${c[0][est.idioma] || c[0].pt}: ${distKm(l.la,l.lo,c[1],c[2])} km`).slice(0,4).join(" · ");
  res.innerHTML = `<button type="button" class="lugar-fechar" aria-label="${t().fechar}">✕</button>
    <h3>${esc(nomeLugar(l))}</h3>
    ${l.c < 300 ? `<p class="lugar-incerto">${x.lugarIncerto}</p>` : ""}
    <p class="lugar-meta">${+l.tot} ${x.ocorrencias}
      · ${x.primeira}: ${linkRef(primeira[0], primeira[1], primeira[2])}
      · ${x.ultima}: ${linkRef(ultima[0], ultima[1], ultima[2])}</p>
    <p class="lugar-refs">${refs}</p>
    <p class="lugar-dist">${x.distancias} — ${dists}</p>
    ${l.f && /^https:\/\//.test(l.f) ? `<p class="lugar-meta"><a href="${esc(l.f)}" target="_blank" rel="noopener">${x.verFoto} ↗</a></p>` : ""}
    ${outros.length ? `<p class="lugar-outros">${t().outrosLugares}: ${outros.map(o=>`<button type="button" data-i="${achados.indexOf(o)}">${esc(nomeLugar(o))} <small>(${esc(nomeLivro(o.r[0][0]))} ${o.r[0][1]})</small></button>`).join(" · ")}</p>` : ""}`;
  res.hidden = false;
  res.querySelectorAll(".lugar-outros button").forEach(b=>b.addEventListener("click", ()=>mostrarLugar(achados[+b.dataset.i], achados)));
  res.scrollTop = 0;
  res.querySelector(".lugar-fechar").addEventListener("click", fecharLugar);
  // o lugar fica fora da ficha: à esquerda dela no desktop, acima dela no celular
  const celular = res.offsetTop > 20;
  est.mapa.setView([l.la, l.lo], Math.max(est.mapa.getZoom(), 9), { animate: false });
  est.mapa.panBy(celular ? [0, res.offsetHeight / 2] : [res.offsetWidth / 2, 0], { animate: false });
  res.closest(".mapa-caixa").scrollIntoView({ block: "nearest" });
}
async function montarViagens(){
  if(!est.viagens){ est.viagens = await json("data/journeys.json"); }
  const alvo = $("viagens");
  if(alvo.dataset.pronto) return;
  alvo.dataset.pronto = "1";
  alvo.innerHTML = est.viagens.map(v=>`<button data-v="${esc(v.id)}">${esc(local(v, "nome").split(" (")[0])}</button>`).join("");
  alvo.querySelectorAll("button").forEach(b=>b.addEventListener("click", ()=>{
    const ativa = b.classList.contains("ativa");
    alvo.querySelectorAll("button").forEach(o=>o.classList.remove("ativa"));
    limparViagem();
    if(ativa) return;
    b.classList.add("ativa");
    desenharViagem(est.viagens.find(v=>v.id===b.dataset.v));
  }));
}
function limparViagem(){
  est.camadaViagem.forEach(c=>est.mapa.removeLayer(c));
  est.camadaViagem = [];
}
function desenharViagem(v){
  const pontos = v.paradas.map(p=>p[1]);
  v.paradas.forEach((p,i)=>{
    const m = L.circleMarker(p[1], {radius:6, color:v.cor, fillColor:v.cor, fillOpacity:.9})
      .addTo(est.mapa)
      .bindPopup(`<b>${i+1}. ${esc((!emPT() && (v["paradas_" + est.idioma] || [])[i]) || p[0])}</b><br>` + p[2].map(([b,c,vv])=>linkRef(b, c, vv, null, "")).join(", "));
    est.camadaViagem.push(m);
  });
  est.mapa.fitBounds(L.latLngBounds(pontos).pad(0.15));
  // linha animada: desenha o percurso trecho a trecho
  let i = 0;
  const linha = L.polyline([pontos[0]], {color:v.cor, weight:3, opacity:.85, dashArray:"6 6"}).addTo(est.mapa);
  est.camadaViagem.push(linha);
  const timer = setInterval(()=>{
    i++;
    if(i >= pontos.length || !est.camadaViagem.includes(linha)){ clearInterval(timer); return; }
    linha.addLatLng(pontos[i]);
  }, 350);
}

/* ---------- contexto do livro ---------- */
async function abrirContexto(){
  let c = null;
  try{ c = (await contextos())[est.livro]; }catch(e){}
  if(!c) return;
  $("ctxTitulo").textContent = nomeLivro(est.livro);
  $("ctxCorpo").innerHTML = fichaContexto(c);
  alternarPainel("painelCtx", true);
}

/* ---------- estante exegética ---------- */
function aplicarEstudo(){
  document.body.classList.toggle("estudo", est.estudo);
  $("colEstudo").classList.toggle("oculto", !est.estudo);
  $("btnEstudo").classList.toggle("ativa", est.estudo);
  $("btnEstudo").setAttribute("aria-pressed", est.estudo);
}
function doutrinasDoVerso(douts, usfm, cap, v){
  if(!douts || !douts.length) return [];
  const achados = [];
  for(const d of douts){
    const secs = (d.sec || []).filter(s=>(s.v || []).some(([l, c, a, b])=>l===usfm && c===cap && v>=a && v<=b));
    if(secs.length) achados.push({ d, secs });
  }
  return achados;
}
function sinalizarAbasEstante(v, doutsVerso){
  const temNota = !!est.notas[`${est.livro}.${est.cap}.${v}`];
  const temDout = doutsVerso !== undefined
    ? doutsVerso.length > 0
    : !!(est.doutrinas && doutrinasDoVerso(est.doutrinas, est.livro, est.cap, v).length)
      || !!(est.cacheCit && ((est.cacheCit[est.livro] || {})[String(est.cap)] || {})[String(v)]);
  const marcar = (aba, ativo)=>{
    const btn = document.querySelector(`#abasEstante .eaba[data-eaba="${aba}"]`);
    if(!btn) return;
    let p = btn.querySelector(".ponto");
    if(ativo && !p){ p = document.createElement("span"); p.className = "ponto"; p.setAttribute("aria-hidden", "true"); btn.appendChild(p); }
    else if(!ativo && p) p.remove();
  };
  marcar("anotacao", temNota);
  marcar("referencias", temDout);
}
function htmlPalavraEstante(v, x){
  const idx = est.cachePalavras.indice;
  const todas = (est.traducao === "blivre" && idx && est.palavrasCap && est.palavrasCap[v]) || [];
  const texto = est.versos[v - 1] || "";
  const ativas = todas.map((m, i)=>({ m, i, voc: ehVoc(m), txt: texto.slice(m[0], m[1]) }))
    .filter(o=>o.m[0] >= 0 && o.m[1] <= texto.length && (o.voc ? est.voc : est.chave));
  if(!ativas.length) return { html:"", strong:null };
  const sel = (est.chaveEstudo !== null && ativas.find(o=>o.i === est.chaveEstudo)) || ativas.find(o=>!o.voc) || null;
  const chips = `<div class="chaves-verso"><span class="chaves-rot">${x.chavesNoVerso}</span>` +
    ativas.map(o=>`<button type="button" class="chip-chave${sel && sel.i===o.i ? " ativa" : ""}" data-i="${o.i}">${esc(o.txt)}</button>`).join("") + `</div>`;
  if(!sel) return { html: chips, strong: null };
  const m = sel.m, lema = sel.voc ? idx.termos && idx.termos[m[2]] : idx.lemas && idx.lemas[m[2]];
  if(!lema) return { html: chips, strong: null };
  if(sel.voc){
    const o = m[3] && idx.orig && idx.orig[m[3]];
    return {
      strong: m[3] || null,
      html: chips + `<div class="estante-palavra voc">
        <div class="voc-topo"><span class="voc-palavra">${esc(lema.p || sel.txt)}</span></div>
        <h4>${x.vocSig}</h4><p class="voc-sig">${esc(lema.s)}</p>
        ${lema.n ? `<p class="voc-nota">${esc(lema.n)}</p>` : ""}
        ${o ? `<div class="voc-orig"><span class="voc-rot">${x.vocOrig}</span> ${htmlOriginalBadge(m[3], o[0], o[1])}</div>` : ""}
        <p class="fonte">${htmlFontesNota([lema.f || []], x.vocFonte)}</p></div>`
    };
  }
  return {
    strong: m[2] || null,
    html: chips + `<div class="estante-palavra">
      <div class="lex-topo">${htmlOriginalBadge(m[2], lema.o, lema.t)}</div>
      <p class="cp-trad"><span>${x.chaveTrad}</span> ${esc(lema.pt)}</p>
      ${m[3] ? `<h4>${x.chaveAqui}</h4><p>${esc(m[3])}</p>` : ""}
      ${lema.nota ? `<h4>${x.chavePalavra}</h4><p>${esc(lema.nota)}</p>` : ""}
      <p class="fonte">${htmlFontesNota([m[4] || [], lema.nota ? lema.f || [] : []], x.chaveFonte)}</p></div>`
  };
}
/* Cabeçalho da estante: a palavra aberta no léxico, "voltar ao versículo" quando ele sai da tela e o modo
   "acompanhar a leitura", em que a estante segue o versículo que está na altura de leitura (um terço da tela). */
function alvoEstudo(strong, lema){
  const el = $("estudoAlvo");
  if(!el) return;
  el.hidden = !strong;
  el.innerHTML = strong ? `<span class="ea-num">${esc(strong)}</span> <span class="escritura" ${strong[0] === "H" ? 'dir="rtl" lang="he"' : 'lang="grc"'}>${esc(lema || "")}</span>` : "";
}
const versoEstudoEl = ()=>document.querySelector(`#leitor .verso[data-v="${est.versoEstudo}"]`);
function irVersoEstudo(){
  const el = versoEstudoEl();
  if(el) el.scrollIntoView({ block:"center", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
}
function aplicarSegue(){
  const b = $("estudoSegue"), x = t();
  if(!b) return;
  b.setAttribute("aria-pressed", !!est.estudoSegue);
  b.title = est.estudoSegue ? x.estudoFixo : x.estudoSegue;
  b.setAttribute("aria-label", b.title);
}
function verificarEstante(){
  const volta = $("estudoVolta");
  if(!volta || !bancadaAtiva()) return;
  const topo = document.querySelector(".topo").getBoundingClientRect().bottom;
  if(est.estudoSegue){
    volta.hidden = true;
    const linha = topo + (innerHeight - topo) * .3;
    const alvo = [...document.querySelectorAll("#leitor .verso")].find(el=>el.getBoundingClientRect().bottom >= linha);
    const escrevendo = document.activeElement && document.activeElement.id === "estanteNota";
    if(alvo && +alvo.dataset.v !== est.versoEstudo && !escrevendo) atualizarEstudo(+alvo.dataset.v);
    return;
  }
  const el = versoEstudoEl();
  if(!el){ volta.hidden = true; return; }
  const r = el.getBoundingClientRect(), acima = r.bottom < topo, abaixo = r.top > innerHeight;
  volta.hidden = !(acima || abaixo);
  if(!volta.hidden) volta.textContent = `${acima ? "↑" : "↓"} ${t().estudoVolta} ${est.versoEstudo}`;
}
function ligarEstante(){
  est.estudoSegue = !!lerLS("logos_estudo_segue", false);
  aplicarSegue();
  $("estudoRef").addEventListener("click", irVersoEstudo);
  $("estudoRef").addEventListener("keydown", (e)=>{ if(e.key === "Enter" || e.key === " "){ e.preventDefault(); irVersoEstudo(); } });
  $("estudoVolta").addEventListener("click", irVersoEstudo);
  $("estudoSegue").addEventListener("click", ()=>{
    est.estudoSegue = !est.estudoSegue;
    gravarLS("logos_estudo_segue", est.estudoSegue);
    aplicarSegue(); verificarEstante();
  });
  let espera = null;
  addEventListener("scroll", ()=>{ clearTimeout(espera); espera = setTimeout(verificarEstante, 140); }, { passive:true });
}
async function atualizarEstudo(v, focarNota){
  if(!bancadaAtiva()) return;
  v = Math.max(1, Math.min(v || 1, est.versos.length || 1));
  est.versoEstudo = v;
  const x = t(), chave = `${est.livro}.${est.cap}.${v}`, estado = `${chave}.${est.estudoAba}`;
  est.estudoAtual = estado;
  document.querySelectorAll(".verso.em-estudo").forEach(o=>{ if(+o.dataset.v !== v) o.classList.remove("em-estudo"); });
  const elVerso = document.querySelector(`.verso[data-v="${v}"]`);
  if(elVerso) elVerso.classList.add("em-estudo");

  $("estudoRef").textContent = refStr(est.livro, est.cap, v);
  $("estudoRef").title = x.irVerso;
  alvoEstudo(null);
  verificarEstante();
  $("estudoCores").innerHTML = CORES.map(c=>
    `<button type="button" class="cor${est.marcas[chave]===c ? " sel" : ""}" data-cor="${c}" title="${x.marcar}: ${x.cores[c]}" aria-label="${x.marcar}: ${x.cores[c]}" aria-pressed="${est.marcas[chave]===c}" style="background:var(--m-${c})"></button>`).join("");
  $("estudoCores").querySelectorAll(".cor").forEach(b=>b.addEventListener("click", ()=>alternarMarcaVerso(v, b.dataset.cor)));
  document.querySelectorAll("#abasEstante .eaba").forEach(b=>{
    const ativa = b.dataset.eaba === est.estudoAba;
    b.classList.toggle("ativa", ativa);
    b.setAttribute("aria-selected", ativa);
  });
  sinalizarAbasEstante(v);
  if(!est.doutrinas) doutrinas().then(ds=>{ if(est.versoEstudo === v) sinalizarAbasEstante(v, doutrinasDoVerso(ds, est.livro, est.cap, v)); });
  if(!(est.cacheCit && est.livro in est.cacheCit)) citacoesDoVerso(est.livro, est.cap, v).then(()=>{ if(est.versoEstudo === v) sinalizarAbasEstante(v); });

  const corpo = $("estudoCorpo");
  if(est.estudoAba === "anotacao"){
    const atual = est.notas[chave] || "";
    corpo.innerHTML = `<div class="estante-cartao nota-editor">
      <p class="estante-sub">${x.anotacao} · ${esc(refStr(est.livro, est.cap, v))}</p>
      <textarea id="estanteNota" placeholder="${x.escrevaNota}" aria-label="${x.anotacao}">${esc(atual)}</textarea>
      <div class="acoes">
        ${atual ? `<button type="button" class="cancelar" id="estanteExcluirNota">${x.excluir}</button>` : ""}
        <button type="button" class="salvar" id="estanteSalvarNota">${x.salvar}</button>
      </div></div>
      <button type="button" class="btn-linha" id="estanteVerNotas" style="justify-content:center">${ico("anotacoes")} ${x.notas}</button>`;
    $("estanteSalvarNota").addEventListener("click", ()=>{
      salvarNotaVerso(v, $("estanteNota").value);
      avisar(x.notaSalva, null, null, 1500);
      atualizarEstudo(v);
    });
    if($("estanteExcluirNota")) $("estanteExcluirNota").addEventListener("click", ()=>{
      salvarNotaVerso(v, "");
      atualizarEstudo(v, true);
    });
    $("estanteVerNotas").addEventListener("click", ()=>{ montarNotas(); alternarPainel("painelNotas", true); });
    if(focarNota) $("estanteNota").focus({ preventScroll:true });
    return;
  }

  corpo.innerHTML = `<p class="estudo-vazio">${x.carregando}</p>`;
  if(est.estudoAba === "original"){
    const ehAT = infoLivro(est.livro).t === "AT", rotulo = ehAT ? x.hebraico : x.grego;
    const inter = await carregarInterlinear(est.livro, est.cap);
    if(est.estudoAtual !== estado) return;
    const pal = htmlPalavraEstante(v, x);
    const palavras = inter && inter[v - 1] && inter[v - 1].length ? inter[v - 1] : null;
    let htmlInter = "";
    if(palavras){
      htmlInter = `<div class="estante-cartao"><p class="estante-sub">${rotulo}</p>${gradeInterlinear(palavras, ehAT)}${htmlMss(ehAT)}<p class="fonte">${x.lexFonte} · ${linkCorrecao(`Interlinear, ${refStr(est.livro, est.cap, v)}`, x)}</p></div>`;
    } else {
      const orig = await carregarLivro("orig", est.livro);
      if(est.estudoAtual !== estado) return;
      const txOrig = orig && orig[est.cap - 1] ? orig[est.cap - 1][v - 1] : "";
      htmlInter = `<div class="estante-cartao"><p class="estante-sub">${rotulo}</p>${txOrig
        ? `<p class="original-texto" dir="${ehAT ? "rtl" : "ltr"}" lang="${ehAT ? "he" : "grc"}">${esc(txOrig)}</p>`
        : `<p class="estudo-vazio">${x.semOriginal}</p>`}</div>`;
    }
    corpo.innerHTML = est.chaveEstudo !== null ? pal.html + htmlInter : htmlInter + pal.html;
    corpo.querySelectorAll(".chip-chave").forEach(b=>b.addEventListener("click", ()=>{
      const idxChip = +b.dataset.i;
      est.chaveEstudo = est.chaveEstudo === idxChip ? null : idxChip;
      document.querySelectorAll(".chave.aberta").forEach(o=>o.classList.remove("aberta"));
      if(est.chaveEstudo !== null){
        const chEl = document.querySelector(`.chave[data-v="${v}"][data-i="${idxChip}"]`);
        if(chEl) chEl.classList.add("aberta");
      }
      atualizarEstudo(v);
    }));
    if(palavras){
      const cartaoInter = corpo.querySelector(".estante-cartao");
      ligarLexico(cartaoInter, true, est.chaveEstudo !== null ? pal.strong : null);
      ligarMss(cartaoInter, v);
    }
    return;
  }

  if(est.estudoAba === "comentario"){
    const com = await carregarComentario(est.livro, est.cap);
    if(est.estudoAtual !== estado) return;
    const autor = com && com.__autor ? autorComentario(com, x).split(" (")[0] : x.comentario;
    corpo.innerHTML = `<div class="estante-cartao"><p class="estante-sub">${esc(autor)}</p>${htmlComentarioCorpo(com, v, x, false)}</div>`;
    return;
  }

  if(est.estudoAba === "referencias"){
    const [refs, douts, cits] = await Promise.all([carregarRefs(est.livro, est.cap), doutrinas(), citacoesDoVerso(est.livro, est.cap, v)]);
    if(est.estudoAtual !== estado) return;
    const dVerso = doutrinasDoVerso(douts, est.livro, est.cap, v);
    sinalizarAbasEstante(v, dVerso.length || cits.length ? [1] : []);
    const htmlDouts = dVerso.map(({ d, secs })=>`<div class="estante-cartao confessional">
      <p class="dout-selo">${x.doutSelo} · ${esc(d.f)}</p>
      <h4 class="cm-titulo">${esc(doutTitulo(d))}</h4>
      ${secs.slice(0, 2).map(s=>`<p class="cm-nota"><b>${esc(s.t)}</b> ${esc(encurtar(doutTexto(s), 360))}</p>`).join("")}
      <button type="button" class="dout-atalho" data-dout="${esc(d.id)}">${x.verDoutrina} ${ico("seta")}</button></div>`).join("");
    const lista = refs ? refs[String(v)] : null;
    const htmlRefs = `<div class="estante-cartao"><p class="estante-sub">${x.referencias}</p>${lista && lista.length
      ? htmlRefsLista(lista, x) : `<p class="estudo-vazio">${x.semRefs}</p>`}</div>`;
    const tresFormas = perfil().conf === "tres-formas";
    const ordemCit = ["/confissoes/confissao-belga/", "/confissoes/heidelberg/", "/confissoes/canones-de-dort/"];
    const citsOrd = tresFormas ? [...cits].sort((a, b)=>(ordemCit.findIndex(o=>a[1].startsWith(o)) + 1 || 9) - (ordemCit.findIndex(o=>b[1].startsWith(o)) + 1 || 9)) : cits;
    corpo.innerHTML = tresFormas ? htmlCitacoes(citsOrd, x) + htmlDouts + htmlRefs : htmlDouts + htmlCitacoes(cits, x) + htmlRefs;
    corpo.querySelectorAll(".dout-atalho").forEach(b=>b.addEventListener("click", ()=>abrirDoutrina(b.dataset.dout)));
    if(lista && lista.length) carregarPreviasRefs(corpo, lista);
  }
}

/* ---------- compartilhar versículo como imagem ---------- */
function quebrarLinhas(ctx, texto, largura){
  const linhas = []; let linha = "";
  for(const palavra of texto.split(/\s+/)){
    const teste = linha ? linha + " " + palavra : palavra;
    if(ctx.measureText(teste).width > largura && linha){ linhas.push(linha); linha = palavra; }
    else linha = teste;
  }
  if(linha) linhas.push(linha);
  return linhas;
}
/* Arte do versículo no estilo do Sola: tema claro (papel linho, carmim e ouro) ou escuro (Vigília), no formato do
   feed (1080×1350) ou dos stories (1080×1920, com o conteúdo longe das faixas que o Instagram cobre). */
const CORES_IMAGEM = {
  claro: { fundo: ["#FDFBF6", "#F4EFE3"], fio: "#C6BBA3", fio2: "rgba(140,45,35,.28)", marca: "#8C2D23", nome: "#1D1B18",
    texto: "#1D1B18", aspa: "rgba(140,45,35,.13)", ref: "#785C2A", trad: "#6D665A", faixa: "#8C2D23", faixaTexto: "#FAF7F0", lema: "#F7EBD8" },
  escuro: { fundo: ["#1E1B17", "#12100E"], fio: "rgba(212,174,106,.45)", fio2: "rgba(220,125,111,.22)", marca: "#D4AE6A", nome: "#F4EFE4",
    texto: "#F4EFE4", aspa: "rgba(212,174,106,.12)", ref: "#D4AE6A", trad: "rgba(244,239,228,.62)", faixa: "#9E3429", faixaTexto: "#F4EFE4", lema: "#F1D9B0" },
};
function espacado(c, texto, x, y, esp){   // texto com espaço entre letras (o letterSpacing do canvas não existe em todo navegador)
  const larg = [...texto].reduce((s, ch)=>s + c.measureText(ch).width, 0) + esp * (texto.length - 1);
  let px = x - larg / 2;
  const al = c.textAlign; c.textAlign = "left";
  for(const ch of texto){ c.fillText(ch, px, y); px += c.measureText(ch).width + esp; }
  c.textAlign = al;
}
/* Fundo, molduras, faixa carmim com o endereço e a marca do Sola, comuns às imagens do versículo e do perfil. */
function molduraImagem(c, W, H, k, stories){
  const g = c.createLinearGradient(0, 0, 0, H); g.addColorStop(0, k.fundo[0]); g.addColorStop(1, k.fundo[1]);
  c.fillStyle = g; c.fillRect(0, 0, W, H);
  c.strokeStyle = k.fio; c.lineWidth = 1.5; c.strokeRect(26, 26, W - 52, H - 52);
  c.strokeStyle = k.fio2; c.lineWidth = 1; c.strokeRect(33, 33, W - 66, H - 66);
  // faixa carmim com o endereço (nos stories, acima da barra de resposta do Instagram)
  const faixaY = stories ? H - 420 : H - 158, faixaA = 132;
  c.fillStyle = k.faixa; c.fillRect(26, faixaY, W - 52, faixaA);
  c.textBaseline = "middle";
  c.fillStyle = k.faixaTexto; c.textAlign = "left"; c.font = '600 44px "Cormorant Garamond", "Cardo", serif';
  c.fillText("solabiblia.com.br", 80, faixaY + faixaA / 2 - 12);
  c.font = '500 18px "Inter", sans-serif'; c.globalAlpha = .8;
  c.fillText("BÍBLIA DE ESTUDO GRATUITA", 82, faixaY + faixaA / 2 + 26); c.globalAlpha = 1;
  c.textAlign = "right"; c.fillStyle = k.lema; c.font = 'italic 400 27px "Cardo", serif';
  c.fillText("Sola Scriptura.", W - 80, faixaY + faixaA / 2 - 16); c.fillText("Soli Deo Gloria.", W - 80, faixaY + faixaA / 2 + 18);
  // marca no topo
  const topo = stories ? 300 : 112;
  c.save(); c.translate(W / 2 - 128, topo - 34); c.scale(2.6, 2.6);
  c.strokeStyle = k.marca; c.lineWidth = 1.6; c.lineCap = "round"; c.lineJoin = "round";
  c.stroke(new Path2D("M3 8c3-1.8 6-1.8 9 0c3-1.8 6-1.8 9 0v12c-3-1.8-6-1.8-9 0c-3-1.8-6-1.8-9 0z")); c.stroke(new Path2D("M12 8v12"));
  c.fillStyle = k.marca; c.beginPath(); c.arc(12, 3.4, 1.7, 0, Math.PI * 2); c.fill(); c.restore();
  c.fillStyle = k.nome; c.textAlign = "center"; c.font = '600 42px "Cormorant Garamond", "Cardo", serif';
  espacado(c, "SOLA", W / 2 + 40, topo, 15);
  return { topo, faixaY };
}
async function desenharVerso(v, formato, tema){
  const texto = est.versos[v-1] || "", ref = refStr(est.livro, est.cap, v), trad = nomeTraducao(est.traducao);
  await Promise.all(['400 64px "Cardo"', 'italic 400 26px "Cardo"', '600 34px "Inter"', '400 24px "Inter"', '600 40px "Cormorant Garamond"']
    .map(f=>document.fonts.load(f))).catch(()=>{});
  const k = CORES_IMAGEM[tema], stories = formato === "stories";
  const W = 1080, H = stories ? 1920 : 1350, M = 112;
  const cv = document.createElement("canvas"); cv.width = W; cv.height = H;
  const c = cv.getContext("2d");
  const { topo, faixaY } = molduraImagem(c, W, H, k, stories);
  // área do versículo: entre a marca e a faixa, com a fonte diminuindo até caber
  const areaIni = topo + 90, areaFim = faixaY - 70, rodapeRef = 128;
  const hebraico = /[֐-׿]/.test(texto);
  let tam = stories ? 76 : 66, linhas, alt;
  do {
    c.font = `${tam}px "Cardo", "Times New Roman", serif`;
    linhas = quebrarLinhas(c, hebraico ? texto : `“${texto}”`, W - 2 * M);
    alt = linhas.length * tam * 1.42;
    tam -= 2;
  } while(alt > areaFim - areaIni - rodapeRef && tam > 28);
  tam += 2;
  let y = areaIni + (areaFim - areaIni - rodapeRef - alt) / 2;
  c.fillStyle = k.aspa; c.font = '600 300px "Cormorant Garamond", serif'; c.textAlign = "center";
  if(!hebraico && y - areaIni >= 150) c.fillText("“", W / 2, y - 10);     // as aspas grandes só quando há espaço
  c.fillStyle = k.texto; c.font = `${tam}px "Cardo", "Times New Roman", serif`; c.direction = hebraico ? "rtl" : "ltr";
  y += tam * .71;
  for(const l of linhas){ c.fillText(l, W / 2, y); y += tam * 1.42; }
  c.direction = "ltr";
  y += 6 - tam * .71;
  c.fillStyle = k.marca === "#8C2D23" ? "#8C2D23" : "#DC7D6F"; c.fillRect(W / 2 - 40, y + 18, 80, 2.5);
  c.fillStyle = k.ref; c.font = '600 32px "Inter", sans-serif';
  espacado(c, ref.toUpperCase(), W / 2, y + 66, 4);
  c.fillStyle = k.trad; c.font = '400 24px "Inter", sans-serif'; c.fillText(trad, W / 2, y + 108);
  return { cv, ref, nome: `${normStr(ref).replace(/[^a-z0-9]+/g, "-")}${stories ? "-stories" : ""}.png` };   // sem acento: o Chrome descarta nomes com "ã"
}
/* Janela com a prévia: escolhe formato e tema, e compartilha (celular), baixa ou copia a imagem. */
async function abrirImagem({ titulo, desenhar, texto }){
  const x = t();
  document.querySelector(".img-verso-fundo")?.remove();
  let formato = lerLS("logos_img_formato", "feed"), tema = lerLS("logos_img_tema", "claro");
  if(!["feed", "stories"].includes(formato)) formato = "feed";
  if(!CORES_IMAGEM[tema]) tema = "claro";
  const fundo = document.createElement("div");
  fundo.className = "img-verso-fundo";
  fundo.innerHTML = `<div class="img-verso" role="dialog" aria-modal="true" aria-labelledby="imgVersoTit">
    <button class="fechar" aria-label="${x.fechar}">✕</button>
    <h3 id="imgVersoTit">${titulo}</h3>
    <div class="img-verso-opcoes">
      <div class="seg" role="group" aria-label="${x.imgFormato}"><button data-formato="feed">${x.imgFeed}</button><button data-formato="stories">${x.imgStories}</button></div>
      <div class="seg" role="group" aria-label="${x.imgTema}"><button data-img-tema="claro">${x.imgClaro}</button><button data-img-tema="escuro">${x.imgEscuro}</button></div>
    </div>
    <div class="img-verso-previa"><img alt=""></div>
    <div class="img-verso-acoes"><button class="btn-ouro" id="imgCompartilhar">${x.compartilhar}</button><button id="imgBaixar">${x.imgBaixar}</button><button id="imgCopiar">${x.imgCopiar}</button></div>
    <p class="fonte" role="status" id="imgVersoAviso"></p>
  </div>`;
  document.body.appendChild(fundo);
  const img = fundo.querySelector("img"), aviso = $("imgVersoAviso");
  let atual = null, blob = null;
  const fechar = ()=>{ fundo.remove(); document.removeEventListener("keydown", tecla); if(img.src) URL.revokeObjectURL(img.src); };
  const tecla = (e)=>{ if(e.key === "Escape") fechar(); };
  document.addEventListener("keydown", tecla);
  fundo.addEventListener("click", (e)=>{ if(e.target === fundo) fechar(); });
  fundo.querySelector(".fechar").addEventListener("click", fechar);
  async function redesenhar(){
    fundo.querySelectorAll("[data-formato]").forEach(b=>b.setAttribute("aria-pressed", b.dataset.formato === formato));
    fundo.querySelectorAll("[data-img-tema]").forEach(b=>b.setAttribute("aria-pressed", b.dataset.imgTema === tema));
    fundo.querySelector(".img-verso-previa").classList.toggle("stories", formato === "stories");
    atual = await desenhar(formato, tema);
    blob = await new Promise(r=>atual.cv.toBlob(r, "image/png"));
    if(img.src) URL.revokeObjectURL(img.src);
    img.src = URL.createObjectURL(blob); img.alt = `${atual.ref} — ${titulo}`;
    aviso.textContent = "";
  }
  fundo.querySelectorAll("[data-formato]").forEach(b=>b.addEventListener("click", ()=>{ formato = b.dataset.formato; gravarLS("logos_img_formato", formato); redesenhar(); }));
  fundo.querySelectorAll("[data-img-tema]").forEach(b=>b.addEventListener("click", ()=>{ tema = b.dataset.imgTema; gravarLS("logos_img_tema", tema); redesenhar(); }));
  const arquivo = ()=>new File([blob], atual.nome, { type: "image/png" });
  const podeCompartilhar = ()=>!!(navigator.canShare && blob && navigator.canShare({ files: [arquivo()] }));
  $("imgCompartilhar").addEventListener("click", async ()=>{
    if(podeCompartilhar()) await navigator.share({ files: [arquivo()], text: texto(atual) }).catch(()=>{});
    else $("imgBaixar").click();
  });
  $("imgBaixar").addEventListener("click", ()=>{
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = atual.nome;
    document.body.appendChild(a); a.click(); a.remove();   // o Chrome só respeita o nome com o link na página
    setTimeout(()=>URL.revokeObjectURL(a.href), 4000);
  });
  if(!(navigator.clipboard && window.ClipboardItem)) $("imgCopiar").hidden = true;
  $("imgCopiar").addEventListener("click", async ()=>{
    try{ await navigator.clipboard.write([new ClipboardItem({ "image/png": blob })]); aviso.textContent = x.imgCopiada; }
    catch(e){ aviso.textContent = x.imgSemCopiar; }
  });
  await redesenhar();
  if(!podeCompartilhar()) $("imgCompartilhar").hidden = true;    // no computador: Baixar e Copiar
  fundo.querySelector(".fechar").focus();
}

function compartilharVerso(v){
  const x = t();
  return abrirImagem({ titulo: x.imgTitulo, desenhar: (f, tm)=>desenharVerso(v, f, tm),
    texto: (a)=>`${a.ref} — https://solabiblia.com.br${urlCapitulo(est.livro, est.cap, v)}` });
}

/* ---------- anotações e backup ---------- */
const RE_CHAVE = /^([1-3A-Z][A-Z0-9]{2})\.(\d{1,3})\.(\d{1,3})$/;
function chaveValida(k){ const m = RE_CHAVE.exec(k); return !!(m && infoLivro(m[1]) && +m[2] >= 1 && +m[2] <= infoLivro(m[1]).ch); }
/* Tira do que está guardado no navegador qualquer coisa que não seja do Sola (arquivo de backup adulterado ou corrompido). */
function limparDados(){
  if(typeof est.marcas !== "object" || !est.marcas) est.marcas = {};
  if(typeof est.notas !== "object" || !est.notas) est.notas = {};
  if(typeof est.progresso !== "object" || !est.progresso) est.progresso = {};
  if(typeof est.lidos !== "object" || !est.lidos) est.lidos = {};
  for(const k of Object.keys(est.lidos)) if(!capValido(k) || !(+est.lidos[k] > 0)) delete est.lidos[k];
  if(typeof est.sinc.pend !== "object" || !est.sinc.pend) est.sinc.pend = {};
  for(const k of Object.keys(est.marcas)) if(!chaveValida(k) || !CORES.includes(est.marcas[k])) delete est.marcas[k];
  for(const k of Object.keys(est.notas)) if(!chaveValida(k) || typeof est.notas[k] !== "string") delete est.notas[k];
}
function exportarBackup(){
  const dados = { marcas: est.marcas, notas: est.notas, planos: est.progresso, lidos: est.lidos, perfil: est.perfil,
    prateleira: est.prateleira, meta: est.metaSemana, v: 3 };
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(dados, null, 1)], {type: "application/json"}));
  a.download = "sola-backup.json";
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(()=>URL.revokeObjectURL(a.href), 4000);
}
/* Junta o arquivo com o que já existe neste navegador (não apaga nada); no mesmo item vale o do arquivo. */
function importarBackup(arquivo, feito){
  const r = new FileReader();
  r.onload = ()=>{
    let msg = t().arquivoInvalido;
    try{
      const d = JSON.parse(r.result);
      if(d && typeof d === "object" && (d.marcas || d.notas || d.planos || d.lidos)){
        const nNotas = Object.keys(d.notas || {}).filter(k=>chaveValida(k) && typeof d.notas[k]==="string").length;
        const nMarcas = Object.keys(d.marcas || {}).filter(k=>chaveValida(k) && CORES.includes(d.marcas[k])).length;
        Object.assign(est.marcas, d.marcas); Object.assign(est.notas, d.notas);
        if(d.lidos && typeof d.lidos === "object") Object.assign(est.lidos, d.lidos);
        if(d.perfil && perfilValido(d.perfil)){ est.perfil = perfilValido(d.perfil); gravarLS("logos_perfil", est.perfil); tocar("estado", "perfil"); aplicarPerfil(); }
        if(d.prateleira && typeof d.prateleira === "object") for(const [id, v] of Object.entries(d.prateleira)) if(livroValido(id, v)) salvarLivro(id, v);
        if(+d.meta > 0){ est.metaSemana = Math.min(500, Math.round(+d.meta)); gravarLS("logos_meta_semana", est.metaSemana); tocar("estado", "meta"); }
        if(d.planos && typeof d.planos === "object") for(const id of Object.keys(d.planos))
          est.progresso[id] = Object.assign({}, est.progresso[id], d.planos[id]);
        limparDados();
        gravarLS("logos_marcas", est.marcas); gravarLS("logos_notas", est.notas); gravarLS("logos_planos", est.progresso); gravarLS("logos_lidos", est.lidos);
        // o que veio do arquivo conta como alteração feita agora (sobe para a conta)
        Object.keys(d.notas || {}).forEach(k=>{ if(k in est.notas) tocar("nota", k); });
        Object.keys(d.marcas || {}).forEach(k=>{ if(k in est.marcas) tocar("marca", k); });
        Object.keys(d.lidos || {}).forEach(k=>{ if(k in est.lidos) tocar("lido", k); });
        DADOS.plano.chaves().forEach(k=>tocar("plano", k));
        msg = `${t().restaurado} ${nNotas} ${t().nAnot}, ${nMarcas} ${t().nMarc}.`;
        if(est.vista==="cap") renderizar({ manter:true });
      }
    }catch(err){}
    feito(msg);
  };
  r.readAsText(arquivo);
}
function montarNotas(aviso){
  const x = t(), alvo = $("listaNotas");
  let acoes = document.querySelector(".notas-acoes");
  if(!acoes){
    acoes = document.createElement("div");
    acoes.className = "notas-acoes";
    acoes.innerHTML = `<button id="btnExportar">⬇ <span></span></button>
      <label for="arqImportar" tabindex="0">⬆ <span></span></label>
      <input type="file" id="arqImportar" accept=".json,application/json" style="display:none">
      <p class="fonte" id="notasAviso" role="status"></p>`;
    alvo.parentNode.insertBefore(acoes, alvo);
    acoes.querySelector("#btnExportar").addEventListener("click", exportarBackup);
    acoes.querySelector("label").addEventListener("keydown", (e)=>{ if(e.key==="Enter") $("arqImportar").click(); });
    acoes.querySelector("#arqImportar").addEventListener("change", (e)=>{
      const f = e.target.files[0]; if(!f) return;
      importarBackup(f, (msg)=>{ e.target.value = ""; montarNotas(msg); });
    });
  }
  acoes.querySelector("#btnExportar span").textContent = x.backup;
  acoes.querySelector("label span").textContent = x.restaurar;
  $("notasAviso").textContent = aviso || "";
  const ordem = est.meta.books.map(b=>b.id);
  const chaves = Object.keys(est.notas).filter(chaveValida).sort((a,b)=>{
    const [la,ca,va] = a.split("."), [lb,cb,vb] = b.split(".");
    return ordem.indexOf(la)-ordem.indexOf(lb) || ca-cb || va-vb;
  });
  if(!chaves.length){ alvo.innerHTML = `<p class="vazio">${x.semNotas}</p>`; return; }
  alvo.innerHTML = chaves.map(k=>{
    const [usfm, cap, v] = k.split(".");
    return `<div class="nota" data-k="${k}">
      <div class="ref">${linkRef(usfm, +cap, +v, esc(refStr(usfm,+cap,+v)), "")}<button>${x.excluir}</button></div>
      <p>${esc(est.notas[k])}</p></div>`;
  }).join("");
  alvo.querySelectorAll(".nota").forEach(el=>{
    el.querySelector("button").addEventListener("click", (e)=>{
      e.stopPropagation();
      delete est.notas[el.dataset.k]; gravarLS("logos_notas", est.notas); tocar("nota", el.dataset.k); montarNotas();
      const [usfm, cap, v] = el.dataset.k.split(".");
      if(est.vista==="cap" && usfm===est.livro && +cap===est.cap){
        const sinal = document.querySelector(`.verso[data-v="${v}"] .indicadores`); if(sinal) sinal.remove();
        if(+v === est.versoEstudo){
          sinalizarAbasEstante(+v);
          if(est.estudoAba === "anotacao" && bancadaAtiva()) atualizarEstudo(+v);
        }
      }
    });
    el.addEventListener("click", (e)=>{ if(!e.target.closest("a,button")) el.querySelector("a").click(); });
  });
}

/* ---------- uso sem internet ---------- */
async function baixarOffline(){
  const x = t(), status = $("offlineStatus"), btn = $("btnOffline");
  if(!("caches" in window)){ status.textContent = x.offSem; return; }
  btn.disabled = true;
  const urls = est.meta.books.map(b=>`/data/bibles/${est.traducao}/${b.id}.json`)
    .concat(["/data/books.json","/data/context.json","/data/plans.json","/data/timeline.json","/data/commentaries/calvin/manifest.json","/data/commentaries/henry/manifest.json"]);
  if(est.traducao === "blivre"){     // as palavras-chave sublinhadas acompanham a Bíblia Livre
    const idx = await comCache(est.cachePalavras, "indice", "data/palavras/indice.json");
    if(idx) urls.push("/data/palavras/indice.json", ...idx.livros.map(l=>`/data/palavras/${l}.json`));
  }
  let feitos = 0, falhas = 0;
  try{
    const cache = await caches.open(CACHE_DADOS);
    for(let i = 0; i < urls.length; i += 6){
      await Promise.all(urls.slice(i, i+6).map(u=>cache.add(urlDados(u)).then(()=>{ feitos++; }, ()=>{ falhas++; })));
      status.textContent = `${x.offBaixando} ${feitos}/${urls.length}`;
    }
  }catch(e){ falhas++; }
  status.textContent = falhas ? x.offErro : x.offPronto;
  btn.disabled = false;
}

/* ---------- registro de estudo: capítulos lidos ---------- */
const RE_CAP = /^([1-3A-Z][A-Z0-9]{2})\.(\d{1,3})$/;
function capValido(k){ const m = RE_CAP.exec(k); return !!(m && infoLivro(m[1]) && +m[2] >= 1 && +m[2] <= infoLivro(m[1]).ch); }
function foiLido(usfm, cap){ return (usfm + "." + cap) in est.lidos; }
function marcarLido(usfm, cap, lido){
  const k = usfm + "." + cap;
  if(lido) est.lidos[k] = Date.now(); else delete est.lidos[k];
  gravarLS("logos_lidos", est.lidos); tocar("lido", k);
  if(lido) convidar("lido");
}
/* Quem avança para o próximo capítulo depois de um tempo razoável na página leu o capítulo. */
function leuAoAvancar(){
  if(est.vista === "cap" && !foiLido(est.livro, est.cap) && Date.now() - (est.capAbertoEm || Date.now()) > 20000)
    marcarLido(est.livro, est.cap, true);
}
function botaoLido(){
  const x = t(), lido = foiLido(est.livro, est.cap);
  return `<div class="fim-cap"><button id="btnLido" class="btn-lido${lido ? " feito" : ""}" aria-pressed="${lido}">${ico("feito")} <span>${lido ? x.lido : x.lidoMarcar}</span></button></div>`;
}
function ligarBotaoLido(){
  const b = $("btnLido");
  if(b) b.addEventListener("click", ()=>{
    marcarLido(est.livro, est.cap, !foiLido(est.livro, est.cap));
    b.parentNode.outerHTML = botaoLido(); ligarBotaoLido();
  });
}
const diaLocal = (d)=>{ d = new Date(d); return d.getFullYear() + "-" + String(d.getMonth()+1).padStart(2,"0") + "-" + String(d.getDate()).padStart(2,"0"); };
function resumoEstudo(){
  const porLivro = {};
  for(const k of Object.keys(est.lidos)){ const l = k.split(".")[0]; porLivro[l] = (porLivro[l] || 0) + 1; }
  const total = est.meta.books.reduce((n, b)=>n + b.ch, 0);
  const lidos = Object.keys(est.lidos).length;
  // sequência: dias seguidos com leitura, terminando hoje ou ontem
  const dias = new Set(Object.values(est.lidos).map(diaLocal));
  const d = new Date(); let seq = 0;
  if(!dias.has(diaLocal(d))) d.setDate(d.getDate() - 1);
  while(dias.has(diaLocal(d))){ seq++; d.setDate(d.getDate() - 1); }
  return { porLivro, total, lidos, seq, notas: Object.keys(est.notas).length, marcas: Object.keys(est.marcas).length };
}
const ordemRef = (a, b)=>{
  const [la, ca, va] = a.split("."), [lb, cb, vb] = b.split("."), o = est.meta.books;
  return o.findIndex(x=>x.id===la) - o.findIndex(x=>x.id===lb) || ca - cb || va - vb;
};

/* ---------- perfil personalizável ----------
   Tudo fica no aparelho (logos_perfil, logos_prateleira) e sobe para a conta como itens "estado" (chaves "perfil" e
   "livro:<id>"), com a mesma regra de sempre: no mesmo item, vale a alteração mais recente. */
const PERFIL_CORES = { carmim:"#8C2D23", ouro:"#7A5E2A", oliva:"#55613A", azul:"#35546E", vinho:"#6B2D3E", grafite:"#4A453D" };
const PERFIL_ICONES = ["cruz", "livro", "lampada", "ancora", "coroa", "pomba"];
const PERFIL_CAPAS = ["linho", "carmim", "ouro", "oliva", "mar", "vigilia"];
const PERFIL_LETRAS = { p:.9, m:1, g:1.12, gg:1.25 };
const SECOES_PAINEL = ["semana", "historico", "recentes", "conquistas", "prateleira", "livros", "planos", "marcacoes", "notas"];
const RE_FOTO = /^data:image\/(jpeg|webp|png);base64,[A-Za-z0-9+/=]+$/;
function perfil(){
  const p = est.perfil && typeof est.perfil === "object" ? est.perfil : {};
  const av = Object.assign({ t:"letra", cor:"carmim", ic:"cruz", foto:"" }, p.av || {});
  const secoes = Object.assign({ ordem:[], ocultas:[] }, p.secoes || {});
  const pub = Object.assign({ on:false, apelido:"", num:true, selos:true, prat:true, conta:"" }, p.pub || {});
  return { nome:"", capa:"linho", vers:"", bio:"", letra:"m", conf:"westminster", ...p, av, secoes, pub };
}
/* Confere um perfil que veio de fora (conta, backup): só campos conhecidos, tamanhos limitados. */
function perfilValido(v){
  if(!v || typeof v !== "object") return null;
  const s = (x, n)=>typeof x === "string" ? x.slice(0, n) : "";
  const av = v.av && typeof v.av === "object" ? v.av : {};
  const pub = v.pub && typeof v.pub === "object" ? v.pub : {};
  return {
    nome: s(v.nome, 40), bio: s(v.bio, 200),
    vers: typeof v.vers === "string" && chaveValida(v.vers) ? v.vers : "",
    capa: PERFIL_CAPAS.includes(v.capa) ? v.capa : "linho",
    letra: v.letra in PERFIL_LETRAS ? v.letra : "m",
    conf: v.conf === "tres-formas" ? "tres-formas" : "westminster",
    av: { t: ["letra", "icone", "foto"].includes(av.t) ? av.t : "letra", cor: av.cor in PERFIL_CORES ? av.cor : "carmim",
          ic: PERFIL_ICONES.includes(av.ic) ? av.ic : "cruz", foto: typeof av.foto === "string" && RE_FOTO.test(av.foto) && av.foto.length < 45000 ? av.foto : "" },
    secoes: { ordem: (v.secoes && Array.isArray(v.secoes.ordem) ? v.secoes.ordem : []).filter(x=>SECOES_PAINEL.includes(x)),
              ocultas: (v.secoes && Array.isArray(v.secoes.ocultas) ? v.secoes.ocultas : []).filter(x=>SECOES_PAINEL.includes(x)) },
    pub: { on: !!pub.on, apelido: typeof pub.apelido === "string" && !problemaApelido(pub.apelido) ? pub.apelido : "",
           num: pub.num !== false, selos: pub.selos !== false, prat: pub.prat !== false,
           conta: typeof pub.conta === "string" && /^[0-9a-f-]{36}$/.test(pub.conta) ? pub.conta : "" },
  };
}
function salvarPerfil(mudanca){
  est.perfil = perfilValido(Object.assign(perfil(), mudanca));
  gravarLS("logos_perfil", est.perfil); tocar("estado", "perfil");
  aplicarPerfil();
}
function aplicarPerfil(){
  document.documentElement.style.setProperty("--escala-texto", PERFIL_LETRAS[perfil().letra] || 1);
  if($("btnPerfil")) atualizarBotaoPerfil();
}
function nomeExibicao(){ const u = est.sessao && est.sessao.user; return perfil().nome.trim() || (u ? nomeUsuario(u) : ""); }
function perfilPersonalizado(){ const p = perfil(); return !!(p.nome.trim() || p.av.t !== "letra" || p.av.cor !== "carmim"); }
function htmlAvatar(classe, p = perfil(), nome = nomeExibicao()){
  const cor = PERFIL_CORES[p.av.cor] || PERFIL_CORES.carmim;
  if(p.av.t === "foto" && p.av.foto) return `<span class="conta-letra ${classe} com-foto" aria-hidden="true"><img src="${p.av.foto}" alt=""></span>`;
  const dentro = p.av.t === "icone" ? ico(p.av.ic) : nome ? esc(nome.trim()[0].toUpperCase()) : ico("pessoa");
  return `<span class="conta-letra ${classe}" style="background:${cor}" aria-hidden="true">${dentro}</span>`;
}
/* foto escolhida no aparelho: recortada no centro e reduzida a 160×160 (cabe com folga na conta) */
function reduzirFoto(arquivo){
  return new Promise((ok, falha)=>{
    if(!arquivo || !/^image\//.test(arquivo.type)) return falha();
    const img = new Image(), url = URL.createObjectURL(arquivo);
    img.onload = ()=>{
      const lado = Math.min(img.naturalWidth, img.naturalHeight), cv = document.createElement("canvas");
      cv.width = cv.height = 160;
      cv.getContext("2d").drawImage(img, (img.naturalWidth - lado) / 2, (img.naturalHeight - lado) / 2, lado, lado, 0, 0, 160, 160);
      URL.revokeObjectURL(url);
      ok(cv.toDataURL("image/jpeg", .82));
    };
    img.onerror = ()=>{ URL.revokeObjectURL(url); falha(); };
    img.src = url;
  });
}
/* o versículo de vida no idioma da interface (Bíblia Livre, KJV ou RVA) */
/* Na Bíblia Livre o título do salmo vem no começo do v. 1 ("Salmo de Davi, para o regente...: Tem misericórdia...")
   e o Salmo 119 abre cada estrofe com a letra hebraica ("Álefe:"); no versículo de vida fica só o texto. */
const TITULO_SALMO_PALAVRAS = /(salmo|c[âa]ntico|can[çc][ãa]o|ora[çc][ãa]o|instru[çc][ãa]o|masquil|mict|regente|davi|asafe|cor[ée]|salom[ãa]o|mois[ée]s|hem[ãa]|et[ãa]|instrumento|sigai|neginote|gitite|seminite|alamote|degraus|louvor|memorial|s[áa]bado)/i;
function tituloSalmoBL(texto){ const m = (texto || "").match(/^([^:]{3,400}?):\s*(?=\S)/); return m && TITULO_SALMO_PALAVRAS.test(m[1]) ? m[0] : ""; }
function semTituloSalmo(l, c, v, texto){
  if(l !== "PSA" || !texto) return texto;
  if(+c === 119 && v % 8 === 1) return texto.replace(/^[^\s:]{2,12}:\s*/, "");
  return +v === 1 ? texto.slice(tituloSalmoBL(texto).length) : texto;
}
/* KJV e RVA: o título é a primeira frase ("A Psalm of David. The Lord is my shepherd"); quais salmos têm título,
   diz a Bíblia Livre (assim um salmo sem título não perde a primeira frase) */
async function semTituloSalmoOutra(l, c, v, texto){
  if(l !== "PSA" || !texto) return texto;
  if(+c === 119 && v % 8 === 1) return texto.replace(/^(\S+\s)?[A-Z]+\.\s*/, "");
  if(+v !== 1) return texto;
  let bl = ""; try{ bl = ((await carregarLivro("blivre", "PSA"))[c - 1] || [])[0] || ""; }catch(e){}
  const m = texto.match(/^.{3,400}?[.?]\s+(?=\S)/) || texto.match(/^.{3,400}?:\s+(?=\S)/);
  return tituloSalmoBL(bl) && m ? texto.slice(m[0].length) : texto;
}
async function textoVersiculoVida(chave){
  if(!chave) return "";
  const [l, c, v] = chave.split(".");
  const trad = est.idioma === "en" ? "kjv" : est.idioma === "es" ? "rva" : "blivre";
  try{ const caps = await carregarLivro(trad, l); const tx = (caps[+c - 1] || [])[+v - 1] || "";
    return trad === "blivre" ? semTituloSalmo(l, +c, +v, tx) : await semTituloSalmoOutra(l, +c, +v, tx); }catch(e){ return ""; }
}
function htmlCartaoPerfil(x, extra, p = perfil(), nome = nomeExibicao() || x.visitante, compartilhar = true){
  const [l, c, v] = (p.vers || "").split(".");
  return `<div class="perfil-cartao capa-${p.capa}">
      <div class="perfil-capa"></div>
      ${compartilhar ? `<button type="button" class="perfil-compartilhar" aria-label="${x.compartilharPerfil}" title="${x.compartilharPerfil}">${ico("compartilhar")}</button>` : ""}
      <div class="perfil-id">${htmlAvatar("grande", p, nome)}
        <div><strong class="perfil-nome">${esc(nome)}</strong>${p.bio ? `<span class="perfil-bio">${esc(p.bio)}</span>` : ""}${extra || ""}</div>
      </div>
      ${p.vers ? `<blockquote class="perfil-vers"><p data-vers-vida="${esc(p.vers)}"></p>
        <cite>${linkRef(l, +c, +v, esc(refStr(l, +c, +v)), "")}</cite></blockquote>` : ""}
    </div>`;
}
async function preencherVersiculoVida(raiz){
  const el = raiz.querySelector("[data-vers-vida]");
  if(el) el.textContent = await textoVersiculoVida(el.dataset.versVida);
}

/* ----- imagem do perfil para compartilhar (mesma janela da imagem do versículo) ----- */
const CAPAS_IMAGEM = { linho:["#F3ECDD", "#DCCBA8"], carmim:["#B24A3C", "#5E1C16"], ouro:["#E4C98E", "#7A5E2A"], oliva:["#7D8A55", "#4F5B33"],
  mar:["#6E93AE", "#2F4E66"], vigilia:["#3A342B", "#12100E"] };
const LOMBADAS = { antiga:"#6B2D3E", medieval:"#55613A", reforma:"#8C2D23", puritanos:"#35546E", avivamento:"#7A5E2A", moderna:"#4A453D",
  filosofia:"#2F5D5A", apologetica:"#5A3E6E", devocional:"#9A4E2E", literatura:"#2E3F5E", biografia:"#6E5A2E", outra:"#6D665A" };
/* desenha no canvas um ícone do próprio site (os <symbol> do index.html) */
function desenharIcone(c, nome, x, y, tam, cor){
  const sim = document.getElementById("i-" + nome); if(!sim) return;
  c.save(); c.translate(x - tam / 2, y - tam / 2); c.scale(tam / 24, tam / 24);
  c.strokeStyle = cor; c.fillStyle = cor; c.lineWidth = 1.7; c.lineCap = "round"; c.lineJoin = "round";
  sim.querySelectorAll("path,circle").forEach(el=>{
    if(el.tagName === "path"){ c.stroke(new Path2D(el.getAttribute("d"))); return; }
    c.beginPath(); c.arc(+el.getAttribute("cx"), +el.getAttribute("cy"), +el.getAttribute("r"), 0, Math.PI * 2);
    if(el.getAttribute("fill") === "currentColor") c.fill(); else c.stroke();
  });
  c.restore();
}
function carregarImagem(src){ return new Promise((ok)=>{ const i = new Image(); i.onload = ()=>ok(i); i.onerror = ()=>ok(null); i.src = src; }); }
function cortarLinha(c, txt, larg){ if(c.measureText(txt).width <= larg) return txt; while(txt && c.measureText(txt + "…").width > larg) txt = txt.slice(0, -1); return txt.trim() + "…"; }
async function desenharPerfil(formato, tema){
  const x = t(), p = perfil(), r = resumoEstudo(), nome = nomeExibicao() || x.visitante;
  await Promise.all(['400 64px "Cardo"', 'italic 400 34px "Cardo"', '600 34px "Inter"', '500 48px "Inter"', '400 24px "Inter"', '600 40px "Cormorant Garamond"']
    .map(f=>document.fonts.load(f))).catch(()=>{});
  const k = CORES_IMAGEM[tema], stories = formato === "stories";
  const W = 1080, H = stories ? 1920 : 1350, M = 120;
  const cv = document.createElement("canvas"); cv.width = W; cv.height = H;
  const c = cv.getContext("2d");
  const { topo, faixaY } = molduraImagem(c, W, H, k, stories);
  c.textBaseline = "alphabetic"; c.textAlign = "center";
  // capa
  const capaY = topo + 58, capaH = stories ? 230 : 180, cc = CAPAS_IMAGEM[p.capa] || CAPAS_IMAGEM.linho;
  const gc = c.createLinearGradient(70, capaY, W - 70, capaY + capaH); gc.addColorStop(0, cc[0]); gc.addColorStop(1, cc[1]);
  c.fillStyle = gc; c.beginPath(); if(c.roundRect) c.roundRect(70, capaY, W - 140, capaH, 18); else c.rect(70, capaY, W - 140, capaH); c.fill();
  // avatar
  const R = stories ? 118 : 96, ax = W / 2, ay = capaY + capaH;
  c.fillStyle = k.fundo[0]; c.beginPath(); c.arc(ax, ay, R + 9, 0, Math.PI * 2); c.fill();
  c.save(); c.beginPath(); c.arc(ax, ay, R, 0, Math.PI * 2); c.clip();
  const foto = p.av.t === "foto" && p.av.foto ? await carregarImagem(p.av.foto) : null;
  if(foto) c.drawImage(foto, ax - R, ay - R, 2 * R, 2 * R);
  else {
    c.fillStyle = PERFIL_CORES[p.av.cor] || PERFIL_CORES.carmim; c.fillRect(ax - R, ay - R, 2 * R, 2 * R);
    if(p.av.t === "icone") desenharIcone(c, p.av.ic, ax, ay, R * 1.15, "#FAF7F0");
    else { c.fillStyle = "#FAF7F0"; c.font = `600 ${Math.round(R * 1.15)}px "Cormorant Garamond", serif`; c.textBaseline = "middle";
      c.fillText((nome.trim()[0] || "?").toUpperCase(), ax, ay + R * .06); c.textBaseline = "alphabetic"; }
  }
  c.restore();
  // nome e bio
  let y = ay + R + (stories ? 90 : 74);
  let tam = stories ? 74 : 64; c.fillStyle = k.nome;
  do { c.font = `600 ${tam}px "Cormorant Garamond", "Cardo", serif`; tam -= 2; } while(c.measureText(nome).width > W - 2 * M && tam > 36);
  c.fillText(nome, W / 2, y);
  if(p.bio){
    c.font = `400 ${stories ? 30 : 27}px "Inter", sans-serif`; c.fillStyle = k.trad;
    quebrarLinhas(c, p.bio, W - 2 * M - 40).slice(0, 2).forEach((l, i)=>{ y += i ? (stories ? 42 : 38) : (stories ? 58 : 52); c.fillText(l, W / 2, y); });
  }
  // versículo de vida
  if(p.vers){
    const txt = await textoVersiculoVida(p.vers), [l, cp, v] = p.vers.split(".");
    if(txt){
      const tv = stories ? 38 : 32, max = stories ? 6 : 4;
      c.font = `italic 400 ${tv}px "Cardo", serif`; c.fillStyle = k.texto;
      let linhas = quebrarLinhas(c, `“${txt}”`, W - 2 * M - 30);
      if(linhas.length > max){ linhas = linhas.slice(0, max); linhas[max - 1] = cortarLinha(c, linhas[max - 1] + "…", W - 2 * M - 30); }
      y += stories ? 84 : 68;
      for(const lin of linhas){ c.fillText(lin, W / 2, y); y += tv * 1.42; }
      c.fillStyle = k.ref; c.font = '600 24px "Inter", sans-serif';
      espacado(c, refStr(l, +cp, +v).toUpperCase(), W / 2, y + 8, 3);
      y += 30;
    }
  }
  // números do estudo
  const feitas = conquistas().filter(q=>q.feito).length;
  const livrosLidos = Object.values(est.prateleira || {}).filter(o=>o && o.st === "lido").length;
  const nums = [[r.lidos, x.capsLidos], [feitas, x.conquistasTit.toLowerCase()], [livrosLidos ? livrosLidos : r.seq, livrosLidos ? x.imgLivrosLidos : x.diasSeguidos]];
  y += stories ? 100 : 80;
  const colW = (W - 2 * M) / 3;
  nums.forEach(([n, rot], i)=>{
    const cx = M + colW * i + colW / 2;
    c.fillStyle = k.nome; c.font = `500 ${stories ? 56 : 48}px "Inter", sans-serif`; c.fillText(Number(n).toLocaleString(est.idioma), cx, y);
    c.fillStyle = k.trad; c.font = '400 22px "Inter", sans-serif'; c.fillText(cortarLinha(c, rot, colW - 20), cx, y + 38);
    if(i){ c.fillStyle = k.fio; c.fillRect(M + colW * i, y - 46, 1.5, 92); }
  });
  y += 64;
  // prateleira: as lombadas dos livros lidos e em leitura, se houver espaço até a faixa
  const cat = est.catPrateleira || { obras: [] };
  const livros = Object.keys(est.prateleira || {}).filter(id=>["lido", "lendo"].includes(est.prateleira[id].st)).map(id=>obraDe(id, cat))
    .sort((a, b)=>(b.em || 0) - (a.em || 0));
  const espaco = faixaY - 60 - y;
  if(livros.length && espaco >= 120){
    const altMax = Math.min(espaco - 30, 240), lw = stories ? 52 : 46, gap = 6;
    const cabem = Math.min(livros.length, Math.floor((W - 2 * M + gap) / (lw + gap)));
    const larg = cabem * (lw + gap) - gap;
    let lx = (W - larg) / 2;
    const base = y + 20 + altMax;
    livros.slice(0, cabem).forEach((o, i)=>{
      const h = altMax * (.78 + ((o.t.length * 7 + i * 3) % 23) / 100);
      c.fillStyle = LOMBADAS[o.tr] || LOMBADAS.outra;
      c.beginPath(); if(c.roundRect) c.roundRect(lx, base - h, lw, h, [4, 4, 0, 0]); else c.rect(lx, base - h, lw, h); c.fill();
      c.fillStyle = "rgba(255,255,255,.14)"; c.fillRect(lx + 4, base - h + 6, 3, h - 12);
      c.save(); c.translate(lx + lw / 2 + 7, base - 12); c.rotate(-Math.PI / 2);
      c.fillStyle = "#FAF7F0"; c.font = `600 ${stories ? 18 : 16}px "Inter", sans-serif`; c.textAlign = "left";
      c.fillText(cortarLinha(c, o.t, h - 24), 0, 0); c.restore();
      lx += lw + gap;
    });
    c.fillStyle = k.ref; c.fillRect((W - larg) / 2 - 24, base, larg + 48, 8);
  }
  return { cv, ref: nome, nome: `perfil-${normStr(nome).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "sola"}${stories ? "-stories" : ""}.png` };
}
async function compartilharPerfil(){
  const x = t();
  await catalogoPrateleira();
  return abrirImagem({ titulo: x.imgPerfilTit, desenhar: desenharPerfil,
    texto: (a)=>`${a.ref} — ${x.imgPerfilTexto} https://solabiblia.com.br${pubAtivo() ? urlPerfilPublico(perfil().pub.apelido) : ""}` });
}

/* ----- página pública do perfil (opcional, com conta): solabiblia.com.br/perfil/<apelido>/ -----
   A pessoa escolhe o apelido e o que mostrar; o app grava um retrato do cartão em perfis_publicos (ferramentas/supabase.sql)
   pela função publicar_perfil() e o refaz depois de cada sincronização. Qualquer visitante lê com a chave pública, por
   fetch simples (sem carregar o cliente do Supabase). As listas abaixo são as mesmas de apelido_permitido() no SQL. */
const APELIDO_RESERVADOS = ["sola","solabiblia","sola-biblia","admin","administrador","administracao","suporte","contato",
  "ajuda","oficial","equipe","moderador","moderacao","root","sistema","perfil","perfis","biblia","api","www","null",
  "undefined","deus","jesus","cristo","jesus-cristo","espirito-santo","senhor","igreja"];
const APELIDO_PROIBIDOS = ["puta","puto","putas","putos","merda","porra","foda","fodase","foder","fodido","fodida","cu",
  "cus","cuzao","cuzinho","bosta","piroca","corno","viado","vadia","vagabunda","vagabundo","otario","babaca",
  "imbecil","cacete","buceta","boceta","xoxota","xereca","punheta","prostituta","prostituto","nazi","nazista",
  "hitler","satanas","satan","diabo","lucifer","demonio","sexo","porno","porn","xxx","anal","nude","nudes",
  "fuck","fucker","fucking","shit","bitch","cunt","dick","cock","pussy","whore","slut","fag","faggot","nigger",
  "nigga","rape","rapist","asshole","bastard","kkk","mierda","joder","cono","pendejo","pendeja","cabron",
  "cabrona","verga","chinga","chingar","maricon","culo","zorra","perra","gilipollas","hijueputa"];
const APELIDO_RAIZES = /^(arromb|vagabund|prostitut|punhet|fodid|caralh|bucet|bocet|xoxot|putari|pornog|fuck|nigg|faggot|pendej|chingad|hijueput|gilipoll|retardad|nazis|satanis)/;
const APELIDO_SEMPRE = /(caralho|buceta|boceta|punheta|xoxota|fuck|nigger|nigga|faggot|hitler|putaria|putinha|putona)/;
function problemaApelido(a){
  if(!/^[a-z0-9][a-z0-9-]{1,28}[a-z0-9]$/.test(a) || a.includes("--")) return "formato";
  if(APELIDO_RESERVADOS.includes(a)) return "reservado";
  if(a.split("-").some(s=>APELIDO_PROIBIDOS.includes(s) || APELIDO_RAIZES.test(s)) || APELIDO_SEMPRE.test(a.replace(/-/g, ""))) return "improprio";
  return "";
}
const limparApelido = (s)=>normStr(s).replace(/[\s_.]+/g, "-").replace(/[^a-z0-9-]/g, "").slice(0, 30);
function sugerirApelido(){ return limparApelido(nomeExibicao()).replace(/-+/g, "-").replace(/^-+|-+$/g, ""); }
const urlPerfilPublico = (a)=>`/perfil/${a}/`;
function pubAtivo(){ const pub = perfil().pub, u = est.sessao && est.sessao.user; return !!(u && pub.on && pub.apelido && pub.conta === u.id); }
/* o retrato publicado: só o que está no cartão e o que a pessoa marcou (nunca anotações, marcações ou datas de leitura) */
function dadosPublicos(){
  const p = perfil(), pub = p.pub, r = resumoEstudo();
  const d = { v: 1, nome: nomeExibicao().slice(0, 40), bio: p.bio, capa: p.capa, vers: p.vers,
    av: Object.assign({ t: p.av.t, cor: p.av.cor, ic: p.av.ic }, p.av.t === "foto" && p.av.foto ? { foto: p.av.foto } : {}) };
  if(pub.num) d.num = { lidos: r.lidos, livros: est.meta.books.filter(b=>(r.porLivro[b.id] || 0) >= b.ch).length,
    seq: r.seq, seqMax: Math.max(sequenciaMaxima(), r.seq) };
  if(pub.selos) d.selos = conquistas().filter(c=>c.feito).map(c=>c.id);
  if(pub.prat) d.prat = Object.entries(est.prateleira || {}).sort((a, b)=>(b[1].em || 0) - (a[1].em || 0)).slice(0, 80)
    .map(([id, o])=>id.startsWith("u-") ? { t: o.t, a: o.a || "", st: o.st } : { id, st: o.st });
  return d;
}
/* grava a página; sem forcar, só quando algo mudou desde o último envio */
async function publicarPerfil(forcar){
  if(!pubAtivo()) return { ok: false };
  const pub = perfil().pub, dados = dadosPublicos(), assinatura = JSON.stringify([pub.apelido, dados]);
  if(!forcar && lerLS("logos_pub_enviado", "") === assinatura) return { ok: true };
  const sb = await clienteConta();
  const { error } = await sb.rpc("publicar_perfil", { p_apelido: pub.apelido, p_dados: dados });
  if(error){
    const m = String(error.message || "");
    return { ok: false, erro: /apelido_em_uso/.test(m) ? "emUso" : /apelido_invalido/.test(m) ? "formato" : "rede" };
  }
  gravarLS("logos_pub_enviado", assinatura);
  return { ok: true };
}
function agendarPublicacao(){
  if(!pubAtivo()) return;
  clearTimeout(est.timerPub);
  est.timerPub = setTimeout(()=>publicarPerfil().catch(e=>console.warn("perfil público", e)), 3000);
}
async function lerPerfilPublico(apelido){
  const r = await fetch(`${CONTA.url}/rest/v1/perfis_publicos?apelido=eq.${encodeURIComponent(apelido)}&select=apelido,dados,atualizado_em`,
    { headers: { apikey: CONTA.chave, Accept: "application/json" }, cache: "no-store" });
  if(!r.ok) throw new Error("perfil público " + r.status);
  const l = await r.json();
  return Array.isArray(l) && l[0] ? l[0] : null;
}
/* seção "Página pública" da aba Perfil */
function htmlPaginaPublica(x){
  if(!temConta()) return "";
  const u = est.sessao && est.sessao.user, pub = perfil().pub;
  if(!u) return `<h3 class="estudo-sub">${x.pubTit}</h3><p class="fonte">${x.pubSemConta}</p>`;
  const ativo = pubAtivo();
  return `<h3 class="estudo-sub">${x.pubTit}${ativo ? ` <small class="sub-conta pub-no-ar">${x.pubNoAr}</small>` : ""}</h3>
    <div class="pub-caixa" id="pubCaixa">
      <p class="fonte">${x.pubTexto}</p>
      <div class="pf-campo"><label for="pubApelido">${x.pubEndereco}</label>
        <div class="pub-link"><span class="pub-endereco"><span>solabiblia.com.br/perfil/</span><input id="pubApelido" maxlength="30" autocapitalize="none" autocomplete="off" spellcheck="false" value="${esc(pub.apelido || sugerirApelido())}"></span>
          ${ativo ? `<button type="button" class="btn-ouro" id="pubCopiar" data-url="https://solabiblia.com.br${urlPerfilPublico(pub.apelido)}">${ico("copiar")} <span>${x.pubCopiar}</span></button>` : ""}</div>
        <small class="fonte" id="pubAviso" role="status"></small></div>
      <div class="pf-campo"><span>${x.pubMostrar}</span>
        ${["num", "selos", "prat"].map(k=>`<label class="pub-opcao"><input type="checkbox" data-pub="${k}" ${pub[k] ? "checked" : ""}> ${x.pubOpcoes[k]}</label>`).join("")}</div>
      <div class="conta-acoes">${ativo
        ? `<button class="btn-ouro" id="pubPublicar">${x.pubAtualizar}</button><a class="btn-linha" href="${urlPerfilPublico(pub.apelido)}">${x.pubVer}</a>
           <button class="link-discreto" id="pubTirar">${x.pubTirar}</button>`
        : `<button class="btn-ouro" id="pubPublicar">${x.pubPublicar}</button>`}</div>
    </div>`;
}
function ligarPaginaPublica(){
  const cx = $("pubCaixa"); if(!cx) return;
  const x = t(), campo = $("pubApelido"), aviso = ()=>$("pubAviso");
  const refazer = async (msg)=>{ const rolar = $("conteudoEstudo").scrollTop; await montarMeuEstudo(); $("conteudoEstudo").scrollTop = rolar; if(msg && aviso()) aviso().textContent = msg; };
  let espera;
  campo.addEventListener("input", ()=>{
    const limpo = limparApelido(campo.value);
    if(limpo !== campo.value) campo.value = limpo;
    clearTimeout(espera);
    espera = setTimeout(async ()=>{
      const a = campo.value, prob = problemaApelido(a);
      if(prob){ aviso().textContent = x.apelidoErros[prob]; return; }
      if(pubAtivo() && a === perfil().pub.apelido){ aviso().textContent = ""; return; }
      try{ const r = await lerPerfilPublico(a); if(campo.value === a) aviso().textContent = r ? x.apelidoErros.emUso : x.apelidoLivre; }
      catch(e){ aviso().textContent = ""; }
    }, 450);
  });
  cx.querySelectorAll("[data-pub]").forEach(c=>c.addEventListener("change", ()=>{
    salvarPerfil({ pub: { ...perfil().pub, [c.dataset.pub]: c.checked } }); agendarPublicacao();
  }));
  $("pubPublicar").addEventListener("click", async ()=>{
    const a = campo.value.replace(/^-+|-+$/g, ""), prob = problemaApelido(a);
    if(prob){ aviso().textContent = x.apelidoErros[prob]; campo.focus(); return; }
    const antes = perfil().pub;
    salvarPerfil({ pub: { ...antes, on: true, apelido: a, conta: est.sessao.user.id } });
    aviso().textContent = x.pubEnviando;
    const r = await publicarPerfil(true).catch(()=>({ ok: false, erro: "rede" }));
    if(!r.ok){
      salvarPerfil({ pub: antes });
      aviso().textContent = r.erro === "emUso" || r.erro === "formato" ? x.apelidoErros[r.erro] : x.pubErro;
      return;
    }
    await refazer(`${x.pubOk} solabiblia.com.br${urlPerfilPublico(a)}`);
  });
  // o link inteiro: um toque no campo seleciona tudo; o botão copia e confirma no próprio botão
  if($("pubCopiar")) $("pubCopiar").addEventListener("click", async ()=>{
    const rot = $("pubCopiar").querySelector("span");
    if(await copiarTexto($("pubCopiar").dataset.url)){
      rot.textContent = x.pubCopiado; clearTimeout(est.timerCopiado);
      est.timerCopiado = setTimeout(()=>{ if(rot.isConnected) rot.textContent = x.pubCopiar; }, 2000);
    } else aviso().textContent = `${x.pubCopieAMao} ${$("pubCopiar").dataset.url}`;
  });
  if($("pubTirar")) $("pubTirar").addEventListener("click", async ()=>{
    if(!confirm(x.pubTirarConfirma)) return;
    try{
      const { error } = await (await clienteConta()).rpc("despublicar_perfil");
      if(error) throw error;
    }catch(e){ console.warn("perfil público", e); aviso().textContent = x.pubErro; return; }
    salvarPerfil({ pub: { ...perfil().pub, on: false } });
    try{ localStorage.removeItem("logos_pub_enviado"); }catch(e){}
    await refazer(x.pubFora);
  });
}
/* a página que o visitante vê em /perfil/<apelido>/ */
async function renderizarPerfilPublico(){
  const x = t(), a = est.apelidoPub, alvo = $("leitor");
  document.title = `@${a} — Sola`;
  alvo.innerHTML = `<div class="perfil-publico"><p class="fonte pub-carregando">${x.pubCarregando}</p></div>`;
  let linha = null, falhou = false;
  try{ linha = temConta() ? await lerPerfilPublico(a) : null; }catch(e){ console.warn("perfil público", e); falhou = true; }
  const [cat] = await Promise.all([catalogoPrateleira()]);
  if(est.vista !== "perfil" || est.apelidoPub !== a) return;   // a pessoa já foi para outra página
  const convite = `<aside class="pub-convite"><p class="heroi-sobre">Sola</p><h2>${x.pubConvite}</h2><p>${x.pubConviteTexto}</p>
      <a class="btn-ouro" href="/">${x.pubComecar} ${ico("seta")}</a></aside>`;
  if(!linha){
    alvo.innerHTML = `<div class="perfil-publico pub-vazio"><h1>${falhou ? x.pubSemRedeTit : x.pubNaoAchou}</h1>
      <p>${falhou ? x.pubSemRede : x.pubNaoAchouTexto}</p>${convite}</div>`;
    return;
  }
  const d = linha.dados && typeof linha.dados === "object" ? linha.dados : {};
  const p = perfilValido(d), nome = p.nome.trim() || a;
  document.title = `${nome} (@${a}) — Sola`;
  const int = (v, max)=>Math.max(0, Math.min(max, Math.round(+v) || 0));
  const total = est.meta.books.reduce((n, b)=>n + b.ch, 0), num = d.num && typeof d.num === "object" ? d.num : null;
  let numeros = "";
  if(num){
    const lidos = int(num.lidos, total), pct = Math.round(lidos / total * 1000) / 10;
    numeros = `<div class="estudo-numeros pub-numeros">
      <div class="num largo"><b>${lidos.toLocaleString(est.idioma)}</b><span>${x.de} ${total.toLocaleString(est.idioma)} ${x.capsLidos} · ${pct.toLocaleString(est.idioma)}%</span>
        <div class="plano-barra"><i style="width:${pct}%"></i></div></div>
      <div class="num"><b>${int(num.livros, 66)}</b><span>${x.pubLivrosBiblia}</span></div>
      <div class="num">${ico("chama")}<b>${int(num.seq, 99999)}</b><span>${x.diasSeguidos}</span></div>
      <div class="num"><b>${int(num.seqMax, 99999)}</b><span>${x.pubMaiorSeq}</span></div></div>`;
  }
  const todos = conquistas(), ids = Array.isArray(d.selos) ? d.selos : [];
  const feitos = todos.filter(c=>ids.includes(c.id));
  const selos = feitos.length ? `<h3 class="estudo-sub">${x.conquistasTit} <small class="sub-conta">${feitos.length}/${todos.length}</small></h3>
    <div class="selos">${feitos.map(c=>`<div class="selo feito"><span class="selo-ic">${ico(c.ic)}</span><b>${esc(x.selos[c.id] || c.id)}</b></div>`).join("")}</div>` : "";
  const livros = (Array.isArray(d.prat) ? d.prat.slice(0, 80) : []).map(o=>{
    if(!o || typeof o !== "object" || !ST_LIVRO.includes(o.st)) return null;
    if(o.id){ const c = cat.obras.find(b=>b.id === o.id); return c ? { ...c, st: o.st } : null; }
    const tt = typeof o.t === "string" ? o.t.slice(0, 120).trim() : "";
    return tt ? { t: tt, a: typeof o.a === "string" ? o.a.slice(0, 80) : "", tr: "outra", st: o.st } : null;
  }).filter(Boolean);
  const prat = livros.length ? `<h3 class="estudo-sub">${x.prateleiraTit} <small class="sub-conta">${livros.length}</small></h3>` + ST_LIVRO.map(st=>{
    const l = livros.filter(o=>o.st === st);
    return l.length ? `<div class="prat"><p class="prat-rot">${x.stLivro[st]} <small>${l.length}</small></p><div class="prat-livros">${l.map(o=>
      `<span class="lombada tr-${o.tr || "outra"}" style="height:${7 + (o.t.length % 5) * .45}rem" title="${esc(o.t + (o.a ? " — " + o.a : ""))}"><span>${esc(o.t)}</span></span>`).join("")}</div></div>` : "";
  }).join("") : "";
  const meu = pubAtivo() && perfil().pub.apelido === a;
  const quando = new Date(linha.atualizado_em);
  alvo.innerHTML = `<div class="perfil-publico">
      ${htmlCartaoPerfil(x, `<span class="perfil-apelido">@${esc(a)}</span>`, p, nome, false)}
      ${numeros}${selos}${prat}
      <div class="pub-rodape">
        ${isNaN(quando) ? "" : `<p class="fonte">${x.pubAtualizado} ${esc(quando.toLocaleDateString(est.idioma, { day:"numeric", month:"long", year:"numeric" }))}</p>`}
        <div class="conta-acoes"><button class="btn-linha" id="pubCompartilharLink">${ico("compartilhar")} ${x.pubCompartilhar}</button>
          ${meu ? `<button class="btn-linha" id="pubEditar">${x.pubEditar}</button>` : ""}</div>
      </div>
      ${convite}
    </div>`;
  preencherVersiculoVida(alvo);
  $("pubCompartilharLink").addEventListener("click", async ()=>{
    const url = "https://solabiblia.com.br" + urlPerfilPublico(a);
    if(navigator.share){ try{ await navigator.share({ title: `${nome} — Sola`, url }); return; }catch(e){ if(e && e.name === "AbortError") return; } }
    if(await copiarTexto(url)) avisar(x.pubLinkCopiado, null, null, 2000);
  });
  if($("pubEditar")) $("pubEditar").addEventListener("click", ()=>abrirMeuEstudo("perfil"));
}

/* ----- editor do perfil (aba Perfil) ----- */
function htmlEditorPerfil(x){
  const p = perfil();
  const ordem = ordemSecoes();
  const nomesSec = x.secoesNomes;
  return `<div class="perfil-editor" id="perfilEditor">
    <label class="pf-campo"><span>${x.pfNome}</span><input id="pfNome" maxlength="40" value="${esc(p.nome)}" placeholder="${esc(nomeExibicao() || x.visitante)}"></label>
    <div class="pf-campo"><span>${x.pfAvatar}</span>
      <div class="seg" role="group" aria-label="${x.pfAvatar}">${["letra", "icone", "foto"].map(tp=>
        `<button type="button" data-av="${tp}" aria-pressed="${p.av.t === tp}">${x["pfAv_" + tp]}</button>`).join("")}</div>
      ${p.av.t === "icone" ? `<div class="pf-opcoes">${PERFIL_ICONES.map(ic=>
        `<button type="button" class="pf-ic${p.av.ic === ic ? " ativo" : ""}" data-ic="${ic}" aria-label="${ic}" aria-pressed="${p.av.ic === ic}">${ico(ic)}</button>`).join("")}</div>` : ""}
      ${p.av.t === "foto" ? `<div class="pf-opcoes"><label class="btn-linha" tabindex="0">${x.pfFotoEscolher}<input type="file" id="pfFoto" accept="image/*" hidden></label>
        <span class="fonte" id="pfFotoAviso">${p.av.foto ? x.pfFotoOk : x.pfFotoDica}</span></div>`
        : `<div class="pf-opcoes">${Object.entries(PERFIL_CORES).map(([n, cor])=>
          `<button type="button" class="pf-cor${p.av.cor === n ? " ativo" : ""}" data-cor="${n}" style="background:${cor}" aria-label="${n}" aria-pressed="${p.av.cor === n}"></button>`).join("")}</div>`}
    </div>
    <div class="pf-campo"><span>${x.pfCapa}</span>
      <div class="pf-opcoes">${PERFIL_CAPAS.map(cp=>`<button type="button" class="pf-capa capa-${cp}${p.capa === cp ? " ativo" : ""}" data-capa="${cp}" aria-label="${x.capas[cp]}" title="${x.capas[cp]}" aria-pressed="${p.capa === cp}"><span class="perfil-capa"></span></button>`).join("")}</div></div>
    <div class="pf-campo"><label class="pf-campo"><span>${x.pfVers}</span><input id="pfVers" maxlength="40" autocomplete="off" value="${p.vers ? esc(refStr(...p.vers.split(".").map((y, i)=>i ? +y : y))) : ""}" placeholder="${x.pfVersDica}"></label>
      <div class="pf-vers-dica" id="pfVersDica" aria-live="polite"></div></div>
    <label class="pf-campo"><span>${x.pfBio}</span><textarea id="pfBio" maxlength="200" rows="2" placeholder="${x.pfBioDica}">${esc(p.bio)}</textarea></label>
    <h4 class="pf-sub">${x.pfEstudo}</h4>
    <div class="pf-campo"><span>${x.pfLetra}</span><div class="seg" role="group" aria-label="${x.pfLetra}">${Object.keys(PERFIL_LETRAS).map(k=>
      `<button type="button" data-letra="${k}" aria-pressed="${p.letra === k}" style="font-size:${PERFIL_LETRAS[k] * .82}rem">A${k === "p" ? "−" : k === "m" ? "" : k === "g" ? "+" : "++"}</button>`).join("")}</div></div>
    <div class="pf-campo"><span>${x.pfConf}</span><div class="seg" role="group" aria-label="${x.pfConf}">
      <button type="button" data-conf="westminster" aria-pressed="${p.conf === "westminster"}">${x.pfConfW}</button>
      <button type="button" data-conf="tres-formas" aria-pressed="${p.conf === "tres-formas"}">${x.pfConf3}</button></div></div>
    <div class="pf-campo"><span>${x.pfSecoes}</span><ol class="pf-secoes">${ordem.map((s, i)=>`<li>
      <label><input type="checkbox" data-sec="${s}" ${p.secoes.ocultas.includes(s) ? "" : "checked"}> ${nomesSec[s]}</label>
      <span><button type="button" class="pf-mover" data-sobe="${s}" ${i ? "" : "disabled"} aria-label="${x.pfSobe}">↑</button><button type="button" class="pf-mover" data-desce="${s}" ${i < ordem.length - 1 ? "" : "disabled"} aria-label="${x.pfDesce}">↓</button></span></li>`).join("")}</ol></div>
  </div>`;
}
function ordemSecoes(){
  const o = perfil().secoes.ordem.filter(s=>SECOES_PAINEL.includes(s));
  return o.concat(SECOES_PAINEL.filter(s=>!o.includes(s)));
}
function ligarEditorPerfil(){
  const ed = $("perfilEditor"); if(!ed) return;
  const x = t();
  const refazer = ()=>{ const rolar = $("conteudoEstudo").scrollTop; montarMeuEstudo().then(()=>{ $("conteudoEstudo").scrollTop = rolar; }); };
  let espera;
  const adiar = (fn)=>{ clearTimeout(espera); espera = setTimeout(fn, 500); };
  $("pfNome").addEventListener("input", (e)=>adiar(()=>{ salvarPerfil({ nome: e.target.value.trim() }); atualizarCartaoTopo(); }));
  $("pfBio").addEventListener("input", (e)=>adiar(()=>{ salvarPerfil({ bio: e.target.value.trim() }); atualizarCartaoTopo(); }));
  // enquanto digita: o que entendeu, o texto do versículo, ou os números para tocar quando falta o versículo
  const versosDe = async (r)=>{ try{ return (await carregarLivro(est.idioma === "en" ? "kjv" : est.idioma === "es" ? "rva" : "blivre", r.livro))[r.cap - 1] || []; }catch(e){ return []; } };
  const dicaVers = async ()=>{
    const el = $("pfVersDica"), txt = $("pfVers").value.trim(), vez = est.vezVers = (est.vezVers || 0) + 1;
    if(!txt){ el.innerHTML = ""; return; }
    const r = parseRef(txt);
    if(!r){ el.innerHTML = `<p class="fonte">${x.pfVersErro}</p>`; return; }
    if(!r.cap){ el.innerHTML = `<p class="fonte"><b>${esc(nomeLivro(r.livro))}</b> — ${x.pfVersFaltaCap}</p>`; return; }
    const versos = await versosDe(r);
    if(vez !== est.vezVers) return;
    if(r.v && versos[r.v - 1]){
      const tv = await textoVersiculoVida(`${r.livro}.${r.cap}.${r.v}`);
      el.innerHTML = `<p class="pf-vers-previa"><b>${esc(refStr(r.livro, r.cap, r.v))}</b> “${esc(tv.length > 150 ? tv.slice(0, 150).trim() + "…" : tv)}”</p>`;
      return;
    }
    el.innerHTML = `<p class="fonte"><b>${esc(nomeLivro(r.livro))} ${r.cap}</b> — ${x.pfVersEscolha}</p>
      <div class="pf-versos">${versos.map((_, i)=>`<button type="button" data-vv="${i + 1}">${i + 1}</button>`).join("")}</div>`;
    el.querySelectorAll("[data-vv]").forEach(b=>b.addEventListener("click", ()=>{ salvarPerfil({ vers: `${r.livro}.${r.cap}.${b.dataset.vv}` }); refazer(); }));
  };
  let esperaVers;
  $("pfVers").addEventListener("input", ()=>{ clearTimeout(esperaVers); esperaVers = setTimeout(dicaVers, 250); });
  $("pfVers").addEventListener("keydown", (e)=>{ if(e.key === "Enter"){ e.preventDefault(); e.target.blur(); } });
  $("pfVers").addEventListener("change", async (e)=>{
    const txt = e.target.value.trim(), r = txt ? parseRef(txt) : null;
    if(!txt){ salvarPerfil({ vers: "" }); return refazer(); }
    if(!r || !r.cap || !r.v || !(await versosDe(r))[r.v - 1]) return;    // incompleta: a dica (já à vista) mostra o que falta
    salvarPerfil({ vers: `${r.livro}.${r.cap}.${r.v}` }); refazer();
  });
  ed.querySelectorAll("[data-av]").forEach(b=>b.addEventListener("click", ()=>{ salvarPerfil({ av: { ...perfil().av, t: b.dataset.av } }); refazer(); }));
  ed.querySelectorAll("[data-ic]").forEach(b=>b.addEventListener("click", ()=>{ salvarPerfil({ av: { ...perfil().av, ic: b.dataset.ic } }); refazer(); }));
  ed.querySelectorAll("[data-cor]").forEach(b=>b.addEventListener("click", ()=>{ salvarPerfil({ av: { ...perfil().av, cor: b.dataset.cor } }); refazer(); }));
  ed.querySelectorAll("[data-capa]").forEach(b=>b.addEventListener("click", ()=>{ salvarPerfil({ capa: b.dataset.capa }); refazer(); }));
  ed.querySelectorAll("[data-letra]").forEach(b=>b.addEventListener("click", ()=>{ salvarPerfil({ letra: b.dataset.letra }); refazer(); }));
  ed.querySelectorAll("[data-conf]").forEach(b=>b.addEventListener("click", ()=>{ salvarPerfil({ conf: b.dataset.conf }); refazer(); }));
  if($("pfFoto")) $("pfFoto").addEventListener("change", async (e)=>{
    try{ const foto = await reduzirFoto(e.target.files[0]); salvarPerfil({ av: { ...perfil().av, t: "foto", foto } }); refazer(); }
    catch(err){ $("pfFotoAviso").textContent = x.pfFotoErro; }
  });
  ed.querySelectorAll("[data-sec]").forEach(c=>c.addEventListener("change", ()=>{
    const ocultas = perfil().secoes.ocultas.filter(s=>s !== c.dataset.sec).concat(c.checked ? [] : [c.dataset.sec]);
    salvarPerfil({ secoes: { ordem: ordemSecoes(), ocultas } });
  }));
  const mover = (s, d)=>{
    const o = ordemSecoes(), i = o.indexOf(s), j = i + d;
    if(j < 0 || j >= o.length) return;
    [o[i], o[j]] = [o[j], o[i]];
    salvarPerfil({ secoes: { ordem: o, ocultas: perfil().secoes.ocultas } }); refazer();
  };
  ed.querySelectorAll("[data-sobe]").forEach(b=>b.addEventListener("click", ()=>mover(b.dataset.sobe, -1)));
  ed.querySelectorAll("[data-desce]").forEach(b=>b.addEventListener("click", ()=>mover(b.dataset.desce, 1)));
}
function atualizarCartaoTopo(){
  const c = document.querySelector("#conteudoEstudo .perfil-cartao");
  if(!c) return;
  const p = perfil(), x = t();
  c.querySelector(".perfil-nome").textContent = nomeExibicao() || x.visitante;
  let bio = c.querySelector(".perfil-bio");
  if(p.bio && !bio){ bio = document.createElement("span"); bio.className = "perfil-bio"; c.querySelector(".perfil-nome").after(bio); }
  if(bio){ if(p.bio) bio.textContent = p.bio; else bio.remove(); }
  const av = c.querySelector(".conta-letra"); if(av) av.outerHTML = htmlAvatar("grande");
}

/* ----- conquistas: tudo calculado do que já está no aparelho ----- */
function sequenciaMaxima(){
  const dias = [...new Set(Object.values(est.lidos).map(diaLocal))].sort();
  let max = 0, atual = 0, ant = null;
  for(const d of dias){
    const dia = new Date(d + "T12:00:00");
    atual = ant && Math.round((dia - ant) / 864e5) === 1 ? atual + 1 : 1;
    max = Math.max(max, atual); ant = dia;
  }
  return max;
}
function conquistas(){
  const r = resumoEstudo(), livros = est.meta.books;
  const cheio = (b)=>(r.porLivro[b.id] || 0) >= b.ch;
  const grupo = (ids)=>{ const bs = livros.filter(b=>ids.includes(b.id)); return [bs.reduce((n, b)=>n + Math.min(r.porLivro[b.id] || 0, b.ch), 0), bs.reduce((n, b)=>n + b.ch, 0)]; };
  const ate = (de, a)=>{ const i = livros.findIndex(b=>b.id === de), j = livros.findIndex(b=>b.id === a); return livros.slice(i, j + 1).map(b=>b.id); };
  const at = livros.filter(b=>b.t === "AT").map(b=>b.id), nt = livros.filter(b=>b.t === "NT").map(b=>b.id);
  const seqMax = Math.max(sequenciaMaxima(), r.seq);
  let planosFeitos = 0;
  try{ planosFeitos = (est.planos || []).filter(pl=>pctPlano(pl) >= 100).length; }catch(e){}
  const lidosPrat = Object.values(est.prateleira || {}).filter(l=>l && l.st === "lido").length;
  const [pent, pentT] = grupo(ate("GEN", "DEU")), [ev, evT] = grupo(["MAT", "MRK", "LUK", "JHN"]);
  const [paulo, pauloT] = grupo(ate("ROM", "PHM")), [ntN, ntT] = grupo(nt), [atN, atT] = grupo(at);
  return [
    ["primeiro", "livro", r.lidos, 1], ["cem", "livro", r.lidos, 100], ["quinhentos", "livro", r.lidos, 500],
    ["livroInteiro", "feito", livros.filter(cheio).length, 1], ["dezLivros", "feito", livros.filter(cheio).length, 10],
    ["salmos", "coroa", Math.min(r.porLivro.PSA || 0, 150), 150], ["pentateuco", "lampada", pent, pentT],
    ["evangelhos", "cruz", ev, evT], ["paulo", "pomba", paulo, pauloT], ["nt", "cruz", ntN, ntT], ["at", "lampada", atN, atT],
    ["biblia", "coroa", r.lidos, r.total],
    ["seq7", "chama", seqMax, 7], ["seq30", "chama", seqMax, 30], ["seq100", "chama", seqMax, 100],
    ["plano", "planos", planosFeitos, 1], ["notas10", "anotacoes", r.notas, 10], ["marcas50", "ancora", r.marcas, 50],
    ["prateleira5", "estante", lidosPrat, 5],
  ].map(([id, ic, n, meta])=>({ id, ic, n: Math.min(n, meta), meta, feito: n >= meta }));
}
function htmlConquistas(x){
  const lista = conquistas(), feitas = lista.filter(c=>c.feito).length;
  return `<h3 class="estudo-sub">${x.conquistasTit} <small class="sub-conta">${feitas}/${lista.length}</small></h3>
    <div class="selos">${lista.map(c=>{
      const nome = x.selos[c.id] || c.id, pct = Math.round(c.n / c.meta * 100);
      return `<div class="selo${c.feito ? " feito" : ""}" title="${esc(nome + " — " + c.n + "/" + c.meta)}">
        <span class="selo-ic">${ico(c.ic)}</span><b>${esc(nome)}</b>
        ${c.feito ? `<small>${x.conquistado}</small>` : `<small>${c.n.toLocaleString(est.idioma)}/${c.meta.toLocaleString(est.idioma)}</small><div class="plano-barra"><i style="width:${pct}%"></i></div>`}
      </div>`; }).join("")}</div>`;
}

/* ----- prateleira: os livros teológicos da pessoa (catálogo em data/prateleira.json + livros à mão) ----- */
async function catalogoPrateleira(){
  if(!est.catPrateleira){ try{ est.catPrateleira = await json("data/prateleira.json"); }catch(e){ est.catPrateleira = { tradicoes:{}, obras:[] }; } }
  return est.catPrateleira;
}
const ST_LIVRO = ["lendo", "lido", "quero"];
function livroValido(id, v){
  if(!v || typeof v !== "object" || !ST_LIVRO.includes(v.st) || !/^[a-z0-9-]{1,40}$/.test(id)) return null;
  const s = (x, n)=>typeof x === "string" ? x.slice(0, n).trim() : "";
  const o = { st: v.st, em: +v.em > 0 ? +v.em : Date.now() };
  if(id.startsWith("u-")){ o.t = s(v.t, 120); o.a = s(v.a, 80); if(!o.t) return null; }
  const nota = s(v.nota, 300); if(nota) o.nota = nota;
  return o;
}
function salvarLivro(id, v){
  est.prateleira = est.prateleira || {};
  const ok = v && livroValido(id, v);
  if(ok) est.prateleira[id] = ok; else delete est.prateleira[id];
  gravarLS("logos_prateleira", est.prateleira); tocar("estado", "livro:" + id);
}
function obraDe(id, cat){
  const own = (est.prateleira || {})[id] || {};
  const o = cat.obras.find(b=>b.id === id);
  return o ? { ...o, ...own, catalogo: true } : { id, t: own.t || "?", a: own.a || "", ano: "", tr: "", liga: [], ...own };
}
function htmlPrateleira(x, cat){
  const meus = Object.keys(est.prateleira || {}).map(id=>obraDe(id, cat)).sort((a, b)=>(b.em || 0) - (a.em || 0));
  const lombada = (o)=>{
    const alt = 7 + (o.t.length % 5) * .45;
    return `<button type="button" class="lombada tr-${o.tr || "outra"}${est.livroAberto === o.id ? " aberta" : ""}" data-livro="${esc(o.id)}" style="height:${alt}rem" title="${esc(o.t + (o.a ? " — " + o.a : ""))}"><span>${esc(o.t)}</span></button>`;
  };
  const prateleiras = ST_LIVRO.map(st=>{
    const l = meus.filter(o=>o.st === st);
    return l.length ? `<div class="prat"><p class="prat-rot">${x.stLivro[st]} <small>${l.length}</small></p><div class="prat-livros">${l.map(lombada).join("")}</div></div>` : "";
  }).join("");
  const aberto = est.livroAberto && est.prateleira && est.prateleira[est.livroAberto] ? obraDe(est.livroAberto, cat) : null;
  const tradNome = (tr)=>tr && cat.tradicoes[tr] ? (cat.tradicoes[tr][est.idioma] || cat.tradicoes[tr].pt) : "";
  const ficha = aberto ? `<div class="prat-ficha">
      <button type="button" class="lugar-fechar" data-fechar-livro aria-label="${x.fechar}">✕</button>
      <h4>${esc(emPT() || !aberto.o ? aberto.t : aberto.o)}</h4>
      <p class="fonte">${esc([aberto.a, aberto.ano, tradNome(aberto.tr)].filter(Boolean).join(" · "))}</p>
      ${aberto.liga && aberto.liga.length ? `<p class="prat-liga">${x.ligaSola}: ${aberto.liga.map(([r, u])=>`<a href="${esc(u)}">${esc(r)}</a>`).join(" · ")}</p>` : ""}
      <div class="prat-acoes"><select data-st-livro="${esc(aberto.id)}">${ST_LIVRO.map(s=>`<option value="${s}"${aberto.st === s ? " selected" : ""}>${x.stLivro[s]}</option>`).join("")}</select>
        <button type="button" class="btn-linha" data-tirar-livro="${esc(aberto.id)}">${x.tirarLivro}</button></div>
    </div>` : "";
  const busca = est.prateleiraBusca;
  const adicionar = busca !== undefined ? `<div class="prat-add">
      <div class="prat-add-topo"><input id="pratBusca" type="search" value="${esc(busca)}" placeholder="${x.pratBuscaDica}" aria-label="${x.pratBuscaDica}">
        <label>${x.pratComo} <select id="pratSt">${ST_LIVRO.map(s=>`<option value="${s}"${(est.pratSt || "lido") === s ? " selected" : ""}>${x.stLivro[s]}</option>`).join("")}</select></label></div>
      <div class="prat-grupos" role="group" aria-label="${x.pratGrupoRot}">${["todos", "teologia", "filosofia", "apologetica", "devocional", "literatura", "biografia"].map(g=>
        `<button type="button" data-grupo="${g}" aria-pressed="${(est.pratGrupo || "todos") === g}">${x.pratGrupos[g]}</button>`).join("")}</div>
      <ul class="prat-cat">${cat.obras.filter(o=>!(est.prateleira || {})[o.id] && ((est.pratGrupo || "todos") === "todos" || o.g === est.pratGrupo)
        && (!busca || normStr(o.t + " " + o.o + " " + o.a).includes(normStr(busca)))).slice(0, 40)
        .map(o=>`<li><button type="button" data-por-livro="${esc(o.id)}"><b>${esc(o.t)}</b> <small>${esc(o.a)}, ${esc(o.ano)}</small></button></li>`).join("")}</ul>
      <form id="pratOutro" class="prat-outro"><span>${x.pratOutro}</span>
        <input name="t" maxlength="120" required placeholder="${x.pratTitulo}" aria-label="${x.pratTitulo}">
        <input name="a" maxlength="80" placeholder="${x.pratAutor}" aria-label="${x.pratAutor}">
        <button class="btn-linha">${x.pratPor}</button></form>
      <p><button type="button" class="link-discreto" id="pratFechar">${x.fechar}</button></p>
    </div>` : `<p><button type="button" class="btn-linha" id="pratAbrir">+ ${x.pratAdicionar}</button></p>`;
  return `<h3 class="estudo-sub">${x.prateleiraTit} <small class="sub-conta">${meus.length}</small></h3>
    ${meus.length ? prateleiras : `<p class="fonte">${x.pratVazia}</p>`}${ficha}${adicionar}`;
}
function ligarPrateleira(raiz){
  const refazer = (foco)=>{
    const rolar = $("conteudoEstudo").scrollTop;
    montarMeuEstudo().then(()=>{ $("conteudoEstudo").scrollTop = rolar; if(foco && $(foco)){ $(foco).focus(); const v = $(foco).value; $(foco).setSelectionRange && $(foco).setSelectionRange(v.length, v.length); } });
  };
  raiz.querySelectorAll("[data-livro]").forEach(b=>b.addEventListener("click", ()=>{ est.livroAberto = est.livroAberto === b.dataset.livro ? null : b.dataset.livro; refazer(); }));
  raiz.querySelectorAll("[data-fechar-livro]").forEach(b=>b.addEventListener("click", ()=>{ est.livroAberto = null; refazer(); }));
  raiz.querySelectorAll("[data-st-livro]").forEach(s=>s.addEventListener("change", ()=>{ const id = s.dataset.stLivro; salvarLivro(id, { ...est.prateleira[id], st: s.value, em: Date.now() }); refazer(); }));
  raiz.querySelectorAll("[data-tirar-livro]").forEach(b=>b.addEventListener("click", ()=>{ salvarLivro(b.dataset.tirarLivro, null); est.livroAberto = null; refazer(); }));
  if($("pratAbrir")) $("pratAbrir").addEventListener("click", ()=>{ est.prateleiraBusca = ""; refazer("pratBusca"); });
  if($("pratFechar")) $("pratFechar").addEventListener("click", ()=>{ est.prateleiraBusca = undefined; refazer(); });
  let espera;
  if($("pratBusca")) $("pratBusca").addEventListener("input", (e)=>{ clearTimeout(espera); espera = setTimeout(()=>{ est.prateleiraBusca = e.target.value; refazer("pratBusca"); }, 250); });
  if($("pratSt")) $("pratSt").addEventListener("change", (e)=>{ est.pratSt = e.target.value; });
  raiz.querySelectorAll("[data-grupo]").forEach(b=>b.addEventListener("click", ()=>{ est.pratGrupo = b.dataset.grupo; refazer(); }));
  raiz.querySelectorAll("[data-por-livro]").forEach(b=>b.addEventListener("click", ()=>{ salvarLivro(b.dataset.porLivro, { st: est.pratSt || "lido", em: Date.now() }); convidar("lido"); refazer("pratBusca"); }));
  if($("pratOutro")) $("pratOutro").addEventListener("submit", (e)=>{
    e.preventDefault();
    const f = e.target, id = "u-" + Date.now().toString(36);
    salvarLivro(id, { st: est.pratSt || "lido", t: f.t.value, a: f.a.value, em: Date.now() });
    refazer("pratBusca");
  });
}

/* ---------- painel "Meu estudo": a semana, a meta e o histórico ---------- */
const METAS_SEMANA = [0, 7, 14, 21, 28, 35, 50];
function inicioDia(d){ d = new Date(d); d.setHours(0, 0, 0, 0); return d; }
/* capítulos lidos por dia ({"2026-11-19": 3}) */
function leiturasPorDia(){
  const n = {};
  for(const em of Object.values(est.lidos)){ const d = diaLocal(em); n[d] = (n[d] || 0) + 1; }
  return n;
}
function htmlSemana(x){
  const porDia = leiturasPorDia(), hoje = inicioDia(Date.now());
  const ini = new Date(hoje); ini.setDate(ini.getDate() - ini.getDay());          // a semana começa no domingo
  const dias = [...Array(7)].map((_, i)=>{ const d = new Date(ini); d.setDate(d.getDate() + i); return d; });
  const valores = dias.map(d=>porDia[diaLocal(d)] || 0);
  const semana = valores.reduce((a, b)=>a + b, 0), comLeitura = valores.filter(Boolean).length;
  let antes = 0;
  for(let i = 1; i <= 7; i++){ const d = new Date(ini); d.setDate(d.getDate() - i); antes += porDia[diaLocal(d)] || 0; }
  const topo = Math.max(3, ...valores);
  const fmt = (d)=>d.toLocaleDateString(est.idioma, { weekday:"long", day:"numeric", month:"short" });
  const barras = dias.map((d, i)=>{
    const v = valores[i], futuro = d > hoje, eHoje = +d === +hoje;
    const dica = x.capsNoDia.replace("{n}", v).replace("{d}", fmt(d));
    return `<div class="sem-dia${eHoje ? " hoje" : ""}${futuro ? " futuro" : ""}" title="${esc(dica)}" aria-label="${esc(dica)}">
      <span class="sem-val">${v || ""}</span><i style="height:${v ? Math.max(8, Math.round(v / topo * 100)) : 0}%"></i>
      <span class="sem-rot">${x.diasSem[i]}</span></div>`;
  }).join("");
  const meta = est.metaSemana, pctMeta = meta ? Math.min(100, Math.round(semana / meta * 100)) : 0;
  const opcoes = METAS_SEMANA.map(n=>`<option value="${n}"${n === meta ? " selected" : ""}>${n ? n + " " + x.metaCaps : x.metaSem}</option>`).join("");
  return `<h3 class="estudo-sub">${x.semanaTit}</h3>
    <div class="semana">
      <div class="sem-barras" role="img" aria-label="${esc(x.semanaTit)}">${barras}</div>
      <div class="sem-resumo">
        <p><b>${semana}</b> ${x.semanaCaps} · <b>${comLeitura}</b> ${x.semanaDias}</p>
        <p class="fonte">${x.semanaAntes}: ${antes}</p>
        <label class="sem-meta">${x.metaRot} <select id="selMeta">${opcoes}</select></label>
        ${meta ? `<div class="plano-barra"><i style="width:${pctMeta}%"></i></div>
          <p class="fonte">${semana >= meta ? x.metaFeita : x.metaFalta.replace("{n}", meta - semana)}</p>` : ""}
      </div>
    </div>`;
}
/* 12 semanas em quadradinhos (colunas = semanas, linhas = dias), um tom só, do claro ao escuro */
function htmlHistorico(x){
  const porDia = leiturasPorDia(), hoje = inicioDia(Date.now());
  const ini = new Date(hoje); ini.setDate(ini.getDate() - ini.getDay() - 7 * 11);
  const nivel = (v)=>v === 0 ? 0 : v === 1 ? 1 : v <= 3 ? 2 : v <= 6 ? 3 : 4;
  let cels = "";
  for(let s = 0; s < 12; s++) for(let d = 0; d < 7; d++){
    const dia = new Date(ini); dia.setDate(dia.getDate() + s * 7 + d);
    if(dia > hoje){ cels += `<i class="hm-cel vazio"></i>`; continue; }
    const v = porDia[diaLocal(dia)] || 0;
    const dica = x.capsNoDia.replace("{n}", v).replace("{d}", dia.toLocaleDateString(est.idioma, { day:"numeric", month:"short" }));
    cels += `<i class="hm-cel n${nivel(v)}" title="${esc(dica)}"></i>`;
  }
  return `<h3 class="estudo-sub">${x.historicoTit}</h3>
    <div class="hm" role="img" aria-label="${esc(x.historicoTit)}">${cels}</div>
    <p class="hm-escala"><span>${x.menos}</span>${[0,1,2,3,4].map(n=>`<i class="hm-cel n${n}"></i>`).join("")}<span>${x.mais}</span></p>`;
}
function htmlRecentes(x){
  const lista = Object.entries(est.lidos).filter(([k])=>capValido(k)).sort((a, b)=>b[1] - a[1]).slice(0, 8);
  if(!lista.length) return "";
  const hoje = +inicioDia(Date.now());
  const quando = (em)=>{
    const dias = Math.round((hoje - +inicioDia(em)) / 864e5);
    return dias <= 0 ? x.hoje : dias === 1 ? x.ontem : dias < 7 ? x.haDias.replace("{n}", dias)
      : new Date(em).toLocaleDateString(est.idioma, { day:"numeric", month:"short" });
  };
  return `<h3 class="estudo-sub">${x.recentesTit}</h3><ul class="recentes">` + lista.map(([k, em])=>{
    const [l, c] = k.split(".");
    return `<li>${linkRef(l, +c, 0, esc(nomeLivro(l) + " " + c), "")}<small>${quando(em)}</small></li>`;
  }).join("") + `</ul>`;
}

/* ---------- painel "Meu estudo" ---------- */
async function montarMeuEstudo(){
  const x = t(), r = resumoEstudo(), alvo = $("conteudoEstudo");
  document.querySelectorAll("#abasEstudo .aba").forEach(b=>{
    const minha = b.dataset.aba === est.abaEstudo;
    b.textContent = b.dataset.aba === "perfil" ? x.abaPerfil : x.abaEstudo;
    b.classList.toggle("ativa", minha); b.setAttribute("aria-selected", minha);
    b.onclick = ()=>{ est.abaEstudo = b.dataset.aba; montarMeuEstudo(); };
  });
  $("tituloEstudo").textContent = est.abaEstudo === "perfil" ? x.abaPerfil : x.meuEstudo;
  const ligarCompartilhar = ()=>alvo.querySelectorAll(".perfil-compartilhar").forEach(b=>b.addEventListener("click", compartilharPerfil));
  if(est.abaEstudo === "perfil"){ alvo.innerHTML = perfilHTML(); ligarPerfil(); ligarConta(); ligarPaginaPublica(); ligarEditorPerfil(); preencherVersiculoVida(alvo); ligarCompartilhar(); return; }
  const ult = lerLS("logos_ultimo", null);
  const pct = r.total ? Math.round(r.lidos / r.total * 1000) / 10 : 0;
  const livros = (tst)=>est.meta.books.filter(b=>b.t===tst).map(b=>{
    const n = r.porLivro[b.id] || 0;
    return `<a class="lv${n >= b.ch ? " cheio" : ""}" href="${urlLivro(b.id)}" style="--p:${Math.round(n / b.ch * 100)}%"><span>${esc(nomeLivro(b.id))}</span><small>${n}/${b.ch}</small></a>`;
  }).join("");
  const marcas = Object.keys(est.marcas).filter(chaveValida).sort(ordemRef);
  const notas = Object.keys(est.notas).filter(chaveValida).sort(ordemRef);
  let planosHTML = "", cat = { tradicoes:{}, obras:[] };
  try{ cat = await catalogoPrateleira(); }catch(e){}
  try{ planosHTML = (await planos()).map(pl=>{ const p = pctPlano(pl); return p ? `<div class="plano-linha"><span>${esc(pl.nome[est.idioma]||pl.nome.pt)}</span><div class="plano-barra"><i style="width:${p}%"></i></div><small>${p}%</small></div>` : ""; }).join(""); }catch(e){}
  const secoes = {
    semana: ()=>htmlSemana(x), historico: ()=>htmlHistorico(x), recentes: ()=>htmlRecentes(x),
    conquistas: ()=>htmlConquistas(x), prateleira: ()=>`<div id="secPrateleira">${htmlPrateleira(x, cat)}</div>`,
    livros: ()=>`<h3 class="estudo-sub">${x.progLivros}</h3>
    ${r.lidos ? "" : `<p class="fonte">${x.semLeitura}</p>`}
    <p class="rotulo-secao pequeno">${x.at}</p><div class="lvs">${livros("AT")}</div>
    <p class="rotulo-secao pequeno">${x.nt}</p><div class="lvs">${livros("NT")}</div>`,
    planos: ()=>planosHTML ? `<h3 class="estudo-sub">${x.planosTit}</h3>${planosHTML}` : "",
    marcacoes: ()=>`<h3 class="estudo-sub">${x.marcacoes}</h3>
    ${marcas.length ? `<div class="marcas-lista">` + marcas.slice(0, 120).map(k=>{ const [l, c, v] = k.split("."); return linkRef(l, +c, +v, esc(refStr(l, +c, +v)), "m-chip m-" + est.marcas[k]); }).join("") + `</div>` : `<p class="fonte">${x.semMarcas}</p>`}`,
    notas: ()=>`<h3 class="estudo-sub">${x.notas}</h3>
    ${notas.length ? notas.slice(0, 4).map(k=>{ const [l, c, v] = k.split("."); return `<p class="nota-curta">${linkRef(l, +c, +v, esc(refStr(l, +c, +v)), "")} ${esc(est.notas[k].slice(0, 140))}${est.notas[k].length > 140 ? "…" : ""}</p>`; }).join("") : ""}
    <p><button class="btn-linha" id="btnTodasNotas">${notas.length ? x.verTodas + " (" + notas.length + ")" : x.notas}</button></p>`,
  };
  const ocultas = perfil().secoes.ocultas;
  alvo.innerHTML = htmlCartaoPerfil(x, `<button type="button" class="link-discreto perfil-editar" id="btnEditarPerfil">${x.personalizar}</button>`) + faixaConta() + `
    <div class="estudo-numeros">
      <div class="num largo"><b>${r.lidos.toLocaleString(est.idioma)}</b><span>${x.de} ${r.total.toLocaleString(est.idioma)} ${x.capsLidos} · ${pct.toLocaleString(est.idioma)}%</span>
        <div class="plano-barra"><i style="width:${pct}%"></i></div></div>
      <div class="num">${ico("chama")}<b>${r.seq}</b><span>${x.diasSeguidos}</span></div>
      <div class="num"><b>${r.notas}</b><span>${x.nNotasRot}</span></div>
      <div class="num"><b>${r.marcas}</b><span>${x.nMarcasRot}</span></div>
    </div>
    ${ult && infoLivro(ult.livro) ? `<p class="estudo-continuar"><a class="btn-ouro" href="${urlCapitulo(ult.livro, ult.cap)}">${x.continuar} ${esc(nomeLivro(ult.livro))} ${+ult.cap} ${ico("seta")}</a></p>` : ""}
    ` + ordemSecoes().filter(s=>!ocultas.includes(s)).map(s=>secoes[s]()).join("");
  preencherVersiculoVida(alvo); ligarCompartilhar();
  if($("secPrateleira")) ligarPrateleira($("secPrateleira"));
  $("btnEditarPerfil").addEventListener("click", ()=>{ est.abaEstudo = "perfil"; montarMeuEstudo().then(()=>{ const ed = $("perfilEditor"); if(ed) ed.scrollIntoView({ block:"start" }); }); });
  if($("btnTodasNotas")) $("btnTodasNotas").addEventListener("click", ()=>{ montarNotas(); alternarPainel("painelNotas", true); });
  if($("selMeta")) $("selMeta").addEventListener("change", (e)=>{
    est.metaSemana = +e.target.value || 0; gravarLS("logos_meta_semana", est.metaSemana); tocar("estado", "meta");
    const rolar = $("conteudoEstudo").scrollTop; montarMeuEstudo().then(()=>{ $("conteudoEstudo").scrollTop = rolar; });
  });
  if($("faixaEntrar")) $("faixaEntrar").addEventListener("click", ()=>{ est.abaEstudo = "perfil"; montarMeuEstudo(); });
}
function abrirMeuEstudo(aba){ est.abaEstudo = aba === "perfil" ? "perfil" : "estudo"; montarMeuEstudo(); alternarPainel("painelEstudo", true); }
/* Na aba Estudo, a conta aparece só como uma faixa: o convite para entrar ou o estado da sincronização. */
function faixaConta(){
  const x = t();
  if(!temConta()) return `<p class="conta-local">${x.contaLocal}</p>`;
  if(!est.sessao) return `<button class="faixa-conta" id="faixaEntrar">${ico("nuvem")}<span><strong>${x.contaTitulo}.</strong> ${x.faixaTexto}</span>${ico("seta")}</button>`;
  return `<p class="faixa-sinc">${ico("nuvem")} <span id="sincEstado" role="status">${textoSinc()}</span></p>`;
}
const nomeUsuario = (u)=>(u.user_metadata && (u.user_metadata.full_name || u.user_metadata.name)) || u.email || "";

/* ---------- aba Perfil: conta, preferências e dados ---------- */
function perfilHTML(){
  const x = t(), u = est.sessao && est.sessao.user;
  const nome = u ? nomeUsuario(u) : x.visitante;
  const desde = u && u.created_at ? new Date(u.created_at).toLocaleDateString(est.idioma, { month:"long", year:"numeric" }) : "";
  let conta = "";
  if(!temConta()) conta = `<p class="conta-local">${x.contaLocal}</p>`;
  else if(!u) conta = `<div class="conta-caixa">
      <div><h3>${ico("nuvem")} ${x.contaTitulo}</h3><p>${x.contaTexto}</p>
        <ul class="conta-vantagens">${x.vantagens.map(v=>`<li>${ico("feito")} ${v}</li>`).join("")}</ul></div>
      <div class="conta-acoes">
        ${CONTA.google ? `<button class="btn-ouro" id="btnGoogle">${x.entrarGoogle}</button>` : ""}
        ${CONTA.email ? `<form id="formEmail"><input type="email" required autocomplete="email" placeholder="${x.seuEmail}" aria-label="${x.seuEmail}"><button class="btn-linha">${x.entrarEmail}</button></form>` : ""}
      </div>
      <p class="fonte" id="contaAviso" role="status"></p></div>`;
  else conta = `<div class="conta-acoes"><button class="btn-linha" id="btnSincAgora">${x.sincAgora}</button><button class="btn-linha" id="btnSair">${x.sair}</button></div>
      <p class="fonte" id="contaAviso" role="status"></p>`;
  return htmlCartaoPerfil(x, `<span class="perfil-conta">${u ? `${esc(u.email || "")}${desde ? ` · ${x.desde} ${esc(desde)}` : ""}</span><span class="perfil-conta" id="sincEstado" role="status">${textoSinc()}`
            : x.visitanteTexto}</span>`) + `
    ${conta}
    ${htmlPaginaPublica(x)}
    <h3 class="estudo-sub">${x.personalizar}</h3>
    ${htmlEditorPerfil(x)}
    <h3 class="estudo-sub">${x.preferencias}</h3>
    <div class="prefs">
      <label><span>${x.idioma}</span><select data-espelho="selIdioma"></select></label>
      <label><span>${x.traducao}</span><select data-espelho="selTraducao"></select></label>
      <label><span>${x.comparar}</span><select data-espelho="selComparar"></select></label>
      <div class="pref-linha"><span>${x.temaRot}</span><div class="seg" role="group" aria-label="${x.temaRot}">
        <button data-tema="claro" aria-pressed="${est.tema !== "escuro"}">${ico("sol")} ${x.claro}</button>
        <button data-tema="escuro" aria-pressed="${est.tema === "escuro"}">${ico("lua")} ${x.escuro}</button></div></div>
      <label class="pref-linha"><span>${x.leituraCorrida}</span><input type="checkbox" id="prefCorrida" ${est.corrida ? "checked" : ""}></label>
      <label class="pref-linha"><span>${x.prefChave}</span><input type="checkbox" id="prefChave" ${est.chave ? "checked" : ""}></label>
      <label class="pref-linha"><span>${x.prefVoc}</span><input type="checkbox" id="prefVoc" ${est.voc ? "checked" : ""}></label>
    </div>
    <h3 class="estudo-sub">${x.seusDados}</h3>
    <div class="conta-acoes">
      <button class="btn-linha" id="perfilBackup">⬇ ${x.backup}</button>
      <label class="btn-linha" for="perfilArq" tabindex="0">⬆ ${x.restaurar}</label>
      <input type="file" id="perfilArq" accept=".json,application/json" style="display:none">
      <button class="btn-linha" id="perfilOffline">${ico("baixar")} ${x.lerOffline}</button>
    </div>
    <p class="fonte" id="perfilAviso" role="status"></p>
    <p class="estudo-rodape"><a href="/privacidade/">${x.privacidade}</a>${u ? ` · <button class="link-discreto" id="btnExcluirConta">${x.excluirConta}</button>` : ""}</p>`;
}
function ligarPerfil(){
  // os seletores do perfil espelham os da barra de leitura: mudar aqui é mudar lá
  document.querySelectorAll("#conteudoEstudo select[data-espelho]").forEach(sel=>{
    const orig = $(sel.dataset.espelho);
    sel.innerHTML = orig.innerHTML; sel.value = orig.value;
    sel.addEventListener("change", ()=>{ orig.value = sel.value; orig.dispatchEvent(new Event("change")); montarMeuEstudo(); });
  });
  document.querySelectorAll("#conteudoEstudo .seg button").forEach(b=>b.addEventListener("click", ()=>{
    est.tema = b.dataset.tema; gravarLS("logos_tema", est.tema); aplicarTema(); montarMeuEstudo();
  }));
  $("prefCorrida").addEventListener("change", ()=>$("btnCorrida").click());
  [["prefChave", "chave", "logos_chave"], ["prefVoc", "voc", "logos_voc"]].forEach(([id, campo, chaveLS])=>
    $(id).addEventListener("change", (e)=>{
      est[campo] = e.target.checked; gravarLS(chaveLS, est[campo]);
      if(est.vista === "cap") renderizar({ manter:true });
    }));
  $("perfilBackup").addEventListener("click", exportarBackup);
  document.querySelector('label[for="perfilArq"]').addEventListener("keydown", (e)=>{ if(e.key==="Enter") $("perfilArq").click(); });
  $("perfilArq").addEventListener("change", (e)=>{
    const f = e.target.files[0]; if(!f) return;
    importarBackup(f, (msg)=>{ e.target.value = ""; $("perfilAviso").textContent = msg; });
  });
  $("perfilOffline").addEventListener("click", ()=>alternarPainel("painelSobre", true));
}
/* O botão de perfil no topo mostra a inicial de quem entrou. */
function atualizarBotaoPerfil(){
  const u = est.sessao && est.sessao.user, b = $("btnPerfil");
  b.innerHTML = u || perfilPersonalizado() ? htmlAvatar("mini") : ico("pessoa");
  b.title = nomeExibicao() || t().abaPerfil;
  b.setAttribute("aria-label", b.title);
}

/* ---------- conta: entrar, sair, excluir ---------- */
const temConta = ()=>!!(CONTA.url && CONTA.chave && (CONTA.google || CONTA.email));
function carregarScript(src){
  return new Promise((res, rej)=>{
    const js = document.createElement("script");
    js.src = src; js.onload = res; js.onerror = ()=>rej(new Error(src));
    document.head.appendChild(js);
  });
}
/* O cliente do Supabase (220 KB) só é carregado quando faz falta: sessão guardada, volta do login ou clique em "Entrar". */
async function clienteConta(){
  if(!temConta()) return null;
  if(!est.sb){
    if(!window.supabase) await carregarScript("/vendor/supabase/supabase.js");
    est.sb = window.supabase.createClient(CONTA.url, CONTA.chave,
      { auth:{ flowType:"pkce", persistSession:true, autoRefreshToken:true, detectSessionInUrl:true, storageKey:"sola-conta" } });
    // fora do retorno de chamada: a biblioteca não deixa chamar o próprio Supabase de dentro dele
    est.sb.auth.onAuthStateChange((evento, sessao)=>{ setTimeout(()=>aoMudarSessao(sessao), 0); });
  }
  return est.sb;
}
function textoSinc(){
  const x = t();
  if(est.sincEstado === "indo") return x.sincIndo;
  if(est.sincEstado === "erro") return x.sincErro;
  return est.sinc.ultima ? `${x.sincOk} · ${new Date(est.sinc.ultima).toLocaleTimeString(est.idioma, { hour:"2-digit", minute:"2-digit" })}` : "";
}
function estadoSinc(e){ est.sincEstado = e; const el = $("sincEstado"); if(el) el.textContent = textoSinc(); }
function avisoConta(texto){ const el = $("contaAviso"); if(el) el.textContent = texto; }
/* Guarda onde a pessoa estava e manda para o login; devolve false se não deu (sem rede, por exemplo). */
async function entrar(como){
  try{
    const sb = await clienteConta();
    try{ sessionStorage.setItem("sola_volta", location.pathname + location.hash); }catch(e){}
    const { error } = await como(sb);
    if(error) throw error;
    return true;
  }catch(e){ console.warn("conta", e); return false; }
}
const entrarGoogle = ()=>entrar(sb=>sb.auth.signInWithOAuth({ provider:"google", options:{ redirectTo: location.origin + "/" } }));
function ligarConta(){
  const x = t(), em = (id, f)=>{ const el = $(id); if(el) el.addEventListener("click", f); };
  em("btnGoogle", async ()=>{ if(!await entrarGoogle()) avisoConta(x.erroConta); });
  const fe = $("formEmail");
  if(fe) fe.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const email = fe.querySelector("input").value.trim();
    const ok = await entrar(sb=>sb.auth.signInWithOtp({ email, options:{ emailRedirectTo: location.origin + "/" } }));
    avisoConta(ok ? `${x.linkEnviado} ${email}.` : x.erroConta);
  });
  em("btnSincAgora", ()=>sincronizar());
  em("btnSair", async ()=>{
    await sincronizar();                       // sobe o que faltava antes de sair
    try{ await est.sb.auth.signOut(); }catch(e){}
  });
  em("btnExcluirConta", async ()=>{
    if(!confirm(x.excluirConfirma)) return;
    try{
      const { error } = await est.sb.rpc("apagar_conta");
      if(error) throw error;
      est.sinc = { pend:{}, cursor:null, conta:null, ultima:0 }; gravarLS("logos_sinc", est.sinc);
      try{ await est.sb.auth.signOut({ scope:"local" }); }catch(e){}
      est.sessao = null; await montarMeuEstudo(); avisar(x.contaExcluida, null, null, 7000);
    }catch(e){ console.warn("conta", e); avisoConta(x.erroConta); }
  });
}
function temDadosLocais(){ return Object.keys(DADOS).some(tp=>tp !== "estado" && DADOS[tp].chaves().length); }
async function aoMudarSessao(sessao){
  const antes = est.sessao && est.sessao.user.id, agora = sessao && sessao.user && sessao.user.id;
  est.sessao = sessao && sessao.user ? sessao : null;
  if(agora && agora !== antes){
    const s = est.sinc;
    if(s.conta && s.conta !== agora){
      // este aparelho tem o estudo de outra conta: não se mistura; a pessoa decide
      if(temDadosLocais() && !confirm(t().contaOutra)){ est.sessao = null; try{ await est.sb.auth.signOut(); }catch(e){} return; }
      for(const tp of Object.keys(DADOS)) if(tp !== "estado"){ DADOS[tp].chaves().forEach(k=>DADOS[tp].por(k, null)); DADOS[tp].salvar(); }
      try{ localStorage.removeItem("logos_ultimo"); localStorage.removeItem("logos_pub_enviado"); }catch(e){}
      s.pend = {}; s.cursor = null;
    } else if(!s.conta){
      // primeira vez neste aparelho: o que já existe aqui entra na conta (no mesmo item, vale o mais recente)
      for(const tp of Object.keys(DADOS)) for(const k of DADOS[tp].chaves()) if(!s.pend[tp + "|" + k]) s.pend[tp + "|" + k] = 1;
      s.cursor = null;
    }
    s.conta = agora; gravarLS("logos_sinc", s);
    await sincronizar();
    atualizarTelas(new Set(Object.keys(DADOS)));   // inclusive quando o aparelho foi esvaziado para a outra conta
  }
  atualizarBotaoPerfil();
  if(est.sessao && est.fecharConvite) est.fecharConvite(false);
  if(!$("painelEstudo").classList.contains("oculto")) montarMeuEstudo();
}

/* ---------- convite para entrar na conta ---------- */
/* Um cartão discreto, no máximo uma vez por visita, em momentos em que a conta ajuda de verdade (a pessoa acabou
   de anotar, marcar ou ler). "Agora não" adia por dias, cada vez mais: 3, 7, 30, 90. */
const CONVITE_ESPERA = [3, 7, 30, 90];
function podeConvidar(){
  if(!temConta() || !CONTA.google || est.sessao || est.fecharConvite || painelAberto() || navigator.onLine === false) return false;
  try{ if(localStorage.getItem("sola-conta") || sessionStorage.getItem("sola_convidou")) return false; }catch(e){ return false; }
  const c = lerLS("logos_convite", null);
  return !c || Date.now() > c.ate;
}
function convidar(motivo){
  if(!podeConvidar()) return;
  clearTimeout(est.timerConvite);
  est.timerConvite = setTimeout(()=>{
    if(podeConvidar() && !est.gaveta && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) mostrarConvite(motivo);
  }, 1500);
}
function mostrarConvite(motivo){
  const x = t(), el = document.createElement("aside");
  el.className = "convite"; el.id = "convite";
  el.setAttribute("role", "dialog"); el.setAttribute("aria-labelledby", "conviteTit");
  el.innerHTML = `<button class="fechar" aria-label="${x.fechar}">✕</button>
    <p class="heroi-sobre">${x.conviteSobre}</p>
    <h3 id="conviteTit">${x.convites[motivo] || x.convites.padrao}</h3>
    <p>${x.conviteTexto}</p>
    <div class="convite-acoes"><button class="btn-ouro" id="conviteEntrar">${x.entrarGoogle}</button><button id="conviteDepois">${x.agoraNao}</button></div>
    <p class="fonte" id="conviteAviso" role="status"></p>`;
  document.body.appendChild(el);
  try{ sessionStorage.setItem("sola_convidou", "1"); }catch(e){}
  est.fecharConvite = (adiar)=>{
    el.remove(); est.fecharConvite = null;
    if(adiar){
      const n = ((lerLS("logos_convite", null) || {}).n || 0) + 1;
      gravarLS("logos_convite", { n, ate: Date.now() + CONVITE_ESPERA[Math.min(n, CONVITE_ESPERA.length) - 1] * 864e5 });
    }
  };
  el.querySelector(".fechar").addEventListener("click", ()=>est.fecharConvite(true));
  $("conviteDepois").addEventListener("click", ()=>est.fecharConvite(true));
  $("conviteEntrar").addEventListener("click", async ()=>{ if(!await entrarGoogle()) $("conviteAviso").textContent = x.erroConta; });
}

/* ---------- convite para instalar (PWA) ----------
   O site já é instalável (manifest + sw.js), mas quase ninguém sabe. Depois de 3 dias de uso, um aviso discreto, no
   máximo um por visita (o mesmo controle do convite da conta) e com o mesmo adiamento progressivo (logos_instalar).
   Android/Chrome: o botão chama o pedido do navegador (beforeinstallprompt). iPhone: não há pedido; mostra o caminho. */
const instalado = ()=>matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
const ehIOS = ()=>/iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
window.addEventListener("beforeinstallprompt", (e)=>{ e.preventDefault(); est.pedidoInstalar = e; });
window.addEventListener("appinstalled", ()=>{ est.pedidoInstalar = null; gravarLS("logos_instalar", { n: 9, ate: Date.now() + 3650 * 864e5 }); });
function contarDiaDeUso(){
  const hoje = new Date().toDateString(), v = lerLS("logos_visitas", { n: 0, dia: "" });
  if(v.dia !== hoje) gravarLS("logos_visitas", { n: (v.n || 0) + 1, dia: hoje });
}
function convidarInstalar(){
  if(instalado() || painelAberto() || est.fecharConvite || !(est.pedidoInstalar || ehIOS())) return;
  if((lerLS("logos_visitas", { n: 0 }).n || 0) < 3) return;
  const c = lerLS("logos_instalar", null);
  if(c && Date.now() <= c.ate) return;
  try{ if(sessionStorage.getItem("sola_convidou")) return; }catch(e){ return; }
  clearTimeout(est.timerInstalar);
  est.timerInstalar = setTimeout(()=>{ if(!painelAberto() && !est.gaveta && !est.fecharConvite) mostrarInstalar(false); }, 2500);
}
function mostrarInstalar(pedido){
  const x = t();
  if(est.fecharConvite) est.fecharConvite(false);
  const el = document.createElement("aside");
  el.className = "convite"; el.id = "convite";
  el.setAttribute("role", "dialog"); el.setAttribute("aria-labelledby", "conviteTit");
  const pode = !!est.pedidoInstalar, ja = instalado();
  el.innerHTML = `<button class="fechar" aria-label="${x.fechar}">✕</button>
    <p class="heroi-sobre">${x.instSobre}</p>
    <h3 id="conviteTit">${ja ? x.instJa : x.instTit}</h3>
    ${ja ? "" : `<p>${x.instTexto}</p>${pode ? "" : `<p class="convite-passos">${ehIOS() ? x.instIos : x.instOutro}</p>`}`}
    <div class="convite-acoes">${pode && !ja ? `<button class="btn-ouro" id="instSim">${ico("baixar")} ${x.instBotao}</button><button id="instDepois">${x.agoraNao}</button>`
      : `<button class="btn-ouro" id="instDepois">${x.instEntendi}</button>`}</div>`;
  document.body.appendChild(el);
  try{ sessionStorage.setItem("sola_convidou", "1"); }catch(e){}
  est.fecharConvite = (adiar)=>{
    el.remove(); est.fecharConvite = null;
    if(adiar && !pedido){
      const n = ((lerLS("logos_instalar", null) || {}).n || 0) + 1;
      gravarLS("logos_instalar", { n, ate: Date.now() + CONVITE_ESPERA[Math.min(n, CONVITE_ESPERA.length) - 1] * 864e5 });
    }
  };
  el.querySelector(".fechar").addEventListener("click", ()=>est.fecharConvite(true));
  $("instDepois").addEventListener("click", ()=>est.fecharConvite(true));
  if($("instSim")) $("instSim").addEventListener("click", async ()=>{
    const p = est.pedidoInstalar; est.pedidoInstalar = null;
    est.fecharConvite(false);
    if(p){ p.prompt(); try{ await p.userChoice; }catch(e){} }
  });
}

/* ---------- sincronização ---------- */
/* Cada tipo de dado do usuário: quais itens existem neste aparelho, como ler um item e como gravá-lo.
   No servidor cada item é uma linha (tipo, chave, valor, apagado, ts); ts = quando foi alterado, no relógio de quem alterou. */
const partir = (k)=>{ const i = k.lastIndexOf("."); return [k.slice(0, i), k.slice(i + 1)]; };
const DADOS = {
  nota:  { chaves:()=>Object.keys(est.notas), ler:(k)=>k in est.notas ? { t: est.notas[k] } : null,
           por:(k, v)=>{ if(v && typeof v.t === "string" && chaveValida(k)) est.notas[k] = v.t.slice(0, 20000); else delete est.notas[k]; },
           salvar:()=>gravarLS("logos_notas", est.notas) },
  marca: { chaves:()=>Object.keys(est.marcas), ler:(k)=>k in est.marcas ? { c: est.marcas[k] } : null,
           por:(k, v)=>{ if(v && CORES.includes(v.c) && chaveValida(k)) est.marcas[k] = v.c; else delete est.marcas[k]; },
           salvar:()=>gravarLS("logos_marcas", est.marcas) },
  plano: { chaves:()=>Object.keys(est.progresso).flatMap(id=>Object.keys(est.progresso[id] || {}).filter(d=>est.progresso[id][d]).map(d=>id + "." + d)),
           ler:(k)=>{ const [id, d] = partir(k); return est.progresso[id] && est.progresso[id][d] ? { f: true } : null; },
           por:(k, v)=>{ const [id, d] = partir(k); if(!/^[\w-]{1,30}$/.test(id) || !/^\d{1,4}$/.test(d)) return;
             est.progresso[id] = est.progresso[id] || {}; if(v && v.f) est.progresso[id][d] = true; else delete est.progresso[id][d]; },
           salvar:()=>gravarLS("logos_planos", est.progresso) },
  lido:  { chaves:()=>Object.keys(est.lidos), ler:(k)=>k in est.lidos ? { em: est.lidos[k] } : null,
           por:(k, v)=>{ if(v && +v.em > 0 && capValido(k)) est.lidos[k] = +v.em; else delete est.lidos[k]; },
           salvar:()=>gravarLS("logos_lidos", est.lidos) },
  estado:{ chaves:()=>(lerLS("logos_ultimo", null) ? ["ultimo"] : []).concat(est.metaSemana ? ["meta"] : [])
             .concat(est.perfil && Object.keys(est.perfil).length ? ["perfil"] : [])
             .concat(Object.keys(est.prateleira || {}).map(id=>"livro:" + id)),
           ler:(k)=>k === "ultimo" ? lerLS("logos_ultimo", null) : k === "meta" ? (est.metaSemana ? { n: est.metaSemana } : null)
             : k === "perfil" ? (est.perfil && Object.keys(est.perfil).length ? perfilValido(est.perfil) : null)
             : k.startsWith("livro:") ? ((est.prateleira || {})[k.slice(6)] || null) : null,
           por:(k, v)=>{ if(k === "ultimo" && v && infoLivro(v.livro) && capValido(v.livro + "." + v.cap)) gravarLS("logos_ultimo", { livro: v.livro, cap: +v.cap });
             if(k === "meta"){ est.metaSemana = v && +v.n > 0 && +v.n <= 500 ? Math.round(+v.n) : 0; gravarLS("logos_meta_semana", est.metaSemana); }
             if(k === "perfil"){ est.perfil = perfilValido(v) || {}; gravarLS("logos_perfil", est.perfil); aplicarPerfil(); }
             if(k.startsWith("livro:")){ const id = k.slice(6), ok = livroValido(id, v); est.prateleira = est.prateleira || {};
               if(ok) est.prateleira[id] = ok; else delete est.prateleira[id]; gravarLS("logos_prateleira", est.prateleira); } },
           salvar:()=>{} },
};
/* Anota que um item mudou agora. Funciona sem conta também: quando a pessoa entrar, sobe com a hora certa. */
function tocar(tipo, chave){
  est.sinc.pend[tipo + "|" + chave] = Date.now();
  gravarLS("logos_sinc", est.sinc);
  agendarSinc();
}
function agendarSinc(ms){
  if(!est.sessao) return;
  clearTimeout(est.timerSinc);
  est.timerSinc = setTimeout(sincronizar, ms ?? 2500);
}
async function sincronizar(){
  if(!est.sessao || !est.sb) return;
  if(est.sincronizando){ est.sincDeNovo = true; return; }
  est.sincronizando = true; est.sincDeNovo = false;
  clearTimeout(est.timerSinc);
  estadoSinc("indo");
  const s = est.sinc, uid = est.sessao.user.id, mudou = new Set();
  try{
    // 1. traz o que mudou na conta desde a última vez; no mesmo item, vale a alteração mais recente
    let cursor = s.cursor;
    for(let de = 0; ; de += 1000){
      let q = est.sb.from("itens").select("tipo,chave,valor,apagado,ts,atualizado_em");
      if(s.cursor) q = q.gte("atualizado_em", s.cursor);
      const { data, error } = await q.order("atualizado_em").order("tipo").order("chave").range(de, de + 999);
      if(error) throw error;
      for(const r of data){
        const d = DADOS[r.tipo], k = r.tipo + "|" + r.chave;
        if(!d) continue;
        if(!(s.pend[k] > +r.ts)){
          const antes = JSON.stringify(d.ler(r.chave));
          d.por(r.chave, r.apagado ? null : r.valor);
          if(JSON.stringify(d.ler(r.chave)) !== antes) mudou.add(r.tipo);
          delete s.pend[k];
        }
        if(!cursor || r.atualizado_em > cursor) cursor = r.atualizado_em;
      }
      if(data.length < 1000) break;
    }
    mudou.forEach(tp=>DADOS[tp].salvar());
    // 2. sobe o que mudou aqui (item que não existe mais aqui sobe como apagado)
    const envio = Object.keys(s.pend).map(k=>{
      const i = k.indexOf("|"), tipo = k.slice(0, i), chave = k.slice(i + 1);
      if(!DADOS[tipo]){ delete s.pend[k]; return null; }
      const valor = DADOS[tipo].ler(chave);
      return { user_id: uid, tipo, chave, valor, apagado: valor === null, ts: s.pend[k] };
    }).filter(Boolean);
    for(let i = 0; i < envio.length; i += 500){
      const lote = envio.slice(i, i + 500);
      const { error } = await est.sb.from("itens").upsert(lote, { onConflict:"user_id,tipo,chave" });
      if(error) throw error;
      for(const r of lote){ const k = r.tipo + "|" + r.chave; if(s.pend[k] === r.ts) delete s.pend[k]; }
    }
    s.cursor = cursor; s.conta = uid; s.ultima = Date.now();
    estadoSinc("ok");
    agendarPublicacao();
  }catch(e){ console.warn("sincronização", e); estadoSinc("erro"); }
  gravarLS("logos_sinc", s);
  est.sincronizando = false;
  if(mudou.size) atualizarTelas(mudou);
  if(est.sincDeNovo) agendarSinc(600);
}
/* Chegou coisa de outro aparelho: redesenha o que está à vista, sem atrapalhar quem está escrevendo. */
function atualizarTelas(tipos){
  if(!est.pronto) return;
  if(!$("painelEstudo").classList.contains("oculto")) montarMeuEstudo();
  if(!$("painelNotas").classList.contains("oculto")) montarNotas();
  if(/^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName) || est.gaveta) return;
  const mexeu = (...l)=>l.some(tp=>tipos.has(tp));
  if(est.vista === "perfil") return;
  if(est.vista === "inicio" ? mexeu("estado", "lido") : est.vista === "livro" ? mexeu("lido") : mexeu("nota", "marca", "lido"))
    renderizar({ manter:true });
}
/* No início: liga a conta se a pessoa já estava dentro ou se está voltando da tela de login. */
async function iniciarConta(){
  if(!temConta()) return;
  $("sobreConta").classList.remove("oculto");
  const voltando = /[?&](code|error|error_description)=/.test(location.search) || /(access_token|error_description)=/.test(location.hash);
  let guardada = false;
  try{ guardada = !!localStorage.getItem("sola-conta"); }catch(e){}
  if(!voltando && !guardada) return;
  try{
    const sb = await clienteConta();
    const { data } = await sb.auth.getSession();   // se está voltando do login, é aqui que o código vira sessão
    if(data && data.session && !est.sessao) await aoMudarSessao(data.session);
    if(voltando && est.sessao){
      const u = est.sessao.user;
      avisar(`${t().entrou} ${u.email || ""}`, null, null, 5000);
    }
  }catch(e){ console.warn("conta", e); }
}

/* ---------- painéis e tema ---------- */
function painelAberto(){ return document.querySelector(".painel:not(.oculto)"); }
function alternarPainel(id, abrir){
  const p = $(id);
  const mostrar = abrir!==undefined ? abrir : p.classList.contains("oculto");
  const antes = est.focoAntes || document.activeElement;
  document.querySelectorAll(".painel").forEach(o=>o.classList.add("oculto"));
  document.body.classList.toggle("com-painel", mostrar);
  if(mostrar){
    est.focoAntes = antes;
    p.classList.remove("oculto");
    const alvo = p.querySelector(".fechar");
    if(alvo) alvo.focus({ preventScroll:true });
  } else {
    est.focoAntes = null;
    if(antes && antes !== document.body && antes.isConnected) antes.focus({ preventScroll:true });
  }
}
function fecharPaineis(){ const p = painelAberto(); if(p) alternarPainel(p.id, false); }

/* ---------- barra de recursos: o que não cabe na linha vai para o menu "Mais" ----------
   Vale em qualquer largura e idioma (no celular cabem dois ou três itens). A ordem do HTML é a prioridade: os
   últimos saem primeiro. Onde a barra de seletores (.controles) não aparece (celular), o menu traz também os
   seletores de idioma, tradução e comparação, espelhando os da barra como os do Perfil. Recalcula quando a barra
   muda de largura, não em "resize" (no celular ele dispara ao rolar). */
const itensNav = ()=>[...document.querySelectorAll(".navbar button[data-nav]:not(#navMais)")];
const controlesOcultos = ()=>!document.querySelector(".controles").getClientRects().length;
function ajustarNav(){
  const nav = document.querySelector(".navbar"), mais = $("navMais");
  if(!nav.clientWidth) return;
  const itens = itensNav();
  itens.forEach(b=>b.classList.remove("nav-fora"));
  mais.classList.add("oculto");
  if(nav.scrollWidth > nav.clientWidth + 1){
    mais.classList.remove("oculto");
    const visiveis = itens.filter(b=>b.getClientRects().length);
    for(let i = visiveis.length - 1; i > 0 && nav.scrollWidth > nav.clientWidth + 1; i--) visiveis[i].classList.add("nav-fora");
  }
  if(!$("menuMais").classList.contains("oculto")){
    if(mais.classList.contains("oculto")) fecharMais(); else { montarMais(); posicionarMais(); }
  }
}
function montarMais(){
  const x = t(), menu = $("menuMais");
  const seletor = (id, rot)=>`<label><span>${rot}</span><select data-espelho="${id}">${$(id).innerHTML}</select></label>`;
  const html = itensNav().filter(b=>b.classList.contains("nav-fora")).map(b=>
    `<button type="button" data-alvo="${b.id}"${b.classList.contains("ativa") ? ` class="ativa"` : ""}${
      b.hasAttribute("aria-pressed") ? ` aria-pressed="${b.getAttribute("aria-pressed")}"` : ""}>${b.innerHTML}</button>`).join("") +
    (controlesOcultos() ? `<hr><div class="prefs menu-prefs" role="group" aria-label="${(NAV[est.idioma] || NAV.pt).prefs}">` +
      seletor("selIdioma", x.idioma) + seletor("selTraducao", x.traducao) + seletor("selComparar", x.comparar) + `</div>` : "");
  // refazer só quando algo mudou: assim o seletor que acabou de ser usado continua com o foco
  if(est.htmlMais !== html){
    menu.innerHTML = est.htmlMais = html;
    menu.querySelectorAll("select[data-espelho]").forEach(sel=>sel.addEventListener("change", ()=>{
      const orig = $(sel.dataset.espelho);
      orig.value = sel.value; orig.dispatchEvent(new Event("change"));
    }));
  }
  menu.querySelectorAll("select[data-espelho]").forEach(sel=>{ sel.value = $(sel.dataset.espelho).value; });
}
function posicionarMais(){
  const menu = $("menuMais"), b = $("navMais").getBoundingClientRect(), topo = document.querySelector(".topo").getBoundingClientRect();
  menu.style.top = (b.bottom - topo.top + 4) + "px";
  menu.style.right = Math.max(8, topo.right - b.right) + "px";
  menu.style.maxHeight = Math.max(160, innerHeight - b.bottom - 16) + "px";
}
function abrirMais(peloTeclado){
  montarMais();
  $("menuMais").classList.remove("oculto");
  $("navMais").setAttribute("aria-expanded", "true");
  $("navMais").classList.add("ativa");
  posicionarMais();
  if(peloTeclado){ const b = $("menuMais").querySelector("button"); if(b) b.focus(); }
}
function fecharMais(devolverFoco){
  if($("menuMais").classList.contains("oculto")) return false;
  $("menuMais").classList.add("oculto");
  $("navMais").setAttribute("aria-expanded", "false");
  $("navMais").classList.remove("ativa");
  if(devolverFoco) $("navMais").focus({ preventScroll:true });
  return true;
}
function aplicarTema(){
  const escuro = est.tema==="escuro";
  document.documentElement.dataset.tema = escuro ? "escuro" : "claro";
  $("btnTema").innerHTML = ico(escuro ? "sol" : "lua");
  $("metaTema").content = escuro ? "#171613" : "#FAF7F0";
  if(est.baseMapa) colorirMapa();
}
function avisar(texto, botao, acao, some){
  document.querySelectorAll(".aviso-topo").forEach(a=>a.remove());
  const a = document.createElement("div");
  a.className = "aviso-topo"; a.setAttribute("role", "alert");
  a.innerHTML = `<span>${esc(texto)}</span>` + (botao ? `<button>${esc(botao)}</button>` : "");
  if(botao) a.querySelector("button").addEventListener("click", acao);
  document.body.appendChild(a);
  if(some) setTimeout(()=>a.remove(), some);
}

/* ---------- inicialização ---------- */
// /?abrir=atlas (e os outros botões do topo): as páginas avulsas das confissões têm o mesmo topo do app, em HTML puro,
// e cada botão vem para cá com o painel a abrir
const ABRIR_TOPO = { meu:"btnMeuEstudo", buscar:"btnBusca", temas:"navTemas", dicionario:"navDic", atlas:"navAtlas",
  tempo:"navTempo", contexto:"navContexto", notas:"btnNotas", ajuda:"navAjuda", livros:"btnLivros", perfil:"btnPerfil" };
function lerAbrir(){
  const p = new URLSearchParams(location.search), id = ABRIR_TOPO[p.get("abrir")];
  if(!p.has("abrir")) return null;
  p.delete("abrir");
  history.replaceState(history.state, "", location.pathname + (p.toString() ? "?" + p : "") + location.hash);
  return id || null;
}
async function iniciar(){
  const abrirAoIniciar = lerAbrir();
  est.idioma = lerLS("logos_idioma","pt"); if(!UI[est.idioma]) est.idioma = "pt";
  est.tema = document.documentElement.dataset.tema || "claro";
  await carregarVersoes();
  try{ est.meta = await json("data/books.json"); }
  catch(e){ avisar(t().erroIniciar, t().recarregar, ()=>location.reload()); return; }
  est.traducao = lerLS("logos_trad","blivre");
  if(!est.meta.translations.find(tr=>tr.id===est.traducao)) est.traducao = "blivre";
  limparDados();
  contarDiaDeUso();
  const rota = lerRota();
  const antigo = /^#\//.test(location.hash) || !rotaDe(location.pathname, "");

  $("selIdioma").value = est.idioma;
  aplicarTextos(); preencherTraducoes(); aplicarTema(); aplicarEstudo(); aplicarPerfil();
  $("btnCorrida").classList.toggle("ativa", est.corrida);
  $("btnCorrida").setAttribute("aria-pressed", est.corrida);
  // voltando da tela de login: primeiro a sessão (o código está no endereço), depois a página em que a pessoa estava
  const voltaLogin = temConta() && /[?&](code|error)=/.test(location.search);
  if(voltaLogin){
    await iniciarConta();
    if(/[?&](code|error)=/.test(location.search)) history.replaceState({}, "", location.pathname);   // sobra do login no endereço
  }
  let volta = null;
  try{ volta = voltaLogin && sessionStorage.getItem("sola_volta"); sessionStorage.removeItem("sola_volta"); }catch(e){}
  const rotaVolta = volta && rotaDe(volta.split("#")[0], volta.includes("#") ? volta.slice(volta.indexOf("#")) : "");
  await navegar(rotaVolta || rota, { substituir: antigo || !!rotaVolta });
  if(!voltaLogin) iniciarConta();

  $("selIdioma").addEventListener("change", (e)=>{
    est.idioma = e.target.value; gravarLS("logos_idioma", est.idioma);
    aplicarTextos(); preencherTraducoes(); gravarLS("logos_trad", est.traducao);
    renderizar({ manter:true });
    // o atlas já montado troca os nomes do mapa e os botões das viagens
    if(est.mapa){ atualizarRotulos(); fecharLugar(); }
    if($("viagens").dataset.pronto){ delete $("viagens").dataset.pronto; montarViagens(); }
  });
  $("selTraducao").addEventListener("change", (e)=>{
    est.traducao = e.target.value; gravarLS("logos_trad", est.traducao);
    preencherTraducoes(); renderizar({ manter:true });
  });
  $("selComparar").addEventListener("change", (e)=>{ est.comparar = e.target.value; renderizar({ manter:true }); });
  $("btnLivros").addEventListener("click", ()=>{ montarListaLivros(); alternarPainel("painelLivros"); });
  $("btnComando").addEventListener("click", ()=>abrirBusca("texto"));
  $("btnMeuEstudo").addEventListener("click", ()=>abrirMeuEstudo("estudo"));
  $("btnBusca").addEventListener("click", ()=>abrirBusca("texto"));
  $("navTemas").addEventListener("click", ()=>abrirBusca("temas"));
  $("navConf").addEventListener("click", ()=>{ location.href = "/confissoes/"; });   // páginas avulsas, fora do app
  $("navDic").addEventListener("click", ()=>abrirBusca("dicionario"));
  $("navTempo").addEventListener("click", ()=>{ montarTempo(); alternarPainel("painelTempo"); });
  $("navAtlas").addEventListener("click", abrirAtlas);
  $("navContexto").addEventListener("click", abrirContexto);
  $("navAjuda").addEventListener("click", abrirAjuda);
  $("btnNotas").addEventListener("click", ()=>{ montarNotas(); alternarPainel("painelNotas"); });
  $("btnPlanos").addEventListener("click", ()=>{ montarPlanos(null); alternarPainel("painelPlanos"); });
  $("btnTema").addEventListener("click", ()=>{
    est.tema = est.tema==="escuro" ? "claro" : "escuro"; gravarLS("logos_tema", est.tema); aplicarTema();
  });
  $("btnCorrida").addEventListener("click", ()=>{
    est.corrida = !est.corrida; gravarLS("logos_corrida", est.corrida);
    $("btnCorrida").classList.toggle("ativa", est.corrida);
    $("btnCorrida").setAttribute("aria-pressed", est.corrida);
    renderizar({ manter:true });
  });
  $("btnEstudo").addEventListener("click", ()=>{
    est.estudo = !est.estudo; gravarLS("logos_estudo", est.estudo); aplicarEstudo();
    if(bancadaAtiva()) atualizarEstudo(est.versoEstudo || 1);
  });
  $("btnFecharEstudo").addEventListener("click", ()=>{
    est.estudo = false; gravarLS("logos_estudo", false); aplicarEstudo();
  });
  document.querySelectorAll("#abasEstante .eaba").forEach(b=>b.addEventListener("click", ()=>{
    est.estudoAba = b.dataset.eaba;
    atualizarEstudo(est.versoEstudo || 1, est.estudoAba === "anotacao");
  }));
  $("estudoCopiar").addEventListener("click", async ()=>{
    const v = est.versoEstudo || 1;
    const ok = await copiarTexto(`“${est.versos[v-1] || ""}” — ${refStr(est.livro, est.cap, v)} (${nomeTraducao(est.traducao)})`);
    if(ok) avisar(t().copiado, null, null, 1500);
  });
  $("estudoCompartilhar").addEventListener("click", ()=>{
    compartilharVerso(est.versoEstudo || 1).catch(e=>console.warn(e));
  });
  matchMedia("(min-width: 1060px)").addEventListener("change", (m)=>{
    if(m.matches && bancadaAtiva()) atualizarEstudo(est.versoEstudo || 1);
  });
  $("btnPerfil").addEventListener("click", ()=>abrirMeuEstudo("perfil"));
  $("navMais").addEventListener("click", (e)=>{
    if(!fecharMais()) abrirMais(e.detail === 0);   // detail 0: Enter ou espaço
  });
  $("menuMais").addEventListener("click", (e)=>{
    const b = e.target.closest("button[data-alvo]");
    if(!b) return;
    fecharMais(b === document.activeElement);   // pelo teclado, o foco volta ao "Mais" quando o painel fechar
    $(b.dataset.alvo).click();
  });
  // fecha ao tocar fora; "pointerdown" porque o Safari do iPhone não manda "click" de toque em área sem ação
  document.addEventListener("pointerdown", (e)=>{ if(!e.target.closest("#menuMais,#navMais")) fecharMais(); });
  if(window.ResizeObserver) new ResizeObserver(()=>ajustarNav()).observe(document.querySelector(".navbar"));
  if(document.fonts){ document.fonts.ready.then(ajustarNav); document.fonts.addEventListener("loadingdone", ajustarNav); }
  atualizarBotaoPerfil();
  $("btnOffline").addEventListener("click", baixarOffline);
  document.querySelectorAll("[data-painel]").forEach(a=>a.addEventListener("click", (e)=>{
    e.preventDefault();
    const id = a.dataset.painel;
    if(id==="painelAtlas") return abrirAtlas();
    if(id==="painelPlanos") montarPlanos(null);
    if(id==="painelTempo") montarTempo();
    if(id==="painelNotas") montarNotas();
    if(id==="painelAjuda") montarAjuda();
    if(id==="painelEstudo"){ est.abaEstudo = "estudo"; montarMeuEstudo(); }
    alternarPainel(id, true);
  }));
  $("btnAtlasBuscar").addEventListener("click", buscarAtlas);
  $("campoAtlas").addEventListener("keydown", (e)=>{ if(e.key==="Enter") buscarAtlas(); });
  $("btnBuscar").addEventListener("click", buscar);
  $("campoBusca").addEventListener("keydown", (e)=>{ if(e.key==="Enter"){ clearTimeout(est.esperaBusca); buscar(); } });
  // resultados enquanto digita (menos na aba Strong, que carrega o léxico inteiro)
  $("campoBusca").addEventListener("input", ()=>{
    clearTimeout(est.esperaBusca);
    if(est.buscaModo !== "strong") est.esperaBusca = setTimeout(()=>buscar(true), 320);
  });
  ligarPrevias();
  ligarEstante();
  const dicaBusca = document.createElement("div");
  dicaBusca.className = "dica-ref-linha"; dicaBusca.setAttribute("aria-live", "polite");
  $("buscaStatus").before(dicaBusca);
  est.dicaBusca = ligarDicaRef($("campoBusca"), dicaBusca, ()=>est.buscaModo === "texto");
  document.querySelectorAll(".fechar").forEach(b=>b.addEventListener("click", ()=>alternarPainel(b.dataset.fecha, false)));
  document.querySelectorAll(".painel").forEach(p=>p.addEventListener("click", (e)=>{ if(e.target===p) alternarPainel(p.id, false); }));

  // links internos (/, /biblia/joao/, /biblia/joao/3/#v16) navegam dentro do app, sem recarregar a página
  document.addEventListener("click", (e)=>{
    if(e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest("a[href]");
    if(!a || a.target || a.origin !== location.origin || a.getAttribute("href").startsWith("#")) return;
    const r = rotaDe(a.pathname, a.hash);
    if(!r) return;
    e.preventDefault();
    fecharPaineis();
    navegar(r);
  }, true);   // na fase de captura: o mapa (Leaflet) não deixa o clique dos balões chegar ao documento
  // botão voltar/avançar do navegador e links antigos com "#/JHN/3"
  const seguirRota = ()=>{
    const r = lerRota(), antigoHash = /^#\//.test(location.hash);
    const mesma = r.vista===est.vista && (r.vista==="inicio" || r.livro===est.livro || (r.vista==="perfil" && r.apelido===est.apelidoPub))
      && (r.vista!=="cap" || r.cap===est.cap);
    if(mesma && !antigoHash){
      if(r.plano !== undefined) return abrirPlano(r.plano, r.dia);
      const alvo = r.v && document.querySelector(`.verso[data-v="${r.v}"]`);
      if(alvo){ est.alvoV = r.v; irAoVerso(alvo); }
      return;
    }
    fecharPaineis();
    navegar(r, { substituir: antigoHash });
  };
  window.addEventListener("popstate", seguirRota);
  window.addEventListener("hashchange", ()=>{ if(/^#\//.test(location.hash)) seguirRota(); });

  document.addEventListener("click", (e)=>{ if(!e.target.closest("#cartaoPalavra,.chave")) fecharPalavra(); });
  document.addEventListener("keydown", (e)=>{
    if((e.ctrlKey || e.metaKey) && !e.altKey && e.key.toLowerCase() === "k"){
      e.preventDefault();
      return abrirBusca("texto");
    }
    if(e.key === "Escape"){
      if(fecharMais(true)) return;
      if(painelAberto()) return fecharPaineis();
      if(fecharPalavra(true)) return;
      if(est.fecharConvite) return est.fecharConvite(true);
      if(est.gaveta && est.versoAtivo){ const el = est.versoAtivo; fecharGavetas(el); el.focus({ preventScroll:true }); }
      return;
    }
    if(e.metaKey || e.ctrlKey || e.altKey || painelAberto() || /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
    if(e.key === "/"){ e.preventDefault(); return abrirBusca("texto"); }
    if(est.vista !== "cap") return;
    const { ant, pro } = vizinhos();
    if(e.key === "ArrowLeft" && ant) irPara(ant.l, ant.c);
    if(e.key === "ArrowRight" && pro){ leuAoAvancar(); irPara(pro.l, pro.c); }
  });

  // outro aparelho pode ter mudado algo: confere ao voltar para a aba e ao recuperar a conexão
  document.addEventListener("visibilitychange", ()=>{ if(!document.hidden && Date.now() - est.sinc.ultima > 30000) agendarSinc(300); });
  window.addEventListener("online", ()=>agendarSinc(300));

  if("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost"))
    navigator.serviceWorker.register("/sw.js").catch(()=>{});
  if(abrirAoIniciar) $(abrirAoIniciar).click();
}
iniciar();
