"""Prepara e aplica cada etapa da tradução do Sola.
uso: python3 etapas.py preparar|aplicar  glosas|temas|dicionario|calvino|henry|verbos

Os originais em inglês nunca são apagados: as traduções vão para pastas pt/
(ou, no caso das glosas, substituem só o que ainda estava em inglês)."""
import json, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SITE = AQUI.parents[1]
DATA = SITE / "data"
TRAB = AQUI / "trabalho"
TRAB.mkdir(exist_ok=True)
REF = re.compile(r"\b[1-3]?[A-Z]{2,3} \d")


def ler(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def gravar(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def entradas(etapa, itens):
    gravar(TRAB / f"{etapa}.json", itens)
    print(f"[{etapa}] {len(itens)} itens, {sum(len(i['texto']) for i in itens) / 1e6:.2f} milhões de caracteres")


def traducoes(etapa):
    arq = TRAB / f"{etapa}_pt.json"
    return ler(arq) if arq.exists() else {}


# ---------------- glosas do interlinear (só o que ainda está em inglês) ----------------
def mapa_glosas():
    arq = SITE / "ferramentas" / "glosas_pt.json"
    return ler(arq) if arq.exists() else {}


PT_COMUNS = set("""de do da dos das para pelo pela em no na nos nas ao aos à que não e ele ela eles elas
dele dela deles dEle dEla eu tu nós vós seu sua seus suas meu minha teu tua nosso nossa este esta estes
isso isto aquele antes depois diante sobre entre contra até com sem dentro fora porque pois mas ou se
então assim também todo toda todos cada um uma era foi será são é disse diz sendo tendo""".split())


def parece_pt(g):
    palavras = re.findall(r"[A-Za-zÀ-ú]+", g)
    return bool(re.search(r"[ãõáéíóúâêôçà]", g)) or any(w in PT_COMUNS for w in palavras)


def preparar_glosas():
    mapa = mapa_glosas()
    ja_pt = set(mapa.values())
    vistas = {}
    for arq in (DATA / "interlinear").glob("*/*.json"):
        for verso in ler(arq):
            for p in verso:
                g = p[3]
                if g and g not in ja_pt and g not in vistas and re.search(r"[A-Za-z]{2}", g) \
                        and not parece_pt(g):
                    vistas[g] = True
    entradas("glosas", [{"id": g, "texto": g} for g in vistas])


# glosas que aparecem sem contexto e saem erradas no tradutor automático
GLOSAS_FIXAS = {
    "beginning": "princípio", "beginning,": "princípio,", "true": "verdadeiro", "will": "vontade",
    "grasped [it].": "compreenderam [-na].", "grasped [it]": "compreenderam [-na]",
    "only begotten": "unigênito", "bosom": "seio", "dwelt": "habitou", "dwelling": "habitação",
    "world": "mundo", "world,": "mundo,", "kingdom": "reino", "righteous": "justo", "saying": "dizendo",
    "blessed": "bem-aventurado", "Blessed": "Bem-aventurados", "mercy": "misericórdia",
    "repent": "arrependei-vos", "believing": "crendo", "believe": "crer", "believes": "crê",
    "may believe": "creiam", "having believed": "tendo crido", "believed": "creram",
    # títulos dos salmos e palavras frequentes dos capítulos que entraram com gerar_interlinear_at.py
    "a poem": "um poema", "the  ascents": "as  subidas", "a miktam": "um mictão", "the  Gittith": "a  Gitite",
    "the  Ezrachite": "o  ezraíta", "awake  !": "desperta  !", "pay attention  !": "atenta  !",
    "be exalted  !": "sê exaltado  !", "I cried for help": "clamei por socorro", "may they exult": "exultem",
    "they shout for joy": "gritam de alegria", "O Most High": "ó Altíssimo",
    "I will sing praises to": "cantarei louvores a", "we give thanks": "damos graças",
    "O strength  my": "ó força  minha", "[is] refuge  my": "[é] refúgio  meu", "[is] a helper": "[é] um ajudador",
    "[are] help  my": "[és] socorro  meu", "he will ransom": "ele resgatará", "may he fulfill": "que ele cumpra",
    "she has bound": "ela se obrigou", "an obligation": "uma obrigação", "obligation": "obrigação",
    "vow": "voto", "vow  her": "voto  dela", "he forbade": "ele proibiu", "a prohibition": "uma proibição",
    "the  rods": "as  varas", "rods": "varas", "camps": "acampamentos", "camps  your": "acampamentos  teus",
    "we will sacrifice": "sacrificaremos", "a swarm": "um enxame", "lion": "leão", "den  the": "a  cova",
    "to  den  the": "à  cova", "to  [the] den of": "à  [a] cova de", "and  satraps  the": "e  os  sátrapas",
    "O Belteshazzar": "ó Beltessazar", "[the] Medes": "[os] medos", "and  [the] Persians": "e  [os] persas",
    "a watcher": "um vigilante", "and  a holy [one]": "e  um santo", "cut down!": "cortai!",
    "[the] stump of": "[o] toco de", "[the] birds of": "[as] aves de", "it grew great": "cresceu",
    "it reached": "alcançou", "and  I will betroth  you": "e  te desposarei", "they are afraid": "eles têm medo",
    "[the] teeth of": "[os] dentes de", "he has scattered": "ele espalhou", "they scattered": "eles espalharam",
    "peaks": "picos", "prince of": "príncipe de", "I multiplied": "multipliquei", "[is] much": "[é] muito",
    "[is] only": "[é] somente", "[those who] love": "[os que] amam", "[those who] speak": "[os que] falam",
    "they shook": "eles tremeram", "you will abhor": "abominarás", "and  let us serve": "e  sirvamos",
    # versículos do NT que entraram com corrigir_interlinear_nt.py
    "Grace [be]": "Graça [seja]", "Christ’s": "de Cristo", "Eternal": "Eterno", "He has reconciled [You]": "Ele [vos] reconciliou",
    "I am appointed;": "estou posto;", "I have been crucified with;": "fui crucificado com;", "Luke.": "Lucas.",
    "Philippi": "Filipos", "Phoebe": "Febe", "They were persuaded": "Foram persuadidos", "Timothy": "Timóteo",
    "[though] having authority": "[embora] tendo autoridade", "[to the] only": "[ao] único", "are proclaiming": "anunciam",
    "assembly.": "igreja.", "by him,": "por ele,", "capital": "capital", "converts,": "convertidos,", "do greet": "saudai",
    "equality;": "igualdade;", "having become,": "tendo-se tornado,", "having been found": "tendo sido achado",
    "having been made known —": "tendo sido dado a conhecer —", "however [are]": "porém [são]", "in times": "em tempos",
    "is becoming visible": "se torna visível", "kept secret,": "guardado em segredo,", "of Pacatiana.": "da Pacaciana.",
    "of Phrygia": "da Frígia", "of Titus": "de Tito", "of [the] mystery": "d[o] mistério", "of faith —": "da fé —",
    "of flame,": "de chama,", "of refreshing": "de refrigério", "of the ages": "dos séculos", "overthrowing": "derrubando",
    "purely": "com pureza", "selfish ambition": "rivalidade", "shall we pay": "pagaremos", "shall we pay?": "pagaremos?",
    "there are:": "há:", "they went.": "foram.", "those ones": "aqueles", "to [the] assembly": "à igreja",
    "to be justified,": "ser justificado,", "to grant": "conceder", "years;": "anos;",
}
CONTRACOES = [(r"\b([Ee])m \[o\]", lambda m: "[" + ("N" if m.group(1) == "E" else "n") + "o]"),
              (r"\b([Ee])m \[a\]", lambda m: "[" + ("N" if m.group(1) == "E" else "n") + "a]"),
              (r"\b([Dd])e \[o\]", lambda m: "[" + m.group(1) + "o]"),
              (r"\b([Dd])e \[a\]", lambda m: "[" + m.group(1) + "a]")]


def ajusta_glosa(g):
    for padrao, troca in CONTRACOES:
        g = re.sub(padrao, troca, g)
    return g


def glosa_confiavel(en, pt):
    """O tradutor automático inventa quando recebe uma palavra solta ("wares" vira "O que é isso?").
    Glosa com cara de invenção fica em inglês, que é melhor do que português errado."""
    if not pt or parece_pt(en):                                  # entrada que já estava (meio) em português
        return False
    if ("?" in pt) != ("?" in en) or ("..." in pt and "..." not in en):
        return False
    if re.search(r'["“”]', pt) and not re.search(r'["“”]', en):
        return False
    if pt.isupper() and not en.isupper() and len(pt) > 3:
        return False
    if re.search(r"\b(\w{3,}),? \1\b", pt, re.I) and not re.search(r"\b(\w{3,}),? \1\b", en, re.I):   # "advogado, advogado"
        return False
    if ("*" in pt and "*" not in en) or len(pt) > 3 * len(en) + 10:
        return False
    return True


def arruma_glosa(en, pt):
    if (en[:1].islower() or en.startswith("I ")) and pt[:1].isupper() and not pt[1:2].isupper():
        pt = pt[0].lower() + pt[1:]
    return pt.rstrip(".") if not en.rstrip().endswith(".") else pt


def aplicar_glosas():
    bruto = traducoes("glosas")
    tr = {en: arruma_glosa(en, pt) for en, pt in bruto.items() if glosa_confiavel(en, pt)}
    if bruto:
        print(f"[glosas] {len(tr)} traduções aceitas, {len(bruto) - len(tr)} recusadas (ficam em inglês)")
    tr.update(GLOSAS_FIXAS)
    n = 0
    for arq in (DATA / "interlinear").glob("*/*.json"):
        versos, mudou = ler(arq), False
        for verso in versos:
            for p in verso:
                pt = ajusta_glosa(tr.get(p[3], p[3]))
                if pt != p[3]:
                    p[3] = pt; n += 1; mudou = True
        if mudou:
            gravar(arq, versos)
    mapa = mapa_glosas()
    mapa.update(tr)
    gravar(SITE / "ferramentas" / "glosas_pt.json", mapa)
    print(f"[glosas] {n} palavras atualizadas no interlinear")


# ---------------- verbos do interlinear ----------------
# A lista (frases verbais quebradas, já com a moldura tirada da gramática) é feita por
# ferramentas/corrigir_glosas.py preparar; a tradução volta para entradas/verbos_pt.json e é aplicada por
# ferramentas/corrigir_glosas.py aplicar, que precisa da fonte da STEPBible (não existe no GitHub Actions).
ENTRADAS = AQUI / "entradas"


def preparar_verbos():
    entradas("verbos", ler(ENTRADAS / "verbos.json"))


def aplicar_verbos():
    tr = traducoes("verbos")
    if not tr:
        return print("[verbos] nada traduzido ainda")
    (ENTRADAS / "verbos_pt.json").write_text(json.dumps(tr, ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"[verbos] {len(tr)} frases em tradutor/entradas/verbos_pt.json: aplique com ferramentas/corrigir_glosas.py aplicar")


# ---------------- temas (Nave) ----------------
def arquivos_temas():
    return [a for a in sorted((DATA / "topics").glob("*.json"))
            if a.name not in ("index.json", "aliases_pt.json", "titulos_pt.json", "doutrinas.json")]


def separa(linha):
    corpo = linha.lstrip("-").strip()
    m = REF.search(corpo)
    texto = (corpo[:m.start()] if m else corpo).strip(" ,;:")
    resto = corpo[m.start():] if m else ""
    return texto, resto


# cabeçalhos que se repetem centenas de vezes no Nave: tradução fixa, revisada
FRASES_NAVE = {
    "general scriptures concerning": "Textos gerais sobre", "figurative": "Figurado",
    "instances of": "Exemplos de", "symbolical": "Simbólico", "prophecies concerning": "Profecias sobre",
    "prophecy concerning": "Profecia sobre", "unclassified scriptures relating to": "Outros textos sobre",
    "death of": "Morte de", "descendants of": "Descendentes de", "exemplified": "Exemplificado",
    "forbidden": "Proibido", "enjoined": "Ordenado", "spiritual": "Espiritual", "of god": "De Deus",
    "of jesus": "De Jesus", "of david": "De Davi", "an ancestor of jesus": "Antepassado de Jesus",
    "a city of the tribe of judah": "Cidade da tribo de Judá", "a levite": "Um levita",
    "a priest": "Um sacerdote", "a benjamite": "Um benjamita", "one of the nethinim": "Um dos netineus",
    "israelites": "Israelitas", "instances of, see": "Exemplos de, veja",
}


def chave_nave(texto):
    return texto.lower().rstrip(":. ")


def texto_para_traduzir(texto):
    # o modelo não traduz texto todo em maiúsculas: normaliza para frase comum
    return texto.capitalize() if texto.isupper() else texto


def preparar_temas():
    itens = []
    for arq in arquivos_temas():
        for assunto, linhas in ler(arq).items():
            for i, l in enumerate(linhas):
                texto, _ = separa(l)
                if texto and re.search("[A-Za-z]", texto) and chave_nave(texto) not in FRASES_NAVE:
                    itens.append({"id": f"{arq.stem}|{assunto}|{i}", "texto": texto_para_traduzir(texto)})
    entradas("temas", itens)


def aplicar_temas():
    tr = traducoes("temas")
    if not tr:
        return print("[temas] nada traduzido ainda")
    for arq in arquivos_temas():
        sec = ler(arq)
        for assunto, linhas in sec.items():
            for i, l in enumerate(linhas):
                texto, _ = separa(l)
                pt = FRASES_NAVE.get(chave_nave(texto)) or tr.get(f"{arq.stem}|{assunto}|{i}")
                if pt and texto.lower().startswith("see "):
                    # remissões ("See music"): padroniza como "Veja ..."
                    pt = re.sub(r"(?i)^(veja|ver|consulte|vide)\s+", "", pt)
                    pt = "Veja " + pt[:1].lower() + pt[1:]
                if pt:
                    _, resto = separa(l)
                    linhas[i] = "-" + pt + (" " + resto if resto else "")
        sec["__pt"] = True
        gravar(DATA / "topics" / "pt" / arq.name, sec)
    print(f"[temas] {len(tr)} linhas gravadas em data/topics/pt/")


# ---------------- dicionário (Easton) ----------------
def arquivos_dic():
    return [a for a in sorted((DATA / "dictionary").glob("*.json"))
            if a.name not in ("index.json", "titulos_pt.json")]


# Referências do Easton ("Prov. 1:9; 3:22; Ps. 45:2") viram códigos USFM ("PRO 1:9; PRO 3:22; PSA 45:2") antes da
# tradução: o nllb.py as protege (o Argos tinha transformado "Ps." em "S.") e o app as mostra como links.
EASTON = {
    "Gen": "GEN", "Ge": "GEN", "Ex": "EXO", "Exod": "EXO", "Lev": "LEV", "Num": "NUM", "Nu": "NUM", "Deut": "DEU",
    "Josh": "JOS", "Judg": "JDG", "Judge": "JDG", "Ruth": "RUT", "1 Sam": "1SA", "2 Sam": "2SA", "1 Kings": "1KI",
    "2 Kings": "2KI", "2 King": "2KI", "1 Chr": "1CH", "2 Chr": "2CH", "1 Chron": "1CH", "2 Chron": "2CH", "1 Ch": "1CH",
    "2 Ch": "2CH",
    "Ezra": "EZR", "Neh": "NEH", "Esther": "EST", "Esth": "EST", "Job": "JOB", "Ps": "PSA", "Psalm": "PSA",
    "Psalms": "PSA", "Prov": "PRO", "Eccl": "ECC", "Eccles": "ECC", "Cant": "SNG", "Song of Sol": "SNG",
    "Isa": "ISA", "Jer": "JER", "Lam": "LAM", "Ezek": "EZK", "Exek": "EZK", "Dan.": "DAN", "Hos": "HOS",
    "Joel": "JOL", "Amos": "AMO", "Obad": "OBA", "Jonah": "JON", "Micah": "MIC", "Mic": "MIC", "Nahum": "NAM",
    "Nah": "NAM", "Hab": "HAB", "Zeph": "ZEP", "Hag": "HAG", "Zech": "ZEC", "Mal": "MAL", "Matt": "MAT",
    "Mat": "MAT", "Mark": "MRK", "Luke": "LUK", "John": "JHN", "Acts": "ACT", "Act": "ACT", "Rom": "ROM",
    "1 Cor": "1CO", "2 Cor": "2CO", "Gal": "GAL", "Eph": "EPH", "Phil": "PHP", "Col": "COL", "1 Thess": "1TH",
    "1 Thes": "1TH", "2 Thess": "2TH", "1 Tim": "1TI", "2 Tim": "2TI", "Titus": "TIT", "Philem": "PHM",
    "Philemon": "PHM", "Heb": "HEB", "James": "JAS", "Jas": "JAS", "1 Pet": "1PE", "2 Pet": "2PE", "1 John": "1JN",
    "2 John": "2JN", "3 John": "3JN", "Jude": "JUD", "Rev": "REV",
}
UM_CAPITULO = {"OBA", "PHM", "2JN", "3JN", "JUD"}   # "Jude 14" é o versículo 14
# "10:6, 13, 14": a lista de versículos para antes de outro livro numerado ("9:48, 1 Sam. 13:20")
_NUM_REF = r"\d+(?::\d+)?(?:[-–]\d+(?::\d+)?)?(?:,\s?\d+(?:[-–]\d+)?(?!\s?[A-Z]))*"
# "Dan" só com ponto: sem ele é a tribo
RE_EASTON = re.compile(r"(?<![\w.])(" + "|".join(re.escape(n) for n in sorted(EASTON, key=len, reverse=True))
                       + r")\.?\s(" + _NUM_REF + r")(?!\d|:\d)")
RE_CONTINUA = re.compile(r";\s?(" + _NUM_REF + r")(?!\d|:\d)")


def ref_usfm(cod, num):
    num = num.replace("–", "-")
    if cod in UM_CAPITULO and ":" not in num:
        num = "1:" + num
    return f"{cod} {num}"


def refs_usfm(texto):
    """"(Prov. 1:9; 3:22; Ps. 45:2)" -> "(PRO 1:9; PRO 3:22; PSA 45:2)". O "; 3:22" logo depois é do mesmo livro."""
    saida, i = [], 0
    for m in RE_EASTON.finditer(texto):
        if m.start() < i:
            continue
        cod = EASTON[m.group(1)]
        saida += [texto[i:m.start()], ref_usfm(cod, m.group(2))]
        j = m.end()
        while (c := RE_CONTINUA.match(texto, j)) and not RE_EASTON.match(texto, c.start(1)):
            depois = texto[c.end():c.end() + 2]
            if ":" not in c.group(1) and re.match(r"\s[a-z]", depois):   # "; 2 vols." não é referência
                break
            saida.append("; " + ref_usfm(cod, c.group(1)))
            j = c.end()
        i = j
    saida.append(texto[i:])
    return "".join(saida)


def limpa_easton(texto):
    """Sujeiras da fonte que atrapalham o tradutor: aspas com barra (\\"), número de link do site antigo
    ("[357]ALOES") e aspas de fechamento separadas da frase ('seguidores. "', que fazia o modelo inventar texto)."""
    texto = texto.replace('\\"', '"')
    texto = re.sub(r"\[\d+\](?=[A-Z])", "", texto)
    return re.sub(r'(?<=[.!?,;])\s+"(?=\s|\)|$)', '"', texto)


def preparar_dicionario():
    itens = []
    for arq in arquivos_dic():
        for termo, defs in ler(arq).items():
            for i, d in enumerate(defs):
                if d.strip():
                    itens.append({"id": f"{arq.stem}|{termo}|{i}", "texto": refs_usfm(limpa_easton(d))})
    entradas("dicionario", itens)


def aplicar_dicionario():
    tr = traducoes("dicionario")
    if not tr:
        return print("[dicionario] nada traduzido ainda")
    for arq in arquivos_dic():
        d = ler(arq)
        for termo, defs in d.items():
            d[termo] = [tr.get(f"{arq.stem}|{termo}|{i}", x) for i, x in enumerate(defs)]
        d["__pt"] = True
        gravar(DATA / "dictionary" / "pt" / arq.name, d)
    print(f"[dicionario] {len(tr)} definições gravadas em data/dictionary/pt/")


# ---------------- comentários (Calvino e Matthew Henry) ----------------
NUM_VERSO = re.compile(r"^\s*\d+(?:\s*[-,]\s*\d+)*\s*[\.:]?\s*")


def preparar_comentario(etapa, pasta):
    base = DATA / "commentaries" / pasta
    itens = []
    for livro in sorted(p for p in base.iterdir() if p.is_dir() and not p.name.startswith("pt")):
        for arq in sorted(livro.glob("*.json"), key=lambda a: int(a.stem)):
            for v, txt in ler(arq).items():
                if v.isdigit() and txt.strip():
                    # o número do versículo no início ("16.") vai separado, senão vira "16 anos."
                    corpo = NUM_VERSO.sub("", txt, count=1)
                    itens.append({"id": f"{livro.name}|{arq.stem}|{v}", "texto": corpo})
    entradas(etapa, itens)


def aplicar_comentario(etapa, pasta):
    tr = traducoes(etapa)
    if not tr:
        return print(f"[{etapa}] nada traduzido ainda")
    base = DATA / "commentaries" / pasta
    por_cap, originais = {}, {}
    for k, v in tr.items():
        livro, cap, verso = k.split("|")
        if (livro, cap) not in originais:
            originais[(livro, cap)] = ler(base / livro / f"{cap}.json")
        m = NUM_VERSO.match(originais[(livro, cap)].get(verso, ""))
        prefixo = m.group(0) if m else ""
        por_cap.setdefault((livro, cap), {})[verso] = prefixo + v
    for (livro, cap), versos in por_cap.items():
        versos["__pt"] = True
        gravar(base / "pt" / livro / f"{cap}.json", versos)
    print(f"[{etapa}] {len(tr)} blocos em {len(por_cap)} capítulos gravados em data/commentaries/{pasta}/pt/")


def preparar_calvino(): preparar_comentario("calvino", "calvin")
def aplicar_calvino(): aplicar_comentario("calvino", "calvin")
def preparar_henry(): preparar_comentario("henry", "henry")
def aplicar_henry(): aplicar_comentario("henry", "henry")


if __name__ == "__main__":
    acao, etapa = sys.argv[1], sys.argv[2]
    globals()[f"{acao}_{etapa}"]()
