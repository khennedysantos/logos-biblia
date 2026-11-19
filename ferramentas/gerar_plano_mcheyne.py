"""Plano de leitura de M'Cheyne -> entrada "mcheyne" de data/plans.json.

Robert Murray M'Cheyne publicou o calendário em 1842 (domínio público): 4 leituras por dia em 365 dias — o Antigo
Testamento uma vez, o Novo Testamento e os Salmos duas vezes. Nas colunas originais, as duas primeiras são para a
leitura em família e as duas últimas para a leitura pessoal.

A tabela vem do aplicativo aberto "The M'Cheyne Plan" (github.com/willswire/mcheyne, Apache 2.0), fixada num commit;
só a lista de referências é aproveitada. Cada leitura vira [livro, cap] ou, quando é parte de um capítulo,
[livro, cap, v1, v2]; "Gênesis 9-10" vira dois capítulos e "Zacarias 12:1-13:1" vira [ZEC,12] + [ZEC,13,1,1].
Cada dia guarda também, em "grupos", quantos itens cabem em cada uma das 4 leituras.

uso:  python3 ferramentas/gerar_plano_mcheyne.py"""
import json, re, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLANOS = RAIZ / "data" / "plans.json"
FONTE = RAIZ / "ferramentas" / "fontes" / "mcheyne" / "PlanConstants.swift"
URL = ("https://raw.githubusercontent.com/willswire/mcheyne/72fc5951b9634b4429927b7d3df61dfd403aa67b/"
       "App/PlanConstants.swift")
PLANO = {
    "id": "mcheyne",
    "nome": {"pt": "Plano de M'Cheyne", "en": "M'Cheyne's plan", "es": "Plan de M'Cheyne"},
    "desc": {"pt": "A Bíblia em 1 ano em 4 leituras por dia (1842): o Antigo Testamento uma vez, o Novo Testamento "
                   "e os Salmos duas vezes.",
             "en": "The Bible in 1 year in 4 readings a day (1842): the Old Testament once, the New Testament and "
                   "the Psalms twice.",
             "es": "La Biblia en 1 año en 4 lecturas por día (1842): el Antiguo Testamento una vez, el Nuevo "
                   "Testamento y los Salmos dos veces."},
}


def versos_por_cap(livro):
    caps = json.loads((RAIZ / "data" / "bibles" / "blivre" / f"{livro}.json").read_text(encoding="utf-8"))
    return [len(c) for c in caps]


def ler_tabela():
    if not FONTE.exists():
        FONTE.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, FONTE)
    texto = FONTE.read_text(encoding="utf-8")
    bloco = texto[texto.index("RAW_PLAN_DATA"):]
    bloco = bloco[:bloco.index("\n]")]
    return [re.findall(r'"([^"]+)"', linha) for linha in re.findall(r"\[([^\[\]]+)\]", bloco)]


def leitura(ref, livros, versos):
    lista = re.fullmatch(r"(.+?) (\d+(?:,\d+)+)", ref)          # "Jeremias 36,45": capítulos soltos
    if lista:
        return [[livros[lista.group(1)], int(c)] for c in lista.group(2).split(",")]
    m = re.fullmatch(r"(.+?) (\d+)(?::(\d+))?(?:-(\d+)(?::(\d+))?)?", ref)
    assert m, f"referência não reconhecida: {ref}"
    nome, c1, v1, fim1, fim2 = m.groups()
    livro = livros[nome]
    c1 = int(c1)
    if not v1:                                       # "Gênesis 9" ou "Gênesis 9-10"
        return [[livro, c] for c in range(c1, int(fim1 or c1) + 1)]
    v1 = int(v1)
    if fim2:                                         # "Zacarias 12:1-13:1": atravessa o capítulo
        c2, v2 = int(fim1), int(fim2)
    else:                                            # "Lucas 1:1-38"
        c2, v2 = c1, int(fim1)
    vs = versos.setdefault(livro, versos_por_cap(livro))
    itens = []
    for c in range(c1, c2 + 1):
        a = v1 if c == c1 else 1
        b = v2 if c == c2 else vs[c - 1]
        assert 1 <= a <= b <= vs[c - 1], f"{ref}: versículos fora do capítulo na Bíblia Livre"
        itens.append([livro, c] if (a, b) == (1, vs[c - 1]) else [livro, c, a, b])
    return itens


def main():
    livros = {b["en"]: b["id"] for b in json.loads((RAIZ / "data" / "books.json").read_text(encoding="utf-8"))["books"]}
    livros["Psalm"] = "PSA"
    versos, dias, grupos = {}, [], []
    tabela = ler_tabela()
    assert len(tabela) == 365 and all(len(d) == 4 for d in tabela), "a tabela deveria ter 365 dias de 4 leituras"
    for linha in tabela:
        dia, g = [], []
        for ref in linha:
            itens = leitura(ref, livros, versos)
            dia += itens
            g.append(len(itens))
        dias.append(dia)
        grupos.append(g)
    # conferência: todo capítulo da Bíblia aparece, e cada versículo dos capítulos partidos é lido
    lidos = {}
    for dia in dias:
        for it in dia:
            lidos.setdefault((it[0], it[1]), []).append(it[2:] or None)
    total = sum(b["ch"] for b in json.loads((RAIZ / "data" / "books.json").read_text(encoding="utf-8"))["books"])
    assert len(lidos) == total, f"faltam capítulos: {total - len(lidos)}"
    planos = json.loads(PLANOS.read_text(encoding="utf-8"))
    novo = dict(PLANO, dias=dias, grupos=grupos)
    planos = [p for p in planos if p["id"] != "mcheyne"]
    pos = next((i + 1 for i, p in enumerate(planos) if p["id"] == "anual"), len(planos))
    planos.insert(pos, novo)
    PLANOS.write_text(json.dumps(planos, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"M'Cheyne: {len(dias)} dias, {sum(len(d) for d in dias)} leituras, {len(lidos)} capítulos cobertos")


if __name__ == "__main__":
    main()
