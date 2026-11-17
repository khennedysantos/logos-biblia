"""Corrige as glosas do interlinear com a ajuda da fonte (STEPBible): cada palavra do site é alinhada com a da fonte
(stepbible.py), que tem a glosa em inglês e a gramática. Assim dá para achar o erro e acertar pela gramática.

O que corrige (cada parte conta no relatório):
1. nomes   — nome próprio ainda em inglês ("Elijah", "Yahweh") ou traduzido como palavra comum ("Ham" -> "Presunto",
             "Beer-sheba" -> "Cerveja") vira o nome da Bíblia Livre (nomes_pt.json; SENHOR para o nome divino).
             Se o versículo traz outra grafia bem parecida ("Jesaías"), vale a do versículo.
2. verbos  — concordância quebrada pela tradução palavra a palavra ("eles viu", "eu têm ouviu", "eles serão
             ajuntou") e verbo no singular com sujeito plural pela gramática. São retraduzidos pelo NLLB no GitHub
             Actions (etapa "verbos"): `preparar` grava a lista em tradutor/entradas/verbos.json, com o sujeito
             tirado da gramática quando a glosa não tem ("sent" 3P -> "they sent" -> "enviaram").
3. gramática — adjetivo grego feminino com glosa masculina ("vida eterno" -> "eterna"); a tabela GRAMATICA
             (glosa inglesa + gramática -> português: "loved" V-AAI-3S -> "amou", "may have" V-PAS-3S -> "tenha").
4. tabela  — glosas que ficaram em inglês (TABELA, escrita à mão).

uso:  python3 ferramentas/corrigir_glosas.py preparar
      python3 ferramentas/corrigir_glosas.py aplicar [--conferir] [--relatorio]
Depois de aplicar, rode validar_dados.py. Pode rodar de novo: o que já está certo não muda."""
import collections, json, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI / "tradutor"))
from stepbible import RAIZ, alinhar, gravar_capitulo, nome_proprio, pessoa   # noqa: E402
from nomes_pt import FUNCAO, candidatos, nome_ingles, semelhanca, textos_blivre  # noqa: E402
from etapas import ajusta_glosa                                               # noqa: E402

ENTRADAS = AQUI / "tradutor" / "entradas"
NOMES = AQUI / "nomes_pt.json"


# ---------------------------------------------------------------- 1. nomes
CONTRAI = [(r"\ba(\s+)(SENHOR)\b", r"ao\1\2"), (r"\bde(\s+)(SENHOR)\b", r"do\1\2"), (r"\bem(\s+)(SENHOR)\b", r"no\1\2"),
           (r"\bpor(\s+)(SENHOR)\b", r"pelo\1\2"), (r"\b(para|contra|com|como|sobre|entre)(\s+)(SENHOR)\b", r"\1 o\2\3")]


def contrai(g):
    for a, b in CONTRAI:
        g = re.sub(a, b, g)
    return g


def pontuacao_final(s):
    m = re.search(r"[,.;:!?]+$", s.strip())
    return m.group(0) if m else ""


def corrigir_nomes(palavras, textos, cand, mapa, conta):
    por_verso = collections.defaultdict(list)
    for w, p in palavras:
        por_verso[(w.livro, w.cap, w.v)].append((w, p))
    for chave, ws in por_verso.items():
        texto, cs = textos.get(chave, ""), cand.get(chave, set())
        i = 0
        while i < len(ws):
            w, p = ws[i]
            j = i + 1
            # "Beer-" + "sheba": a segunda parte começa com minúscula ("Jerusalém, Jerusalém" é repetição, não composto)
            # composto: "Beth" + "Shemesh", "Beer" + "Sheba" (a segunda parte vem sem prefixo e com outro nome);
            # "Saul" + "and  Saul" ou "Naaliel" + "and from  Naaliel" é o mesmo nome repetido
            while j < len(ws) and w.strong and ws[j][0].strong == w.strong and nome_proprio(w.gram) \
                    and "  " not in ws[j][0].en.strip() \
                    and nome_ingles(ws[j][0].en).lower() != nome_ingles(ws[j - 1][0].en).lower():
                j += 1
            if not (w.strong and nome_proprio(w.gram)):
                i += 1
                continue
            if j - i > 1:
                composto(ws[i:j], texto, cs, mapa, conta)
            else:
                simples(w, p, texto, cs, mapa, conta)
            i = j


