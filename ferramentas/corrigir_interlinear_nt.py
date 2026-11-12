"""Completa o interlinear grego (data/interlinear/{livro}/{cap}.json) nos ~50 pontos do Novo Testamento
em que a numeração dos versículos difere entre as edições (Rm 16:25-27, 2Co 13:13-14, Jo 7:53, At 19:41,
Fp 1:16-17...). A fonte é o TAGNT — Translators Amalgamated Greek NT, STEPBible.org / Tyndale House, CC BY.

Na fonte, a referência alternativa vem depois da principal: "2Co.13.12[13.13]". Entre colchetes está a
numeração da KJV/Textus Receptus, que é a das nossas traduções — vale ela. Entre parênteses ou chaves está
a de outras edições (NA28, Bizantino) — aí vale a principal. O gerador antigo descartava todas essas linhas.
Em três lugares a Bíblia Livre segue a numeração principal e não a da KJV (lista PRINCIPAL, conferida no texto).

Só os versículos afetados são refeitos; o resto do NT não é tocado. As glosas em português que já existem
são mantidas; as novas vêm das palavras iguais já traduzidas no próprio NT e de ferramentas/glosas_pt.json.

uso:  python3 ferramentas/corrigir_interlinear_nt.py            (baixa a fonte na 1ª vez, ~30 MB)
      python3 ferramentas/corrigir_interlinear_nt.py --conferir  (só mostra o que mudaria)
"""
import collections, json, re, sys, urllib.parse, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
FONTES = Path(__file__).resolve().parent / "fontes"
BASE = "https://raw.githubusercontent.com/STEPBible/STEPBible-Data/master/Translators%20Amalgamated%20OT%2BNT/"
NOME = "TAGNT {} - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt"
REF = re.compile(r"^([1-3A-Za-z][A-Za-z]{2})\.(\d+)\.(\d+)(?:([\[({])(\d+)\.(\d+)[\])}])?#\d+=\S+$")
GREGO = re.compile(r"^(.*?)\s*\(([^)]*)\)\s*$")
MARCA = re.compile(r"^\s*[\[{]\d+(?:\.\d+)?[\]}]\s*")   # "[13] Greet", "{14.24} To Him": número do versículo alternativo dentro da glosa
# Fp 1:16-17 (ordem dos versículos), 3Jo 15 e Ap 12:18: a Bíblia Livre numera como a referência principal
PRINCIPAL = {("PHP", 1, 16), ("PHP", 1, 17), ("3JN", 1, 15), ("REV", 12, 18)}


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def baixar():
    FONTES.mkdir(exist_ok=True)
    saida = []
    for a in ("Mat-Jhn", "Act-Rev"):
        destino = FONTES / f"TAGNT-{a}.txt"
        if not destino.exists():
            print(f"baixando TAGNT {a}…", flush=True)
            urllib.request.urlretrieve(BASE + urllib.parse.quote(NOME.format(a)), destino)
        saida.append(destino)
    return saida


def main():
    conferir = "--conferir" in sys.argv
    versos = collections.defaultdict(list)   # (livro, cap, v) -> palavras [grego, transliteração, strong, glosa_en]
    afetados = set()
    for arq in baixar():
        for linha in arq.read_text(encoding="utf-8").split("\n"):
            c = linha.split("\t")
            m = REF.match(c[0])
            if not m or len(c) < 4:
                continue
            livro, cap, v = m.group(1).upper(), int(m.group(2)), int(m.group(3))
            if m.group(4) == "[" and (livro, cap, v) not in PRINCIPAL:
                cap, v = int(m.group(5)), int(m.group(6))
            if m.group(4):
                afetados.add((livro, cap, v))
            g = GREGO.match(c[1])
            s = re.match(r"G(\d+)", c[3])
            versos[(livro, cap, v)].append([g.group(1) if g else c[1], g.group(2) if g else "",
                                            "G" + str(int(s.group(1))) if s else "", MARCA.sub("", c[2])])

    # o que já está traduzido no NT ensina a glosa de cada palavra nova
    capitulos, aprendido = {}, collections.defaultdict(collections.Counter)
    for (livro, cap, v), palavras in versos.items():
        if (livro, cap) not in capitulos:
            capitulos[(livro, cap)] = ler(DATA / "interlinear" / livro / f"{cap}.json")
        ant = capitulos[(livro, cap)]
        velho = ant[v - 1] if v <= len(ant) else []
        if [p[0] for p in velho] == [p[0] for p in palavras]:
            for a, n in zip(velho, palavras):
                aprendido[n[3]][a[3]] += 1
    aprendido = {en: c.most_common(1)[0][0] for en, c in aprendido.items()}
    mapa = ler(RAIZ / "ferramentas" / "glosas_pt.json")

    mudados, novas, em_ingles = set(), 0, []
    for livro, cap, v in sorted(afetados):
        ant = capitulos[(livro, cap)]
        while len(ant) < v:
            ant.append([])
        palavras = versos[(livro, cap, v)]
        if [p[0] for p in ant[v - 1]] == [p[0] for p in palavras]:
            continue   # já está certo (o script já rodou)
        feitas = collections.defaultdict(list)   # glosas que este versículo já tinha, por palavra grega
        for p in ant[v - 1]:
            feitas[p[0]].append(p[3])
        for p in palavras:
            en = p[3]
            if feitas[p[0]]:
                p[3] = feitas[p[0]].pop(0)
            else:
                p[3] = aprendido.get(en) or mapa.get(en) or en
                novas += 1
                if p[3] == en and re.search(r"[a-z]{3}", en):
                    em_ingles.append(en)
        ant[v - 1] = palavras
        mudados.add((livro, cap))
    if not conferir:
        for livro, cap in mudados:
            (DATA / "interlinear" / livro / f"{cap}.json").write_text(
                json.dumps(capitulos[(livro, cap)], ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(afetados)} versículos com numeração alternativa; {len(mudados)} capítulos corrigidos, {novas} palavras novas")
    if em_ingles:
        print(f"{len(em_ingles)} glosas ainda em inglês (rode ferramentas/tradutor/traduzir_tudo.sh glosas): "
              + " | ".join(sorted(set(em_ingles))[:40]))


if __name__ == "__main__":
    main()
