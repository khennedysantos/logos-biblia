"""Importa da CCEL o comentário de Calvino nos livros em que ele tinha vindo incompleto -> data/commentaries/calvin/.

Nos Salmos, em 1 e 2 Timóteo, em Tito, em Zacarias e em Malaquias, a base antiga trazia só o começo de cada capítulo
(o cabeçalho, o texto bíblico e o comentário do primeiro versículo), repetido em todos os versículos. Aqui o texto vem
inteiro dos volumes da Calvin Translation Society na CCEL (domínio público, ThML), separado pelos marcadores de
comentário de cada versículo (<scripCom parsed="|Ps|1|3|0|0">):

  - o comentário de cada versículo fica na chave dele, sem a tabela com o texto bíblico (inglês e latim), que o site
    já mostra, e sem as notas de rodapé do tradutor inglês;
  - o que vem antes do primeiro marcador do capítulo (o argumento do salmo, a introdução do capítulo) abre o primeiro
    versículo comentado;
  - nas preleções de Zacarias e Malaquias, a oração do fim de cada preleção fica no versículo em que ela termina;
  - prefácios, dedicatórias e a "versão de Calvino" do fim de cada volume ficam de fora, como nos outros livros.

O português desses livros é apagado (era a tradução do pedaço repetido) e refeito pelo NLLB no GitHub Actions:
aba Actions -> "Traduzir (NLLB)", etapa calvino, livros = PSA,1TI,2TI,TIT,ZEC,MAL.

uso:  python3 ferramentas/calvino_ccel.py            (baixa os volumes para ferramentas/fontes/ccel/calvin/, fora do git)"""
import html, json, re, sys, urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calvino_caudas import PASSAGEM_EN                              # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "ferramentas" / "fontes" / "ccel" / "calvin"
BASE = RAIZ / "data" / "commentaries" / "calvin"
VOLUMES = {"PSA": ["calcom08", "calcom09", "calcom10", "calcom11", "calcom12"],
           "1TI": ["calcom43"], "2TI": ["calcom43"], "TIT": ["calcom43"], "ZEC": ["calcom30"], "MAL": ["calcom30"]}
OSIS = {"Ps": "PSA", "1Tim": "1TI", "2Tim": "2TI", "Titus": "TIT", "Zech": "ZEC", "Mal": "MAL"}
# divisões cujo texto é do comentário; as outras (prefácios, a "versão de Calvino" do livro inteiro, índices) ficam de fora
DIVISOES = {"Psalm", "Chapter", "chapter", "Scripture", "lecture", "prayer"}
# títulos soltos que não são comentário: "CHAPTER 1", "PSALM 23.", "Lecture One Hundred…", o título do volume
TITULO = re.compile(r"^(?:[^a-z]{1,80}|Lecture [A-Za-z -]+\.?|Commentary|upon the book of Psalms|Prayer)$")
MARCO = re.compile(r'<scripCom\b[^>]*\bparsed="\|([A-Za-z0-9]+)\|(\d+)\|(\d+)\|[^"]*"[^>]*/?>'
                   r'|<div\d\b([^>]*)>|</ThML\.body>', re.S)


def baixar(vol):
    arq = FONTES / f"{vol}.xml"
    if not arq.exists():
        FONTES.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(f"https://www.ccel.org/ccel/calvin/{vol}.xml", headers={"User-Agent": "Mozilla/5.0 (Sola)"})
        arq.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    return arq.read_text(encoding="utf-8")


def texto(frag):
    """ThML -> texto, com parágrafos separados por linha em branco; o lema em itálico do começo vira "1. Lema. Texto" """
    frag = re.sub(r"<note\b.*?</note>", "", frag, flags=re.S)
    frag = re.sub(r"<table\b.*?</table>", "", frag, flags=re.S)
    pars = []
    for p in re.findall(r"<p\b[^>]*>(.*?)</p>", frag, flags=re.S):
        p = re.sub(r"^\s*<b>\s*(\d+)\.?\s*</b>\.?\s*", r"\1. ", p)                       # "<b>1</b>" -> "1. "
        p = re.sub(r"^((?:\d+\. )?)\s*<i>([^<]{3,200}?)</i>\s*(?=[A-Z“‘(])",               # lema em itálico no começo
                   lambda m: m.group(1) + m.group(2).strip().rstrip(".,;:") + ". ", p)
        p = html.unescape(re.sub(r"<[^>]+>", "", p))
        p = " ".join(p.split())
        if p and not TITULO.match(p):
            pars.append(p)
    return "\n\n".join(pars)


