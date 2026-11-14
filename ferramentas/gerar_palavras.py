"""Palavras-chave sublinhadas no texto (data/palavras/).

No capítulo, algumas palavras da Bíblia Livre aparecem sublinhadas; um toque abre um cartão com a palavra
original (hebraico ou grego), a tradução e uma nota curta dizendo por que ela pesa ali.

Tudo o que o site mostra sai deste arquivo, escrito à mão:

  lema("H1254", "criar", r"cri[aeo]\\w*", "nota geral da palavra")
      Número de Strong, tradução curta, as formas que a Bíblia Livre usa (expressão regular, sem diferença
      de maiúsculas) e a nota. Com nota, a palavra é sublinhada na PRIMEIRA vez em que aparece em cada
      capítulo (para não encher o texto de sublinhados). Sem nota, só onde houver um contexto() para ela.

  contexto("PSA.51.10", "H1254", "nota deste versículo")
      Nota própria daquele versículo: sempre sublinha, e no cartão vem antes da nota geral.
      n=2 escolhe a segunda vez em que a palavra aparece no versículo; formas= troca a expressão regular.

O script acha a palavra original no interlinear (data/interlinear) e a correspondente em português no
texto da Bíblia Livre. Se o número de Strong não estiver no versículo, ou a forma em português não for
encontrada, o contexto() é recusado com erro: é a proteção contra número ou referência errados.

Saída: data/palavras/indice.json (as palavras originais e as notas gerais) e data/palavras/{LIVRO}.json
(capítulo → versículo → [início, fim, strong, nota de contexto]; início e fim contam caracteres do
versículo na Bíblia Livre). Rode de novo sempre que mexer aqui ou no texto da Bíblia Livre.

uso:  python3 ferramentas/gerar_palavras.py              (grava data/palavras/)
      python3 ferramentas/gerar_palavras.py --relatorio   (não grava; mostra a cobertura de cada palavra)
"""
import collections, json, re, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
SAIDA = DATA / "palavras"
MAX_POR_VERSO = 5

LEMAS, CONTEXTOS = {}, {}


def lema(strong, pt, formas, nota=None):
    assert strong not in LEMAS, f"{strong} repetido"
    LEMAS[strong] = {"pt": pt, "formas": formas, "nota": nota}


def contexto(ref, strong, nota, n=1, formas=None):
    assert (ref, strong, n) not in CONTEXTOS, f"{ref} {strong} repetido"
    CONTEXTOS[(ref, strong, n)] = {"nota": nota, "formas": formas}


# =====================================================================================================
# ANTIGO TESTAMENTO — palavras com nota geral
# =====================================================================================================
lema("H1254", "criar", r"(?!crian)cri[aeo]\w*|criei",
     "No sentido de criar, este verbo só tem Deus como sujeito em toda a Bíblia hebraica: ninguém mais “bara”. "
     "Descreve o que só ele faz surgir — o universo, um povo, um coração novo.")
lema("H2617", "amor leal, bondade", r"bondades?|misericórdias?|benignidades?|benevolências?|beneficências?|piedade|lealdade|fidelidade|favor|amor",
     "Hesed: mais que um sentimento, é o amor fiel de quem se comprometeu por aliança e não volta atrás. "
     "Nenhuma palavra do português cobre tudo; por isso aparece como bondade, misericórdia ou benignidade.")
lema("H3722", "fazer expiação", r"expiaç\w+|expi\w+|reconcili\w+|propici\w+|perdo\w+|purific\w+|apazigu\w+|aplac\w+",
     "Cobrir a culpa pagando o preço que afasta a ira. É o verbo do Dia da Expiação (Levítico 16): "
     "o pecado não é ignorado; é tratado por um sacrifício no lugar do culpado.")
lema("H3727", "propiciatório", r"propiciatório|tampa|cobertura|coberta",
     "A tampa de ouro da arca, onde o sangue era aspergido uma vez por ano. Romanos 3:25 usa a palavra grega "
     "correspondente para Cristo: ele é o lugar onde Deus e o pecador se encontram.")
lema("H1285", "aliança", r"alianças?|pactos?|concertos?|acordos?",
     "Compromisso solene que cria um vínculo, com promessas e obrigações. A história bíblica se organiza em "
     "torno das alianças de Deus: com Noé, Abraão, Israel, Davi — e a nova aliança.")
lema("H1350", "resgatar (como parente próximo)", r"redentor\w*|remi\w+|redim\w+|resgat\w+|libert\w+|vingador\w*|parente\w*",
     "O resgatador era o parente próximo com o dever de comprar de volta a terra ou a liberdade de um familiar e "
     "de defender a sua causa (Levítico 25; Rute). Quando Deus recebe esse nome, apresenta-se como o parente que "
     "assume a dívida do seu povo.")
lema("H6299", "resgatar", r"resgat\w+|remi\w+|redim\w+|livr\w+|libert\w+",
     "Libertar pagando um preço. É um dos verbos do êxodo: Deus resgatou Israel da escravidão, e o povo "
     "resgatado passa a pertencer a quem o resgatou.")
lema("H3444", "salvação", r"salvaç(?:ão|ões)|livramentos?|socorro|vitórias?",
     "Yeshuá. Da mesma raiz vem o nome Josué — em grego, Jesus: “o SENHOR salva” (Mateus 1:21).")
lema("H4899", "ungido", r"ungid\w+|messias",
     "Mashiach: rei ou sacerdote separado com óleo para uma missão. É a palavra que deu “Messias”; "
     "em grego, “Cristo”.")
lema("H6918", "santo", r"sant\w+",
     "Separado, à parte de tudo o que é comum. Dito de Deus, aponta para a sua pureza e para a distância "
     "infinita entre ele e as criaturas; dito do povo, para alguém reservado para ele.")
lema("H6588", "transgressão, rebelião", r"transgress\w+|rebeli\w+|prevaricaç\w+|delitos?|ofensas?|crimes?",
     "Não é um deslize: é revolta contra uma autoridade legítima, como a de um súdito que rompe com o seu rei.")
lema("H5771", "iniquidade, culpa", r"iniquidades?|maldades?|perversidades?|culpas?|castigos?|delitos?",
     "Da ideia de torto, desviado. A mesma palavra nomeia o pecado, a culpa que ele gera e o castigo que ele "
     "merece — por isso alguém pode “levar a iniquidade” de outro (Isaías 53:6).")