def nome_no_verso(strong, en, texto, cs, mapa):
    """O nome da Bíblia Livre; se o versículo usa outra grafia bem parecida ("Jesaías"), a do versículo."""
    geral = mapa.get(strong, [None, None])[1]
    if geral and (geral in cs or geral in texto):
        return geral
    melhor = max(cs, key=lambda c: semelhanca(en, c), default=None)
    if melhor and not melhor.isupper() and semelhanca(en, melhor) >= 0.8:
        return melhor
    return geral


def simples(w, p, texto, cs, mapa, conta):
    en = nome_ingles(w.en)
    if not en:
        return
    alvo = nome_no_verso(w.strong, en, texto, cs, mapa)
    g = p[3]
    palavra = lambda x: re.compile(r"(?<![\wÀ-ÿ])" + re.escape(x) + r"(?![\wÀ-ÿ])")
    if not alvo or palavra(alvo).search(g):
        return
    if palavra(en).search(g):                              # ainda em inglês: "e  Benaiah"
        novo = palavra(en).sub(alvo, g)
    elif en == FUNCAO.sub("", w.en.strip(" ,.;:!?")) and g[:1].isupper():
        novo = alvo + pontuacao_final(w.en)                # a glosa é só o nome: "Presunto" (Ham), "Jeosafá"
    else:                                                  # "e Jeosafá": troca a palavra com maiúscula parecida
        m = list(re.finditer(r"[A-ZÀ-Ý][\wÀ-ÿ'’-]*", g))
        if len(m) != 1 or semelhanca(en, m[0].group(0)) < 0.5:
            return
        novo = g[:m[0].start()] + alvo + g[m[0].end():]
    novo = contrai(novo)
    if novo != g:
        conta["nomes"][(w.en, g, novo)] += 1
        p[3] = novo


def composto(partes, texto, cs, mapa, conta):
    """Nome de duas palavras na fonte ("Beer-" + "sheba"): o nome da Bíblia Livre ("Berseba") dividido entre elas."""
    ens = [re.sub(r"^.*?\s{2,}", "", w.en).strip(" ,.;:") for w, _ in partes]
    inteiro = ens[0].rstrip("-") + "-" + "-".join(e.lstrip("-") for e in ens[1:])
    alvo = max(cs, key=lambda c: semelhanca(inteiro, c), default=None)
    if not alvo or semelhanca(inteiro, alvo) < 0.6:
        geral = mapa.get(partes[0][0].strong, [None, None])[1]
        if not geral or semelhanca(inteiro, geral) < 0.6:
            return
        alvo = geral
    pedacos = dividir(alvo, ens)
    if not pedacos:
        return
    for (w, p), pedaco in zip(partes, pedacos):
        prefixo = re.match(r"^(.*?\s{2,})", w.en)
        novo = (traduz_prefixo(prefixo.group(1)) if prefixo else "") + pedaco + pontuacao_final(w.en)
        novo = contrai(novo)
        if novo != p[3]:
            conta["nomes"][(w.en, p[3], novo)] += 1
            p[3] = novo


def dividir(nome, partes_en):
    """"Bete-Semes" em ["Bete-", "Semes"]; "Berseba" em ["Ber-", "seba"] (onde as partes se parecem com o inglês)."""
    k = len(partes_en)
    if nome.count("-") == k - 1:
        p = nome.split("-")
        return [x + "-" for x in p[:-1]] + [p[-1]]
    if k == 2 and len(nome) >= 5:
        corte = max(range(2, len(nome) - 1),
                    key=lambda c: semelhanca(partes_en[0], nome[:c]) + semelhanca(partes_en[1], nome[c:]))
        return [nome[:corte] + "-", nome[corte:]]
    return None


