"""Catálogo da prateleira do perfil (data/prateleira.json): clássicos da fé cristã, sobretudo da tradição reformada,
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
}
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
        obras.append({"id": id_, "t": t, "o": o, "a": a, "ano": ano, "tr": trad,
                      "liga": [[r, u] for r, u in liga]})
    assert not faltam, f"páginas que não existem: {faltam}"
    doc = {"tradicoes": {k: {"pt": v[0], "en": v[1], "es": v[2]} for k, v in TRADICOES.items()}, "obras": obras}
    DESTINO.write_text(json.dumps(doc, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(obras)} obras na prateleira, {sum(len(o['liga']) for o in obras)} ligações com o Sola")


if __name__ == "__main__":
    main()
