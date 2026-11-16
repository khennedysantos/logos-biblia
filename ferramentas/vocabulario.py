"""Vocabulário: palavras difíceis, antigas ou técnicas do texto da Bíblia Livre, com o sentido em português de hoje.

É a segunda camada de sublinhado do capítulo (traço pontilhado). A primeira, a das palavras-chave, fica em
gerar_palavras.py e fala da palavra original; esta explica a palavra em português: medidas, moedas, objetos do
culto, povos, cargos e palavras que o leitor de hoje não usa ou entende de outro jeito.

  t(palavra, formas, significado, nota, s=(...), exige=False, id=None)

  palavra      como aparece no topo do cartão (None = a própria palavra sublinhada, para listas como as pedras)
  formas       expressão regular das formas no texto, sem diferença de maiúsculas; use (?-i:...) para exigir
               minúscula ("him", a medida, não o nome próprio)
  significado  o sentido, curto
  nota         uma ou duas frases a mais (opcional)
  s            números de Strong que correspondem à palavra. Quando um deles está no versículo, o cartão mostra
               também a palavra original
  exige        só sublinha onde um dos números de s estiver no versículo (para palavras com outro sentido
               comum: "funda" a arma, não "cova funda")

Cada termo é sublinhado na primeira vez em que aparece em cada capítulo. A ordem importa: quando duas entradas
cobrem o mesmo trecho, vale a que vem antes ("mar de fundição" antes de "fundição").
Depois de mexer aqui: python3 ferramentas/gerar_palavras.py  (e --relatorio para conferir onde cada uma caiu).
"""

TERMOS = []


def t(palavra, formas, significado, nota=None, s=(), exige=False, id=None):
    TERMOS.append({"palavra": palavra, "formas": formas, "significado": significado, "nota": nota,
                   "s": tuple(s), "exige": exige, "id": id})


# ------------------------------------------------------------------ medidas
t("côvado", r"côvados?", "medida de comprimento: do cotovelo à ponta do dedo médio, cerca de 45 cm",
  "Ezequiel usa um côvado maior, de cerca de 52 cm (Ezequiel 40:5).", s=("H520", "G4083"))
t("palmo", r"palmos?", "a mão aberta, do polegar à ponta do mínimo: cerca de 22 cm (meio côvado)", s=("H2239",),
  exige=True)
t("palmo (largura da mão)", r"palmos?", "a largura da mão, quatro dedos juntos: cerca de 7,5 cm",
  s=("H2947", "H2948"), exige=True, id="palmo-mao")
t("cana", r"canas?", "junco, planta de caule oco",
  "Também a haste do candelabro e, em Ezequiel e no Apocalipse, uma vara de medir de cerca de 3 metros "
  "(Ezequiel 40:5; Apocalipse 21:15).", s=("H7070", "G2563"))
t("estádio", r"estádios?", "medida grega de distância, cerca de 185 metros",
  "Emaús ficava a sessenta estádios de Jerusalém: uns 11 km (Lucas 24:13).", s=("G4712",))
t("milha", r"milhas?", "a milha romana, cerca de 1,5 km", s=("G3400",), exige=True)
t("jeira", r"jeiras?", "a área que uma junta de bois ara em um dia", s=("H6776",))
t("efa", r"(?-i:efas?)", "medida de grãos, cerca de 22 litros (as estimativas variam)",
  "Dez efas fazem um ômer, a medida grande (Ezequiel 45:11).", s=("H374",))
t("bato", r"batos?", "medida de líquidos (vinho, azeite) igual ao efa: cerca de 22 litros", s=("H1324",), exige=True)
t("him", r"(?-i:him)", "medida de líquidos, cerca de 4 litros (as estimativas variam)", s=("H1969",))
t("logue", r"logues?", "pequena medida de azeite, cerca de um terço de litro", s=("H3849",))
t("coro", r"coros?", "a maior medida de grãos e de azeite: dez batos, cerca de 220 litros", s=("H3734",), exige=True)
t("ômer", r"ômer(?:es)?", "medida grande de grãos, a carga de um jumento: dez efas, cerca de 220 litros",
  s=("H2563",), exige=True, id="omer")
t("ômer (feixe)", r"ômer(?:es)?", "feixe de espigas",
  "Na festa das primícias, o primeiro feixe da colheita era movido diante do SENHOR (Levítico 23:10-11).",
  s=("H6016",), exige=True, id="omer-feixe")
t("gômer", r"(?-i:gômer(?:es)?)", "medida de cerca de 2 litros, a décima parte do efa (Êxodo 16:36)",
  "Era a porção de maná que cada pessoa colhia por dia no deserto (Êxodo 16:16).", s=("H6016",))

# ------------------------------------------------------------------ pesos e dinheiro
t("siclo", r"siclos?", "unidade de peso, cerca de 11,5 gramas",
  "Antes das moedas, pagava-se pesando prata: 'trinta siclos de prata' é um preço, não um número de moedas.",
  s=("H8255",))
t("óbolo", r"óbolos?", "a menor unidade de peso: a vigésima parte do siclo, cerca de meio grama", s=("H1626",))
t("mina", r"minas?", "peso de cerca de 600 gramas (50 a 60 siclos)",
  "Na parábola de Lucas 19, a mina é uma quantia de dinheiro: cerca de cem denários, uns cem dias de trabalho.",
  s=("H4488", "G3414"), exige=True)
t("talento", r"talentos?", "a maior unidade de peso, cerca de 34 kg (3.000 siclos)",
  "Um talento de prata era uma fortuna: no Novo Testamento, uns 6.000 denários, o salário de vinte anos "
  "(Mateus 18:24; 25:15).", s=("H3603", "G5007"))
t("dracma", r"dracmas?", "moeda grega de prata, de valor parecido com o denário",
  "Em Esdras e Neemias, as 'dracmas de ouro' são moedas persas de ouro (dáricos).",
  s=("G1406", "H1871", "H150"))
t("denário", r"denários?", "moeda romana de prata: o pagamento de um dia de trabalho (Mateus 20:2)", s=("G1220",))