lema("H5162", "arrepender-se; consolar", r"arrepend\w+|consol\w+|compadec\w+|confort\w+",
     "Suspirar fundo: conforme o contexto, consolar ou mudar de atitude. Quando se diz que Deus “se arrepende”, "
     "o texto descreve em linguagem humana a mudança no seu trato com as pessoas, não um erro seu (Números 23:19).")
lema("H7356", "compaixão", r"misericórdias?|compaix\w+|piedade|ternuras?|entranhas",
     "Plural de “ventre materno”: a compaixão que uma mãe sente pelo filho que gerou.")
lema("H2580", "graça, favor", r"graças?|favor\w*|agrado",
     "Favor que não é devido. “Achar graça aos olhos” de alguém é ser bem recebido sem ter como exigir isso.")
lema("H8451", "lei, instrução", r"leis?|instruç\w+|ensino\w*|doutrinas?",
     "Torá. Vem de “apontar, ensinar”: mais que um código, é a instrução de um pai. Pode indicar um "
     "mandamento, os cinco livros de Moisés ou toda a Escritura.")
lema("H835", "bem-aventurado", r"bem-aventurad\w+|feliz|felizes|ditos\w+",
     "Uma exclamação: “como é feliz!”. Abre o livro dos Salmos e descreve quem está no caminho certo diante "
     "de Deus, não quem apenas se sente bem.")
lema("H6754", "imagem", r"imagem|imagens|estátuas?|figuras?",
     "Estátua ou figura que representa alguém. Em Gênesis, o ser humano é posto na criação como a imagem de "
     "Deus — seu representante, como as estátuas que os reis antigos erguiam nos territórios que governavam.")
lema("H3374", "temor", r"temor\w*|reverência",
     "Não é pavor: é a reverência de quem leva Deus a sério — sabe quem ele é e vive de acordo. "
     "Provérbios o chama de princípio da sabedoria.")
lema("H1892", "vapor, vaidade", r"vaidades?|futilidades?|inutilidades?|fútil|fúteis|sopro|vapor|vão|vã|vãos|vãs|ilus\w+",
     "Literalmente vapor, sopro: o que não se consegue segurar. Eclesiastes usa a palavra dezenas de vezes "
     "para a vida “debaixo do sol”: passageira e impossível de controlar.")
lema("H7585", "Sheol, o mundo dos mortos", r"xeol|sheol|seol|sepulturas?|sepulcros?|infernos?|cova|abismo|mundo dos mortos",
     "O lugar dos mortos, para onde todos descem. Conforme a tradução aparece como sepultura, inferno ou "
     "Xeol; no Antigo Testamento ainda não é o “inferno” no sentido de castigo final.")
lema("H6453", "Páscoa", r"páscoas?",
     "De “passar por cima”: o SENHOR poupou as casas marcadas com o sangue do cordeiro (Êxodo 12). "
     "O Novo Testamento chama Cristo de “nossa páscoa” (1 Coríntios 5:7).")

# ----- só onde houver nota de contexto -----
lema("H7225", "princípio", r"princípio|começo|primícias?")
lema("H430", "Deus", r"deus(?:es)?")
lema("H7307", "espírito, vento, sopro", r"espíritos?|ventos?|sopro|fôlego")
lema("H2233", "semente, descendência", r"sementes?|descendência|descendentes?|linhagem|posteridade")
lema("H7779", "ferir, esmagar", r"fer\w+|esmag\w+|pis\w+")
lema("H539", "crer, confiar", r"cr\w+|confi\w+|fi\w+")
lema("H2803", "contar, imputar", r"imput\w+|atribu\w+|cont\w+|consider\w+|reput\w+|pens\w+|planej\w+")
lema("H1961", "ser", r"sou|serei|é|era|foi|estarei")
lema("H7965", "paz", r"paz")
lema("H8085", "ouvir", r"ouv\w+|escut\w+|obedec\w+")
lema("H259", "um, único", r"um|único|uma")
lema("H157", "amar", r"am\w+")
lema("H3519", "glória", r"glórias?|honra")
lema("H7462", "pastorear", r"pastor\w*|apascent\w+")
lema("H5375", "levantar, carregar", r"perdo\w+|lev\w+|carreg\w+|tir\w+")
lema("H3680", "cobrir", r"cobert\w+|cobr\w+|encobr\w+|encobert\w+")
lema("H4229", "apagar", r"apag\w+|risc\w+|desf\w+")
lema("H2403", "pecado", r"pecados?")
lema("H3526", "lavar", r"lav\w+")
lema("H2398", "pecar; tirar o pecado", r"purific\w+|pec\w+|expi\w+")
lema("H1794", "esmagar", r"contrit\w+|quebrantad\w+|abatid\w+|esmag\w+")
lema("H5959", "moça, virgem", r"virgem|virgens|moças?|jovem|donzelas?")
lema("H2490", "traspassar", r"traspass\w+|fer\w+|perfur\w+")
lema("H1792", "moer, esmagar", r"mo[íi]\w+|moê\w+|esmag\w+|quebrant\w+")
lema("H6293", "fazer atingir", r"fez (?:cair|vir)|lanç\w+|interced\w+|car\w+|pôs")
lema("H817", "oferta pela culpa", r"expiaç\w+(?: d[oae] (?:pecado|culpa))?|ofert\w+(?: pel[oa] (?:pecado|culpa))?|culpa")
lema("H6663", "ser justo; declarar justo", r"justific\w+")
lema("H2319", "novo", r"nov[oa]s?")
lema("H3820", "coração", r"coraç(?:ão|ões)")
lema("H530", "firmeza, fidelidade", r"fé|fidelidade|verdade|lealdade")

# =====================================================================================================
# NOVO TESTAMENTO — palavras com nota geral
# =====================================================================================================
lema("G26", "amor", r"amor\w*|caridade",
     "Agapē: o amor que decide o bem do outro e se entrega por ele, sem depender do mérito de quem é amado. "
     "O Novo Testamento o define pela cruz (1 João 4:10).")
lema("G5485", "graça", r"graça|favor",
     "Charis: favor que não se merece nem se paga. Para Paulo é o resumo do evangelho: Deus dá de graça, em "
     "Cristo, o que jamais poderíamos conquistar.")
