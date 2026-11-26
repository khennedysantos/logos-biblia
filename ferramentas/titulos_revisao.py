"""Títulos do Easton (dicionário) e do Nave (temas) revisados à mão -> data/{dictionary,topics}/titulos_pt.json.

Os títulos antigos vieram do tradutor automático (Argos/NLLB), que traduzia nomes próprios como palavras comuns
("Shittim" -> "Merda", "Beer-sheba" -> "Cerveja-Sheba", "Job, Book of" -> "Trabalho, Livro de", "Thummim" ->
"Polegar") ou deixava o inglês pela metade ("Esther, Livro de", "Bill Of Divórcio"). Em nov/2026 o Google mostrou
uma dessas páginas no Search Console, e a lista foi revista na sessão do agente (sem API): os nomes seguem a grafia
da Bíblia Livre (conferida no texto dela pelo --conferir) e os livros, os nomes de books.json.

O endereço da página sai do título, então trocar o título troca o endereço (o antigo deixa de existir).
Também refaz as remissões do Nave ("See SHITTIM" -> "Veja SITIM"), que usam o título em maiúsculas.

uso:  python3 ferramentas/titulos_revisao.py              (aplica; idempotente)
      python3 ferramentas/titulos_revisao.py --conferir   (mostra as palavras dos títulos novos que não estão na Bíblia Livre)
depois: python3 ferramentas/gerar_paginas.py"""
import glob, json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"

DICIONARIO = {
    "Abba": "Aba", "Adam, the city of": "Adã, a cidade", "Adria": "Adriático", "Amana": "Amaná",
    "Amplias": "Amplíato", "Anem": "Aném", "Appii Forum": "Praça de Ápio", "Ashurites": "Assuri",
    "Ass": "Jumento", "Augustus band": "Esquadrão imperial", "Baalath-beer": "Baalate-Beer",
    "Babylon, kingdom of": "Babilônia, reino da", "Baptism, Christian": "Batismo cristão",
    "Baptism, John's": "Batismo de João", "Bath-rabbim": "Bate-Rabim", "Beer": "Beer", "Beer-elim": "Beer-Elim",
    "Beer-lahai-roi": "Beer-Laai-Roi", "Beeroth of the children of Jaakan": "Beerote dos filhos de Jaacã",
    "Beth-car": "Bete-Car", "Beth-shemesh": "Bete-Semes", "Beth-tappuah": "Bete-Tapua",
    "Caesara Philippi": "Cesareia de Filipe", "Canaan, the language of": "Canaã, a língua de",
    "Castor and Pollux": "Castor e Pólux", "Cleopas": "Cleofas", "Cock-crowing": "Canto do galo",
    "Coele-Syria": "Celessíria", "Corinthians, First Epistle to the": "Coríntios, Primeira Epístola aos",
    "Crisping-pin": "Alfinete de frisar", "Dagon's house": "Casa de Dagom", "Dale, the king's": "Vale do Rei",
    "David, City of": "Davi, Cidade de", "Doleful creatures": "Criaturas lúgubres", "Dung": "Esterco",
    "Dung-gate": "Porta do Esterco", "Dung-hill": "Monturo", "Dwell": "Habitar",
    "Ephraim in the wilderness": "Efraim, junto ao deserto", "Ephraim, Gate of": "Efraim, Porta de",
    "Ephraim, The tribe of": "Efraim, tribo de", "Ephraim, Wood of": "Efraim, Bosque de",
    "Esther, Book of": "Ester, Livro de", "Ezekiel, Book of": "Ezequiel, Livro de", "Fair Havens": "Bons Portos",
    "Fallow-ground": "Terra por lavrar", "Festus, Porcius": "Festo, Pórcio", "Fining pot": "Crisol",
    "Fuller's field": "Campo do Lavandeiro", "Fuller's soap": "Sabão de lavandeiro",
    "Gibeah of Judah": "Gibeá de Judá", "Gibeah of Phinehas": "Gibeá de Fineias",
    "Gilead, Balm of": "Gileade, Bálsamo de", "Gimzo": "Ginzo", "Grace, means of": "Graça, meios de",
    "Hadad-rimmon": "Hadade-Rimom", "Harosheth of the Gentiles": "Harosete dos Gentios",
    "Hermonites, the": "Hermonitas", "Herod Arippa II.": "Herodes Agripa II",
    "Isaiah, The Book of": "Isaías, Livro de", "Italian band": "Esquadrão Italiano", "Jachin and Boaz": "Jaquim e Boaz",
    "Jacob's Well": "Poço de Jacó", "James, Epistle of": "Tiago, Epístola de", "Jehonadab": "Jonadabe",
    "Jehovah-shalom": "Jeová-Shalom", "Jeremiah, Book of": "Jeremias, Livro de",
    "John, First Epistle of": "João, Primeira Epístola de", "John, Second Epistle of": "João, Segunda Epístola de",
    "John, Third Epistle of": "João, Terceira Epístola de", "Joshua, The Book of": "Josué, Livro de",
    "Judah upon Jordan": "Judá junto ao Jordão", "Judah, Kingdom of": "Judá, Reino de", "Judah, Tribe of": "Judá, tribo de",
    "Jude, Epistle of": "Judas, Epístola de", "Kneading-trough": "Amassadeira", "Lign-aloes": "Aloés (árvore)",
    "Luke, Gospel according to": "Lucas, Evangelho segundo", "Maaleh-acrabbim": "Subida de Acrabim",
    "Micah, Book of": "Miqueias, Livro de", "Moreh, the Hill of": "Moré, Colina de", "Moresheth-gath": "Moresete-Gate",
    "Music, Instrumental": "Música instrumental", "Nahum, Book of": "Naum, Livro de", "Naphtali, Mount": "Naftali, Monte de",
    "Nimrim, Waters of": "Ninrim, Águas de", "Obadiah, Book of": "Obadias, Livro de", "Olves, Mount of": "Oliveiras, Monte das",
    "Oreb, The rock of": "Orebe, Rocha de", "Peter, First Epistle of": "Pedro, Primeira Epístola de",
    "Peter, Second Epistle of": "Pedro, Segunda Epístola de", "Philemon, Epistle to": "Filemom, Epístola a",
    "Porch, Solomon's": "Pórtico de Salomão", "Porcius Festus": "Pórcio Festo", "Potters field": "Campo do Oleiro",
    "Put, Phut": "Pute", "Ramath of the south": "Ramá do sul", "Reuben, Tribe of": "Rúben, tribo de",
    "Ruth The Book of": "Rute, Livro de", "Seething pot": "Panela fervente", "Serpent, Fiery": "Serpente ardente",
    "Shalim, Land of": "Saalim, Terra de", "Shalisha, Land of": "Salisa, Terra de",
    "Shallecheth, The gate of": "Salequete, Porta de", "Shaveh, Valley of": "Savé, Vale de",
    "Shiloah, The waters of": "Siloé, Águas de", "Shinar, The Land of": "Sinear, Terra de",
    "Shittah-tree": "Acácia (sitim)", "Shittim": "Sitim", "Shrines, Silver": "Nichos de prata",
    "Shual, The land of": "Sual, Terra de", "Siddim, Vale of": "Sidim, Vale de", "Siloah, The pool of": "Siloé, Tanque de",
    "Siloam, Tower of": "Siloé, Torre de", "Simeon, The tribe of": "Simeão, tribo de",
    "Solomon, Song of": "Cantares de Salomão", "Teil tree": "Terebinto", "Thyine wood": "Madeira de tuia",
    "Tiglath-Pileser I.": "Tiglate-Pileser I", "Tiglath-Pileser III.": "Tiglate-Pileser III",
    "Timothy, First Epistle to": "Timóteo, Primeira Epístola a", "Timothy, Second Epistle to": "Timóteo, Segunda Epístola a",
    "Titus, Epistle to": "Tito, Epístola a", "Tryphena and Tryphosa": "Trifena e Trifosa",
    "Tyropoeon Valley": "Vale do Tiropeão", "Vaticanus, Codex": "Códice Vaticano", "Works, Covenant of": "Obras, Pacto das",
    "Works, Good": "Boas obras", "Yoke-fellow": "Companheiro de jugo", "Zaanaim": "Zaanim",
    "Zebulun, Lot of": "Zebulom, Herança de", "Zebulun, Tribe of": "Zebulom, tribo de",
    "Zophim, Field of": "Zofim, Campo de", "Zuph, Land of": "Zufe, Terra de",
    # nomes de lugar fora da grafia da Bíblia Livre (data/places.json) ou traduzidos como palavra comum
    "Accad": "Acade", "Addar": "Adar", "Addon": "Adom", "Anathoth": "Anatote", "Areopagus": "Areópago", "Asshur": "Assur",
    "Beautiful gate": "Porta Formosa", "Canneh": "Cané", "Chorazin": "Corazim", "East": "Oriente", "East gate": "Porta Oriental",
    "Gibeon": "Gibeão", "Heres": "Heres", "Ibleam": "Ibleão", "Kittim": "Quitim", "Madmen": "Madmém", "Mesha": "Messa",
    "Metheg-ammah": "Metegue-Amá", "Mitylene": "Mitilene", "Pharpar": "Farpar", "Pi-beseth": "Pibesete",
    "Pirathon": "Piratom", "Ptolemais": "Ptolemaida", "Resen": "Resém", "Sepharad": "Sefarade", "Shepham": "Sefã",
    "Shimron": "Sinrom", "Shimron-meron": "Sinrom-Merom", "Suphah": "Sufa", "Trachonitis": "Traconites",
    "Trogyllium": "Trogílio", "Zalmonah": "Zalmona", "Zarephath": "Sarepta", "Zephath": "Zefate",
    "Job, Book of": "Jó, Livro de", "Heled": "Helede", "Piram": "Pirã", "Sechu": "Secu",
    "Solomon's Porch": "Pórtico de Salomão", "Stream of Egypt": "Ribeiro do Egito", "Thummim": "Tumim",
    "Christs, False": "Cristos, falsos", "Musician, Chief": "Mestre de canto",
    "Ephesians, Epistle to": "Efésios, Epístola aos", "Galatians, Epistle to": "Gálatas, Epístola aos",
    "Hebrews, Epistle to": "Hebreus, Epístola aos", "Philippians, Epistle to": "Filipenses, Epístola aos",
    "Hosea, Prophecies of": "Oseias, Profecias de", "Temple, Herod's": "Templo de Herodes",
}

