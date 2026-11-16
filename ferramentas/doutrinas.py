"""Doutrinas da fé reformada (presbiteriana) para a busca de Temas, com os versículos em que se apoiam.

São temas que não aparecem com esse nome no texto bíblico (pedobatismo, Trindade, perseverança dos santos...).
A base é a Confissão de Fé de Westminster (CFW, 1647), o Breve Catecismo (BC) e os textos de prova que eles
citam; o resumo é síntese do Sola, não citação.

  D(id, título, sinônimos, fonte, resumo, [(título da seção, "GEN 17:7; ACT 2:38-39; ..."), ...])

Referências na numeração da Bíblia Livre: "LIV cap:v", "LIV cap:v-v" ou "LIV cap:v,v". Depois de mexer aqui:
python3 ferramentas/gerar_doutrinas.py (confere cada referência e grava data/topics/doutrinas.json com o texto).
"""

DOUTRINAS = []


def D(id, titulo, sin, fonte, resumo, secoes):
    DOUTRINAS.append({"id": id, "titulo": titulo, "sin": sin, "fonte": fonte, "resumo": resumo, "secoes": secoes})


# ------------------------------------------------------------------ visões de conjunto
D("cinco-solas", "As cinco solas da Reforma", ["solas", "sola scriptura", "sola fide", "sola gratia", "solus christus",
  "soli deo gloria", "reforma protestante"], "Princípios da Reforma do século XVI",
  "Resumo do que os reformadores recuperaram: a Escritura é a única regra de fé; a salvação é só pela graça, recebida só "
  "pela fé, só por causa de Cristo, e tudo para a glória de Deus somente.",
  [("Somente a Escritura", "2TI 3:16-17; ISA 8:20"),
   ("Somente a graça", "EPH 2:8-9; ROM 11:6"),
   ("Somente a fé", "ROM 3:28; GAL 2:16"),
   ("Somente Cristo", "ACT 4:12; 1TI 2:5"),
   ("Glória somente a Deus", "ROM 11:36; 1CO 10:31")])
D("tulip", "Os cinco pontos do calvinismo (TULIP)", ["calvinismo", "tulip", "doutrinas da graça", "sínodo de dort",
  "cinco pontos"], "Cânones de Dort (1619); CFW 3, 6, 8, 10, 17",
  "Resposta do Sínodo de Dort aos remonstrantes: o homem está morto no pecado, Deus escolheu por graça quem salvaria, "
  "Cristo morreu eficazmente pelos seus, o Espírito chama de modo que não falha, e os salvos são guardados até o fim. "
  "Cada ponto tem o seu próprio tema na busca.",
  [("Depravação total", "ROM 3:10-12; EPH 2:1"),
   ("Eleição incondicional", "EPH 1:4-5; ROM 9:11-13"),
   ("Expiação limitada (redenção particular)", "JHN 10:11, 15; MAT 1:21"),
   ("Graça irresistível (vocação eficaz)", "JHN 6:37, 44; ROM 8:30"),
   ("Perseverança dos santos", "JHN 10:27-29; PHP 1:6")])

# ------------------------------------------------------------------ Escritura e Deus
D("sola-scriptura", "Somente a Escritura (Sola Scriptura)", ["sola scriptura", "suficiência das escrituras",
  "autoridade da bíblia", "regra de fé", "tradição", "cânon"], "CFW 1; BC 2-3",
  "A Bíblia é a Palavra de Deus escrita e a única regra infalível de fé e de vida. Tudo o que é necessário para a "
  "salvação e para agradar a Deus está nela, de forma expressa ou por consequência necessária; nada deve ser "
  "acrescentado, nem por novas revelações nem por tradições humanas.",
  [("A Escritura é suficiente para salvar e instruir", "2TI 3:15-17; JHN 20:31"),
   ("É a regra para julgar todo ensino", "ISA 8:20; ACT 17:11; GAL 1:8-9"),
   ("Nada se acrescenta nem se tira", "DEU 4:2; REV 22:18-19"),
   ("A tradição humana não tem autoridade sobre a Palavra", "MRK 7:7-9, 13; COL 2:8")])
D("inspiracao", "Inspiração e inerrância da Bíblia", ["inspiração", "inerrância", "infalibilidade",
  "palavra de deus", "bíblia é a palavra de deus"], "CFW 1.4-5, 1.8",
  "Toda a Escritura foi soprada por Deus: os autores humanos escreveram movidos pelo Espírito Santo, e por isso o que "
  "ela afirma é verdadeiro e tem a autoridade do próprio Deus. A certeza plena dessa autoridade vem do testemunho "
  "interno do Espírito no coração.",
  [("Soprada por Deus", "2TI 3:16; 2PE 1:20-21"),
   ("A Palavra de Deus é verdade", "JHN 17:17; PSA 19:7-9; PRO 30:5"),
   ("Não pode falhar", "MAT 5:18; JHN 10:35"),
   ("O Espírito dá a certeza", "1CO 2:10-14; 1JN 2:20, 27")])
D("trindade", "Trindade", ["trindade", "trino", "pai filho e espírito santo", "divindade de cristo",
  "divindade do espírito santo"], "CFW 2.3; BC 6",
  "Há um só Deus vivo e verdadeiro, e nele há três pessoas, o Pai, o Filho e o Espírito Santo, da mesma substância, "
  "iguais em poder e glória. O Pai não é gerado, o Filho é eternamente gerado do Pai e o Espírito procede do Pai e do "
  "Filho.",
  [("Um só Deus", "DEU 6:4; 1CO 8:4-6"),
   ("Três pessoas nomeadas juntas", "MAT 3:16-17; MAT 28:19; 2CO 13:14"),
   ("O Filho é Deus", "JHN 1:1, 14; JHN 20:28; ROM 9:5; HEB 1:8"),
   ("O Espírito Santo é Deus", "ACT 5:3-4; 1CO 3:16"),
   ("O Espírito procede do Pai e é enviado pelo Filho", "JHN 15:26; GAL 4:6")])
