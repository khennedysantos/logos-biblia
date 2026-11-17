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
        if not verbo_ruim(w, p[3]) or da_gramatica(w):
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


def da_gramatica(w):
    return any(w.en.strip(" ,.;:") == en and w.gram.startswith(gram) for en, gram in GRAMATICA)


def corrigir_gramatica(palavras, conta):
    for i, (w, p) in enumerate(palavras):
        # João 1: "ὁ λόγος" é "a Palavra" (o artigo grego é masculino, a palavra portuguesa é feminina)
        if w.gram.startswith("T-") and p[3] in ("o", "<o>") and i + 1 < len(palavras) \
                and palavras[i + 1][0][:3] == w[:3] and palavras[i + 1][1][3].startswith("Palavra"):
            novo = p[3].replace("o", "a")
            conta["gramatica"][(w.en, p[3], novo)] += 1
            p[3] = novo
            continue
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
    corrigir_tabela(palavras, conta)
    corrigir_gramatica(palavras, conta)
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