TEMAS = {
    "ABBA": "Aba", "AGENCY, FREE MORAL": "Livre-arbítrio", "ANGEL (Holy Trinity)": "Anjo (Santa Trindade)",
    "ANGEL (a spirit)": "Anjo (um espírito)", "APPII-FORUM": "Praça de Ápio", "AQUILA AND PRISCILLA": "Áquila e Priscila",
    "ASHURITES": "Assuri", "BABES": "Criancinhas", "BASHAN-HAVOTH-JAIR": "Basã-Havote-Jair", "BEER": "Beer",
    "BEER-ELIM": "Beer-Elim", "BEER-LAHAI-ROI": "Beer-Laai-Roi", "BEER-SHEBA": "Berseba", "BETH-SHEMESH": "Bete-Semes",
    "BETH-SHITTAH": "Bete-Sita", "BETH-TAPPUAH": "Bete-Tapua", "BILL OF DIVORCE": "Carta de divórcio",
    "BURNING BUSH": "Sarça ardente", "CAESAREA PHILIPPI": "Cesareia de Filipe", "CASTOR AND POLLUX": "Castor e Pólux",
    "CIVIL DAMAGES": "Danos civis", "CLEOPAS": "Cleofas", "COL-HOZEH": "Col-Hozé", "CONDEMNATION, SELF": "Autocondenação",
    "CRISPING PINS": "Alfinetes de frisar", "DELUSION, SELF": "Autoengano", "DOVE, TURTLE": "Rola",
    "EQUITY (FAIRNESS)": "Equidade (justiça)", "EVIL-MERODACH": "Evil-Merodaque", "FAIR HAVENS": "Bons Portos",
    "FULLER'S FIELD": "Campo do Lavandeiro", "GILOH": "Gilo", "GIMZO": "Ginzo", "GNASHING OF TEETH": "Ranger de dentes",
    "GOLDEN CANDLESTICK": "Candelabro de ouro", "GOPHER WOOD": "Madeira de gofer", "HALF-HOMER": "Meio-hômer",
    "HALHUL": "Halul", "HORSE-LEECH": "Sanguessuga", "JEHONADAB": "Jonadabe", "JEHOVAH-JIREH": "Jeová-Jiré",
    "JUDGMENT-HALL": "Pretório", "JUDGMENT-SEAT": "Tribunal", "KINE (BOVINE)": "Vacas (gado)", "KING'S DALE": "Vale do Rei",
    "KNEADING-TROUGH": "Amassadeira", "LEAVEN (YEAST)": "Fermento", "LUKEWARMNESS": "Mornidão",
    "MAALEH-ACRABBIM": "Subida de Acrabim", "MERCY-SEAT": "Propiciatório", "MOTE (A SPECK)": "Cisco (argueiro)",
    "MURRAIN (A DISEASE OF LIVESTOCK)": "Peste do gado", "OLIVES, MOUNT OF": "Oliveiras, Monte das", "OSEE": "Oseias",
    "PARSIMONY (STINGINESS)": "Mesquinhez", "PENURIOUSNESS (STINGINESS)": "Avareza (sovinice)",
    "PERFIDY (TREACHERY)": "Perfídia (traição)", "PINNACLE (WING)": "Pináculo",
    "PRODIGALITY (WAYWARDNESS)": "Prodigalidade (desperdício)", "RAIMENT (CLOTHING)": "Vestes",
    "SABBATH DAY' S JOURNEY": "Caminho de um sábado", "SELF-DENIAL": "Abnegação", "SERAPHIM (SERAPHS)": "Serafins",
    "SHEWBREAD (SHOWBREAD)": "Pães da proposição", "SHITTIM": "Sitim", "STAVES (LONG POLES)": "Varas",
    "STIFF-NECKED": "Dura cerviz", "STOOL": "Assento", "SURETY (GUARANTEE)": "Fiança (garantia)",
    "SYRIA-MAACHAH": "Síria de Maaca", "TONGUES (the gift)": "Línguas (o dom)", "UZZEN-SHERAH": "Uzém-Seerá",
    "WINEBIBBER (A WINO)": "Beberrão", "WORKS": "Obras", "ZACCHAEUS (ZACCHEUS)": "Zaqueu",
    "ZACHARIAS (ZECHARIAH)": "Zacarias", "ZEAL, RELIGIOUS": "Zelo religioso",
    "ACCAD": "Acade", "ANATHOTH": "Anatote", "AREOPAGUS": "Areópago", "ARPAD": "Arpade", "ASSHUR": "Assur",
    "CANNEH": "Cané", "CHORAZIN": "Corazim", "ELTOLAD": "Eltolade", "EZEM": "Ezém", "FISH GATE": "Porta do Peixe",
    "GIBEON": "Gibeão", "HERES": "Heres", "IBLEAM": "Ibleão", "LASHARON": "Lasarom", "MESHA": "Messa",
    "MITYLENE": "Mitilene", "PHARPAR": "Farpar", "PI-BESETH": "Pibesete", "PIRATHON": "Piratom", "PTOLEMAIS": "Ptolemaida",
    "PUT": "Pute", "SEPHARAD": "Sefarade", "SHEEP GATE": "Porta das Ovelhas", "SHINAR": "Sinear",
    "TRACHONITIS": "Traconites", "TROGYLLIUM": "Trogílio", "ZAREPHATH": "Sarepta", "ZEPHATH": "Zefate",
    "AVITES": "Aveus", "CHOOSING": "Escolha", "COZ": "Coz", "HUSHAM": "Husão", "IRI": "Iri", "LETUSHIM": "Letusim",
    "PUDENS": "Pudente", "SHOPHACH": "Sofaque", "SOLOMON'S PORCH": "Pórtico de Salomão", "THUMMIM": "Tumim",
    "URIM AND THUMMIM": "Urim e Tumim",
}

