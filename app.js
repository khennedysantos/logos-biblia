/* Sola — Estudo Bíblico. SPA em JS puro, sem dependências. */
"use strict";

/* ---------- textos da interface ---------- */
const UI = {
  pt: { idioma:"Idioma", traducao:"Tradução", comparar:"Comparar com…", semComparar:"Sem comparação",
    livros:"Livros", buscar:"Buscar", notas:"Minhas anotações", marcar:"Marcar",
    cores:{ouro:"ouro", verde:"verde", azul:"azul", rosa:"rosa"},
    original:"Original", comentario:"Comentário", anotacao:"Anotação", copiar:"Copiar", copiado:"Copiado!",
    grego:"Grego — Textus Receptus", hebraico:"Hebraico — Códice de Leningrado",
    lexDef:"Definição (Strong)", lexKjv:"Como a KJV traduz", lexFonte:"Léxico de Strong (1890), definições em tradução automática · Texto marcado: STEPBible/Tyndale House (CC BY)",
    referencias:"Referências", semRefs:"Sem referências para este versículo.", refFonte:"Referências: openbible.info (CC-BY)",
    leituraCorrida:"Leitura contínua",
    abaTexto:"Texto", abaTemas:"Temas", abaDic:"Dicionário",
    exTema:"ex.: fé, aliança, justificação", exDic:"ex.: Abraão, altar, aliança",
    conteudoEN:"Conteúdo no original em inglês — tradução em andamento.",
    tradAuto:"Tradução automática do original em inglês.", lerMais:"Ler mais", lerMenos:"Recolher", compartilhar:"Compartilhar", gerandoImagem:"Gerando…",
    comRef:"Comentário referente ao v.", comBloco:"(o comentário cobre um bloco de versículos)",
    comInicio:"Neste capítulo, o comentário começa no v.",
    semLivroCalvin:"Ainda não há comentário para este livro.",
    autorCalvin:"João Calvino (1509–1564), domínio público", autorHenry:"Matthew Henry (1662–1714), domínio público",
    notaHenry:"Calvino não comentou este livro; aqui, o comentário é de Matthew Henry, pastor puritano.",
    fonteNave:"Nave's Topical Bible (1897), domínio público", fonteEaston:"Dicionário Bíblico de Easton (1897), domínio público",
    semOriginal:"Texto original indisponível para este versículo.",
    semComentario:"Ainda não há comentário para este versículo.",
    avisoIdiomaComentario:"Comentário exibido no original em inglês — tradução em andamento.",
    fonte:"Fonte", salvar:"Salvar", cancelar:"Cancelar", excluir:"Excluir", fechar:"Fechar",
    escrevaNota:"Escreva sua reflexão sobre este versículo…",
    semNotas:"Você ainda não tem anotações. Toque em um versículo e escolha “Anotação”.",
    bibliaToda:"Buscar na Bíblia toda", carregando:"Carregando…",
    buscando:"Buscando…", resultados:"resultado(s)", nadaEncontrado:"Nada encontrado.", mostrando:"mostrando os primeiros",
    digiteBusca:"Digite ao menos 3 letras, ou uma referência como “João 3:16”.", at:"Antigo Testamento", nt:"Novo Testamento",
    exPlaceholder:"ex.: graça e verdade, ou João 3:16",
    contexto:"Contexto", voltar:"Voltar", dia:"Dia", dias:"dias", capitulos:"capítulos", todosCaps:"Todos os capítulos",
    autor:"Autor", data:"Data", local:"Local", publico:"Público", tema:"Tema", paralelos:"Paralelos",
    escala:["Criação","Êxodo","Davi","Exílio","Cristo","Igreja"],
    erroCarregar:"Não foi possível carregar este texto. Verifique a conexão.", tentar:"Tentar de novo",
    erroIniciar:"Não foi possível carregar o Sola. Verifique a conexão.", recarregar:"Recarregar",
    heroiSobre:"Sola Scriptura", heroiTitulo:"A Escritura, <em>em profundidade</em>",
    heroiTexto:"A Bíblia completa com o grego e o hebraico palavra por palavra, léxico de Strong, comentários de Calvino e Matthew Henry, referências cruzadas e atlas. Gratuito, sem anúncios, em português.",
    heroiCampo:"João 3:16, Sl 23 ou uma palavra", continuar:"Continuar em", comecar:"Começar por João",
    versoDia:"Versículo do dia",
    grupos:{pentateuco:"Pentateuco", historicos:"Históricos", poeticos:"Poéticos e sapienciais", maiores:"Profetas maiores",
      menores:"Profetas menores", evangelhos:"Evangelhos e Atos", paulo:"Cartas de Paulo", gerais:"Cartas gerais e Apocalipse"},
    recursos:[["Original e Strong","Cada palavra do grego e do hebraico com transliteração, tradução literal e o verbete do léxico."],
      ["Comentários clássicos","João Calvino em 47 livros e Matthew Henry em outros 18, versículo por versículo."],
      ["Referências cruzadas","A Escritura interpreta a Escritura: as passagens paralelas de cada versículo."],
      ["Temas e dicionário","Mais de 5.000 temas de Nave e 3.900 verbetes do dicionário de Easton."],
      ["Atlas bíblico","1.300 lugares no mapa, com as viagens missionárias de Paulo."],
      ["Planos de leitura","A Bíblia em um ano, o Novo Testamento em 90 dias, Salmos e Provérbios."]],
    sobreLivro:"Sobre o livro", comentarioDe:"Comentário",
    backup:"Backup", restaurar:"Restaurar", restaurado:"Restaurado deste arquivo:", arquivoInvalido:"Este arquivo não é um backup do Sola.",
    nAnot:"anotação(ões)", nMarc:"marcação(ões)",
    offBaixando:"Baixando…", offPronto:"Pronto: esta tradução inteira está guardada neste aparelho.",
    offErro:"Não deu para baixar tudo. Verifique a conexão e tente de novo.", offSem:"Este navegador não permite guardar o site para uso sem internet.",
    meuEstudo:"Meu estudo", lidoMarcar:"Marcar capítulo como lido", lido:"Capítulo lido", capsLidos:"capítulos lidos", capLido1:"capítulo lido", de:"de",
    diasSeguidos:"dia(s) seguidos", nNotasRot:"anotações", nMarcasRot:"versículos marcados", progLivros:"Progresso por livro",
    marcacoes:"Versículos marcados", semMarcas:"Nenhum versículo marcado ainda. Toque em um versículo e escolha uma cor.", verTodas:"Ver todas",
    planosTit:"Planos de leitura", semLeitura:"Marque os capítulos como lidos ao terminar e acompanhe aqui o seu progresso.",
    contaLocal:"Seu estudo fica guardado só neste aparelho. Para levar a outro, use Backup e Restaurar em “Minhas anotações”.",
    contaTitulo:"Continue em qualquer aparelho", contaTexto:"Entre para guardar anotações, marcações, capítulos lidos e planos na sua conta. É gratuito e opcional.",
    entrarGoogle:"Entrar com Google", entrarEmail:"Receber link por e-mail", linkEnviado:"Enviamos um link de acesso para", seuEmail:"seu e-mail",
    sair:"Sair", sincAgora:"Sincronizar agora", sincIndo:"Sincronizando…", sincOk:"Tudo guardado na sua conta",
    sincErro:"Sem conexão com a conta: o que você fizer fica neste aparelho e sobe depois", entrou:"Você entrou como", erroConta:"Não foi possível conectar à conta agora. Tente de novo.",
    contaOutra:"Este aparelho tem o estudo de outra conta. Trocar pelo estudo da conta em que você entrou agora? O que ainda não tinha sido sincronizado da outra conta será perdido.",
    excluirConta:"Excluir minha conta", excluirConfirma:"Excluir a sua conta e tudo o que está guardado nela no servidor? Isso não pode ser desfeito. O que está neste aparelho continua aqui.",
    contaExcluida:"Conta excluída. O que estava neste aparelho continua aqui." },
  en: { idioma:"Language", traducao:"Translation", comparar:"Compare with…", semComparar:"No comparison",
    livros:"Books", buscar:"Search", notas:"My notes", marcar:"Highlight",
    cores:{ouro:"gold", verde:"green", azul:"blue", rosa:"pink"},
    original:"Original", comentario:"Commentary", anotacao:"Note", copiar:"Copy", copiado:"Copied!",
    grego:"Greek — Textus Receptus", hebraico:"Hebrew — Leningrad Codex",
    lexDef:"Definition (Strong)", lexKjv:"KJV renderings", lexFonte:"Strong's Lexicon (1890) · Tagged text: STEPBible/Tyndale House (CC BY)",
    referencias:"Cross-refs", semRefs:"No cross-references for this verse.", refFonte:"Cross-references: openbible.info (CC-BY)",
    leituraCorrida:"Continuous reading",
    abaTexto:"Text", abaTemas:"Topics", abaDic:"Dictionary",
    exTema:"e.g. faith, covenant", exDic:"e.g. Abraham, altar",
    conteudoEN:"Content in the original English.",
    tradAuto:"", lerMais:"Read more", lerMenos:"Show less", compartilhar:"Share", gerandoImagem:"Creating…",
    comRef:"Commentary on v.", comBloco:"(the commentary covers a block of verses)",
    comInicio:"In this chapter, the commentary begins at v.",
    semLivroCalvin:"No commentary available for this book yet.",
    autorCalvin:"John Calvin (1509–1564), public domain", autorHenry:"Matthew Henry (1662–1714), public domain",
    notaHenry:"Calvin did not comment on this book; this commentary is by Matthew Henry, Puritan pastor.",
    fonteNave:"Nave's Topical Bible (1897), public domain", fonteEaston:"Easton's Bible Dictionary (1897), public domain",
    semOriginal:"Original text unavailable for this verse.",
    semComentario:"No commentary available for this verse yet.",
    avisoIdiomaComentario:"Commentary shown in the original English.",
    fonte:"Source", salvar:"Save", cancelar:"Cancel", excluir:"Delete", fechar:"Close",
    escrevaNota:"Write your reflection on this verse…",
    semNotas:"No notes yet. Tap a verse and choose “Note”.",
    bibliaToda:"Search the whole Bible", carregando:"Loading…",
    buscando:"Searching…", resultados:"result(s)", nadaEncontrado:"Nothing found.", mostrando:"showing the first",
    digiteBusca:"Type at least 3 letters, or a reference such as “John 3:16”.", at:"Old Testament", nt:"New Testament",
    exPlaceholder:"e.g. grace and truth, or John 3:16",
    contexto:"Context", voltar:"Back", dia:"Day", dias:"days", capitulos:"chapters", todosCaps:"All chapters",
    autor:"Author", data:"Date", local:"Place", publico:"Audience", tema:"Theme", paralelos:"Parallels",
    escala:["Creation","Exodus","David","Exile","Christ","Church"],
    erroCarregar:"Could not load this text. Check your connection.", tentar:"Try again",
    erroIniciar:"Could not load Sola. Check your connection.", recarregar:"Reload",
    heroiSobre:"Sola Scriptura", heroiTitulo:"Scripture, <em>in depth</em>",
    heroiTexto:"The whole Bible with Greek and Hebrew word by word, Strong's lexicon, commentaries by Calvin and Matthew Henry, cross-references and an atlas. Free, with no ads.",
    heroiCampo:"John 3:16, Ps 23 or a word", continuar:"Continue in", comecar:"Start with John",
    versoDia:"Verse of the day",
    grupos:{pentateuco:"Pentateuch", historicos:"History", poeticos:"Poetry and wisdom", maiores:"Major prophets",
      menores:"Minor prophets", evangelhos:"Gospels and Acts", paulo:"Paul's letters", gerais:"General letters and Revelation"},
    recursos:[["Original and Strong","Every Greek and Hebrew word with transliteration, literal gloss and its lexicon entry."],
      ["Classic commentaries","John Calvin on 47 books and Matthew Henry on another 18, verse by verse."],
      ["Cross-references","Scripture interprets Scripture: parallel passages for every verse."],
      ["Topics and dictionary","Over 5,000 topics from Nave and 3,900 entries from Easton's dictionary."],
      ["Bible atlas","1,300 places on the map, with Paul's missionary journeys."],
      ["Reading plans","The Bible in a year, the New Testament in 90 days, Psalms and Proverbs."]],
    sobreLivro:"About the book", comentarioDe:"Commentary",
    backup:"Backup", restaurar:"Restore", restaurado:"Restored from this file:", arquivoInvalido:"This file is not a Sola backup.",
    nAnot:"note(s)", nMarc:"highlight(s)",
    offBaixando:"Downloading…", offPronto:"Done: this whole translation is stored on this device.",
    offErro:"Could not download everything. Check your connection and try again.", offSem:"This browser cannot store the site for offline use.",
    meuEstudo:"My study", lidoMarcar:"Mark chapter as read", lido:"Chapter read", capsLidos:"chapters read", capLido1:"chapter read", de:"of",
    diasSeguidos:"day(s) in a row", nNotasRot:"notes", nMarcasRot:"highlighted verses", progLivros:"Progress by book",
    marcacoes:"Highlighted verses", semMarcas:"No highlighted verses yet. Tap a verse and pick a colour.", verTodas:"See all",
    planosTit:"Reading plans", semLeitura:"Mark chapters as read when you finish them and follow your progress here.",
    contaLocal:"Your study is stored on this device only. To move it, use Backup and Restore under “My notes”.",
    contaTitulo:"Pick up on any device", contaTexto:"Sign in to keep your notes, highlights, chapters read and plans in your account. Free and optional.",
    entrarGoogle:"Sign in with Google", entrarEmail:"Email me a link", linkEnviado:"We sent a sign-in link to", seuEmail:"your email",
    sair:"Sign out", sincAgora:"Sync now", sincIndo:"Syncing…", sincOk:"Everything is saved to your account",
    sincErro:"Cannot reach your account: changes stay on this device and upload later", entrou:"Signed in as", erroConta:"Could not reach the account right now. Try again.",
    contaOutra:"This device holds another account's study. Replace it with the study from the account you just signed in to? Anything not yet synced from the other account will be lost.",
    excluirConta:"Delete my account", excluirConfirma:"Delete your account and everything stored in it on the server? This cannot be undone. What is on this device stays here.",
    contaExcluida:"Account deleted. What was on this device is still here." },
  es: { idioma:"Idioma", traducao:"Traducción", comparar:"Comparar con…", semComparar:"Sin comparación",
    livros:"Libros", buscar:"Buscar", notas:"Mis notas", marcar:"Resaltar",
    cores:{ouro:"oro", verde:"verde", azul:"azul", rosa:"rosa"},
    original:"Original", comentario:"Comentario", anotacao:"Nota", copiar:"Copiar", copiado:"¡Copiado!",
    grego:"Griego — Textus Receptus", hebraico:"Hebreo — Códice de Leningrado",
    lexDef:"Definición (Strong)", lexKjv:"Traducciones en la KJV", lexFonte:"Léxico de Strong (1890) · Texto marcado: STEPBible/Tyndale House (CC BY)",
    referencias:"Referencias", semRefs:"Sin referencias para este versículo.", refFonte:"Referencias: openbible.info (CC-BY)",
    leituraCorrida:"Lectura continua",
    abaTexto:"Texto", abaTemas:"Temas", abaDic:"Diccionario",
    exTema:"ej.: fe, pacto", exDic:"ej.: Abraham, altar",
    conteudoEN:"Contenido en el inglés original.",
    tradAuto:"", lerMais:"Leer más", lerMenos:"Ocultar", compartilhar:"Compartir", gerandoImagem:"Generando…",
    comRef:"Comentario sobre el v.", comBloco:"(el comentario abarca un bloque de versículos)",
    comInicio:"En este capítulo, el comentario comienza en el v.",
    semLivroCalvin:"Aún no hay comentario para este libro.",
    autorCalvin:"Juan Calvino (1509–1564), dominio público", autorHenry:"Matthew Henry (1662–1714), dominio público",
    notaHenry:"Calvino no comentó este libro; aquí el comentario es de Matthew Henry, pastor puritano.",
    fonteNave:"Nave's Topical Bible (1897), dominio público", fonteEaston:"Diccionario Bíblico de Easton (1897), dominio público",
    semOriginal:"Texto original no disponible para este versículo.",
    semComentario:"Aún no hay comentario para este versículo.",
    avisoIdiomaComentario:"Comentario mostrado en el inglés original.",
    fonte:"Fuente", salvar:"Guardar", cancelar:"Cancelar", excluir:"Eliminar", fechar:"Cerrar",
    escrevaNota:"Escribe tu reflexión sobre este versículo…",
    semNotas:"Aún no tienes notas. Toca un versículo y elige “Nota”.",
    bibliaToda:"Buscar en toda la Biblia", carregando:"Cargando…",
    buscando:"Buscando…", resultados:"resultado(s)", nadaEncontrado:"No se encontró nada.", mostrando:"mostrando los primeros",
    digiteBusca:"Escribe al menos 3 letras, o una referencia como “Juan 3:16”.", at:"Antiguo Testamento", nt:"Nuevo Testamento",
    exPlaceholder:"ej.: gracia y verdad, o Juan 3:16",
    contexto:"Contexto", voltar:"Volver", dia:"Día", dias:"días", capitulos:"capítulos", todosCaps:"Todos los capítulos",
    autor:"Autor", data:"Fecha", local:"Lugar", publico:"Destinatarios", tema:"Tema", paralelos:"Paralelos",
    escala:["Creación","Éxodo","David","Exilio","Cristo","Iglesia"],
    erroCarregar:"No se pudo cargar este texto. Revisa la conexión.", tentar:"Reintentar",
    erroIniciar:"No se pudo cargar Sola. Revisa la conexión.", recarregar:"Recargar",
    heroiSobre:"Sola Scriptura", heroiTitulo:"La Escritura, <em>en profundidad</em>",
    heroiTexto:"La Biblia completa con el griego y el hebreo palabra por palabra, léxico de Strong, comentarios de Calvino y Matthew Henry, referencias cruzadas y atlas. Gratis y sin anuncios.",
    heroiCampo:"Juan 3:16, Sal 23 o una palabra", continuar:"Continuar en", comecar:"Empezar por Juan",
    versoDia:"Versículo del día",
    grupos:{pentateuco:"Pentateuco", historicos:"Históricos", poeticos:"Poéticos y sapienciales", maiores:"Profetas mayores",
      menores:"Profetas menores", evangelhos:"Evangelios y Hechos", paulo:"Cartas de Pablo", gerais:"Cartas generales y Apocalipsis"},
    recursos:[["Original y Strong","Cada palabra del griego y del hebreo con transliteración, traducción literal y su entrada del léxico."],
      ["Comentarios clásicos","Juan Calvino en 47 libros y Matthew Henry en otros 18, versículo por versículo."],
      ["Referencias cruzadas","La Escritura interpreta la Escritura: pasajes paralelos de cada versículo."],
      ["Temas y diccionario","Más de 5.000 temas de Nave y 3.900 entradas del diccionario de Easton."],
      ["Atlas bíblico","1.300 lugares en el mapa, con los viajes misioneros de Pablo."],
      ["Planes de lectura","La Biblia en un año, el Nuevo Testamento en 90 días, Salmos y Proverbios."]],
    sobreLivro:"Sobre el libro", comentarioDe:"Comentario",
    backup:"Copia", restaurar:"Restaurar", restaurado:"Restaurado de este archivo:", arquivoInvalido:"Este archivo no es una copia de Sola.",
    nAnot:"nota(s)", nMarc:"resaltado(s)",
    offBaixando:"Descargando…", offPronto:"Listo: esta traducción completa está guardada en este dispositivo.",
    offErro:"No se pudo descargar todo. Revisa la conexión e inténtalo de nuevo.", offSem:"Este navegador no permite guardar el sitio para usarlo sin conexión.",
    meuEstudo:"Mi estudio", lidoMarcar:"Marcar capítulo como leído", lido:"Capítulo leído", capsLidos:"capítulos leídos", capLido1:"capítulo leído", de:"de",
    diasSeguidos:"día(s) seguidos", nNotasRot:"notas", nMarcasRot:"versículos resaltados", progLivros:"Progreso por libro",
    marcacoes:"Versículos resaltados", semMarcas:"Aún no hay versículos resaltados. Toca un versículo y elige un color.", verTodas:"Ver todas",
    planosTit:"Planes de lectura", semLeitura:"Marca los capítulos como leídos al terminar y sigue aquí tu progreso.",
    contaLocal:"Tu estudio se guarda solo en este dispositivo. Para llevarlo a otro, usa Copia y Restaurar en “Mis notas”.",
    contaTitulo:"Continúa en cualquier dispositivo", contaTexto:"Entra para guardar notas, resaltados, capítulos leídos y planes en tu cuenta. Gratis y opcional.",
    entrarGoogle:"Entrar con Google", entrarEmail:"Recibir enlace por correo", linkEnviado:"Enviamos un enlace de acceso a", seuEmail:"tu correo",
    sair:"Salir", sincAgora:"Sincronizar ahora", sincIndo:"Sincronizando…", sincOk:"Todo guardado en tu cuenta",
    sincErro:"Sin conexión con la cuenta: los cambios quedan en este dispositivo y se suben después", entrou:"Entraste como", erroConta:"No se pudo conectar con la cuenta ahora. Inténtalo de nuevo.",
    contaOutra:"Este dispositivo tiene el estudio de otra cuenta. ¿Cambiarlo por el de la cuenta con la que acabas de entrar? Lo que no se había sincronizado de la otra cuenta se perderá.",
    excluirConta:"Eliminar mi cuenta", excluirConfirma:"¿Eliminar tu cuenta y todo lo guardado en ella en el servidor? No se puede deshacer. Lo que está en este dispositivo sigue aquí.",
    contaExcluida:"Cuenta eliminada. Lo que estaba en este dispositivo sigue aquí." },
};
const NAV = {
  pt:{meu:"Meu estudo",buscar:"Buscar",temas:"Temas",dicionario:"Dicionário",planos:"Planos",tempo:"Linha do tempo",atlas:"Atlas",contexto:"Contexto",notas:"Anotações",estudo:"Modo estudo"},
  en:{meu:"My study",buscar:"Search",temas:"Topics",dicionario:"Dictionary",planos:"Plans",tempo:"Timeline",atlas:"Atlas",contexto:"Context",notas:"Notes",estudo:"Study mode"},
  es:{meu:"Mi estudio",buscar:"Buscar",temas:"Temas",dicionario:"Diccionario",planos:"Planes",tempo:"Cronología",atlas:"Atlas",contexto:"Contexto",notas:"Notas",estudo:"Modo estudio"}
};
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
  corrida: lerLS("logos_corrida", false), estudo: lerLS("logos_estudo", false), progresso: lerLS("logos_planos", {}),
  lidos: lerLS("logos_lidos", {}),                                       // capítulos lidos: {"JHN.3": quando}
  sinc: Object.assign({ pend:{}, cursor:null, conta:null, ultima:0 }, lerLS("logos_sinc", null)),   // o que falta subir para a conta
  sb:null, sessao:null, sincEstado:"",
  cacheBiblia:{}, cacheComent:{}, cacheInter:{}, cacheLex:{}, cacheRefs:{}, cacheTemas:{}, cacheDic:{}, titulosPT:{},
  livrosCom:null, idxTemas:null, idxDic:null, aliasPT:null, planos:null, tempo:null, ctx:null,
  lugares:null, mapa:null, marcadores:[], viagens:null, camadaViagem:[],
  versos:[], versoAtivo:null, gaveta:null, buscaModo:"texto", vez:0, vezBusca:0, focoAntes:null,
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
async function json(url){ const r = await fetch(url.startsWith("data/") ? "/" + url : url); if(!r.ok) throw new Error(url); return r.json(); }
/* Guarda no cache o que deu certo; o que falhou (sem rede) pode ser pedido de novo. */
async function comCache(cache, chave, url){
  if(!(chave in cache)){
    try{ cache[chave] = await json(url); }
    catch(e){ return null; }
  }
  return cache[chave];
}
const carregarLivro = (trad, usfm)=>comCache(est.cacheBiblia, trad+"/"+usfm, `data/bibles/${trad}/${usfm}.json`);
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
/* Lê um endereço e devolve a rota: {vista:"inicio"} | {vista:"livro",livro} | {vista:"cap",livro,cap,v} | null (não é do app). */
function rotaDe(caminho, hash){
  const h = (hash||"").match(/^#\/([A-Z0-9]{3})\/(\d+)(?:\/(\d+))?/);   // links antigos: #/JHN/3
  if(h && infoLivro(h[1])) return { vista:"cap", livro:h[1], cap:Math.min(Math.max(+h[2],1), infoLivro(h[1]).ch), v:+h[3]||0 };
  const v = +((hash||"").match(/^#v(\d+)$/)||[])[1] || 0;
  let m = caminho.match(/^\/biblia\/([a-z0-9-]+)\/(\d+)\/?$/);
  if(m){ const b = livroPorSlug(m[1]); if(b && +m[2] >= 1 && +m[2] <= b.ch) return { vista:"cap", livro:b.id, cap:+m[2], v }; }
  m = caminho.match(/^\/biblia\/([a-z0-9-]+)\/?$/);
  if(m){ const b = livroPorSlug(m[1]); if(b) return { vista:"livro", livro:b.id }; }
  return caminho === "/" || caminho === "/index.html" ? { vista:"inicio" } : null;
}
function lerRota(){ return rotaDe(location.pathname, location.hash) || { vista:"inicio" }; }   // endereço desconhecido (404): início
function urlAtual(){
  return est.vista==="inicio" ? "/" : est.vista==="livro" ? urlLivro(est.livro) : urlCapitulo(est.livro, est.cap, est.alvoV);
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
  if(r.vista==="cap"){ est.cap = r.cap; est.alvoV = r.v || 0; est.abrir = r.abrir || null; }
  else { est.alvoV = 0; est.abrir = null; }
  return renderizar(Object.assign({ nav:true }, op));
}
function irPara(usfm, cap, v, abrir){ return navegar({ vista:"cap", livro:usfm, cap, v, abrir }); }

/* ---------- interface base ---------- */
function aplicarTextos(){
  const x = t();
  document.documentElement.lang = est.idioma==="pt" ? "pt-BR" : est.idioma;
  document.querySelectorAll(".navbar [data-nav] [data-label]").forEach(sp=>{
    const chave = sp.parentNode.dataset.nav;
    if(NAV[est.idioma][chave]) sp.textContent = NAV[est.idioma][chave];
  });
  $("lblIdioma").textContent = x.idioma;
  $("lblTraducao").textContent = x.traducao;
  $("lblComparar").textContent = x.comparar;
  $("tituloLivros").textContent = x.livros;
  $("tituloBusca").textContent = x.buscar;
  $("tituloNotas").textContent = x.notas;
  $("lblBibliaToda").textContent = x.bibliaToda;
  $("btnCorrida").title = x.leituraCorrida;
  document.querySelectorAll(".fechar").forEach(b=>b.setAttribute("aria-label", x.fechar));
  prepararAbas();
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
  est.versoAtivo = null; est.gaveta = null;
  if(est.vista==="inicio"){
    renderizarInicio();
    $("lblLivroAtual").textContent = x.livros;
    document.title = "Sola — Estudo Bíblico";
  } else if(est.vista==="livro"){
    await renderizarLivro();
    $("lblLivroAtual").textContent = nomeLivro(est.livro);
    document.title = `${nomeLivro(est.livro)} — Sola`;
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
    }
  }
  atualizarURL(op.substituir);
  if(est.vista!=="cap" && !op.manter && est.pronto) window.scrollTo({ top:0, behavior:"instant" });
  est.pronto = true;
}

/* ---------- página inicial ---------- */
function renderizarInicio(){
  const x = t(), ult = lerLS("logos_ultimo", null);
  const temUlt = ult && infoLivro(ult.livro) && ult.cap >= 1 && ult.cap <= infoLivro(ult.livro).ch;
  const icones = ["original","comentario","refs","temas","atlas","planos"];
  const resumo = resumoEstudo(), nLidos = resumo.lidos;
  const testamento = (tst)=>`<section class="testamento"><h2>${tst==="AT" ? x.at : x.nt}</h2>${ornamento}
    <div class="grupos">` + GRUPOS.filter(g=>g[0]===tst).map(g=>
      `<div class="grupo-livros"><h3>${x.grupos[g[1]]}</h3>` + g[2].map(id=>
        `<a href="${urlLivro(id)}">${esc(nomeLivro(id))}<span>${infoLivro(id).ch}</span></a>`).join("") + `</div>`).join("") +
    `</div></section>`;
  $("leitor").innerHTML = `<div class="inicio">
    <section class="heroi">
      <p class="heroi-sobre">${x.heroiSobre}</p>
      <h1>${x.heroiTitulo}</h1>${ornamento}
      <p class="heroi-texto">${x.heroiTexto}</p>
      <form class="heroi-busca" id="formInicio" role="search">
        <input id="campoInicio" type="search" placeholder="${x.heroiCampo}" aria-label="${x.buscar}" autocomplete="off">
        <button type="submit">${x.buscar}</button>
      </form>
      <div class="heroi-acoes">
        ${temUlt ? `<a class="btn-ouro" href="${urlCapitulo(ult.livro, ult.cap)}">${x.continuar} ${esc(nomeLivro(ult.livro))} ${ult.cap} ${ico("seta")}</a>` : ""}
        <a class="${temUlt ? "btn-linha" : "btn-ouro"}" href="${urlCapitulo("JHN", 1)}">${x.comecar}</a>
      </div>
      ${nLidos ? `<p class="heroi-estudo"><button id="btnEstudoInicio">${ico("pessoa")} ${x.meuEstudo}: ${nLidos} ${nLidos === 1 ? x.capLido1 : x.capsLidos}${resumo.seq > 1 ? ` · ${resumo.seq} ${x.diasSeguidos}` : ""}</button></p>` : ""}
    </section>
    <section class="dia"><p class="rotulo-secao">${x.versoDia}</p><blockquote id="versoDia"></blockquote><span id="versoDiaRef"></span></section>
    <section class="recursos">` + x.recursos.map((r,i)=>
      `<button class="recurso" data-recurso="${i}">${ico(icones[i])}<h3>${r[0]}</h3><p>${r[1]}</p></button>`).join("") +
    `</section>` + testamento("AT") + testamento("NT") + `</div>`;
  $("formInicio").addEventListener("submit", (e)=>{
    e.preventDefault();
    const termo = $("campoInicio").value.trim();
    if(!termo) return;
    const r = parseRef(termo);
    if(r) return irPara(r.livro, r.cap, r.v);
    abrirBusca("texto"); $("chkBibliaToda").checked = true; $("campoBusca").value = termo; buscar();
  });
  if($("btnEstudoInicio")) $("btnEstudoInicio").addEventListener("click", abrirMeuEstudo);
  const acoes = [()=>irPara("JHN",1,1,"original"), ()=>irPara("ROM",8,28,"comentario"), ()=>irPara("JHN",3,16,"referencias"),
    ()=>abrirBusca("temas"), abrirAtlas, ()=>{ montarPlanos(null); alternarPainel("painelPlanos", true); }];
  document.querySelectorAll(".recurso").forEach(b=>b.addEventListener("click", acoes[+b.dataset.recurso]));
  // versículo do dia: o mesmo para todos, muda à meia-noite
  const hoje = new Date(), dia = Math.floor(Date.UTC(hoje.getFullYear(), hoje.getMonth(), hoje.getDate()) / 864e5);
  const [l, c, v] = VERSOS_DIA[dia % VERSOS_DIA.length];
  const vez = ++est.vez;
  carregarLivro(est.traducao, l).then(livro=>{
    if(vez !== est.vez || !$("versoDia")) return;
    const texto = livro && livro[c-1] && livro[c-1][v-1];
    if(!texto) return;
    $("versoDia").textContent = `“${texto}”`;
    $("versoDiaRef").innerHTML = linkRef(l, c, v, esc(refStr(l, c, v)), "ref-dia");
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
  const par = (c.par||[]).map(([l,ch])=>linkRef(l, ch)).join(" · ");
  return `<dl class="ctx-grade">
    <dt>${x.autor}</dt><dd>${esc(c.a)}</dd>
    <dt>${x.data}</dt><dd>${esc(c.d)}</dd>
    <dt>${x.local}</dt><dd>${esc(c.l)}</dd>
    <dt>${x.publico}</dt><dd>${esc(c.p)}</dd>
    <dt>${x.tema}</dt><dd>${esc(c.t)}</dd>
    ${par ? `<dt>${x.paralelos}</dt><dd>${par}</dd>` : ""}
  </dl>
  <div class="ctx-barra"><i style="left:${+c.pos||0}%"></i></div>
  <div class="ctx-escala">${x.escala.map(e=>`<span>${e}</span>`).join("")}</div>`;
}

/* ---------- leitura ---------- */
async function renderizarCapitulo(op){
  const x = t(), leitor = $("leitor"), vez = ++est.vez;
  const info = infoLivro(est.livro);
  if(est.cap > info.ch || est.cap < 1) est.cap = 1;
  leitor.classList.add("carregando");
  const [livro, livroComp] = await Promise.all([
    carregarLivro(est.traducao, est.livro),
    est.comparar ? carregarLivro(est.comparar, est.livro) : null,
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
  const versosComp = livroComp ? (livroComp[est.cap-1]||[]) : null;
  if(est.corrida){
    html += `<p class="escritura corrida">` + versos.filter(Boolean).map(esc).join(" ") + `</p>`;
  } else {
    versos.forEach((texto, i)=>{
      if(!texto && !(versosComp && versosComp[i])) return;
      const v = i+1, chave = `${est.livro}.${est.cap}.${v}`;
      const marca = CORES.includes(est.marcas[chave]) ? " m-"+est.marcas[chave] : "";
      const temNota = est.notas[chave] ? `<span class="indicadores" title="${x.anotacao}">✎</span>` : "";
      html += `<div class="verso${marca}" id="v${v}" data-v="${v}" tabindex="0">
        <p class="escritura"><sup>${v}</sup>${esc(texto)}${temNota}</p>
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
  leitor.querySelectorAll(".verso").forEach(el=>{
    // com uma gaveta aberta, passar o mouse por outro versículo não troca o ativo (senão a gaveta fecha sozinha)
    // logo depois de chegar por um link, o mouse parado em cima de outro versículo também não rouba o destaque
    el.addEventListener("mouseenter", ()=>{ montarBarra(el); if(!est.gaveta && Date.now() > (est.semHover||0)) ativarVerso(el); });
    el.addEventListener("focus", ()=>montarBarra(el));
    el.addEventListener("click", (e)=>{ if(e.target.closest(".barra,.gavetas")) return; ativarVerso(el, true); });
    el.addEventListener("keydown", (e)=>{
      if(e.target === el && (e.key === "Enter" || e.key === " ")){ e.preventDefault(); ativarVerso(el, true); }
    });
  });
  atualizarNav();
  const alvo = est.alvoV && leitor.querySelector(`.verso[data-v="${est.alvoV}"]`);
  if(alvo) irAoVerso(alvo, est.abrir);
  else if(!op.manter && est.pronto) window.scrollTo({ top:0, behavior:"instant" });
  est.abrir = null;
}
/* Rola até o versículo pedido (busca, referência cruzada, link com #v16), destaca e abre as ferramentas dele. */
function irAoVerso(el, abrir){
  est.semHover = Date.now() + 900;
  el.scrollIntoView({ block:"center", behavior:"instant" });
  el.classList.remove("destino"); void el.offsetWidth; el.classList.add("destino");
  ativarVerso(el, true);
  if(abrir) acaoVerso(el, +el.dataset.v, abrir);
}

function ativarVerso(el, toque){
  if(est.versoAtivo && est.versoAtivo!==el){ est.versoAtivo.classList.remove("ativo"); fecharGavetas(est.versoAtivo); }
  est.versoAtivo = el;
  el.classList.add("ativo");
  const topoFixo = document.querySelector(".topo").getBoundingClientRect().bottom;
  el.classList.toggle("barra-baixo", el.getBoundingClientRect().top < topoFixo + 28);
  montarBarra(el);
  if(toque || est.ultimoEstudo !== el.dataset.v + est.cap + est.livro){
    est.ultimoEstudo = el.dataset.v + est.cap + est.livro;
    atualizarEstudo(+el.dataset.v);
  }
}
function fecharGavetas(el){ const g = el.querySelector(".gavetas"); if(g) g.innerHTML=""; est.gaveta=null; }

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
    b.addEventListener("click", ()=>{
      const c = b.dataset.cor;
      if(est.marcas[chave]===c){ delete est.marcas[chave]; } else { est.marcas[chave]=c; }
      gravarLS("logos_marcas", est.marcas); tocar("marca", chave);
      CORES.forEach(o=>el.classList.toggle("m-"+o, est.marcas[chave]===o));
      barra.querySelectorAll(".cor").forEach(o=>{
        o.classList.toggle("sel", est.marcas[chave]===o.dataset.cor);
        o.setAttribute("aria-pressed", est.marcas[chave]===o.dataset.cor);
      });
    });
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
/* Grade palavra por palavra (gaveta "Original" e coluna do modo estudo). */
function gradeInterlinear(palavras, ehAT){
  return `<div class="inter-grid" ${ehAT?'dir="rtl"':''}>` + palavras.map(p=>
    `<button class="inter-palavra" data-strong="${esc(p[2]||"")}">
       <span class="ip-surf escritura" ${ehAT?'dir="rtl" lang="he"':'lang="grc"'}>${esc(p[0].replace(/\\/g, ""))}</span>
       <span class="ip-translit">${esc(p[1])}</span>
       <span class="ip-gloss">${esc(p[3])}</span>
       <span class="ip-strong">${esc(p[2]||"")}</span>
     </button>`).join("") + `</div><div class="lex-caixa oculto" aria-live="polite"></div>`;
}
function ligarLexico(alvo, completo){
  const x = t(), caixa = alvo.querySelector(".lex-caixa");
  alvo.querySelectorAll(".inter-palavra").forEach(btn=>btn.addEventListener("click", async ()=>{
    const strong = btn.dataset.strong;
    alvo.querySelectorAll(".inter-palavra").forEach(o=>o.classList.remove("sel"));
    if(!strong || (caixa.dataset.atual===strong && !caixa.classList.contains("oculto"))){
      caixa.classList.add("oculto"); caixa.dataset.atual=""; return;
    }
    btn.classList.add("sel");
    caixa.dataset.atual = strong;
    caixa.classList.remove("oculto");
    caixa.innerHTML = `<em>${x.carregando}</em>`;
    const lex = await carregarLexico(strong[0]);
    const ent = lex && lex[strong];
    if(caixa.dataset.atual !== strong) return;
    if(!ent){ caixa.innerHTML = ""; caixa.classList.add("oculto"); return; }
    caixa.innerHTML = `
      <div class="lex-topo"><span class="escritura lex-lemma">${esc(ent.lemma)}</span>
        <span class="lex-translit">${esc(ent.translit)}</span>
        <span class="lex-num">${esc(strong)}</span></div>
      <p class="lex-def">${completo ? `<strong>${x.lexDef}:</strong> ` : ""}${esc((emPT() && ent.defpt) || ent.def)}</p>
      ${completo && ent.kjv && est.idioma==="en" ? `<p class="lex-def"><strong>${x.lexKjv}:</strong> ${esc(ent.kjv)}</p>` : ""}`;
  }));
}

async function acaoVerso(el, v, acao, botao){
  const x = t(), chave = `${est.livro}.${est.cap}.${v}`;
  const gavetas = el.querySelector(".gavetas");
  if(acao==="compartilhar"){
    const rot = botao.textContent; botao.textContent = x.gerandoImagem;
    try{ await compartilharVerso(v); } catch(e){ console.warn(e); }
    botao.textContent = rot;
    return;
  }
  if(acao==="copiar"){
    const ok = await copiarTexto(`“${est.versos[v-1] || ""}” — ${refStr(est.livro, est.cap, v)} (${nomeTraducao(est.traducao)})`);
    if(ok && botao){ const rot = botao.textContent; botao.textContent = x.copiado; setTimeout(()=>{ botao.textContent = rot; }, 1400); }
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
      const mss = ehAT ? "" : `<div class="mss-abas">
          <button data-mss="tr">Textus Receptus</button>
          <button data-mss="byz">Bizantino</button>
          <button data-mss="diff">Diferenças</button>
        </div><div class="mss-alvo"></div>`;
      gavetas.innerHTML = gaveta(rotulo, gradeInterlinear(palavras, ehAT) + mss + `<p class="fonte">${x.lexFonte}</p>`);
      ligarLexico(gavetas, true);
      gavetas.querySelectorAll(".mss-abas button").forEach(b=>b.addEventListener("click", async ()=>{
        const alvo = gavetas.querySelector(".mss-alvo");
        const ativa = b.classList.contains("ativa");
        gavetas.querySelectorAll(".mss-abas button").forEach(o=>o.classList.remove("ativa"));
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
    const achado = comentarioProximo(com, v);
    let corpo;
    if(achado){
      const nota = achado.v !== v
        ? `<p class="aviso-idioma">${achado.seguinte ? x.comInicio : x.comRef} ${achado.v} ${achado.seguinte ? "" : x.comBloco}</p>` : "";
      const longo = achado.texto.length > 1400;
      const aviso = est.idioma==="en" ? "" : (com.__pt ? x.tradAuto : x.avisoIdiomaComentario);
      const henry = com.__autor === "henry" ? `<p class="aviso-idioma">${x.notaHenry}</p>` : "";
      corpo = `${henry}${nota}<p class="comentario-texto${longo ? " recolhido" : ""}">${esc(achado.texto)}</p>
        ${longo ? `<button class="ler-mais" aria-expanded="false">${x.lerMais}</button>` : ""}
        <p class="fonte">${x.fonte}: ${autorComentario(com, x)}</p>
        ${aviso ? `<p class="aviso-idioma">${aviso}</p>` : ""}`;
    } else {
      const lv = est.livrosCom || {calvin:[], henry:[]};
      corpo = `<p class="comentario-texto">${autorDoLivro(lv, est.livro) ? x.semComentario : x.semLivroCalvin}</p>`;
    }
    gavetas.innerHTML = gaveta(x.comentario, corpo);
    const lm = gavetas.querySelector(".ler-mais");
    if(lm) lm.addEventListener("click", ()=>{
      const abrir = gavetas.querySelector(".comentario-texto").classList.toggle("recolhido") === false;
      lm.textContent = abrir ? x.lerMenos : x.lerMais;
      lm.setAttribute("aria-expanded", abrir);
    });
  }
  if(acao==="referencias"){
    const refs = await carregarRefs(est.livro, est.cap);
    if(!aberta()) return;
    const lista = refs ? refs[String(v)] : null;
    if(!lista || !lista.length){
      gavetas.innerHTML = gaveta(x.referencias, `<p class="comentario-texto">${x.semRefs}</p>`);
    } else {
      gavetas.innerHTML = gaveta(x.referencias,
        `<div class="refs">` + lista.map((r,ri)=>{
          const rot = esc(`${nomeLivro(r[0])} ${r[1]}:${r[2]}${r[3]>r[2] ? "-"+r[3] : ""}`);
          return `<div class="ref-item">${linkRef(r[0], r[1], r[2], rot, "ref-ir")}<span class="ref-previa" data-ri="${ri}"></span></div>`;
        }).join("") + `</div><p class="fonte">${x.refFonte}</p>`);
      lista.forEach(async (r,ri)=>{
        const livro = await carregarLivro(est.traducao, r[0]);
        const alvo = gavetas.querySelector(`.ref-previa[data-ri="${ri}"]`);
        if(alvo && livro && livro[r[1]-1] && livro[r[1]-1][r[2]-1]) alvo.textContent = livro[r[1]-1][r[2]-1];
      });
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
      const valor = gavetas.querySelector("#campoNota").value.trim();
      if(valor) est.notas[chave] = valor; else delete est.notas[chave];
      gravarLS("logos_notas", est.notas); tocar("nota", chave);
      fecharGavetas(el);
      // só o sinal de anotação deste versículo muda: a página não é redesenhada (e não pula para o topo)
      let sinal = el.querySelector(".indicadores");
      if(valor && !sinal){
        sinal = document.createElement("span");
        sinal.className = "indicadores"; sinal.title = x.anotacao; sinal.textContent = "✎";
        el.querySelector("p.escritura").appendChild(sinal);
      } else if(!valor && sinal) sinal.remove();
    });
    gavetas.querySelector("#campoNota").focus({ preventScroll:true });
    gavetas.firstElementChild.scrollIntoView({ block:"nearest" });   // a gaveta inteira à vista, com os botões fora da barra de baixo
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
/* "João 3:16", "jo 3 16", "1 co 13", "sl 23" -> {livro, cap, v} */
function parseRef(txt){
  const cru = txt.trim().toLowerCase();
  const m = normStr(cru).match(/^([1-3]?\s*[a-z]+(?:\s+[a-z]+)*)\.?\s*(\d+)(?:\s*[:.,\s]\s*(\d+))?(?:\s*-\s*\d+)?$/);
  if(!m) return null;
  const nome = m[1].replace(/\s+/g, "");
  let livro = null;
  if(/^jó/.test(cru)) livro = infoLivro("JOB");   // sem o acento, "jo" é João
  if(!livro && ABREV[nome]) livro = infoLivro(ABREV[nome]);
  const nomes = (b)=>[b.pt, b.en, b.es, b.id].map(n=>normStr(n).replace(/\s+/g, ""));
  if(!livro) livro = est.meta.books.find(b=>nomes(b).includes(nome));
  if(!livro && nome.length >= 3) livro = est.meta.books.find(b=>nomes(b).some(n=>n.startsWith(nome)));
  const cap = +m[2];
  if(!livro || cap < 1 || cap > livro.ch) return null;
  return { livro: livro.id, cap, v: +m[3] || 0 };
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
async function buscar(){
  if(est.buscaModo==="temas") return buscarTemas();
  if(est.buscaModo==="dicionario") return buscarDic();
  const x = t(), termo = $("campoBusca").value.trim();
  const res = $("buscaResultados"), status = $("buscaStatus");
  res.innerHTML = "";
  const ref = parseRef(termo);
  if(ref){ alternarPainel("painelBusca", false); return irPara(ref.livro, ref.cap, ref.v); }
  if(termo.length < 3){ status.textContent = x.digiteBusca; return; }
  const frase = normStr(termo).replace(/\s+/g, " ");
  const palavras = frase.split(" ").filter(p=>p.length > 1);
  const ids = $("chkBibliaToda").checked || est.vista==="inicio" ? est.meta.books.map(b=>b.id) : [est.livro];
  status.textContent = x.buscando;
  const vez = ++est.vezBusca;
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
  res.innerHTML = achados.slice(0, LIMITE).map(a=>
    `<a class="res" href="${urlCapitulo(a.usfm, a.cap, a.v)}" style="display:block;text-decoration:none;color:inherit">
       <div class="ref">${esc(refStr(a.usfm,a.cap,a.v))}</div><p>${destacar(a.texto, a.termos)}</p></a>`).join("");
}

function avisoConteudo(x, temPT){ return !emPT() ? "" : `<p class="aviso-en">${temPT ? x.tradAuto : x.conteudoEN}</p>`; }
function rotuloDuplo(tit, n){
  return tit[n] && tit[n].toLowerCase() !== n.toLowerCase()
    ? `${esc(tit[n])} <span style="opacity:.55;font-weight:400">(${esc(n)})</span>` : esc(n);
}
const RE_REF = /\b([1-3]?[A-Z]{2,3})\s(\d+):(\d+)(?:-(\d+))?/g;
function linkarRefs(txt){
  return esc(txt).replace(RE_REF, (m, l, c, v)=> infoLivro(l)
    ? linkRef(l, +c, +v, esc(`${nomeLivro(l)} ${c}:${v}`) + (m.includes("-") ? m.slice(m.indexOf("-")) : "")) : m);
}
/* Lista de verbetes (temas ou dicionário) e, ao escolher um, o conteúdo dele. */
function listarVerbetes(nomes, tit, abrir){
  const x = t(), res = $("buscaResultados"), status = $("buscaStatus");
  if(!nomes.length){ status.textContent = x.nadaEncontrado; return; }
  status.textContent = `${nomes.length} ${x.resultados}`;
  res.innerHTML = nomes.map((n,i)=>`<div class="res" data-n="${i}" tabindex="0" role="button"><div class="ref">${rotuloDuplo(tit, n)}</div></div>`).join("");
  res.querySelectorAll(".res").forEach(el=>{
    const ir = async ()=>{
      const nome = nomes[+el.dataset.n];
      res.innerHTML = `<h3 class="res-titulo">${rotuloDuplo(tit, nome)}</h3>` + await abrir(nome);
      status.textContent = "";
    };
    el.addEventListener("click", ir);
    el.addEventListener("keydown", (e)=>{ if(e.key==="Enter"){ ir(); } });
  });
}
async function buscarTemas(){
  const x = t(), termo = $("campoBusca").value.trim();
  $("buscaResultados").innerHTML = ""; $("buscaStatus").textContent = "";
  if(termo.length < 2){ $("buscaStatus").textContent = x.digiteBusca; return; }
  const [idx, alias, tit] = await Promise.all([idxTemas(), aliasPT(), emPT() ? titulos("topics") : {}]);
  const alvo = normStr(termo);
  const diretos = idx.filter(s=>normStr(s).includes(alvo) || (tit[s] && normStr(tit[s]).includes(alvo)));
  const viaAlias = Object.entries(alias).filter(([pt])=>normStr(pt).includes(alvo)).map(([,en])=>en);
  listarVerbetes([...new Set([...viaAlias, ...diretos])].slice(0, 40), tit, async (nome)=>{
    const secao = await temaSecao(nome[0].toUpperCase());
    return (secao[nome] || []).map(l=>`<p class="tema-linha">${linkarRefs(l.replace(/^-/, ""))}</p>`).join("") +
      `<p class="fonte">${x.fonteNave}</p>` + avisoConteudo(x, !!secao.__pt);
  });
}
async function buscarDic(){
  const x = t(), termo = $("campoBusca").value.trim();
  $("buscaResultados").innerHTML = ""; $("buscaStatus").textContent = "";
  if(termo.length < 2){ $("buscaStatus").textContent = x.digiteBusca; return; }
  const [idx, tit] = await Promise.all([idxDic(), emPT() ? titulos("dictionary") : {}]);
  const alvo = normStr(termo);
  listarVerbetes(idx.filter(s=>normStr(s).includes(alvo) || (tit[s] && normStr(tit[s]).includes(alvo))).slice(0, 40), tit, async (nome)=>{
    const dic = await dicLetra(nome[0].toUpperCase());
    return (dic[nome]||[]).map(d=>`<p class="dic-def">${esc(d)}</p>`).join("") +
      `<p class="fonte">${x.fonteEaston}</p>` + avisoConteudo(x, !!dic.__pt);
  });
}
function abrirBusca(modo){
  alternarPainel("painelBusca", true);
  const alvo = document.querySelector(`.busca-abas .aba[data-modo="${modo}"]`);
  if(alvo) alvo.onclick();
  $("campoBusca").focus();
}
function prepararAbas(){
  const x = t();
  const exemplo = ()=>est.buscaModo==="texto" ? x.exPlaceholder : est.buscaModo==="temas" ? x.exTema : x.exDic;
  document.querySelectorAll(".busca-abas .aba").forEach(b=>{
    b.textContent = b.dataset.modo==="texto" ? x.abaTexto : b.dataset.modo==="temas" ? x.abaTemas : x.abaDic;
    b.onclick = ()=>{
      est.buscaModo = b.dataset.modo;
      document.querySelectorAll(".busca-abas .aba").forEach(o=>{ o.classList.toggle("ativa", o===b); o.setAttribute("aria-selected", o===b); });
      document.querySelector(".busca-escopo").style.display = est.buscaModo==="texto" ? "" : "none";
      $("campoBusca").placeholder = exemplo();
      $("buscaResultados").innerHTML = ""; $("buscaStatus").textContent = "";
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
async function montarPlanos(planoAberto){
  const alvo = $("conteudoPlanos"), x = t();
  const ps = await planos();
  if(!planoAberto){
    alvo.innerHTML = ps.map(pl=>{
      const pct = pctPlano(pl);
      return `<div class="plano-card" data-id="${esc(pl.id)}" tabindex="0" role="button">
        <h3>${esc(pl.nome[est.idioma]||pl.nome.pt)}</h3>
        <div class="plano-barra"><i style="width:${pct}%"></i></div>
        <div class="plano-pct">${pct}% · ${pl.dias.length} ${x.dias}</div></div>`;
    }).join("");
    alvo.querySelectorAll(".plano-card").forEach(c=>{
      c.addEventListener("click", ()=>montarPlanos(c.dataset.id));
      c.addEventListener("keydown", (e)=>{ if(e.key==="Enter") montarPlanos(c.dataset.id); });
    });
    return;
  }
  const pl = ps.find(p=>p.id===planoAberto);
  const pr = est.progresso[pl.id] || {};
  alvo.innerHTML = `<button class="voltar-planos">‹ ${x.voltar}</button>
    <h3 class="plano-titulo">${esc(pl.nome[est.idioma]||pl.nome.pt)}</h3>` +
    pl.dias.map((caps,i)=>
      `<div class="dia-linha"><span class="dia-num">${x.dia} ${i+1}</span>
        <span class="dia-caps">${caps.map(([l,c])=>linkRef(l, c, 0, null, "")).join(", ")}</span>
        <input type="checkbox" class="dia-check" data-i="${i}" aria-label="${x.dia} ${i+1}" ${pr[i]?"checked":""}></div>`).join("");
  alvo.querySelector(".voltar-planos").addEventListener("click", ()=>montarPlanos(null));
  alvo.querySelectorAll(".dia-check").forEach(ch=>ch.addEventListener("change", ()=>{
    est.progresso[pl.id] = est.progresso[pl.id] || {};
    est.progresso[pl.id][ch.dataset.i] = ch.checked;
    gravarLS("logos_planos", est.progresso); tocar("plano", pl.id + "." + ch.dataset.i);
  }));
  const primeiro = pl.dias.findIndex((_,i)=>!pr[i]);
  if(primeiro > 3){ const el = alvo.querySelectorAll(".dia-linha")[primeiro]; if(el) el.scrollIntoView({block:"center"}); }
}

/* ---------- linha do tempo ---------- */
async function montarTempo(){
  if(!est.tempo){ est.tempo = await json("data/timeline.json"); }
  $("conteudoTempo").innerHTML = est.tempo.eras.map(era=>
    `<div class="era"><h3>${esc(era.nome)}</h3>` + era.eventos.map(ev=>
      `<div class="evento"><span class="data">${esc(ev.d)}</span>
       <span class="corpo">${esc(ev.t)} — ` + ev.r.map(([l,c])=>linkRef(l, c)).join(", ") +
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
    est.mapa = L.map("mapa").setView([31.77, 35.21], 6);
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",
      { attribution: '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>', maxZoom: 15 }).addTo(est.mapa);
  }
  setTimeout(()=>est.mapa.invalidateSize(), 150);
}
function buscarAtlas(){
  const termo = normStr($("campoAtlas").value.trim());
  const res = $("atlasResultados");
  if(termo.length < 2 || !est.lugares || !est.mapa){ res.innerHTML = ""; return; }
  const achados = est.lugares.filter(l=>normStr(l.n).includes(termo) || (l.p && normStr(l.p).includes(termo))).slice(0, 12);
  const nomeL = (l)=> (emPT() && l.p) || l.n;
  est.marcadores.forEach(m=>est.mapa.removeLayer(m)); est.marcadores = [];
  res.innerHTML = achados.length ? achados.map((l,i)=>`<div class="res" data-i="${i}"><div class="ref">${esc(nomeL(l))}</div>
    <p>${l.r.slice(0,6).map(([b,c,v])=>linkRef(b, c, v, esc(nomeLivro(b)+" "+c))).join(" · ")}</p></div>`).join("")
    : `<p class="busca-status">${t().nadaEncontrado}</p>`;
  achados.forEach(l=>{
    const m = L.marker([l.la, l.lo]).addTo(est.mapa).bindPopup(esc(nomeL(l)));
    est.marcadores.push(m);
  });
  if(achados.length){ est.mapa.setView([achados[0].la, achados[0].lo], achados.length===1 ? 9 : 7); est.marcadores[0].openPopup(); }
  res.querySelectorAll(".res").forEach(el=>el.addEventListener("click", (e)=>{
    if(e.target.closest("a")) return;
    mostrarLugar(achados[+el.dataset.i]);
  }));
}
const CIDADES_CHAVE = [["Jerusalém",31.7784,35.2354],["Babilônia",32.5364,44.4208],["Roma",41.8919,12.5113],["Éfeso",37.9411,27.3419],["Alexandria",31.2001,29.9187],["Damasco",33.5132,36.2919]];
function distKm(a1,o1,a2,o2){
  const R=6371, r=Math.PI/180;
  const dA=(a2-a1)*r, dO=(o2-o1)*r;
  const h=Math.sin(dA/2)**2 + Math.cos(a1*r)*Math.cos(a2*r)*Math.sin(dO/2)**2;
  return Math.round(2*R*Math.asin(Math.sqrt(h)));
}
function mostrarLugar(l){
  const res = $("atlasResultados");
  const refs = l.r.map(([b,c,v])=>linkRef(b, c, v)).join(" · ");
  const primeira = l.r[0], ultima = l.ult || l.r[l.r.length-1];
  const dists = CIDADES_CHAVE.filter(c=>c[0].toLowerCase()!==l.n.toLowerCase() && c[0] !== l.p)
    .map(c=>`${c[0]}: ${distKm(l.la,l.lo,c[1],c[2])} km`).slice(0,4).join(" · ");
  res.innerHTML = `<div class="lugar-card">
    <h3>${esc((emPT() && l.p) || l.n)}</h3>
    <p class="lugar-meta">${+l.tot} ocorrência(s) na Bíblia
      · Primeira: ${linkRef(primeira[0], primeira[1], primeira[2])}
      · Última: ${linkRef(ultima[0], ultima[1], ultima[2])}</p>
    <p class="lugar-refs">${refs}</p>
    <p class="lugar-dist">Distâncias aproximadas — ${dists}</p>
    ${l.f && /^https:\/\//.test(l.f) ? `<p class="lugar-meta"><a href="${esc(l.f)}" target="_blank" rel="noopener">Ver foto (Wikimedia Commons) ↗</a></p>` : ""}
  </div>`;
  est.mapa.setView([l.la, l.lo], 9);
}
async function montarViagens(){
  if(!est.viagens){ est.viagens = await json("data/journeys.json"); }
  const alvo = $("viagens");
  if(alvo.dataset.pronto) return;
  alvo.dataset.pronto = "1";
  alvo.innerHTML = est.viagens.map(v=>`<button data-v="${esc(v.id)}">${esc(v.nome.split(" (")[0])}</button>`).join("");
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
      .bindPopup(`<b>${i+1}. ${esc(p[0])}</b><br>` + p[2].map(([b,c,vv])=>linkRef(b, c, vv, null, "")).join(", "));
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

/* ---------- modo estudo ---------- */
function aplicarEstudo(){
  document.body.classList.toggle("estudo", est.estudo);
  $("colEstudo").classList.toggle("oculto", !est.estudo);
  $("btnEstudo").classList.toggle("ativa", est.estudo);
  $("btnEstudo").setAttribute("aria-pressed", est.estudo);
}
async function atualizarEstudo(v){
  if(!est.estudo || window.innerWidth < 1100) return;
  const x = t(), ref = esc(refStr(est.livro, est.cap, v)), chave = est.livro + est.cap + "." + v;
  const alvoO = $("estudoOriginal"), alvoC = $("estudoComentario");
  est.estudoAtual = chave;
  alvoO.innerHTML = alvoC.innerHTML = `<p class="estudo-vazio">${x.carregando}</p>`;
  const ehAT = infoLivro(est.livro).t==="AT";
  const [inter, com] = await Promise.all([carregarInterlinear(est.livro, est.cap), carregarComentario(est.livro, est.cap)]);
  if(est.estudoAtual !== chave) return;
  const palavras = inter && inter[v-1] ? inter[v-1] : [];
  if(palavras.length){
    alvoO.innerHTML = `<p class="lugar-meta" style="margin-top:0">${ref}</p>` + gradeInterlinear(palavras, ehAT);
    ligarLexico(alvoO, false);
  } else {
    alvoO.innerHTML = `<p class="estudo-vazio">${x.semOriginal}</p>`;
  }
  const achado = comentarioProximo(com, v);
  alvoC.innerHTML = achado
    ? `<p class="lugar-meta" style="margin-top:0">${ref} — ${autorComentario(com, x).split(" (")[0]}${achado.v !== v ? ` · ${achado.seguinte ? x.comInicio : x.comRef} ${achado.v}` : ""}</p>
       <p class="comentario-texto">${esc(achado.texto)}</p>
       ${est.idioma!=="en" ? `<p class="aviso-idioma">${com.__pt ? x.tradAuto : x.avisoIdiomaComentario}</p>` : ""}`
    : `<p class="estudo-vazio">${x.semComentario}</p>`;
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
async function compartilharVerso(v){
  const texto = est.versos[v-1] || "";
  const ref = refStr(est.livro, est.cap, v);
  const trad = nomeTraducao(est.traducao);
  await Promise.all([document.fonts.load('64px "Cardo"'), document.fonts.load('600 34px "Inter"'), document.fonts.load('600 40px "Cormorant Garamond"')]).catch(()=>{});
  const W = 1080, H = 1350, M = 120;
  const cv = document.createElement("canvas"); cv.width = W; cv.height = H;
  const c = cv.getContext("2d");
  const fundo = c.createLinearGradient(0, 0, W, H);
  fundo.addColorStop(0, "#1B2438"); fundo.addColorStop(1, "#131A2A");
  c.fillStyle = fundo; c.fillRect(0, 0, W, H);
  c.strokeStyle = "rgba(217,185,120,.55)"; c.lineWidth = 2; c.strokeRect(44, 44, W-88, H-88);
  // logotipo: o livro aberto com o ponto de luz (mesmo desenho do ícone do site)
  c.save(); c.translate(W/2 - 36, 128); c.scale(3, 3);
  c.strokeStyle = "#D9B978"; c.lineWidth = 1.5; c.lineCap = "round"; c.lineJoin = "round";
  c.stroke(new Path2D("M3 8c3-1.8 6-1.8 9 0c3-1.8 6-1.8 9 0v12c-3-1.8-6-1.8-9 0c-3-1.8-6-1.8-9 0z"));
  c.stroke(new Path2D("M12 8v12")); c.fillStyle = "#D9B978";
  c.beginPath(); c.arc(12, 3.4, 1.7, 0, Math.PI*2); c.fill(); c.restore();
  // texto do versículo, com a fonte reduzindo até caber
  let tam = 66, linhas, alt;
  do {
    c.font = `${tam}px "Cardo", Georgia, serif`;
    linhas = quebrarLinhas(c, `“${texto}”`, W - 2*M);
    alt = linhas.length * tam * 1.42;
    tam -= 2;
  } while(alt > H - 600 && tam > 30);
  c.fillStyle = "#F1E9D8"; c.textAlign = "center"; c.textBaseline = "middle";
  let y = (H - alt) / 2 + tam * 0.7 - 20;
  for(const l of linhas){ c.fillText(l, W/2, y); y += (tam + 2) * 1.42; }
  c.fillStyle = "#D9B978"; c.fillRect(W/2 - 40, y + 4, 80, 2);
  c.font = '600 34px "Inter", sans-serif';
  c.fillText(ref.toUpperCase(), W/2, y + 62);
  c.font = '400 26px "Inter", sans-serif'; c.fillStyle = "rgba(241,233,216,.6)";
  c.fillText(trad, W/2, y + 110);
  c.font = '600 44px "Cormorant Garamond", "Cardo", serif'; c.fillStyle = "#F1E9D8";
  c.fillText("S O L A", W/2, H - 158);
  c.font = '500 26px "Inter", sans-serif'; c.fillStyle = "#D9B978";
  c.fillText("solabiblia.com.br", W/2, H - 108);
  const blob = await new Promise(r=>cv.toBlob(r, "image/png"));
  const nome = `${normStr(ref).replace(/[^a-z0-9]+/g, "-")}.png`;   // sem acento: o Chrome descarta nomes com "ã"
  const arquivo = new File([blob], nome, { type: "image/png" });
  const link = "https://solabiblia.com.br" + urlCapitulo(est.livro, est.cap, v);
  if(navigator.canShare && navigator.canShare({ files: [arquivo] })){
    await navigator.share({ files: [arquivo], text: `${ref} — ${link}` }).catch(()=>{});
  } else {
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = nome;
    document.body.appendChild(a); a.click(); a.remove();   // o Chrome só respeita o nome com o link na página
    setTimeout(()=>URL.revokeObjectURL(a.href), 4000);
  }
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
    acoes.querySelector("#btnExportar").addEventListener("click", ()=>{
      const dados = { marcas: est.marcas, notas: est.notas, planos: est.progresso, v: 1 };
      const a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([JSON.stringify(dados, null, 1)], {type: "application/json"}));
      a.download = "sola-backup.json";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(()=>URL.revokeObjectURL(a.href), 4000);
    });
    acoes.querySelector("label").addEventListener("keydown", (e)=>{ if(e.key==="Enter") $("arqImportar").click(); });
    acoes.querySelector("#arqImportar").addEventListener("change", (e)=>{
      const f = e.target.files[0]; if(!f) return;
      const r = new FileReader();
      r.onload = ()=>{
        let msg = t().arquivoInvalido;
        try{
          const d = JSON.parse(r.result);
          if(d && typeof d === "object" && (d.marcas || d.notas || d.planos)){
            // junta com o que já existe neste navegador (não apaga nada); no mesmo versículo vale o do arquivo
            const nNotas = Object.keys(d.notas || {}).filter(k=>chaveValida(k) && typeof d.notas[k]==="string").length;
            const nMarcas = Object.keys(d.marcas || {}).filter(k=>chaveValida(k) && CORES.includes(d.marcas[k])).length;
            Object.assign(est.marcas, d.marcas); Object.assign(est.notas, d.notas);
            if(d.planos && typeof d.planos === "object") for(const id of Object.keys(d.planos))
              est.progresso[id] = Object.assign({}, est.progresso[id], d.planos[id]);
            limparDados();
            gravarLS("logos_marcas", est.marcas); gravarLS("logos_notas", est.notas); gravarLS("logos_planos", est.progresso);
            // o que veio do arquivo conta como alteração feita agora (sobe para a conta)
            Object.keys(d.notas || {}).forEach(k=>{ if(k in est.notas) tocar("nota", k); });
            Object.keys(d.marcas || {}).forEach(k=>{ if(k in est.marcas) tocar("marca", k); });
            DADOS.plano.chaves().forEach(k=>tocar("plano", k));
            msg = `${t().restaurado} ${nNotas} ${t().nAnot}, ${nMarcas} ${t().nMarc}.`;
            if(est.vista==="cap") renderizar({ manter:true });
          }
        }catch(err){}
        e.target.value = "";
        montarNotas(msg);
      };
      r.readAsText(f);
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
  let feitos = 0, falhas = 0;
  try{
    const cache = await caches.open(CACHE_DADOS);
    for(let i = 0; i < urls.length; i += 6){
      await Promise.all(urls.slice(i, i+6).map(u=>cache.add(u).then(()=>{ feitos++; }, ()=>{ falhas++; })));
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

/* ---------- painel "Meu estudo" ---------- */
async function montarMeuEstudo(){
  const x = t(), r = resumoEstudo(), alvo = $("conteudoEstudo");
  const ult = lerLS("logos_ultimo", null);
  const pct = r.total ? Math.round(r.lidos / r.total * 1000) / 10 : 0;
  const livros = (tst)=>est.meta.books.filter(b=>b.t===tst).map(b=>{
    const n = r.porLivro[b.id] || 0;
    return `<a class="lv${n >= b.ch ? " cheio" : ""}" href="${urlLivro(b.id)}" style="--p:${Math.round(n / b.ch * 100)}%"><span>${esc(nomeLivro(b.id))}</span><small>${n}/${b.ch}</small></a>`;
  }).join("");
  const marcas = Object.keys(est.marcas).filter(chaveValida).sort(ordemRef);
  const notas = Object.keys(est.notas).filter(chaveValida).sort(ordemRef);
  let planosHTML = "";
  try{ planosHTML = (await planos()).map(pl=>{ const p = pctPlano(pl); return p ? `<div class="plano-linha"><span>${esc(pl.nome[est.idioma]||pl.nome.pt)}</span><div class="plano-barra"><i style="width:${p}%"></i></div><small>${p}%</small></div>` : ""; }).join(""); }catch(e){}
  alvo.innerHTML = contaHTML() + `
    <div class="estudo-numeros">
      <div class="num largo"><b>${r.lidos.toLocaleString(est.idioma)}</b><span>${x.de} ${r.total.toLocaleString(est.idioma)} ${x.capsLidos} · ${pct.toLocaleString(est.idioma)}%</span>
        <div class="plano-barra"><i style="width:${pct}%"></i></div></div>
      <div class="num">${ico("chama")}<b>${r.seq}</b><span>${x.diasSeguidos}</span></div>
      <div class="num"><b>${r.notas}</b><span>${x.nNotasRot}</span></div>
      <div class="num"><b>${r.marcas}</b><span>${x.nMarcasRot}</span></div>
    </div>
    ${ult && infoLivro(ult.livro) ? `<p class="estudo-continuar"><a class="btn-ouro" href="${urlCapitulo(ult.livro, ult.cap)}">${x.continuar} ${esc(nomeLivro(ult.livro))} ${+ult.cap} ${ico("seta")}</a></p>` : ""}
    <h3 class="estudo-sub">${x.progLivros}</h3>
    ${r.lidos ? "" : `<p class="fonte">${x.semLeitura}</p>`}
    <p class="rotulo-secao pequeno">${x.at}</p><div class="lvs">${livros("AT")}</div>
    <p class="rotulo-secao pequeno">${x.nt}</p><div class="lvs">${livros("NT")}</div>
    ${planosHTML ? `<h3 class="estudo-sub">${x.planosTit}</h3>${planosHTML}` : ""}
    <h3 class="estudo-sub">${x.marcacoes}</h3>
    ${marcas.length ? `<div class="marcas-lista">` + marcas.slice(0, 120).map(k=>{ const [l, c, v] = k.split("."); return linkRef(l, +c, +v, esc(refStr(l, +c, +v)), "m-chip m-" + est.marcas[k]); }).join("") + `</div>` : `<p class="fonte">${x.semMarcas}</p>`}
    <h3 class="estudo-sub">${x.notas}</h3>
    ${notas.length ? notas.slice(0, 4).map(k=>{ const [l, c, v] = k.split("."); return `<p class="nota-curta">${linkRef(l, +c, +v, esc(refStr(l, +c, +v)), "")} ${esc(est.notas[k].slice(0, 140))}${est.notas[k].length > 140 ? "…" : ""}</p>`; }).join("") : ""}
    <p><button class="btn-linha" id="btnTodasNotas">${notas.length ? x.verTodas + " (" + notas.length + ")" : x.notas} · ${x.backup}</button></p>
    ${est.sessao ? `<p class="estudo-rodape"><button class="link-discreto" id="btnExcluirConta">${x.excluirConta}</button></p>` : ""}`;
  $("btnTodasNotas").addEventListener("click", ()=>{ montarNotas(); alternarPainel("painelNotas", true); });
  ligarConta();
}
function abrirMeuEstudo(){ montarMeuEstudo(); alternarPainel("painelEstudo", true); }

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
function contaHTML(){
  const x = t();
  if(!temConta()) return `<p class="conta-local">${x.contaLocal}</p>`;
  if(!est.sessao) return `<div class="conta-caixa">
      <div><h3>${ico("nuvem")} ${x.contaTitulo}</h3><p>${x.contaTexto}</p></div>
      <div class="conta-acoes">
        ${CONTA.google ? `<button class="btn-ouro" id="btnGoogle">${x.entrarGoogle}</button>` : ""}
        ${CONTA.email ? `<form id="formEmail"><input type="email" required autocomplete="email" placeholder="${x.seuEmail}" aria-label="${x.seuEmail}"><button class="btn-linha">${x.entrarEmail}</button></form>` : ""}
      </div>
      <p class="fonte" id="contaAviso" role="status"></p></div>`;
  const u = est.sessao.user, nome = (u.user_metadata && (u.user_metadata.full_name || u.user_metadata.name)) || u.email || "";
  return `<div class="conta-caixa logada">
      <div class="conta-quem"><span class="conta-letra" aria-hidden="true">${esc((nome[0] || "?").toUpperCase())}</span>
        <div><strong>${esc(nome)}</strong><span id="sincEstado" role="status">${textoSinc()}</span></div></div>
      <div class="conta-acoes"><button class="btn-linha" id="btnSincAgora">${x.sincAgora}</button><button class="btn-linha" id="btnSair">${x.sair}</button></div>
      <p class="fonte" id="contaAviso" role="status"></p></div>`;
}
function textoSinc(){
  const x = t();
  if(est.sincEstado === "indo") return x.sincIndo;
  if(est.sincEstado === "erro") return x.sincErro;
  return est.sinc.ultima ? `${x.sincOk} · ${new Date(est.sinc.ultima).toLocaleTimeString(est.idioma, { hour:"2-digit", minute:"2-digit" })}` : "";
}
function estadoSinc(e){ est.sincEstado = e; const el = $("sincEstado"); if(el) el.textContent = textoSinc(); }
function avisoConta(texto){ const el = $("contaAviso"); if(el) el.textContent = texto; }
function ligarConta(){
  const x = t(), em = (id, f)=>{ const el = $(id); if(el) el.addEventListener("click", f); };
  const entrar = async (como)=>{
    try{
      const sb = await clienteConta();
      try{ sessionStorage.setItem("sola_volta", location.pathname + location.hash); }catch(e){}
      const { error } = await como(sb);
      if(error) throw error;
    }catch(e){ console.warn("conta", e); avisoConta(x.erroConta); }
  };
  em("btnGoogle", ()=>entrar(sb=>sb.auth.signInWithOAuth({ provider:"google", options:{ redirectTo: location.origin + "/" } })));
  const fe = $("formEmail");
  if(fe) fe.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const email = fe.querySelector("input").value.trim();
    await entrar(sb=>sb.auth.signInWithOtp({ email, options:{ emailRedirectTo: location.origin + "/" } }));
    if(!$("contaAviso").textContent) avisoConta(`${x.linkEnviado} ${email}.`);
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
      try{ localStorage.removeItem("logos_ultimo"); }catch(e){}
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
  if(!$("painelEstudo").classList.contains("oculto")) montarMeuEstudo();
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
  estado:{ chaves:()=>lerLS("logos_ultimo", null) ? ["ultimo"] : [], ler:(k)=>k === "ultimo" ? lerLS("logos_ultimo", null) : null,
           por:(k, v)=>{ if(k === "ultimo" && v && infoLivro(v.livro) && capValido(v.livro + "." + v.cap)) gravarLS("logos_ultimo", { livro: v.livro, cap: +v.cap }); },
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
function aplicarTema(){
  const escuro = est.tema==="escuro";
  document.documentElement.dataset.tema = escuro ? "escuro" : "claro";
  $("btnTema").innerHTML = ico(escuro ? "sol" : "lua");
  $("metaTema").content = escuro ? "#0C1019" : "#F7F3EA";
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
async function iniciar(){
  est.idioma = lerLS("logos_idioma","pt"); if(!UI[est.idioma]) est.idioma = "pt";
  est.tema = document.documentElement.dataset.tema || "claro";
  try{ est.meta = await json("data/books.json"); }
  catch(e){ avisar(t().erroIniciar, t().recarregar, ()=>location.reload()); return; }
  est.traducao = lerLS("logos_trad","blivre");
  if(!est.meta.translations.find(tr=>tr.id===est.traducao)) est.traducao = "blivre";
  limparDados();
  const rota = lerRota();
  const antigo = /^#\//.test(location.hash) || !rotaDe(location.pathname, "");

  $("selIdioma").value = est.idioma;
  aplicarTextos(); preencherTraducoes(); aplicarTema(); aplicarEstudo();
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
  });
  $("selTraducao").addEventListener("change", (e)=>{
    est.traducao = e.target.value; gravarLS("logos_trad", est.traducao);
    preencherTraducoes(); renderizar({ manter:true });
  });
  $("selComparar").addEventListener("change", (e)=>{ est.comparar = e.target.value; renderizar({ manter:true }); });
  $("btnLivros").addEventListener("click", ()=>{ montarListaLivros(); alternarPainel("painelLivros"); });
  $("btnMeuEstudo").addEventListener("click", abrirMeuEstudo);
  $("btnBusca").addEventListener("click", ()=>abrirBusca("texto"));
  $("navTemas").addEventListener("click", ()=>abrirBusca("temas"));
  $("navDic").addEventListener("click", ()=>abrirBusca("dicionario"));
  $("navTempo").addEventListener("click", ()=>{ montarTempo(); alternarPainel("painelTempo"); });
  $("navAtlas").addEventListener("click", abrirAtlas);
  $("navContexto").addEventListener("click", abrirContexto);
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
  });
  $("btnAjustes").addEventListener("click", ()=>{
    const aberto = document.querySelector(".controles").classList.toggle("aberto");
    $("btnAjustes").classList.toggle("ativa", aberto);
    $("btnAjustes").setAttribute("aria-expanded", aberto);
  });
  $("btnOffline").addEventListener("click", baixarOffline);
  document.querySelectorAll("[data-painel]").forEach(a=>a.addEventListener("click", (e)=>{
    e.preventDefault();
    const id = a.dataset.painel;
    if(id==="painelAtlas") return abrirAtlas();
    if(id==="painelPlanos") montarPlanos(null);
    if(id==="painelTempo") montarTempo();
    if(id==="painelNotas") montarNotas();
    if(id==="painelEstudo") montarMeuEstudo();
    alternarPainel(id, true);
  }));
  $("btnAtlasBuscar").addEventListener("click", buscarAtlas);
  $("campoAtlas").addEventListener("keydown", (e)=>{ if(e.key==="Enter") buscarAtlas(); });
  $("btnBuscar").addEventListener("click", buscar);
  $("campoBusca").addEventListener("keydown", (e)=>{ if(e.key==="Enter") buscar(); });
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
    const mesma = r.vista===est.vista && (r.vista==="inicio" || r.livro===est.livro) && (r.vista!=="cap" || r.cap===est.cap);
    if(mesma && !antigoHash){
      const alvo = r.v && document.querySelector(`.verso[data-v="${r.v}"]`);
      if(alvo){ est.alvoV = r.v; irAoVerso(alvo); }
      return;
    }
    fecharPaineis();
    navegar(r, { substituir: antigoHash });
  };
  window.addEventListener("popstate", seguirRota);
  window.addEventListener("hashchange", ()=>{ if(/^#\//.test(location.hash)) seguirRota(); });

  document.addEventListener("keydown", (e)=>{
    if(e.key === "Escape"){
      if(painelAberto()) return fecharPaineis();
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
}
iniciar();
