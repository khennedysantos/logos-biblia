"""Gera o interlinear hebraico (data/interlinear/{livro}/{cap}.json) e o texto hebraico
(data/bibles/orig/{livro}.json) do Antigo Testamento a partir do TAHOT — Translators Amalgamated
Hebrew OT, STEPBible.org / Tyndale House, licença CC BY.

Por que existe: o hebraico numera capítulos e versículos de outro jeito em ~2.300 versículos (títulos
dos Salmos, Gn 32, Nm 17, Jl 3, Ml 4...). A fonte traz as duas numerações — "Psa.51.1(51.3)" é o
versículo 1 nas nossas Bíblias e o 3 no hebraico. Este script usa sempre a primeira, que é a da
Bíblia Livre, da KJV e da Reina-Valera; assim o original cai no versículo certo.

O número de Strong é o da raiz (entre chaves na fonte), nunca o do prefixo (H9001–H9009, que não
existem no léxico). O título do salmo (versículo 0 na fonte) entra no começo do versículo 1.

As glosas em português já revisadas são mantidas: onde o versículo não mudou, a glosa antiga fica;
nas palavras novas vale o dicionário ferramentas/glosas_pt.json (glosa inteira ou, se não houver,
parte por parte: "and  spear" = "e" + "lança"). O que não estiver lá sai em inglês e é traduzido
depois por `ferramentas/tradutor/traduzir_tudo.sh glosas`.

uso:  python3 ferramentas/gerar_interlinear_at.py            (baixa a fonte na 1ª vez, ~70 MB)
      python3 ferramentas/gerar_interlinear_at.py --conferir  (só mostra o que mudaria)
"""
import collections, json, re, sys, urllib.parse, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
FONTES = Path(__file__).resolve().parent / "fontes"
BASE = "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Translators Amalgamated OT+NT/"
ARQUIVOS = ["Gen-Deu", "Jos-Est", "Job-Sng", "Isa-Mal"]
NOME = "TAHOT {} - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt"
REF = re.compile(r"^([1-3A-Za-z][A-Za-z]{2})\.(\d+)\.(\d+)(?:\(\d+\.\d+\))?#\d+=\S+$")
RAIZ_STRONG = re.compile(r"\{H(\d+)[A-Za-z]?\}")


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def gravar(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def baixar():
    FONTES.mkdir(exist_ok=True)
    for a in ARQUIVOS:
        destino = FONTES / f"TAHOT-{a}.txt"
        if not destino.exists():
            print(f"baixando TAHOT {a}…", flush=True)
            urllib.request.urlretrieve(BASE.replace(" ", "%20").replace("+", "%2B") + urllib.parse.quote(NOME.format(a)), destino)
    return [FONTES / f"TAHOT-{a}.txt" for a in ARQUIVOS]


def strong(dstrong):
    """Número da raiz. Os H9000+ são marcas da STEPBible para prefixos e sufixos (não são de Strong):
    palavra feita só deles, como "lo" (a ele), fica sem número em vez de apontar para um verbete que não existe."""
    m = RAIZ_STRONG.search(dstrong)
    n = int(m.group(1)) if m else 9000
    return f"H{n}" if n < 9000 else ""


def ler_fonte(arquivos):
    """{livro: {cap: {versículo: [[hebraico, transliteração, strong, glosa_en], ...]}}}"""
    dados = collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(list)))
    for arq in arquivos:
        for linha in arq.read_text(encoding="utf-8").split("\n"):
            c = linha.split("\t")
            m = REF.match(c[0])
            if not m or len(c) < 5:
                continue
            livro, cap, v = m.group(1).upper(), int(m.group(2)), int(m.group(3))
            dados[livro][cap][v].append([c[1].replace("/", ""), c[2].replace(".", "").replace("/", ""),
                                         strong(c[4]), c[3].replace("/", " ")])
    return dados


def texto_corrido(palavras):
    """Junta as palavras de um versículo: tira a barra de pontuação e cola o que vem depois do maqqef."""
    t = " ".join(p[0].replace("\\", "") for p in palavras)
    return t.replace("־ ", "־")


def main():
    conferir = "--conferir" in sys.argv
    dados = ler_fonte(baixar())
    meta = {b["id"]: b for b in ler(DATA / "books.json")["books"] if b["t"] == "AT"}
    assert set(dados) == set(meta), f"livros diferentes: {set(dados) ^ set(meta)}"
    mapa = ler(RAIZ / "ferramentas" / "glosas_pt.json")

    # 1ª passada: versículos iguais aos que já estão no site ensinam a tradução de cada glosa
    antigos, aprendido = {}, collections.defaultdict(collections.Counter)
    for livro in meta:
        for cap, versos in dados[livro].items():
            arq = DATA / "interlinear" / livro / f"{cap}.json"
            if not arq.exists():
                continue
            ant = antigos[(livro, cap)] = ler(arq)
            for v, palavras in versos.items():
                velho = ant[v - 1] if 1 <= v <= len(ant) else []
                if v >= 1 and [p[0] for p in velho] == [p[0] for p in palavras]:
                    for a, n in zip(velho, palavras):
                        if a[3] != n[3]:
                            aprendido[n[3]][a[3]] += 1
    aprendido = {en: c.most_common(1)[0][0] for en, c in aprendido.items()}

    def traduz(en):
        return aprendido.get(en) or mapa.get(en)

    def compor(en):
        partes = [traduz(x) for x in en.split("  ")]
        return "  ".join(partes) if len(partes) > 1 and all(partes) else None

    caps_novos = caps_mudados = strongs_corrigidos = em_ingles = 0
    faltam = collections.Counter()
    for livro, info in meta.items():
        assert max(dados[livro]) == info["ch"], f"{livro}: {max(dados[livro])} capítulos na fonte, {info['ch']} no site"
        hebraico = []
        for cap in range(1, info["ch"] + 1):
            versos = dados[livro][cap]
            titulo = versos.pop(0, [])          # título do salmo
            versos[1] = titulo + versos[1]
            ant = antigos.get((livro, cap))
            saida = []
            for v in range(1, max(versos) + 1):
                palavras = versos.get(v, [])
                velho = ant[v - 1] if ant and v <= len(ant) else []
                igual = [p[0] for p in velho] == [p[0] for p in palavras]
                for i, p in enumerate(palavras):
                    en = p[3]
                    if igual:
                        p[3] = velho[i][3]
                        strongs_corrigidos += velho[i][2] != p[2]
                    else:
                        p[3] = traduz(en) or compor(en) or en
                        if p[3] == en and re.search(r"[A-Za-z]{2}", en) and en not in mapa.values():
                            faltam[en] += 1
                            em_ingles += 1
                saida.append(palavras)
            hebraico.append([texto_corrido(p) for p in saida])
            if ant is None:
                caps_novos += 1
            elif ant != saida:
                caps_mudados += 1
            if not conferir:
                gravar(DATA / "interlinear" / livro / f"{cap}.json", saida)
        if not conferir:
            gravar(DATA / "bibles" / "orig" / f"{livro}.json", hebraico)

    print(f"{caps_novos} capítulos novos, {caps_mudados} corrigidos, "
          f"{strongs_corrigidos} números de Strong trocados do prefixo para a raiz")
    print(f"{em_ingles} palavras ({len(faltam)} glosas diferentes) ainda em inglês"
          + (": rode ferramentas/tradutor/traduzir_tudo.sh glosas" if faltam else ""))
    if faltam:
        gravar(FONTES / "glosas_sem_traducao.json", dict(faltam.most_common()))


if __name__ == "__main__":
    main()