# palavras comuns traduzidas no sentido errado ("Dumb" -> "Burro", "Oil" -> "Petróleo", "Fast" -> "Rápido") ou ao pé da letra
DICIONARIO.update({
    "Abraham's bosom": "Seio de Abraão", "Anger": "Ira", "Apparel": "Vestuário", "Armour-bearer": "Escudeiro",
    "Armoury": "Arsenal", "Artificer": "Artífice", "Artillery": "Armas", "Assurance": "Certeza", "Babe": "Criancinha",
    "Bake": "Assar", "Balance": "Balança", "Bands": "Laços", "Bar": "Ferrolho", "Bath": "Bato", "Battering-ram": "Aríete",
    "Battle-axe": "Machado de guerra", "Battlement": "Parapeito", "Bay tree": "Loureiro", "Beaten oil": "Azeite batido",
    "Bed-chamber": "Quarto de dormir", "Beeves": "Bois", "Beg": "Mendigar", "Betroth": "Desposar", "Bless": "Abençoar",
    "Bloody sweat": "Suor de sangue", "Boil": "Úlcera", "Bosses": "Bossas do escudo", "Bottle": "Odre", "Bow": "Arco",
    "Bowels": "Entranhas", "Bowing": "Inclinar-se", "Bravery": "Enfeites", "Breach": "Brecha", "Breastplate": "Peitoral",
    "Bribe": "Suborno", "Bruit": "Rumor", "Bunch": "Molho", "Burden": "Fardo", "Burial": "Sepultamento",
    "Burnt offering": "Holocausto", "By-word": "Motivo de escárnio", "Cab": "Cabo (medida)", "Call": "Chamado",
    "Calling": "Vocação", "Carriage": "Bagagem", "Cart": "Carroça", "Casement": "Janela gradeada", "Cattle": "Gado",
    "Cauls": "Coifas", "Chaldee language": "Língua caldeia", "Chambering": "Devassidão", "Changes of raiment": "Mudas de roupa",
    "Charger": "Prato", "Charmer": "Encantador", "Chest": "Arca", "Chestnut tree": "Castanheiro", "Chief priest": "Sumo sacerdote",
    "Churl": "Avarento", "Closet": "Quarto", "Coat": "Túnica", "Coat of mail": "Cota de malha", "Collection": "Coleta",
    "College": "Segundo bairro", "Confection": "Composição aromática", "Confectionaries": "Perfumistas",
    "Contentment": "Contentamento", "Conversation": "Procedimento", "Corn": "Cereal", "Couch": "Leito",
    "Counsellor": "Conselheiro", "Courses": "Turnos", "Court": "Átrio", "Covetousness": "Cobiça", "Cup-bearer": "Copeiro",
    "Custom": "Tributo", "Cutting": "Incisões na carne", "Damnation": "Condenação", "Darling": "Minha única",
    "Day's journey": "Jornada de um dia", "Dayspring": "Aurora", "Deal, Tenth": "Décima parte", "Deep": "Abismo",
    "Degrees, Song of": "Cânticos dos degraus", "Deputy": "Procônsul", "Devil": "Diabo", "Dial": "Relógio de sol",
    "Dine": "Jantar", "Divination": "Adivinhação", "Dog": "Cão", "Door-posts": "Umbrais", "Dove's dung": "Esterco de pomba",
    "Dragon well": "Fonte do Dragão", "Draught-house": "Latrina", "Drawer of water": "Tirador de água", "Dream": "Sonho",
    "Drink": "Bebida", "Drink, strong": "Bebida forte", "Drink-offering": "Libação", "Dumb": "Mudo", "Earing": "Aradura",
    "East sea": "Mar Oriental", "East, Children of the": "Filhos do Oriente", "Effectual call": "Vocação eficaz",
    "Elect lady": "Senhora eleita", "Engines": "Máquinas de guerra", "Ensign": "Estandarte", "Entertain": "Hospedar",
    "Evening": "Tarde", "Everlasting": "Eterno", "Evil-speaking": "Maledicência", "Exercise, bodily": "Exercício físico",
    "Fan": "Pá de joeirar", "Fast": "Jejum", "Fat": "Gordura", "Father": "Pai", "Fatling": "Animal cevado",
    "Fear of the Lord the": "Temor do Senhor", "Fellowship": "Comunhão", "Fenced cities": "Cidades fortificadas",
    "Ferry boat": "Barca", "Festivals, Religious": "Festas religiosas", "Finer": "Refinador", "Fire": "Fogo",
    "First-fruits": "Primícias", "Fish-hooks": "Anzóis", "Fish-pools": "Viveiros de peixes", "Fishing, the art of": "Pesca",
    "Fleece": "Velo", "Fly": "Mosca", "Fold": "Aprisco", "Footstool": "Escabelo", "Forehead": "Testa",
    "Foreknowledge of God": "Presciência de Deus", "Forgiveness of sin": "Perdão dos pecados",
    "Free-will offering": "Oferta voluntária",
    "Fulness": "Plenitude", "Furrow": "Sulco", "Gallows": "Forca", "Gate": "Porta", "Ghost": "Espírito", "Gift": "Dádiva",
    "Gifts, spiritual": "Dons espirituais", "Godliness": "Piedade", "Golden calf": "Bezerro de ouro",
    "Goodness": "Bondade", "Goodly trees": "Árvores formosas", "Grass": "Erva", "Hail": "Granizo", "Halt": "Coxo",
    "Handbreadth": "Palmo", "Handwriting": "Escrito de dívida", "Hanging": "Enforcamento", "Head-bands": "Faixas da cabeça",
    "Head-dress": "Turbante", "Heave offering": "Oferta alçada", "Help-meet": "Auxiliadora", "Helps": "Socorros",
    "Hireling": "Assalariado", "Hold": "Fortaleza", "Holy place": "Lugar santo", "Honey": "Mel",
    "Horse-gate": "Porta dos Cavalos", "Horse-leech": "Sanguessuga", "Hose": "Calções", "Husbandman": "Lavrador",
    "Imagery": "Câmaras de imagens", "Jaw-bone": "Queixada", "Jealousy offering": "Oferta de ciúmes",
    "Jehovah-jireh": "Jeová-Jiré", "Jephthah's vow": "Voto de Jefté", "Judgment hall": "Pretório",
    "Judgment seat": "Tribunal", "Judgment, The final": "Juízo final", "Judgments of God": "Juízos de Deus",
    "Kid": "Cabrito", "Kingly office of Christ": "Ofício real de Cristo", "Kings, The Books of": "Reis, Livros de",
    "Kir of Moab": "Quir de Moabe", "Knead": "Amassar", "Knock": "Bater", "Lawyer": "Intérprete da lei",
    "League": "Aliança", "Left-handed": "Canhoto", "Levirate Law": "Lei do levirato", "Lewdness": "Lascívia",
    "Lie": "Mentira", "Lime": "Cal", "Lock": "Fechadura", "Lodge": "Choça", "Log": "Logue", "Lord's Prayer": "Pai-Nosso",
    "Magistrate": "Magistrado", "Mail, Coat of": "Cota de malha", "Main-sail": "Vela da proa", "Man": "Homem",
    "Manslayer": "Homicida", "Meat-offering": "Oferta de manjares", "Millet": "Painço", "Mincing": "Andar afetado",
    "Mine": "Mina", "Minstrel": "Tangedor", "Mite": "Lepto", "Money-changer": "Cambista", "Moth": "Traça", "Mourn": "Luto",
    "Murmuring": "Murmuração", "Muzzle": "Açaimar", "Naked": "Nu", "Naughty figs": "Figos ruins",
    "New Moon, Feast of": "Lua Nova, Festa da", "Nose-jewels": "Joias do nariz", "Numbering of the people": "Recenseamento do povo",
    "Obeisance": "Reverência", "Oil": "Azeite", "Oil-tree": "Oleastro", "Ointment": "Unguento", "Old gate": "Porta Velha",
    "Onycha": "Ônica", "Paran, Mount": "Parã, Monte", "Parlour": "Sala", "Pillar": "Coluna", "Plain": "Planície",
    "Plane tree": "Plátano", "Pledge": "Penhor", "Pool": "Tanque", "Pools of Solomon": "Tanques de Salomão",
    "Post": "Correio", "Potsherd": "Caco de barro", "Proportion of faith": "Proporção da fé", "Pulse": "Legumes",
    "Ranges": "Fogareiros", "Recorder": "Cronista", "Rent": "Rasgo", "Rereward": "Retaguarda", "Rest": "Descanso",
    "Revelation": "Revelação", "Roll": "Rolo", "Rudder bands": "Amarras do leme", "Sabbath day's journey": "Caminho de um sábado",
    "Sackcloth": "Pano de saco", "Sardine stone": "Sárdio", "Schoolmaster": "Aio", "Scourging": "Açoite",
    "Sea, The": "Mar", "Sea, The molten": "Mar de fundição", "Servitor": "Servo", "Shearing-house": "Casa da tosquia",
    "Sheep-fold": "Aprisco", "Sheep-gate": "Porta das Ovelhas", "Sheriffs": "Magistrados", "Sickle": "Foice",
    "Sin, Wilderness of": "Sim, Deserto de", "Sin-offering": "Oferta pelo pecado", "Sitting": "Assentar-se",
    "Skin, Coats made of": "Túnicas de pele", "Skull, The place of a": "Caveira, Lugar da", "Slime": "Betume",
    "Songs": "Cânticos", "Spirit, Holy": "Espírito Santo", "Spring": "Fonte", "Star, Morning": "Estrela da manhã",
    "Stealing": "Furto", "Stomacher": "Corpete", "Stones, Precious": "Pedras preciosas", "Salt, The city of": "Cidade do Sal",
    "Salt, Valley of": "Vale do Sal",
    "Stranger": "Estrangeiro", "Stripes": "Açoites", "Suburbs": "Arredores", "Supper": "Ceia", "Swallow": "Andorinha",
    "Swine": "Porcos", "Tabering": "Tamborilar", "Tables": "Tábuas", "Tackling": "Cordame", "Tale": "Conta", "Tares": "Joio",
    "Target": "Escudo", "Taverns, The three": "Três Tavernas", "Taxing": "Recenseamento", "Temple, the Second": "Segundo Templo",
    "Tenth deal": "Décima parte", "Testimony, Tabernacle of": "Tabernáculo do Testemunho",
    "Thessalonians, Epistles to the": "Tessalonicenses, Epístolas aos", "Thieves, The two": "Dois ladrões",
    "Thorn in the flesh": "Espinho na carne", "Threshing": "Debulha", "Tinkling ornaments": "Enfeites tilintantes",
    "Tires": "Turbantes", "Tob, The land of": "Tobe, Terra de", "Tob-adonijah": "Tobe-Adonias", "Toll": "Imposto",
    "Tongues, Gift of": "Línguas, Dom de", "Tow": "Estopa", "Trespass offering": "Oferta pela culpa", "Trumpets": "Trombetas",
    "Trumpets, Feast of": "Trombetas, Festa das", "Vagabond": "Errante", "Wages": "Salário", "Wagon": "Carroça",
    "Wailing-place, Jews'": "Muro das Lamentações", "Wandering": "Peregrinação no deserto",
    "Wars of the Lord, The Book of the": "Guerras do Senhor, Livro das", "Washing": "Lavagem", "Watches": "Vigílias",
    "Watchings": "Vigílias", "Waterspouts": "Cataratas", "Wave offerings": "Ofertas movidas", "Weeks, Feast of": "Semanas, Festa das",
    "Well": "Poço", "Wine-press": "Lagar", "Winefat": "Lagar", "Wise, wisdom": "Sábio, sabedoria", "Wise men": "Magos",
    "Witch": "Feiticeira", "Witchcraft": "Feitiçaria", "Word, The": "Verbo, o", "Writing": "Escrita",
})
TEMAS.update({
    "ABSTINENCE, TOTAL": "Abstinência total", "ACCUSATION, FALSE": "Acusação falsa", "ACTIONS AT LAW": "Processos judiciais",
    "ADJUDICATION AT LAW": "Julgamento judicial", "AGE, OLD": "Velhice", "AGED": "Idosos", "AFFLICTED": "Aflitos",
    "ANGER": "Ira", "ARMS": "Armas", "ASSAULT AND BATTERY": "Agressão física", "ASSURANCE": "Certeza",
    "BACKBITING": "Maledicência", "BATH": "Bato", "BATTERING-RAM": "Aríete", "BATTLE-AX": "Machado de guerra",
    "BATTLEMENTS": "Parapeitos", "BEATEN WORK": "Obra batida", "BEATING": "Espancamento", "BEAUTY AND BANDS": "Formosura e Laços",
    "BELIEVING": "Crer", "BITTER HERBS": "Ervas amargas", "BLASTING": "Crestamento", "BOASTING": "Jactância", "BOIL": "Úlcera",
    "BOILING POT": "Panela fervente", "BORING THE EAR": "Furar a orelha", "BOTCH": "Úlcera maligna", "BOTTLE": "Odre",
    "BOW": "Arco", "BOWELS": "Entranhas", "BOWING": "Inclinar-se", "BOX TREE": "Buxo", "BRASS": "Bronze",
    "BRAZEN SEA": "Mar de bronze", "BRAZEN SERPENT": "Serpente de bronze", "BREATH": "Fôlego", "BREASTPLATE": "Peitoral",
    "BROTHERLY KINDNESS": "Amor fraternal", "BURDEN": "Fardo", "BURIAL": "Sepultamento", "BURNING": "Queima",
    "BURNT OFFERING": "Holocausto", "BUSYBODY": "Intrometido", "CAB": "Cabo (medida)", "CALL": "Chamado",
    "CAPITAL PUNISHMENT": "Pena de morte", "CARNAL MINDEDNESS": "Mentalidade carnal", "CART": "Carroça", "CARVING": "Entalhe",
    "CASTING": "Fundição", "CATTLE": "Gado", "CHARGE": "Encargo", "CHARGER": "Prato",
    "CHARMERS AND CHARMING": "Encantadores e encantamentos", "CHEERFULNESS": "Alegria", "CHEST": "Arca",
    "CHESTNUT TREE": "Castanheiro", "CHOSEN, OR ELECTED": "Escolhidos ou eleitos", "CIVIL SERVICE": "Serviço público",
    "CLEANSING": "Purificação", "CLOSET": "Quarto", "COAT OF MAIL": "Cota de malha", "COLLECTION": "Coleta",
    "COLLEGE": "Segundo bairro", "COMPLAINT": "Queixa", "CONCEIT": "Presunção", "CONDESCENSION OF GOD": "Condescendência de Deus",
    "CONSUMPTION": "Tísica", "CONTEMPT OF COURT": "Desacato ao tribunal", "CONTENTION": "Contenda", "CONTENTMENT": "Contentamento",
    "CONVERSATION": "Procedimento", "CORN": "Cereal", "CORPORAL PUNISHMENT": "Castigo corporal", "COUNSEL": "Conselho",
    "COUNSELLOR": "Conselheiro", "COUNTENANCE": "Semblante", "COVETOUSNESS": "Cobiça", "CREEPING THINGS": "Répteis",
    "CRITICISM, UNJUST": "Crítica injusta", "CROSS-QUESTIONING": "Interrogatório", "CUPBEARER": "Copeiro", "CURSING": "Maldição",
    "CUTTING": "Incisões na carne", "DAILY OFFERING": "Oferta diária", "DAMNED": "Condenados", "DANCING": "Dança",
    "DEAD (PEOPLE)": "Mortos", "DECEIT": "Engano", "DECREES, DIVINE": "Decretos divinos", "DELIVERANCE": "Livramento",
    "DENYING JESUS": "Negação de Jesus", "DEPUTY": "Procônsul", "DERISION": "Escárnio", "DEVIL": "Diabo",
    "DIAL": "Relógio de sol", "DITCH": "Vala", "DIVINATION": "Adivinhação", "DOER": "Praticantes",
    "DOG (SODOMITE?)": "Cão (sodomita?)", "DOUBTING": "Dúvida", "DREAM": "Sonho", "DRINK": "Bebida",
    "DRINK OFFERING": "Libação", "DRIVING": "Condução de carros",
    "DRUNKENNESS": "Embriaguez", "DUKE": "Príncipe", "DUMB (DEAFNESS, MUTE)": "Mudez (surdez)", "DUTY (TAX)": "Imposto",
    "DYING": "Moribundos", "EAST SEA": "Mar Oriental", "EAST WIND": "Vento oriental", "ENQUIRING OF GOD": "Consultar a Deus",
    "ENSIGN": "Estandarte", "EQUALITY, OF MEN": "Igualdade dos homens", "ESCAPE": "Fuga", "ESTATE": "Propriedades",
    "ETERNAL PUNISHMENT": "Castigo eterno", "EVERLASTING PUNISHMENT": "Castigo eterno", "EVIL": "Mal",
    "EVIL FOR GOOD": "Mal por bem", "EVIL SPEAKING": "Maledicência", "EXCHANGERS": "Cambistas", "EYELIDS": "Pálpebras",
    "FALSE ACCUSATION": "Acusação falsa", "FALSE TEACHERS": "Falsos mestres", "FAN": "Pá de joeirar", "FAT": "Gordura",
    "FATHER": "Pai", "FATHER-IN-LAW": "Sogro", "FATHERLESS": "Órfãos", "FATTED CALF": "Novilho cevado",
    "FAULT FINDING": "Censura", "FELLOWSHIP": "Comunhão", "FETTERS": "Grilhões", "FIGHT OF FAITH": "Combate da fé",
    "FILE": "Lima", "FINE": "Multa", "FIRE": "Fogo", "FIRST FRUITS": "Primícias", "FIRSTLING": "Primeiras crias",
    "FISH SPEAR": "Arpão", "FLATTERY": "Bajulação", "FLY": "Mosca", "FOOTSTOOL": "Escabelo",
    "FORGETTING GOD": "Esquecer-se de Deus", "FORTUNE TELLING": "Adivinhação", "FORTUNE, CHANGES OF": "Reveses da sorte",
    "FREE-WILL OFFERINGS": "Ofertas voluntárias", "FRUIT TREES": "Árvores frutíferas", "FUTURE PUNISHMENT": "Castigo futuro",
    "GALLOWS": "Forca", "GENTLENESS": "Mansidão", "GHOST": "Espírito", "GIFTS FROM GOD": "Dádivas de Deus",
    "GIVING": "Contribuição", "GLEANING": "Respiga", "GLORIFYING GOD": "Glorificar a Deus", "GODLINESS": "Piedade",
    "GODLY": "Piedosos", "GOLDEN ALTAR": "Altar de ouro", "GOOD AND EVIL": "Bem e mal", "GOOD FOR EVIL": "Bem por mal",
    "GRASS": "Erva", "GROUND": "Solo", "HAIL": "Granizo", "HANDBREADTH": "Palmo", "HANGING": "Enforcamento",
    "HANGINGS": "Cortinas", "HASTE": "Pressa", "HAUGHTINESS": "Altivez", "HEADBANDS": "Faixas da cabeça",
    "HEARERS": "Ouvintes", "HEAVE OFFERING": "Oferta alçada", "HEDGE": "Sebe", "HIRE": "Salário", "HIRELING": "Assalariado",
    "HOLY PLACE": "Lugar santo", "HONEY": "Mel", "HUMILIATION AND SELF-AFFLICTION": "Humilhação e aflição de si mesmo",
    "HUSBANDMAN": "Lavrador", "HUSBANDRY": "Agricultura", "I AM THAT I AM": "Eu Sou o que Sou",
    "IMPORTUNITY": "Insistência", "INGATHERING, FEAST OF": "Colheita, Festa da", "INTOLERANCE, RELIGIOUS": "Intolerância religiosa",
    "ISH-BOSHETH": "Is-Bosete", "ISRAEL, PROPHECIES CONCERNING": "Israel, profecias sobre", "ISSUE OF BLOOD": "Fluxo de sangue",
    "JAILER (JAILOR)": "Carcereiro", "JEWELS": "Joias", "JUDGING": "Julgar", "JUDGMENTS": "Juízos",
    "LACHRYMATORY (TEAR BOTTLE)": "Lacrimatório (vaso de lágrimas)", "LANDMARKS": "Marcos (divisas)",
    "LASCIVIOUSNESS": "Lascívia", "LAWYER": "Intérprete da lei", "LAYING ON OF HANDS": "Imposição de mãos", "LEAGUE": "Aliança",
    "LEARNING": "Saber", "LEFT-HANDED": "Canhoto", "LIME": "Cal", "LOAVES": "Pães", "LOCK": "Fechadura", "LOG": "Logue",
    "LONGSUFFERING": "Longanimidade", "LOOKING-GLASS": "Espelho", "LORD'S DAY": "Dia do Senhor", "LORD'S PRAYER": "Pai-Nosso",
    "LORD'S SUPPER": "Ceia do Senhor", "LOST, THE": "Perdidos", "LOT, THE": "Sortes", "LYING": "Mentira",
    "MAGISTRATE": "Magistrado", "MAIL": "Correspondência", "MALFEASANCE IN OFFICE": "Abuso no cargo", "MAN": "Homem",
    "MANSLAYER": "Homicida", "MARINERS (SAILORS)": "Marinheiros", "MASTER WORKMAN": "Mestre de obras",
    "MEAT OFFERING": "Oferta de manjares", "MEDDLING": "Intromissão", "MILLET": "Painço", "MINCING": "Andar afetado",
    "MINORITY REPORT": "Parecer da minoria", "MOCKING": "Zombaria", "MONEY CHANGERS": "Cambistas", "MOTH": "Traça",
    "MULBERRY TREE": "Amoreira", "MURMURING": "Murmuração", "NEEDLEWORK": "Bordado", "NIGHT": "Noite", "NURSE": "Ama",
    "OBJECT TEACHING": "Ensino por objetos",
    "OCCULT SCIENCE": "Ciências ocultas", "OIL": "Azeite", "OINTMENT": "Unguento", "ONYCHA": "Ônica",
    "OPINION, PUBLIC": "Opinião pública", "ORDINANCE": "Ordenança", "PEACE OFFERINGS": "Ofertas pacíficas", "PEN": "Pena",
    "PEOPLE, COMMON": "Povo comum", "PERSONAL CALL": "Chamado pessoal", "PIECE OF SILVER": "Peça de prata",
    "PILLAR": "Coluna", "PIN": "Estaca", "PITY": "Compaixão", "PLEDGE": "Penhor", "PLUMMET": "Prumo",
    "POLL TAX": "Imposto por cabeça", "POOL": "Tanque", "PORCH": "Pórtico", "POST": "Correio", "POTSHERD": "Caco de barro",
    "PULSE": "Legumes", "QUICKENING": "Vivificação", "RAISING": "Ressurreição de mortos", "READING": "Leitura",
    "RECORDER": "Cronista", "RECREATION (REST)": "Recreação (descanso)", "RELEASE": "Remissão", "RENDING": "Rasgar as vestes",
    "RESPECT OF PERSONS": "Acepção de pessoas", "RESPONSIVE RELIGIOUS SERVICE": "Culto responsivo", "REST": "Descanso",
    "REVELATION": "Revelação", "RICH, THE": "Ricos", "RICHES": "Riquezas", "RISING": "Levantar cedo", "ROLL": "Rolo",
    "SACKCLOTH": "Pano de saco", "SAVIOUR (SAVIOR)": "Salvador", "SAW": "Serra", "SCALES": "Escamas e balanças",
    "SCALL": "Tinha", "SCEPTER (SCEPTRE)": "Cetro", "SCOURGING": "Açoite", "SCRIBE (S)": "Escribas", "SCRIPTURES": "Escrituras",
    "SCURVY": "Sarna", "SELF-CONDEMNATION": "Autocondenação", "SELF-CONFIDENCE": "Autoconfiança",
    "SELF-DECEPTION": "Autoengano", "SELF-DELUSION": "Autoilusão", "SELF-EXALTATION": "Autoexaltação",
    "SELF-EXAMINATION": "Autoexame", "SELF-INCRIMINATION": "Autoincriminação", "SELF-INDULGENCE": "Autoindulgência",
    "SELF-RIGHTEOUSNESS": "Justiça própria", "SELF-WILL": "Vontade própria", "SHEET": "Lençol", "SHOUTING": "Gritos",
    "SICK, THE": "Doentes", "SICKLE": "Foice", "SIGN": "Sinal", "SIN MONEY": "Dinheiro pelo pecado", "SINGING": "Canto",
    "SLEEP": "Sono", "SLIME": "Betume", "SMITING": "Golpes", "SON-IN-LAW": "Genro", "SOUNDING": "Sondagem", "SPEAKING": "Fala",
    "SPINDLE": "Fuso", "SPITTING": "Cuspir", "SPOONS": "Colheres", "STALL": "Estábulo", "STAMMERING": "Gagueira",
    "STANDARD": "Estandarte", "STEALING": "Furto", "STEWARD": "Mordomo", "STOCKS": "Tronco", "STOMACHER": "Corpete",
    "STOREHOUSES": "Celeiros", "STRAIGHT": "Direita (rua)", "STRAIT GATE": "Porta estreita", "STRANGERS": "Estrangeiros",
    "STRANGLED": "Animais sufocados", "STRIPES": "Açoites", "STUMBLING": "Tropeço", "SUBURBS": "Arredores",
    "SUPERSCRIPTION (INSCRIPTION)": "Inscrição", "SUPPER": "Ceia", "SURFEITING": "Glutonaria", "SWALLOW": "Andorinha",
    "SWEARING": "Juramentos", "SWEAT": "Suor", "SWEET INCENSE": "Incenso aromático", "SWINE": "Porcos",
    "TABERNACLES, FEAST OF": "Tabernáculos, Festa dos", "TALKING": "Conversa", "TARES": "Joio", "TARGET": "Escudo",
    "TASTE": "Paladar", "TEACHERS": "Mestres", "TEACHING": "Ensino", "TEIL TREE": "Terebinto", "TEMPER": "Temperamento",
    "THANK OFFERINGS": "Ofertas de gratidão", "THANKFULNESS": "Gratidão", "THRESHING": "Debulha", "THYINE": "Tuia",
    "TIRE": "Turbante", "TITLE, TO REAL ESTATE": "Título de propriedade", "TOE": "Dedo do pé", "TOLL": "Imposto",
    "TOW": "Estopa", "TRADE": "Comércio", "TRESPASS": "Transgressão", "TROUBLE": "Aflição", "TRUMPET": "Trombeta",
    "TRUMPETS": "Trombetas", "TURTLEDOVE": "Rola", "UNCLEANNESS": "Impureza",
    "UNICORN (WILD OX, R. V.)": "Unicórnio (boi selvagem, R. V.)", "UPRIGHTNESS": "Retidão", "VESTMENTS": "Vestes sacerdotais",
    "VINEYARD": "Vinha", "VIRGINITY": "Virgindade", "WAGES": "Salário", "WAGON": "Carroça", "WAILING": "Lamento",
    "WAITING": "Espera", "WALKING": "Andar", "WALLS, OF THE CITIES": "Muros das cidades", "WASHING": "Lavagem",
    "WATCH": "Vigília", "WAY": "Caminho", "WEALTH": "Riqueza", "WEEPING": "Choro", "WHIRLWIND": "Redemoinho",
    "WHISPER": "Sussurro", "WHISPERER": "Mexeriqueiro", "WHORE": "Prostituta", "WHOREDOM": "Prostituição",
    "WHOREMONGER": "Devasso", "WICKED (PEOPLE)": "Ímpios", "WINE PRESS": "Lagar", "WITCHCRAFT": "Feitiçaria",
    "WRITING": "Escrita",
    # títulos que não são palavras da King James (conceitos do Nave, termos técnicos do Easton)
    "ARCHERY": "Arqueiros", "ARKITES": "Arqueus", "ARMOR-BEARER": "Escudeiro", "ARREST": "Prisão (detenção)",
    "AVARICE": "Avareza", "BACKSLIDERS": "Desviados", "BATTERY": "Agressão", "BEHEADING": "Decapitação",
    "BENEDICTIONS": "Bênçãos", "BEQUESTS": "Legados", "BEREAVEMENT": "Luto (perda)", "BETTING": "Apostas",
    "BIGOTRY": "Fanatismo", "BORROWING": "Empréstimo", "BOSS": "Bossa do escudo", "BURGLARY": "Arrombamento",
    "CELLAR": "Adega", "CHEATING": "Trapaça", "CHEMARIM": "Quemarim", "CHILDLESSNESS": "Falta de filhos", "CHORUSES": "Coros",
    "CLERGYMAN": "Clérigo", "COLOSSE (COLOSSAE)": "Colossos", "COMPASSES": "Compasso", "COMPROMISE": "Acordo",
    "CONCUBINAGE": "Concubinato", "CONFECTIONER": "Perfumista", "CONSCIENTIOUSNESS": "Escrúpulo",
    "CONVEYANCE": "Transferência de terras", "CORNERSTONE": "Pedra angular", "CRIMINATION": "Incriminação",
    "CUPIDITY": "Cobiça", "DAMAGES AND COMPENSATION": "Danos e indenização", "DATE": "Tâmara", "DECEPTION": "Engano",
    "DEFILEMENT": "Contaminação", "DESIGN": "Desígnio", "DISCOURAGEMENT": "Desânimo", "DISSEMBLING": "Dissimulação",
    "EARTHENWARE": "Louça de barro", "ECCLESIASTICISM": "Eclesiasticismo", "ELECTIONEERING": "Campanha eleitoral",
    "ENGINE": "Máquina de guerra", "ENGRAFTING": "Enxerto", "EXPEDIENCY": "Conveniência", "EXPOSTULATION": "Admoestação",
    "FESTIVALS": "Festas", "FICKLENESS": "Inconstância", "FINGERBREADTH": "Dedo (medida)", "FISHPOOL": "Viveiro de peixes",
    "FITCH": "Ervilhaca", "FOUNDING": "Fundição", "GENERALS, DISTINGUISHED": "Generais ilustres", "GODLESSNESS": "Impiedade",
    "GOUT (?)": "Gota (?)", "GRANDFATHER": "Avô", "GRATITUDE": "Gratidão", "HARLOTRY": "Prostituição",
    "HOLIDAY": "Dia de festa", "HOMICIDE": "Homicídio", "HYBRIDIZING": "Hibridação", "IFS, OF THE BIBLE": "Condicionais da Bíblia",
    "INGRAFTING": "Enxerto", "INHOSPITABLENESS": "Falta de hospitalidade", "INTOXICANTS": "Bebidas embriagantes",
    "INTOXICATION": "Embriaguez", "INVECTIVE": "Invectiva", "LAMENESS": "Coxeadura", "LARCENY": "Furto",
    "LENDING": "Empréstimo", "LICENTIOUSNESS": "Libertinagem", "LITIGATION": "Litígio", "LITTER": "Liteira",
    "LIVERY": "Libré (uniforme)", "LOVEFEASTS": "Ágapes", "MALINGERING": "Simulação de doença", "MASKING": "Disfarce",
    "MECHANIC": "Artesão", "MOWING": "Ceifa", "MUSTER": "Alistamento", "NEOPHYTES": "Neófitos", "NO": "Nô",
    "NONCONFORMITY": "Inconformismo", "OFFENSES": "Ofensas", "ON": "Om", "OVERCOMING": "Vencer",
    "PACK ANIMALS": "Animais de carga", "PARLOR": "Sala", "PAWN": "Penhor", "PENALTY": "Pena", "PENITENCE": "Penitência",
    "PICTURE": "Pintura", "PLANE": "Plaina", "PLEADING": "Súplica", "PRAYERFULNESS": "Vida de oração",
    "PRAYERLESSNESS": "Falta de oração", "PROBATION": "Provação", "PROFANITY": "Linguagem profana",
    "PROTRACTED MEETINGS": "Reuniões prolongadas", "RAVISHMENT": "Violação", "READINGS, SELECT": "Leituras selecionadas",
    "RECONNOISSANCE": "Reconhecimento militar", "REGICIDE": "Regicídio", "REVILING": "Injúria", "REVIVALS": "Avivamentos",
    "SCYTHIANS": "Citas", "SECRETARY (RECORDIST)": "Secretário (cronista)", "SHERIFF": "Magistrado",
    "SINLESSNESS": "Impecabilidade", "SPELT": "Espelta", "SPINNING": "Fiação", "STEADFASTNESS": "Firmeza",
    "SUBJECTS": "Súditos", "SUING": "Processos", "SWADDLE": "Faixas de criança", "TANTALIZING": "Provocação",
    "TECHNICALITIES": "Formalidades", "THADDAEUS": "Tadeu", "TOLERATION": "Tolerância", "TRAFFIC": "Comércio",
    "TRAMP": "Andarilho", "TRUSTEE": "Administrador", "UNCHARITABLENESS": "Falta de caridade", "UNFAITHFULNESS": "Infidelidade",
    "UNFRUITFULNESS": "Infrutuosidade", "WATCHFULNESS": "Vigilância", "WEEDING": "Capina", "WILLFULNESS": "Obstinação",
    "WRESTLING": "Luta", "ZECHARIAH (ZECHARIAS)": "Zacarias", "ALPHEUS (ALPHAEUS)": "Alfeu", "ARCHELAUS (ARCHAELAUS)": "Arquelau",
    "BARTIMEUS (BARTIMAEUS)": "Bartimeu", "ALLOY, OF METALS": "Liga de metais", "APOSTROPHE": "Apóstrofe",
    "PELETHITES": "Peleteus", "UZZIEL": "Uziel",
})
DICIONARIO.update({
    "Adam, a type": "Adão, um tipo", "Backbite": "Difamar", "Backslide": "Desviar-se", "Behead": "Decapitar", "Bench": "Banco",
    "By": "Por (sentido antigo)", "Cellar": "Adega", "Colossians, Epistle to the": "Colossenses, Epístola aos",
    "Corinthians, Second Epistle to the": "Coríntios, Segunda Epístola aos", "Date": "Tâmara", "Dye": "Tingir",
    "Espouse": "Desposar", "Ezra, Book of": "Esdras, Livro de", "Hinge": "Gonzo", "Idumaea": "Idumeia",
    "Libertine": "Libertos", "Litter": "Liteira", "Mount": "Monte", "Mount of beatitudes": "Monte das Bem-Aventuranças",
    "Mowing": "Ceifa", "No": "Nô", "On": "Om", "Potipherah": "Potífera", "Quarantania": "Quarentana (monte)",
    "Quotations": "Citações", "Romans, Epistle to the": "Romanos, Epístola aos", "Sergeants": "Oficiais de justiça",
    "Sermon on the mount": "Sermão do Monte", "So": "Sô", "Stater": "Estáter", "Subscriptions": "Notas finais das epístolas",
    "Tablet": "Tábua", "Thaddaeus": "Tadeu", "Transfiguration, the": "Transfiguração", "Wean": "Desmamar",
    "Jehovah-shammah": "Jeová-Samá", "Pelethites": "Peleteus", "Uzziel": "Uziel", "Archevite": "Arquevitas",
    "Jehovah-tsidkenu": "Jeová-Tsidquenu", "Lieutenant": "Sátrapas", "Milaiai": "Milalai",
})