D("soberania-de-deus", "Soberania de Deus", ["soberania", "atributos de deus", "onipotência", "onisciência",
  "imutabilidade", "deus soberano"], "CFW 2.1-2; BC 4",
  "Deus é espírito, infinito, eterno e imutável no seu ser, sabedoria, poder, santidade, justiça, bondade e verdade. "
  "Ele tem domínio absoluto sobre todas as criaturas e faz tudo segundo o conselho da sua vontade.",
  [("Deus faz tudo o que lhe agrada", "PSA 115:3; PSA 135:6; DAN 4:35"),
   ("Opera todas as coisas segundo a sua vontade", "EPH 1:11; ISA 46:9-10"),
   ("Imutável", "MAL 3:6; JAS 1:17"),
   ("Conhece tudo", "PSA 139:1-4; HEB 4:13")])

# ------------------------------------------------------------------ decretos, criação, providência
D("predestinacao", "Predestinação", ["predestinação", "decretos de deus", "decreto eterno", "presciência",
  "eleição e reprovação"], "CFW 3; BC 7, 20",
  "Desde toda a eternidade Deus ordenou livre e imutavelmente tudo o que acontece, sem ser autor do pecado e sem "
  "violentar a vontade das criaturas. Para manifestar a sua glória, predestinou alguns para a vida eterna em Cristo, "
  "por pura graça; os demais, deixou no seu pecado, para a justa condenação.",
  [("Deus ordenou tudo o que acontece", "EPH 1:11; ROM 11:33-36; ACT 2:23; ACT 4:27-28"),
   ("Predestinados em Cristo, para louvor da sua graça", "EPH 1:4-6; ROM 8:29-30"),
   ("Por graça, não por obras previstas", "ROM 9:11-16; 2TI 1:9"),
   ("Os que são deixados no seu pecado", "ROM 9:17-22; 1PE 2:8; JUD 1:4"),
   ("A doutrina é para humildade e consolo", "ROM 11:5-6, 20; 2PE 1:10")])
D("eleicao-incondicional", "Eleição incondicional", ["eleição", "eleitos", "escolhidos", "eleição incondicional"],
  "CFW 3.5; Cânones de Dort I",
  "Deus escolheu em Cristo, antes da fundação do mundo, os que seriam salvos. A escolha não se baseou em fé, obras ou "
  "mérito que ele previu neles, mas só no seu beneplácito; a fé e as boas obras são fruto da eleição, não a causa.",
  [("Escolhidos antes da fundação do mundo", "EPH 1:4-5; 2TH 2:13"),
   ("Não pelas obras", "ROM 9:11-13, 16; 2TI 1:9"),
   ("A fé vem da eleição", "ACT 13:48; JHN 6:37; JHN 10:26"),
   ("Deus escolhe o que é fraco", "1CO 1:27-29; DEU 7:7-8")])
D("criacao", "Criação", ["criação", "criação do nada", "seis dias", "criador"], "CFW 4; BC 9-10",
  "Deus, Pai, Filho e Espírito Santo, criou do nada o mundo e tudo o que há nele, no espaço de seis dias, e tudo era "
  "muito bom. Criou o homem e a mulher à sua imagem, em conhecimento, justiça e santidade, com a lei de Deus escrita "
  "no coração.",
  [("Deus criou todas as coisas", "GEN 1:1; HEB 11:3; REV 4:11"),
   ("O Filho e o Espírito na criação", "JHN 1:2-3; COL 1:16; GEN 1:2"),
   ("O homem à imagem de Deus", "GEN 1:26-27; ECC 7:29; EPH 4:24")])
D("providencia", "Providência", ["providência", "governo de deus", "deus no controle", "sustento"], "CFW 5; BC 11",
  "Deus sustenta, dirige e governa todas as criaturas, ações e coisas, das maiores às menores, por sua providência "
  "santíssima, sábia e poderosa. Até o mal que os homens planejam ele dirige para o bem, sem deixar de ser santo.",
  [("Deus sustenta e governa tudo", "HEB 1:3; NEH 9:6; PSA 145:15-16"),
   ("Até nas menores coisas", "MAT 10:29-31; PRO 16:33"),
   ("Até o mal, para o bem", "GEN 50:20; ROM 8:28"),
   ("Sem ser autor do pecado", "JAS 1:13-14; 1JN 2:16")])

# ------------------------------------------------------------------ pecado
D("pecado-original", "Queda e pecado original", ["pecado original", "queda", "adão", "culpa de adão"],
  "CFW 6; BC 13-19",
  "Adão foi posto como cabeça da humanidade; quando ele pecou, a culpa do seu pecado foi imputada a todos os seus "
  "descendentes, e a natureza corrompida passou a eles. Por isso todos nascem em pecado e debaixo da ira de Deus.",
  [("A queda", "GEN 3:6-8; GEN 2:16-17"),
   ("Em Adão todos pecaram", "ROM 5:12, 18-19; 1CO 15:21-22"),
   ("Nascidos em pecado", "PSA 51:5; PSA 58:3; EPH 2:3")])
D("depravacao-total", "Depravação total", ["depravação total", "incapacidade total", "morte espiritual",
  "escravidão da vontade"], "CFW 6.4; CFW 9.3; Cânones de Dort III-IV",
  "O pecado atingiu o homem inteiro: mente, vontade e afetos. Não quer dizer que cada pessoa seja tão má quanto "
  "poderia, mas que ninguém é capaz, por si mesmo, de se converter ou de fazer algo que agrade a Deus para a salvação.",
  [("Mortos nos delitos e pecados", "EPH 2:1-3; COL 2:13"),
   ("Ninguém busca a Deus", "ROM 3:10-12; PSA 14:2-3"),
   ("O coração é enganoso", "JER 17:9; GEN 6:5"),
   ("Incapaz de vir a Deus por si", "JHN 6:44; ROM 8:7-8; 1CO 2:14")])