lema("G1344", "justificar, declarar justo", r"justific\w+|torn\w+ just\w+|declar\w+ just\w+|absolvid\w+",
     "Termo de tribunal: declarar justo, absolver. Não é tornar alguém interiormente bom, e sim o veredito de "
     "Deus a favor do pecador que confia em Cristo (Romanos 3:24; 4:5).")
lema("G1343", "justiça", r"justiças?",
     "O que é reto diante de Deus. Em Paulo, “justiça de Deus” é também o presente que ele dá: a condição de "
     "justo que o pecador recebe pela fé (Romanos 1:17; Filipenses 3:9).")
lema("G2435", "propiciação, propiciatório", r"propiciaç\w+|propiciatório|sacrifício de reconciliação",
     "Na Bíblia grega é o nome da tampa da arca, onde o sangue era aspergido no Dia da Expiação. Paulo diz que "
     "Deus apresentou Cristo como esse lugar: nele a justa ira contra o pecado é satisfeita.")
lema("G2434", "propiciação", r"propiciaç\w+|expiaç\w+|sacrifício(?: para (?:o )?perdão)?",
     "Sacrifício que afasta a ira de Deus contra o pecado. E foi o próprio Deus quem o providenciou: a cruz "
     "não convence um Deus relutante; ela é a prova do seu amor (1 João 4:10).")
lema("G629", "redenção", r"redenç\w+|resgate|libertaç\w+|livramento",
     "Soltura mediante pagamento de resgate — a palavra usada para a libertação de escravos e prisioneiros "
     "de guerra. O preço, diz Paulo, foi o sangue de Cristo (Efésios 1:7).")
lema("G3049", "contar, lançar na conta", r"imput\w+|atribu\w+|cont(?:a|o|e|ou|ad)\w*|consider\w+|reput\w+|lev\w+ em conta",
     "Verbo de contabilidade: lançar na conta de alguém. Em Romanos 4, Deus lança justiça na conta de quem crê "
     "e não lança o pecado: é o que a teologia chama de imputação.")
lema("G2643", "reconciliação", r"reconciliaç\w+",
     "Passar da inimizade à paz. No Novo Testamento é sempre Deus quem reconcilia e o ser humano quem é "
     "reconciliado: a iniciativa é toda dele (2 Coríntios 5:18–19).")
lema("G2644", "reconciliar", r"reconcili\w+",
     "Passar da inimizade à paz. No Novo Testamento é sempre Deus quem reconcilia e o ser humano quem é "
     "reconciliado: a iniciativa é toda dele (2 Coríntios 5:18–19).")
lema("G3341", "arrependimento", r"arrependimentos?|conversão",
     "Metanoia: mudança de mente. Reconhecer o pecado e voltar-se para Deus — não só remorso, mas meia-volta.")
lema("G3340", "arrepender-se", r"arrepend\w+",
     "Mudar de mente: reconhecer o pecado e voltar-se para Deus — não só remorso, mas meia-volta.")
lema("G1577", "igreja, assembleia", r"igrejas?|congregaç\w+|assembleias?",
     "Ekklēsia: assembleia convocada. Na Bíblia grega traduz a “congregação” de Israel reunida diante de Deus; "
     "no Novo Testamento é o povo de Cristo, reunido num lugar ou em toda parte — nunca um prédio.")
lema("G3439", "único, unigênito", r"unigênit\w+|únic\w+",
     "Único no seu gênero. Dito de Jesus, afirma que ele é Filho de um modo que ninguém mais é: "
     "não um entre muitos, mas o Filho único e eterno do Pai.")
lema("G4637", "armar a tenda, habitar", r"habit\w+|estend\w+|tabernácul\w+",
     "Literalmente “armou a sua tenda”. Lembra o tabernáculo no deserto, onde a glória de Deus morava no "
     "meio do povo.")
lema("G2315", "soprada por Deus", r"(?:divinamente )?inspirad\w+",
     "Palavra única no Novo Testamento: “soprada por Deus”. Não diz apenas que os autores foram inspirados, "
     "mas que o próprio texto saiu do sopro de Deus — por isso tem a autoridade dele.")
lema("G3875", "Consolador, Advogado", r"consolador|advogado|ajudador|intercessor|auxiliador|paráclito",
     "Paraklētos: alguém chamado para ficar ao lado — advogado, defensor, quem encoraja. Jesus chama assim o "
     "Espírito Santo, e 1 João 2:1 dá o mesmo título ao próprio Jesus diante do Pai.")
lema("G3466", "mistério", r"mistérios?|segredos?",
     "Não é um enigma para iniciados: é um plano de Deus antes oculto e agora revelado em Cristo, para ser "
     "anunciado a todos.")
lema("G2098", "evangelho, boa notícia", r"evangelho\w*|boas novas",
     "Boa notícia — no mundo antigo, o anúncio de uma vitória ou da chegada de um rei. Não é um conselho "
     "sobre o que fazer; é a notícia do que Deus fez em Cristo.")
lema("G37", "santificar", r"santific\w+|consagr\w+",
     "Separar para Deus. O Novo Testamento usa o verbo para o que já é verdade de todo crente (1 Coríntios 6:11) "
     "e para o processo de se tornar, na prática, o que já se é.")
lema("G38", "santificação", r"santificaç\w+|santidade",
     "Ser separado para Deus. O Novo Testamento fala disso como algo já feito em todo crente e como um "
     "caminho a percorrer: tornar-se, na prática, o que já se é em Cristo.")
lema("G5206", "adoção de filhos", r"adoç\w+(?: de filhos)?|filhos adotados|adotiv\w+|adotad\w+|filiaç\w+",
     "Termo jurídico romano: o adotado recebia o nome, a herança e todos os direitos de um filho legítimo. "
     "O crente não é só perdoado: é recebido na família.")
lema("G4309", "predestinar", r"predestin\w+|predetermin\w+|preorden\w+|(?:d?antes )?(?:determin|orden)\w+",
     "Demarcar de antemão (“horizonte” vem da mesma raiz). No Novo Testamento só tem Deus como sujeito e "
     "sempre aponta para um alvo: a adoção, a semelhança com Cristo, a glória.")
lema("G1586", "escolher", r"escolh\w+|eleg\w+|elei\w+",
     "Escolher para si. Dito de Deus, a ênfase está em quem escolhe, não nas qualidades do escolhido "
     "(1 Coríntios 1:27–29).")
lema("G1588", "eleito, escolhido", r"eleit\w+|escolhid\w+",
     "Escolhido. Dito do povo de Deus, a ênfase está em quem escolhe, não nas qualidades do escolhido.")
