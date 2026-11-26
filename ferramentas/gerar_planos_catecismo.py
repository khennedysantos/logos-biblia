"""Planos de catecismo em 52 semanas -> entradas "breve-catecismo" e "catecismo-batista" de data/plans.json.

O Breve Catecismo de Westminster (107 perguntas) e o Catecismo Batista de Keach (114) não têm divisão própria em
semanas, como o Heidelberg tem em Domingos (gerar_plano_heidelberg.py). Aqui as perguntas são repartidas na ordem em
52 semanas, duas ou três por semana, com as semanas de três espalhadas pelo ano. Planos com "doc" são de catecismo
(cada dia é uma lista de números de perguntas); "rot" é o nome de cada dia ("Semana"), e "rots", o plural.

uso:  python3 ferramentas/gerar_planos_catecismo.py"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLANOS = RAIZ / "data" / "plans.json"
SEMANA = {"pt": "Semana", "en": "Week", "es": "Semana"}
SEMANAS = {"pt": "semanas", "en": "weeks", "es": "semanas"}
CATECISMOS = [
    {"id": "breve-catecismo", "doc": "breve-catecismo",
     "nome": {"pt": "Breve Catecismo em 52 semanas", "en": "Shorter Catechism in 52 weeks",
              "es": "Catecismo Menor en 52 semanas"},
     "desc": {"pt": "As 107 perguntas e respostas do Breve Catecismo de Westminster (1647) em um ano, duas ou três "
                    "por semana, para estudar e decorar em família.",
              "en": "The 107 questions and answers of the Westminster Shorter Catechism (1647) in a year, two or "
                    "three a week, to study and memorize as a family.",
              "es": "Las 107 preguntas y respuestas del Catecismo Menor de Westminster (1647) en un año, dos o tres "
                    "por semana, para estudiar y memorizar en familia."}},
    {"id": "catecismo-batista", "doc": "catecismo-batista",
     "nome": {"pt": "Catecismo Batista em 52 semanas", "en": "Baptist Catechism in 52 weeks",
              "es": "Catecismo Bautista en 52 semanas"},
     "desc": {"pt": "As 114 perguntas e respostas do Catecismo Batista de Benjamin Keach (1693) em um ano, duas ou "
                    "três por semana, para estudar e decorar em família.",
              "en": "The 114 questions and answers of Benjamin Keach's Baptist Catechism (1693) in a year, two or "
                    "three a week, to study and memorize as a family.",
              "es": "Las 114 preguntas y respuestas del Catecismo Bautista de Benjamin Keach (1693) en un año, dos "
                    "o tres por semana, para estudiar y memorizar en familia."}},
]


def repartir(n, semanas=52):
    """n perguntas em `semanas` grupos seguidos, com as sobras espalhadas: [[1, 2], [3, 4, 5], …]"""
    dias, inicio = [], 1
    for s in range(semanas):
        fim = (s + 1) * n // semanas                     # divisão inteira: os grupos maiores ficam espalhados
        dias.append(list(range(inicio, fim + 1)))
        inicio = fim + 1
    return dias


def main():
    planos = json.loads(PLANOS.read_text(encoding="utf-8"))
    for base in CATECISMOS:
        itens = json.loads((RAIZ / "data" / "confissoes" / f"{base['doc']}.json").read_text(encoding="utf-8"))["itens"]
        assert [int(q["n"]) for q in itens] == list(range(1, len(itens) + 1)), base["doc"]
        plano = dict(base, rot=SEMANA, rots=SEMANAS, dias=repartir(len(itens)))
        planos = [p for p in planos if p["id"] != plano["id"]] + [plano]
        print(f"plano {plano['id']}: {len(plano['dias'])} semanas, {len(itens)} perguntas")
    PLANOS.write_text(json.dumps(planos, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
