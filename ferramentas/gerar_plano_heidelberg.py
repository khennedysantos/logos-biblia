"""Plano "Catecismo de Heidelberg em 52 Domingos" -> entrada "heidelberg" de data/plans.json.

O Catecismo de Heidelberg (1563) foi dividido pelos próprios autores em 52 Domingos, para ser ensinado um por semana
ao longo do ano. Cada dia do plano é um Domingo, com os números das perguntas dele, tirados do campo "domingo" de
data/confissoes/heidelberg.json (ferramentas/confissoes_ccel.py). Planos de catecismo têm "doc" (o arquivo em
data/confissoes/) e, nos dias, números de perguntas em vez de capítulos da Bíblia.

uso:  python3 ferramentas/gerar_plano_heidelberg.py"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLANOS = RAIZ / "data" / "plans.json"
DOC = RAIZ / "data" / "confissoes" / "heidelberg.json"
PLANO = {
    "id": "heidelberg",
    "doc": "heidelberg",
    "nome": {"pt": "Catecismo de Heidelberg em 52 Domingos", "en": "Heidelberg Catechism in 52 Lord's Days",
             "es": "Catecismo de Heidelberg en 52 domingos"},
    "desc": {"pt": "Um Domingo do catecismo por semana, como os autores o dividiram em 1563: as 129 perguntas "
                   "e respostas em um ano.",
             "en": "One Lord's Day of the catechism each week, as its authors divided it in 1563: all 129 "
                   "questions and answers in a year.",
             "es": "Un domingo del catecismo por semana, como lo dividieron sus autores en 1563: las 129 preguntas "
                   "y respuestas en un año."},
}


def main():
    itens = json.loads(DOC.read_text(encoding="utf-8"))["itens"]
    domingos = {}
    for it in itens:
        domingos.setdefault(int(it["domingo"]), []).append(int(it["n"]))
    assert sorted(domingos) == list(range(1, 53)), "o Heidelberg deveria ter os Domingos 1 a 52"
    plano = dict(PLANO, dias=[sorted(domingos[d]) for d in range(1, 53)])
    planos = json.loads(PLANOS.read_text(encoding="utf-8"))
    planos = [p for p in planos if p["id"] != plano["id"]] + [plano]
    PLANOS.write_text(json.dumps(planos, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"plano {plano['id']}: {len(plano['dias'])} Domingos, {sum(map(len, plano['dias']))} perguntas")


if __name__ == "__main__":
    main()