lema("G3824", "regeneração", r"regeneraç\w+|renovaç\w+|novo nascimento",
     "“Nascer de novo” numa palavra só. Em Tito 3:5 é a obra do Espírito na pessoa; em Mateus 19:28, a "
     "renovação de toda a criação.")
lema("G313", "gerar de novo", r"regener\w+|(?:de novo )?(?:ger|nasc)\w+(?: de novo)?|renasc\w+",
     "Gerar de novo. Quem age é Deus: ninguém gera a si mesmo.")
lema("G1242", "aliança, testamento", r"alianças?|testamentos?|pactos?|concertos?",
     "Diathēkē: disposição feita por uma só parte — por isso também significa “testamento”. Deus não negocia "
     "os termos: ele estabelece a aliança e garante o seu cumprimento.")
lema("G3316", "mediador", r"mediador\w*",
     "Quem fica entre duas partes para uni-las. “Há um só mediador entre Deus e os homens” (1 Timóteo 2:5): "
     "sendo Deus e homem, Cristo representa os dois lados.")
lema("G386", "ressurreição", r"ressurreiç\w+",
     "Literalmente “pôr-se de pé outra vez”. Não é a sobrevivência da alma: é o corpo que se levanta, "
     "como o de Cristo.")
lema("G3952", "vinda, presença", r"vinda|presença|chegada",
     "Presença ou chegada. No mundo antigo era o termo para a visita oficial de um rei a uma cidade; "
     "por isso o Novo Testamento o usa para a volta de Cristo.")
lema("G602", "revelação", r"revelaç\w+|manifestaç\w+",
     "Tirar o véu. O que só se conhece porque Deus mostrou — o contrário de uma descoberta humana.")
lema("G2842", "comunhão, participação", r"comunhão|comunicaç\w+|participaç\w+|contribuiç\w+|cooperaç\w+",
     "Ter em comum, participar junto. Abrange a comunhão com Deus, a vida partilhada entre irmãos e até a "
     "oferta em dinheiro: quem participa de Cristo reparte o que tem.")
lema("G1680", "esperança", r"esperanças?",
     "Não é torcida: é expectativa segura, porque se apoia na promessa de Deus e na ressurreição de Cristo "
     "(1 Pedro 1:3).")
lema("G5281", "perseverança", r"paciência|perseverança|constância|firmeza",
     "Ficar firme debaixo do peso. Não é resignação: é a constância de quem continua porque espera algo.")
lema("G3107", "bem-aventurado", r"bem-aventurad\w+|bendit\w+|feliz|felizes",
     "Feliz de verdade, aprovado por Deus. As bem-aventuranças não descrevem um sentimento, mas a condição "
     "de quem pertence ao Reino — mesmo chorando ou perseguido.")
lema("G5", "Aba, Pai", r"aba",
     "Aramaico, a língua de casa de Jesus: o jeito íntimo e respeitoso de um filho chamar o pai. Jesus orou "
     "assim no Getsêmani, e o Espírito leva os filhos adotados a orar com a mesma palavra.")
lema("G3134", "“Vem, nosso Senhor!”", r"maranata|vem,? senhor",
     "Aramaico preservado sem tradução: “Nosso Senhor, vem!” — uma das orações mais antigas da igreja.")
lema("G4352", "adorar, prostrar-se", r"ador\w+|prostr\w+",
     "Curvar-se até o chão diante de alguém. É o gesto devido a Deus; por isso pesa tanto quando Jesus o "
     "recebe sem recusar (Mateus 14:33; 28:17) e quando anjos e apóstolos o recusam (Apocalipse 22:8–9).")
lema("G3083", "resgate", r"resgate",
     "O preço pago para libertar um escravo ou prisioneiro. É assim que Jesus resume a própria morte.")
lema("G487", "resgate em lugar de", r"resgate",
     "Resgate “no lugar de”: a palavra junta “preço de libertação” e “em troca de”. Cristo se deu como "
     "substituto.")
lema("G728", "penhor, garantia", r"penhor|garantia",
     "Termo comercial: a entrada que garante o pagamento do restante. O Espírito Santo é a primeira parcela "
     "da herança — e a garantia de que o resto virá.")
lema("G859", "perdão, remissão", r"perdão|remissão",
     "Soltar, mandar embora, cancelar uma dívida. O perdão bíblico não finge que a dívida não existia: "
     "alguém arcou com ela (Mateus 26:28).")
lema("G1694", "Emanuel", r"emanuel",
     "“Deus conosco”, em hebraico. Mateus abre o evangelho com esse nome e o fecha com a promessa "
     "“eu estou convosco todos os dias” (28:20).")
lema("G3841", "Todo-Poderoso", r"todo[- ]poderoso|onipotente",
     "Aquele que tem tudo nas mãos. Quase todas as vezes em que aparece no Novo Testamento estão no "
     "Apocalipse, livro escrito para uma igreja perseguida.")

# ----- só onde houver nota de contexto -----
lema("G3056", "palavra", r"palavras?|verbo")
lema("G2316", "Deus", r"deus")
lema("G4561", "carne", r"carne")
lema("G25", "amar", r"am\w+")
lema("G5368", "amar, ter afeição", r"am\w+")
lema("G2889", "mundo", r"mundo")
lema("G4100", "crer", r"cr\w+")
lema("G166", "eterno", r"etern\w+")
lema("G509", "de novo; do alto", r"de novo|do alto|de cima")
lema("G1510", "ser", r"sou")
lema("G5055", "concluir, cumprir", r"(?:está )?consumado|cumprid\w+|(?:está )?terminado")
lema("G2424", "Jesus", r"jesus")
lema("G4102", "fé", r"fé")
lema("G5302", "estar em falta", r"destituíd\w+|carec\w+|falt\w+|priv\w+")
lema("G2631", "condenação", r"condenaç\w+")
lema("G4267", "conhecer de antemão", r"(?:d?antes |já )?(?:conhec|soub|sab)\w+(?: de antemão| antes)?")
lema("G2962", "Senhor", r"senhor")
lema("G2937", "criação", r"criaturas?|criaç\w+")
lema("G266", "pecado", r"pecado")
lema("G1805", "comprar para libertar", r"resgat\w+|remi\w+|redim\w+")
lema("G4161", "obra feita", r"feitura|obra|criaç\w+")
lema("G3444", "forma", r"forma")
lema("G2758", "esvaziar", r"esvazi\w+|aniquil\w+")
lema("G4416", "primogênito", r"primogênit\w+")
lema("G5481", "impressão exata", r"(?:a )?expressa imagem|(?:a )?imagem exata|expressão exata|(?:a )?imagem")
lema("G5287", "fundamento, garantia", r"(?:o )?firme fundamento|fundamento|certeza|confiança|substância")