def extrair(vol, livros):
    """{(livro, cap): {versículo: texto}} dos livros pedidos que estão neste volume"""
    t = baixar(vol)
    corpo = t[t.find("<ThML.body"):]
    saida = defaultdict(lambda: defaultdict(list))
    livro = cap = None
    verso, dentro, pos = 0, False, 0
    for m in MARCO.finditer(corpo):
        if dentro and livro in livros and cap:
            trecho = texto(corpo[pos:m.start()])
            if trecho:
                saida[(livro, cap)][verso].append(trecho)
        pos = m.end()
        if m.group(1):                                     # comentário de um versículo
            livro, cap, verso = OSIS.get(m.group(1), m.group(1)), int(m.group(2)), int(m.group(3))
            dentro = True
        elif m.group(4) is not None:                       # nova divisão
            at = dict(re.findall(r'(\w+)="([^"]*)"', m.group(4)))
            tipo, titulo = at.get("type", ""), at.get("title", "")
            dentro = tipo in DIVISOES
            if tipo == "book":
                livro = {"Commentary on First Timothy": "1TI", "Commentary on Second Timothy": "2TI",
                         "Commentary on Titus": "TIT", "Commentary on Philemon": "PHM",
                         "Commentary on Zechariah": "ZEC", "Commentary on Malachi": "MAL"}.get(titulo)
                cap = None
            elif tipo == "Psalm":
                livro, cap, verso = "PSA", int(re.search(r"\d+", titulo).group()), 0
            elif tipo.lower() == "chapter":
                cap, verso = int(re.search(r"\d+", titulo).group()), 0
    return saida


def montar(blocos, n_versos):
    """junta os pedaços de cada versículo; a introdução (versículo 0) abre o primeiro versículo comentado"""
    versos = {v: "\n\n".join(p) for v, p in sorted(blocos.items()) if p}
    intro = versos.pop(0, "")
    fora = [v for v in versos if v > n_versos]
    for v in fora:                                         # versículo além do fim do capítulo: junta no anterior
        anterior = max((w for w in versos if w <= n_versos), default=None)
        if anterior:
            versos[anterior] += "\n\n" + versos.pop(v)
    if intro:
        if versos:
            primeiro = min(versos)
            versos[primeiro] = intro + "\n\n" + versos[primeiro]
        else:
            versos[1] = intro
    if versos:                                             # "Then follows —" no fim do capítulo fica sem sentido
        ultimo = max(versos)
        versos[ultimo] = PASSAGEM_EN.sub("", versos[ultimo]).rstrip()
    return {str(v): t for v, t in sorted(versos.items())}, fora


def main():
    livros = set(sys.argv[1:]) or set(VOLUMES)
    biblia = {}
    problemas, total = [], {}
    por_vol = defaultdict(set)
    for l in livros:
        for vol in VOLUMES[l]:
            por_vol[vol].add(l)
    capitulos = defaultdict(lambda: defaultdict(list))
    for vol, ls in por_vol.items():
        for chave, versos in extrair(vol, ls).items():
            for v, partes in versos.items():
                capitulos[chave][v].extend(partes)
    for l in sorted(livros):
        biblia[l] = json.loads((RAIZ / "data" / "bibles" / "blivre" / f"{l}.json").read_text(encoding="utf-8"))
        caps = sorted(c for (b, c) in capitulos if b == l)
        n_caps = len(biblia[l]) if isinstance(biblia[l], list) else len(biblia[l])
        if caps != list(range(1, n_caps + 1)):
            problemas.append(f"{l}: capítulos {caps[:3]}…{caps[-3:]} (a Bíblia tem {n_caps})")
        for c in caps:
            cap_bl = biblia[l][c - 1] if isinstance(biblia[l], list) else biblia[l][str(c)]
            n_versos = len(cap_bl)
            versos, fora = montar(capitulos[(l, c)], n_versos)
            if fora:
                problemas.append(f"{l} {c}: comentário dos versículos {fora} (o capítulo tem {n_versos}) foi junto do anterior")
            (BASE / l).mkdir(exist_ok=True)
            (BASE / l / f"{c}.json").write_text(json.dumps(versos, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            velho = BASE / "pt" / l / f"{c}.json"
            if velho.exists():
                velho.unlink()                             # a tradução era do pedaço repetido; o NLLB refaz
            total[l] = total.get(l, 0) + sum(len(t) for t in versos.values())
        livro_pt = BASE / "pt" / l
        if livro_pt.exists() and not any(livro_pt.iterdir()):
            livro_pt.rmdir()
    for l, n in sorted(total.items()):
        print(f"{l}: {n / 1e6:.2f} milhões de caracteres")
    for p in problemas:
        print("  ⚠", p)


if __name__ == "__main__":
    main()