# ------------------------------------------------------------------ tabernáculo e templo
t("tabernáculo", r"tabernáculos?", "a tenda sagrada onde Deus habitava no meio de Israel, no deserto",
  "Era desmontável e acompanhou o povo até a construção do templo de Salomão (Êxodo 25–40).",
  s=("H4908", "H168", "G4633"))
t("lugar santíssimo", r"(?:lugar|o) santíssimo", "a sala mais interna do tabernáculo e do templo, onde ficava a arca",
  "Só o sumo sacerdote entrava ali, uma vez por ano, no Dia da Expiação (Levítico 16; Hebreus 9:7).", s=("H6944",))
t("pães da proposição", r"pães da proposição",
  "os doze pães postos toda semana sobre a mesa do Lugar Santo, diante de Deus (Levítico 24:5-9)",
  "Depois de trocados, eram comidos pelos sacerdotes; Davi os comeu numa emergência (1 Samuel 21:6; Marcos 2:26).",
  s=("G4286",))
t("candelabro", r"candelabros?|castiçal|castiçais",
  "o candelabro de ouro de sete braços (a menorá), que iluminava o Lugar Santo",
  "No Apocalipse, os candelabros representam as igrejas (Apocalipse 1:20).", s=("H4501", "G3087"))
t("átrio", r"átrios?", "o pátio cercado em volta do tabernáculo e, depois, do templo", s=("H2691", "G833"))
t("alpendre", r"alpendres?|pórticos?", "varanda coberta na entrada de um edifício",
  "No templo, a grande entrada da frente; no tempo de Jesus, o 'pórtico de Salomão' era uma galeria coberta do "
  "templo (João 10:23).", s=("H197", "G4745"))
t("pia", r"pias?", "a grande bacia de bronze onde os sacerdotes lavavam as mãos e os pés antes de servir",
  "Ficava entre a tenda e o altar (Êxodo 30:18-21).", s=("H3595",), exige=True)
t("mar de fundição", r"mar de fundição",
  "o 'mar' do templo de Salomão: uma enorme bacia de bronze fundido, sobre doze bois",
  "Guardava a água em que os sacerdotes se lavavam (1 Reis 7:23-26; 2 Crônicas 4:6).")
t("de fundição", r"(?:imagens?|deuses|bezerros?|ídolos?|estátuas?) de fundição|de fundição",
  "feito de metal derretido despejado num molde (diz-se sobretudo dos ídolos)",
  "O bezerro de ouro era 'de fundição' (Êxodo 32:4).", s=("H4541",))
t("capitel", r"capitéis|capitel", "a parte de cima de uma coluna, trabalhada e enfeitada", s=("H3805",))
t("querubim", r"querubins?|querubim", "ser celestial que guarda a presença de Deus",
  "Querubins guardaram o caminho do Éden (Gênesis 3:24), e duas figuras deles, de ouro, cobriam a arca com as "
  "asas (Êxodo 25:18-20).", s=("H3742", "G5502"))
t("serafim", r"serafins?|serafim", "ser celestial de seis asas, que Isaías viu diante do trono de Deus (Isaías 6:2)",
  "O nome lembra 'ardentes'.", s=("H8314",))

# ------------------------------------------------------------------ sacerdotes e suas vestes
t("levitas", r"levitas?", "os descendentes de Levi, a tribo separada para o serviço do santuário",
  "Os sacerdotes eram os levitas da família de Arão; os demais cuidavam da tenda e do templo, da música e do "
  "ensino. Não receberam território: viviam dos dízimos (Números 18:21).", s=("H3881", "G3019"))
t("éfode", r"éfodes?", "veste sacerdotal, uma espécie de avental bordado com ouro, usado pelo sumo sacerdote",
  "O peitoral ficava preso a ele (Êxodo 28:6-14). Houve também éfodes usados como objeto de culto, até de "
  "idolatria (Juízes 8:27).", s=("H646",))
t("peitoral", r"peitora(?:l|is)",
  "peça quadrada presa ao éfode, sobre o peito do sumo sacerdote, com doze pedras preciosas",
  "Cada pedra levava o nome de uma tribo de Israel (Êxodo 28:15-21).", s=("H2833",))
t("Urim e Tumim", r"urim|tumim",
  "objetos guardados no peitoral do sumo sacerdote, usados para consultar a vontade de Deus (Êxodo 28:30)",
  "Não se sabe exatamente como eram. Os nomes significam 'luzes' e 'perfeições'.", s=("H224", "H8550"))
t("mitra", r"mitras?", "o turbante de linho do sumo sacerdote",
  "Na frente levava uma lâmina de ouro com as palavras 'Santidade ao SENHOR' (Êxodo 28:36-38).", s=("H4701",))
t("redenho", r"redenhos?", "a parte gordurosa presa ao fígado, queimada no altar com a gordura do animal",
  s=("H3508",))

# ------------------------------------------------------------------ sacrifícios e ritos
t("holocausto", r"holocaustos?", "sacrifício em que o animal era inteiramente queimado no altar, entregue todo a Deus",
  "É o sentido original da palavra (Levítico 1).", s=("H5930", "G3646"))
t("sacrifícios pacíficos", r"(?:sacrifícios?|ofertas?) pacífic[oa]s?|pacífic[oa]s",
  "sacrifício de comunhão: parte era queimada no altar, parte ficava para os sacerdotes, e o resto era comido em "
  "festa pelo ofertante e sua família", "Expressava paz e comunhão com Deus (Levítico 3; 7:11-18).",
  s=("H8002",), exige=True)
t("oferta movida", r"ofertas? movidas?|(?:sacrifício|peito) movido",
  "parte do sacrifício que o sacerdote erguia e movia diante do altar, apresentando-a a Deus",
  "Depois ficava para os sacerdotes (Levítico 7:30-34).", s=("H8573",))