# =====================================================================================================
# NOTAS DE CONTEXTO — por que a palavra pesa naquele versículo
# =====================================================================================================
contexto("GEN.1.1", "H7225",
         "Não é só “antes de tudo”: é o começo absoluto do tempo e do universo. Deus já estava lá; tudo o mais teve início.")
contexto("GEN.1.1", "H1254",
         "Primeiro verbo da Bíblia, e nas Escrituras só Deus é o seu sujeito. Aqui nenhuma matéria-prima é mencionada: "
         "Deus não molda o que já existia; ele faz existir (Hebreus 11:3).")
contexto("GEN.1.1", "H430",
         "Elohim: forma plural, mas com o verbo no singular (“criou”). O plural expressa majestade e plenitude; "
         "o texto fala de um só Deus.")
contexto("GEN.1.2", "H7307",
         "A palavra significa vento, sopro e espírito. Aqui o Espírito de Deus paira sobre as águas como a ave sobre o "
         "ninho (o mesmo verbo de Deuteronômio 32:11): presente desde o primeiro ato da criação.")
contexto("GEN.1.27", "H1254",
         "O verbo “criar” aparece três vezes neste único versículo. A repetição marca o ponto mais alto do capítulo: "
         "homem e mulher, os dois à imagem de Deus.")
contexto("GEN.3.15", "H2233",
         "Primeira promessa do evangelho. “Semente” é singular e coletivo ao mesmo tempo: uma linhagem — e, no fim, "
         "um descendente (Gálatas 3:16) — que enfrentará a serpente.")
contexto("GEN.3.15", "H7779",
         "O mesmo verbo para os dois golpes, em lugares diferentes: a cabeça da serpente (golpe mortal) e o calcanhar do "
         "descendente (ferida real, mas não definitiva). A cruz cumpre os dois.")
contexto("GEN.15.6", "H539",
         "Da raiz de “amém”: apoiar-se no que é firme. Abrão nada fez além de confiar na promessa. É o versículo que "
         "Paulo usa para explicar a justificação pela fé (Romanos 4:3; Gálatas 3:6).")
contexto("GEN.15.6", "H2803",
         "Verbo de contabilidade: lançar na conta. A justiça não foi algo que Abrão produziu; foi creditada a ele.")
contexto("EXO.3.14", "H1961",
         "“Eu sou o que sou”: Deus se apresenta como aquele que simplesmente é — não depende de nada, não muda. "
         "O nome YHWH (“o SENHOR”) vem desse verbo, e Jesus o aplica a si mesmo em João 8:58.")
contexto("EXO.34.6", "H2617",
         "Deus define o próprio nome. O hesed é o amor leal da aliança — proclamado logo depois do bezerro de ouro, a "
         "quem não o merecia. Este versículo ecoa pela Bíblia inteira (Salmo 103:8; Jonas 4:2).")
contexto("LEV.17.11", "H3722",
         "A razão do sacrifício: a vida está no sangue, e uma vida é dada no lugar de outra. Hebreus 9:22 resume: "
         "“sem derramamento de sangue não há remissão”.")
contexto("NUM.6.26", "H7965",
         "Shalom: mais que ausência de conflito — inteireza, tudo no devido lugar. É a última palavra da bênção "
         "sacerdotal, o resumo de tudo o que Deus dá.")
contexto("DEU.6.4", "H8085",
         "Shemá: ouvir para obedecer. A palavra dá nome à confissão de fé de Israel, recitada todos os dias; "
         "Jesus a cita como o primeiro mandamento (Marcos 12:29).")
contexto("DEU.6.4", "H259",
         "O SENHOR é um só, o único: não divide a sua glória com nenhum outro deus. Por isso o versículo seguinte "
         "pede o coração inteiro.")
contexto("DEU.6.5", "H157",
         "Aqui o amor é mandamento, não só sentimento: lealdade de todo o ser a quem amou primeiro (Deuteronômio 7:7–8).")
contexto("PSA.19.1", "H3519",
         "Literalmente “peso”: aquilo que torna alguém importante. A glória de Deus é o peso do que ele é, tornado "
         "visível — aqui, num céu que todos podem ver.")
contexto("PSA.23.1", "H7462",
         "No hebraico é um verbo: “o SENHOR é quem me apascenta”. Os reis eram chamados pastores do povo; Davi, que "
         "foi pastor e rei, declara que ele mesmo tem um. Jesus toma o título para si em João 10:11.")
contexto("PSA.32.1", "H5375",
         "Literalmente “levantada, carregada”: a transgressão é tirada de cima de quem a cometeu. Alguém a carrega "
         "(Isaías 53:4, 12).")
contexto("PSA.32.1", "H3680",
         "Coberto para não ser mais visto — por Deus, não pelo pecador. O versículo 5 faz o contraste: quando Davi "
         "parou de encobrir, Deus cobriu.")
contexto("PSA.32.2", "H2803",
         "Lançar na conta. Bem-aventurado é aquele em cuja conta Deus não lança o pecado: Paulo cita este versículo "
         "em Romanos 4:8 para explicar a justificação.")
contexto("PSA.51.1", "H4229",
         "Apagar como quem raspa a tinta de um registro: Davi pede que a dívida seja riscada do livro.")
contexto("PSA.51.1", "H6588",
         "Davi usa as três palavras hebraicas para pecado nos dois primeiros versículos: transgressão (rebelião), "
         "iniquidade (desvio) e pecado (errar o alvo). Não suaviza nada.")
contexto("PSA.51.2", "H3526",
         "O verbo é o de lavar roupa — pisar, esfregar, bater. Davi não pede um enxágue; pede a lavagem pesada de "
         "quem sabe que a mancha é funda.")
contexto("PSA.51.2", "H2403",
         "Errar o alvo, ficar aquém do que Deus requer. É a palavra mais comum para pecado no Antigo Testamento.")