# ------------------------------------------------------------------ alianças
D("pacto-das-obras", "Pacto das obras", ["pacto das obras", "aliança das obras", "pacto da vida", "aliança com adão"],
  "CFW 7.2; BC 12",
  "O primeiro pacto de Deus com o homem foi um pacto de obras: a vida foi prometida a Adão, e nele à sua "
  "descendência, sob a condição de obediência perfeita; a desobediência traria a morte.",
  [("A ordem e a ameaça", "GEN 2:16-17"),
   ("Faze isto e viverás", "LEV 18:5; ROM 10:5; GAL 3:10-12"),
   ("Adão como figura de Cristo", "ROM 5:12-14; HOS 6:7")])
D("pacto-da-graca", "Pacto da graça (teologia da aliança)", ["pacto da graça", "aliança da graça",
  "teologia da aliança", "teologia do pacto", "alianças", "pactos"], "CFW 7.3-6; BC 20",
  "Depois da queda, Deus fez um segundo pacto, o da graça: oferece a vida e a salvação por Jesus Cristo, pedindo fé "
  "nele, e promete dar o Espírito para que os eleitos creiam. É um só pacto, administrado de modos diferentes nas "
  "promessas, nos sacrifícios e na circuncisão do Antigo Testamento e, plenamente, no evangelho.",
  [("A primeira promessa", "GEN 3:15"),
   ("Serei o teu Deus e o da tua descendência", "GEN 17:7; JER 31:33; 2CO 6:16"),
   ("A promessa a Abraão é para os que creem", "GAL 3:7-9, 14, 16, 29; ROM 4:11"),
   ("A nova aliança", "JER 31:31-34; HEB 8:6-10; LUK 22:20"),
   ("Um só povo, uma só salvação", "ACT 15:11; HEB 11:13; ROM 11:17-18")])

# ------------------------------------------------------------------ Cristo
D("cristo-mediador", "Cristo, o único mediador", ["mediador", "duas naturezas", "encarnação", "união hipostática",
  "deus e homem", "solus christus"], "CFW 8; BC 21-22",
  "O Filho eterno de Deus se fez homem, e assim foi e continua a ser Deus e homem, em duas naturezas distintas e uma "
  "só pessoa. É o único mediador entre Deus e os homens: só por ele há salvação.",
  [("O Verbo se fez carne", "JHN 1:1, 14; GAL 4:4"),
   ("Deus e homem", "PHP 2:6-8; COL 2:9; ROM 1:3-4"),
   ("Um só mediador", "1TI 2:5; ACT 4:12; JHN 14:6"),
   ("Sem pecado, semelhante a nós", "HEB 2:14-17; HEB 4:15")])
D("oficios-de-cristo", "Os ofícios de Cristo: profeta, sacerdote e rei", ["profeta sacerdote e rei", "tríplice ofício",
  "ofícios de cristo", "sumo sacerdote"], "CFW 8.1; BC 23-26",
  "Cristo, como nosso Redentor, exerce três ofícios: é profeta, que nos revela a vontade de Deus; sacerdote, que se "
  "ofereceu uma vez em sacrifício e intercede por nós; e rei, que nos governa, defende e vence os seus inimigos.",
  [("Profeta", "DEU 18:15; ACT 3:22; JHN 1:18"),
   ("Sacerdote", "HEB 7:24-27; HEB 9:14, 28"),
   ("Rei", "PSA 2:6; ISA 9:6-7; 1CO 15:25")])
D("expiacao-limitada", "Expiação limitada (redenção particular)", ["expiação limitada", "redenção particular",
  "expiação definida", "por quem cristo morreu"], "CFW 8.5, 8.8; Cânones de Dort II",
  "Cristo, com a sua obediência e morte, satisfez plenamente a justiça do Pai e adquiriu a redenção para todos os que "
  "o Pai lhe deu. A sua morte não apenas tornou a salvação possível, mas a garantiu de fato para o seu povo. O "
  "evangelho continua a ser oferecido a todos sem distinção.",
  [("Pelas ovelhas", "JHN 10:11, 14-15, 26"),
   ("Pela sua igreja", "EPH 5:25-27; ACT 20:28"),
   ("Ele salva o seu povo", "MAT 1:21; ISA 53:11"),
   ("Os que o Pai lhe deu", "JHN 17:2, 9; JHN 6:37-39"),
   ("O evangelho é anunciado a todos", "MAT 28:19; ISA 45:22")])
D("substituicao", "Substituição penal (Cristo em nosso lugar)", ["substituição", "substituição penal", "satisfação",
  "propiciação", "expiação", "sacrifício de cristo"], "CFW 8.4-5; BC 25",
  "Na cruz, Cristo tomou o lugar do seu povo: levou sobre si o pecado e o castigo que eles mereciam e satisfez a "
  "justiça de Deus, afastando a sua ira.",
  [("Ferido pelas nossas transgressões", "ISA 53:4-6, 10"),
   ("Feito pecado por nós", "2CO 5:21; 1PE 2:24; 1PE 3:18"),
   ("Feito maldição em nosso lugar", "GAL 3:13"),
   ("Propiciação", "ROM 3:25-26; 1JN 2:2; 1JN 4:10")])