PREFIXOS = {"and": "e", "to": "a", "from": "de", "in": "em", "of": "de", "the": "o", "[the]": "[o]", "<the>": "<o>",
            "towards": "para", "<towards>": "<para>", "<in>": "<em>", "<to>": "<a>", "like": "como", "with": "com"}


def traduz_prefixo(pre):
    partes = pre.split("  ")
    return "  ".join(PREFIXOS.get(x.strip(), x.strip()) for x in partes if x.strip()) + "  "


# ---------------------------------------------------------------- 2. verbos (NLLB)
# Frases curtas com sujeito o NLLB traduz bem ("they saw" -> "eles viram"); sozinho, um verbo inglês não diz a
# pessoa ("sent"), e "may X" fora de contexto vira "pode X". Por isso cada glosa vai numa moldura tirada da
# gramática, que depois é retirada: sujeito ("they sent" -> "enviaram"), subjuntivo ("so that he may have" ->
# "para que ele tenha" -> "tenha") e particípio ("the one who is believing" -> "aquele que crê" -> "crê").
PRONOMES = {"1S": "I", "2S": "you", "3S": "he", "1P": "we", "2P": "you all", "3P": "they"}
# sujeito no começo, depois de um colchete ("[who] he was raised") ou de um auxiliar de pergunta ("are you angry")
SUJEITO_EN = re.compile(r"^(?:\[[^\]]*\]\s*)?(?:(?:are|is|was|were|am|did|do|does|have|has|had|will|shall|would|"
                        r"should|could|can)\s+)?(?:I|you|he|she|it|we|they)\b", re.I)
TIRAR = {
    "fin": re.compile(r"^(?:eu|tu|ele|ela|nós|vós|eles|elas|você|vocês)\s+", re.I),
    "subj": re.compile(r"^(?:para que|a fim de que|de modo que|para|que)\s+(?:(?:eu|tu|ele|ela|nós|vós|eles|elas|você|vocês)\s+)?", re.I),
    "part": re.compile(r"^(?:aquele|aquela|aqueles|aquelas|o|a|os|as|quem)\s+(?:que\s+)?", re.I),
}
QUEBRADO = [
    re.compile(r"\b(?:eu|tu|nós|vós|eles|elas|vocês)\s+(?!vou\b|sou\b|estou\b|dou\b)[a-zà-ú]+(?:ou|eu|iu)\b", re.I),
    re.compile(r"\b(?:têm|tem|tinha|tinham|serão|será|eram|era|são|sido|ser|foram|foi|seria)\s+[a-zà-ú]+(?:ou|eu|iu)\b"),
    re.compile(r"\b(?:sou|é|são|era|eram|fui|foi|foram)\s+[a-zà-ú]+ndo\b"),
    re.compile(r"^que nós [a-zà-ú]+(?:ar|er|ir)\b"),
]
PREFIXO_VERBO = {"and": "e", "but": "mas", "¿": "¿", "for": "pois", "then": "então", "so": "assim"}
SUBJUNTIVO = re.compile(r"^V-\w*S-\d")                      # grego: V-PAS-3S, V-2AMS-3S, V-APS-3P
PARTICIPIO = re.compile(r"^V-\w+P-[NGDAV]")                  # grego: V-PAP-NSM


def verbo_ruim(w, g):
    if any(r.search(g) for r in QUEBRADO):
        return True
    if SUBJUNTIVO.match(w.gram) and re.match(r"(?:may|might|should)\b", w.en):
        return True
    if PARTICIPIO.match(w.gram) and re.search(r"\b(?:é|são|está|estão) [a-zà-ú]+(?:ar|er|ir)\b", g):
        return True
    pe = pessoa(w.gram)
    if not pe:
        return False
    pal = re.findall(r"[a-zà-ú]+", g.lower())
    verbo = next((x for x in pal if x not in ("e", "mas", "não", "se", "me", "te", "o", "a", "os", "as", "lhe", "lhes")), "")
    if pe in ("1P", "2P", "3P") and re.search(r"(?:ou|iu)$|(?<![dmst])eu$", verbo) and "você" not in pal[:1]:
        return True
    if pe == "2P" and pal[:1] == ["você"]:
        return True
    return pe == "3S" and bool(re.search(r"(?:aram|eram|iram)$", verbo))


