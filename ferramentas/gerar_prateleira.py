"""Catálogo da prateleira do perfil (data/prateleira.json): clássicos da teologia cristã (sobretudo da tradição
reformada), da filosofia, da apologética, da vida devocional, da literatura cristã e biografias e história da igreja,
que a pessoa marca como lido, lendo ou "quero ler" (ela também pode pôr qualquer outro livro à mão).

Cada obra traz a ligação teológica com o acervo do Sola ("liga": páginas das confissões, livros e capítulos da
Bíblia comentados por ela). Só fatos públicos — título, autor, ano, tradição —, sem texto das obras. O script confere
que cada página ligada existe no site gerado (rode depois do gerar_paginas.py).
uso:  python3 ferramentas/gerar_prateleira.py"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "data" / "prateleira.json"
TRADICOES = {   # id -> (nome pt, en, es)
    "antiga": ("Igreja antiga", "Early church", "Iglesia antigua"),
    "medieval": ("Idade Média", "Middle Ages", "Edad Media"),
    "reforma": ("Reforma", "Reformation", "Reforma"),
    "puritanos": ("Puritanos e ortodoxia reformada", "Puritans and Reformed orthodoxy", "Puritanos y ortodoxia reformada"),
    "avivamento": ("Avivamentos e séc. XIX", "Revivals and 19th century", "Avivamientos y siglo XIX"),
    "moderna": ("Séculos XX e XXI", "20th and 21st centuries", "Siglos XX y XXI"),
    "filosofia": ("Filosofia", "Philosophy", "Filosofía"),
    "apologetica": ("Apologética", "Apologetics", "Apologética"),
    "devocional": ("Vida cristã e devocionais", "Christian life and devotionals", "Vida cristiana y devocionales"),
    "literatura": ("Literatura cristã", "Christian literature", "Literatura cristiana"),
    "biografia": ("Biografias e história da igreja", "Biographies and church history", "Biografías e historia de la iglesia"),
}
# grupos do filtro do catálogo: a teologia junta as seis tradições
GRUPO = {"antiga": "teologia", "medieval": "teologia", "reforma": "teologia", "puritanos": "teologia", "avivamento": "teologia",
         "moderna": "teologia", "filosofia": "filosofia", "apologetica": "apologetica", "devocional": "devocional",
         "literatura": "literatura", "biografia": "biografia"}
# (id, título em português, título original, autor, ano, tradição, [(rótulo, endereço no Sola)])
OBRAS = [
    ("contra-heresias", "Contra as Heresias", "Adversus Haereses", "Ireneu de Lião", "c. 180", "antiga",
     [("Credo Apostólico", "/confissoes/credos/apostolico/")]),
    ("encarnacao-verbo", "Sobre a Encarnação do Verbo", "De Incarnatione", "Atanásio de Alexandria", "c. 318", "antiga",
     [("Credo Niceno", "/confissoes/credos/niceno/"), ("João 1:14", "/biblia/joao/1/14/")]),
    ("confissoes-agostinho", "Confissões", "Confessiones", "Agostinho de Hipona", "c. 400", "antiga",
     [("Romanos 13:14", "/biblia/romanos/13/14/"), ("CFW 9: Do livre-arbítrio", "/confissoes/westminster/9/")]),
    ("cidade-de-deus", "A Cidade de Deus", "De Civitate Dei", "Agostinho de Hipona", "426", "antiga",
     [("CFW 5: Da providência", "/confissoes/westminster/5/")]),
    ("cur-deus-homo", "Por que Deus se fez homem", "Cur Deus Homo", "Anselmo de Cantuária", "1098", "medieval",
     [("Heidelberg, pergunta 12", "/confissoes/heidelberg/12/"), ("Confissão Belga, artigo 20", "/confissoes/confissao-belga/20/")]),
    ("imitacao-cristo", "A Imitação de Cristo", "De Imitatione Christi", "Tomás de Kempis", "c. 1427", "medieval", []),
    ("liberdade-crista", "Da Liberdade Cristã", "Von der Freiheit eines Christenmenschen", "Martinho Lutero", "1520", "reforma",
     [("CFW 20: Da liberdade cristã", "/confissoes/westminster/20/")]),
    ("escravidao-vontade", "A Escravidão da Vontade", "De Servo Arbitrio", "Martinho Lutero", "1525", "reforma",
     [("CFW 9: Do livre-arbítrio", "/confissoes/westminster/9/"), ("Confissão Belga, artigo 14", "/confissoes/confissao-belga/14/")]),
    ("galatas-lutero", "Comentário de Gálatas", "In Epistolam ad Galatas", "Martinho Lutero", "1535", "reforma",
     [("Gálatas", "/biblia/galatas/"), ("CFW 11: Da justificação", "/confissoes/westminster/11/")]),
    ("loci-melanchthon", "Loci Communes", "Loci Communes", "Filipe Melanchthon", "1521", "reforma", []),
    ("institutas", "Institutas da Religião Cristã", "Institutio Christianae Religionis", "João Calvino", "1559", "reforma",
     [("Comentário de Calvino em Romanos", "/biblia/romanos/1/"), ("Confissão de Westminster", "/confissoes/westminster/")]),
    ("calvino-romanos", "Comentário de Romanos", "Commentarius in Epistolam ad Romanos", "João Calvino", "1540", "reforma",
     [("Romanos, com o comentário de Calvino", "/biblia/romanos/")]),
    ("calvino-salmos", "Comentário dos Salmos", "In Librum Psalmorum Commentarius", "João Calvino", "1557", "reforma",
     [("Salmos, com o comentário de Calvino", "/biblia/salmos/")]),
    ("confissao-belga", "Confissão Belga", "Confession de foi", "Guido de Brès", "1561", "reforma",
     [("Confissão Belga no Sola", "/confissoes/confissao-belga/")]),
    ("heidelberg", "Catecismo de Heidelberg", "Heidelberger Katechismus", "Zacarias Ursino e Gaspar Oleviano", "1563", "reforma",
     [("Catecismo de Heidelberg no Sola", "/confissoes/heidelberg/")]),
    ("ursino-comentario", "Comentário ao Catecismo de Heidelberg", "Explicationes Catecheseos", "Zacarias Ursino", "1591", "reforma",
     [("Catecismo de Heidelberg", "/confissoes/heidelberg/")]),
    ("helvetica-segunda", "Segunda Confissão Helvética", "Confessio Helvetica Posterior", "Heinrich Bullinger", "1566", "reforma", []),
    ("dort", "Cânones de Dort", "Canones Synodi Dordrechtanae", "Sínodo de Dort", "1619", "puritanos",
     [("Cânones de Dort no Sola", "/confissoes/canones-de-dort/")]),
    ("westminster", "Confissão de Fé de Westminster", "The Westminster Confession of Faith", "Assembleia de Westminster", "1647", "puritanos",
     [("Confissão de Westminster no Sola", "/confissoes/westminster/")]),
    ("breve-catecismo", "Breve Catecismo de Westminster", "The Shorter Catechism", "Assembleia de Westminster", "1647", "puritanos",
     [("Breve Catecismo no Sola", "/confissoes/breve-catecismo/")]),
    ("morte-da-morte", "A Morte da Morte na Morte de Cristo", "The Death of Death in the Death of Christ", "John Owen", "1647", "puritanos",
     [("Cânones de Dort, capítulo 2", "/confissoes/canones-de-dort/2/"), ("CFW 8: De Cristo, o Mediador", "/confissoes/westminster/8/")]),
    ("mortificacao", "A Mortificação do Pecado", "Of the Mortification of Sin in Believers", "John Owen", "1656", "puritanos",
     [("Romanos 8:13", "/biblia/romanos/8/13/"), ("CFW 13: Da santificação", "/confissoes/westminster/13/")]),
    ("comunhao-com-deus", "Comunhão com Deus", "Of Communion with God", "John Owen", "1657", "puritanos",
     [("1 João 1:3", "/biblia/1-joao/1/3/")]),
    ("pastor-reformado", "O Pastor Reformado", "The Reformed Pastor", "Richard Baxter", "1656", "puritanos",
     [("Atos 20:28", "/biblia/atos/20/28/")]),
    ("descanso-eterno", "O Descanso Eterno dos Santos", "The Saints' Everlasting Rest", "Richard Baxter", "1650", "puritanos",
     [("Hebreus 4:9", "/biblia/hebreus/4/9/")]),
    ("armadura", "O Cristão em Completa Armadura", "The Christian in Complete Armour", "William Gurnall", "1655", "puritanos",
     [("Efésios 6", "/biblia/efesios/6/")]),
    ("remedios-preciosos", "Remédios Preciosos contra as Artimanhas de Satanás", "Precious Remedies Against Satan's Devices",
     "Thomas Brooks", "1652", "puritanos", [("2 Coríntios 2:11", "/biblia/2-corintios/2/11/")]),
    ("peregrino", "O Peregrino", "The Pilgrim's Progress", "John Bunyan", "1678", "puritanos",
     [("Hebreus 11:13", "/biblia/hebreus/11/13/")]),
    ("graca-abundante", "Graça Abundante ao Principal dos Pecadores", "Grace Abounding to the Chief of Sinners", "John Bunyan",
     "1666", "puritanos", [("1 Timóteo 1:15", "/biblia/1-timoteo/1/15/")]),
    ("corpo-divindade", "Um Corpo de Divindade", "A Body of Divinity", "Thomas Watson", "1692", "puritanos",
     [("Breve Catecismo", "/confissoes/breve-catecismo/")]),
    ("arrependimento-watson", "A Doutrina do Arrependimento", "The Doctrine of Repentance", "Thomas Watson", "1668", "puritanos",
     [("CFW 15: Do arrependimento", "/confissoes/westminster/15/")]),
    ("turretini", "Institutas de Teologia Elêntica", "Institutio Theologiae Elencticae", "François Turretini", "1679–1685", "puritanos",
     [("Confissão de Westminster", "/confissoes/westminster/")]),
    ("witsius", "A Economia das Alianças", "De Oeconomia Foederum Dei", "Herman Witsius", "1677", "puritanos",
     [("CFW 7: Do pacto de Deus", "/confissoes/westminster/7/")]),
    ("brakel", "O Culto Racional do Cristão", "Redelijke Godsdienst", "Wilhelmus à Brakel", "1700", "puritanos", []),
    ("henry-comentario", "Comentário Bíblico", "Exposition of the Old and New Testaments", "Matthew Henry", "1706", "puritanos",
     [("Juízes, com o comentário de Henry", "/biblia/juizes/")]),
    ("afeicoes-religiosas", "As Afeições Religiosas", "A Treatise Concerning Religious Affections", "Jonathan Edwards", "1746", "avivamento",
     [("1 Pedro 1:8", "/biblia/1-pedro/1/8/")]),
    ("liberdade-vontade", "A Liberdade da Vontade", "Freedom of the Will", "Jonathan Edwards", "1754", "avivamento",
     [("CFW 9: Do livre-arbítrio", "/confissoes/westminster/9/")]),
    ("pecadores-maos", "Pecadores nas Mãos de um Deus Irado", "Sinners in the Hands of an Angry God", "Jonathan Edwards", "1741", "avivamento",
     [("Deuteronômio 32:35", "/biblia/deuteronomio/32/35/")]),
    ("mcheyne", "Memórias e Sermões", "Memoir and Remains", "Robert Murray M'Cheyne (org. Andrew Bonar)", "1844", "avivamento", []),
    ("hodge-sistematica", "Teologia Sistemática", "Systematic Theology", "Charles Hodge", "1871–1873", "avivamento",
     [("Confissão de Westminster", "/confissoes/westminster/")]),
    ("aa-hodge", "Esboços de Teologia", "Outlines of Theology", "A. A. Hodge", "1860", "avivamento",
     [("Confissão de Westminster", "/confissoes/westminster/")]),
    ("tudo-de-graca", "Tudo de Graça", "All of Grace", "Charles H. Spurgeon", "1886", "avivamento",
     [("Efésios 2:8", "/biblia/efesios/2/8/")]),
    ("licoes-alunos", "Lições aos Meus Alunos", "Lectures to My Students", "Charles H. Spurgeon", "1875", "avivamento", []),
    ("tesouro-davi", "O Tesouro de Davi", "The Treasury of David", "Charles H. Spurgeon", "1869–1885", "avivamento",
     [("Salmos", "/biblia/salmos/")]),
    ("santidade-ryle", "Santidade", "Holiness", "J. C. Ryle", "1877", "avivamento",
     [("Hebreus 12:14", "/biblia/hebreus/12/14/"), ("CFW 13: Da santificação", "/confissoes/westminster/13/")]),
    ("calvinismo-kuyper", "Calvinismo", "Lectures on Calvinism", "Abraham Kuyper", "1898", "avivamento", []),
    ("bavinck", "Dogmática Reformada", "Gereformeerde Dogmatiek", "Herman Bavinck", "1895–1901", "moderna",
     [("Confissão Belga", "/confissoes/confissao-belga/")]),
    ("machen", "Cristianismo e Liberalismo", "Christianity and Liberalism", "J. Gresham Machen", "1923", "moderna", []),
    ("berkhof", "Teologia Sistemática", "Systematic Theology", "Louis Berkhof", "1938", "moderna",
     [("Confissão de Westminster", "/confissoes/westminster/")]),
    ("murray-redencao", "Redenção Consumada e Aplicada", "Redemption Accomplished and Applied", "John Murray", "1955", "moderna",
     [("CFW 10: Da vocação eficaz", "/confissoes/westminster/10/"), ("Romanos 8:30", "/biblia/romanos/8/30/")]),
    ("mero-cristianismo", "Cristianismo Puro e Simples", "Mere Christianity", "C. S. Lewis", "1952", "moderna", []),
    ("tozer", "O Conhecimento do Santo", "The Knowledge of the Holy", "A. W. Tozer", "1961", "moderna",
     [("CFW 2: De Deus e da Santíssima Trindade", "/confissoes/westminster/2/")]),
    ("packer", "O Conhecimento de Deus", "Knowing God", "J. I. Packer", "1973", "moderna",
     [("Jeremias 9:24", "/biblia/jeremias/9/24/")]),
    ("sproul-santidade", "A Santidade de Deus", "The Holiness of God", "R. C. Sproul", "1985", "moderna",
     [("Isaías 6", "/biblia/isaias/6/")]),
    ("stott-cruz", "A Cruz de Cristo", "The Cross of Christ", "John Stott", "1986", "moderna",
     [("Confissão Belga, artigo 21", "/confissoes/confissao-belga/21/")]),
    ("lloyd-jones", "Depressão Espiritual", "Spiritual Depression", "D. Martyn Lloyd-Jones", "1965", "moderna",
     [("Salmo 42", "/biblia/salmos/42/")]),
    ("suma-teologica", "Suma Teológica", "Summa Theologiae", "Tomás de Aquino", "1265–1274", "medieval",
     [("CFW 2: De Deus e da Santíssima Trindade", "/confissoes/westminster/2/")]),
    # filosofia
    ("apologia-socrates", "Apologia de Sócrates", "Ἀπολογία Σωκράτους", "Platão", "c. 399 a.C.", "filosofia", []),
    ("republica", "A República", "Πολιτεία", "Platão", "c. 375 a.C.", "filosofia", []),
    ("etica-nicomaco", "Ética a Nicômaco", "Ἠθικὰ Νικομάχεια", "Aristóteles", "c. 340 a.C.", "filosofia", []),
    ("meditacoes-aurelio", "Meditações", "Τὰ εἰς ἑαυτόν", "Marco Aurélio", "c. 175", "filosofia", []),
    ("consolacao", "A Consolação da Filosofia", "De Consolatione Philosophiae", "Boécio", "524", "filosofia",
     [("CFW 5: Da providência", "/confissoes/westminster/5/")]),
    ("principe", "O Príncipe", "Il Principe", "Nicolau Maquiavel", "1532", "filosofia", []),
    ("discurso-metodo", "Discurso do Método", "Discours de la méthode", "René Descartes", "1637", "filosofia", []),
    ("leviata", "Leviatã", "Leviathan", "Thomas Hobbes", "1651", "filosofia", [("Jó 41", "/biblia/jo/41/")]),
    ("ensaio-locke", "Ensaio sobre o Entendimento Humano", "An Essay Concerning Human Understanding", "John Locke", "1689", "filosofia", []),
    ("critica-razao-pura", "Crítica da Razão Pura", "Kritik der reinen Vernunft", "Immanuel Kant", "1781", "filosofia", []),
    ("temor-tremor", "Temor e Tremor", "Frygt og Bæven", "Søren Kierkegaard", "1843", "filosofia",
     [("Gênesis 22", "/biblia/genesis/22/")]),
    ("zaratustra", "Assim Falou Zaratustra", "Also sprach Zarathustra", "Friedrich Nietzsche", "1883–1885", "filosofia", []),
    ("dooyeweerd", "No Crepúsculo do Pensamento Ocidental", "In the Twilight of Western Thought", "Herman Dooyeweerd", "1960", "filosofia", []),
    ("abolicao-homem", "A Abolição do Homem", "The Abolition of Man", "C. S. Lewis", "1943", "filosofia", []),
    ("plantinga", "Deus, a Liberdade e o Mal", "God, Freedom, and Evil", "Alvin Plantinga", "1974", "filosofia",
     [("CFW 5: Da providência", "/confissoes/westminster/5/")]),
    # apologética
    ("pensamentos-pascal", "Pensamentos", "Pensées", "Blaise Pascal", "1670", "apologetica", [("Eclesiastes 3:11", "/biblia/eclesiastes/3/11/")]),
    ("ortodoxia", "Ortodoxia", "Orthodoxy", "G. K. Chesterton", "1908", "apologetica", [("Credo Apostólico", "/confissoes/credos/apostolico/")]),
    ("van-til", "A Defesa da Fé", "The Defense of the Faith", "Cornelius Van Til", "1955", "apologetica",
     [("CFW 1: Da Escritura Sagrada", "/confissoes/westminster/1/")]),
    ("schaeffer", "O Deus que Intervém", "The God Who Is There", "Francis Schaeffer", "1968", "apologetica", [("Atos 17", "/biblia/atos/17/")]),
    ("deus-banco-reus", "Deus no Banco dos Réus", "God in the Dock", "C. S. Lewis", "1970", "apologetica", []),
    ("craig-fe-razoavel", "Em Guarda", "On Guard", "William Lane Craig", "2010", "apologetica", [("1 Pedro 3:15", "/biblia/1-pedro/3/15/")]),
    # vida cristã e devocionais
    ("presenca-deus", "A Prática da Presença de Deus", "La Pratique de la présence de Dieu", "Irmão Lourenço", "1692", "devocional", []),
    ("manha-noite", "Manhã e Noite", "Morning and Evening", "Charles H. Spurgeon", "1865", "devocional", [("Salmo 5:3", "/biblia/salmos/5/3/")]),
    ("tudo-para-ele", "Tudo para Ele", "My Utmost for His Highest", "Oswald Chambers", "1927", "devocional", []),
    ("discipulado", "Discipulado", "Nachfolge", "Dietrich Bonhoeffer", "1937", "devocional", [("Mateus 5", "/biblia/mateus/5/")]),
    ("vida-comunhao", "Vida em Comunhão", "Gemeinsames Leben", "Dietrich Bonhoeffer", "1939", "devocional", [("Salmo 133", "/biblia/salmos/133/")]),
    ("busca-deus", "À Procura de Deus", "The Pursuit of God", "A. W. Tozer", "1948", "devocional", [("Salmo 42:1", "/biblia/salmos/42/1/")]),
    ("celebracao-disciplina", "Celebração da Disciplina", "Celebration of Discipline", "Richard Foster", "1978", "devocional", []),
    # literatura cristã
    ("divina-comedia", "A Divina Comédia", "La Divina Commedia", "Dante Alighieri", "c. 1320", "literatura", []),
    ("paraiso-perdido", "O Paraíso Perdido", "Paradise Lost", "John Milton", "1667", "literatura", [("Gênesis 3", "/biblia/genesis/3/")]),
    ("crime-castigo", "Crime e Castigo", "Преступление и наказание", "Fiódor Dostoiévski", "1866", "literatura", [("João 11", "/biblia/joao/11/")]),
    ("karamazov", "Os Irmãos Karamázov", "Братья Карамазовы", "Fiódor Dostoiévski", "1880", "literatura", [("João 12:24", "/biblia/joao/12/24/")]),
    ("ben-hur", "Ben-Hur", "Ben-Hur: A Tale of the Christ", "Lew Wallace", "1880", "literatura", []),
    ("em-seus-passos", "Em Seus Passos", "In His Steps", "Charles Sheldon", "1896", "literatura", [("1 Pedro 2:21", "/biblia/1-pedro/2/21/")]),
    ("cartas-diabo", "Cartas de um Diabo a seu Aprendiz", "The Screwtape Letters", "C. S. Lewis", "1942", "literatura",
     [("Efésios 6:11", "/biblia/efesios/6/11/")]),
    ("grande-divorcio", "O Grande Divórcio", "The Great Divorce", "C. S. Lewis", "1945", "literatura", []),
    ("narnia", "As Crônicas de Nárnia", "The Chronicles of Narnia", "C. S. Lewis", "1950–1956", "literatura", []),
    ("senhor-aneis", "O Senhor dos Anéis", "The Lord of the Rings", "J. R. R. Tolkien", "1954–1955", "literatura", []),
    # biografias e história da igreja
    ("eusebio", "História Eclesiástica", "Ἐκκλησιαστικὴ ἱστορία", "Eusébio de Cesareia", "c. 325", "biografia", [("Atos", "/biblia/atos/")]),
    ("martires-foxe", "O Livro dos Mártires", "Actes and Monuments", "John Foxe", "1563", "biografia", [("Hebreus 11", "/biblia/hebreus/11/")]),
    ("vida-calvino-beza", "A Vida de Calvino", "Vita Calvini", "Teodoro de Beza", "1564", "biografia", []),
    ("brainerd", "A Vida de David Brainerd", "The Life of David Brainerd", "Jonathan Edwards", "1749", "biografia", []),
    ("hudson-taylor", "O Segredo Espiritual de Hudson Taylor", "Hudson Taylor's Spiritual Secret", "Howard e Geraldine Taylor", "1932", "biografia", []),
    ("aqui-estou", "Cativo à Palavra: a vida de Lutero", "Here I Stand: A Life of Martin Luther", "Roland Bainton", "1950", "biografia", []),
    ("portoes-esplendor", "Através dos Portões do Esplendor", "Through Gates of Splendor", "Elisabeth Elliot", "1957", "biografia", []),
    ("refugio-secreto", "O Refúgio Secreto", "The Hiding Place", "Corrie ten Boom", "1971", "biografia", [("Salmo 91", "/biblia/salmos/91/")]),
]


def main():
    faltam, ids = [], set()
    obras = []
    for id_, t, o, a, ano, trad, liga in OBRAS:
        assert id_ not in ids, f"id repetido: {id_}"
        assert trad in TRADICOES, id_
        ids.add(id_)
        for _, url in liga:
            if not (RAIZ / url.strip("/") / "index.html").exists():
                faltam.append(f"{id_}: {url}")
        obras.append({"id": id_, "t": t, "o": o, "a": a, "ano": ano, "tr": trad, "g": GRUPO[trad],
                      "liga": [[r, u] for r, u in liga]})
    assert not faltam, f"páginas que não existem: {faltam}"
    doc = {"tradicoes": {k: {"pt": v[0], "en": v[1], "es": v[2]} for k, v in TRADICOES.items()}, "obras": obras}
    print({g: sum(1 for o in obras if o["g"] == g) for g in sorted(set(GRUPO.values()))})
    DESTINO.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(obras)} obras na prateleira, {sum(len(o['liga']) for o in obras)} ligações com o Sola")


if __name__ == "__main__":
    main()