# ------------------------------------------------------------------ aplicação da salvação
D("livre-arbitrio", "Livre-arbítrio e escravidão da vontade", ["livre-arbítrio", "livre arbítrio", "vontade",
  "arminianismo", "monergismo"], "CFW 9; Cânones de Dort III-IV",
  "O homem não é forçado a pecar: escolhe o que deseja. Mas, depois da queda, a sua vontade está presa ao pecado e "
  "perdeu toda a capacidade de querer o bem espiritual que acompanha a salvação. Só quando Deus o converte é que ele "
  "passa a querer e fazer o bem.",
  [("Escravos do pecado", "JHN 8:34; ROM 6:16-20"),
   ("Ninguém pode vir se o Pai não o trouxer", "JHN 6:44, 65"),
   ("Deus é quem opera o querer", "PHP 2:13; EZK 36:26-27"),
   ("Livres de fato pelo Filho", "JHN 8:36")])
D("vocacao-eficaz", "Vocação eficaz e graça irresistível", ["vocação eficaz", "chamado eficaz", "graça irresistível",
  "graça eficaz", "regeneração", "novo nascimento", "conversão"], "CFW 10; BC 29-31",
  "Deus chama eficazmente os seus eleitos pela Palavra e pelo Espírito: ilumina a mente, tira o coração de pedra, "
  "renova a vontade e os traz a Cristo, de modo que eles vêm livremente, porque foram feitos dispostos pela graça.",
  [("Os que ele chamou, também justificou", "ROM 8:30; 2TI 1:9"),
   ("Coração novo", "EZK 36:26-27; DEU 30:6"),
   ("Nascer de novo, do Espírito", "JHN 3:3-8; JAS 1:18; 1PE 1:23"),
   ("Deus abre o coração", "ACT 16:14; 2CO 4:6"),
   ("Todos os que o Pai dá virão", "JHN 6:37, 44-45")])
D("uniao-com-cristo", "União com Cristo", ["união com cristo", "em cristo", "unidos a cristo"], "CFW 26.1; CM 66-69",
  "Pela fé e pelo Espírito, o crente é unido a Cristo: morre e ressuscita com ele, está nele e recebe dele todos os "
  "benefícios da salvação, como justificação, adoção, santificação e glorificação.",
  [("Eu nele e ele em mim", "JHN 15:4-5; JHN 17:23; GAL 2:20"),
   ("Mortos e ressuscitados com ele", "ROM 6:4-5; COL 3:1-3"),
   ("Toda bênção em Cristo", "EPH 1:3-7; 1CO 1:30")])
D("justificacao", "Justificação pela fé somente (Sola Fide)", ["justificação", "sola fide", "somente a fé",
  "imputação", "justiça imputada", "justiça de cristo", "salvação pela fé"], "CFW 11; BC 33",
  "Deus justifica gratuitamente os que chama: não infundindo neles justiça, mas perdoando os seus pecados e "
  "considerando-os justos, por causa da obediência e da morte de Cristo, imputadas a eles e recebidas só pela fé. A fé "
  "que justifica nunca fica sozinha, mas é acompanhada das demais graças.",
  [("Justificados gratuitamente pela graça", "ROM 3:22-28; TIT 3:5-7"),
   ("Pela fé, sem as obras da lei", "GAL 2:16; ROM 4:5; PHP 3:9"),
   ("A justiça de Cristo atribuída a nós", "2CO 5:21; ROM 5:17-19; ROM 4:6-8"),
   ("Abraão creu e foi considerado justo", "GEN 15:6; ROM 4:3, 22-25"),
   ("A fé verdadeira produz obras", "JAS 2:17, 22, 26; GAL 5:6")])
D("sola-gratia", "Somente a graça (Sola Gratia)", ["sola gratia", "graça", "salvação pela graça", "mérito"],
  "CFW 11.3; CFW 16.5",
  "A salvação, do começo ao fim, é presente de Deus, sem nenhum mérito do homem: até a fé com que a recebemos é dom "
  "dele.",
  [("Pela graça sois salvos", "EPH 2:8-9; TIT 3:5"),
   ("Se é pela graça, já não é pelas obras", "ROM 11:6; ROM 4:4-5"),
   ("Não depende de quem quer", "ROM 9:16; JHN 1:12-13")])
D("adocao", "Adoção", ["adoção", "filhos de deus"], "CFW 12; BC 34",
  "Os justificados são adotados como filhos de Deus: recebem o seu nome, o Espírito de adoção, acesso ao Pai, a sua "
  "proteção e correção de Pai, e a herança como co-herdeiros com Cristo.",
  [("Adotados por meio de Cristo", "EPH 1:5; GAL 4:4-7"),
   ("O Espírito clama 'Aba, Pai'", "ROM 8:15-17"),
   ("Filhos pela fé", "JHN 1:12; 1JN 3:1-2"),
   ("O Pai corrige os filhos", "HEB 12:6-10")])
D("santificacao", "Santificação", ["santificação", "santidade", "mortificação", "vida cristã"], "CFW 13; BC 35",
  "Os que foram chamados e regenerados são também santificados, de fato e pessoalmente, pela Palavra e pelo Espírito: "
  "o domínio do pecado é destruído e eles crescem em santidade. A obra é verdadeira, mas imperfeita nesta vida, numa "
  "luta contínua entre a carne e o Espírito.",
  [("É vontade de Deus", "1TH 4:3; 1TH 5:23; HEB 12:14"),
   ("Pela Palavra e pelo Espírito", "JHN 17:17; 2TH 2:13; 2CO 3:18"),
   ("O pecado não terá domínio", "ROM 6:6, 14; COL 3:5, 10"),
   ("Luta contínua", "GAL 5:17; ROM 7:18-25; 1JN 1:8"),
   ("Deus completa a obra", "PHP 1:6; PHP 2:12-13")])