def entrada_verbo(w):
    """(prefixo já em português, frase para o NLLB, moldura a tirar da tradução: "fin", "subj", "part" ou "")"""
    partes = w.en.split("  ")
    prefixo = []
    while len(partes) > 1 and partes[0].strip() in PREFIXO_VERBO:
        prefixo.append(PREFIXO_VERBO[partes.pop(0).strip()])
    frase = re.sub(r"\s+", " ", " ".join(partes)).strip().rstrip(",.;:")
    pe = pessoa(w.gram)
    if SUBJUNTIVO.match(w.gram) and re.match(r"(?:may|might|should)\b", frase) and pe:
        return " ".join(prefixo), f"so that {PRONOMES[pe]} {frase}", "subj"
    if PARTICIPIO.match(w.gram) and re.match(r"(?:is|are) ", frase):
        plural = re.match(r"V-\w+P-\w(P)", w.gram)
        return " ".join(prefixo), ("those who " if plural else "the one who ") + frase, "part"
    if pe and not SUJEITO_EN.match(frase) and not re.match(r"(?:let|may|Let|May)\b", frase):
        return " ".join(prefixo), PRONOMES[pe] + " " + frase, "fin"
    if pe == "2P" and frase.lower().startswith("you ") and not frase.lower().startswith("you all"):
        frase = "you all " + frase[4:]
    return " ".join(prefixo), frase, ""