t("flor de farinha", r"flor de farinha", "a farinha mais fina, peneirada: a melhor, usada nas ofertas", s=("H5560",))
t("libação", r"libaç(?:ão|ões)", "oferta de bebida (vinho) derramada junto com o sacrifício",
  "Paulo usa a imagem para a própria vida, que estava sendo derramada (Filipenses 2:17; 2 Timóteo 4:6).",
  s=("H5262", "G4689"))
t("primícias", r"primícias?", "os primeiros frutos da colheita (e as primeiras crias), entregues a Deus",
  "Reconheciam que tudo vem dele (Êxodo 23:19). Paulo chama Cristo ressuscitado de 'primícias' dos que morreram "
  "(1 Coríntios 15:20).", s=("H7225", "H1061", "G536"))
t("dízima (medida)", r"dízim[oa]s?", "a décima parte de um efa: cerca de 2 litros de farinha",
  "Em Levítico e Números, 'duas dízimas de flor de farinha' é uma quantidade, não o dízimo.",
  s=("H6241",), exige=True, id="dizima-medida")
t("dízimo", r"dízim[oa]s?", "a décima parte da colheita, do rebanho ou do ganho, entregue a Deus",
  "Sustentava os levitas, os pobres e as festas (Deuteronômio 14:22-29).",
  s=("H4643", "H6237", "G1181", "G586", "G1183"), exige=True)
t("expiação", r"expiaç(?:ão|ões)",
  "cobrir a culpa por meio de um sacrifício, para restaurar a relação com Deus",
  "Em Levítico, 'expiação' também é o nome do sacrifício oferecido pelo pecado ('o novilho da expiação').",
  s=("H3722", "H2403", "H3725"))
t("incenso", r"incensos?", "mistura de resinas aromáticas queimada no altar do incenso, de manhã e à tarde",
  "É imagem das orações que sobem a Deus (Salmo 141:2; Apocalipse 8:3-4).", s=("H7004", "H3828", "H6999", "G2368"))
t("incensário", r"incensários?", "recipiente onde se punham brasas para queimar incenso",
  s=("H4289", "H4730", "G2369", "G3031"))
t("aspergir", r"esparg\w+|asperg\w+|aspersão", "borrifar (sangue, água ou azeite)",
  "Era gesto de purificação e de consagração (Êxodo 24:8; Hebreus 9:19-22).", s=("H2236", "H5137", "G4472"))
t("ungir", r"ung(?:ir|iu|iram|irá|irás|irão|irei|i|e|es|em|ia|indo|id[oa]s?)|unç(?:ão|ões)",
  "derramar azeite sobre alguém ou algo para separá-lo para Deus",
  "Assim eram consagrados reis, sacerdotes e profetas. 'Messias' (hebraico) e 'Cristo' (grego) significam "
  "'ungido'.", s=("H4886", "H4888", "G5548", "G218", "G5545"))
t("nazireu", r"nazireus?|nazireado",
  "pessoa consagrada a Deus por um voto: não bebia vinho, não cortava o cabelo e não tocava em mortos",
  "O voto podia ser por um tempo ou pela vida toda, como o de Sansão (Números 6; Juízes 13:5).",
  s=("H5139", "H5145"))
t("ázimos", r"ázimos?", "pães sem fermento",
  "A Festa dos Pães Ázimos, logo depois da Páscoa, lembrava a pressa da saída do Egito (Êxodo 12:39).",
  s=("H4682", "G106"))
t("levedado", r"leved\w+", "fermentado, feito com fermento (levedura)",
  "Na Páscoa, todo fermento era tirado de casa (Êxodo 12:15). Jesus usa o fermento como imagem do que se "
  "espalha por dentro, para o bem ou para o mal (Mateus 13:33; 16:6).", s=("H2557", "H7603", "G2219"))

# ------------------------------------------------------------------ festas e calendário
t("Festa dos Tabernáculos", r"(?:solenidade|festa) das cabanas",
  "a festa da colheita do outono: durante sete dias o povo morava em cabanas",
  "Lembrava os anos no deserto (Levítico 23:39-43).", s=("H5521",))
t("solenidade", r"solenidades?", "festa religiosa marcada pela Lei, com reunião do povo e sacrifícios",
  s=("H2282", "H4150", "H6116"))
t("lua nova", r"luas? novas?",
  "o primeiro dia de cada mês, que começava com a lua nova, marcado com festa e sacrifícios (Números 28:11)",
  s=("H2320", "G3561"))
t("pentecostes", r"pentecostes", "'quinquagésimo', em grego: a festa da colheita do trigo, cinquenta dias depois da Páscoa",
  "No Antigo Testamento, a Festa das Semanas (Deuteronômio 16:9-10). Em Atos 2, o dia em que o Espírito Santo "
  "foi derramado.", s=("G4005",))
t("jubileu", r"jubileus?",
  "o quinquagésimo ano, em que as terras voltavam às famílias e os israelitas escravizados eram libertados",
  "Ninguém podia perder para sempre a herança da família (Levítico 25).", s=("H3104",))
t("remissão", r"remissão",
  "perdão de uma dívida ou de uma culpa",
  "A cada sete anos, o 'ano da remissão' cancelava as dívidas entre israelitas (Deuteronômio 15:1-2).",
  s=("H8059", "H8058"), exige=True)

# ------------------------------------------------------------------ puro e impuro
t("imundo", r"imund\w*|impur\w*", "impuro, impedido de se aproximar do culto até ser purificado",
  "Na Lei, a impureza vinha de coisas como tocar num morto, certas doenças e certos animais; não é o mesmo que "
  "pecado (Levítico 11–15). No Novo Testamento a palavra também descreve a impureza moral.",
  s=("H2931", "H2930", "H2932", "G169", "G167"))
t("lepra", r"lepras?|lepros[oa]s?",
  "na Bíblia, nome de várias doenças de pele, não só da hanseníase de hoje",
  "Também havia 'lepra' em roupas e paredes, provavelmente mofo (Levítico 13–14). O doente ficava impuro e vivia "
  "fora do acampamento.", s=("H6883", "H6879", "G3014", "G3015"))
