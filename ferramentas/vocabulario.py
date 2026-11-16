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
cobrem o mesmo trecho, vale a que vem antes ("mar de fundição" antes de "fundição"). Fora isso, duas entradas sem
exige não devem casar a mesma forma: a segunda sublinharia a mesma palavra de novo, mais adiante no capítulo.
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
t("pães da proposição", r"(?:pães|pão|mesa) da proposição",
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
t("profano", r"profan\w*", "comum, não consagrado; 'profanar' é tratar como comum o que é santo, desonrá-lo",
  "Os sacerdotes deviam ensinar a diferença entre o santo e o profano (Levítico 10:10); Esaú é chamado profano "
  "(Hebreus 12:16).", s=("H2455", "H2491", "G952", "H2490", "G953"))
t("anátema", r"anátemas?", "algo consagrado à destruição; no Novo Testamento, maldito, entregue ao juízo de Deus",
  "Paulo usa a palavra em Gálatas 1:8-9 e Romanos 9:3.", s=("H2764", "G331"))
t("abominação", r"abomin\w+",
  "algo repugnante, detestável aos olhos de Deus ('abominar' é detestar)",
  "Muitas vezes se refere à idolatria e às práticas ligadas a ela.",
  s=("H8441", "H8251", "H8263", "G946", "H8581", "H8262", "G948", "G947"))
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
t("heteus", r"heteus?|(?<=filhos de )hete|(?<=filhas de )hete", "um dos povos de Canaã",
  "De um heteu Abraão comprou a caverna de Macpela (Gênesis 23); Urias, marido de Bate-Seba, era heteu.",
  s=("H2850", "H2845"))
t("heveus", r"heveus?", "um dos povos de Canaã; os gibeonitas eram heveus (Josué 9:7)", s=("H2340",))
t("jebuseus", r"jebuseus?", "o povo de Jebus, a cidade que Davi conquistou e que passou a se chamar Jerusalém",
  "2 Samuel 5:6-9.", s=("H2983",))
t("perizeus", r"perizeus?|ferezeus?", "um dos povos que habitavam Canaã antes de Israel", s=("H6522",))
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
t("vau", r"vaus?(?!:)", "trecho raso de um rio, por onde se atravessa a pé", s=("H4569", "H5679"))
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
t("despojo", r"despoj\w+", "os bens tomados do inimigo vencido: gado, roupas, armas, objetos de valor; 'despojar' é "
  "tomar esses bens, saquear",
  "Em sentido figurado, 'despojar-se' é tirar de si, como quem tira uma roupa: Paulo fala em despojar-se do velho "
  "homem (Colossenses 3:9).", s=("H7998", "H957", "H7997", "G554", "G1562"))
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
t(None, r"mictão|gitite|alamote|seminite|masquil|sigaiom|altachete|susanedute|mute-laben|(?<=“)maalate(?: leanote)?|"
        r"siguionote|higaiom",
  "termo dos títulos dos Salmos, ligado ao tipo de poema ou à forma de cantar", "O sentido exato se perdeu.",
  id="titulo-de-salmo")
t("aleluia", r"aleluias?", "'louvai a Yah': louvai ao SENHOR, em hebraico", s=("H1984", "H3050", "G239"))
t("hosana", r"hosanas?", "'salva, por favor!', em hebraico (Salmo 118:25)",
  "Virou grito de aclamação ao Messias na entrada de Jesus em Jerusalém (Mateus 21:9).", s=("G5614",))
t("corbã", r"corbã", "'oferta', em hebraico: bem dedicado a Deus",
  "Jesus condena quem usava esse voto para deixar de sustentar os pais (Marcos 7:11).", s=("G2878",))
t("saltério", r"saltérios?", "instrumento de cordas, parecido com a harpa", s=("H5035", "H6460"))
t("címbalo", r"címbalos?", "par de pratos de metal que se batem um no outro", s=("H4700", "H6767", "G2950"))
t("tamborim", r"tamborins?|tamborim|tamboris|tamboril|adufes?", "pandeiro: aro de madeira com couro esticado, tocado com a mão",
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
  "A terra que só produz espinhos e abrolhos é imagem de quem rejeita a graça recebida (Hebreus 6:7-8).", s=("H1863", "G5146"))
t("sarmento", r"sarmentos?", "ramo novo da videira", s=("H1612", "H2156"))
t(None, r"ônix|jaspes?|safiras?|sárdi[oa]s?|sardônicas?|topázios?|berilos?|ametistas?|ágatas?|crisólitos?|"
        r"carbúnculos?|esmeraldas?|calcedônias?|jacintos?|crisoprásios?|rubis?|rubi|turquesas?",
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
t("escândalo", r"escândalos?|escandaliz\w+",
  "armadilha, tropeço: o que leva alguém a pecar ou a perder a fé ('escandalizar' é fazer tropeçar)",
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

# ------------------------------------------------------------------ verbos e expressões da Bíblia
t("edificar", r"(?:re)?edific\w+|(?:re)?edifiqu\w+", "construir; 'reedificar' é reconstruir",
  "No Novo Testamento, também fortalecer a fé e a vida de alguém: o amor edifica (1 Coríntios 8:1; 14:12).", s=("H1129", "G3618", "G3619"))
t("clamar", r"clam\w*", "gritar, chamar em voz alta; sobretudo pedir socorro a Deus ('clamor' é esse grito)",
  "Deus ouviu o clamor do seu povo no Egito (Êxodo 3:7) e ouve quem clama a ele (Salmo 34:6).", s=("H2199", "H2201", "H6817", "H6818", "G2896", "H7768", "H7775", "H7121"))
t("perecer", r"perec\w+|pereç\w+", "morrer, ser destruído, acabar",
  "Em João 3:16 é o contrário da vida eterna: perder-se para sempre.", s=("H6", "G622"))
t("profetizar", r"profetiz\w+", "falar em nome de Deus, anunciando a sua palavra",
  "Nem sempre é prever o futuro: o profeta também denuncia o pecado, consola e chama ao arrependimento "
  "(1 Coríntios 14:3).", s=("H5012", "G4395"))
t("ajuntar", r"ajunt\w+", "juntar, reunir. 'Ajuntamento' é a reunião, a multidão; nas leis de Levítico e "
  "Números, também a relação sexual",
  "'Ser ajuntado ao seu povo' é morrer e ir para junto dos antepassados (Gênesis 25:8; 49:33).", s=("H622", "H6908", "G4863"))
t("inclinar", r"inclin\w+", "curvar, dobrar",
  "'Inclinar o ouvido' é prestar atenção, escutar com cuidado; 'inclinar o coração' é voltar a vontade para algo.", s=("H5186", "H7812"))
t("afligir", r"aflig\w+|aflij\w+|aflit[oa]s?", "fazer sofrer, oprimir; 'aflito' é quem sofre, angustiado",
  "No Dia da Expiação, 'afligir a alma' era jejuar e humilhar-se diante de Deus (Levítico 16:29).", s=("H6031", "H6041", "G2346"))
t("achegar-se", r"acheg\w+|achegu\w+", "aproximar-se, chegar perto",
  "Na Lei, 'achegar-se' ao altar é aproximar-se para servir ou para oferecer (Levítico 21:17-21).", s=("H7126", "H5066", "H1692"))
t("engrandecer", r"engrandec\w+|engrandeç\w+", "tornar grande; exaltar, proclamar a grandeza de alguém",
  "'Engrandecer-se' também pode ser encher-se de orgulho.", s=("H1431", "G3170"))
t("degolar", r"degol\w+", "cortar o pescoço; nos sacrifícios, abater o animal",
  "O animal era degolado para que o sangue escorresse e fosse levado ao altar (Levítico 1:5).", s=("H7819", "H2873"))
t("fartar", r"fart(?!ura)\w*", "saciar, encher de comida; 'farto' é satisfeito", s=("H7646", "G5526"))
t("blasfemar", r"blasf[eê]m\w+", "falar contra Deus com desprezo, insultá-lo ('blasfêmia' é esse insulto)",
  "A Lei punia com a morte quem blasfemava o nome do SENHOR (Levítico 24:16). Jesus foi acusado de blasfêmia por "
  "se dizer o Filho de Deus (Marcos 14:61-64).", s=("G987", "G988", "G989", "H1442", "H5006", "H5344"))
t("transgredir", r"transgred\w+|transgrid\w+", "desobedecer, passar por cima de uma ordem ou de uma lei", s=("H6586", "H4603", "H5674", "G3845"))
t("pranto", r"prant\w+", "choro alto e sentido, sobretudo pelos mortos; 'prantear' é chorar a morte de alguém",
  "O luto durava dias, com lamentos e roupas de saco (Gênesis 50:10).", s=("H4553", "H5594", "H60", "H56", "H5092", "G2805", "G3997"))
t("desolação", r"desol\w+", "devastação, ruína; um lugar desolado fica vazio e abandonado",
  "A 'abominação da desolação' (Daniel 9:27; Mateus 24:15) é o sacrilégio que profana o lugar santo e anuncia a "
  "sua destruição.", s=("H8077", "H8047", "H8074", "G2050"))
t("desamparar", r"desampar\w+", "abandonar, deixar sem ajuda",
  "No Salmo 22:1, que Jesus repetiu na cruz, o justo pergunta por que Deus o desamparou (Mateus 27:46).", s=("H5800", "G1459", "H5203"))
t("ceifar", r"ceif\w+", "colher o cereal maduro, cortando-o com a foice; 'ceifa' é a colheita",
  "Jesus compara o fim dos tempos a uma colheita (Mateus 13:30, 39; Apocalipse 14:15).", s=("H7114", "H7105", "G2325", "G2326", "G2327"))
t("súplica", r"súplicas?|supli(?:c|qu)\w+", "pedido humilde e insistente; 'suplicar' é pedir assim", s=("H8467", "H8469", "G1162", "H2603"))
t("arrebatar", r"arrebat\w+", "tomar à força ou de repente, levar embora",
  "Elias foi arrebatado ao céu (2 Reis 2:11), e os que estiverem vivos na volta de Cristo serão arrebatados para "
  "encontrá-lo (1 Tessalonicenses 4:17).", s=("G726", "H2963", "H2966", "H1497"))
t("bendizer", r"bendiz\w*|bendig\w+|bendiss\w+", "falar bem de; louvar, agradecer",
  "Quando Deus bendiz, abençoa; quando o homem bendiz a Deus, louva-o e agradece (Salmo 103:1-2).", s=("H1288", "G2127"))
t("exortar", r"exort\w+", "aconselhar com insistência, animar a fazer o bem ('exortação' é esse conselho)", s=("G3870", "G3874"))
t("murmurar", r"murmur\w+", "queixar-se, reclamar baixinho e com revolta",
  "Israel murmurou contra Deus e contra Moisés no deserto (Êxodo 16:2-8; 1 Coríntios 10:10).", s=("H3885", "H8519", "H7279", "G1111", "G1112"))
t("prostituir-se", r"prostitu(?!tas?(?!\w))\w+", "entregar-se à prostituição; nos profetas, imagem da idolatria",
  "Israel, a esposa do SENHOR, 'se prostituía' quando ia atrás de outros deuses (Oseias 1–3; Ezequiel 16).", s=("H2181", "H8457", "H2184", "H2183", "G4203", "G4202"))
t("escarnecer", r"escarnec\w+|escarneç\w+", "zombar, ridicularizar ('escarnecedor' é quem zomba)",
  "Em Provérbios, o escarnecedor é quem despreza a correção e zomba do que é santo (Provérbios 9:7-8; Salmo 1:1).", s=("H3887", "H3932", "H3933", "H7046", "G1702"))
t("peregrino", r"peregrin\w+", "quem mora como estrangeiro, sem terra própria; 'peregrinar' é viver assim, ou viajar",
  "Os patriarcas viveram como peregrinos em Canaã, e os cristãos também são peregrinos neste mundo (Hebreus "
  "11:13; 1 Pedro 2:11).", s=("H1481", "H1616", "H4033", "H8453", "G3927", "G3941", "G3940"))
t("restituir", r"restitu\w+", "devolver, pagar de volta o que foi tirado",
  "A Lei mandava restituir o que foi roubado, com acréscimo (Êxodo 22:1-4); Zaqueu prometeu devolver quatro "
  "vezes mais (Lucas 19:8).", s=("H7999",))
t("atemorizar", r"atemoriz\w+", "assustar, encher de medo", s=("H2865", "H6206", "G1719"))
t("bramido", r"bram\w+", "rugido forte (do leão, do mar, de uma multidão); 'bramar' é rugir", s=("H7580", "H7581", "H1993", "H5098"))
t("açoite", r"açoit\w+", "chicote, ou cada golpe dado com ele; 'açoitar' é chicotear",
  "A Lei limitava o castigo a quarenta golpes (Deuteronômio 25:3; 2 Coríntios 11:24). Jesus foi açoitado antes "
  "de ser crucificado (João 19:1).", s=("H7752", "G3146", "G3148", "G5417", "G1194"))
t("fender", r"fend\w+", "rachar, abrir ao meio ('fenda' é a rachadura)",
  "Os animais puros tinham a unha fendida, dividida em duas (Levítico 11:3).", s=("H1234", "H8156", "H8157", "H6536"))
t("jazer", r"(?-i:jaz(?:er|ia|iam|ias|em|es|e|erá|erás|erão|ido|endo)?)",
  "estar deitado, estendido; dito também de quem está morto ou sepultado", s=("H7901", "G2749", "G2621"))
t("rapar", r"rap(?:ar|ou|aram|ará|arão|arás|e|es|em|ado|ada|ados|adas|ando|a|am|ei|areis|ai)",
  "raspar (o cabelo, a barba), cortar rente",
  "Rapar a cabeça era sinal de luto e de humilhação, e também fazia parte da purificação (Jó 1:20; Números 6:18).", s=("H1548", "H7139", "G3587"))
t("aquietar", r"aquiet\w+", "acalmar, sossegar", s=("H8252", "H8367", "H1826", "G2869"))
t("assoviar", r"assovi\w+", "dar um assobio",
  "Nos profetas, quem passa pelas ruínas de um povo castigado assovia de espanto e de zombaria (Jeremias 19:8); "
  "e Deus 'assovia' para chamar as nações (Isaías 5:26).", s=("H8319", "H8322"))
t("vivificar", r"vivific\w+|vivifiqu\w+", "dar vida, fazer viver", s=("G2227", "H2421"))
t("apalpar", r"apalp\w+", "tocar com as mãos, tatear",
  "Isaque apalpou Jacó achando que era Esaú (Gênesis 27:21-22).", s=("H4959", "H4184", "G5584"))
t("tragar", r"trag(?:ar|ou|aram|ará|arão|ado|ada|ados|adas|ando|ue|uem)", "engolir de uma vez, devorar",
  "A terra tragou Corá e os seus (Números 16:32). Na ressurreição, a morte será tragada pela vitória "
  "(1 Coríntios 15:54).", s=("H1104", "G2666"))
t("destilar", r"destil\w+(?! leite e mel)", "gotejar, escorrer gota a gota",
  "Os montes que 'destilam mosto' são imagem da fartura que Deus dará (Joel 3:18; Amós 9:13).", s=("H5197", "H5140", "H6201", "H7491"))
t("cobiçar", r"cobiç\w+|cobic\w+", "desejar com avidez, sobretudo o que pertence a outro ('cobiça' é esse desejo)",
  "'Não cobiçarás' é o décimo mandamento (Êxodo 20:17): o pecado começa no desejo do coração (Romanos 7:7).", s=("H2530", "H2531", "H183", "G1937", "G1939"))
t("suscitar", r"suscit\w+", "fazer surgir, levantar alguém para uma missão",
  "Deus 'suscitava' juízes e profetas para o seu povo (Juízes 2:16; Deuteronômio 18:15). Suscitar descendência "
  "ao irmão morto era a lei do levirato (Deuteronômio 25:5-6).", s=("H5782", "H6965", "H2992", "G1453", "G1825"))
t("transtornar", r"transtorn\w+", "virar de cabeça para baixo, derrubar; lançar em confusão",
  "Na Bíblia o sentido é bem mais forte que hoje: Deus 'transtorna' montanhas e exércitos (Jó 9:5; "
  "Êxodo 14:25).", s=("H2015", "H5557", "H2040"))
t("definhar", r"definh\w+", "ir perdendo as forças aos poucos, enfraquecer", s=("H535", "H7710", "G3584"))
t("untar", r"unt(?:ar|ou|aram|ará|arás|ado|ada|ados|adas|ai|a|am|e|es)", "passar azeite ou gordura em algo", s=("H4886", "H1878", "G2025"))
t("ruminar", r"rumin\w+", "mastigar de novo o alimento que volta do estômago, como fazem os bois",
  "Pela Lei, só eram puros os animais que ruminavam e tinham a unha fendida (Levítico 11:3).", s=("H1625",))
t("jubilar", r"jubil(?!eu)\w+|júbilos?", "alegrar-se muito, festejar com gritos de alegria ('júbilo' é essa alegria)", s=("H1523", "H7442", "H8643", "H5970", "H5937", "H8057", "G21"))
t("desposar", r"despos\w+", "tomar como esposa ('desposada' é a noiva já prometida)",
  "O noivado já ligava os noivos por compromisso legal, antes de morarem juntos; assim estavam Maria e José "
  "(Deuteronômio 22:23; Mateus 1:18).", s=("H781", "G3423"))
t("rebocar", r"reboc\w+|reboqu\w+", "cobrir uma parede com massa, o reboco (e não puxar um veículo)",
  "Ezequiel critica os profetas que rebocam uma parede fraca: escondem o perigo com palavras de paz (Ezequiel "
  "13:10-15).", s=("H2902", "H7874"))
t("afronta", r"afront\w+", "insulto, humilhação pública; 'afrontar' é insultar, humilhar", s=("H2781", "H2778", "H3637"))
t("desembainhar", r"desembainh\w+", "tirar a espada da bainha, o estojo onde ela fica", s=("H7324", "H8025"))
t("declinar", r"declin\w+", "baixar, inclinar-se; a sombra que declina é a do fim do dia", s=("H5186",))
t("conjurar", r"conjur\w+", "fazer alguém jurar, obrigá-lo por juramento solene", s=("H7650", "G3726", "G1844"))
t("folgar", r"folg\w+", "descansar, parar o trabalho; também alegrar-se",
  "No sábado, o povo, os servos e os animais deviam folgar; nos anos sabáticos, a terra também 'folgava' "
  "(Êxodo 23:12; Levítico 26:34).", s=("H7673", "H5117"))
t("apregoar", r"aprego\w+", "anunciar em voz alta, proclamar publicamente", s=("G2784", "H7121"))
t("testificar", r"testific\w+|testifiqu\w+", "dar testemunho, declarar como testemunha",
  "Em Êxodo 25–30, 'ali testificarei' traduz o verbo do encontro marcado: é Deus prometendo encontrar-se com o "
  "seu povo na tenda (Êxodo 29:42-43).", s=("H5749", "G3140", "G1263"))
t("demandar", r"demand\w+", "pedir, exigir, pedir contas ('demanda' é o pedido, ou a causa que se defende num "
  "julgamento)")
t("gloriar-se", r"glori(?:ar|o|as|a|amos|am|ei|ou|aram|e|es|em|emos|ai|ando|ado|aste|ava|avam|armos|ardes)",
  "orgulhar-se, vangloriar-se; ou alegrar-se com orgulho em algo",
  "Quem se gloria, glorie-se no Senhor (1 Coríntios 1:31, citando Jeremias 9:24).", s=("H1984", "H6286", "G2744"))
t("lisonja", r"lisonj\w+", "elogio falso e interesseiro; 'lisonjear' é bajular", s=("H2513", "H2509", "H2505", "H3655"))
t("recostar-se", r"recost\w+|reclin\w+", "apoiar-se, encostar-se para descansar",
  "Nos banquetes, comia-se recostado em almofadas ou divãs, apoiado no cotovelo.", s=("H8172", "G345", "G347", "G377"))
t("aparentar-se", r"aparent(?:ai|ar|arás|arão|aram|aste|ou|ares|armos)", "tornar-se parente por casamento",
  "Israel não devia se aparentar com os povos de Canaã (Deuteronômio 7:3; Esdras 9:14).", s=("H2859",))
t("sobrevir", r"sobrev(?:ir|irá|irão|ém|êm|eio|ieram|inha|inham|indo|iesse|ier|ierem|irem)",
  "acontecer de repente, chegar (geralmente um mal)", s=("H7122", "G1904", "G4819"))
t("regozijo", r"regozij\w+", "grande alegria; 'regozijar-se' é alegrar-se muito", s=("H7797", "H5937", "H8055"))
t("enxertar", r"enxert\w+", "inserir o ramo de uma planta em outra, para que cresçam unidos",
  "Paulo compara os gentios a ramos de oliveira brava enxertados na oliveira boa, o povo de Deus "
  "(Romanos 11:17-24).", s=("G1461",))
t("imolar", r"imol\w+", "sacrificar, matar como oferta", s=("H2076", "G2380"))
t("entalhar", r"entalh\w+", "esculpir, gravar na madeira ou na pedra ('entalhadura' é o desenho assim feito)", s=("H4734", "H6603", "H6605", "H7049", "H6458"))
t("padecer", r"padec\w+|padeç\w+", "sofrer",
  "Cristo padeceu uma vez pelos pecados, o justo pelos injustos (1 Pedro 3:18).", s=("G3958",))
t("repúdio", r"repúdios?|repudi\w+", "rejeição; 'repudiar' a esposa é divorciar-se dela, mandá-la embora",
  "A Lei previa a 'carta de repúdio' (Deuteronômio 24:1); Jesus ensinou que no princípio não foi assim "
  "(Mateus 19:3-9).", s=("H1644", "H3748", "G647", "G630"))
t("abrasar", r"abras\w+", "queimar com fogo forte, incendiar")
t("senhorear", r"(?:en)?senhore(?:ar|arás|ará|arão|ava|avam|ie|iem|ou|aram|ando|ares|arem)",
  "dominar, governar como senhor",
  "Deus deu ao ser humano a tarefa de dominar sobre a criação (Gênesis 1:26-28).", s=("H4910", "H7287", "G2961", "G2634"))
t("minguar", r"mingu\w+|míngua", "diminuir, ir faltando ('à míngua' é na falta de tudo)", s=("H4591", "H2637"))
t("constranger", r"constrang\w+|constranj\w+", "insistir muito, pressionar alguém a fazer algo",
  "Não tem o sentido de hoje, de envergonhar: a sunamita 'constrangeu' Eliseu a comer, isto é, insistiu "
  "(2 Reis 4:8).", s=("H6693", "H6484", "H2388", "G315", "G4912"))
t("deleitar", r"deleit\w+", "dar ou sentir grande prazer ('deleite' é esse prazer)",
  "'Deleita-te no SENHOR' (Salmo 37:4).", s=("H6026", "H8173", "H8191", "H2654"))
t("arrendar", r"arrend\w+", "alugar uma terra ou uma vinha a outros, que pagam com parte da colheita",
  "Na parábola, o dono arrendou a vinha a lavradores maus (Mateus 21:33-41).", s=("G1554",))
t("embalsamar", r"embalsam\w+", "preparar o corpo de um morto com resinas e especiarias para conservá-lo",
  "Os egípcios embalsamaram Jacó e José (Gênesis 50:2-3, 26).", s=("H2590",))
t("dizimar", r"dizim(?:ar|arás|ou|aram|ará|a|am|ado|ais|amos|o)",
  "dar ou cobrar o dízimo (e não exterminar, como hoje)",
  "Jesus critica quem dizimava até as ervas da horta e esquecia a justiça (Mateus 23:23).", s=("H6237", "G586", "G1183"))
t("desbaratar", r"desbarat\w+", "derrotar, pôr em fuga", s=("H2000",))
t("acometer", r"acomet\w+", "atacar, lançar-se contra")
t("arremeter", r"arremet\w+", "lançar-se com força contra, atacar")
t("alvoroço", r"alvoroç\w+", "agitação, tumulto; 'alvoroçar' é agitar, perturbar", s=("G2350", "G2351", "G5017"))
t("inquirir", r"inquir\w+", "perguntar, investigar")
t("enternecer", r"enternec\w+", "comover, encher de ternura", s=("H3648", "H7401"))
t("escarvar", r"escarv\w+", "cavar o chão com a pata, como faz o cavalo", s=("H2658",))
t("entretecer", r"entretec\w+", "tecer junto, entrelaçar", s=("H8276",))
t("cirandar", r"cirand(?:ar|ad[oa]s?|ou|arei)", "peneirar, sacudir na peneira para separar o grão da palha",
  "Jesus avisou Pedro de que Satanás pedira para cirandá-los como trigo (Lucas 22:31).", s=("H3531", "H5128", "G4617"))
t("bradar", r"brad\w+", "gritar alto ('brado' é o grito)", s=("G994", "G2896", "G2905", "H7321"))
t("mortificar", r"mortific\w+|mortifiqu\w+", "fazer morrer",
  "'Mortificar' as obras da carne é combatê-las até a morte, pelo Espírito (Romanos 8:13; Colossenses 3:5).", s=("G2289", "G3499"))
t("caiar", r"cai(?:ar|ais|ad[oa]s?)|caiadura", "pintar de branco com cal",
  "Jesus chamou os fariseus de 'sepulcros caiados': bonitos por fora, cheios de podridão por dentro "
  "(Mateus 23:27).", s=("G2867", "H1528"))
t("padejar", r"padej\w+", "lançar o grão debulhado ao ar com a pá, para o vento levar a palha",
  "Imagem do juízo que separa e espalha (Isaías 41:16; Jeremias 4:11).", s=("H2219",))
t("trilhar", r"trilh(?:ar|ou|ado|ada|ará|arei|arás|arão|am|avam|ava|adores?)",
  "debulhar o cereal, pisando-o com bois ou passando sobre ele o trilho, uma prancha pesada",
  "A Lei não deixava amordaçar o boi enquanto trilhava (Deuteronômio 25:4).", s=("H1758", "G248"))
t("retinir", r"retin\w+", "soar, zumbir",
  "'Retinir os ouvidos' é o choque de quem ouve uma notícia terrível (1 Samuel 3:11; 2 Reis 21:12).", s=("H6750",))
t("erigir", r"erig\w+|erij\w+", "levantar, construir (um altar, uma coluna)", s=("H5324", "H6965"))
t("outorgar", r"outorg\w+", "conceder, dar")
t("sobrepujar", r"sobrepuj\w+", "superar, ser maior que")
t("desarraigar", r"desarraig\w+", "arrancar pela raiz", s=("H5428", "H6131", "G1610"))
t("entenebrecer", r"entenebrec\w+|entenebreç\w+", "escurecer", s=("H3543",))

# ------------------------------------------------------------------ palavras que mudaram de sentido
t("aborrecer", r"aborrec\w+|aborreç\w+", "odiar, detestar (e não entediar, como hoje)",
  "No segundo mandamento, Deus fala dos 'que me aborrecem', isto é, dos que o odeiam (Êxodo 20:5).", s=("H8130", "H8135", "G3404"))
t("assombro", r"assombr\w+", "espanto, pavor; 'assombrar' é espantar (nada a ver com fantasmas)", s=("H8047", "H8074", "H926", "H1204", "H6342", "G1839", "G2284"))
t("adulterar", r"adulter(?:ar|ou|aram|as|a|am|ará|arás|arão|ado|ada|ando|e|es|em|ei|ais)",
  "cometer adultério (e não falsificar, como hoje)",
  "Os profetas chamam de adultério a idolatria de Israel, infiel ao SENHOR como uma esposa infiel (Jeremias 3:8-9).", s=("G3431", "H5003", "G3429"))
t("zelo", r"zelos[oa]s?|zelo", "ardor, dedicação intensa",
  "Dito de Deus, 'zeloso' é o seu santo ciúme: como o marido fiel, ele não aceita dividir o seu povo com outros "
  "deuses (Êxodo 20:5; 34:14).", s=("H7067", "H7068", "H7065", "G2205", "G2207", "G2206"))
t("simples", r"simples", "ingênuo, inexperiente, que se deixa levar com facilidade",
  "Em Provérbios e nos Salmos, o 'simples' precisa aprender sabedoria, e Deus o protege (Salmo 19:7; 116:6).",
  s=("H6612",), exige=True)
t("dote", r"dotes?", "o valor que o noivo pagava à família da noiva",
  "Na Bíblia quem paga é o noivo, ao contrário do costume europeu posterior (Gênesis 34:12; Êxodo 22:16-17).", s=("H4119",))
t("corrupção", r"corrupç(?:ão|ões)|corruptíve(?:l|is)",
  "apodrecimento, decomposição; também defeito ou perversão. 'Corruptível' é o que se estraga e morre",
  "Não é o sentido de hoje, de suborno: 'ver a corrupção' é apodrecer no túmulo, e o Santo de Deus não a viu "
  "(Salmo 16:10; Atos 2:27-31).", s=("G1312", "G5356", "G5349", "H7845", "H4893"))
t("seita", r"seitas?", "partido, escola, grupo (sem o sentido negativo de hoje)",
  "A mesma palavra grega designa os fariseus e os saduceus; os acusadores de Paulo chamavam os cristãos de "
  "'seita dos nazarenos' (Atos 24:5, 14).", s=("G139",), exige=True)
t("santos", r"(?:(?<=os )|(?<=aos )|(?<=dos )|(?<=nos )|(?<=pelos ))santos(?! (?:profetas|anjos|apóstolos|homens))",
  "no Novo Testamento, todos os que pertencem a Cristo, separados por Deus para ele",
  "Não é um grupo especial de crentes: Paulo escreve 'aos santos' de cada igreja (1 Coríntios 1:2; "
  "Filipenses 1:1).", s=("G40",), exige=True)
t("laço", r"laços?", "armadilha de caçador, feita de corda; figurado, cilada, perigo escondido",
  "Os povos e os deuses de Canaã seriam um laço para Israel (Êxodo 23:33; Josué 23:13).",
  s=("H6341", "H4170"), exige=True)
t("sóbrio", r"sóbri[oa]s?|sobriedade", "equilibrado, vigilante, com domínio de si",
  "No Novo Testamento é mais do que não estar bêbado: é ter a mente desperta e controlada (1 Tessalonicenses 5:6-8; "
  "1 Pedro 5:8).", s=("G3525", "G3524", "G4998", "G4997"))
t("cálice", r"cálices?", "taça",
  "Figurado, a porção que Deus dá a alguém, de bênção ou de juízo: o cálice da ira (Jeremias 25:15) e o cálice "
  "que Jesus pediu que passasse dele (Mateus 26:39).", s=("H3563", "G4221"))
t("tribulação", r"tribulaç(?:ão|ões)", "sofrimento, aflição intensa, perseguição",
  "Jesus avisou que no mundo os seus teriam aflições, mas que ele venceu o mundo (João 16:33).", s=("G2347", "H6869", "H6862"))
t("mansidão", r"mans[oa]s?|mansidão|mansamente", "brandura: o manso é paciente e não se vinga",
  "Não é fraqueza: Moisés era muito manso (Números 12:3), e Jesus se diz manso e humilde de coração "
  "(Mateus 11:29). Dito de animais, manso é o domesticado.", s=("H6035", "H6038", "G4239", "G4236", "G4235", "G4240"))
t("ímpio", r"ímpi[oa]s?|impied\w+|impiamente", "quem vive sem Deus e despreza a sua lei; 'impiedade' é essa atitude",
  "Nos Salmos e nos Provérbios, o ímpio é o contrário do justo (Salmo 1:1-6).", s=("H7563", "H7561", "H7562", "H1100", "G765", "G763", "G764"))
t("íntegro", r"íntegr[oa]s?|integridade", "inteiro, honesto, sem falsidade; 'integridade' é essa retidão",
  "Jó era íntegro e reto (Jó 1:1): não sem pecado, mas de coração sincero diante de Deus.", s=("H8535", "H8537", "H8538", "H8549", "H8003"))
t("soberba", r"soberb\w+|ensoberbec\w+", "orgulho, arrogância; 'soberbo' é o orgulhoso",
  "Provérbios 16:18 diz que ela vem antes da queda; Deus resiste aos soberbos (Tiago 4:6).", s=("H1347", "H1346", "H1343", "H2087", "H2102", "G5244", "G5243"))
t("vanglória", r"vangl[oó]ri\w+", "orgulho vazio, desejo de ser admirado; 'vangloriar-se' é gabar-se", s=("G2754", "G2755", "G212"))
t("lícito", r"lícit[oa]s?", "permitido pela lei",
  "Os fariseus discutiam com Jesus o que era lícito fazer no sábado (Mateus 12:10-12).", s=("G1832",))
t(None, r"irrepreensíve(?:l|is)|irrepreensivelmente|inculpáve(?:l|is)",
  "de conduta sem acusação: contra quem não há queixa justa",
  "Não quer dizer sem pecado. É a primeira exigência para quem lidera a igreja (1 Timóteo 3:2).",
  id="irrepreensivel", s=("G423", "G410", "G273", "G274", "G299", "G298"))
t("temente", r"tementes?", "quem teme a Deus: quem o respeita e lhe obedece",
  "Em Atos, 'tementes a Deus' são também os gentios que adoravam o Deus de Israel sem se tornar judeus, como "
  "Cornélio (Atos 10:2; 13:16).", s=("H3373", "G5399", "G2318"))
t("iníquo", r"iníqu[oa]s?", "injusto, perverso", s=("H5767", "H5766", "G94"))
t("devassidão", r"devassid(?:ão|ões)|devass[oa]s?", "vida sem freio, entregue aos prazeres e à imoralidade", s=("G810", "G766"))
t("fornicação", r"fornic\w+", "relação sexual fora do casamento; nos profetas, imagem da idolatria",
  "No Novo Testamento, a palavra grega (porneia) cobre todo tipo de imoralidade sexual (1 Coríntios 6:18).", s=("G4202", "G4203", "G1608", "H2181"))
t("infâmia", r"infâmias?|infames?", "desonra pública, vergonha; 'infame' é quem a merece", s=("H1681", "G819", "G820"))
t("ocioso", r"ocios[oa]s?|ociosidade", "parado, sem fazer nada; 'ociosidade' é a preguiça",
  "Paulo manda os ociosos trabalharem e comerem o próprio pão (2 Tessalonicenses 3:11-12).", s=("G692", "H7386", "H6103", "H7503"))
t("idôneo", r"idône[oa]s?", "capaz, apto para uma tarefa",
  "Em Gênesis 2:18, a ajuda 'idônea' é a que corresponde ao homem, que está à altura dele.", s=("H5048", "G2425"))
t("vindouro", r"vindour[oa]s?", "que há de vir, futuro", s=("G3195", "G2064"))
t("porvir", r"porvir", "o futuro, o que há de vir")
t("sempiterno", r"sempitern[oa]s?", "eterno, que dura para sempre")
t("execrável", r"execráve(?:l|is)", "detestável, abominável")
t("copioso", r"copios[oa]s?", "abundante")
t("turbação", r"turbaç(?:ão|ões)", "perturbação, inquietação", s=("H6330",))
t("desterrado", r"desterr\w+", "expulso da sua terra, exilado", s=("H1540", "H5080", "H1473"))
t("ermo", r"ermos?", "lugar deserto, despovoado")
t("refrigério", r"refrigérios?", "alívio, descanso que renova as forças",
  "Pedro fala dos tempos de refrigério que vêm da presença do Senhor (Atos 3:19).", s=("G403", "H5314", "H7304"))
t("chamamento", r"chamamentos?", "chamado, vocação: o chamado de Deus para a salvação e o serviço", s=("G2821",))
t("caterva", r"catervas?", "bando, multidão desordenada")
t("iguaria", r"iguarias?", "comida saborosa, prato especial", s=("H4303", "H4864"))
t("formosura", r"formosuras?", "beleza", s=("H3308", "H8597", "H1926"))
t("semblante", r"semblantes?", "rosto, a expressão do rosto", s=("H2122", "H6440"))
t("maioral", r"maiora(?:l|is)", "chefe, o principal de um grupo", s=("H7261", "H6579", "H7218"))
t("tributo", r"tributos?", "imposto pago a um rei ou a um império dominante; às vezes, trabalho forçado", s=("H4522", "H4371", "H4061", "H4503", "G2778", "G5411"))
t("fiador", r"fiador(?:es)?|fiança", "quem se responsabiliza pela dívida ou pela pessoa de outro",
  "Judá se fez fiador de Benjamim diante do pai (Gênesis 43:9); Provérbios adverte contra ficar por fiador de "
  "estranhos (Provérbios 6:1-5; 11:15).", s=("H6148", "G1450"))
t("penhor", r"penhor\w*", "objeto entregue como garantia de uma dívida ('penhorar' é tomar essa garantia)",
  "A Lei mandava devolver antes da noite a capa do pobre tomada em penhor, porque era o seu cobertor "
  "(Êxodo 22:26-27).", s=("H2254", "H2258", "H5667", "H6162", "H6161"))
t("êxtase", r"êxtases?", "estado em que alguém fica fora de si, tomado por uma visão",
  "Pedro e Paulo tiveram visões assim (Atos 10:10; 22:17).", s=("G1611",))
t("agouro", r"agour\w+", "sinal que se interpretava como anúncio do futuro ('agoureiro' é quem lê esses sinais)",
  "A Lei proíbe os agoureiros (Deuteronômio 18:10); Balaão reconheceu que não há agouro contra o povo de Deus "
  "(Números 23:23).", s=("H5172", "H5173", "H6049"))
t("adivinhação", r"adivinh\w+", "tentar descobrir o futuro ou o oculto por sinais, sortes ou espíritos",
  "A Lei proíbe toda adivinhação e feitiçaria (Deuteronômio 18:10-12).", s=("H7080", "H7081", "H3049", "H1505", "H5172", "G3132", "G4436"))
t("astrólogo", r"astrólogos?", "quem tentava ler o futuro nos astros",
  "Os astrólogos da Babilônia não souberam revelar o sonho do rei (Daniel 2:2-11).", s=("H826", "H825", "H1895"))
t("necromante", r"necromantes?|necromancia", "quem diz consultar os mortos",
  "A Lei proíbe consultar os mortos (Deuteronômio 18:11); Saul o fez antes da sua última batalha (1 Samuel 28).", s=("H178", "H3049"))
t("pitonisa", r"pitonisas?", "mulher que diz consultar os mortos ou ter um espírito de adivinhação",
  "Saul consultou uma em En-Dor (1 Samuel 28:7-8); em Filipos, Paulo expulsou de uma escrava o espírito de "
  "adivinhação (Atos 16:16-18).", s=("H178", "G4436", "G3132"))
t("sodomitas", r"sodomitas?", "homens que se prostituíam nos cultos pagãos",
  "Não se refere aos moradores de Sodoma: no original é o 'consagrado' à prostituição dos templos de Canaã, "
  "prática que os reis fiéis expulsaram da terra (1 Reis 15:12; 2 Reis 23:7).", s=("H6945",), exige=True)

# ------------------------------------------------------------------ pessoas, cargos e ofícios
t("oleiro", r"oleiros?", "quem faz vasos de barro",
  "Deus é comparado ao oleiro, que molda o barro como quer (Jeremias 18:1-6; Romanos 9:20-21).", s=("H3335", "G2763"))
t("artífice", r"artífices?", "artesão habilidoso: quem trabalha a madeira, o metal ou a pedra", s=("H2796", "G5079"))
t("ourives", r"ourives", "artesão que trabalha o ouro e a prata",
  "Os profetas zombam dos ídolos feitos pelo ourives e carregados nos ombros (Isaías 40:19; 46:6-7).", s=("H6884",))
t("flecheiro", r"flecheiros?", "soldado armado de arco e flecha, arqueiro", s=("H7228", "H3384", "H7198"))
t("pajem", r"(?:pajens?|pajem)(?: de armas)?", "rapaz que acompanha e serve um senhor; 'pajem de armas' é o que "
  "carrega as armas dele")
t("camareiro", r"camareir[oa]s?", "oficial que cuidava dos aposentos do rei: homem de confiança da corte",
  "Blasto, camareiro do rei Herodes (Atos 12:20).", s=("G2846",))
t("curtidor", r"curtidor(?:es)?", "quem prepara o couro dos animais",
  "Pedro ficou em Jope na casa de Simão, o curtidor (Atos 9:43; 10:6).", s=("G1038",))
t("cambistas", r"cambistas?|cambiadores?", "quem trocava moedas no templo, cobrando uma taxa",
  "As ofertas do templo eram pagas com moedas próprias; Jesus derrubou as mesas dos cambistas, que faziam da casa "
  "de oração um comércio (João 2:14-16; Mateus 21:12-13).", s=("G2855", "G2773"))
t("duque", r"duques?|ducados?", "chefe de clã",
  "Não é o título de nobreza europeu: os 'duques' de Edom eram os chefes das famílias de Esaú (Gênesis 36:15-43).", s=("H441",))
t("testador", r"testador", "quem faz um testamento",
  "Hebreus 9:16-17 compara a nova aliança a um testamento, que só vale depois da morte de quem o fez.", s=("G1303",))
t("apóstolo", r"apóstol[oa]s?|apostolado", "'enviado', em grego",
  "Os doze discípulos que Jesus escolheu para serem suas testemunhas, e também Paulo (Lucas 6:13; Atos 1:21-26; "
  "1 Coríntios 15:7-9).", s=("G652", "G651"))
t("evangelista", r"evangelistas?", "quem anuncia o evangelho",
  "Filipe é chamado assim (Atos 21:8); é um dos dons que Cristo deu à igreja (Efésios 4:11).", s=("G2099",))
t("presbítero", r"presbíter[oa]s?|presbitério", "'mais velho', em grego: o líder que pastoreia e governa a igreja local",
  "No Novo Testamento, os presbíteros também são chamados de bispos, isto é, supervisores (Atos 20:17, 28; "
  "Tito 1:5-7). O presbitério é o conselho deles (1 Timóteo 4:14).", s=("G4245", "G4244"))
t("bispo", r"bispos?|episcopado", "'supervisor', em grego: quem cuida e governa a igreja local",
  "Paulo lista as qualidades do bispo em 1 Timóteo 3:1-7.", s=("G1985", "G1984"))
t("diácono", r"diácon[oa]s?|diaconisas?",
  "'servo', em grego: quem serve a igreja nas tarefas práticas e no cuidado dos necessitados",
  "1 Timóteo 3:8-13.", s=("G1249",))
t("arcanjo", r"arcanjos?", "anjo principal",
  "Miguel é chamado arcanjo (Judas 9); a voz do arcanjo anunciará a volta do Senhor (1 Tessalonicenses 4:16).", s=("G743",))
t("César", r"césar(?:es)?", "título dos imperadores romanos, tirado do nome de Júlio César",
  "No tempo do ministério de Jesus o imperador era Tibério; o César a quem Paulo apelou era Nero (Lucas 3:1; "
  "Atos 25:11).", s=("G2541",))

# ------------------------------------------------------------------ povos e gentílicos
t("queneus", r"queneus?", "povo nômade, aparentado de Moisés por casamento, que viveu junto de Israel",
  "O sogro de Moisés era queneu (Juízes 1:16), e Jael, que matou Sísera, era mulher de um queneu (Juízes 4:17).", s=("H7017",))
t("quenezeu", r"quenezeu", "descendente de Quenaz", "Assim são chamados Calebe e sua família (Números 32:12; "
  "Josué 14:6).", s=("H7074",))
t(None, r"zuzins|emins|zanzumins|aveus|cadmoneus|quenezeus", "povos antigos de Canaã e arredores",
  "Alguns eram tidos como gigantes, como os anaquins (Deuteronômio 2:10-23).", id="povos-antigos", s=("H368", "H2104", "H2157", "H5761", "H6935", "H7074"))
t(None, r"arqueus|sineus|arvadeus|zemareus|hamateus", "povos descendentes de Canaã (Gênesis 10:15-18)",
  id="povos-de-canaa", s=("H6208", "H5513", "H721", "H6786", "H2577"))
t("girgaseus", r"girgaseus?|gergeseus?", "um dos povos que habitavam Canaã antes de Israel (Gênesis 15:21; "
  "Josué 3:10)", s=("H1622",))
t("horeus", r"horeus?", "antigos moradores das montanhas de Seir, desalojados pelos descendentes de Esaú",
  "Deuteronômio 2:12, 22.", s=("H2752",))
t("caftoreus", r"caftoreus|caftorins?", "os de Caftor, provavelmente a ilha de Creta",
  "Dali vieram os filisteus (Deuteronômio 2:23; Amós 9:7).", s=("H3732",))
t("arameus", r"arameus?|arameias?|aramaic[oa]s?|siríac[oa]s?|sírios?|sírias?",
  "os arameus, ou sírios: povo da Síria e da Mesopotâmia, com capital em Damasco; aramaico (ou siríaco) é a sua "
  "língua",
  "O aramaico era a língua da diplomacia no tempo dos assírios (2 Reis 18:26) e é a de partes de Esdras e de "
  "Daniel. Jesus falava aramaico (Marcos 5:41).", s=("H761", "H762"))
t("cuxita", r"cuxitas?", "natural de Cuxe, a terra ao sul do Egito (a antiga Etiópia, no atual Sudão)",
  "Ebede-Meleque, que tirou Jeremias da cisterna, era cuxita (Jeremias 38:7-13).", s=("H3569",))
t("sidônios", r"sidônios?|sidônias?", "os de Sidom, cidade fenícia do litoral, ao norte de Israel",
  "Jezabel era filha do rei dos sidônios (1 Reis 16:31).", s=("H6722",))
t("tírios", r"tírios?", "os de Tiro, cidade fenícia do litoral, famosa pelo comércio",
  "Hirão, rei de Tiro, mandou cedros e artífices para o templo de Salomão (1 Reis 5).", s=("H6876",))
t("sabeus", r"sabeus", "o povo de Sabá, no sul da Arábia",
  "Em Jó 1:15, um bando de sabeus atacou e levou os bois e as jumentas de Jó.", s=("H7615", "H5436"))
t("elamitas", r"elamitas?", "os de Elão, país a leste da Babilônia, no atual Irã",
  "Havia elamitas em Jerusalém no dia de Pentecostes (Atos 2:9).", s=("H896", "G1639"))
t("hagarenos", r"hagarenos", "povo nômade do deserto, a leste de Gileade (1 Crônicas 5:10, 19-20)", s=("H1905",))
t("ismaelitas", r"ismaelitas?", "descendentes de Ismael, filho de Abraão e Agar",
  "Mercadores ismaelitas levaram José ao Egito (Gênesis 37:25-28).", s=("H3459",))
t("agagita", r"agagitas?", "descendente de Agague, rei dos amalequitas",
  "Hamã, o inimigo dos judeus no livro de Ester, era agagita (Ester 3:1).", s=("H91",))
t("gibeonitas", r"gibeonitas?", "os habitantes de Gibeom, cidade heveia perto de Jerusalém",
  "Enganaram Josué para fazer aliança com Israel e passaram a cortar lenha e tirar água para o santuário "
  "(Josué 9).", s=("H1393",))
t("recabitas", r"recabitas?", "descendentes de Jonadabe, filho de Recabe",
  "Por ordem dele, não bebiam vinho, não plantavam vinhas e moravam em tendas; Deus os deu como exemplo de "
  "fidelidade (Jeremias 35).", s=("H7397",))
t("quereteus e peleteus", r"quereteus|queretitas|peleteus", "a guarda pessoal do rei Davi",
  "Eram provavelmente estrangeiros ligados a Creta e aos filisteus, sob o comando de Benaia (2 Samuel 8:18; 15:18).", s=("H3774", "H6432"))
t(None, r"geteus?|giteus|asdoditas?|ecronitas?|gazitas?|asquelonitas?",
  "habitante de uma das cinco cidades dos filisteus: Gaza, Asdode, Ascalom, Gate e Ecrom",
  "Obede-Edom, em cuja casa ficou a arca, e Itai, fiel a Davi, eram geteus, isto é, de Gate (2 Samuel 6:10; "
  "15:19).", id="cidades-filisteias", s=("H1663", "H796", "H6139", "H5841", "H832"))
t(None, r"rubenitas?|gaditas?|simeonitas?|benjamitas?|efraimitas?|zebulonitas?|danitas?|aseritas?|naftalitas?",
  "membro de uma das tribos de Israel, que levam o nome do antepassado: rubenitas, de Rúben; gaditas, de Gade; "
  "benjamitas, de Benjamim",
  "Rúben, Gade e metade da tribo de Manassés ficaram com terras a leste do Jordão (Números 32).",
  id="tribos-de-israel", s=("H7206", "H1425", "H8099", "H1145", "H2075", "H1839"))
t("coatitas", r"coatitas?", "os levitas da família de Coate",
  "Carregavam os objetos mais santos do tabernáculo, como a arca, depois de cobertos pelos sacerdotes "
  "(Números 4:1-15).", s=("H6956",))
t("gersonitas", r"gersonitas?", "os levitas da família de Gérson",
  "Carregavam as cortinas e as coberturas do tabernáculo (Números 4:21-28).", s=("H1649",))
t("meraritas", r"meraritas?", "os levitas da família de Merari",
  "Carregavam as tábuas, as colunas e as bases do tabernáculo (Números 4:29-33).", s=("H4848",))
t("coraítas", r"coraítas?", "os levitas descendentes de Corá",
  "Eram porteiros e cantores do templo; vários salmos levam o nome dos filhos de Corá (Salmos 42–49).", s=("H7145",))
t(None, r"hebronitas?|izaritas?|anramitas?|uzielitas?|malitas?|musitas?|libnitas?|simeítas?|hezronitas?|zeraítas?|"
        r"jezeritas?|suamitas?|enoquitas?|paluítas?|nemuelitas?|jaminitas?|jaquinitas?|saulitas?|zefonitas?|hagitas?|"
        r"oznitas?|eritas?|aroditas?|arelitas?|selanitas?|perezitas?|hamulitas?|tolaítas?|puvitas?|jasubitas?|"
        r"sinronitas?|sereditas?|elonitas?|jaleelitas?|maquiritas?|helequitas?|asrielitas?|siquemitas?|semidaítas?|"
        r"heferitas?|sutelaítas?|bequeritas?|taanitas?|eranitas?|belaítas?|asbelitas?|airamitas?|sufamitas?|"
        r"hufamitas?|arditas?|naamanitas?|imnaítas?|isvitas?|beriitas?|heberitas?|malquielitas?|jazeelitas?|gunitas?|"
        r"silemitas?|abiezritas?",
  "clã, família de uma tribo de Israel, chamada pelo nome de quem a originou",
  "Números 26 lista os clãs de cada tribo no segundo recenseamento, pouco antes da entrada em Canaã.",
  id="clas-de-israel")
t(None, r"netofatitas?|piratonitas?|husatitas?|beerotitas?|haroditas?|pelonitas?|anatotitas?|aoítas?|maacatitas?|"
        r"itritas?|hararitas?|taquemonitas?|eznitas?|araítas?|paltitas?|barumitas?|meolatitas?|gilonitas?|"
        r"neelamitas?|jairitas?|meronotitas?|morastitas?|zifitas?|gessuritas?",
  "indica a origem: a cidade, a terra ou o clã de onde a pessoa vem (como hoje se diz 'paulista' ou 'mineiro')",
  "Nas listas dos valentes de Davi, cada guerreiro é identificado assim (2 Samuel 23:8-39; 1 Crônicas 11:10-47).",
  id="natural-de")
t("gileadita", r"gileaditas?", "natural de Gileade, a região montanhosa a leste do Jordão",
  "Jefté e Barzilai eram gileaditas (Juízes 11:1; 2 Samuel 17:27).", s=("H1569",))
t("efrateu", r"efrateus?", "natural de Efrata, o antigo nome de Belém",
  "Assim são chamados a família de Noemi e Jessé, pai de Davi (Rute 1:2; 1 Samuel 17:12). Em 1 Reis 11:26 "
  "(Jeroboão), quer dizer efraimita.", s=("H673",))
t("sunamita", r"sunamitas?", "natural de Suném, aldeia no vale de Jezreel",
  "Abisague, que cuidou de Davi na velhice, e a mulher que hospedava Eliseu eram sunamitas (1 Reis 1:3; "
  "2 Reis 4:8-12).", s=("H7767",))
t("jezreelita", r"jezreelitas?", "natural de Jezreel, cidade do vale do mesmo nome",
  "Nabote, cuja vinha Acabe cobiçou, era jezreelita (1 Reis 21:1).", s=("H3158",))
t("silonita", r"silonitas?", "natural de Siló, onde ficou o tabernáculo no tempo dos juízes",
  "O profeta Aías era silonita (1 Reis 11:29).", s=("H7888",))
t("arquita", r"arquitas?", "do clã dos arquitas, perto de Betel",
  "Husai, o arquita, amigo de Davi, desfez o conselho de Aitofel (2 Samuel 15:32-37; 17:5-14).", s=("H757",))
t("adulamita", r"adulamitas?", "natural de Adulão, cidade de Judá", "Hira, amigo de Judá (Gênesis 38:1, 12, 20).", s=("H5726",))
t("horonita", r"horonitas?", "natural de Bete-Horom",
  "Sambalate, o horonita, se opôs à reconstrução dos muros de Jerusalém (Neemias 2:10, 19).", s=("H2772",))
t("temanita", r"temanitas?", "natural de Temã, região de Edom", "Elifaz, um dos amigos de Jó (Jó 2:11).", s=("H8489",))
t("suíta", r"suítas?", "descendente de Suá, filho de Abraão e Quetura", "Bildade, um dos amigos de Jó (Jó 2:11).", s=("H7747",))
t("naamita", r"naamitas?", "natural de Naamá", "Zofar, um dos amigos de Jó (Jó 2:11).", s=("H6691",))
t("buzita", r"buzitas?", "descendente de Buz, parente de Abraão", "Eliú, o jovem que fala a Jó (Jó 32:2).", s=("H940",))
t("cireneu", r"cireneus?", "natural de Cirene, cidade grega no norte da África (na atual Líbia)",
  "Simão, o cireneu, foi obrigado a carregar a cruz de Jesus (Marcos 15:21).", s=("G2956",))
t("gadarenos", r"gadarenos|gerasenos|gergesenos", "moradores da região de Gadara (ou Gerasa), a leste do mar da "
  "Galileia",
  "Ali Jesus libertou um homem possuído por muitos demônios, que entraram numa manada de porcos (Marcos 5:1-20).", s=("G1086",))
t("areópago", r"areópago|areopagita", "o 'monte de Ares' em Atenas, e o conselho que se reunia ali",
  "Ali Paulo falou aos atenienses sobre o 'deus desconhecido' (Atos 17:19-34).", s=("G697", "G698"))
t("epicureus e estoicos", r"epicureus|estoicos", "escolas da filosofia grega",
  "Os epicureus buscavam a tranquilidade e o prazer moderado; os estoicos, viver segundo a razão, com domínio das "
  "paixões. Debateram com Paulo em Atenas (Atos 17:18).", s=("G1946", "G4770"))
t("nicolaítas", r"nicolaítas", "seguidores de um tal Nicolau, grupo que Jesus reprovou nas igrejas de Éfeso e de "
  "Pérgamo", "Apocalipse 2:6, 15. Pelo contexto, parece que ensinavam a participar da idolatria e da imoralidade.", s=("G3531",))

# ------------------------------------------------------------------ casa, campo e ofícios
t("umbral", r"umbra(?:l|is)", "a soleira da porta, ou as peças laterais da sua moldura",
  "Os mandamentos deviam ser escritos nos umbrais da casa (Deuteronômio 6:9).", s=("H4201", "H5592", "H4670", "H352"))
t("verga", r"vergas?", "a trave de cima da porta, apoiada nos umbrais", "Êxodo 12:7, 22-23.", s=("H4947",))
t("parapeito", r"parapeitos?", "mureta na beira de um terraço",
  "A Lei mandava fazê-lo no terraço da casa nova, para que ninguém caísse (Deuteronômio 22:8).", s=("H4624",))
t("recâmara", r"recâmaras?", "quarto interno, o cômodo mais reservado da casa", s=("H2315",))
t("estrado", r"estrados?", "tablado, plataforma (em Gênesis 49:4, a cama); 'estrado dos pés' é o banquinho onde "
  "se apoiam os pés",
  "A arca e o templo são chamados estrado dos pés de Deus (1 Crônicas 28:2; Lamentações 2:1).", s=("H1916", "G5286", "H3326"))
t("antemuro", r"antemuros?", "muro avançado, construído na frente da muralha principal", s=("H2426",))
t("aqueduto", r"aquedutos?", "canal que leva água de um lugar a outro",
  "Ezequias fez um canal que trazia a água para dentro de Jerusalém (2 Reis 20:20).", s=("H8585",))
t("liteira", r"liteiras?", "cadeira coberta, levada nos ombros por carregadores", s=("H668", "H6632"))
t("caçarola", r"caçarolas?", "panela", s=("H6517", "H5518"))
t("guisado", r"guisad[oa]s?", "cozido de carne ou de legumes, ensopado",
  "Esaú vendeu a primogenitura por um guisado de lentilhas (Gênesis 25:29-34).", s=("H4303", "H5138"))
t("mantimento", r"mantimentos?", "comida, provisão de alimento", s=("H6720", "H400", "H4241"))
t("herdade", r"herdades?", "propriedade de família, a terra herdada", s=("H5159", "H272"))
t("olival", r"olivais|olival", "plantação de oliveiras", s=("H2132",))
t("pepinal", r"pepinal", "plantação de pepinos",
  "A cabana do vigia, sozinha no meio dela, é imagem do abandono de Jerusalém (Isaías 1:8).", s=("H4750",))
t("arrebaldes", r"arrebaldes?", "os arredores de uma cidade, o terreno livre em volta dela", s=("H4054",))
t("aprisco", r"apriscos?", "curral cercado onde as ovelhas passam a noite",
  "Davi foi tirado dos apriscos para pastorear o povo de Deus (Salmo 78:70).", s=("H4356", "H1448", "H4942"))
t("manjedoura", r"manjedouras?", "cocho onde se põe a comida dos animais",
  "Jesus recém-nascido foi deitado numa manjedoura (Lucas 2:7).", s=("G5336", "H18"))
t("tosquiar", r"tosqui\w+", "cortar a lã das ovelhas ('tosquia' é esse trabalho)",
  "A tosquia era tempo de festa (1 Samuel 25:2-8). O Servo de Isaías 53:7 se cala como a ovelha diante de quem a "
  "tosquia.", s=("H1494", "G2751"))
t("vindima", r"vindim\w+", "a colheita das uvas; 'vindimar' é colhê-las",
  "Imagem do juízo de Deus (Apocalipse 14:18-19).", s=("H1210", "H1219", "G5166"))
t("sementeira", r"sementeiras?", "a semeadura; o tempo de semear", s=("H2232", "H2233"))
t("restolho", r"restolhos?", "a palha que sobra no campo depois da colheita",
  "Queima de uma vez: imagem de quem enfrenta o juízo de Deus (Isaías 47:14; Malaquias 4:1).", s=("H7179",))
t("relha", r"relhas?", "a lâmina de ferro do arado, que corta a terra",
  "Os filisteus não deixavam ferreiros em Israel; para afiar as relhas era preciso ir a eles (1 Samuel 13:19-21).", s=("H4281",))
t("aguilhada", r"aguilhadas?", "vara comprida com ponta de ferro, para tocar os bois",
  "Sangar matou seiscentos filisteus com uma aguilhada (Juízes 3:31).", s=("H4451",))
t("cabresto", r"cabrestos?", "correia posta na cabeça do animal para guiá-lo", s=("H4964",))
t("albarda", r"albardas?", "sela rústica de animal de carga", s=("H3733",))
t("cajado", r"cajados?", "bastão de apoio; o do pastor tinha a ponta curva", s=("H4938", "H4731", "H4294", "G4464"))
t("bordão", r"bordão|bordões", "bastão de apoio para caminhar", s=("H4938", "H4731", "H4294", "G4464"))
t("buril", r"buris|buril", "ferramenta de ponta dura para gravar na pedra ou no metal",
  "O pecado de Judá está escrito com buril de ferro e ponta de diamante (Jeremias 17:1).", s=("H2747", "H5842"))
t("colchete", r"colchetes?", "gancho que prende uma peça na outra",
  "Colchetes de ouro uniam as cortinas do tabernáculo pelas laçadas (Êxodo 26:6).", s=("H7165",))
t("laçadas", r"laçadas?", "alças de fio",
  "Nas cortinas do tabernáculo, recebiam os colchetes que as uniam (Êxodo 26:4-6).", s=("H3924",))
t("engaste", r"engast\w+", "armação de metal que prende uma pedra preciosa; 'engastar' é prender a pedra assim",
  "As pedras do peitoral e das ombreiras do éfode ficavam em engastes de ouro (Êxodo 28:11-13).", s=("H4865", "H4396", "H2799"))
t("ombreiras", r"ombreiras?", "peças que ficam sobre os ombros; também os batentes da porta",
  "As ombreiras do éfode levavam duas pedras de ônix com os nomes das tribos de Israel (Êxodo 28:7-12). Em "
  "Provérbios 8:34, são os batentes da porta.", s=("H3802",))
t("juntura", r"junturas?", "ponto de união entre duas peças, a junta",
  "Uma flecha atingiu o rei Acabe entre as junturas da armadura (1 Reis 22:34).", s=("H4225", "H1694"))
t("urdidura", r"urdiduras?", "os fios esticados no tear, por onde passa a trama ao tecer",
  "Aparece na lei da 'lepra' nas roupas (Levítico 13:48-59).", s=("H8359",))
t("recamado", r"recamad[oa]s?", "bordado com fios coloridos", s=("H7551",))
t("vestiduras", r"vestiduras?", "roupas, vestes",
  "Rasgar as vestiduras era sinal de dor, de luto ou de indignação (Gênesis 37:34; Mateus 26:65).", s=("H899", "H8071", "H3830", "H8278", "G2440"))
t("sábanas", r"sábanas?", "lençóis ou camisas de linho fino", "Juízes 14:12-13.", s=("H5466",))
t("caneleiras", r"caneleiras?", "peças da armadura que protegem as pernas", "Golias as usava (1 Samuel 17:6).", s=("H4697",))
t("madeiro", r"madeiros?", "peça grande de madeira, tronco",
  "Pela Lei, o condenado era pendurado num madeiro (Deuteronômio 21:22-23); os apóstolos usam a palavra para a "
  "cruz de Cristo (Atos 5:30; Gálatas 3:13).", s=("G3586", "H6086"))
t("estopa", r"estopas?", "fibra grossa de linho, que pega fogo com facilidade",
  "As cordas que prendiam Sansão se partiram como fio de estopa que chega perto do fogo (Juízes 16:9).", s=("H5296",))
t("betume", r"betume", "piche, asfalto natural",
  "Com ele a arca de Noé foi vedada (Gênesis 6:14) e também o cesto em que puseram Moisés (Êxodo 2:3).", s=("H3724", "H2564"))
t("alambre", r"alambre", "liga de cobre, como o bronze ou o latão", s=("H5178",))
t("pedrarias", r"pedrarias", "pedras preciosas")
t("pórfiro", r"pórfiro", "pedra dura, vermelha ou arroxeada, usada em pisos de luxo", s=("H923",))
t("pederneira", r"pederneiras?", "pedra muito dura, que solta faíscas: o sílex",
  "Facas de pederneira foram usadas na circuncisão (Josué 5:2); 'rosto como pederneira' é a firmeza de quem não "
  "volta atrás (Isaías 50:7).", s=("H2496", "H6864"))
t("tição", r"tição|tições", "pedaço de lenha ainda em brasa",
  "'Tição tirado do fogo' é quem foi salvo por pouco da destruição (Amós 4:11; Zacarias 3:2).", s=("H181",))
t("féretro", r"féretros?", "maca ou caixão em que se leva o morto")
t("coletoria", r"coletorias?", "posto de cobrança de impostos",
  "Mateus estava sentado na coletoria quando Jesus o chamou (Mateus 9:9).", s=("G5058",))
t("arca do tesouro", r"arcas? do tesouro", "a caixa das ofertas no templo",
  "Ali Jesus viu a viúva pobre lançar duas moedinhas (Marcos 12:41-44).", s=("G1049",))
t("arca", r"arcas?(?! do tesouro)", "caixa, baú",
  "A arca da aliança era o baú de madeira revestido de ouro que guardava as tábuas da Lei, coberto pelo "
  "propiciatório (Êxodo 25:10-22). A arca de Noé era um grande barco (Gênesis 6:14-16).",
  s=("H727", "H8392", "G2787"))

# ------------------------------------------------------------------ animais e plantas
t("asno", r"asn[oa]s?", "jumento; 'asna' é a jumenta",
  "Animal de carga e de montaria. Jesus entrou em Jerusalém montado num jumentinho, como Zacarias 9:9 anunciara "
  "(Mateus 21:5).", s=("H2543", "H860", "H5895", "G3688", "G5268"))
t("novilho", r"novilh[oa]s?", "boi novo; 'novilha' é a vaca nova",
  "Oferta comum nos sacrifícios (Levítico 4:3). As cinzas de uma novilha vermelha eram usadas na água da "
  "purificação (Números 19).", s=("H6499", "H6510", "H5695", "H5697"))
t("cevado", r"cevados?", "engordado para o abate", "O boi cevado era comida de festa (Provérbios 15:17).", s=("H4806", "H75", "H1277", "G4618"))
t("rês", r"rês|reses", "cabeça de gado (boi, ovelha, cabra)", s=("H7716",))
t("gado vacum", r"(?:gado )?vacum", "gado bovino: bois e vacas", s=("H1241",))
t("montês", r"montes(?:as?|es)", "selvagem, que vive solto nos montes e nos lugares desertos",
  "Davi se escondeu nos penhascos das cabras monteses, em En-Gedi (1 Samuel 24:2).", s=("H3277", "H6501"))
t("dromedário", r"dromedári[oa]s?", "camelo de uma corcova, usado em viagens longas", s=("H1072", "H7409"))
t("chacal", r"chaca(?:l|is)", "animal parecido com o lobo e a raposa, que vive em bandos nos desertos e nas ruínas",
  "Nos profetas, cidade que vira 'morada de chacais' é cidade arruinada e deserta (Jeremias 9:11; Isaías 13:22).", s=("H8577", "H8565"))
t("áspide", r"áspides?", "cobra venenosa, provavelmente a naja", s=("H6620",))
t("peçonha", r"peçonhas?", "veneno de animal, como o da cobra", s=("H7219", "H2534"))
t("grou", r"grous?", "ave grande e pernalta, que migra em bandos", s=("H5693",))
t("locusta", r"locustas?", "uma espécie de gafanhoto", s=("H697", "H2284"))
t("pulgão", r"pulg(?:ão|ões)", "praga que devora as plantações (na Bíblia, provavelmente uma espécie ou fase do "
  "gafanhoto)", s=("H2625",))
t("esperança (inseto)", r"esperanças?", "inseto verde parecido com o gafanhoto", "Levítico 11:22.",
  s=("H2728",), exige=True, id="esperanca-inseto")
t(None, r"quebra-ossos|esmerilh(?:ão|ões)|milhafres?|mochos?|corujão|corvos?-marinhos?|galinhas?-d'água|"
        r"gaviões-pescadores|gavião-pescador|corujas?-brancas?|íbis|(?<=a )poupas?",
  "ave que a Lei declarava impura (Levítico 11:13-19; Deuteronômio 14:11-18)",
  "Muitas dessas aves não se sabe identificar com certeza, e os nomes variam de uma tradução para outra.",
  id="ave-impura", s=("H6538", "H5822"))
t(None, r"doninhas?|lagartos? pintados?|lagartixas? de parede|salamandras?|camaleões|camaleão",
  "pequeno animal que a Lei declarava impuro (Levítico 11:29-30)", "A identificação de vários deles é incerta.",
  id="animal-impuro", s=("H2467",))
t("beemote", r"beemote", "animal enorme que Deus descreve a Jó, talvez o hipopótamo",
  "Jó 40:15-24: mostra o poder do Criador sobre criaturas que o homem não doma.", s=("H930",))
t("leviatã", r"leviatã", "grande animal das águas: em Jó 41, talvez o crocodilo",
  "Nos Salmos e em Isaías, imagem dos poderes do caos que Deus vence (Salmo 74:14; Isaías 27:1).", s=("H3882",))
t("sarça", r"sarças?", "arbusto espinhoso",
  "Deus falou a Moisés de uma sarça que ardia sem se consumir (Êxodo 3:2-4).", s=("H5572", "G942"))
t("junco", r"juncos?", "planta de caule fino e flexível, que cresce na beira da água",
  "Dela se faziam cestos e até barcos (Êxodo 2:3; Isaías 18:2).", s=("H1573", "H100", "H5488"))
t("papiro", r"papiros?", "planta alta dos pântanos do Nilo; com ela se faziam barcos e o papel antigo", s=("H1573", "H16"))
t("faia", r"faias?", "árvore de madeira nobre do Líbano, provavelmente o cipreste ou o zimbro",
  "Não é a faia europeia. Sua madeira foi usada no templo de Salomão (1 Reis 5:8-10; 6:15).", s=("H1265",))
t("álamo", r"álamos?", "árvore alta da beira dos rios, o choupo", s=("H3839",))
t("junípero", r"juníperos?|zimbros?", "arbusto do deserto, provavelmente a giesta, que dá alguma sombra",
  "Elias, desanimado, sentou-se debaixo de um junípero e pediu para morrer (1 Reis 19:4-5).", s=("H7574",))
t("murta", r"murtas?", "arbusto perfumado de folhas sempre verdes",
  "Seus ramos serviam para as cabanas da Festa dos Tabernáculos (Neemias 8:15).", s=("H1918",))
t("sândalo", r"sândalos?", "madeira nobre e perfumada",
  "Foi trazida de Ofir para o templo e para os instrumentos de música de Salomão (1 Reis 10:11-12).", s=("H484",))
t("gôfer", r"gôfer", "a madeira da arca de Noé (Gênesis 6:14); não se sabe ao certo que árvore era", s=("H1613",))
t("renovo", r"renovos?", "broto novo que nasce de uma planta ou de um tronco cortado",
  "Os profetas chamam de 'Renovo' o Messias que viria da família de Davi (Isaías 4:2; Jeremias 23:5; "
  "Zacarias 3:8).", s=("H6780", "H5342", "H3127", "H6288"))
t("endro", r"endro", "erva aromática (o aneto), usada como tempero",
  "Jesus critica quem dá o dízimo até do endro e do cominho e esquece a justiça e a misericórdia (Mateus 23:23).", s=("H7100", "G432"))
t("cálamo", r"cálamos?", "cana aromática que entrava no óleo da unção (Êxodo 30:23)", s=("H7070",))
t("estoraque", r"estoraque", "resina aromática que entrava no incenso sagrado (Êxodo 30:34)", s=("H5198",))
t("bdélio", r"bdélio", "resina aromática e preciosa (ou talvez uma pedra preciosa) da terra de Havilá "
  "(Gênesis 2:12)", s=("H916",))
t("favo", r"favos?", "as casinhas de cera que as abelhas fazem e enchem de mel",
  "As palavras de Deus são mais doces que o mel e o favo (Salmo 19:10).", s=("H5317", "H3295", "H6688"))
t("mosto", r"mostos?", "suco de uva fresco, vinho novo",
  "Junto com o trigo e o azeite, é sinal da bênção de Deus sobre a terra (Deuteronômio 7:13).", s=("H8492", "H6071", "G1098"))
t("mondaduras", r"mondaduras?", "tiras de onde se tirou a casca, deixando a madeira branca à mostra",
  "Gênesis 30:37.", s=("H6479",))
t("tutano", r"tutanos?", "a medula, a parte mole que fica dentro dos ossos; figurado, o melhor de algo", s=("H4221", "H4229"))
t("espinhaço", r"espinhaço", "a espinha dorsal, a coluna", s=("H6096",))

# ------------------------------------------------------------------ corpo e doenças
t("enfermo", r"enferm(?:[oa]s?|idades?|ou|aram|ar|ará)", "doente; 'enfermidade' é doença", s=("H2470", "H2483", "G770", "G772", "G769", "G732"))
t("chaga", r"chagas?", "ferida aberta",
  "Isaías 53:5 e 1 Pedro 2:24 falam das feridas do Servo, que trazem cura ao seu povo.", s=("H5061", "H4347", "H2250", "H2914", "G4127", "G1668"))
t("coxo", r"cox(?:o|os)", "que manca, aleijado da perna",
  "O coxo curado na porta do templo saiu andando, pulando e louvando a Deus (Atos 3:2-8).", s=("H6455", "G5560"))
t("pústula", r"pústulas?", "bolha ou ferida com pus", "A sexta praga do Egito (Êxodo 9:9-10).", s=("H76", "H4556", "H5597"))
t("impigem", r"impi(?:n)?g(?:em|ens)", "doença de pele que forma manchas e escamas",
  "O animal com impigem não podia ser oferecido (Levítico 22:22).", s=("H3217",))
t("tísica", r"tísic[oa]s?", "doença que consome o corpo aos poucos", s=("H7829",))
t("corrimento", r"corrimentos?", "secreção, fluxo que escorre do corpo",
  "Pela Lei, deixava a pessoa impura até se purificar (Levítico 15:2-15).", s=("H2100", "H2101"))
t("seminal", r"seminal", "do sêmen",
  "Pela Lei, o derramamento seminal deixava o homem impuro até a tarde (Levítico 15:16).", s=("H7902",))
t("têmporas", r"têmporas?", "os lados da testa, perto dos olhos",
  "Jael cravou uma estaca na têmpora de Sísera (Juízes 4:21).", s=("H7541",))

# ------------------------------------------------------------------ culto, tempo e calendário
t("vivente", r"viventes?", "ser vivo, o que tem vida",
  "'Alma vivente' é o ser que tem vida (Gênesis 2:7); 'a terra dos viventes' é este mundo, onde se vive "
  "(Salmo 27:13).", s=("H2416", "G2226", "G2198"))
t("luminares", r"luminares?|luminárias?", "fontes de luz: o sol, a lua e as estrelas; 'luminária' é a lâmpada",
  "Deus os pôs no céu para separar o dia da noite e marcar as estações (Gênesis 1:14-16).", s=("H3974", "G5458", "G3088"))
t("resplendor", r"resplend\w+|resplandec\w+|resplandeç\w+|resplandescentes?",
  "brilho intenso; 'resplandecer' é brilhar muito", s=("H5051", "H7160", "H2096", "H215", "G541", "G2989"))
t("cetro", r"cetros?", "bastão que o rei segura como símbolo do seu poder",
  "Gênesis 49:10 promete que o cetro não sairia de Judá: dali viria o rei, Davi e, depois dele, o Messias.", s=("H7626", "H8275", "G4464"))
t("obra servil", r"(?:obras? )?servil", "trabalho comum, o serviço do dia a dia",
  "Nos dias santos das festas, nenhuma 'obra servil' podia ser feita (Levítico 23:7-8).", s=("H5656",))
t("unguento", r"unguentos?", "óleo perfumado ou pomada, para ungir o corpo ou tratar feridas",
  "As mulheres prepararam especiarias e unguentos para o corpo de Jesus (Lucas 23:56).", s=("H7543", "H7545", "H4842", "H4841", "G3464"))
t("testemunho (tenda)", r"testemunho",
  "aqui, 'encontro': a tenda do testemunho é a tenda do encontro, onde Deus se encontrava com Moisés e com o povo",
  "Êxodo 33:7-11; Números 7:89.", s=("H4150",), exige=True, id="testemunho-tenda")
t("testemunho (a Lei)", r"testemunho",
  "a Lei de Deus, que testemunha a sua vontade; no tabernáculo, as tábuas da Lei guardadas na arca",
  "Por isso a arca é chamada 'arca do testemunho' (Êxodo 25:16, 22).", s=("H5715",), exige=True,
  id="testemunho-lei")
t("testemunhos", r"testemunhos", "os mandamentos de Deus, que testemunham a sua vontade",
  "Deuteronômio 6:17; Salmo 119:2.", s=("H5713", "H5715"), exige=True)
t(None, r"(?-i:(?<!.)(?:Álefe|Bete|Guímel|Dálete|Hê|Vau|Záin|Hete|Tete|Iode|Cafe|Lâmede|Mem|Nun|Sâmeque|Áin|Pê|Tsadê|"
        r"Cofe|Rexe|Xin|Tau)(?=:))",
  "letra do alfabeto hebraico",
  "O Salmo 119 é um acróstico: cada grupo de oito versículos começa com a mesma letra, na ordem do alfabeto.",
  id="letra-hebraica")
t("purim", r"purim", "festa judaica que celebra o livramento dos judeus no tempo de Ester",
  "O nome vem de 'pur', sorte: Hamã lançou sortes para marcar o dia da matança (Ester 3:7; 9:24-28).", s=("H6332",))
t("preparação", r"preparação", "o dia antes do sábado (a sexta-feira), em que se preparava tudo para o descanso",
  "Jesus morreu no dia da preparação, e seu corpo foi sepultado antes do começo do sábado (Marcos 15:42; "
  "João 19:31, 42).", s=("G3904",), exige=True)
t("primeiro dia da semana", r"primeiro dia da semana", "o domingo, o dia seguinte ao sábado",
  "Foi o dia da ressurreição de Jesus, e nele os cristãos se reuniam (Mateus 28:1; Atos 20:7; "
  "1 Coríntios 16:2).", s=("G4521",))
t("hora sexta", r"hora (?:terceira|sexta|nona|décima|undécima)|(?:terceira|sexta|nona|décima|undécima) hora",
  "as horas do dia eram contadas a partir do nascer do sol, por volta das 6 da manhã",
  "A hora terceira são 9 h; a sexta, meio-dia; a nona, 15 h (Marcos 15:25, 33-34).", s=("G5610",))
t("quarta vigília", r"(?:primeira|segunda|terceira|quarta) vigília",
  "a noite era dividida em quatro vigílias, turnos de guarda de três horas a partir das 18 h",
  "A quarta vigília vai das 3 às 6 da manhã: foi quando Jesus andou sobre o mar (Mateus 14:25).", s=("G5438",))
t("dispersão", r"dispersão", "os judeus que viviam espalhados pelas nações, fora da terra de Israel",
  "Tiago 1:1.", s=("G1290",), exige=True)
t("gólgota", r"gólgota", "'lugar da caveira', em aramaico: o lugar fora de Jerusalém onde Jesus foi crucificado",
  "Mateus 27:33; João 19:17.", s=("G1115",))
t("inferno (geena)", r"infernos?", "aqui, a Geena: o castigo eterno",
  "O nome vem do vale de Hinom, ao sul de Jerusalém, onde reis de Judá chegaram a sacrificar crianças a ídolos "
  "(Jeremias 7:31-32); Jesus o usa para o juízo final (Mateus 5:22, 29-30; 10:28).",
  s=("G1067",), exige=True, id="geena")
t("belzebu", r"belzebu", "nome dado ao chefe dos demônios (Mateus 12:24)",
  "Vem de Baal-Zebube, deus da cidade filisteia de Ecrom (2 Reis 1:2).", s=("G954",))
t("belial", r"belial", "'inútil, perverso', em hebraico: 'homens de Belial' são homens sem caráter",
  "Paulo usa o nome para Satanás (2 Coríntios 6:15).", s=("H1100", "G955"))
t("abadom", r"abadom|apoliom", "'destruição', em hebraico; em grego, Apoliom, 'destruidor': o anjo do abismo",
  "Apocalipse 9:11.", s=("G3", "G623"))
t("eloí", r"eloí|eli,? eli|lamá|lemá|sabactâni", "em aramaico: 'Deus meu, Deus meu, por que me desamparaste?'",
  "O grito de Jesus na cruz, com as palavras do Salmo 22:1 (Mateus 27:46; Marcos 15:34).", s=("G1682", "G2241", "G2982", "G4518"))
t("efatá", r"efatá", "'abre-te', em aramaico (Marcos 7:34)", s=("G2188",))
t("talita cumi", r"talit[aá],? cumi", "'menina, levanta-te', em aramaico (Marcos 5:41)", s=("G5008", "G2891"))
t("mene, tequel", r"(?-i:MENE|TEQUEL|PERES|PARSIM|UFARSIM)", "as palavras escritas por uma mão na parede do palácio de "
  "Belsazar",
  "Daniel as interpretou: Deus contou os dias do reino, o rei foi pesado e achado em falta, e o reino seria "
  "dividido entre medos e persas (Daniel 5:25-28).", s=("H4484", "H8625", "H6537"))
t("pedra angular", r"(?:pedra|cabeça) (?:angular|de esquina)",
  "a pedra principal da esquina, que firma e alinha toda a construção",
  "A pedra que os construtores rejeitaram tornou-se a principal: os apóstolos aplicam o Salmo 118:22 a Cristo "
  "(Atos 4:11; 1 Pedro 2:6-7).", s=("H6438", "G204", "G1137"))
t("apostasia", r"apostasias?|apóstatas?", "abandono da fé", "2 Tessalonicenses 2:3.", s=("G646",))
t("heresias", r"heresias?", "ensinos falsos que dividem a igreja", "2 Pedro 2:1.", s=("G139",))

# ------------------------------------------------------------------ medidas e pesos (2)
t("braça", r"braças?", "medida de profundidade, cerca de 1,85 m (a distância entre as mãos com os braços abertos)",
  "Atos 27:28.", s=("G3712",))
t("metreta", r"metretas?", "medida grega de líquidos, cerca de 40 litros",
  "As talhas de Caná levavam duas ou três metretas cada uma (João 2:6).", s=("G3355",))
t("libra", r"libras?", "aqui, a mina: peso de cerca de 600 gramas", s=("H4488",))
t("arrátel", r"arrátel", "a libra romana: cerca de 330 gramas",
  "Maria ungiu Jesus com um arrátel de nardo puro (João 12:3).", s=("G3046",))
t("quaternos", r"quaternos?", "grupos de quatro soldados, que se revezavam na guarda", "Atos 12:4.", s=("G5069",))

# ------------------------------------------------------------------ cores e tecidos do culto
t("púrpura", r"púrpuras?", "tecido tingido de vermelho-arroxeado, caríssimo, usado por reis e ricos",
  "Lídia era vendedora de púrpura (Atos 16:14); os soldados vestiram Jesus de púrpura para zombar dele como rei "
  "(Marcos 15:17).", s=("H713", "G4209", "G4210"))
t("escarlate", r"escarlat[ae]s?|carmesi(?:m|ns)", "vermelho vivo; também o tecido tingido dessa cor",
  "Isaías 1:18 usa essa cor para os pecados que Deus promete tornar brancos como a neve.",
  s=("H8144", "H8438", "G2847"))
t("azul", r"azul", "aqui, a lã ou o fio tingido de azul-violeta, usado nas cortinas do tabernáculo e nas vestes "
  "do sumo sacerdote", "Êxodo 26:1; 28:31. Também as franjas das roupas levavam um cordão azul (Números 15:38).",
  s=("H8504",), exige=True)
t("véu", r"véus?", "a cortina que separava o Lugar Santo do Lugar Santíssimo",
  "Rasgou-se de alto a baixo na morte de Jesus: o caminho até Deus foi aberto (Mateus 27:51; Hebreus 10:19-20).",
  s=("H6532", "G2665"), exige=True)
t("apagadores", r"apagadores?", "os pratinhos onde se recolhiam os pavios queimados das lâmpadas do candelabro",
  "Êxodo 25:38.", s=("H4289",))
t("oferta alçada", r"(?:ofertas? )?alçadas?", "a parte da oferta separada (erguida) para Deus e entregue aos "
  "sacerdotes", s=("H8641",))
t("ofertas voluntárias", r"(?:ofertas? )?voluntárias?", "oferta dada por vontade própria, além do que a Lei exigia",
  "Levítico 7:16; Êxodo 35:29.", s=("H5071",), exige=True)
t("cheiro suave", r"(?:cheiro|aroma|perfume) suave", "expressão dos sacrifícios: oferta que agrada a Deus",
  "Paulo diz que Cristo se entregou por nós como oferta de cheiro suave (Efésios 5:2).", s=("H5207", "G2175"))
t("Azazel", r"azazel", "o bode 'por Azazel': no Dia da Expiação, levava simbolicamente os pecados do povo para o "
  "deserto", "Levítico 16:8-10, 20-22. O sentido do nome é discutido: talvez 'o bode que vai embora', ou um lugar "
  "no deserto.", s=("H5799",))
t("juízos", r"juízos", "as decisões justas de Deus: as normas da sua Lei; às vezes, os seus castigos",
  "No Egito, Deus libertou o seu povo 'com grandes juízos' (Êxodo 6:6).", s=("H4941", "H8201"), exige=True)
t("chifre", r"chifres?", "chifre; figurado, força e poder",
  "'Levantar o chifre' de alguém é dar-lhe vitória e honra (1 Samuel 2:1, 10; Salmo 18:2). Os 'chifres do altar' "
  "eram as pontas dos seus quatro cantos (Êxodo 27:2).", s=("H7161", "G2768"))

# ------------------------------------------------------------------ deuses dos povos vizinhos
t("Baal", r"baal(?!-)", "o principal deus dos cananeus, senhor da chuva e da fertilidade",
  "Seu culto, junto com o de Aserá, foi a grande tentação de Israel; Elias desafiou os profetas de Baal no "
  "Carmelo (1 Reis 18).", s=("H1168",), exige=True)
t("Astarote", r"astarotes?|astarte", "deusa cananeia da fertilidade e da guerra (a Astarte dos fenícios)",
  "Salomão seguiu Astarote, deusa dos sidônios (1 Reis 11:5).", s=("H6253",), exige=True)
t("Moloque", r"moloque", "deus a quem se ofereciam crianças queimadas no fogo",
  "A Lei proíbe esse culto com pena de morte (Levítico 18:21; 20:2-5); Josias profanou o lugar onde era feito "
  "(2 Reis 23:10).", s=("H4432", "G3434"))
t("Quemos", r"quemos|camos", "o deus dos moabitas", "1 Reis 11:7; Jeremias 48:7, 13.", s=("H3645",))
t("Milcom", r"milcom", "o deus dos amonitas", "1 Reis 11:5, 33.", s=("H4445",))
t("Dagom", r"dagom", "o deus dos filisteus",
  "Sua imagem caiu diante da arca de Deus (1 Samuel 5:1-5); Sansão derrubou o templo dele (Juízes 16:23-30).",
  s=("H1712",))
t("Tamuz", r"tamuz", "deus babilônico da vegetação, cuja morte era chorada todos os anos", "Ezequiel 8:14.",
  s=("H8542",))
t("Bel", r"(?-i:Bel)", "o principal deus da Babilônia (Marduque)", "Isaías 46:1; Jeremias 50:2.", s=("H1078",))
t("Nisroque", r"nisroque", "um deus da Assíria",
  "Senaqueribe foi morto pelos próprios filhos quando adorava no templo dele (2 Reis 19:37).", s=("H5268",))
t("Renfã", r"renfã", "nome de um deus-astro (talvez Saturno) adorado por Israel no deserto, segundo Estêvão",
  "Atos 7:43; Amós 5:26.", s=("G4481",))
t("Diana", r"diana|ártemis", "Ártemis, a deusa grega cujo grande templo ficava em Éfeso", "Atos 19:23-41.",
  s=("G735",))
t("Júpiter e Mercúrio", r"júpiter|mercúrio", "Zeus, o principal deus grego, e Hermes, seu mensageiro, chamados "
  "pelos nomes latinos", "Em Listra, o povo pensou que Barnabé e Paulo eram esses deuses (Atos 14:11-13).",
  s=("G2203", "G2060"))

# ------------------------------------------------------------------ meses do calendário hebraico
t("Abibe", r"abibe", "o primeiro mês do ano religioso (março–abril), o mês da Páscoa",
  "Depois do exílio passou a se chamar Nisã (Êxodo 13:4; Ester 3:7).", s=("H24",))
t("Nisã", r"nisã", "o primeiro mês do ano religioso (março–abril), o mês da Páscoa; antes, Abibe", s=("H5212",))
t("Sivã", r"sivã", "o terceiro mês (maio–junho)", s=("H5510",))
t("Elul", r"elul", "o sexto mês (agosto–setembro)", "Neemias 6:15.", s=("H435",))
t("Etanim", r"etanim", "o sétimo mês (setembro–outubro), o das festas do fim da colheita", "1 Reis 8:2.",
  s=("H388",))
t("Bul", r"(?-i:Bul)", "o oitavo mês (outubro–novembro)", "1 Reis 6:38.", s=("H945",))
t("Quisleu", r"quisleu", "o nono mês (novembro–dezembro)", s=("H3691",))
t("Tebete", r"tebete", "o décimo mês (dezembro–janeiro)", s=("H2887",))
t("Sebate", r"sebate", "o décimo primeiro mês (janeiro–fevereiro)", s=("H7627",))
t("Adar", r"adar", "o décimo segundo mês (fevereiro–março), o da festa de Purim", "Ester 3:7; 9:21.",
  s=("H143",), exige=True)

# ------------------------------------------------------------------ títulos e cargos
t("Faraó", r"faraó", "título dos reis do Egito, e não um nome próprio",
  "Em egípcio quer dizer 'casa grande', o palácio. Vários faraós diferentes aparecem na Bíblia.",
  s=("H6547", "G5328"))
t("Herodes", r"herodes", "nome de uma família de reis da Judeia sob o domínio de Roma",
  "Herodes, o Grande, mandou matar os meninos de Belém (Mateus 2:16); seu filho Herodes Antipas mandou matar João "
  "Batista e zombou de Jesus (Marcos 6:14-29; Lucas 23:7-12); seu neto Herodes Agripa matou Tiago e prendeu Pedro "
  "(Atos 12:1-4).", s=("G2264",))
t("Candace", r"candace", "título das rainhas da Etiópia (Núbia), e não um nome próprio", "Atos 8:27.",
  s=("G2582",))
t(None, r"rabsaqué|tartã|rabe-saris|rabe-mague",
  "título de alto oficial: Tartã é o comandante do exército; Rabe-Saris, o chefe dos oficiais da corte; Rabsaqué, "
  "um alto chefe que falava em nome do rei", "2 Reis 18:17-37; Jeremias 39:3.", s=("H7262", "H8661", "H7249"),
  id="oficiais-da-assiria")
t("príncipe", r"príncipes?", "chefe, líder, autoridade (não necessariamente filho de rei)",
  "Os 'príncipes' de Israel eram os chefes das tribos e dos clãs, e os do rei, os seus oficiais (Números 7:2; "
  "1 Reis 4:2). Jesus é o Príncipe da paz (Isaías 9:6).", s=("H8269", "H5387", "H5057", "H5081", "G758"))
t("arauto", r"arautos?", "mensageiro que anuncia em público as ordens do rei", "Daniel 3:4.", s=("H3744",))
t("escrivão", r"escrivão|escrivães", "secretário: o oficial que redigia e guardava os documentos do governo",
  s=("H5613", "H5608", "G1122"))
t("encantador", r"encantador(?:es)?|encantament\w+", "quem pratica magia com fórmulas e feitiços",
  "Os encantadores do Egito imitaram alguns sinais de Moisés (Êxodo 7:11, 22).",
  s=("H2748", "H2267", "H3909", "H3049", "H6049"))
t("tutor", r"tutor(?:es)?", "quem cuida e educa os filhos de outro até eles crescerem",
  "Paulo diz que a Lei foi como um tutor que nos conduziu até Cristo (Gálatas 3:24-25).",
  s=("G3807", "G2012", "H539"))
t("homem de Deus", r"homem de deus", "título do profeta, o homem enviado e usado por Deus",
  "Moisés, Elias e Eliseu são chamados assim (Deuteronômio 33:1; 2 Reis 4:9).", s=("H376",))
t("filhos dos profetas", r"filhos dos profetas", "os discípulos dos profetas, grupos que viviam e aprendiam com "
  "eles", "2 Reis 2:3-15; 4:38.", s=("H5030",))
t("o Pregador", r"pregador", "o título do autor de Eclesiastes (em hebraico, Coélet: 'o que fala à assembleia')",
  "Eclesiastes 1:1-2.", s=("H6953",), exige=True)

# ------------------------------------------------------------------ nomes e títulos de Deus e de Cristo
t("SENHOR dos exércitos", r"(?:senhor|deus) dos exércitos", "título de Deus como comandante dos exércitos do céu "
  "(os anjos e os astros) e do seu povo",
  "Davi enfrentou Golias em nome do SENHOR dos exércitos (1 Samuel 17:45).", s=("H6635",))
t("Altíssimo", r"altíssimo", "título de Deus: o que está acima de todos os deuses e de todos os reis",
  "Melquisedeque era sacerdote do Deus Altíssimo (Gênesis 14:18-20).", s=("H5945", "H5943", "G5310"), exige=True)
t("anjo do SENHOR", r"anjo do senhor", "o mensageiro especial de Deus, que fala como o próprio Deus",
  "Ele fala em primeira pessoa como o SENHOR (Gênesis 16:7-13; 22:11-18; Êxodo 3:2-6). Desde os primeiros "
  "cristãos, muitos viram nele uma aparição do Filho antes da encarnação.", s=("H4397", "G32"))
t("filho do homem", r"filhos? do homem", "ser humano, mortal",
  "É assim que Deus chama Ezequiel, lembrando a fragilidade do profeta diante da sua glória (Ezequiel 2:1).",
  s=("H120",), exige=True, id="filho-do-homem-mortal")
t("Filho do Homem", r"filho do homem", "o título que Jesus mais usou para si mesmo",
  "Vem de Daniel 7:13-14, em que 'um como filho do homem' recebe de Deus um reino eterno (Marcos 14:62).",
  s=("G444", "H606"), exige=True)
t("Filho de Davi", r"filho de davi", "título do Messias: o descendente prometido de Davi, que reinaria para sempre",
  "Os que pediam socorro a Jesus o chamavam assim (Mateus 9:27; 20:30; 2 Samuel 7:12-16).", s=("G1138",),
  exige=True)
t("Reino dos céus", r"reino dos céus", "o reino de Deus",
  "Mateus prefere dizer 'dos céus', como os judeus, que por respeito evitavam pronunciar o nome de Deus.",
  s=("G932", "G3772"))
t("Alfa e Ômega", r"alfa e (?:o )?ômega", "a primeira e a última letra do alfabeto grego: o começo e o fim de tudo",
  "Apocalipse 1:8; 21:6; 22:13.", s=("G1", "G5598"))
t("filha de Sião", r"(?:virgem )?filha de sião", "Jerusalém e o seu povo, retratados como uma moça",
  s=("H1323", "H6726"))
t("Sião", r"sião", "o monte de Jerusalém onde ficava a fortaleza de Davi e, depois, o templo",
  "Virou nome poético da própria Jerusalém e do povo de Deus; Hebreus 12:22 fala da Sião celestial.",
  s=("H6726", "G4622"))
t("Horebe", r"horebe", "outro nome do monte Sinai, 'o monte de Deus', onde ele deu a Lei",
  "Êxodo 3:1; Deuteronômio 5:2. Ali Elias também se encontrou com Deus (1 Reis 19:8).", s=("H2722",))

# ------------------------------------------------------------------ céu, abismo e fim dos tempos
t("firmamento", r"firmamento", "a abóbada do céu, que os antigos viam como uma cúpula firme sobre a terra",
  "Gênesis 1:6-8 conta como Deus a fez para separar as águas; o Salmo 19:1 diz que ela anuncia a obra das suas "
  "mãos.", s=("H7549",))
t("abismo (águas)", r"abismos?", "as águas profundas: o mar sem fundo, ou as águas debaixo da terra",
  "Gênesis 1:2; 7:11.", s=("H8415",), exige=True, id="abismo-aguas")
t("abismo", r"abismos?", "a prisão dos demônios e da besta",
  "Lucas 8:31; Apocalipse 9:1-2; 20:1-3.", s=("G12",), exige=True, id="abismo-prisao")
t("paraíso", r"paraíso", "'jardim', em persa: o lugar de descanso dos que morrem em Cristo, na presença de Deus",
  "Lucas 23:43; 2 Coríntios 12:4; Apocalipse 2:7.", s=("G3857",))
t("Armagedom", r"armagedom", "'monte de Megido', em hebraico: onde os reis da terra se reúnem para a batalha final",
  "Apocalipse 16:16. Megido foi palco de batalhas famosas (Juízes 5:19; 2 Reis 23:29).", s=("G717",))
t("Gogue e Magogue", r"(?<!, )gogue|magogue", "Gogue, da terra de Magogue: o chefe das nações que atacam o povo de Deus "
  "no fim", "Ezequiel 38–39; Apocalipse 20:8. Magogue também é o nome de um filho de Jafé (Gênesis 10:2).",
  s=("H1463", "H4031", "G1136", "G3098"))
t("dragão", r"dragões|dragão", "Satanás, a antiga serpente", "Apocalipse 12:9; 20:2.", s=("G1404",), exige=True)
t("besta", r"bestas?", "animal feroz; em Daniel e no Apocalipse, imagem dos impérios e poderes que se levantam "
  "contra Deus", "Daniel 7; Apocalipse 13.", s=("G2342", "H2423"))
t("principados", r"principados?", "poderes espirituais, anjos ou demônios, que exercem autoridade",
  "Romanos 8:38; Efésios 6:12; Colossenses 2:15.", s=("G746",))
t("livro da vida", r"livro da vida", "o registro de Deus com os nomes dos que pertencem a ele",
  "Filipenses 4:3; Apocalipse 20:12-15.", s=("G976", "G2222"))
t("dormir", r"dorm\w+", "dormir; no Novo Testamento, muitas vezes morrer, à espera da ressurreição",
  "João 11:11-14; 1 Tessalonicenses 4:13-15.", s=("G2837",), exige=True)

# ------------------------------------------------------------------ geografia
t("mar salgado", r"mar salgado", "o mar Morto",
  "É tão salgado que nele não há peixes; fica no ponto mais baixo da terra.", s=("H4417",))
t("mar de Quinerete", r"quinerete|genesaré|tiberíades", "o mar da Galileia (também chamado de Tiberíades)",
  s=("H3672", "G1082", "G5085"))
t("mar grande", r"mar grande", "o mar Mediterrâneo")
t("Arabá", r"arabá", "o vale seco que vai do mar da Galileia, ao longo do Jordão, até o golfo de Ácaba",
  s=("H6160",))
t("Padã-Arã", r"padã-arã", "a região da alta Mesopotâmia, em volta de Harã, onde vivia a família de Abraão",
  "Gênesis 25:20; 28:2.", s=("H6307",))
t("Ofir", r"ofir", "região famosa pelo ouro, de localização incerta (talvez no sul da Arábia ou na costa da "
  "África)", "1 Reis 9:28; 10:11.", s=("H211",))
t("Társis", r"társis", "cidade distante, no extremo oeste do Mediterrâneo, provavelmente na Espanha",
  "Jonas tentou fugir para lá (Jonas 1:3). Os 'navios de Társis' eram os grandes navios de longa viagem.",
  s=("H8659",))
t("Mizraim", r"mizraim", "o nome hebraico do Egito", "Gênesis 10:6, 13.", s=("H4714",))
t("Sinear", r"sinear", "a planície da Babilônia, na Mesopotâmia", "Gênesis 11:2.", s=("H8152",))
t("Javã", r"(?-i:Javã)", "a Grécia (os jônios); em Gênesis 10, o antepassado dos gregos", s=("H3120",))
t("Quitim", r"quitim", "Chipre e, depois, as terras do Mediterrâneo ocidental", s=("H3794",))

# ------------------------------------------------------------------ expressões
t("alma", r"almas?", "a pessoa, o ser vivo, a vida; também o íntimo, onde se sente e se deseja",
  "Na Bíblia hebraica a alma não é só uma parte de dentro: o homem 'foi feito alma vivente' (Gênesis 2:7), e "
  "'todas as almas da casa de Jacó' são todas as pessoas da família (Gênesis 46:27).", s=("H5315", "G5590"),
  exige=True)
t("toda carne", r"toda (?:a )?carne", "todos os seres vivos, sobretudo os seres humanos, em sua fraqueza",
  "Gênesis 6:12; Isaías 40:5-6; Joel 2:28.", s=("H1320",))
t(None, r"casa de (?:davi|israel|jacó|judá|josé|saul|acabe|jeroboão|levi|arão)",
  "a família, a descendência: 'casa de Davi' é a dinastia dele, e 'casa de Israel', o povo todo",
  "Deus prometeu a Davi uma 'casa', uma dinastia que duraria para sempre (2 Samuel 7:11-16).", s=("H1004", "G3624"),
  id="casa-de")
t("descansou com seus pais", r"descans\w+(?: [A-ZÀ-Ú][\wÀ-ÿ-]+)? com seus pais", "morreu",
  "Expressão comum nos livros dos Reis e das Crônicas: a morte descrita como descanso junto dos antepassados.",
  s=("H7901",))
t("caminho de toda a terra", r"caminho de toda a terra", "a morte, o caminho de todos os seres humanos",
  "Josué 23:14; 1 Reis 2:2.")
t("conhecer", r"conhec\w+(?=(?: de novo)?(?: [A-ZÀ-Ú][\wÀ-ÿ]+)? (?:a |à )?(?:sua mulher|homem|varão))",
  "aqui, ter relações sexuais com alguém", "É o modo hebraico de falar da união do casal (Gênesis 4:1).",
  s=("H3045", "G1097"), id="conhecer-intimo")
t("andar com Deus", r"and(?:ava|ou) com deus", "viver em comunhão com Deus, obedecendo a ele",
  "Enoque e Noé andavam com Deus (Gênesis 5:22-24; 6:9).", s=("H1980",))
t("buscar a face", r"busc\w+ (?:a )?(?:minha |tua |sua )?face", "procurar a presença de Deus, em oração e culto",
  "Salmo 27:8; 1 Crônicas 16:11.", s=("H6440",))
t("mão debaixo da coxa", r"debaixo d[ae] (?:minha |tua |sua )?coxa", "gesto de juramento solene",
  "Abraão pediu isso a seu servo, e Jacó a José (Gênesis 24:2, 9; 47:29).", s=("H3409",))
t("leite e mel", r"(?:que )?(?:mana|destila) leite e mel", "imagem da fartura da terra prometida",
  "Êxodo 3:8; 13:5.", s=("H2100",))
t("por amor de", r"por amor de", "por causa de, em consideração a",
  "Deus poupou o reino por amor de Davi, isto é, por causa da promessa feita a ele (1 Reis 11:12-13).",
  s=("H4616", "H5668"))
t("partir o pão", r"part(?:ir|iam|ia|indo|iu|imos) o pão", "comer juntos; em Atos, também celebrar a Ceia do Senhor",
  "Lucas 24:35; Atos 2:42, 46; 20:7.", s=("G2806",))
t("imposição das mãos", r"imposição das mãos|impor as mãos|imporem as mãos", "pôr as mãos sobre alguém para "
  "abençoar, curar ou enviar para um serviço", "Atos 6:6; 8:17-18; 1 Timóteo 4:14.", s=("G1936",))
t("sacudir o pó", r"sacudi\w* o pó", "gesto de rompimento com quem rejeita a mensagem",
  "Mateus 10:14; Atos 13:51.", s=("G1621",))
t("carne e sangue", r"carne e sangue", "o ser humano, com as suas limitações",
  "Mateus 16:17; 1 Coríntios 15:50; Efésios 6:12.", s=("G4561", "G129"))
t("olho mau", r"olho mau|mau olho", "avareza, mesquinhez; o contrário da generosidade",
  "Provérbios 28:22; Mateus 20:15.", s=("H7451", "G4190"))
t("estranho", r"estranh[oa]s?", "de fora: o estrangeiro, ou quem não pertence à família, ao sacerdócio ou ao povo",
  "Na Lei, 'estranho' é quem não é sacerdote (Êxodo 30:33); o 'fogo estranho' era um fogo que Deus não tinha "
  "ordenado (Levítico 10:1); em Provérbios, a 'mulher estranha' é a mulher de outro (Provérbios 2:16).",
  s=("H2114",), exige=True)
t("alheio", r"alhei[oa]s?", "de outro; 'deuses alheios' são os deuses dos outros povos",
  "Josué 24:20; Jeremias 7:6.", s=("H312", "H5236", "G245"))
t("perdição", r"perdição", "ruína, destruição; sobretudo a ruína eterna, a condenação",
  "Judas é chamado 'filho da perdição' (João 17:12).", s=("G684", "H6", "H343"))
t("possessão", r"possess(?:ão|ões)", "propriedade, o que se possui; sobretudo a terra dada por Deus",
  "Não tem o sentido de possessão por demônios: Abraão comprou um campo 'em possessão de sepultura' (Gênesis "
  "23:9, 20).", s=("H272", "H3425", "H4180"))

# ------------------------------------------------------------------ coisas e lugares (2)
t("carro", r"carros?", "carruagem puxada por animais; na guerra, o carro de combate, puxado por cavalos",
  "Os 'carros de ferro' dos cananeus eram a arma mais temida da época (Josué 17:16; Juízes 1:19).",
  s=("H7393", "H4818", "H5699", "G716"))
t("rolo", r"rolos?", "o livro antigo: folhas de couro ou de papiro costuradas e enroladas",
  "Jeremias 36; Salmo 40:7.", s=("H4039", "G975"), exige=True)
t("ferrolho", r"ferrolhos?", "a tranca que fecha a porta por dentro", s=("H1280",))
t("molho", r"(?-i:molhos?)(?= de)", "feixe, maço (e não o tempero!)", "Êxodo 12:22.", s=("H92",))
t("fluxo", r"fluxo", "corrimento, hemorragia",
  "Pela Lei, deixava a pessoa impura (Levítico 15). A mulher que tocou a roupa de Jesus sofria de um fluxo de "
  "sangue havia doze anos (Marcos 5:25-34).", s=("H2100", "H2101", "G4511"))
t("chuva temporã", r"temporãs?", "a das primeiras chuvas do outono, que amolecem a terra para semear",
  "A tardia é a da primavera, que enche o grão antes da colheita (Jeremias 5:24; Tiago 5:7).", s=("H3138",))
t("alva", r"(?-i:alva)", "o amanhecer, a primeira claridade do dia", "Gênesis 32:24.", s=("H7837",))
t("lavandeiro", r"lavandeiros?", "quem lavava e alvejava tecidos",
  "O 'campo do lavandeiro', fora de Jerusalém, era onde se estendiam os panos para secar (Isaías 7:3).",
  s=("H3526",))
t("açucena", r"açucenas?", "o lírio", s=("H7799",))
t("balaústres", r"balaústres?", "colunas de grade, corrimão (aqui, o sentido exato é incerto)", "1 Reis 10:12.",
  s=("H4552",))
t("lanceta", r"lancetas?", "lança pequena", s=("H7420",))
t("ascuas", r"ascuas?", "brasas; pedras quentes sobre as quais se assava o pão", "1 Reis 19:6.", s=("H7529",))
t("caibros", r"caibros?", "as vigas que sustentam o telhado", s=("H7351",))
t("sebe", r"sebes?", "cerca viva, feita de plantas e espinhos", s=("H7753", "G5418"))
t("monturo", r"monturos?", "monte de lixo e de esterco", s=("H5122", "H830"))
t("madrepérola", r"madrepérolas?", "a camada brilhante de dentro das conchas", s=("H1858",))
t("salitre", r"salitre|potassa", "mineral (soda) usado para lavar, como sabão",
  "Nem lavando-se com ele Israel tiraria a mancha do seu pecado (Jeremias 2:22).", s=("H5427", "H1287"))
t("malvas", r"malvas?", "erva salgada do deserto, comida dos mais pobres", "Jó 30:4.", s=("H4408",))
t("olmeiro", r"olmeiros?", "árvore grande e de boa sombra (no original, talvez outra árvore)",
  s=("H8410", "H424"))
t("cássia", r"cássia", "casca aromática, parecida com a canela", "Êxodo 30:24; Salmo 45:8.", s=("H6916",))
t("hena", r"(?-i:hena)", "arbusto de flores perfumadas; de suas folhas se faz a tinta de henna",
  "Cantares 1:14.", s=("H3724",), exige=True)
t("cardos", r"cardos?", "plantas espinhosas do campo",
  "Espinhos e cardos são sinal da terra amaldiçoada depois da queda (Gênesis 3:18).",
  s=("H1863", "H2336", "H8068"))
t("coelho", r"coelhos?", "aqui, o híraco (damão): pequeno mamífero que vive entre as rochas",
  "Salmo 104:18 o chama de morador das rochas.", s=("H8227",))
t("serpentes ardentes", r"serpentes? ardentes?", "serpentes venenosas, cuja mordida queimava",
  "No original, saraf, a mesma palavra de 'serafim' ('ardentes'). Os que olhavam para a serpente de bronze "
  "viviam; Jesus aplica a imagem a si mesmo (Números 21:6-9; João 3:14-15).", s=("H8314",))
t("orla", r"orlas?", "borda, beirada (de uma cortina ou de uma roupa)", s=("H7757", "H8193", "H7020", "G2899"))
t("escápula", r"escápulas?", "a omoplata, o osso das costas junto ao ombro", s=("H7929",))
t("zurrar", r"zurr\w+", "dar o grito do jumento", s=("H5101",))
t("manquejar", r"manquej\w+", "mancar; aqui, tropeçar", s=("H6761",))
t("alaúde", r"alaúdes?", "instrumento de cordas (no original, 'de dez cordas')", s=("H6218",))

# ------------------------------------------------------------------ palavras antigas ou literárias (2)
t("esquadrinhar", r"esquadrinh\w+", "examinar em detalhe, investigar a fundo", s=("H974", "H2713"))
t("admoestar", r"admoest\w+", "advertir, aconselhar com firmeza", s=("H2094", "G3560"))
t("pelejar", r"pelej\w+", "lutar, combater", s=("H3898",))
t("empalar", r"empal\w+", "executar alguém espetando-o numa estaca", s=("H2211",))
t("perjúrio", r"perjúrios?", "juramento falso", s=("H422",))
t("jota e til", r"jota|(?-i:til)", "as menores marcas da escrita: o jota é a menor letra do alfabeto hebraico, e o "
  "til, um pequeno traço que distingue uma letra de outra", "Mateus 5:18.", s=("G2503", "G2762"))
t("multiforme", r"multiforme", "variada, de muitas formas", "Efésios 3:10.", s=("G4182",))
t("cauterizada", r"cauteriz\w+", "marcada com ferro em brasa: insensível", "1 Timóteo 4:2.", s=("G2743",))
t("comichão", r"comichão", "coceira; 'ter comichão nos ouvidos' é querer ouvir só o que agrada",
  "2 Timóteo 4:3.", s=("G2833",))
t("incontaminado", r"incontaminad[oa]s?", "puro, sem mancha", s=("G283",))
t("concidadãos", r"concidadãos?", "cidadãos da mesma cidade", "Efésios 2:19.", s=("G4847",))
t("coerdeiros", r"coerdeir[oa]s?", "herdeiros junto com outro", "Romanos 8:17.", s=("G4789",))
t("superabundar", r"superabund\w+", "transbordar, sobrar com fartura", "Romanos 5:20.", s=("G5248", "G4052"))
t("lascívia", r"lascívi\w+|lascivamente", "sensualidade sem freio", s=("H2154",))
t("piedoso", r"piedos[oa]s?", "compassivo, misericordioso",
  "No Antigo Testamento, 'piedoso' é quem tem compaixão: Deus é misericordioso e piedoso (Êxodo 34:6).",
  s=("H2587",), exige=True)
t("equidade", r"equidade", "justiça imparcial, retidão", s=("H4339", "H3476"))

# ------------------------------------------------------------------ nomes que a própria Bíblia explica
t("Betel", r"betel", "'casa de Deus', em hebraico",
  "Ali Deus apareceu a Jacó em sonho (Gênesis 28:10-19). Depois, Jeroboão pôs na cidade um bezerro de ouro, e os "
  "profetas condenaram o santuário (1 Reis 12:28-29; Amós 4:4).", s=("H1008",))
t("Peniel", r"peniel|penuel", "'rosto de Deus', em hebraico: o lugar onde Jacó lutou com Deus",
  "Gênesis 32:24-31.", s=("H6439",))
t("Ebenézer", r"ebenézer", "'pedra de ajuda', em hebraico",
  "Samuel deu esse nome à pedra que levantou dizendo: até aqui nos ajudou o SENHOR (1 Samuel 7:12).", s=("H72",))
t("Massá e Meribá", r"massá|meribá", "'prova' e 'contenda': nomes do lugar onde Israel, reclamando água, pôs Deus "
  "à prova", "Êxodo 17:7; Números 20:13. O Salmo 95:8 relembra o episódio como advertência.",
  s=("H4532", "H4809"), exige=True)
t("Icabode", r"icabode", "'onde está a glória?', em hebraico",
  "A mãe deu esse nome ao menino quando a arca de Deus foi tomada pelos filisteus (1 Samuel 4:19-22).",
  s=("H350",))
t("Mara", r"(?-i:Mara)", "'amarga', em hebraico",
  "Nome do lugar das águas amargas que Deus tornou doces (Êxodo 15:23-25); Noemi pediu para ser chamada assim "
  "(Rute 1:20).", s=("H4785", "H4755"))
t("O SENHOR proverá", r"o senhor proverá", "o nome que Abraão deu ao monte onde Deus providenciou um carneiro no "
  "lugar de Isaque", "Gênesis 22:8-14.")
t("Babel", r"babel", "o nome hebraico da Babilônia; soa como o verbo 'confundir'",
  "Gênesis 11:9 explica o nome pela confusão das línguas.", s=("H894",))
t("Cefas", r"cefas", "'pedra', em aramaico: o nome que Jesus deu a Simão, o mesmo que Pedro (do grego petra)",
  "João 1:42; 1 Coríntios 1:12.", s=("G2786",))
t("Boanerges", r"boanerges", "'filhos do trovão': o apelido que Jesus deu a Tiago e João", "Marcos 3:17.",
  s=("G993",))
t("Dídimo", r"dídimo", "'gêmeo', em grego: o apelido de Tomé", "João 11:16; 20:24.", s=("G1324",))
t("Siloé", r"siloé", "'enviado': o tanque de Jerusalém onde Jesus mandou o cego se lavar",
  "João 9:7; Isaías 8:6.", s=("G4611", "H7975"))
t("Betesda", r"betesda", "tanque de Jerusalém, cercado de cinco alpendres, onde Jesus curou um paralítico",
  "João 5:2-9.", s=("G964",))
t("Aceldama", r"aceldama|hacéldama", "'campo de sangue', em aramaico", "Atos 1:19.", s=("G184",))
t("Decápolis", r"decápolis", "'dez cidades': região de cidades gregas a leste do Jordão",
  "Mateus 4:25; Marcos 5:20.", s=("G1179",))

# ------------------------------------------------------------------ culto e Lei (3)
t("escultura", r"esculturas?", "imagem esculpida para ser adorada: um ídolo",
  "O segundo mandamento proíbe fazer escultura para adorar (Êxodo 20:4; Deuteronômio 4:16).",
  s=("H6459", "H6456"), exige=True)
t("primogênito", r"primogênit[oa]s?", "o primeiro filho (ou a primeira cria)",
  "Os primogênitos de Israel pertenciam a Deus e eram resgatados, em memória da Páscoa no Egito (Êxodo 13:2, "
  "13-15).", s=("H1060", "H1067", "H1069"), exige=True)
t("consagração", r"consagraç(?:ão|ões)", "a cerimônia que instalava os sacerdotes no serviço",
  "Êxodo 29; Levítico 8. No original é o 'enchimento' das mãos: o sacerdote recebia nas mãos as porções do "
  "sacrifício.", s=("H4394",), exige=True)
t("descobrir a nudez", r"descobri\w* (?:a )?(?:sua |tua |a sua |a tua )?nudez",
  "ter relações sexuais (expressão da Lei para as uniões proibidas)", "Levítico 18 e 20.", s=("H6172",))
t("carpideiras", r"carpideiras?", "mulheres pagas para chorar e lamentar nos funerais", "Jeremias 9:17.",
  s=("H6969",))
t("maldizente", r"maldizentes?", "quem fala mal dos outros, injuria e difama", "1 Coríntios 5:11; 6:10.",
  s=("G3060",))
