"""Os credos da Igreja antiga (domínio público) -> data/confissoes/credos.json: o Credo Apostólico, o Credo Niceno
(Niceno-Constantinopolitano, 381), o Credo de Atanásio (Quicumque vult) e a Definição de Calcedônia (451).

Tradução do Sola, feita com IA a partir dos originais latinos e gregos (domínio público, como textos antigos) e
conferida com um texto inglês também em domínio público, que vai junto como referência:
- Apostólico e Atanásio: Livro de Oração Comum da Igreja da Inglaterra (1662);
- Niceno: texto inglês tradicional, derivado do mesmo livro (via github.com/NonlinearFruit/Creeds.json);
- Calcedônia: Philip Schaff, The Creeds of Christendom, vol. 2 (1877).
(As versões do Creeds.json para o Apostólico — ELLC, 1988 — e para Calcedônia — Bettenson, 1943 — têm direitos e
não são usadas.)

As notas só explicam o que os próprios Padrões de Westminster dizem sobre o trecho, com o link para eles.
Uso: python3 ferramentas/credos.py   (depois: python3 ferramentas/gerar_paginas.py)"""
import json
from pathlib import Path

DESTINO = Path(__file__).resolve().parent.parent / "data" / "confissoes" / "credos.json"

CREDOS = [
    {
        "id": "apostolico",
        "titulo": "Credo Apostólico",
        "titulo_en": "The Apostles' Creed",
        "quando": "forma atual por volta do século VIII; raiz no credo batismal de Roma (século II)",
        "lingua": "latim",
        "sobre": "O resumo mais antigo e conhecido da fé cristã. Nasceu da confissão que se fazia no batismo em Roma "
                 "e chegou à forma atual por volta do século VIII. Não foi escrito pelos apóstolos, mas resume o "
                 "ensino deles.",
        "texto": [
            "Creio em Deus Pai todo-poderoso, criador do céu e da terra.",
            "E em Jesus Cristo, seu único Filho, nosso Senhor, que foi concebido pelo Espírito Santo, nasceu da "
            "virgem Maria, padeceu sob Pôncio Pilatos, foi crucificado, morto e sepultado; desceu ao inferno; ao "
            "terceiro dia ressurgiu dos mortos; subiu ao céu e está sentado à direita de Deus Pai todo-poderoso, de "
            "onde há de vir para julgar os vivos e os mortos.",
            "Creio no Espírito Santo, na santa Igreja católica, na comunhão dos santos, na remissão dos pecados, na "
            "ressurreição do corpo e na vida eterna. Amém.",
        ],
        "texto_en": [
            "I believe in God the Father Almighty, Maker of heaven and earth:",
            "And in Jesus Christ his only Son our Lord, Who was conceived by the Holy Ghost, Born of the Virgin Mary, "
            "Suffered under Pontius Pilate, Was crucified, dead, and buried: He descended into hell; The third day he "
            "rose again from the dead; He ascended into heaven, And sitteth on the right hand of God the Father "
            "Almighty; From thence he shall come to judge the quick and the dead.",
            "I believe in the Holy Ghost; The holy Catholick Church; The Communion of Saints; The Forgiveness of "
            "sins; The Resurrection of the body, And the Life everlasting. Amen.",
        ],
        "fonte_en": "Book of Common Prayer (1662)",
        "notas": [
            ["desceu ao inferno",
             "O Catecismo Maior de Westminster explica: depois da morte, Cristo foi sepultado e permaneceu no estado "
             "dos mortos e sob o poder da morte até o terceiro dia — “o que foi expresso de outra forma nestas "
             "palavras: ele desceu ao inferno”.",
             "/confissoes/catecismo-maior/50/", "Catecismo Maior, pergunta 50"],
            ["Igreja católica",
             "“Católica” quer dizer universal: a Confissão de Westminster fala da “Igreja católica ou universal”, "
             "formada por todos os eleitos, reunidos sob Cristo, sua cabeça.",
             "/confissoes/westminster/25/", "Confissão de Westminster 25.1"],
        ],
    },
    {
        "id": "niceno",
        "titulo": "Credo Niceno",
        "titulo_en": "The Nicene Creed",
        "quando": "Concílio de Niceia (325), ampliado no Concílio de Constantinopla (381)",
        "lingua": "grego",
        "sobre": "Formulado no Concílio de Niceia (325) contra o arianismo, que negava a plena divindade do Filho, e "
                 "ampliado no Concílio de Constantinopla (381), sobretudo no artigo sobre o Espírito Santo. É o credo "
                 "mais usado em toda a cristandade, e por isso também é chamado Niceno-Constantinopolitano.",
        "texto": [
            "Cremos em um só Deus, Pai todo-poderoso, criador do céu e da terra e de todas as coisas visíveis e "
            "invisíveis.",
            "E em um só Senhor, Jesus Cristo, o Filho unigênito de Deus, gerado do Pai antes de todos os séculos: "
            "Deus de Deus, Luz de Luz, verdadeiro Deus de verdadeiro Deus; gerado, não feito; de uma só substância "
            "com o Pai; por quem todas as coisas foram feitas.",
            "O qual, por nós, homens, e por nossa salvação, desceu dos céus, encarnou-se pelo Espírito Santo, da "
            "virgem Maria, e se fez homem; foi também crucificado por nós sob Pôncio Pilatos; padeceu e foi "
            "sepultado; ao terceiro dia ressuscitou, segundo as Escrituras; subiu aos céus e está sentado à direita "
            "do Pai; e de novo há de vir com glória, para julgar os vivos e os mortos; e o seu reino não terá fim.",
            "E cremos no Espírito Santo, Senhor e doador da vida, que procede do Pai e do Filho; que com o Pai e o "
            "Filho é juntamente adorado e glorificado; que falou pelos profetas.",
            "E cremos na Igreja una, santa, católica e apostólica. Confessamos um só batismo para remissão dos "
            "pecados; e esperamos a ressurreição dos mortos e a vida do mundo vindouro. Amém.",
        ],
        "texto_en": [
            "We believe in one God, the Father Almighty, Maker of heaven and earth, and of all things visible and "
            "invisible.",
            "And in one Lord Jesus Christ, the only-begotten Son of God, begotten of the Father before all worlds; God "
            "of God, Light of Light, very God of very God; begotten, not made, being of one substance with the Father, "
            "by whom all things were made.",
            "Who, for us men and for our salvation, came down from heaven, and was incarnate by the Holy Spirit of the "
            "virgin Mary, and was made man; and was crucified also for us under Pontius Pilate; He suffered and was "
            "buried; and the third day He rose again, according to the Scriptures; and ascended into heaven, and sits "
            "on the right hand of the Father; and He shall come again, with glory, to judge the quick and the dead; "
            "whose kingdom shall have no end.",
            "And we believe in the Holy Ghost, the Lord and Giver of Life; who proceeds from the Father and the Son; "
            "who with the Father and the Son together is worshipped and glorified; who spoke by the prophets.",
            "And we believe in one holy catholic and apostolic Church. We acknowledge one baptism for the remission "
            "of sins; and we look for the resurrection of the dead, and the life of the world to come. Amen.",
        ],
        "fonte_en": "texto inglês tradicional, em domínio público (via github.com/NonlinearFruit/Creeds.json)",
        "notas": [
            ["de uma só substância",
             "Em grego, homooúsios: o Filho tem a mesma essência do Pai. A Confissão de Westminster diz o mesmo: na "
             "unidade da Divindade há três pessoas “de uma mesma substância, poder e eternidade”.",
             "/confissoes/westminster/2/", "Confissão de Westminster 2.3"],
            ["que procede do Pai e do Filho",
             "O texto grego de 381 diz apenas “que procede do Pai”. As igrejas do Ocidente acrescentaram “e do Filho” "
             "(em latim, Filioque), e a Confissão de Westminster também confessa que o Espírito Santo procede "
             "eternamente do Pai e do Filho.",
             "/confissoes/westminster/2/", "Confissão de Westminster 2.3"],
        ],
    },
    {
        "id": "atanasio",
        "titulo": "Credo de Atanásio",
        "titulo_en": "The Athanasian Creed (Quicunque vult)",
        "quando": "texto latino, provavelmente dos séculos V ou VI",
        "lingua": "latim",
        "sobre": "Também chamado Quicumque vult, pelas primeiras palavras em latim. Não foi escrito por Atanásio de "
                 "Alexandria: é um texto latino, provavelmente dos séculos V ou VI, que recebeu o nome dele por "
                 "defender a mesma fé que ele defendeu. É a exposição mais detalhada da Trindade e da pessoa de "
                 "Cristo entre os credos antigos.",
        "texto": [
            "Todo aquele que quer ser salvo deve, antes de tudo, guardar a fé católica. Quem não a conservar íntegra "
            "e inviolada sem dúvida perecerá eternamente.",
            "E a fé católica é esta: que adoremos um só Deus na Trindade, e a Trindade na Unidade, sem confundir as "
            "pessoas nem dividir a substância. Pois uma é a pessoa do Pai, outra a do Filho e outra a do Espírito "
            "Santo. Mas a divindade do Pai, do Filho e do Espírito Santo é uma só: igual a glória, coeterna a "
            "majestade.",
            "Tal como é o Pai, tal é o Filho e tal é o Espírito Santo. O Pai é incriado, o Filho é incriado e o "
            "Espírito Santo é incriado. O Pai é imenso, o Filho é imenso e o Espírito Santo é imenso. O Pai é eterno, "
            "o Filho é eterno e o Espírito Santo é eterno. E, contudo, não são três eternos, mas um só eterno; assim "
            "como não são três incriados nem três imensos, mas um só incriado e um só imenso.",
            "Do mesmo modo, o Pai é todo-poderoso, o Filho é todo-poderoso e o Espírito Santo é todo-poderoso; e, "
            "contudo, não são três todo-poderosos, mas um só todo-poderoso. Assim, o Pai é Deus, o Filho é Deus e o "
            "Espírito Santo é Deus; e, contudo, não são três deuses, mas um só Deus. Assim, o Pai é Senhor, o Filho é "
            "Senhor e o Espírito Santo é Senhor; e, contudo, não são três senhores, mas um só Senhor. Pois, assim "
            "como a verdade cristã nos obriga a confessar cada pessoa, por si mesma, como Deus e Senhor, assim a "
            "religião católica nos proíbe dizer que há três deuses ou três senhores.",
            "O Pai não foi feito por ninguém: nem criado, nem gerado. O Filho é só do Pai: não feito, nem criado, "
            "mas gerado. O Espírito Santo é do Pai e do Filho: não feito, nem criado, nem gerado, mas procedente. Há, "
            "portanto, um só Pai, não três pais; um só Filho, não três filhos; um só Espírito Santo, não três "
            "espíritos santos.",
            "E nesta Trindade nenhum é antes ou depois do outro, nenhum é maior ou menor que o outro; mas as três "
            "pessoas são, todas, coeternas e iguais entre si. De modo que em tudo, como já foi dito, deve ser adorada "
            "a Unidade na Trindade e a Trindade na Unidade. Quem, pois, quer ser salvo, assim deve pensar da "
            "Trindade.",
            "Além disso, é necessário para a salvação eterna que creia também fielmente na encarnação de nosso "
            "Senhor Jesus Cristo. Pois a fé verdadeira é que creiamos e confessemos que nosso Senhor Jesus Cristo, o "
            "Filho de Deus, é Deus e homem. É Deus, da substância do Pai, gerado antes dos séculos; e é homem, da "
            "substância de sua mãe, nascido no tempo. Perfeito Deus e perfeito homem, que subsiste de alma racional e "
            "carne humana. Igual ao Pai segundo a divindade, e menor que o Pai segundo a humanidade.",
            "Embora seja Deus e homem, não são dois, mas um só Cristo: um só, não pela conversão da divindade em "
            "carne, mas pela assunção da humanidade em Deus; um só inteiramente, não por confusão de substância, mas "
            "pela unidade da pessoa. Pois, assim como a alma racional e a carne são um só homem, assim Deus e homem "
            "são um só Cristo.",
            "Ele padeceu por nossa salvação, desceu ao inferno, ao terceiro dia ressuscitou dos mortos; subiu aos "
            "céus, está sentado à direita de Deus Pai todo-poderoso, de onde há de vir para julgar os vivos e os "
            "mortos. Na sua vinda, todos os homens ressuscitarão com os seus corpos e prestarão contas das suas "
            "próprias obras. E os que tiverem feito o bem irão para a vida eterna; e os que tiverem feito o mal, para "
            "o fogo eterno.",
            "Esta é a fé católica: quem não a crer fiel e firmemente não poderá ser salvo.",
        ],
        "texto_en": [
            "Whosoever will be saved, before all things it is necessary that he hold the catholic faith. Which faith "
            "unless every one do keep whole and undefiled, without doubt he shall perish everlastingly.",
            "And the catholic faith is this: that we worship one God in Trinity, and Trinity in Unity; neither "
            "confounding the Persons, nor dividing the Essence. For there is one Person of the Father; another of the "
            "Son; and another of the Holy Ghost. But the Godhead of the Father, of the Son, and of the Holy Ghost, is "
            "all one; the Glory equal, the Majesty coeternal.",
            "Such as the Father is; such is the Son; and such is the Holy Ghost. The Father uncreated; the Son "
            "uncreated; and the Holy Ghost uncreated. The Father unlimited; the Son unlimited; and the Holy Ghost "
            "unlimited. The Father eternal; the Son eternal; and the Holy Ghost eternal. And yet they are not three "
            "eternals; but one eternal. As also there are not three uncreated; nor three infinites, but one "
            "uncreated; and one infinite.",
            "So likewise the Father is Almighty; the Son Almighty; and the Holy Ghost Almighty. And yet they are not "
            "three Almighties; but one Almighty. So the Father is God; the Son is God; and the Holy Ghost is God. And "
            "yet they are not three Gods; but one God. So likewise the Father is Lord; the Son Lord; and the Holy "
            "Ghost Lord. And yet not three Lords; but one Lord. For like as we are compelled by the Christian verity; "
            "to acknowledge every Person by himself to be God and Lord; So are we forbidden by the catholic religion; "
            "to say, There are three Gods, or three Lords.",
            "The Father is made of none; neither created, nor begotten. The Son is of the Father alone; not made, nor "
            "created; but begotten. The Holy Ghost is of the Father and of the Son; neither made, nor created, nor "
            "begotten; but proceeding. So there is one Father, not three Fathers; one Son, not three Sons; one Holy "
            "Ghost, not three Holy Ghosts.",
            "And in this Trinity none is before, or after another; none is greater, or less than another. But the "
            "whole three Persons are coeternal, and coequal. So that in all things, as aforesaid; the Unity in "
            "Trinity, and the Trinity in Unity, is to be worshipped. He therefore that will be saved, let him thus "
            "think of the Trinity.",
            "Furthermore it is necessary to everlasting salvation; that he also believe faithfully the Incarnation of "
            "our Lord Jesus Christ. For the right Faith is, that we believe and confess; that our Lord Jesus Christ, "
            "the Son of God, is God and Man; God, of the Essence of the Father; begotten before the worlds; and Man, "
            "of the Essence of his Mother, born in the world. Perfect God; and perfect Man, of a reasonable soul and "
            "human flesh subsisting. Equal to the Father, as touching his Godhead; and inferior to the Father as "
            "touching his Manhood.",
            "Who although he is God and Man; yet he is not two, but one Christ. One; not by conversion of the Godhead "
            "into flesh; but by assumption of the Manhood by God. One altogether; not by confusion of Essence; but by "
            "unity of Person. For as the reasonable soul and flesh is one man; so God and Man is one Christ;",
            "Who suffered for our salvation; descended into hell; rose again the third day from the dead. He ascended "
            "into heaven, he sitteth on the right hand of the God the Father Almighty, from whence he will come to "
            "judge the living and the dead. At whose coming all men will rise again with their bodies; And shall give "
            "account for their own works. And they that have done good shall go into life everlasting; and they that "
            "have done evil, into everlasting fire.",
            "This is the catholic faith; which except a man believe truly and firmly, he cannot be saved.",
        ],
        "fonte_en": "Book of Common Prayer (1662), via github.com/NonlinearFruit/Creeds.json",
        "notas": [
            ["a fé católica",
             "“Católica” quer dizer universal: a fé de toda a Igreja, em todos os lugares e tempos, e não de uma "
             "denominação.",
             "/confissoes/westminster/25/", "Confissão de Westminster 25.1"],
            ["Espírito Santo é do Pai e do Filho",
             "É a mesma confissão de Westminster: o Pai não é gerado nem procede de ninguém; o Filho é eternamente "
             "gerado do Pai; o Espírito Santo procede eternamente do Pai e do Filho.",
             "/confissoes/westminster/2/", "Confissão de Westminster 2.3"],
        ],
    },
    {
        "id": "calcedonia",
        "titulo": "Definição de Calcedônia",
        "titulo_en": "The Chalcedonian Definition",
        "quando": "Concílio de Calcedônia (451)",
        "lingua": "grego",
        "sobre": "Definição do Concílio de Calcedônia (451) sobre a pessoa de Cristo: uma só pessoa em duas naturezas, "
                 "divina e humana, sem confusão e sem divisão. Rejeita tanto quem misturava as duas naturezas numa só "
                 "quanto quem separava Cristo em duas pessoas.",
        "texto": [
            "Seguindo, pois, os santos pais, todos unanimemente ensinamos que se deve confessar um só e o mesmo "
            "Filho, nosso Senhor Jesus Cristo: perfeito na divindade e perfeito na humanidade; verdadeiro Deus e "
            "verdadeiro homem, de alma racional e corpo; consubstancial ao Pai segundo a divindade, e consubstancial "
            "a nós segundo a humanidade, em tudo semelhante a nós, exceto no pecado; gerado do Pai antes dos séculos "
            "segundo a divindade, e, nestes últimos dias, por nós e por nossa salvação, nascido da virgem Maria, a "
            "mãe de Deus, segundo a humanidade;",
            "um só e o mesmo Cristo, Filho, Senhor, Unigênito, reconhecido em duas naturezas, sem confusão, sem "
            "mudança, sem divisão, sem separação; de modo nenhum suprimida a diferença das naturezas por causa da "
            "união, mas antes preservada a propriedade de cada natureza, e concorrendo ambas numa só pessoa e numa só "
            "subsistência; não partido nem dividido em duas pessoas, mas um só e o mesmo Filho e Unigênito, Deus "
            "Verbo, o Senhor Jesus Cristo;",
            "conforme os profetas desde o princípio ensinaram a respeito dele, e o próprio Senhor Jesus Cristo nos "
            "ensinou, e o credo dos santos pais nos transmitiu.",
        ],
        "texto_en": [
            "We, then, following the holy Fathers, all with one consent, teach men to confess one and the same Son, "
            "our Lord Jesus Christ, the same perfect in Godhead and also perfect in manhood; truly God and truly man, "
            "of a reasonable soul and body; consubstantial with the Father according to the Godhead, and "
            "consubstantial with us according to the Manhood; in all things like unto us, without sin; begotten "
            "before all ages of the Father according to the Godhead, and in these latter days, for us and for our "
            "salvation, born of the Virgin Mary, the Mother of God, according to the Manhood;",
            "one and the same Christ, Son, Lord, Only-begotten, to be acknowledged in two natures, inconfusedly, "
            "unchangeably, indivisibly, inseparably; the distinction of natures being by no means taken away by the "
            "union, but rather the property of each nature being preserved, and concurring in one Person and one "
            "Subsistence, not parted or divided into two persons, but one and the same Son, and only begotten, God "
            "the Word, the Lord Jesus Christ;",
            "as the prophets from the beginning have declared concerning him, and the Lord Jesus Christ himself has "
            "taught us, and the Creed of the holy Fathers has handed down to us.",
        ],
        "fonte_en": "Philip Schaff, The Creeds of Christendom, vol. 2 (1877)",
        "notas": [
            ["a mãe de Deus",
             "Em grego, Theotókos. O título fala de Cristo: quem nasceu de Maria é uma só pessoa, verdadeiro Deus e "
             "verdadeiro homem. A Confissão de Westminster diz que as duas naturezas, inteiras, perfeitas e "
             "distintas, foram unidas numa só pessoa, sem conversão, composição ou confusão.",
             "/confissoes/westminster/8/", "Confissão de Westminster 8.2"],
        ],
    },
]


def main():
    for c in CREDOS:
        assert len(c["texto"]) == len(c["texto_en"]), f"{c['id']}: parágrafos diferentes em português e inglês"
        for trecho, *_ in c["notas"]:
            assert trecho in " ".join(c["texto"]), f"{c['id']}: a nota cita “{trecho}”, que não está no texto"
    doc = {"id": "credos", "titulo": "Credos da Igreja antiga", "titulo_en": "The Ancient Creeds", "ano": "séc. IV–VIII",
           "tipo": "credos",
           "fonte": "Textos antigos, em domínio público; tradução do Sola a partir do latim e do grego, conferida com "
                    "textos ingleses em domínio público.",
           "itens": [dict(c, n=c["id"]) for c in CREDOS]}
    DESTINO.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[credos] {len(CREDOS)} credos em {DESTINO.name}")


if __name__ == "__main__":
    main()