t("profano", r"profan[oa]s?", "comum, não consagrado; ou quem trata as coisas santas com desprezo",
  "Os sacerdotes deviam ensinar a diferença entre o santo e o profano (Levítico 10:10); Esaú é chamado profano "
  "(Hebreus 12:16).", s=("H2455", "H2491", "G952"))
t("anátema", r"anátemas?", "algo consagrado à destruição; no Novo Testamento, maldito, entregue ao juízo de Deus",
  "Paulo usa a palavra em Gálatas 1:8-9 e Romanos 9:3.", s=("H2764", "G331"))
t("abominação", r"abomina(?:ç(?:ão|ões)|ve(?:l|is))",
  "algo repugnante, detestável aos olhos de Deus", "Muitas vezes se refere à idolatria e às práticas ligadas a ela.",
  s=("H8441", "H8251", "H8263", "G946"))
t("circuncisão", r"circunc\w+",
  "o corte do prepúcio, feito no oitavo dia: o sinal da aliança de Deus com Abraão (Gênesis 17:10-12)",
  "No Novo Testamento, 'a circuncisão' também designa os judeus, e Paulo fala da 'circuncisão do coração' "
  "(Romanos 2:29).", s=("H4135", "G4061", "G4059"))
t("incircunciso", r"incircunc\w+",
  "não circuncidado: quem não pertence ao povo da aliança",
  "'Incircunciso de coração e de ouvidos' é quem se fecha para Deus (Jeremias 9:26; Atos 7:51).",
  s=("H6189", "H6190", "G203", "G564"))
t("prepúcio", r"prepúcios?", "a pele que cobre a ponta do pênis, cortada na circuncisão", s=("H6190", "G203"))

# ------------------------------------------------------------------ cargos e grupos
t("vidente", r"videntes?", "antigo nome do profeta",
  "1 Samuel 9:9 explica que o profeta, antes, era chamado de vidente.", s=("H7203", "H2374"))
t("anciãos", r"anciãos?", "os homens mais velhos; como grupo, os chefes que lideravam e julgavam o povo",
  "Na igreja, os presbíteros, que a pastoreiam (Atos 14:23; Tito 1:5).", s=("H2205", "G4245"))
t("escribas", r"escribas?",
  "no Novo Testamento, os mestres da Lei, que a copiavam, interpretavam e ensinavam",
  "No Antigo, também o secretário do rei (2 Samuel 8:17) e o estudioso da Lei, como Esdras (Esdras 7:6).",
  s=("H5608", "G1122"))
t("fariseus", r"fariseus?",
  "grupo judeu dedicado a cumprir à risca a Lei e as tradições dos antigos",
  "Muitos se opuseram a Jesus, que denunciou sua hipocrisia (Mateus 23). Paulo tinha sido fariseu "
  "(Filipenses 3:5).", s=("G5330",))
t("saduceus", r"saduceus?", "grupo judeu ligado aos sacerdotes e ao templo",
  "Não criam na ressurreição, nem em anjos ou espíritos (Atos 23:8).", s=("G4523",))
t("herodianos", r"herodianos", "judeus que apoiavam a dinastia de Herodes e, com ela, o domínio romano",
  "Uniram-se aos fariseus contra Jesus (Marcos 3:6; 12:13).", s=("G2265",))
t("zelote", r"zelotes?", "membro de um movimento judeu zeloso da Lei, contrário ao domínio romano",
  "Simão, um dos doze apóstolos, era chamado assim (Lucas 6:15).", s=("G2208", "G2581"))
t("rabi", r"rabi|rabôni", "'meu mestre': título de respeito dado aos mestres da Lei",
  "'Rabôni' é a forma mais afetuosa, usada por Maria Madalena (João 20:16).", s=("G4461", "G4462"))
t("sinagoga", r"sinagogas?", "casa de reunião dos judeus para a oração, a leitura e o ensino das Escrituras",
  "Jesus e Paulo ensinavam nelas, sobretudo aos sábados (Lucas 4:16; Atos 17:1-2).", s=("G4864",))
t("gentios", r"gentios?", "os povos não judeus (as 'nações')", s=("G1484", "H1471"))
t("prosélito", r"prosélitos?", "não judeu que se converteu ao judaísmo", s=("G4339",))
t("samaritanos", r"samaritan[oa]s?", "os habitantes de Samaria, de origem israelita misturada com povos trazidos pelos assírios",
  "Tinham seu próprio templo no monte Gerizim, e judeus e samaritanos se evitavam (2 Reis 17:24; João 4:9).",
  s=("G4541", "G4542"))
t("cobradores de impostos", r"cobrador(?:es)?(?: de impostos)?|publicanos?",
  "judeus que cobravam impostos para os romanos, muitas vezes cobrando a mais para si",
  "Eram vistos como traidores e postos junto com os 'pecadores' (Lucas 15:1). Mateus e Zaqueu tinham sido "
  "cobradores (Mateus 9:9; Lucas 19:2).", s=("G5057", "G5058", "G754"), exige=True)
t("centurião", r"centuri(?:ão|ões)", "oficial romano que comandava cerca de cem soldados", s=("G1543", "G2760"),
  exige=True)
t("centurião (chefe de cem)", r"centuri(?:ão|ões)", "comandante de cem soldados", s=("H3967",), exige=True,
  id="chefe-de-cem")
t("legião", r"legi(?:ão|ões)", "unidade do exército romano, com uns seis mil soldados; daí, 'um número enorme'",
  "Marcos 5:9; Mateus 26:53.", s=("G3003",))
t("pretório", r"pretório", "a residência do governador romano e o quartel da sua guarda",
  "Ali Jesus foi entregue aos soldados de Pilatos (Marcos 15:16).", s=("G4232",))
t("tetrarca", r"tetrarcas?", "governante de uma parte de um território",
  "Herodes Antipas, tetrarca da Galileia, mandou matar João Batista (Lucas 3:1; Mateus 14:1-10).", s=("G5076",))