TIPOS = {"dictionary": DICIONARIO, "topics": TEMAS}


def gravar(p, d):
    p.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def conferir():
    voc = set()
    for f in glob.glob(str(DATA / "bibles" / "blivre" / "*.json")):
        for c in json.loads(Path(f).read_text(encoding="utf-8")):
            for v in c:
                voc.update(w.lower() for w in re.findall(r"\w+", v))
    for tipo, corr in TIPOS.items():
        titulos = json.loads((DATA / tipo / "titulos_pt.json").read_text(encoding="utf-8"))
        for en, pt in corr.items():
            if en not in titulos:
                print(f"{tipo}: {en!r} não existe no titulos_pt.json")
            fora = [w for w in re.findall(r"\w+", pt) if w.lower() not in voc]
            if fora:
                print(f"{tipo}: {en} -> {pt}   fora da Bíblia Livre: {fora}")


def aplicar():
    for tipo, corr in TIPOS.items():
        p = DATA / tipo / "titulos_pt.json"
        titulos = json.loads(p.read_text(encoding="utf-8"))
        mudou = {en: pt for en, pt in corr.items() if en in titulos and titulos[en] != pt}
        titulos.update(mudou)
        gravar(p, titulos)
        print(f"{tipo}: {len(mudou)} títulos trocados")
    # remissões do Nave: a linha "-See X" (inglês) vira "-Veja <título de X em maiúsculas>"
    titulos = json.loads((DATA / "topics" / "titulos_pt.json").read_text(encoding="utf-8"))
    n = 0
    for f in sorted((DATA / "topics").glob("[A-Z].json")):
        en, ppt = json.loads(f.read_text(encoding="utf-8")), DATA / "topics" / "pt" / f.name
        pt = json.loads(ppt.read_text(encoding="utf-8"))
        for chave, linhas in en.items():
            for i, linha in enumerate(linhas):
                m = re.fullmatch(r"(-?)See ([A-Z][A-Z ,'()\-]+?)\.?", linha.strip())
                if not m or chave not in pt or i >= len(pt[chave]) or m.group(2) not in TEMAS:
                    continue
                nova = f"{m.group(1)}Veja {titulos[m.group(2)].upper()}"
                if pt[chave][i] != nova:
                    pt[chave][i], n = nova, n + 1
        gravar(ppt, pt)
    print(f"temas: {n} remissões refeitas")


if __name__ == "__main__":
    conferir() if "--conferir" in sys.argv else aplicar()