D("fe-salvadora", "Fé salvadora", ["fé", "fé salvadora", "crer", "confiança em cristo"], "CFW 14; BC 86",
  "A fé que salva é dom de Deus, produzida pelo Espírito por meio da Palavra. Seu ato principal é aceitar, receber e "
  "descansar somente em Cristo para a justificação, a santificação e a vida eterna.",
  [("A fé é dom de Deus", "EPH 2:8; PHP 1:29"),
   ("Vem pelo ouvir a Palavra", "ROM 10:14, 17"),
   ("Receber a Cristo e descansar nele", "JHN 1:12; ACT 16:31; GAL 2:20"),
   ("O que é a fé", "HEB 11:1, 6")])
D("arrependimento", "Arrependimento para a vida", ["arrependimento", "conversão", "contrição"], "CFW 15; BC 87",
  "Arrependimento é graça do evangelho: o pecador, vendo o perigo e a feiura do pecado e a misericórdia de Deus em "
  "Cristo, se entristece, odeia o pecado e se volta dele para Deus, decidido a andar em obediência.",
  [("Deus concede o arrependimento", "ACT 11:18; 2TI 2:25"),
   ("Tristeza segundo Deus", "2CO 7:10-11; PSA 51:3-4, 17"),
   ("Voltar-se do pecado para Deus", "EZK 18:30-31; ISA 55:7; ACT 26:20"),
   ("Arrependimento e fé andam juntos", "MRK 1:15; ACT 20:21")])
D("boas-obras", "Boas obras", ["boas obras", "obras", "fruto da fé"], "CFW 16",
  "Boas obras são as que Deus ordenou na sua Palavra, não as inventadas pelos homens. São fruto e prova da fé "
  "verdadeira e glorificam a Deus, mas não merecem a salvação, porque mesmo as melhores ainda são imperfeitas.",
  [("Criados em Cristo para as boas obras", "EPH 2:10; TIT 2:14"),
   ("Para a glória de Deus", "MAT 5:16; 1CO 10:31"),
   ("Não por obras de justiça que fizemos", "TIT 3:5; ISA 64:6"),
   ("Somos servos inúteis", "LUK 17:10; ROM 3:20")])
D("perseveranca", "Perseverança dos santos", ["perseverança dos santos", "segurança eterna", "uma vez salvo",
  "salvação não se perde"], "CFW 17; Cânones de Dort V",
  "Os que Deus aceitou em Cristo e santificou pelo Espírito não podem cair total nem finalmente do estado de graça: "
  "perseverarão até o fim e serão salvos. A firmeza não depende da vontade deles, mas da eleição, da intercessão de "
  "Cristo e da habitação do Espírito. Podem cair em pecados graves por um tempo, mas são restaurados.",
  [("Ninguém as arrebatará da minha mão", "JHN 10:27-29; JHN 6:39"),
   ("Nada nos separará do amor de Deus", "ROM 8:30, 35-39"),
   ("Deus completará a obra", "PHP 1:6; 1PE 1:5"),
   ("Selados pelo Espírito", "EPH 1:13-14; EPH 4:30"),
   ("Cristo intercede", "LUK 22:32; HEB 7:25")])
D("certeza-da-salvacao", "Certeza da salvação", ["certeza da salvação", "segurança da salvação", "assurance"],
  "CFW 18; BC 36",
  "Os que creem verdadeiramente podem ter, nesta vida, a certeza de que estão em estado de graça, firmada nas "
  "promessas de Deus, nas evidências da graça e no testemunho do Espírito. A certeza pode ser abalada, mas nunca se "
  "perde de todo, e é dever buscá-la.",
  [("Para que saibais que tendes a vida eterna", "1JN 5:13; 1JN 3:14, 24"),
   ("O Espírito testemunha", "ROM 8:15-16"),
   ("Procurai confirmar a vossa vocação", "2PE 1:10; HEB 6:11"),
   ("Pode ser abalada e restaurada", "PSA 51:8, 12; PSA 77:1-10")])

# ------------------------------------------------------------------ lei, liberdade e culto
D("lei-de-deus", "Lei de Deus e seus três usos", ["lei", "dez mandamentos", "lei moral", "três usos da lei",
  "antinomismo", "decálogo"], "CFW 19; BC 39-84",
  "A lei moral, resumida nos Dez Mandamentos, obriga todos para sempre. O crente não está debaixo dela como pacto de "
  "obras para ser justificado, mas ela lhe serve de regra de vida. Também mostra o pecado e leva a Cristo, e refreia "
  "o mal na sociedade. As leis cerimoniais e civis de Israel tiveram seu fim.",
  [("Os Dez Mandamentos", "EXO 20:1-17; DEU 5:6-21"),
   ("A lei mostra o pecado e leva a Cristo", "ROM 3:20; ROM 7:7; GAL 3:24"),
   ("Regra de vida para o crente", "ROM 3:31; ROM 13:8-10; 1JN 5:3"),
   ("Não estamos debaixo da lei para justificação", "ROM 6:14; GAL 2:16"),
   ("As cerimônias eram sombra de Cristo", "COL 2:16-17; HEB 10:1")])
D("liberdade-crista", "Liberdade cristã e liberdade de consciência", ["liberdade cristã", "liberdade de consciência",
  "legalismo", "adiáfora"], "CFW 20",
  "Cristo libertou os crentes da culpa do pecado, da condenação da lei e do jugo das cerimônias. Só Deus é Senhor da "
  "consciência: ela fica livre das doutrinas e mandamentos humanos contrários ou acrescentados à Palavra. A liberdade "
  "não é licença para pecar.",
  [("Estai firmes na liberdade", "GAL 5:1, 13; JHN 8:36"),
   ("Não sujeitos a mandamentos de homens", "COL 2:20-23; MAT 15:9; ACT 4:19"),
   ("Não use a liberdade para pecar", "1PE 2:16; ROM 6:1-2"),
   ("Cuidado com o irmão fraco", "ROM 14:1-6, 13-23; 1CO 8:9")])