t("procônsul", r"procônsul(?:es)?", "governador romano de uma província",
  "Como Sérgio Paulo, em Chipre, e Gálio, na Acaia (Atos 13:7; 18:12).", s=("G446", "G445"))
t("sátrapas", r"sátrapas?", "governadores das províncias do Império Persa (Ester; Daniel)", s=("H323",))
t("magos", r"magos?", "sábios da corte que interpretavam sonhos, estudavam os astros e praticavam adivinhação",
  "Os magos que visitaram Jesus eram estudiosos dos astros vindos do Oriente (Mateus 2:1).",
  s=("H2748", "G3097"))
t("concubina", r"concubinas?", "mulher que vivia com um homem como esposa de segunda categoria, sem os direitos da esposa",
  s=("H6370",))
t("eunuco", r"eunucos?", "homem castrado que servia na corte; a palavra passou a designar também um alto funcionário do rei",
  "Como o eunuco etíope que Filipe batizou (Atos 8:27).", s=("H5631", "G2135"))
t("copeiro", r"copeiros?", "o oficial que servia o vinho ao rei: cargo de confiança",
  "Neemias era copeiro do rei persa (Neemias 1:11).", s=("H4945",))
t("escudeiro", r"escudeiros?", "ajudante que carregava as armas de um guerreiro")
t("mordomo", r"mordomos?", "o administrador da casa, encarregado dos bens e dos servos de um senhor ou do rei")
t("atalaia", r"atalaias?", "sentinela, vigia posto no muro ou numa torre para avisar quem se aproximava",
  s=("H6822", "H5341"))
t("escabelo", r"escabelos?", "banquinho para descansar os pés",
  "Fazer dos inimigos o escabelo dos pés é vencê-los por completo (Salmo 110:1).", s=("H1916", "G5286"))

# ------------------------------------------------------------------ povos
t("filisteus", r"filiste(?:u|us|ia)",
  "povo do litoral sul de Canaã, com cinco cidades principais: Gaza, Asdode, Ascalom, Gate e Ecrom",
  "Foram os grandes inimigos de Israel no tempo dos juízes, de Saul e de Davi; Golias era filisteu.",
  s=("H6430",))
t("cananeus", r"canane(?:u|us|ia|ias)", "os povos que habitavam Canaã antes de Israel",
  "Às vezes o nome designa todos eles; às vezes, um povo entre outros (Gênesis 15:19-21).",
  s=("H3669", "G5478"), exige=True)
t("amorreus", r"amorreus?", "um dos povos de Canaã, que vivia nas montanhas e a leste do Jordão",
  "Seom e Ogue, vencidos por Israel antes de entrar na terra, eram reis amorreus (Números 21:21-35).",
  s=("H567",))
t("heteus", r"heteus?", "um dos povos de Canaã",
  "De um heteu Abraão comprou a caverna de Macpela (Gênesis 23); Urias, marido de Bate-Seba, era heteu.",
  s=("H2850", "H2845"))
t("heveus", r"heveus?", "um dos povos de Canaã; os gibeonitas eram heveus (Josué 9:7)", s=("H2340",))
t("jebuseus", r"jebuseus?", "o povo de Jebus, a cidade que Davi conquistou e que passou a se chamar Jerusalém",
  "2 Samuel 5:6-9.", s=("H2983",))
t("perizeus", r"perizeus?", "um dos povos que habitavam Canaã antes de Israel", s=("H6522",))
t("anaquins", r"anaquins|refains", "povos antigos de Canaã, famosos pela grande estatura",
  "Os espias de Moisés tiveram medo deles (Números 13:33; Deuteronômio 2:10-11).", s=("H6062", "H6061", "H7497"))
t("amalequitas", r"amalequitas?", "povo nômade do deserto do sul, descendente de Esaú (Gênesis 36:12)",
  "Atacou Israel logo depois da saída do Egito (Êxodo 17:8-16).", s=("H6003", "H6002"))
t("midianitas", r"midianitas?", "povo do deserto, descendente de Abraão e Quetura (Gênesis 25:2)",
  "Moisés casou com uma midianita; no tempo de Gideão eles oprimiram Israel (Êxodo 2:16-21; Juízes 6).",
  s=("H4084", "H4080"))
t("moabitas", r"moabitas?", "povo a leste do mar Morto, descendente de Ló (Gênesis 19:37)",
  "Rute era moabita.", s=("H4125", "H4124"))
t("amonitas", r"amonitas?", "povo a leste do Jordão, descendente de Ló (Gênesis 19:38)",
  "Sua capital era Rabá, onde hoje fica Amã, na Jordânia.", s=("H5984", "H5983"))
t("edomitas", r"edomitas?", "os descendentes de Esaú (Edom), ao sul do mar Morto",
  "Povo aparentado de Israel e muitas vezes inimigo dele (Obadias).", s=("H130", "H123"))
t("caldeus", r"caldeus?", "povo do sul da Mesopotâmia que dominou a Babilônia; Nabucodonosor era caldeu",
  "Em Daniel, 'caldeus' também designa a classe dos sábios e astrólogos da corte (Daniel 2:2).",
  s=("H3778", "H3779"))
t("assírios", r"assírios?", "o povo do grande império da Mesopotâmia, com capital em Nínive",
  "Destruíram o reino do norte, Israel, e deportaram seu povo (2 Reis 17).", s=("H804",))

# ------------------------------------------------------------------ culto aos ídolos
t("bosque", r"bosques?", "poste ou árvore sagrada da deusa cananeia Aserá",
  "Onde o original diz aserá, a Bíblia Livre traduz 'bosque'. Israel devia derrubá-los (Deuteronômio 7:5).",
  s=("H842",), exige=True, id="bosque-asera")
t("lugares altos", r"lugar(?:es)? altos?|altos",
  "santuários no alto de colinas, com altar, muitas vezes dedicados a ídolos",
  "Mesmo reis fiéis deixaram de destruí-los, até que Ezequias e Josias os derrubaram (1 Reis 15:14; 2 Reis "
  "18:4; 23:8).",
  s=("H1116",), exige=True)