contexto("PSA.51.7", "H2398", formas=r"limpa-me do pecado", nota=
         "Literalmente “despeca-me”: o verbo “pecar” numa forma que significa tirar o pecado. O hissopo era o ramo "
         "usado para aspergir o sangue na Páscoa e na purificação do leproso (Êxodo 12:22; Levítico 14).")
contexto("PSA.51.10", "H1254",
         "Davi não pede um conserto; pede uma criação. É o verbo de Gênesis 1:1, que só tem Deus como sujeito: um "
         "coração puro não é algo que o pecador produz em si mesmo. É obra que só Deus faz, tão dele quanto fazer o mundo.")
contexto("PSA.51.17", "H1794", formas=r"triste", nota=
         "Esmagado, triturado. O sacrifício que Deus aceita é o coração que parou de se defender.")
contexto("PSA.136.1", "H2617",
         "O refrão repete hesed em todos os 26 versículos: cada fato da criação e da história de Israel é lido como "
         "prova do amor leal de Deus.")
contexto("ISA.6.3", "H6918",
         "Dito três vezes — a única qualidade de Deus repetida assim na Bíblia. Em hebraico, repetir é o superlativo: "
         "santo acima de qualquer medida.")
contexto("ISA.7.14", "H5959",
         "Almá: moça em idade de casar, que naquela cultura se presumia virgem. A tradução grega feita por judeus "
         "antes de Cristo traz parthenos (“virgem”), e é assim que Mateus 1:23 cita o texto.")
contexto("ISA.9.6", "H7965",
         "Shalom: inteireza, tudo devolvido ao seu lugar. O menino prometido não apenas traz a paz; é o Príncipe dela.")
contexto("ISA.53.5", "H2490",
         "Perfurado, traspassado — verbo de morte violenta. “Por” nossas transgressões: o castigo é dele, a culpa era nossa.")
contexto("ISA.53.5", "H1792",
         "Esmagado, triturado. O mesmo verbo volta no versículo 10: “ao SENHOR agradou moê-lo”. A cruz não foi acidente.")
contexto("ISA.53.5", "H7965",
         "O castigo que nos traz a paz (shalom) caiu sobre ele: a nossa paz com Deus teve um preço, e foi outro quem pagou.")
contexto("ISA.53.6", "H6293",
         "Fazer encontrar, fazer atingir: o SENHOR fez a culpa de todos convergir sobre o Servo. É a linguagem do "
         "bode expiatório de Levítico 16.")
contexto("ISA.53.10", "H817",
         "Asham: a oferta pela culpa de Levítico 5, que repara o dano causado. O Servo não só oferece o sacrifício — "
         "ele é o sacrifício.")
contexto("ISA.53.11", "H6663",
         "Declarar justo. O Servo justo torna justos a muitos, levando ele mesmo as iniquidades deles: a troca que "
         "Paulo explica em 2 Coríntios 5:21.")
contexto("JER.31.31", "H2319",
         "Não uma aliança remendada, mas nova: a lei escrita no coração e o pecado perdoado de vez (v. 33–34). Jesus a "
         "inaugura na Ceia: “este cálice é a nova aliança no meu sangue” (Lucas 22:20).")
contexto("EZK.36.26", "H3820",
         "O centro da pessoa: de onde vêm pensamento, vontade e desejo. Deus não promete reformar o coração de pedra; "
         "promete trocá-lo.")
contexto("HAB.2.4", "H530",
         "Emuná: firmeza, fidelidade — a confiança que se mantém. O Novo Testamento cita este versículo três vezes "
         "(Romanos 1:17; Gálatas 3:11; Hebreus 10:38); foi o texto que abriu os olhos de Lutero.")
contexto("MIC.6.8", "H2617",
         "Deus não pede apenas que se pratique a misericórdia: pede que se ame o hesed — o mesmo amor leal que ele "
         "tem pelo seu povo.")

contexto("MAT.1.21", "G2424",
         "Forma grega do hebraico Yeshua (Josué): “o SENHOR salva”. O anjo explica o nome na própria frase — "
         "“porque ele salvará o seu povo dos seus pecados”.")
contexto("MAT.16.18", "G1577",
         "Primeira vez que a palavra aparece no Novo Testamento, e Jesus diz “minha igreja”: a assembleia do povo de "
         "Deus agora se reúne em torno dele.")
contexto("JHN.1.1", "G3056",
         "Logos: palavra, razão, mensagem. Para o leitor judeu, a Palavra pela qual Deus criou (“E disse Deus…”) e se "
         "revelou; para o grego, o princípio racional do universo. João afirma que esse Logos é uma pessoa — e, no "
         "versículo 14, que se fez carne.")
contexto("JHN.1.1", "G2316", n=2, nota=
         "“A Palavra era Deus”: no grego, “Deus” vem antes do verbo e sem artigo, o que descreve a natureza da "
         "Palavra — tudo o que Deus é, ela é — sem confundi-la com o Pai, com quem ela “estava”.")
contexto("JHN.1.14", "G3056",
         "O mesmo Logos do versículo 1 — eterno, com Deus, Deus. Agora João diz o impensável: ele se tornou o que "
         "não era, sem deixar de ser o que era.")
contexto("JHN.1.14", "G4561",
         "Não “entrou num corpo” nem “pareceu humano”: tornou-se carne — humanidade real, frágil e mortal. A palavra "
         "mais crua disponível, contra quem negava que o Filho tivesse corpo de verdade (1 João 4:2).")
contexto("JHN.3.3", "G509", formas=r"voltar a nascer", nota=
         "A palavra grega (anōthen) significa “de novo” e também “do alto”. Nicodemos entende só o primeiro sentido (voltar ao "
         "ventre?); Jesus fala dos dois: um nascimento novo que vem de cima, de Deus.")
contexto("JHN.3.16", "G25",
         "Agapaō: amor que se mostra em dar, não só em sentir. A medida vem na própria frase — “de tal maneira… que deu”.")
contexto("JHN.3.16", "G2889",
         "Em João, “mundo” é a humanidade que virou as costas para Deus (1:10). O espanto do versículo não é o tamanho "
         "do mundo, e sim que Deus ame um mundo assim.")
contexto("JHN.3.16", "G4100",
         "No grego, “crer para dentro de” (pisteuō eis): não só aceitar que algo é verdade, mas confiar-se a uma "
         "pessoa. O verbo está no presente: aquele que segue crendo.")
contexto("JHN.3.16", "G166",
         "“Da era vindoura”: não é só vida que não acaba; é a vida do mundo futuro, que já começa para quem crê "
         "(5:24; 17:3).")