def preparar():
    _, palavras = alinhar()
    itens = {}
    for w, p in palavras:
        if verbo_ruim(w, p[3]) and re.search(r"[A-Za-z]", w.en):
            _, frase, _ = entrada_verbo(w)
            itens[frase] = {"id": frase, "texto": frase}
    ENTRADAS.mkdir(exist_ok=True)
    (ENTRADAS / "verbos.json").write_text(json.dumps(list(itens.values()), ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(itens)} frases verbais para o NLLB gravadas em {(ENTRADAS / 'verbos.json').relative_to(RAIZ)}")


def corrigir_verbos(palavras, conta):
    arq = ENTRADAS / "verbos_pt.json"
    if not arq.exists():
        return print("(verbos: ainda sem a tradução do NLLB em tradutor/entradas/verbos_pt.json)")
    tr = json.loads(arq.read_text(encoding="utf-8"))
    for w, p in palavras:
        if not verbo_ruim(w, p[3]):
            continue
        prefixo, frase, moldura = entrada_verbo(w)
        pt = (tr.get(frase) or "").strip().rstrip(".")
        if moldura:
            pt = TIRAR[moldura].sub("", pt, count=1)
        if not pt or re.search(r"[A-Za-z]{3,}", pt) and not re.search(r"[ãõáéíóúâêôçà]|\b(?:e|de|que|se|o|a)\b", pt) \
                and pt.lower() in w.en.lower():
            continue                                        # o modelo devolveu o inglês: fica como está
        if w.en[:1].islower() and not pt[:2].isupper():
            pt = pt[0].lower() + pt[1:]
        novo = (prefixo + "  " if prefixo else "") + pt + pontuacao_final(w.en)
        if novo != p[3]:
            conta["verbos"][(w.en, p[3], novo)] += 1
            p[3] = novo


# ---------------------------------------------------------------- 3. gramática
# glosa inglesa + começo da gramática -> português. Vale depois do NLLB, então acerta também o que ele errar.
GRAMATICA = {
    ("loved", "V-AAI-3S"): "amou", ("loved", "V-AAI-3P"): "amaram", ("loved", "V-AAI-1S"): "amei",
    ("may have", "V-PAS-3S"): "tenha", ("may have", "V-PAS-2P"): "tenhais",
    ("is believing", "V-PAP"): "crê", ("is loving", "V-PAP"): "ama", ("are believing", "V-PAP-"): "creem",
    ("may perish", "V-2AMS-3S"): "pereça",
    ("believed", "V-AAI-3S"): "creu", ("believed", "V-AAI-3P"): "creram",
    ("they believed", "V-AAI-3P"): "creram", ("they believed", "HV"): "creram",
    ("In [the]", "PREP"): "Em [o]",
    ("everyone", "A-NSM"): "todo", ("everyone", "A-ASM"): "todo", ("everyone", "A-NSN"): "todo",
    ("everyone", "A-GSM"): "de todo", ("everyone", "A-VSM"): "todo",
}
ADJ_FEMININO = re.compile(r"^A-[NGDAV][SP]F")
# glosa de "adjetivo" grego que em português é substantivo, numeral ou advérbio: não muda de gênero
NAO_FLEXIONA = {"deserto", "quatro", "como", "dízimo", "lucro", "descanso", "ferro", "cedo", "vidro", "tudo", "meno",
                "cinco", "dentro", "fora", "pouco"}


def corrigir_gramatica(palavras, conta):
    for w, p in palavras:
        g, novo = p[3], None
        for (en, gram), pt in GRAMATICA.items():
            if w.en.strip(" ,.;:") == en and w.gram.startswith(gram):
                novo = pt + pontuacao_final(w.en)
                break
        if novo is None and w.en.startswith("having ") and re.match(r"ter [a-zà-ú]+(?:ado|ida|ido|ada|to|ta)\b", g):
            novo = "tendo " + g[4:]                                   # "having loved": "ter amado" -> "tendo amado"
        if novo is None and ADJ_FEMININO.match(w.gram):
            m = re.fullmatch(r"([a-zà-ú]+)o(s?)([,.;:!?]*)", g)     # "vida eterno" -> "eterna"
            if m and m.group(1) + "o" not in NAO_FLEXIONA and not m.group(1).endswith("nd"):
                novo = m.group(1) + "a" + m.group(2) + m.group(3)
        if novo is not None:
            novo = ajusta_glosa(novo)
            if novo != g:
                conta["gramatica"][(w.en, g, novo)] += 1
                p[3] = novo


# ---------------------------------------------------------------- 4. tabela (o que ficou em inglês)
TABELA = {}


def corrigir_tabela(palavras, conta):
    for w, p in palavras:
        pt = TABELA.get(w.en)
        if pt is None or p[3] == pt:
            continue
        if p[3] != w.en and not re.search(r"[A-Za-z]{3}", p[3]):
            continue
        conta["tabela"][(w.en, p[3], pt)] += 1
        p[3] = pt


# ----------------------------------------------------------------
def aplicar():
    conferir = "--conferir" in sys.argv
    caps, palavras = alinhar()
    antes = {k: json.dumps(v, ensure_ascii=False) for k, v in caps.items()}
    textos, minusc = textos_blivre()
    cand = {k: candidatos(t, minusc) for k, t in textos.items()}
    mapa = json.loads(NOMES.read_text(encoding="utf-8"))
    conta = {k: collections.Counter() for k in ("nomes", "verbos", "gramatica", "tabela")}
    corrigir_nomes(palavras, textos, cand, mapa, conta)
    corrigir_verbos(palavras, conta)
    corrigir_gramatica(palavras, conta)
    corrigir_tabela(palavras, conta)
    mudados = [k for k, v in caps.items() if json.dumps(v, ensure_ascii=False) != antes[k]]
    if not conferir:
        for livro, cap in mudados:
            gravar_capitulo(livro, cap, caps[(livro, cap)])
    for parte, c in conta.items():
        print(f"{parte}: {sum(c.values())} palavras ({len(c)} glosas diferentes)")
        if "--relatorio" in sys.argv:
            for (en, velho, novo), n in c.most_common(80):
                print(f"   {n:5}  {en!r}: {velho!r} -> {novo!r}")
    print(f"{len(mudados)} capítulos {'mudariam (nada gravado)' if conferir else 'gravados'}")


if __name__ == "__main__":
    {"preparar": preparar, "aplicar": aplicar}[sys.argv[1]]()