t("baalins", r"baalins", "plural de Baal: as imagens e os cultos do deus cananeu Baal", s=("H1168",))

# ------------------------------------------------------------------ objetos, campo e casa
t("eira", r"eiras?", "terreiro duro e plano onde se debulhava e separava o grão da palha",
  "Rute encontrou Boaz numa eira (Rute 3); numa eira comprada por Davi foi construído o templo (2 Crônicas 3:1).",
  s=("H1637", "G257"))
t("debulhar", r"debulh\w+", "separar os grãos da espiga, batendo ou pisando na eira", s=("H1758", "G248"))
t("lagar", r"lagar(?:es)?", "tanque escavado na pedra onde se pisavam as uvas para fazer vinho",
  "Pisar as uvas no lagar é imagem do juízo de Deus (Isaías 63:3; Apocalipse 14:19-20).", s=("H3342", "H1660", "G3025", "G5276"))
t("odre", r"odres?", "saco de couro, geralmente de cabra, para guardar vinho, água ou leite",
  "Vinho novo, ainda fermentando, rompia os odres velhos (Mateus 9:17).", s=("H4997", "H2573", "G779"))
t("cântaro", r"cântaros?", "jarro grande de barro, usado para buscar água", s=("H3537", "G5201"))
t("botija", r"botijas?", "jarro pequeno de barro, para azeite ou água")
t("alforje", r"alforjes?", "bolsa de viagem para levar comida")
t("alabastro", r"alabastros?", "pedra clara e macia de que se faziam frascos de perfume (Marcos 14:3)", s=("G211",))
t("jugo", r"jugos?", "peça de madeira posta sobre o pescoço de dois bois para puxarem juntos",
  "Figurado: domínio, servidão; mas também o ensino que se aceita seguir: Jesus convida a tomar o seu jugo "
  "(Mateus 11:29-30).", s=("H5923", "H4133", "G2218"))
t("aguilhão", r"aguilh(?:ão|ões)", "vara pontuda para tocar os bois; também o ferrão",
  "Resistir a Deus é como o boi que dá coice contra o aguilhão (Atos 26:14). Paulo fala do aguilhão, o ferrão, "
  "da morte (1 Coríntios 15:55-56).", s=("G2759",))
t("prumo", r"prumos?", "fio com um peso na ponta, para ver se uma parede está reta",
  "Em Amós 7:7-8, imagem de Deus examinando o seu povo.", s=("H594", "H4949"))
t("cisterna", r"cisternas?", "reservatório escavado na rocha para guardar água da chuva",
  "Vazia, servia de prisão: José e Jeremias foram jogados numa (Gênesis 37:24; Jeremias 38:6).", s=("H953",))
t("masmorra", r"masmorras?", "cisterna ou cova usada como prisão", s=("H953",))
t("manancial", r"mananciais|manancial", "nascente, fonte de água", s=("H4726",))
t("ribeiro", r"ribeiros?", "riacho; muitas vezes um vale que só tem água na estação das chuvas",
  s=("H5158",))
t("vau", r"vaus?", "trecho raso de um rio, por onde se atravessa a pé", s=("H4569", "H5679"))
t("cidades de refúgio", r"cidades? de refúgio",
  "seis cidades onde quem matava alguém sem querer podia se abrigar até ser julgado",
  "Ali ficava protegido do 'vingador do sangue' (Números 35:9-15).", s=("H4733",))
t("tenazes", r"tenazes", "pinça para pegar brasas", s=("H4457",))
t("grilhões", r"grilhões", "correntes de ferro presas aos pés de um preso", s=("G3976",))
t("vaso", r"vasos?", "qualquer recipiente ou utensílio",
  "Os 'vasos' do templo são todos os objetos do culto. A palavra também descreve a pessoa como instrumento nas "
  "mãos de Deus (Atos 9:15; 2 Timóteo 2:21).", s=("H3627", "G4632"))

# ------------------------------------------------------------------ roupas
t("túnica", r"túnicas?", "roupa comprida usada por baixo do manto", s=("H3801", "G5509"))
t("franjas", r"franjas?", "borlas presas às pontas do manto, para lembrar os mandamentos (Números 15:38-39)",
  s=("H6734", "G2899"))
t("filactérios", r"filactérios?",
  "caixinhas de couro com trechos da Lei, amarradas na testa e no braço na hora da oração",
  "Jesus criticou quem as usava grandes para se exibir (Mateus 23:5).", s=("G5440",))
t("pano de saco", r"(?:roupas?|vestidos?|vestes?|panos?) de sacos?|de sacos?",
  "tecido grosseiro de pelo de cabra, vestido em sinal de luto ou de arrependimento",
  "Os ninivitas se vestiram de saco quando ouviram Jonas (Jonas 3:5).", s=("H8242", "G4526"), exige=True)

# ------------------------------------------------------------------ guerra
t("despojo", r"despojos?", "os bens tomados do inimigo vencido: gado, roupas, armas, objetos de valor",
  s=("H7998", "H957"))
t("aljava", r"aljavas?", "estojo onde se levam as flechas", s=("H827", "H8522"))
t("couraça", r"couraças?", "armadura que protege o peito",
  "'A couraça da justiça' (Efésios 6:14).", s=("H8302", "G2382"))
t("pavês", r"pav(?:ês|eses)", "escudo grande, que cobria o corpo inteiro", s=("H6793",))
t("aríete", r"aríetes?", "tronco pesado, às vezes com ponta de ferro, para derrubar portões e muros",
  s=("H3733",))
t("baluarte", r"baluartes?", "fortificação, muralha de defesa; figurado, proteção")
t("funda", r"fundas?", "arma de arremesso: uma tira de couro com que se atiravam pedras",
  "Foi a arma de Davi contra Golias (1 Samuel 17:49-50).", s=("H7050",), exige=True)

# ------------------------------------------------------------------ música e salmos
t("selá", r"selá", "palavra de sentido incerto que aparece nos Salmos e em Habacuque",
  "Provavelmente uma indicação musical: uma pausa ou um interlúdio.", s=("H5542",), exige=True)
