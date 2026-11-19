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
5. revisão — as ~2.000 glosas mais frequentes lidas com o inglês ao lado (glosas_revisao.py).
6. sufixos — glosa hebraica com sufixo pronominal remontada parte por parte ("hand  his" -> "mão  dele").
7. formas  — "você" -> tu/vós, "eu têm falado" -> "eu falei", imperativo, plural de adjetivo, maiúscula (conjugar.py).
8. artigos — artigo grego concordando com a palavra portuguesa ("o terra" -> "a terra", "fazer" -> "do").
9. llm     — por último, as correções de sentido revisadas por LLM versículo a versículo (glosas_llm.json, gerado por
             tradutor/glosas_llm.py). Só trocam a glosa que ainda está igual à que o modelo viu ("de"); a palavra já
             corrigida fica fora das regras acima, para não ser desfeita.
             Depois delas entram as correções escritas à mão em glosas_manuais.json, no mesmo formato ("de" é a glosa
             que as regras deixaram; o glosas_llm.py regrava o glosas_llm.json, por isso as manuais ficam à parte).

uso:  python3 ferramentas/corrigir_glosas.py preparar
      python3 ferramentas/corrigir_glosas.py aplicar [--conferir] [--relatorio]
Depois de aplicar, rode validar_dados.py. As etapas se repetem até nada mudar: rodar de novo não muda nada."""
import collections, json, re, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI)); sys.path.insert(0, str(AQUI / "tradutor"))
from stepbible import RAIZ, alinhar, gravar_capitulo, nome_proprio, pessoa   # noqa: E402
from nomes_pt import FUNCAO, candidatos, nome_ingles, semelhanca, textos_blivre  # noqa: E402
from etapas import ajusta_glosa                                               # noqa: E402
from conjugar import P, Verbos, imperativo, infinitivos, participio, presente  # noqa: E402
from glosas_revisao import REVISAO                                            # noqa: E402

ENTRADAS = AQUI / "tradutor" / "entradas"
NOMES = AQUI / "nomes_pt.json"
GLOSAS_LLM = AQUI / "glosas_llm.json"
GLOSAS_MANUAIS = AQUI / "glosas_manuais.json"     # correções à mão no mesmo formato ({"LIVRO|cap|v|i": {de, para}})
SUBSTANTIVOS = AQUI / "substantivos_pt.json"


def hebraico(gram):
    """gramática hebraica ou aramaica ("HNcmsc/Sp3ms", "ANcbsa"); a grega tem hífen ("N-NSM", "A-NSM")"""
    return gram[:1] in ("H", "A") and gram[1:2] != "-"


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
    melhor = max(sorted(cs), key=lambda c: semelhanca(en, c), default=None)
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
    alvo = max(sorted(cs), key=lambda c: semelhanca(inteiro, c), default=None)
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


GERUNDIO = {"ar": "ando", "er": "endo", "ir": "indo", "or": "ondo"}


def limpa_nllb(pt, frase, en):
    """Vícios do modelo: o "you all" que a moldura pôs vira "todos"/"tudo"; "estava a fazer" (português de
    Portugal) vira "estava fazendo"; "Já ouvimos" (o modelo acrescenta "já"); "rezar" vira "orar"."""
    pt = pt.strip().rstrip(".")
    if "you all" in frase and "all" not in en.lower():
        pt = re.sub(r"\s*\b(?:todos|todas|tudo)\b", "", pt).strip()
    if "already" not in en.lower():
        pt = re.sub(r"(?i)^já\s+", "", pt)
    pt = re.sub(r"\b((?i:est(?:ou|á|ás|ava|avas|ávamos|avam|ão|amos|ive|eve|ivemos|iveram|ivesse|eja|ejam|ar|ará|arão|aria|ais|áis))\s+)a\s+([a-zà-ú]*?)(ar|er|ir|or)\b",
                lambda m: m.group(1) + m.group(2) + GERUNDIO[m.group(3)], pt)
    if not re.search(r"\b(?:say|said|tell|told)\b", en):
        pt = re.sub(r"\b(ouvi|ouviu|ouvimos|ouviram|ouviste|ouvistes)\s+(?:dizer|falar)\b", r"\1", pt)   # "ouvi dizer"
    if re.search(r"\bcall", en):
        pt = re.sub(r"\blig(uei|ou|aram|ar|amos|a|am|ando)\b", lambda m: "cham" + {"uei": "ei"}.get(m.group(1), m.group(1)), pt)
    pt = re.sub(r"\s*[:!?.,;]+$", "", pt) if re.search(r"[:!?.,;]$", pt) and not re.search(r"[!?]", en) else pt
    return re.sub(r"\brez(ar|a|am|em|e|ou|aram|ando|arão|ará|ai)\b", r"or\1", pt)


def corrigir_verbos(palavras, conta):
    arq = ENTRADAS / "verbos_pt.json"
    if not arq.exists():
        return print("(verbos: ainda sem a tradução do NLLB em tradutor/entradas/verbos_pt.json)")
    tr = json.loads(arq.read_text(encoding="utf-8"))
    for w, p in palavras:
        if not verbo_ruim(w, p[3]) or da_gramatica(w) or da_revisao(w) is not None:
            continue
        prefixo, frase, moldura = entrada_verbo(w)
        pt = limpa_nllb(tr.get(frase) or "", frase, w.en)
        if moldura:
            pt = TIRAR[moldura].sub("", pt, count=1)
        if w.en.startswith("I ") and pt[:1].isupper():
            pt = pt[0].lower() + pt[1:]                            # "Eu matei": como as outras glosas, minúsculo
        if not pt or re.search(r"[A-Za-z]{3,}", pt) and not re.search(r"[ãõáéíóúâêôçà]|\b(?:e|de|que|se|o|a)\b", pt) \
                and pt.lower() in w.en.lower():
            continue                                        # o modelo devolveu o inglês: fica como está
        if w.en[:1].islower() and not pt[:2].isupper():
            pt = pt[0].lower() + pt[1:]
        fim = pontuacao_final(w.en)
        pt = re.sub(r"\s*[!?]+$", "", pt) if fim and re.search(r"[!?]$", pt) else pt
        novo = (prefixo + "  " if prefixo else "") + pt + fim
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


PLURAL_ESPECIAL = {"mal": "maus", "bom": "bons", "são": "sãos", "vão": "vãos", "cristão": "cristãos", "pagão": "pagãos",
                   "irmão": "irmãos", "mão": "mãos", "pão": "pães", "cão": "cães", "capitão": "capitães", "cidadão": "cidadãos",
                   "grão": "grãos", "órfão": "órfãos"}
NAO_PLURAL = NAO_FLEXIONA | {"tudo", "nada", "muito mais", "mais", "menos", "cada", "todo-poderoso", "seis", "sete", "oito",
                            "nove", "dez", "doze", "três", "dois", "duas", "tolice", "um", "uma", "mil", "cem", "vinte", "trinta",
                            "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa", "onze", "quatorze",
                            "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"}


def pluralizar(p):
    if p in PLURAL_ESPECIAL:
        return PLURAL_ESPECIAL[p]
    if p.endswith("ão"):
        return p[:-2] + "ões"
    if re.search(r"[aeiouéêó]$", p):
        return p + "s"
    if p.endswith("vel"):
        return p[:-3] + "veis"
    if p.endswith("il"):
        return p[:-2] + ("eis" if re.search(r"[áéíóú]", p[:-2]) else "is")
    if re.search(r"[aeou]l$", p):
        return p[:-1] + {"a": "is", "e": "is", "o": "is", "u": "is"}[p[-2]] if p[-2] in "au" else \
            p[:-2] + {"e": "éis", "o": "óis"}[p[-2]]
    if re.search(r"[rz]$", p):
        return p + "es"
    if p.endswith("m"):
        return p[:-1] + "ns"
    return None


def plural_adjetivo(g, feminino):
    """glosa de um adjetivo grego plural ainda no singular ("pobre", "todo") -> "pobres", "todos"/"todas" """
    m = re.fullmatch(r"([a-zà-ú]+)([,.;:!]*)", g)
    if not m or m.group(1) in NAO_PLURAL or m.group(1).endswith("s"):
        return None
    p = m.group(1)
    if re.search(r"(?:ar|er|ir|ou|eu|iu|ndo|mente)$", p):                 # verbo, gerúndio, advérbio: não é adjetivo
        return None
    if feminino and p.endswith("o") and not p.endswith("ão") and p not in NAO_FLEXIONA:
        p = p[:-1] + "a"
    pl = pluralizar(p)
    return pl + m.group(2) if pl else None


def da_gramatica(w):
    return any(w.en.strip(" ,.;:") == en and w.gram.startswith(gram) for en, gram in GRAMATICA)


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
        ultima = w.gram.split("/")[-1]
        if novo is None and (re.match(r"[AN]-[NGDAV]P[MFN]$", w.gram) or hebraico(w.gram) and re.match(r"H?Aa[mfbc]p", ultima)):
            fem = w.gram[5:6] == "F" if not hebraico(w.gram) else re.match(r"H?Aaf", ultima) is not None
            novo = plural_adjetivo(g, fem)                                 # "os pobre" -> "os pobres"; "deuses outro"
        if novo is not None:
            novo = ajusta_glosa(novo)
            if novo != g:
                conta["gramatica"][(w.en, g, novo)] += 1
                p[3] = novo


# ---------------------------------------------------------------- 4. tabela (o que ficou em inglês)
# Glosa inglesa (sem a pontuação final) -> português. Só troca onde a glosa ainda é o inglês (ou parece inglês).
TABELA = {
    # termos e transliterações (a forma da Bíblia Livre)
    "Selah": "Selá", "Sela": "Selá", "acacia": "acácia", "Sabbath": "sábado", "shekels": "siclos", "manna": "maná",
    "aha!": "ah!", "Aha!": "Ah!", "Ha!": "Ah!", "ha": "ah", "mat": "esteira", "animal[s]": "animal[is]", "citi[es]": "cidade[s]",
    "gospel": "evangelho", "olive": "oliveira", "loops": "laçadas", "private": "particular", "fury": "fúria",
    "custom": "costume", "Leviathan": "Leviatã", "stadia": "estádios", "branch": "ramo", "splinter": "cisco",
    "cors": "coros", "cor[s] of": "coro[s] de", "Praetorium": "Pretório", "fin": "barbatana", "gerah[s]": "gera[s]",
    "reed": "cana", "curd<s>": "coalhada<s>", "denarii": "denários", "colt": "jumentinho", "Zebub": "Zebube",
    "Millo": "Milo", "Artemis": "Ártemis", "trigon": "trígono", "wadis": "ribeiros", "Hosanna": "Hosana",
    "Hosanna!": "Hosana!", "tashcheth": "tasquite", "Havvoth": "Havote", "hewing": "lavrando", "elder": "ancião",
    "Ephesian": "efésio", "cud": "ruminação", "copper": "cobre", "leanness": "magreza", "destroyers": "destruidores",
    "flint": "pederneira", "Magi": "magos", "Shoshannim": "Sosanim", "brimstone": "enxofre", "pit": "cova",
    "alamoth": "alamote", "alumoth": "alamote", "gentiles": "gentios", "Tyrian": "tírio", "lavers": "pias",
    "jaminites": "jaminitas", "jaminite": "jaminita", "dim": "escuro", "chance": "acaso", "Thessalonica": "Tessalônica",
    "Deacons": "Diáconos", "design": "propósito", "Berachah": "Beraca", "Lair": "covil", "lodges": "pousadas",
    "led": "conduzido", "stern": "popa", "host": "hospedeiro", "sycamores": "sicômoros", "teqel": "tequel",
    "Anak": "Anaque", "hyssop": "hissopo", "sashes": "faixas", "palm": "palmeira", "Meribath": "Meribá",
    "Meribah": "Meribá", "Abba": "Aba", "Zaphon": "Zafom", "herbage": "erva", "calamus": "cálamo", "Ramath": "Ramá",
    "saris": "oficial", "fowlers": "passarinheiros", "encamp": "acampar", "Rabboni": "Raboni", "chaff": "palha",
    "Abaddon": "Abadom", "Orion": "Órion", "Anakites": "anaquins", "rampart": "baluarte", "eczema": "sarna",
    "lepta": "leptos", "lepton": "lepto", "ax": "machado", "lake": "lago", "grainfields": "searas",
    "Gerasenes": "gerasenos", "Gadarenes": "gadarenos", "lema": "lamá", "sabachthani": "sabactâni",
    "requite": "retribuir", "eduth": "edute", "Jeduthun": "Jedutum", "jasper": "jaspe", "fawns": "filhotes",
    "Shimeathites": "simeatitas", "Harashim": "Harasim", "leavens": "fermenta", "commits": "comete",
    "proverb[s]": "provérbio[s]", "Ziphites": "zifeus", "Ashtaroth": "Astarote", "holily": "santamente",
    "Sukkites": "suquitas", "slings": "fundas", "castings": "fundições", "algum<s>": "sândalo<s>",
    "levity": "leviandade", "thorugh": "através de", "strikes": "fere", "race": "corrida", "Corinthians": "coríntios",
    "snuffers": "espevitadeiras", "capture": "captura", "carousal": "farra", "blots": "manchas", "continue": "continuai",
    "Basshebeth": "Bassebete", "Ahoah": "Aoá", "coppersmith": "latoeiro", "homestead": "herdade", "Ago": "atrás",
    "Cyrenian": "cireneu", "incited": "incitou", "Python": "píton", "Awoken": "desperto", "Grecian": "grego",
    "babbler": "tagarela", "Areopagite": "areopagita", "Asiarchs": "asiarcas", "Parthians": "partos", "Medes": "medos",
    "elderhood": "presbitério", "spearmen": "lanceiros", "tackle": "aparelho", "amiss": "mal",
    "Alexandrian": "alexandrino", "Alexandrians": "alexandrinos", "Colonnade": "pórtico", "Freedmen": "libertos",
    "Rephan": "Renfã", "Hellenists": "helenistas", "Scythian": "cita", "flake-like": "em flocos", "stacte": "estoraque",
    "boughs": "ramos", "bough[s]": "ramo[s]", "Bamah": "Bamá", "Sabeans": "sabeus", "kindle": "acender",
    "topaz": "topázio", "terebinth": "terebinto", "Evident": "evidente", "carousing": "orgias", "seahs": "medidas",
    "seahs of": "medidas de", "mandrakes": "mandrágoras", "gopher": "gofer", "shiggionoth": "sigionote",
    "Partakers": "participantes", "Levitical": "levítico", "bowmen": "flecheiros", "roomy": "espaçoso",
    "cliffs": "penhascos", "beryl": "berilo", "mire": "lodo", "elm": "olmeiro", "brushwood<s>": "graveto<s>",
    "bridling": "refreando", "Shibboleth": "Chibolete", "Sibboleth": "Sibolete", "Lehi": "Leí", "tawny": "fulvo",
    "Shemesh": "Semes", "bristly": "eriçado", "vipers": "víboras", "sandal": "sandália", "shepherd": "pastor",
    "morsel": "bocado", "litras": "libras", "metretae": "metretas", "soudarion": "lenço", "Clay": "barro",
    "Behemoth": "Beemote", "purslane": "beldroega", "marsh": "pântano", "tread": "pisar", "autumnal": "outonal",
    "crimson": "carmesim", "graves": "sepulturas", "assarion": "asse", "Yoke": "jugo", "manger": "manjedoura",
    "hills": "colinas", "rebuking": "repreendendo", "tablet": "tábua", "brow": "topo", "bier": "esquife",
    "Immanuel": "Emanuel", "didrachmas": "didracmas", "foreman": "mordomo", "dill": "endro", "mill": "moinho",
    "gall": "fel", "meek": "manso", "kodranten!": "quadrante!", "net-casting": "lançando a rede", "Eloi": "Eloí",
    "Talitha": "Talita", "koum!": "cumi!", "Syrophoenician": "siro-fenícia", "Ephphatha!": "Efatá!", "usury": "usura",
    "Sophereth": "Soferete", "myrtle": "murta", "homers": "ômeres", "Cushite": "cuxita", "lodge": "pousar",
    "Zophim": "Zofim", "soda": "salitre", "reprove": "repreender", "counsel<s>": "conselho<s>", "flash": "relâmpago",
    "extol": "exaltai", "Mahalath": "Maalate", "Machalath": "Maalate", "evil deeds": "más obras", "plotted": "tramou",
    "in <the>  prosperiti<es>": "em <as>  prosperidade<s>", "voluntariness<es>": "voluntariedade<s>",
    "repetition[s]": "repetição[ões]", "Higgaion": "Higaiom", "golden": "dourado", "harping": "tocando harpa",
    "swung": "brandiu", "citron": "tuia", "sardonyx": "sardônica", "sardius": "sárdio", "jacinth": "jacinto",
    "choenixes": "medidas", "Lamb!": "Cordeiro!", "censer": "incensário", "Wormwood": "Absinto", "leads": "leva",
    "nard": "nardo", "Cretans": "cretenses", "Cretan": "cretense", "sorrel": "alazão", "dappled": "malhado",
    "¿  I": "¿  eu", "Temeni": "Temeni", "Haahashtari": "Haastari", "Jehieli": "Jeieli", "will": "vontade",
    # glosas hebraicas em partes (sufixo possessivo depois do nome) e perguntas que ficaram em inglês
    "palm  my": "palma  minha", "palm  his": "palma  sua", "palm  the": "a  palma", "rod  his": "vara  sua",
    "rods  their": "varas  suas", "net  my": "rede  minha", "nest  its": "ninho  seu", "edge  its": "borda  sua",
    "boughs  its": "ramos  seus", "chambers  its": "câmaras  suas", "grain  his": "grão  seu", "prime  my": "vigor  meu",
    "jaw  its": "queixada  sua", "jaws  my": "queixadas  minhas", "halter  its": "cabresto  seu",
    "sneezing<s>  its": "espirro<s>  seus", "moustache  his": "bigode  seu", "acquaintances  my": "conhecidos  meus",
    "nostril[s]  your": "narina[s]  tuas", "work<s>  my": "obra<s>  minhas", "community  your": "comunidade  tua",
    "myrrh  my": "mirra  minha", "O rock  my": "ó rocha  minha", "from  sanctuari<es>  your": "de  santuário<s>  teus",
    "bowls of": "tigelas de", "treasuring up": "entesourando", "interest of": "juro de", "<into>  dung": "<em>  esterco",
    "Mizpah of": "Mispa de", "<of> [which] not": "<de> [que] não", "<into>  guilt": "<em>  culpa",
    "has he come out": "saiu ele", "money of": "dinheiro de", "[will] delay": "[vai] tardar", "he reckon": "ele considera",
    "are you speaking": "estás falando", "did they steal  you": "roubaram-te", "has it been taken away": "foi tirado",
    "did you treat with contempt  me": "desprezaste-me", "and  <obj.>  [the] [one] living of": "e  <obj.>  [o] [que] vive de",
    "did you sign": "assinaste", "¿  was he able": "¿  pôde ele", "[one who] is wounded of": "[o que] é ferido de",
    "grinding [it]": "moendo [-o]", "will he lie down": "deitar-se-á", "[one who] slays": "[o que] mata",
    "knead [it]": "amassai [-a]", "and  it be[longs]": "e  pertence", "<in>  [the] sinew of": "<em>  [o] tendão de",
    "<into>  burning": "<para>  queima", "[one who] rejoices": "[o que] se alegra", "<into>  a burning of": "<em>  queima de",
    "will you restrain yourself": "conter-te-ás", "<the>  hired": "<o>  contratado", "[the] land of  <towards>": "[a] terra de  <para>",
    "and  [the] land of  <towards>": "e  [a] terra de  <para>", "<in>  [the] thickets of": "<em>  [os] matagais de",
    "will it speak": "falará", "¿  will you play": "¿  brincarás", "has he uncovered": "descobriu ele",
    "has he opened": "abriu ele", "<into>  seven": "<em>  sete", "rule over": "dominar", "heard [it]": "ouviram [isso]",
    "At the pledging": "No penhor", "In [the] fourth": "[No] quarto", "[one who] scatters": "[o que] espalha",
    "cub of": "filhote de", "<the>  wares": "<as>  mercadorias", "<obj.>[about]": "<obj.>[sobre]",
    "<the>  feeble": "<os>  fracos", "¿  will they finish": "¿  terminarão", "<the>  debris": "<o>  entulho",
    "[will] meat": "[será] carne", "beaten out of": "batido de", "<into>  consuming": "<para>  consumir",
    "and  to  [the] obligation of": "e  a  [a] obrigação de", "[will] snatch up": "[vai] arrebatar",
    "they take pleasure in": "eles se agradam de", "[are] he": "[é] ele", "will he lead  me": "guiar-me-á",
    "[one who] he pants": "[o que] ofega", "will you forget  me": "esquecer-me-ás", "will you hide": "esconderás",
    "[the] desires of": "[os] desejos de", "[one who] recognizes": "[o que] reconhece", "and  [the] request of": "e  [o] pedido de",
    "have you forsaken  me": "desamparaste-me", "<in>  [the] troubles of": "<em>  [as] angústias de",
    "from  [the] hostility of": "de  [a] hostilidade de", "have you forgotten  me": "esqueceste-me",
    "will he search out": "esquadrinhará", "rich [ones] of": "ricos de", "desirous of": "desejoso de",
    "a miscarriage of": "um aborto de", "will you attack": "atacareis", "<the>  pushed down": "<o>  derrubado",
    "things of": "coisas de", "thousands of": "milhares de", "heavens of": "céus de", "may I be delivered": "seja eu livrado",
    "[one who] is at peace with  me": "[o que] está em paz comigo", "¿  has it come to an end": "¿  acabou",
    "¿  has he forgotten": "¿  esqueceu", "has he shut off": "encerrou ele", "[is] wounding  my": "[é] ferida  minha",
    "have you smoked": "fumegaste", "have you broken down": "derrubaste", "will they give thanks to?  you": "darão graças a?  ti",
    "¿  will it be known": "¿  será conhecido", "receiving [it]": "recebendo [-o]", "obtained [it]": "obtido [-o]",
    "cleaving to": "apegando-se a", "it is like": "é semelhante",
}
SO_INGLES = set("""the and of to he she they you will is are was were have has had his her their my your who which that it
be not for with from on by at we shall may let been being this these those them him us does did all out up into upon over
said says saying what when where there then than but or if so its our whom whose would could should might must""".split())


def parece_ingles(g, en):
    if g.strip() == en.strip():
        return True
    pal = re.findall(r"[A-Za-z]+", g)
    return bool(pal) and sum(x.lower() in SO_INGLES for x in pal) >= max(1, len(pal) // 2)


def corrigir_tabela(palavras, conta):
    for w, p in palavras:
        fim = pontuacao_final(w.en) if w.en.strip() not in TABELA else ""
        chave = w.en.strip()[:len(w.en.strip()) - len(fim)] if fim else w.en.strip()
        pt = TABELA.get(chave)
        if pt is None or not parece_ingles(p[3], w.en) and p[3] not in ('"Tows of"', '"Ned its"', '"Boughs its"', "No concurso",
                                                                         "No quarto...", "remain over", "moagem [it]",
                                                                         "amassar [it]", "ouvimos [it]", "recebendo [it].",
                                                                         "obtidos [it];", '"Cleaving to"', "treasing up",
                                                                         "♪Into> esterco", "# # Into # # Culpa #", "[ Will] atraso",
                                                                         "[ Will] carne", "[ Will] pegar", "[Into] queimando",
                                                                         "[Into> sete", "[Into] consumindo", "<the<br>contratado",
                                                                         "mirrrh my", "Mizpah of"):
            continue
        novo = pt + fim
        if novo != p[3]:
            conta["tabela"][(w.en, p[3], novo)] += 1
            p[3] = novo


# ---------------------------------------------------------------- 5. revisão (glosas_revisao.py)
def _pontuacao(en):
    fim = pontuacao_final(en)
    chave = en.strip()
    return (chave[:len(chave) - len(fim)].rstrip() if fim else chave), fim


_POR_GRAMATICA = collections.defaultdict(list)
for _k, _v in REVISAO.items():
    if isinstance(_k, tuple) and _k[1] not in ("H", "G"):
        _POR_GRAMATICA[_k[0]].append((_k[1], _v))


def da_revisao(w):
    chave, _ = _pontuacao(w.en)
    for sel, pt in _POR_GRAMATICA.get(chave, ()):
        if w.gram.startswith(sel):
            return pt
    for k in ((chave, "H" if hebraico(w.gram) else "G"), chave):
        if k in REVISAO:
            return REVISAO[k]
    if chave[:1].isupper() and chave[:2] not in ("O ", "I "):        # "It came to pass": vale "it came to pass"
        return da_revisao(w._replace(en=chave[0].lower() + w.en.strip()[1:]))
    return None


def pessoa_da_palavra(gram):
    """"2S", "3P"...: a do sufixo pronominal hebraico, se há; senão a do verbo"""
    suf = sufixo(gram) if hebraico(gram) else None
    if suf:
        return {"1s": "1S", "2s": "2S", "1p": "1P", "2p": "2P"}.get(suf, "3P" if suf.endswith("p") else "3S")
    return pessoa(gram)


def corrigir_revisao(palavras, conta):
    for w, p in palavras:
        pt = da_revisao(w)
        if isinstance(pt, dict):                                      # {"2S": "guardarás", "2P": "guardareis"}
            pt = pt.get(pessoa_da_palavra(w.gram)) or pt.get("*")
        if pt is None:
            continue
        novo = pt + _pontuacao(w.en)[1]
        if w.en[:1].isupper() and not w.en.startswith(("I ", "O ")) and not pt[:1].isupper() and pt[:1] not in "<[¿":
            novo = novo[0].upper() + novo[1:]
        if novo != p[3]:
            conta["revisao"][(w.en, p[3], novo)] += 1
            p[3] = novo


# ---------------------------------------------------------------- 6. gênero e número em português
_LEXICO = {}


def lexico():
    """{palavra: (gênero, número)} tirado da Bíblia Livre: o determinante antes da palavra ("da terra", "as obras",
    "seu coração") diz o gênero e o número dela em português. Só palavras com pelo menos 2 ocorrências claras."""
    if _LEXICO:
        return _LEXICO
    det = {}
    for g, n, ws in [("m", "s", "o do no ao pelo um dum num este esse aquele deste desse daquele neste nesse naquele meu teu "
                                "seu nosso vosso"),
                     ("f", "s", "da na à pela uma duma numa esta essa aquela desta dessa daquela nesta nessa naquela minha "
                                "tua sua nossa vossa"),
                     ("m", "p", "os dos aos pelos uns estes esses aqueles destes desses daqueles nestes nesses naqueles meus "
                                "teus seus nossos vossos"),
                     ("f", "p", "as das nas às pelas umas estas essas aquelas destas dessas daquelas nestas nessas naquelas "
                                "minhas tuas suas nossas vossas")]:
        for x in ws.split():
            det[x] = (g, n)
    conta = collections.defaultdict(collections.Counter)
    for t in textos_blivre()[0].values():
        toks = re.findall(r"[A-Za-zÀ-ÿ]+", t)
        for a, b in zip(toks, toks[1:]):
            if a.lower() in det:
                conta[b.lower()][det[a.lower()]] += 1
    for pal, c in conta.items():
        tot = sum(c.values())
        if tot < 2:
            continue
        fem = sum(v for (g, _), v in c.items() if g == "f")
        pl = sum(v for (_, n), v in c.items() if n == "p")
        g = "f" if fem >= 0.75 * tot else "m" if fem <= 0.25 * tot else None
        n = "p" if pl >= 0.75 * tot else "s" if pl <= 0.25 * tot else None
        _LEXICO[pal] = (g, n)
    return _LEXICO


VAZIAS = set("um uma uns umas o a os as de do da dos das em no na nos nas ao à aos às e para por pelo pela pelos pelas com "
             "que se mas pois ó meu minha meus minhas teu tua teus tuas seu sua seus suas nosso nossa nossos nossas vosso vossa "
             "vossos vossas dele dela deles delas é são era eram está estão".split())
TERMINA_F = re.compile(r"(?:ção|ções|são|sões|dade|dades|tude|tudes|gem|gens|ez|eza|ezas|ice|ices|a|as|ãe|ães)$")


def genero_numero(glosa, g_orig=None, n_orig=None):
    """(gênero, número) da palavra principal da glosa portuguesa ("[o] coração de" -> m, s). Sem dado no léxico,
    vale a terminação ("-ção", "-a": feminino) e depois o gênero e o número da palavra original."""
    t = next((x for x in re.findall(r"[A-Za-zÀ-ÿ]+", glosa or "") if x.lower() not in VAZIAS), None)
    g, n = g_orig, n_orig
    if t:
        lg, ln = lexico().get(t.lower(), (None, None))
        if lg or ln:
            g, n = lg or g, ln or n
        elif t[:1].islower() and not t.endswith("ndo"):
            g = "f" if TERMINA_F.search(t) else "m" if re.search(r"(?:o|os|or|ores)$", t) else g
            n = "p" if t.endswith("s") and n is None else n
    return g or "m", n or "s"


FLEXAO = {"meu": ("meu", "minha", "meus", "minhas"), "teu": ("teu", "tua", "teus", "tuas"),
          "nosso": ("nosso", "nossa", "nossos", "nossas"), "vosso": ("vosso", "vossa", "vossos", "vossas"),
          "o": ("o", "a", "os", "as"), "do": ("do", "da", "dos", "das"), "ao": ("ao", "à", "aos", "às"),
          "no": ("no", "na", "nos", "nas"), "pelo": ("pelo", "pela", "pelos", "pelas"),
          "aquele": ("aquele", "aquela", "aqueles", "aquelas"), "daquele": ("daquele", "daquela", "daqueles", "daquelas"),
          "àquele": ("àquele", "àquela", "àqueles", "àquelas"), "oqual": ("o qual", "a qual", "os quais", "as quais"),
          "algum": ("algum", "alguma", "alguns", "algumas"), "este": ("este", "esta", "estes", "estas"),
          "tu": ("tu", "tu", "vós", "vós")}


def flexiona(chave, g, n):
    cap = chave[:1].isupper()
    v = FLEXAO[chave.lower()][{("m", "s"): 0, ("f", "s"): 1, ("m", "p"): 2, ("f", "p"): 3}[(g, n)]]
    return v[0].upper() + v[1:] if cap else v


# ---------------------------------------------------------------- 7. hebraico: sufixos pronominais
# O sufixo hebraico vem separado na glosa inglesa ("hand  his", "to  him", "and  from  servants  your"), e a tradução
# automática juntava as partes ou inventava ("pouse o seu", "Ela é uma boa garota"). Essas glosas são remontadas parte
# por parte: preposições e conjunções (PREP_HEB), o substantivo (substantivos_pt.json) e o pronome pela gramática do
# sufixo — terceira pessoa "dele/dela/deles/delas" (como o inglês: his, her, their); primeira e segunda concordam com o
# substantivo português ("mão  minha", "olhos  teus"). Sp2ms é "tu"; Sp2mp é "vós", como na Bíblia Livre.
PREP_HEB = {
    "and": "e", "in": "em", "to": "a", "from": "de", "for": "para", "by": "por", "on": "sobre", "upon": "sobre", "with": "com",
    "according to": "segundo", "of": "de", "at": "em", "like": "como", "as": "como", "some of": "alguns de",
    "any of": "qualquer de", "one of": "um de", "among": "entre", "more than": "mais do que", "since": "desde",
    "against": "contra", "over": "sobre", "into": "para", "towards": "para", "toward": "para", "above": "acima de",
    "concerning": "acerca de", "about": "acerca de", "because of": "por causa de", "on account of": "por causa de",
    "away from": "longe de", "beside": "junto de", "before": "diante de", "after": "depois de", "between": "entre",
    "behind": "atrás de", "under": "debaixo de", "beneath": "debaixo de", "around": "ao redor de", "in place of": "em lugar de",
    "instead of": "em lugar de", "besides": "além de", "near": "perto de", "through": "por", "until": "até", "unto": "a",
    "within": "dentro de", "in front of": "diante de", "for own sake": "por amor de", "for sake": "por amor de",
    "woe! to": "ai de", "¿": "¿", "<obj.>": "<obj.>", "from with": "de junto de", "from before": "de diante de",
    "from between": "de entre", "from under": "de debaixo de", "from after": "de após", "from upon": "de sobre",
    "from on": "de sobre", "than": "do que", "except": "exceto",
}
COMPARA = {"like", "as", "more than", "than", "except"}               # "como tu", "mais do que eu": pronome sujeito
PRON_SUJ_SUF = {"1s": "eu", "2s": "tu", "3ms": "ele", "3fs": "ela", "1p": "nós", "2p": "vós", "3mp": "eles", "3fp": "elas"}
VERBO_COLCHETE = {"is": ("está", "é"), "are": ("estão", "são"), "was": ("estava", "era"), "were": ("estavam", "eram"),
                  "am": ("estou", "sou"), "will be": ("estará", "será"), "be": ("esteja", "seja"),
                  "belongs": "pertence", "belonged": "pertencia", "belong": "pertencem", "will belong": "pertencerá",
                  "belonging": "pertencente", "has been": "esteve", "becomes": "torna-se"}
LOCAL = {"in", "on", "upon", "with", "at", "among", "over", "from", "under", "before", "after", "between", "behind", "above"}


def traduz_prep(parte):
    """"[is] in <the>" -> "[está] em"; "<to>" -> "<a>"; None se não conhece"""
    p = re.sub(r"\s*<the>\s*", " ", parte).strip()
    if not p:
        return ""
    m = re.match(r"^\[([^\]]+)\]\s*(.*)$", p)
    verbo = ""
    if m:
        v, p = m.group(1), m.group(2)
        if v not in VERBO_COLCHETE:
            return None
        pt = VERBO_COLCHETE[v]
        if isinstance(pt, tuple):
            pt = pt[0] if p.strip("<>") in LOCAL else pt[1]
        verbo = f"[{pt}]"
        if not p:
            return verbo
    ang = None if p in PREP_HEB else re.fullmatch(r"<([^<>]+)>", p)
    base = PREP_HEB.get(ang.group(1) if ang else p)
    if base is None:
        return None
    base = f"<{base}>" if ang and base != "<obj.>" else base
    return (verbo + " " + base).strip()


PRON_OBJ = {"1s": "mim", "2s": "ti", "3ms": "ele", "3fs": "ela", "1p": "nós", "2p": "vós", "3mp": "eles", "3fp": "elas"}
REFLEXIVOS = {"himself", "herself", "itself", "themselves"}
OBJETO_EN = {"me", "you", "him", "her", "it", "us", "them", "myself", "yourself", "himself", "herself", "itself",
             "ourselves", "yourselves", "themselves"}
POSSESSIVO_EN = {"my", "your", "his", "her", "its", "our", "their"}
CONTRACOES_PRON = [(r"\bde\s+(el[ae]s?)\b", r"d\1"), (r"\bem\s+(el[ae]s?)\b", r"n\1"), (r"\bcom\s+mim\b", "comigo"),
                   (r"\bcom\s+ti\b", "contigo"), (r"\bcom\s+nós\b", "conosco"), (r"\bcom\s+vós\b", "convosco"),
                   (r"\bcom\s+si\b", "consigo")]


def sufixo(gram):
    """"Sp3ms" -> ("3ms" para a 3ª pessoa, "2s"/"2p" etc. para as outras)"""
    m = re.search(r"Sp([123])([mfbc])([sp])$", gram)
    if not m:
        return None
    p, g, n = m.groups()
    return f"3{'f' if g == 'f' else 'm'}{n}" if p == "3" else p + n


def possessivo(suf, g, n):
    if suf.startswith("3"):
        return {"3ms": "dele", "3fs": "dela", "3mp": "deles", "3fp": "delas"}[suf]
    return flexiona({"1s": "meu", "2s": "teu", "1p": "nosso", "2p": "vosso"}[suf], g, n)


MARCAS_NOME = re.compile(r"^((?:O |\[is\] |\[are\] |\[am\] |\[was\] |\[were\] |own |<of> )*)(.*)$")


def traduz_substantivo(en, subst):
    """"[are] servants" -> ("[são] servos", "servos"); None se o substantivo não está no dicionário"""
    marcas, nucleo = MARCAS_NOME.match(en.strip()).groups()
    pt = subst.get(nucleo)
    if not pt:
        return None
    _, n = genero_numero(pt)
    antes = []
    for mk in re.findall(r"O |\[\w+\] |own |<of> ", marcas):
        mk = mk.strip()
        antes.append({"O": "ó", "[is]": "[é]", "[am]": "[sou]", "[was]": "[era]", "[were]": "[eram]", "own": "",
                      "<of>": "<de>", "[are]": "[são]" if n == "p" else "[és]"}[mk])
    return " ".join(x for x in antes + [pt] if x), pt


def juntar(partes):
    s = "  ".join(x for x in partes if x)
    for a, b in CONTRACOES_PRON:
        s = re.sub(a, b, s)
    return s


def remonta_sufixo(w, p, subst):
    """A glosa hebraica com sufixo pronominal remontada; None se não é desse tipo ou se alguma parte é desconhecida."""
    if not hebraico(w.gram) or "/Sp" not in "/" + w.gram[1:]:
        return None
    suf = sufixo(w.gram)
    morf = w.gram[1:].split("/")
    partes = [x.strip() for x in w.en.split("  ")]
    if not suf or len(partes) != len(morf) or len(partes) < 2:
        return None
    fim = pontuacao_final(partes[-1])
    ultima = partes[-1].strip(" ,.;:!?")
    juntas = []                                                       # "from  with  you": "de junto de  ti"
    for x in partes[:-1]:
        x2 = re.sub(r"\s*<the>\s*", " ", x).strip()
        if juntas and juntas[-1] == "from" and x2 in ("with", "before", "between", "under", "after", "upon", "on"):
            juntas[-1] = "from " + x2
        else:
            juntas.append(x)
    partes = juntas + [partes[-1]]
    nominal = bool(re.match(r"(?:N[cgpt]|A[acog]|V\w[rs])", morf[-2]))  # substantivo, adjetivo ou particípio
    if ultima in POSSESSIVO_EN and (nominal or ultima != "her"):       # "and  from  servants  your"
        prefixos = [traduz_prep(x) for x in partes[:-2]]
        nome = traduz_substantivo(partes[-2], subst)
        if None in prefixos:
            return None
        if nome is None:                                              # substantivo fora do dicionário: só a concordância
            atual = p[3].split("  ")
            if len(atual) != len(partes) or not re.fullmatch(r"(?:meu|minha|meus|minhas|teu|tua|teus|tuas|seu|sua|seus|"
                                                              r"suas|nosso|nossa|nossos|nossas|vosso|vossa|vossos|vossas|"
                                                              r"dele|dela|deles|delas)[,.;:!?]*", atual[-1].strip()):
                return None
            g, n = genero_numero(atual[-2], *genero_hebraico(morf[-2]))
            return "  ".join(atual[:-1] + [possessivo(suf, g, n) + fim])
        texto, pt = nome
        g, n = genero_numero(pt, *genero_hebraico(morf[-2]))
        saida = juntar(prefixos + [texto, possessivo(suf, g, n)]) + fim
    elif ultima in OBJETO_EN and not nominal:                         # "to  him", "<obj.>  them", "from  with <the>  you"
        prefixos = [traduz_prep(x) for x in partes[:-1]]
        if None in prefixos or not any(prefixos):
            return None
        base = re.sub(r"^\[[^\]]+\]\s*|\s*<the>\s*", "", partes[-2]).strip("<> ")
        pron = "si" if ultima in REFLEXIVOS else PRON_SUJ_SUF[suf] if base in COMPARA else PRON_OBJ[suf]
        saida = juntar(prefixos + [pron]) + fim
    else:
        return None
    if w.en[:1].isupper() and not w.en.startswith(("O ", "I ")) and saida[:1].islower():
        saida = saida[0].upper() + saida[1:]
    return saida


def genero_hebraico(morf):
    """"Ncfpc" -> ("f", "p"); comum ou dual: o número português decide"""
    m = re.match(r"(?:Nc|Ng|Np|Aa|Ac|Ao|V\w\w)([mfbc])([spd])", morf)
    if not m:
        return None, None
    g = {"m": "m", "f": "f"}.get(m.group(1))
    return g, {"s": "s", "p": "p", "d": "p"}[m.group(2)]


def corrigir_sufixos(palavras, conta):
    subst = json.loads(SUBSTANTIVOS.read_text(encoding="utf-8"))
    for w, p in palavras:
        novo = remonta_sufixo(w, p, subst)
        if novo is None and hebraico(w.gram) and re.fullmatch(r"H?R", w.gram.split("/")[-1]) \
                and re.fullmatch(r"\[[^\]]+\] [a-z ]+", w.en.strip()):
            novo = traduz_prep(w.en.strip())                               # "[is] with" -> "[está] com"
        if novo and novo != p[3]:
            conta["sufixos"][(w.en, p[3], novo)] += 1
            p[3] = novo


# ---------------------------------------------------------------- 8. formas: tu/vós, pretérito, maiúsculas
# "você"/"vocês" (tradução automática) vira "tu"/"vós", com o verbo conjugado (conjugar.py): "você fará" -> "tu farás",
# "você vai fazer" -> "tu farás", "de você" -> "de ti". O perfeito inglês traduzido ao pé da letra ("eu têm falado",
# "ele tem dado") vira pretérito ("eu falei", "ele deu"). Glosa que começa com maiúscula sem motivo ("E ele disse")
# passa para minúscula, como as outras.
PRON_SUJ = {"eu": "1S", "tu": "2S", "ele": "3S", "ela": "3S", "isso": "3S", "nós": "1P", "vós": "2P", "eles": "3P",
            "elas": "3P", "você": "2S", "vocês": "2P"}
AUX_TER = {"tenho": "1S", "tens": "2S", "tem": "3S", "temos": "1P", "tendes": "2P", "têm": "3P"}
MINUSCULAS = set("E O A Os As Um Uma Uns Umas Eu Ele Ela Eles Elas Nós Vós Tu Você Vocês Para De Do Da Dos Das No Na Nos "
                 "Nas Em Com Por Pelo Pela Sobre Antes Depois Então Mas Porque Pois Que Se Não Isso Isto Este Esta Esse "
                 "Essa Aquele Aquela Todo Toda Todos Todas Tudo Ao À Aos Às Entre Contra Como Quando Onde Assim Também "
                 "Ainda Já Agora Aqui Ali Lá Eis Seu Sua Meu Minha Teu Tua Nosso Nossa Dele Dela Deles Delas".split())
_VERBOS = []


def verbos():
    if not _VERBOS:
        pal = set(textos_blivre()[1])
        _VERBOS.append(Verbos(infinitivos(pal)))
    return _VERBOS[0]


VOCE = re.compile(r"\b(?P<pron>[Vv]ocês?)(?P<ja> já)?(?P<refl> se)?(?P<neg> não)?(?P<cl> (?:me|nos|o|a|os|as|lhe|lhes))? "
                  r"(?:(?:vai|vão|irá|irão) (?P<refl2>se )?(?P<inf>[a-zà-ú]+(?:ar|er|ir|or|ôr))(?![\w-])|(?P<forma>[a-zà-ú]+)(?![\w-]))")


def segunda_pessoa(g, pes):
    """"você fará" -> "tu farás"; pes = "2S" ou "2P" (da gramática, quando há)"""
    V = verbos()

    def troca(m):
        pron = m.group("pron")
        plural = pron.lower() == "vocês"
        alvo = pes or ("2P" if plural else "2S")
        if m.group("inf"):                                             # "você vai fazer" -> "tu farás"
            nova = V.futuro_de(m.group("inf"), alvo)
        elif m.group("forma") in NAO_VERBO or m.group("forma") in PREPOSICOES:
            return m.group(0)
        else:
            nova = V.trocar_pessoa(m.group("forma"), "3P" if plural else "3S", alvo)
        if not nova:
            return m.group(0)
        tu = "tu" if alvo == "2S" else "vós"
        tu = tu.capitalize() if pron[:1].isupper() else tu
        refl = (" te" if alvo == "2S" else " vos") if m.group("refl") or m.group("refl2") else ""
        return f"{tu}{m.group('ja') or ''}{refl}{m.group('neg') or ''}{m.group('cl') or ''} {nova}"
    g = VOCE.sub(troca, g)
    # "você" objeto depois do verbo ("eu vou fazer você" -> "fazer-te") e "você" sozinho ("não você", "todos vocês")
    def objeto(m):
        verbo, pron = m.group(1), m.group(2)
        e_verbo = verbo in V.formas or verbo in V.part or re.search(r"(?:ar|er|ir|ndo)$", verbo)
        if not e_verbo or verbo in NAO_VERBO:
            return m.group(0)
        return f"{verbo}-{'vos' if pron.lower() == 'vocês' or pes == '2P' else 'te'}"
    g = re.sub(r"\b([a-zà-ú]+)\s+(vocês?)\b(?!\s+(?!" + "|".join(PREPOSICOES) + r")\b[a-zà-ú])", objeto, g)
    g = re.sub(r"\b([Vv])ocês\b(?!\s+[a-zà-ú])", lambda m: "Vós" if m.group(1) == "V" else "vós", g)
    g = re.sub(r"\b([Vv])ocê\b(?!\s+[a-zà-ú])", lambda m: ("Tu" if m.group(1) == "V" else "tu") if (pes or "2S") == "2S"
               else ("Vós" if m.group(1) == "V" else "vós"), g)
    return g


NAO_VERBO = set("não que se de para com e mas como então exceto aqui ali lá todos todas só também nem ou porque pois quando "
                "onde até sobre entre contra sem perante".split())
PREPOSICOES = ["para", "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "a", "ao", "à", "com", "por", "pelo",
               "pela", "sobre", "até", "contra", "entre", "fora", "diante", "depois", "antes"]
PREP_VOCE = [(r"\bcom você\b", "contigo"), (r"\bcom vocês\b", "convosco"), (r"\b(de|para|em|a|por|sobre|contra|entre|"
             r"diante de|depois de|antes de|sem|até|perante) você\b", r"\1 ti"),
             (r"\b(de|para|em|a|por|sobre|contra|entre|diante de|depois de|antes de|sem|até|perante) vocês\b", r"\1 vós")]


def preterito(g, pes):
    """"eu têm falado" -> "eu falei"; "isso tem sido escrito" -> "isso foi escrito" """
    V = verbos()

    def troca(m):
        pron, aux, sido, part = m.group(1), m.group(2), m.group(3), m.group(4)
        p_ = PRON_SUJ.get((pron or "").strip().lower()) or pes or AUX_TER[aux]
        if sido:
            ser = V.preterito_de("sido", p_)
            return f"{pron or ''}{ser} {part}" if ser else m.group(0)
        nova = V.preterito_de(part, p_)
        return f"{pron or ''}{nova}" if nova else m.group(0)
    return re.sub(r"\b((?:eu|tu|ele|ela|isso|nós|vós|eles|elas) )?(tenho|tens|tem|temos|tendes|têm) (sido )?"
                  r"([a-zà-ú]+(?:ado|ido|ito|eito|isto|osto|erto|indo))\b", troca, g)


def participio_depois_de_ter(g):
    """"tendo enviou", "ele tinha disse" -> "tendo enviado", "ele tinha dito" """
    V = verbos()

    def troca(m):
        infs = {i for i, t, _ in V.formas.get(m.group(2), ()) if t == "pret"}
        parts = {participio(i) for i in infs} - {None}
        return m.group(1) + parts.pop() if len(parts) == 1 else m.group(0)
    return re.sub(r"\b((?:[Tt]endo|[Tt]inha|tinhas|[Tt]inham|tínhamos|ter|[Hh]avia|haviam|haver|tenho|tens|tem|temos|"
                  r"tendes|têm) )([a-zà-ú]+)\b", troca, g)


PESSOA_PRON = {"eu": "1S", "tu": "2S", "nós": "1P", "vós": "2P", "ele": "3S", "ela": "3S", "eles": "3P", "elas": "3P"}
VAI = {"vou": "1S", "vais": "2S", "vai": "3S", "vamos": "1P", "ides": "2P", "vão": "3P"}


def concordancia_pronome(g):
    """"tu são" -> "tu és", "nós saber" -> "nós sabemos", "eu têm" -> "eu tenho", "eles foi" -> "eles foram".
    Com ele/ela/eles/elas só no pretérito, futuro, imperfeito e condicional: no presente a forma pode ser um
    substantivo ("eles casa")."""
    V = verbos()

    def troca(m):
        pron, verbo = m.group(1), m.group(2)
        alvo = PESSOA_PRON[pron.lower()]
        analises = V.formas.get(verbo, set())
        if any(pe == alvo for _, _, pe in analises):
            return m.group(0)
        if alvo.startswith("3"):
            if analises and all(t in ("pret", "fut", "imperf", "cond") for _, t, _ in analises):
                nova = V.trocar_pessoa(verbo, "3S" if alvo == "3P" else "3P", alvo)
                return f"{pron} {nova}" if nova else m.group(0)
            if verbo in V.infs and not analises:
                return f"{pron} {presente(verbo)[P.index(alvo)]}"
            return m.group(0)
        if verbo in V.infs and not analises - {(i, t, pe) for i, t, pe in analises if t == "pres"}:
            return f"{pron} {presente(verbo)[P.index(alvo)]}"
        for de in ("3S", "3P"):
            if any(pe == de for _, _, pe in analises):
                nova = V.trocar_pessoa(verbo, de, alvo)
                if nova:
                    return f"{pron} {nova}"
        if verbo in V.infs:
            return f"{pron} {presente(verbo)[P.index(alvo)]}"
        return m.group(0)
    return re.sub(r"\b([Ee]u|[Tt]u|[Nn]ós|[Vv]ós|[Ee]les?|[Ee]las?) ([a-zà-úâêô]+)\b", troca, g)


def futuro_simples(g):
    """"e eu vou cortar" -> "e eu cortarei" (o inglês tem "will")"""
    V = verbos()

    def troca(m):
        pron, aux, se, inf = m.group(1), m.group(2), m.group(3), m.group(4)
        pe = PESSOA_PRON.get(pron.lower(), VAI[aux])
        nova = V.futuro_de(inf, pe)
        clitico = ({"1S": "me ", "2S": "te ", "1P": "nos ", "2P": "vos "}.get(pe, "se ") if se == "se " else se) if se else ""
        return f"{pron} {clitico}{nova}" if nova else m.group(0)
    return re.sub(r"\b([Ee]u|[Tt]u|[Ee]les?|[Ee]las?|[Nn]ós|[Vv]ós) (vou|vais|vai|vamos|ides|vão) "
                  r"((?:se|me|te|nos|vos|lhe|lhes|o|a|os|as) )?([a-zà-ú]+(?:ar|er|ir|or|ôr))(?![\w-])", troca, g)


IMPERATIVO = re.compile(r"V\w(v)(\d)[mfc]?([sp])|V-\w+M-(\d)([SP])")


def imperativo_glosa(w, g):
    """imperativo traduzido como infinitivo ("seek": "buscar" -> "busca"/"buscai"; grego "do take": "fazer tomar" -> "tomai")"""
    m = IMPERATIVO.search(w.gram.split("/")[-1] if hebraico(w.gram) else w.gram)
    if not m:
        return g
    pes = (m.group(2) + m.group(3).upper()) if m.group(2) else (m.group(4) + m.group(5))
    if pes not in ("2S", "2P"):
        return g
    mm = re.fullmatch(r"((?:e|mas|e não|não)\s+)?(?:fazer )?([a-zà-ú]+(?:ar|er|ir|or|ôr))(-se)?([!,.;:]*)", g.strip())
    if not mm or (mm.group(1) or "").strip().startswith("não"):
        return g
    inf = mm.group(2)
    if inf not in verbos().infs and not re.search(r"(?:ar|er|ir)$", inf):
        return g
    imp = imperativo(inf, pes)
    if not imp:
        return g
    if mm.group(3):
        imp += "-te" if pes == "2S" else "-vos"
    pre = mm.group(1) or ""
    return (pre.rstrip() + "  " if pre else "") + imp + mm.group(4)


def minusculas_blivre():
    """quantas vezes cada palavra aparece em minúscula na Bíblia Livre ("amor": muitas; "Gibeá": nenhuma)"""
    if not _MINUSC:
        _MINUSC.append(textos_blivre()[1])
    return _MINUSC[0]


_MINUSC = []
PRONOME_DIVINO = re.compile(r"\b(?:Me|Mine|My|Myself|Him|His|He|Himself|You|Your|Yours|Yourself)\b")


def minuscula_inicial(w, g):
    """"E ele disse" -> "e ele disse" quando o inglês começa com minúscula (o tradutor pôs maiúscula)"""
    t = re.match(r"^([A-ZÀ-Ý][a-zà-ú]*)\b", g)
    if not t or PRONOME_DIVINO.search(w.en):
        return g
    if t.group(1) not in MINUSCULAS and minusculas_blivre()[t.group(1).lower()] < 5:   # nome próprio: fica
        return g
    if re.match(r"^[a-z<\[]", w.en.strip()) or w.en.startswith("I ") and t.group(1) == "Eu":
        return g[0].lower() + g[1:]
    return g


def corrigir_formas(palavras, conta):
    for w, p in palavras:
        g = p[3]
        pes = pessoa(w.gram)
        pes = pes if pes in ("2S", "2P") else None
        if hebraico(w.gram) and not pes:
            suf = sufixo(w.gram)
            pes = {"2s": "2S", "2p": "2P"}.get(suf)
        novo = minuscula_inicial(w, g)
        if re.search(r"\b[Vv]ocês?\b", novo):
            for a, b in PREP_VOCE:
                novo = re.sub(a, b, novo)
            if pes == "2P":
                novo = re.sub(r"\b(de|para|em|a|por|sobre) ti\b", r"\1 vós", novo).replace("contigo", "convosco")
            novo = segunda_pessoa(novo, pes)
            novo = re.sub(r"\bvocê mesmo\b", "ti mesmo" if not pes or pes == "2S" else "vós mesmos", novo)
        if re.search(r"[A-Za-zÀ-ÿ]\s*(?::|…|\.\.\.)[:….]*$", novo) and not re.search(r"[:…]$|\.\.\.$", w.en.strip()):
            novo = re.sub(r"\s*[:….]+$", "", novo)                        # "e ele disse:" (o dois-pontos é do tradutor)
        novo = re.sub(r"\b(de|a|para|em|por|sobre|contra|entre) tu\b", r"\1 ti", novo)
        novo = re.sub(r"\bcom tu\b", "contigo", novo)
        novo = re.sub(r"\b[Dd]e Ele\b", "dEle", novo)
        novo = re.sub(r"\bde (el[ae]s?|est[ea]s?|ess[ea]s?|aquel[ea]s?|isto|isso|aquilo)\b", r"d\1", novo)  # "de estes"
        novo = re.sub(r"\b(eu|tu|ele|ela|nós|vós|eles|elas|mim|ti|si) (?:\1|eu) (mesm[oa]s?)\b", r"\1 \2", novo,
                      flags=re.I)                                          # "ele ele mesmo", "mim eu mesmo"
        novo = re.sub(r"\b(?:(um|uma) )?queimad[ao] oferta\b", lambda m: "um holocausto" if m.group(1) else "holocausto", novo)
        novo = re.sub(r"\bqueimad[ao]s? ofertas\b", "holocaustos", novo)
        if w.en.startswith("to ") and re.match(r"a [a-zà-ú]+(?:ar|er|ir|or|ôr)\b", novo):
            novo = novo[2:]                                                # "to see": "a ver" -> "ver" (infinitivo grego)
        novo = re.sub(r"\bshekel(s?)\b", lambda m: "siclo" + m.group(1), novo)
        if hebraico(w.gram) and w.gram.endswith("/Sd") and re.search(r"(?:towards>?|-ward)$", w.en.strip()) \
                and da_revisao(w) is None:
            resto = re.sub(r"\s*-?\s*(?:em direção(?: a| para)?|para frente)\s*$", "", novo).strip()
            if resto and not resto.startswith("para"):                  # "Babilônia em direção" -> "para  Babilônia"
                novo = "para  " + resto
        if re.search(r"\bcall", w.en):                                   # "call" virou "ligar" (telefone)
            novo = re.sub(r"\blig(uei|ou|aram|ar|amos|a|am|ando)\b", lambda m: "cham" + {"uei": "ei"}.get(m.group(1), m.group(1)), novo)
        if re.match(r"it ", w.en) and re.match(r"(?:isso|ele|ela) [a-zà-ú]", novo):
            novo = novo.split(" ", 1)[1]                                   # "it will be done": "isso será feito" -> "será feito"
        novo = re.sub(r"\bpecado (oferta)\b", r"\1 pelo pecado", novo)
        novo = re.sub(r"\b(?:(um|uma) )?cereal oferta\b", lambda m: ("uma " if m.group(1) else "") + "oferta de cereais", novo)
        novo = re.sub(r"\b(aqueles?|aquelas?|\])\s*quem\b", r"\1 que", novo)      # "[aqueles] quem" -> "[aqueles] que"
        novo = re.sub(r"\[(é|sou|são|era|eram)\] acerca da? (\w+r)\b",
                      lambda m: "[" + {"é": "está", "sou": "estou", "são": "estão", "era": "estava", "eram": "estavam"}[m.group(1)]
                      + "] para " + m.group(2), novo)                      # "[is] about to give"
        novo = re.sub(r"\[(é|são|era|eram|sou)\] ([a-zà-ú]+ndo|em pé|assentad[oa]s?|sentad[oa]s?|deitad[oa]s?)\b",
                      lambda m: "[" + {"é": "está", "são": "estão", "era": "estava", "eram": "estavam", "sou": "estou"}[m.group(1)]
                      + "] " + m.group(2), novo)                           # "[são] dizendo" -> "[estão] dizendo"
        novo = imperativo_glosa(w, novo)
        novo = participio_depois_de_ter(novo)
        if re.search(r"\b(?:tenho|tens|tem|temos|tendes|têm) ", novo) and re.search(r"\b(?:have|has)\b", w.en):
            novo = preterito(novo, pessoa(w.gram))
        if re.search(r"\b(?:will|shall)\b", w.en):
            novo = futuro_simples(novo)
        novo = concordancia_pronome(novo)
        novo = minuscula_inicial(w, novo)
        if novo != g:
            conta["formas"][(w.en, g, novo)] += 1
            p[3] = novo


# ---------------------------------------------------------------- 9. artigos gregos
# O artigo grego tinha sempre a glosa "o" ("o terra", "o obras") e "of the" virava "fazer". O artigo agora concorda
# com a palavra portuguesa a que se refere (a primeira, no mesmo versículo, com o mesmo caso, número e gênero —
# de preferência um substantivo): "a terra", "as obras", "da vida", "à igreja". O gênero e o número vêm da glosa
# portuguesa (léxico da Bíblia Livre: "λόγος" é "a palavra"), e na falta dela, do grego (neutro = masculino).
ARTIGO = {
    "the": "{o}", "<the>": "<{o}>", "of the": "{do}", "to the": "{ao}", "those": "{aquele}", "The": "{O}",
    "the [one]": "{o} [que]", "which": "{oqual}", "the [One]": "{o} [que]", "in the": "{no}", "The [one]": "{O} [que]",
    "to those": "{àquele}", "with the": "com {o}", "of those": "{daquele}", "on the": "sobre {o}", "for the": "para {o}",
    "by the": "{pelo}", "Those": "{Aquele}", "which [is]": "{oqual} [é]", "which [are]": "{oqual} [são]", "To the": "{Ao}",
    "to the [one]": "{ao} [que]", "that which": "{o} que", "On the": "Sobre {o}", "at the": "{no}", "The [One]": "{O} [que]",
    "than the": "do que {o}", "from the": "{do}", "[is] the": "[é] {o}", "the [One who]": "{o} [que]", "some": "{algum}",
    "Some": "{Algum}", "to the [One]": "{ao} [que]", "that which [is]": "{o} que [é]", "the [ones]": "{o} [que]",
    "this": "{este}", "of the [One]": "{do} [que]", "of the [One who]": "{do} [que]", "To those": "{Àquele}",
    "those who": "{aquele} que", "To the [one]": "{Ao} [que]", "To the [One]": "{Ao} [que]", "for those": "para {aquele}",
    "with those": "com {aquele}", "the [one who]": "{o} [que]", "of the [one]": "{do} [que]", "<of the>": "<{do}>",
    "over the": "sobre {o}", "the [one] who": "{o} [que]", "the [One] who": "{o} [que]", "Of the": "{Do}",
    "against the": "contra {o}", "the ones": "{o} que", "[on] the": "[sobre] {o}", "he who": "{aquele} que",
    "He who": "{Aquele} que", "he who [is]": "{aquele} que [é]", "He who [is]": "{Aquele} que [é]", "among the": "entre {o}",
    "as the": "como {o}", "about the": "acerca {do}", "[to] the": "[a] {o}", "[in] the": "[em] {o}", "[of] the": "[de] {o}",
    "<of> the": "<de> {o}", "<to the>": "<{ao}>", "to the [ones]": "{ao} [que]", "before the": "diante {do}",
    "during the": "durante {o}", "when the": "quando {o}", "For the": "Para {o}", "[are] the": "[são] {o}",
    "of the [one who is]": "{do} [que é]", "[as] the": "[como] {o}", "[Is] the": "[É] {o}", "[be] the": "[ser] {o}",
    "the [One who is]": "{o} [que é]", "of the -": "{do} -", "those [who]": "{aquele} [que]", "who": "{o} que",
    "you who [are]": "{tu} que", "You who [are]": "{Tu} que", "who [is]": "{o} que [é]", "that [is]": "{o} que [é]",
}


def cabeca(verso, i):
    """índice da palavra a que o artigo verso[i] se refere: o primeiro substantivo seguinte com o mesmo caso, número e
    gênero; sem ele, a primeira palavra concordante (adjetivo, particípio); para no verbo finito."""
    pat = re.compile(r"-" + verso[i][0].gram[2:5] + r"(?:-|$)")
    primeiro = None
    for j in range(i + 1, min(len(verso), i + 7)):
        gm = verso[j][0].gram
        if pat.search(gm):
            if gm.startswith("N-"):
                return j
            if primeiro is None:
                primeiro = j
        elif re.match(r"V-\w+-[123]", gm):
            break
    return primeiro


def corrigir_artigos(palavras, conta):
    versos = collections.defaultdict(list)
    for w, p in palavras:
        if not hebraico(w.gram):
            versos[(w.livro, w.cap, w.v)].append((w, p))
    for vs in versos.values():
        for i, (w, p) in enumerate(vs):
            if not w.gram.startswith("T-") or len(w.gram) < 5:
                continue
            chave, fim = _pontuacao(w.en)
            modelo = ARTIGO.get(chave)
            if not modelo:
                continue
            g_gr, n_gr = ("f" if w.gram[4] == "F" else "m"), ("p" if w.gram[3] == "P" else "s")
            j = cabeca(vs, i)
            g, n = g_gr, n_gr
            if j is not None and vs[j][0].gram.startswith("N-") and not re.search(r"-[PLT]$", vs[j][0].gram):
                g, _ = genero_numero(vs[j][1][3], g_gr, None)
                plural_pt = lexico().get(_principal(vs[j][1][3]), (None, None))[1] == "p"    # "trevas", "vestes"
                n = "p" if n_gr == "p" or plural_pt else "s"
            novo = re.sub(r"\{(\w+)\}", lambda m: flexiona(m.group(1), g, n), modelo) + fim
            if novo != p[3]:
                conta["artigos"][(w.en, p[3], novo)] += 1
                p[3] = novo


def _principal(glosa):
    return next((x.lower() for x in re.findall(r"[A-Za-zÀ-ÿ]+", glosa or "") if x.lower() not in VAZIAS), "")


# ---------------------------------------------------------------- 9. revisão por LLM
def chave_palavra(w):
    return f"{w.livro}|{w.cap}|{w.v}|{w.i}"


def correcoes_llm():
    """as do LLM mais as escritas à mão palavra por palavra (glosas_manuais.json, que valem por cima)"""
    llm = json.loads(GLOSAS_LLM.read_text(encoding="utf-8")) if GLOSAS_LLM.exists() else {}
    if GLOSAS_MANUAIS.exists():
        llm.update(json.loads(GLOSAS_MANUAIS.read_text(encoding="utf-8")))
    return llm


def corrigir_llm(palavras, llm, conta):
    for w, p in palavras:
        c = llm.get(chave_palavra(w))
        if c and p[3] == c["de"]:
            conta["llm"][(w.en, p[3], c["para"])] += 1
            p[3] = c["para"]


# ----------------------------------------------------------------
def aplicar():
    conferir = "--conferir" in sys.argv
    caps, palavras = alinhar()
    antes = {k: json.dumps(v, ensure_ascii=False) for k, v in caps.items()}
    textos, minusc = textos_blivre()
    cand = {k: candidatos(t, minusc) for k, t in textos.items()}
    mapa = json.loads(NOMES.read_text(encoding="utf-8"))
    conta = {k: collections.Counter() for k in ("nomes", "verbos", "tabela", "revisao", "sufixos", "gramatica", "formas",
                                                 "artigos", "llm")}
    llm = correcoes_llm()
    todas = palavras          # as já corrigidas pelo LLM não passam pelas regras (que poderiam desfazer a correção)
    palavras = [(w, p) for w, p in todas if not (c := llm.get(chave_palavra(w))) or p[3] != c["para"]]
    for volta in range(1, 6):         # uma correção abre caminho para outra ("O Tofeth" -> "o Tofeth" -> "o Tofete"):
        antes_da_volta = [p[3] for _, p in palavras]                  # repete até não mudar nada, e então rodar de novo
        c = conta if volta == 1 else {k: collections.Counter() for k in conta}   # também não muda
        corrigir_nomes(palavras, textos, cand, mapa, c)
        corrigir_verbos(palavras, c)
        corrigir_tabela(palavras, c)
        corrigir_revisao(palavras, c)
        corrigir_sufixos(palavras, c)
        corrigir_gramatica(palavras, c)
        corrigir_formas(palavras, c)
        corrigir_artigos(palavras, c)
        if [p[3] for _, p in palavras] == antes_da_volta:
            break
    corrigir_llm(todas, llm, conta)
    mudados = [k for k, v in caps.items() if json.dumps(v, ensure_ascii=False) != antes[k]]
    if not conferir:
        for livro, cap in mudados:
            gravar_capitulo(livro, cap, caps[(livro, cap)])
    for parte, c in conta.items():
        print(f"{parte}: {sum(c.values())} palavras ({len(c)} glosas diferentes)")
        if "--relatorio" in sys.argv:
            for (en, velho, novo), n in c.most_common(80):
                print(f"   {n:5}  {en!r}: {velho!r} -> {novo!r}")
    print(f"{len(mudados)} capítulos {'mudariam (nada gravado)' if conferir else 'gravados'} ({volta} voltas)")


if __name__ == "__main__":
    {"preparar": preparar, "aplicar": aplicar}[sys.argv[1]]()
