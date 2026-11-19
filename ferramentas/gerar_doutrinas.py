"""Gera data/topics/doutrinas.json a partir da Confissão de Fé de Westminster (data/confissoes/westminster.json).

As "doutrinas" da busca de Temas, da doutrina do dia e da aba "CFW & Refs" são os 33 capítulos da própria Confissão
(1647, domínio público, tradução em português feita por tradutor/confissoes_llm.py): cada capítulo traz os parágrafos
com os textos de prova da Assembleia de Westminster. Não há mais resumo escrito à parte — o texto é o da Confissão.

uso:  python3 ferramentas/gerar_doutrinas.py           (grava)
      python3 ferramentas/gerar_doutrinas.py --texto   (não grava; imprime cada capítulo, para ler)
"""
import json, re, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
SAIDA = DATA / "topics" / "doutrinas.json"
RE_MARCA = re.compile(r"\s?\[\d+\]")
# palavras de busca de cada capítulo, além do título (termos usuais, não doutrina: só ajudam a achar o capítulo)
BUSCA = {
    "1": "escritura bíblia palavra de deus cânon inspiração sola scriptura", "2": "deus trindade pai filho espírito santo",
    "3": "decreto predestinação eleição soberania", "4": "criação", "5": "providência soberania",
    "6": "queda pecado original depravação", "7": "pacto aliança obras graça", "8": "cristo mediador encarnação expiação",
    "9": "livre-arbítrio vontade", "10": "vocação eficaz chamado regeneração novo nascimento",
    "11": "justificação sola fide fé imputação", "12": "adoção filhos de deus", "13": "santificação",
    "14": "fé salvadora", "15": "arrependimento conversão", "16": "boas obras", "17": "perseverança dos santos",
    "18": "certeza segurança da salvação", "19": "lei de deus mandamentos dez mandamentos", "20": "liberdade cristã consciência",
    "21": "culto adoração sábado dia do senhor domingo", "22": "juramentos votos", "23": "magistrado civil governo estado",
    "24": "casamento divórcio família", "25": "igreja", "26": "comunhão dos santos", "27": "sacramentos",
    "28": "batismo", "29": "ceia do senhor santa ceia eucaristia", "30": "disciplina eclesiástica censuras",
    "31": "sínodos concílios", "32": "morte ressurreição estado depois da morte", "33": "juízo final",
}


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def slug(nome):
    s = unicodedata.normalize("NFD", nome)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = re.sub(r"^(da|do|das|dos|de) ", "", s.lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def main():
    wcf = ler(DATA / "confissoes" / "westminster.json")
    saida = []
    for cap in wcf["partes"]:
        titulo = cap.get("titulo") or cap["titulo_en"]
        secoes = []
        for it in cap["itens"]:
            refs = [r[:4] if len(r) == 4 else [r[0], r[1], r[2], 999] for lista in it["provas"].values() for r in lista]
            secoes.append({"t": f"{cap['n']}.{it['n']}", "p": RE_MARCA.sub("", it.get("pt") or it["en"]).strip(),
                           "pe": RE_MARCA.sub("", it["en"]).strip(),
                           "v": [[l, c, a or 1, b or 999] for l, c, a, b in refs]})
        primeiro = secoes[0]["p"] if secoes else ""
        resumo = re.split(r"(?<=[.;:])\s", primeiro, maxsplit=1)[0]
        saida.append({"id": slug(titulo) or f"cap-{cap['n']}", "t": titulo, "te": cap["titulo_en"],
                      "s": BUSCA.get(cap["n"], "").split() + [cap["titulo_en"].lower()],
                      "f": f"CFW {cap['n']}", "r": resumo,
                      "u": f"/confissoes/westminster/{cap['n']}/", "sec": secoes})
    assert len({d["id"] for d in saida}) == len(saida), "dois capítulos com o mesmo id"
    if "--texto" in sys.argv:
        for d in saida:
            print(f"\n######## {d['f']} — {d['t']}")
            for s in d["sec"]:
                print(f"  {s['t']} {s['p'][:300]}")
        return
    SAIDA.write_text(json.dumps(saida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    n = sum(len(s["v"]) for d in saida for s in d["sec"])
    print(f"{len(saida)} capítulos da Confissão, {n} referências → {SAIDA.relative_to(RAIZ)} ({SAIDA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