contexto("JHN.8.58", "G1510",
         "Não “eu era”: “eu sou” — o presente sem começo, eco do nome que Deus revelou a Moisés (Êxodo 3:14). "
         "Os ouvintes entenderam: pegaram pedras para apedrejá-lo por blasfêmia.")
contexto("JHN.19.30", "G5055",
         "Tetelestai: uma palavra só em grego. “Cumprido, concluído” — não o suspiro de quem desiste, mas o anúncio de "
         "quem terminou a obra. O tempo verbal indica algo feito de uma vez, cujo efeito permanece.")
contexto("JHN.21.17", "G5368",
         "Jesus pergunta duas vezes com agapaō e, na terceira, usa phileō, o verbo de Pedro. João costuma alternar os "
         "dois como sinônimos; o que pesa aqui são as três perguntas, uma para cada negação.")
contexto("ROM.1.17", "G1343",
         "“Justiça de Deus”: não só a qualidade de Deus ser justo, mas a justiça que ele dá — a condição de justo "
         "recebida pela fé. Lutero escreveu que, ao entender isso, sentiu as portas do paraíso se abrirem.")
contexto("ROM.1.17", "G4102",
         "Do começo ao fim, pela fé (“de fé em fé”). Paulo apoia a frase em Habacuque 2:4.")
contexto("ROM.3.21", "G1343",
         "A virada da carta (“Mas agora”). Depois de mostrar que ninguém é justo (3:10), Paulo anuncia uma justiça "
         "que vem de Deus, sem depender da lei, para todos os que creem.")
contexto("ROM.3.23", "G5302",
         "Ficar para trás, estar em falta. O verbo está no presente: todos pecaram (fato consumado) e continuam "
         "aquém da glória de Deus.")
contexto("ROM.3.24", "G1344",
         "Declarados justos “gratuitamente” — a mesma palavra de João 15:25, “sem motivo”. Não há em quem é "
         "justificado nada que explique o veredito; a causa está toda na graça e na redenção em Cristo.")
contexto("ROM.3.28", "G4102",
         "A conclusão do argumento: o veredito de “justo” vem pela fé, sem contar as obras da lei. Lutero traduziu "
         "“somente pela fé”; a palavra “somente” não está no grego, mas é o sentido da frase.")
contexto("ROM.4.5", "G1344",
         "Deus “justifica o ímpio”: a frase mais ousada de Paulo. O veredito não espera a pessoa melhorar; alcança "
         "quem não tem obra nenhuma a apresentar e apenas crê.")
contexto("ROM.8.1", "G2631",
         "Termo de tribunal: a sentença e a sua execução. No grego, “nenhuma” abre a frase, com toda a ênfase — "
         "nem um pouco de condenação.")
contexto("ROM.8.29", "G4267",
         "Na Bíblia, “conhecer” pessoas é mais que saber sobre elas: é relacionar-se, amar (Amós 3:2). O texto não "
         "diz que Deus conheceu de antemão algo sobre elas, e sim que conheceu a elas.")
contexto("ROM.10.9", "G2962",
         "“Jesus é Senhor” é a confissão mais antiga da igreja. Kyrios é a palavra que a Bíblia grega usa para o nome "
         "de Deus (YHWH) — e era o título que César reivindicava.")
contexto("2CO.5.17", "G2937",
         "Ktisis: criação. Quem está em Cristo não é apenas alguém melhorado — pertence à nova criação que Deus "
         "prometeu (Isaías 65:17) e que já começou.")
contexto("2CO.5.21", "G266",
         "A grande troca: aquele que não conheceu pecado foi tratado como pecado, para que nós fôssemos tratados como "
         "justos. Ele não se tornou pecador; carregou o que era nosso.")
contexto("GAL.3.13", "G1805",
         "Comprar no mercado e tirar de lá — o verbo da compra de um escravo para libertá-lo. O preço: ele se fez "
         "maldição em nosso lugar.")
contexto("EPH.2.8", "G5485",
         "“Pela graça” vem primeiro na frase: é a causa. A fé é o meio pelo qual se recebe, não a contribuição "
         "humana — e o conjunto todo, diz Paulo, “não vem de vós, é dom de Deus”.")
contexto("EPH.2.8", "G4102",
         "A fé não é a obra que substitui as obras: é a mão vazia que recebe. Por isso Paulo acrescenta logo "
         "“e isto não vem de vós”.")
contexto("EPH.2.10", "G4161", formas=r"feitos", nota=
         "Poiēma: obra saída das mãos de um artífice (de onde vem “poema”). As boas obras não são a causa da salvação "
         "(v. 9); são o propósito para o qual fomos refeitos.")
contexto("PHP.2.6", "G3444",
         "Morphē: não a aparência externa, mas aquilo que alguém realmente é. “Em forma de Deus” = verdadeiramente "
         "Deus; “forma de servo” (v. 7) = verdadeiramente servo.")
contexto("PHP.2.7", "G2758",
         "“Esvaziou-se” — e a frase explica como: não deixando de ser Deus, mas “tomando a forma de servo”. "
         "Ele se esvaziou acrescentando a humanidade, não subtraindo a divindade.")
contexto("PHP.2.11", "G2962",
         "O nome acima de todo nome: Kyrios, a palavra que a Bíblia grega usa para YHWH. Paulo aplica a Jesus o que "
         "Isaías 45:23 diz do próprio Deus.")
contexto("COL.1.15", "G4416",
         "Não “o primeiro a ser criado”: o versículo seguinte diz que tudo foi criado por ele. Primogênito é título de "
         "posição — o herdeiro, o que tem a primazia sobre toda a criação (Salmo 89:27).")
contexto("HEB.1.3", "G5481",
         "Charaktēr: a marca deixada por um sinete — a impressão exata. O Filho não é parecido com Deus; é a "
         "reprodução exata do seu ser.")
contexto("HEB.11.1", "G4102",
         "A definição não diz o que a fé sente, e sim o que ela faz: trata como real o que Deus prometeu, antes de ver.")
contexto("HEB.11.1", "G5287",
         "Hypostasis: o que fica por baixo e sustenta — fundamento, garantia. Nos documentos da época, também o "
         "título de propriedade: a fé é ter em mãos a escritura do que ainda não se vê.")
