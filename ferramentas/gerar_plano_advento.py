"""Plano "Advento com Calvino" -> entrada "advento" de data/plans.json (o primeiro da lista, por ser da estação).

27 dias, do 1º Domingo do Advento (29/11/2026) ao Natal (25/12): as promessas (Gênesis, Números, Deuteronômio), os
profetas (Isaías, Jeremias, Miqueias, Ageu), os anúncios e o nascimento (Lucas 1–2, Mateus 1–2) e o sentido da
encarnação (João 1, Gálatas 4, Filipenses 2, Hebreus 1). Cada dia tem um título ("titulos", nos 3 idiomas) e um
versículo-chave ("calvino": [livro, cap, v]) que o app abre já com o comentário de Calvino; o script confere que o
versículo existe na Bíblia Livre e que Calvino o comenta (em pt/, no próprio versículo ou num bloco que o cobre) e
deixa de fora os livros de tradução provisória. Calvino comentou Isaías inteiro, mas o acervo não tem Isaías 49–66
(os arquivos vieram vazios da fonte): nesses dias o versículo-chave é a passagem do Novo Testamento que cita o profeta
(1 Pedro 2:24 para Isaías 53; Lucas 4:18 para Isaías 61). "inicio" faz o plano abrir no dia da data, enquanto nada foi marcado.

uso:  python3 ferramentas/gerar_plano_advento.py      (depois: python3 ferramentas/gerar_paginas.py)"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLANOS = RAIZ / "data" / "plans.json"
CALVINO = RAIZ / "data" / "commentaries" / "calvin"

# (leituras, versículo-chave, título pt, título en, título es); leitura = [livro, cap] ou [livro, cap, v1, v2]
DIAS = [
    # 1ª semana: a promessa
    ([["GEN", 3, 1, 24]], ["GEN", 3, 15], "A primeira promessa", "The first promise", "La primera promesa"),
    ([["GEN", 12, 1, 9]], ["GEN", 12, 3], "Em ti serão benditas todas as famílias", "In you all families will be blessed",
     "En ti serán benditas todas las familias"),
    ([["GEN", 49, 1, 12]], ["GEN", 49, 10], "O cetro não se arredará de Judá", "The scepter shall not depart from Judah",
     "No será quitado el cetro de Judá"),
    ([["NUM", 24, 15, 19]], ["NUM", 24, 17], "Uma estrela procederá de Jacó", "A star shall come out of Jacob",
     "Saldrá estrella de Jacob"),
    ([["DEU", 18, 15, 22]], ["DEU", 18, 15], "Um profeta como Moisés", "A prophet like Moses", "Un profeta como Moisés"),
    ([["ISA", 7, 1, 17]], ["ISA", 7, 14], "Emanuel, Deus conosco", "Immanuel, God with us", "Emanuel, Dios con nosotros"),
    ([["ISA", 9, 1, 7]], ["ISA", 9, 6], "Um menino nos nasceu", "Unto us a child is born", "Un niño nos es nacido"),
    # 2ª semana: o Rei e o Servo
    ([["ISA", 11, 1, 10]], ["ISA", 11, 1], "O rebento do tronco de Jessé", "The shoot from the stump of Jesse",
     "La vara del tronco de Isaí"),
    ([["ISA", 40, 1, 11]], ["ISA", 40, 3], "Preparai o caminho do Senhor", "Prepare the way of the Lord",
     "Preparad el camino del Señor"),
    ([["ISA", 42, 1, 9]], ["ISA", 42, 1], "Eis o meu Servo", "Behold my Servant", "He aquí mi Siervo"),
    ([["ISA", 52, 13, 15], ["ISA", 53], ["1PE", 2, 21, 25]], ["1PE", 2, 24], "Ferido por nossas transgressões",
     "Wounded for our transgressions", "Herido por nuestras rebeliones"),
    ([["JER", 23, 1, 8]], ["JER", 23, 5], "O Renovo justo de Davi", "The righteous Branch of David",
     "El Renuevo justo de David"),
    ([["MIC", 5, 1, 5]], ["MIC", 5, 2], "Tu, Belém Efrata", "But you, Bethlehem Ephrathah", "Tú, Belén Efrata"),
    ([["ISA", 61, 1, 3], ["LUK", 4, 16, 21]], ["LUK", 4, 18], "O Espírito do Senhor está sobre mim", "The Spirit of the Lord is upon me",
     "El Espíritu del Señor está sobre mí"),
    # 3ª semana: a vinda anunciada
    ([["HAG", 2, 1, 9]], ["HAG", 2, 7], "O desejado de todas as nações", "The desire of all nations",
     "El deseado de todas las naciones"),
    ([["LUK", 1, 1, 25]], ["LUK", 1, 17], "O anúncio a Zacarias", "The announcement to Zechariah", "El anuncio a Zacarías"),
    ([["LUK", 1, 26, 38]], ["LUK", 1, 35], "O anúncio a Maria", "The announcement to Mary", "El anuncio a María"),
    ([["LUK", 1, 39, 56]], ["LUK", 1, 46], "A minha alma engrandece ao Senhor", "My soul magnifies the Lord",
     "Engrandece mi alma al Señor"),
    ([["LUK", 1, 57, 80]], ["LUK", 1, 68], "Bendito o Senhor, que visitou o seu povo",
     "Blessed be the Lord, who has visited his people", "Bendito el Señor, que ha visitado a su pueblo"),
    ([["MAT", 1, 1, 17]], ["MAT", 1, 1], "Filho de Davi, filho de Abraão", "Son of David, son of Abraham",
     "Hijo de David, hijo de Abraham"),
    ([["MAT", 1, 18, 25]], ["MAT", 1, 21], "Ele salvará o seu povo dos seus pecados",
     "He will save his people from their sins", "Él salvará a su pueblo de sus pecados"),
    # 4ª semana: o Filho enviado
    ([["GAL", 4, 1, 7]], ["GAL", 4, 4], "Na plenitude dos tempos", "In the fullness of time", "En el cumplimiento del tiempo"),
    ([["PHP", 2, 1, 11]], ["PHP", 2, 7], "Esvaziou-se a si mesmo", "He emptied himself", "Se despojó a sí mismo"),
    ([["HEB", 1, 1, 14]], ["HEB", 1, 2], "Deus nos falou pelo Filho", "God has spoken to us by his Son",
     "Dios nos ha hablado por el Hijo"),
    ([["MAT", 2, 1, 12]], ["MAT", 2, 2], "Onde está o rei que nasceu?", "Where is he who has been born king?",
     "¿Dónde está el rey que ha nacido?"),
    ([["LUK", 2, 1, 20]], ["LUK", 2, 11], "Hoje vos nasceu o Salvador", "Unto you is born this day a Savior",
     "Os ha nacido hoy un Salvador"),
    ([["JHN", 1, 1, 18]], ["JHN", 1, 14], "O Verbo se fez carne", "The Word became flesh", "El Verbo se hizo carne"),
]
PLANO = {
    "id": "advento",
    "nome": {"pt": "Advento com Calvino", "en": "Advent with Calvin", "es": "Adviento con Calvino"},
    "desc": {"pt": "Do 1º Domingo do Advento ao Natal (29/11 a 25/12): as promessas, os profetas e o nascimento de "
                   "Cristo, com o comentário de João Calvino no versículo-chave de cada dia.",
             "en": "From the first Sunday of Advent to Christmas (Nov 29 – Dec 25): the promises, the prophets and the "
                   "birth of Christ, with John Calvin's commentary on each day's key verse.",
             "es": "Del primer domingo de Adviento a Navidad (29/11 al 25/12): las promesas, los profetas y el "
                   "nacimiento de Cristo, con el comentario de Juan Calvino en el versículo clave de cada día."},
    "inicio": "2026-11-29",
}


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def calvino_cobre(l, c, v):
    """o comentário em português no versículo ou no bloco anterior que o cobre"""
    arq = CALVINO / "pt" / l / f"{c}.json"
    if not arq.exists():
        return False
    com = ler(arq)
    return any(str(x) in com and com[str(x)].strip() for x in range(v, 0, -1))


def main():
    provisorio = set(ler(CALVINO / "manifest.json").get("provisorio", []))
    biblia = {}
    for leituras, (l, c, v), *_ in DIAS:
        for r in leituras + [[l, c, v, v]]:
            caps = biblia.setdefault(r[0], ler(RAIZ / "data" / "bibles" / "blivre" / f"{r[0]}.json"))
            assert 1 <= r[1] <= len(caps), f"capítulo fora da Bíblia Livre: {r}"
            if len(r) > 2:
                assert 1 <= r[2] <= r[3] <= len(caps[r[1] - 1]) and caps[r[1] - 1][r[3] - 1], f"versículo fora: {r}"
        assert l not in provisorio, f"{l} está com a tradução provisória de Calvino"
        assert calvino_cobre(l, c, v), f"Calvino não comenta {l} {c}:{v}"
    plano = {**PLANO, "dias": [d[0] for d in DIAS], "calvino": [d[1] for d in DIAS],
             "titulos": {"pt": [d[2] for d in DIAS], "en": [d[3] for d in DIAS], "es": [d[4] for d in DIAS]}}
    planos = [p for p in ler(PLANOS) if p["id"] != "advento"]
    PLANOS.write_text(json.dumps([plano] + planos, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"advento: {len(DIAS)} dias, de {PLANO['inicio']} ao Natal")


if __name__ == "__main__":
    main()