D("principio-regulador", "Princípio regulador do culto", ["princípio regulador", "culto", "adoração", "liturgia",
  "culto a deus", "culto bíblico"], "CFW 21.1; BC 50-51",
  "O modo aceitável de adorar a Deus foi instituído por ele mesmo e está limitado à sua vontade revelada: não deve ser "
  "adorado segundo invenções humanas, nem por imagens, nem de qualquer modo que a Escritura não prescreva. Fazem parte "
  "do culto a leitura e a pregação da Palavra, a oração, o canto, os sacramentos e as ofertas.",
  [("Não acrescentarás nem diminuirás", "DEU 12:32; DEU 4:2"),
   ("Fogo estranho", "LEV 10:1-3"),
   ("Não farás imagem para adorar", "EXO 20:4-6; DEU 4:15-16"),
   ("Em espírito e em verdade", "JHN 4:23-24"),
   ("Culto inventado é vão", "MAT 15:9; COL 2:23"),
   ("Os elementos do culto", "ACT 2:42; COL 3:16; 1TI 4:13; 1CO 11:23-26")])
D("dia-do-senhor", "Dia do Senhor (o sábado cristão)", ["dia do senhor", "domingo", "sábado cristão",
  "quarto mandamento", "guardar o domingo"], "CFW 21.7-8; BC 57-62",
  "Deus separou um dia em sete para ser santo para ele. Desde a criação até a ressurreição de Cristo era o sétimo dia; "
  "desde a ressurreição, é o primeiro dia da semana, o Dia do Senhor, que deve ser guardado para o culto público e "
  "particular, deixando os trabalhos e as recreações comuns, exceto as obras de necessidade e de misericórdia.",
  [("Lembra-te do dia de descanso", "EXO 20:8-11; GEN 2:2-3"),
   ("Chamarás ao sábado deleitoso", "ISA 58:13-14"),
   ("O primeiro dia da semana, dia da ressurreição", "MAT 28:1; JHN 20:19, 26"),
   ("A igreja se reunia no primeiro dia", "ACT 20:7; 1CO 16:1-2; REV 1:10"),
   ("Obras de necessidade e misericórdia", "MAT 12:1-13; MRK 2:27-28")])
D("juramentos-e-votos", "Juramentos e votos", ["juramento", "votos", "jurar"], "CFW 22",
  "O juramento legítimo é parte do culto: em assunto grave, invoca-se a Deus como testemunha da verdade. Só se deve "
  "jurar pelo nome de Deus, com verdade e para cumprir. Os votos são feitos só a Deus e devem ser cumpridos.",
  [("Pelo nome de Deus jurarás", "DEU 6:13; DEU 10:20"),
   ("Juramento em causa justa", "HEB 6:16; 2CO 1:23"),
   ("Não jurar em vão nem por qualquer coisa", "EXO 20:7; MAT 5:34-37; JAS 5:12"),
   ("Cumprir o voto", "ECC 5:4-5; PSA 76:11")])
D("magistrado-civil", "O magistrado civil (governo e Estado)", ["governo", "estado", "magistrado", "autoridades",
  "igreja e estado", "política"], "CFW 23",
  "Deus instituiu as autoridades civis para a sua glória e o bem público, para proteger os bons e punir os maus. Os "
  "cristãos devem orar por elas, honrá-las, pagar impostos e obedecer-lhes no que é lícito; as autoridades, por sua "
  "vez, não podem tomar para si a pregação da Palavra, os sacramentos ou as chaves do reino.",
  [("As autoridades foram instituídas por Deus", "ROM 13:1-7; 1PE 2:13-14"),
   ("Orar pelas autoridades", "1TI 2:1-2"),
   ("Dai a César o que é de César", "MAT 22:21"),
   ("Importa obedecer a Deus", "ACT 4:19; ACT 5:29"),
   ("O rei não pode usurpar o culto", "2CH 26:18-19")])
D("casamento", "Casamento e divórcio", ["casamento", "matrimônio", "divórcio", "família"], "CFW 24",
  "O casamento é a união de um homem e uma mulher, instituída por Deus para a ajuda mútua, a continuação da "
  "humanidade e da igreja e para evitar a impureza. O crente deve casar-se no Senhor. O divórcio só é legítimo por "
  "adultério ou por abandono que nenhum meio pode remediar.",
  [("Instituído na criação", "GEN 2:18, 24; MAT 19:4-6"),
   ("Um só marido e uma só mulher", "MAL 2:15; 1CO 7:2"),
   ("Casar-se somente no Senhor", "1CO 7:39; 2CO 6:14"),
   ("Divórcio por infidelidade", "MAT 5:31-32; MAT 19:8-9"),
   ("Abandono", "1CO 7:15"),
   ("Cristo e a igreja", "EPH 5:22-33")])

# ------------------------------------------------------------------ igreja
D("igreja", "A igreja visível e invisível", ["igreja", "igreja invisível", "igreja visível", "eclesiologia",
  "corpo de cristo", "noiva de cristo"], "CFW 25",
  "A igreja invisível é o conjunto de todos os eleitos, reunidos em Cristo, a cabeça. A igreja visível é formada por "
  "todos os que professam a verdadeira fé, com os seus filhos; a ela Cristo deu o ministério, a Palavra e os "
  "sacramentos. Cristo é o único cabeça da igreja.",
  [("A igreja, corpo e noiva de Cristo", "EPH 1:22-23; EPH 5:23-27; COL 1:18"),
   ("Os que professam e os seus filhos", "1CO 1:2; 1CO 7:14; ACT 2:39"),
   ("O ministério dado à igreja", "EPH 4:11-13; MAT 28:19-20"),
   ("Nem todos os de dentro são verdadeiros", "MAT 13:24-30, 47; 1JN 2:19")])