t("regente", r"regente", "o mestre de música, que dirigia o canto do templo",
  "Aparece nos títulos dos Salmos ('para o regente').", s=("H5329",))
t(None, r"mictão|gitite|alamote|seminite|masquil|sigaiom",
  "termo dos títulos dos Salmos, ligado ao tipo de poema ou à forma de cantar", "O sentido exato se perdeu.",
  id="titulo-de-salmo")
t("aleluia", r"aleluias?", "'louvai a Yah': louvai ao SENHOR, em hebraico", s=("H1984", "H3050", "G239"))
t("hosana", r"hosanas?", "'salva, por favor!', em hebraico (Salmo 118:25)",
  "Virou grito de aclamação ao Messias na entrada de Jesus em Jerusalém (Mateus 21:9).", s=("G5614",))
t("corbã", r"corbã", "'oferta', em hebraico: bem dedicado a Deus",
  "Jesus condena quem usava esse voto para deixar de sustentar os pais (Marcos 7:11).", s=("G2878",))
t("saltério", r"saltérios?", "instrumento de cordas, parecido com a harpa", s=("H5035", "H6460"))
t("címbalo", r"címbalos?", "par de pratos de metal que se batem um no outro", s=("H4700", "H6767", "G2950"))
t("tamborim", r"tamborins?|tamborim|tamboris|adufes?", "pandeiro: aro de madeira com couro esticado, tocado com a mão",
  "Miriã o tocou depois da travessia do mar (Êxodo 15:20).", s=("H8596",))

# ------------------------------------------------------------------ natureza
t("maná", r"maná", "o alimento que Deus deu a Israel durante os quarenta anos no deserto",
  "O nome soa como a pergunta 'o que é isto?' (Êxodo 16:15). Jesus se apresenta como o verdadeiro pão do céu "
  "(João 6:31-35).", s=("H4478", "G3131"))
t("codorniz", r"codorni(?:z|zes)", "ave pequena, a codorna",
  "Deus a enviou em bando para alimentar Israel no deserto (Êxodo 16:13; Números 11:31).", s=("H7958",))
t("cervo", r"corç[ao]s?|cerv(?:o|os|a|as)", "o veado; corça e cerva são a fêmea",
  "Símbolo de agilidade e de graça (Salmo 18:33; Cantares 2:9).")
t("velo", r"velo", "a lã de um carneiro, inteira, como sai na tosquia",
  "O sinal que Gideão pediu a Deus (Juízes 6:36-40).", s=("H1492",))
t("hissopo", r"hissopo", "planta pequena e aromática, cujos ramos serviam para aspergir",
  "Com ele se passou o sangue nos umbrais na Páscoa (Êxodo 12:22), e Davi pede para ser purificado com "
  "hissopo (Salmo 51:7).", s=("H231", "G5301"))
t("mirra", r"mirras?", "resina aromática e cara, usada em perfumes, unções e no preparo de corpos para o sepultamento",
  "Foi um dos presentes dos magos (Mateus 2:11).", s=("H4753", "G4666"))
t("nardo", r"nardos?", "perfume caríssimo, feito da raiz de uma planta do Himalaia",
  "Maria ungiu Jesus com nardo puro (João 12:3).", s=("H5373", "G3487"))
t("aloés", r"aloés", "madeira ou resina aromática usada em perfumes",
  "Usado com a mirra para preparar o corpo de Jesus (João 19:39).", s=("H174", "G250"))
t("bálsamo", r"bálsamos?", "resina perfumada e medicinal",
  "O 'bálsamo de Gileade' era famoso (Jeremias 8:22).", s=("H6875",))
t("acácia", r"acácias?", "árvore resistente do deserto, de madeira dura e leve",
  "A arca e o tabernáculo foram feitos com ela (Êxodo 25:10).", s=("H7848",))
t("sicômoro", r"sicômoros?", "figueira grande, de figos pequenos e baratos",
  "Zaqueu subiu num para ver Jesus (Lucas 19:4).", s=("H8256", "G4809"))
t("mandrágora", r"mandrágoras?", "planta de raiz grossa e frutos perfumados, que se acreditava favorecer a fertilidade",
  "Gênesis 30:14-16.", s=("H1736",))
t("absinto", r"absintos?", "erva de gosto muito amargo; figurado, amargura e sofrimento",
  "No Apocalipse, nome da estrela que amargou as águas (Apocalipse 8:11).", s=("H3939", "G894"))
t("fel", r"fel", "a bílis, líquido muito amargo; figurado, amargura",
  "Na cruz, deram a Jesus vinho misturado com fel (Mateus 27:34).", s=("H7219", "H4846", "G5521"))
t("joio", r"joio", "erva daninha que, enquanto cresce, se parece com o trigo",
  "Só dá para distinguir quando espiga; daí a parábola de Mateus 13:24-30.", s=("G2215",))
t("abrolhos", r"abrolhos?", "plantas rasteiras cheias de espinhos",
  "'Espinhos e abrolhos' são sinal da terra amaldiçoada (Gênesis 3:18).", s=("H1863", "G5146"))
t("sarmento", r"sarmentos?", "ramo novo da videira", s=("H1612", "H2156"))
t(None, r"ônix|jaspes?|safiras?|sárdi[oa]s?|sardônicas?|topázios?|berilos?|ametistas?|ágatas?|crisólitos?|"
        r"carbúnculos?|esmeraldas?|calcedônias?|jacintos?|crisoprásios?|rubis?|rubi",
  "pedra preciosa",
  "Os nomes antigos das pedras nem sempre correspondem aos de hoje, e a identificação exata de muitas é incerta. "
  "Doze delas estavam no peitoral do sumo sacerdote (Êxodo 28:17-20) e doze nos alicerces da nova Jerusalém "
  "(Apocalipse 21:19-20).", id="pedra-preciosa")