contexto("JAS.2.17", "G4102",
         "Tiago não corrige Paulo; fala de outra coisa. A fé que nada produz é só uma declaração (v. 14, “se alguém "
         "disser que tem fé”). A fé que justifica nunca fica sozinha.")
contexto("1PE.1.20", "G4267",
         "Conhecido de antemão: não que Deus apenas soubesse o que aconteceria — a cruz foi plano dele antes da "
         "criação do mundo (Atos 2:23).")
contexto("1JN.4.8", "G26",
         "Não apenas “Deus é amoroso”: amor é o que ele é em si mesmo, antes de haver mundo — Pai, Filho e Espírito. "
         "Mas a frase não se inverte: o amor não é Deus.")
contexto("1JN.4.10", "G2434",
         "João define o amor pela cruz: não que nós tenhamos amado, mas que ele enviou o Filho como propiciação — "
         "o sacrifício que afasta a ira. Amor e justiça se encontram no mesmo ato.")


# =====================================================================================================
def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def gravar(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def padrao(formas):
    return re.compile(r"(?<![\w-])(?:" + formas + r")(?!\w)", re.I)     # "lava-me" e "contou-lhe" valem


def main():
    relatorio = "--relatorio" in sys.argv
    livros = ler(DATA / "books.json")["books"]
    lexico = {"H": ler(DATA / "strongs" / "H.json"), "G": ler(DATA / "strongs" / "G.json")}
    for s in LEMAS:
        assert s in lexico[s[0]], f"{s} não existe no léxico"
        LEMAS[s]["re"] = padrao(LEMAS[s]["formas"])
    for (ref, s, n), c in CONTEXTOS.items():
        assert s in LEMAS, f"contexto {ref}: falta lema({s!r}, ...)"
        c["re"] = padrao(c["formas"]) if c["formas"] else LEMAS[s]["re"]

    usados, erros = set(), []
    vistos = collections.Counter()        # vezes em que a palavra original aparece
    marcados = collections.Counter()      # vezes em que foi sublinhada
    perdidos = collections.defaultdict(list)
    total, n_caps, saida = 0, 0, {}
    for b in livros:
        texto_livro = ler(DATA / "bibles" / "blivre" / f"{b['id']}.json")
        for cap in range(1, b["ch"] + 1):
            arq = DATA / "interlinear" / b["id"] / f"{cap}.json"
            if not arq.exists():
                continue
            inter, versos, ja_no_cap, do_cap = ler(arq), texto_livro[cap - 1], set(), {}
            for i, palavras in enumerate(inter):
                texto = versos[i] if i < len(versos) else ""
                if not texto:
                    continue
                ref, vez, candidatos = f"{b['id']}.{cap}.{i + 1}", collections.Counter(), []
                no_verso = collections.Counter(p[2] for p in palavras)
                for j, p in enumerate(palavras):
                    s = p[2]
                    if s not in LEMAS:
                        continue
                    vez[s] += 1
                    vistos[s] += 1
                    onde = (j + .5) / len(palavras)          # em que altura do versículo a palavra original está
                    c = CONTEXTOS.get((ref, s, vez[s]))
                    if c:
                        usados.add((ref, s, vez[s]))
                        candidatos.append((0, len(candidatos), s, vez[s], c, onde))
                    elif LEMAS[s]["nota"]:
                        candidatos.append((1, len(candidatos), s, vez[s], None, onde))
                ocupados, feitos = [], []
                for prioridade, _, s, n, c, onde in sorted(candidatos):
                    if len(feitos) >= MAX_POR_VERSO or (not c and s in ja_no_cap):
                        continue
                    achados = [m.span() for m in (c["re"] if c else LEMAS[s]["re"]).finditer(texto)]
                    livres = [a for a in achados if not any(a[0] < o[1] and o[0] < a[1] for o in ocupados)]
                    # mesma quantidade no original e no português: a n-ésima é a n-ésima. Senão, vale a forma que
                    # está mais ou menos na mesma altura do versículo (a ordem das palavras costuma acompanhar).
                    if len(achados) == no_verso[s] and achados[n - 1] in livres:
                        alvo = achados[n - 1]
                    else:
                        alvo = min(livres, key=lambda a: abs((a[0] + a[1]) / 2 / len(texto) - onde)) if livres else None
                    if not alvo:
                        if c:
                            erros.append(f"{ref} {s}: nenhuma forma encontrada em “{texto}”")
                        elif len(perdidos[s]) < 4:
                            perdidos[s].append(f"{ref}: {texto[:110]}")
                        continue
                    ocupados.append(alvo)
                    ja_no_cap.add(s)
                    marcados[s] += 1
                    feitos.append([alvo[0], alvo[1], s] + ([c["nota"]] if c else []))
                if feitos:
                    do_cap[str(i + 1)] = sorted(feitos)
                    total += len(feitos)
            if do_cap:
                saida.setdefault(b["id"], {})[str(cap)] = do_cap
                n_caps += 1

    for chave in CONTEXTOS:
        if chave not in usados:
            erros.append(f"{chave[0]} {chave[1]}: a palavra original não está nesse versículo (ou não {chave[2]} vezes)")
    if erros:
        sys.exit("ERROS nas notas de contexto:\n  " + "\n  ".join(erros))

    if relatorio:
        for s, l in LEMAS.items():
            print(f"{s:6} {l['pt'][:28]:28} aparece {vistos[s]:4}  sublinhada {marcados[s]:4}" + ("" if l["nota"] else "  (só contexto)"))
            for p in perdidos.get(s, []):
                print("         sem forma em " + p)
    else:
        shutil.rmtree(SAIDA, ignore_errors=True)
        for livro, do_livro in saida.items():          # um arquivo por livro: {capítulo: {versículo: [[início, fim, strong, nota?]]}}
            gravar(SAIDA / f"{livro}.json", do_livro)
        gravar(SAIDA / "indice.json", {                 # o que o cartão mostra de cada palavra, e que livros têm arquivo
            "lemas": {s: {"o": lexico[s[0]][s]["lemma"], "t": lexico[s[0]][s]["translit"], "pt": l["pt"],
                          **({"nota": l["nota"]} if l["nota"] else {})} for s, l in LEMAS.items() if marcados[s]},
            "livros": list(saida)})
    print(f"{total} palavras sublinhadas em {n_caps} capítulos de {len(saida)} livros; "
          f"{len(LEMAS)} palavras originais, {len(CONTEXTOS)} notas de contexto")


if __name__ == "__main__":
    main()