D("sacerdocio-dos-crentes", "Sacerdócio de todos os crentes", ["sacerdócio universal", "sacerdócio dos crentes",
  "sacerdócio de todos os crentes"], "Princípio da Reforma; CFW 26",
  "Todo crente tem acesso direto a Deus por meio de Cristo, o único sumo sacerdote, sem outro mediador humano, e é "
  "chamado a oferecer a Deus sacrifícios espirituais e a servir os irmãos com os seus dons. Isso não elimina os "
  "ofícios que Cristo deu à igreja.",
  [("Sacerdócio real", "1PE 2:5, 9; REV 1:5-6"),
   ("Acesso direto pelo sangue de Cristo", "HEB 4:14-16; HEB 10:19-22"),
   ("Um só mediador", "1TI 2:5"),
   ("Sacrifícios espirituais", "ROM 12:1; HEB 13:15-16")])
D("comunhao-dos-santos", "Comunhão dos santos", ["comunhão dos santos", "comunhão", "unidade da igreja"], "CFW 26",
  "Unidos a Cristo, os crentes estão unidos uns aos outros em amor: participam dos dons e das graças uns dos outros e "
  "devem ajudar-se no culto, no crescimento espiritual e nas necessidades materiais.",
  [("Comunhão com o Pai, com o Filho e entre nós", "1JN 1:3, 7"),
   ("Um só corpo, muitos membros", "1CO 12:12-27; ROM 12:4-5"),
   ("Perseveravam na comunhão", "ACT 2:42-45; HEB 10:24-25"),
   ("Levai as cargas uns dos outros", "GAL 6:2, 10; 1JN 3:17")])
D("governo-presbiteriano", "Governo presbiteriano da igreja", ["presbiterianismo", "governo da igreja",
  "presbíteros", "concílio", "presbitério", "sínodo", "conselho da igreja", "presbiteriana"], "CFW 30-31",
  "Cristo, o único rei e cabeça da igreja, a governa por meio de oficiais: presbíteros (anciãos), eleitos e "
  "ordenados, que governam em conjunto, e não por um único homem. As igrejas se reúnem em concílios maiores, como o "
  "de Jerusalém, para decidir questões de doutrina e de disciplina à luz da Palavra.",
  [("Presbíteros em cada igreja", "ACT 14:23; TIT 1:5; ACT 20:17, 28"),
   ("Presbíteros que governam e que ensinam", "1TI 5:17; 1TH 5:12-13; HEB 13:17"),
   ("O concílio de Jerusalém", "ACT 15:2, 6, 22-23, 28-29; ACT 16:4"),
   ("A imposição de mãos do presbitério", "1TI 4:14"),
   ("Cristo é o único cabeça", "EPH 1:22; COL 1:18; MAT 23:8-10")])
D("oficiais-da-igreja", "Ofícios da igreja: presbíteros e diáconos", ["oficiais", "presbítero", "diácono",
  "pastor", "bispo", "ordenação", "ministro"], "Forma de governo presbiteriana; CFW 31",
  "O Novo Testamento apresenta os ofícios permanentes da igreja: presbíteros (também chamados bispos), que pastoreiam, "
  "ensinam e governam, e diáconos, que cuidam do serviço e das necessidades. As qualificações estão nas cartas a "
  "Timóteo e a Tito.",
  [("Presbítero e bispo, o mesmo ofício", "ACT 20:17, 28; TIT 1:5-7; 1PE 5:1-3"),
   ("Qualificações do presbítero", "1TI 3:1-7; TIT 1:5-9"),
   ("Qualificações do diácono", "1TI 3:8-13; ACT 6:1-6"),
   ("Pastores e mestres dados por Cristo", "EPH 4:11-12")])
D("disciplina", "Disciplina da igreja", ["disciplina", "disciplina eclesiástica", "excomunhão", "chaves do reino",
  "censura"], "CFW 30",
  "Cristo deu aos oficiais da igreja as chaves do reino: admitir e excluir, corrigir e restaurar. A disciplina "
  "existe para recuperar o irmão que caiu, proteger a igreja e honrar a Cristo, e vai da admoestação à exclusão.",
  [("As chaves do reino", "MAT 16:19; MAT 18:17-18; JHN 20:21-23"),
   ("O passo a passo", "MAT 18:15-17"),
   ("Afastar o que vive em pecado", "1CO 5:4-5, 11-13; 2TH 3:6, 14-15"),
   ("Para restaurar", "GAL 6:1; 2CO 2:6-8; 1TI 5:20")])

# ------------------------------------------------------------------ sacramentos
D("sacramentos", "Sacramentos (meios de graça)", ["sacramentos", "meios de graça", "ordenanças", "selos"],
  "CFW 27; BC 88, 91-93",
  "Os sacramentos são sinais e selos santos do pacto da graça, instituídos por Cristo, que representam Cristo e os "
  "seus benefícios e confirmam o nosso interesse nele. Não têm poder em si mesmos: tornam-se eficazes pela bênção de "
  "Cristo e pela ação do Espírito nos que os recebem com fé. No Novo Testamento são dois: o batismo e a Ceia do "
  "Senhor.",
  [("Sinal e selo da justiça da fé", "ROM 4:11; GEN 17:7, 10"),
   ("Instituídos por Cristo", "MAT 28:19; 1CO 11:23-26"),
   ("O sinal não salva por si", "1PE 3:21; ROM 2:28-29; 1CO 10:1-5"),
   ("Os meios de graça", "ACT 2:41-42")])
