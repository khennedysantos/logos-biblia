"""Leitura da fonte do interlinear (STEPBible / Tyndale House, CC BY) e alinhamento com o site.

O interlinear do site (data/interlinear) guarda só a glosa em português; a fonte tem, para cada palavra, a glosa
em inglês, a gramática e (no NT) uma glosa em espanhol. Alinhando as duas (mesmo versículo, mesmas palavras
originais), cada palavra do site recupera esses dados — é o que permite achar e corrigir glosas erradas.

A fonte fica em ferramentas/fontes/ (fora do git); gerar_interlinear_at.py e corrigir_interlinear_nt.py baixam.
A numeração é a da Bíblia Livre, como nesses dois scripts: no NT vale a referência entre colchetes (KJV), menos
nos versículos de PRINCIPAL; no AT vale a primeira, e o título do salmo (versículo 0) entra no versículo 1."""
import collections, json, re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
FONTES = Path(__file__).resolve().parent / "fontes"
REF_NT = re.compile(r"^([1-3A-Za-z][A-Za-z]{2})\.(\d+)\.(\d+)(?:([\[({])(\d+)\.(\d+)[\])}])?#\d+=\S+$")
REF_AT = re.compile(r"^([1-3A-Za-z][A-Za-z]{2})\.(\d+)\.(\d+)(?:\(\d+\.\d+\))?#\d+=\S+$")
GREGO = re.compile(r"^(.*?)\s*\(([^)]*)\)\s*$")
MARCA = re.compile(r"^\s*[\[{]\d+(?:\.\d+)?[\]}]\s*")
PRINCIPAL = {("PHP", 1, 16), ("PHP", 1, 17), ("3JN", 1, 15), ("REV", 12, 18)}
Palavra = collections.namedtuple("Palavra", "livro cap v i original en gram es strong")


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def fonte_nt():
    """{(livro, cap, v): [(grego, en, gramática, es), ...]}"""
    versos = collections.defaultdict(list)
    for a in ("Mat-Jhn", "Act-Rev"):
        for linha in (FONTES / f"TAGNT-{a}.txt").read_text(encoding="utf-8").split("\n"):
            c = linha.split("\t")
            m = REF_NT.match(c[0])
            if not m or len(c) < 9:
                continue
            livro, cap, v = m.group(1).upper(), int(m.group(2)), int(m.group(3))
            if m.group(4) == "[" and (livro, cap, v) not in PRINCIPAL:
                cap, v = int(m.group(5)), int(m.group(6))
            g = GREGO.match(c[1])
            gram = c[3].split("=", 1)[1] if "=" in c[3] else ""
            versos[(livro, cap, v)].append((g.group(1) if g else c[1], MARCA.sub("", c[2]), gram, c[8]))
    return versos


def fonte_at():
    """{(livro, cap, v): [(hebraico, en, gramática, ""), ...]} — "and/ spear" vira "and  spear", como no site."""
    versos = collections.defaultdict(list)
    for a in ("Gen-Deu", "Jos-Est", "Job-Sng", "Isa-Mal"):
        for linha in (FONTES / f"TAHOT-{a}.txt").read_text(encoding="utf-8").split("\n"):
            c = linha.split("\t")
            m = REF_AT.match(c[0])
            if not m or len(c) < 6:
                continue
            versos[(m.group(1).upper(), int(m.group(2)), int(m.group(3)))].append(
                (c[1].replace("/", ""), c[3].replace("/", " "), c[5], ""))
    for chave in [k for k in versos if k[2] == 0]:
        versos[(chave[0], chave[1], 1)] = versos.pop(chave) + versos[(chave[0], chave[1], 1)]
    return versos


def alinhar():
    """Devolve (capitulos, palavras): capitulos = {(livro, cap): versos do site, para alterar e gravar};
    palavras = lista de (Palavra, referência à lista [original, transliteração, strong, glosa] do site)."""
    fonte = {**fonte_nt(), **fonte_at()}
    capitulos, palavras = {}, []
    for arq in sorted((DATA / "interlinear").glob("*/*.json")):
        livro, cap = arq.parent.name, int(arq.stem)
        versos = capitulos[(livro, cap)] = ler(arq)
        for v, verso in enumerate(versos, 1):
            f = fonte.get((livro, cap, v), [])
            if [p[0] for p in verso] == [x[0] for x in f]:
                for i, (p, x) in enumerate(zip(verso, f)):
                    palavras.append((Palavra(livro, cap, v, i, p[0], x[1], x[2], x[3], p[2]), p))
    return capitulos, palavras


def gravar_capitulo(livro, cap, versos):
    (DATA / "interlinear" / livro / f"{cap}.json").write_text(
        json.dumps(versos, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def nome_proprio(gram):
    """Grego: N-NSM-P (pessoa), -L (lugar), -T (título). Hebraico/aramaico: HNpm, HR/Npl, ANpm..."""
    return bool(re.search(r"-[PL](?:-|$)", gram)) or bool(re.search(r"(?:^[HA]|/)Np", gram))


def pessoa(gram):
    """'1S', '3P'... de um verbo finito; None se não for (particípio, infinitivo, nome)."""
    m = re.search(r"V-\w+?-(\d)([SP])", gram)                     # grego: V-AAI-3P
    if m:
        return m.group(1) + m.group(2)
    m = re.search(r"V\w\w([123])[mfc]([sp])", gram)               # hebraico e aramaico: HVqp3cp
    return m.group(1) + m.group(2).upper() if m else None