# ------------------------------------------------------------------ corpo e pessoas
t("lombos", r"lombos?", "a região da cintura e dos quadris",
  "'Cingir os lombos' é prender a roupa longa na cintura para ter liberdade de movimento: preparar-se para "
  "trabalhar, lutar ou partir (1 Reis 18:46; Lucas 12:35). 'Sair dos lombos' de alguém é ser seu descendente.",
  s=("H4975", "H2504", "G3751"))
t("cingir", r"cing\w+|cinj\w+", "prender em volta da cintura (cinto, espada, roupa); envolver, cercar",
  "'Cingir-se' é preparar-se para agir; ver 'lombos'.", s=("H2296", "G4024", "G2224"))
t("cerviz", r"cerviz", "a nuca, a parte de trás do pescoço",
  "'Povo de dura cerviz' é o povo teimoso, que não se curva, como o boi que não aceita o jugo (Êxodo 32:9; "
  "Atos 7:51).", s=("H6203", "G4644"))
t("rins", r"rins", "os rins",
  "No sacrifício, eram queimados no altar com a gordura (Levítico 3:4). Em sentido figurado, o íntimo da pessoa, "
  "seus sentimentos e intenções: Deus examina o coração e os rins (Jeremias 17:10; Apocalipse 2:23).",
  s=("H3629", "G3510"))
t("entranhas", r"entranhas", "as vísceras, o ventre; figurado, o centro dos sentimentos, sobretudo a compaixão",
  "Em grego, a mesma palavra (splanchna) designa as entranhas e a compaixão (Filipenses 2:1; Colossenses 3:12).", s=("H4578", "H7356", "G4698"))
t("cãs", r"cãs", "cabelos brancos; figurado, a velhice",
  "Provérbios 16:31 as chama de coroa de honra.", s=("H7872",))
t("varão", r"var(?:ão|ões)", "homem, sobretudo o homem adulto e de valor", s=("H376", "H1397", "G435"))
t("primogenitura", r"primogenituras?", "os direitos do filho mais velho: a porção dobrada da herança e a liderança da família",
  "Esaú a vendeu por um prato de comida (Gênesis 25:29-34; Hebreus 12:16).", s=("H1062", "G4415"))
t("remanescente", r"remanescentes?", "o que restou",
  "Nos profetas, a parte fiel do povo que Deus preserva depois do juízo (Isaías 10:20-22; Romanos 11:5).",
  s=("H7611", "H7605", "H6413", "G2640", "G3005"))

# ------------------------------------------------------------------ palavras antigas ou literárias
t("porquanto", r"porquanto", "porque, visto que")
t("porventura", r"porventura", "por acaso; talvez")
t("derredor", r"(?:ao |em )?derredor", "ao redor, em volta")
t("dalém", r"dalém", "do outro lado de (um rio, um mar)",
  "'Dalém do Jordão' costuma indicar a região a leste do rio.")
t("acepção de pessoas", r"acepç(?:ão|ões)(?: de pessoas)?",
  "favoritismo: tratar alguém melhor por causa da aparência, da posição ou do dinheiro",
  "Deus não faz acepção de pessoas, e a igreja também não deve fazer (Atos 10:34; Tiago 2:1-4).", s=("G4382", "G4380", "G4381"))
t("mácula", r"máculas?", "mancha, defeito",
  "O animal oferecido devia ser 'sem mácula' (Levítico 22:20); Cristo é o cordeiro sem defeito (1 Pedro 1:19).",
  s=("H3971", "H8549", "G299"))
t("vereda", r"veredas?", "caminho estreito, trilha; figurado, o modo de viver", s=("H5410", "H734", "H4570", "G5147"))
t("escárnio", r"escárnios?", "zombaria, desprezo", s=("H7814", "H7047", "H8322"))
t("tropeço", r"tropeços?", "o que faz alguém tropeçar e cair: na Bíblia, cair em pecado ou abandonar a fé",
  "'Pedra de tropeço' (Isaías 8:14; Romanos 9:33).", s=("H4383", "G4348", "G4625"))
t("escândalo", r"escândalos?",
  "armadilha, tropeço: o que leva alguém a pecar ou a perder a fé",
  "Não é o sentido de hoje, de 'notícia vergonhosa' (Mateus 18:7; 1 Coríntios 1:23).", s=("G4625", "G4624"))
t("quebrantar", r"quebrant\w+", "quebrar, abater",
  "'Quebrantado' é o abatido, humilhado; 'quebrantamento', ruína ou destruição.", s=("H7665", "H7667", "H1792"))
t("assolação", r"assol\w+", "devastação, ruína completa; 'assolar' é devastar", s=("H8077", "H8074", "H7701"))
t("pestilência", r"pestilências?", "epidemia, doença que se espalha e mata muitos", s=("H1698", "G3061"))
t("mortandade", r"mortandades?", "matança em grande número, ou morte de muitos por uma praga",
  s=("H4046", "H5062", "H4194"))
t("concerto", r"concertos?", "aliança, pacto: sentido antigo da palavra, sem relação com música", s=("H1285",))
t("sortes", r"sortes", "lançar sortes: sortear com pedras ou varetas marcadas, deixando a decisão com Deus",
  "Quem lança a sorte é o homem, mas a decisão vem do SENHOR (Provérbios 16:33). Assim a terra foi repartida "
  "(Josué 18) e Matias foi escolhido apóstolo (Atos 1:26).", s=("H1486", "G2819"))
t("carnal", r"carna(?:l|is)", "guiado pela natureza humana, e não pelo Espírito de Deus",
  "1 Coríntios 3:1-3; Romanos 8:5-8.", s=("G4559", "G4560"), exige=True)
t("incorrupção", r"incorrup\w+|incorruptíve(?:l|is)", "o que não se corrompe nem se estraga",
  "Em 1 Coríntios 15:42-54, é o corpo da ressurreição, que não morre mais.", s=("G861", "G862", "G90"))
t("anticristo", r"anticristos?", "quem se opõe a Cristo e se põe no lugar dele",
  "1 João 2:18-22; 4:3.", s=("G500",))