D("batismo", "Batismo", ["batismo", "aspersão", "modo do batismo", "batismo nas águas"], "CFW 28; BC 94",
  "O batismo é o sacramento que sinaliza e sela a união com Cristo, a purificação dos pecados, a regeneração e a "
  "entrada na igreja visível. É feito com água, em nome do Pai, do Filho e do Espírito Santo. A imersão não é "
  "necessária: o batismo é corretamente ministrado por aspersão ou efusão. Não deve ser repetido.",
  [("A ordem de batizar", "MAT 28:19-20; MRK 16:16"),
   ("Sinal da união com Cristo", "ROM 6:3-5; GAL 3:27; COL 2:11-12"),
   ("Sinal da purificação e do Espírito", "ACT 2:38; ACT 22:16; TIT 3:5"),
   ("Aspersão e derramamento nas Escrituras", "EZK 36:25; HEB 10:22; ACT 2:17, 33; HEB 9:10, 13, 19"),
   ("Um só batismo", "EPH 4:5")])
D("pedobatismo", "Batismo infantil (pedobatismo)", ["batismo infantil", "pedobatismo", "batismo de crianças",
  "batismo de bebês", "batismo de recém-nascidos", "filhos dos crentes"], "CFW 28.4; Catecismo Maior 166; BC 95",
  "Não só os que professam a fé devem ser batizados, mas também os filhos pequenos dos crentes. A razão é o pacto: "
  "Deus prometeu ser o Deus dos crentes e da sua descendência, e a circuncisão, sinal desse pacto, era dada aos "
  "meninos de oito dias. No Novo Testamento, a promessa continua sendo 'para vós e para vossos filhos', os filhos de "
  "um crente são chamados santos, e casas inteiras foram batizadas. O batismo ocupa o lugar da circuncisão como "
  "sinal do mesmo pacto.",
  [("A promessa é para os crentes e seus filhos", "GEN 17:7; ACT 2:38-39"),
   ("O sinal do pacto era dado às crianças", "GEN 17:10-14; GEN 21:4"),
   ("O batismo ocupa o lugar da circuncisão", "COL 2:11-12; ROM 4:11; GAL 3:7-9, 14, 29"),
   ("Os filhos de crente são santos", "1CO 7:14"),
   ("Casas inteiras batizadas", "ACT 16:14-15; ACT 16:31-34; 1CO 1:16"),
   ("Jesus recebe as crianças no reino", "MRK 10:13-16; LUK 18:15-16"),
   ("As crianças fazem parte do povo da aliança", "DEU 29:10-13; JOL 2:16; EPH 6:1-4")])
D("ceia-do-senhor", "Ceia do Senhor", ["santa ceia", "ceia do senhor", "eucaristia", "comunhão", "presença real",
  "transubstanciação"], "CFW 29; BC 96-97",
  "Na Ceia, instituída por Cristo na noite em que foi traído, o pão e o vinho são dados e recebidos em memória da "
  "sua morte. Os elementos continuam sendo pão e vinho (não há transubstanciação, e a Ceia não é sacrifício repetido), "
  "mas os que comem com fé recebem e se alimentam de Cristo crucificado, de modo real porém espiritual, pela ação do "
  "Espírito. Cada um deve examinar-se antes de participar.",
  [("A instituição", "MAT 26:26-28; 1CO 11:23-26"),
   ("Comunhão com o corpo e o sangue de Cristo", "1CO 10:16-17"),
   ("Um só sacrifício, uma vez por todas", "HEB 9:25-28; HEB 10:10-14"),
   ("Em memória e anúncio da sua morte", "LUK 22:19-20; 1CO 11:26"),
   ("Examine-se cada um", "1CO 11:27-29")])

# ------------------------------------------------------------------ últimas coisas
D("estado-intermediario", "Morte e estado intermediário", ["morte", "estado intermediário", "alma após a morte",
  "purgatório", "céu", "o que acontece depois da morte"], "CFW 32.1; BC 37",
  "Na morte, o corpo volta ao pó, mas a alma não morre nem dorme: a dos justos, feita perfeita em santidade, vai "
  "imediatamente para a presença de Cristo, esperando a redenção do corpo; a dos ímpios vai para o tormento. As "
  "Escrituras não conhecem outro lugar, como o purgatório.",
  [("O pó volta à terra, o espírito a Deus", "ECC 12:7; GEN 3:19"),
   ("Hoje estarás comigo no paraíso", "LUK 23:43; PHP 1:23; 2CO 5:6-8"),
   ("Os espíritos dos justos aperfeiçoados", "HEB 12:23; REV 14:13"),
   ("Os ímpios em tormento", "LUK 16:22-26")])
D("ressurreicao", "Ressurreição do corpo", ["ressurreição", "ressurreição dos mortos", "corpo glorificado"],
  "CFW 32.2-3; BC 38",
  "No último dia, os mortos ressuscitarão com o mesmo corpo, transformado: os justos, para a honra, num corpo "
  "glorioso semelhante ao de Cristo; os injustos, para a desonra e a condenação.",
  [("Justos e injustos ressuscitarão", "JHN 5:28-29; ACT 24:15; DAN 12:2"),
   ("Corpo transformado, como o de Cristo", "1CO 15:42-44, 51-54; PHP 3:21"),
   ("Cristo, as primícias", "1CO 15:20-23; 1TH 4:14-17")])
D("juizo-final", "Juízo final", ["juízo final", "julgamento", "dia do juízo", "inferno", "condenação eterna",
  "vida eterna"], "CFW 33",
  "Deus marcou um dia em que julgará o mundo com justiça por meio de Jesus Cristo. Todos comparecerão diante dele; os "
  "justos receberão a vida eterna, por graça, e os ímpios, o castigo eterno. O dia é desconhecido, para que vivamos "
  "vigiando.",
  [("Um dia marcado, por meio de Cristo", "ACT 17:31; JHN 5:22, 27"),
   ("Todos comparecerão", "2CO 5:10; ROM 14:10-12; ECC 12:14"),
   ("Vida eterna e castigo eterno", "MAT 25:31-46; 2TH 1:7-10"),
   ("Ninguém sabe o dia: vigiai", "MAT 24:36, 42-44; MRK 13:32-37")])
