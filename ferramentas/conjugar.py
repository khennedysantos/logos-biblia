"""Conjugação mínima do português, para corrigir glosas do interlinear (corrigir_glosas.py):
- "você fará" -> "tu farás", "vocês farão" -> "vós fareis" (o interlinear e a Bíblia Livre usam tu/vós);
- "ele tem falado", "eu têm feito" (tradução palavra a palavra do perfeito inglês) -> "ele falou", "eu fiz".

Reconhece a forma pela lista de verbos (infinitivos do texto da Bíblia Livre e das glosas) e pelas tabelas de
irregulares abaixo; forma que não reconhece, ou que pode ser de dois verbos com resultados diferentes, fica como está.
Pessoas: "1S", "2S", "3S", "1P", "2P", "3P" (as de stepbible.pessoa)."""
import re

P = ("1S", "2S", "3S", "1P", "2P", "3P")

# pretérito perfeito irregular
PRET = {
    "ser": "fui foste foi fomos fostes foram", "ir": "fui foste foi fomos fostes foram",
    "fazer": "fiz fizeste fez fizemos fizestes fizeram", "dizer": "disse disseste disse dissemos dissestes disseram",
    "ver": "vi viste viu vimos vistes viram", "dar": "dei deste deu demos destes deram",
    "pôr": "pus puseste pôs pusemos pusestes puseram", "vir": "vim vieste veio viemos viestes vieram",
    "ter": "tive tiveste teve tivemos tivestes tiveram", "estar": "estive estiveste esteve estivemos estivestes estiveram",
    "saber": "soube soubeste soube soubemos soubestes souberam", "trazer": "trouxe trouxeste trouxe trouxemos trouxestes trouxeram",
    "querer": "quis quiseste quis quisemos quisestes quiseram", "poder": "pude pudeste pôde pudemos pudestes puderam",
    "haver": "houve houveste houve houvemos houvestes houveram",
}
# presente irregular (todas as pessoas)
PRES = {
    "ser": "sou és é somos sois são", "estar": "estou estás está estamos estais estão", "ter": "tenho tens tem temos tendes têm",
    "vir": "venho vens vem vimos vindes vêm", "ir": "vou vais vai vamos ides vão", "ver": "vejo vês vê vemos vedes veem",
    "dar": "dou dás dá damos dais dão", "crer": "creio crês crê cremos credes creem", "ler": "leio lês lê lemos ledes leem",
    "fazer": "faço fazes faz fazemos fazeis fazem", "dizer": "digo dizes diz dizemos dizeis dizem",
    "trazer": "trago trazes traz trazemos trazeis trazem", "querer": "quero queres quer queremos quereis querem",
    "poder": "posso podes pode podemos podeis podem", "pôr": "ponho pões põe pomos pondes põem",
    "haver": "hei hás há havemos haveis hão", "saber": "sei sabes sabe sabemos sabeis sabem",
    "ouvir": "ouço ouves ouve ouvimos ouvis ouvem", "pedir": "peço pedes pede pedimos pedis pedem",
    "perder": "perco perdes perde perdemos perdeis perdem", "subir": "subo sobes sobe subimos subis sobem",
    "fugir": "fujo foges foge fugimos fugis fogem", "dormir": "durmo dormes dorme dormimos dormis dormem",
    "servir": "sirvo serves serve servimos servis servem", "seguir": "sigo segues segue seguimos seguis seguem",
    "sentir": "sinto sentes sente sentimos sentis sentem", "mentir": "minto mentes mente mentimos mentis mentem",
    "ferir": "firo feres fere ferimos feris ferem", "vestir": "visto vestes veste vestimos vestis vestem",
    "valer": "valho vales vale valemos valeis valem", "medir": "meço medes mede medimos medis medem",
    "odiar": "odeio odeias odeia odiamos odiais odeiam",
}
# imperfeito irregular
IMPERF = {"ser": "era eras era éramos éreis eram", "ter": "tinha tinhas tinha tínhamos tínheis tinham",
          "vir": "vinha vinhas vinha vínhamos vínheis vinham", "pôr": "punha punhas punha púnhamos púnheis punham"}
# raiz do futuro e do condicional
FUTURO = {"fazer": "far", "dizer": "dir", "trazer": "trar", "pôr": "por"}
# presente do subjuntivo irregular (todas as pessoas)
SUBJ = {"ser": "seja sejas seja sejamos sejais sejam", "estar": "esteja estejas esteja estejamos estejais estejam",
        "ir": "vá vás vá vamos vades vão", "dar": "dê dês dê demos deis deem", "saber": "saiba saibas saiba saibamos saibais saibam",
        "querer": "queira queiras queira queiramos queirais queiram", "haver": "haja hajas haja hajamos hajais hajam"}
# derivados que se conjugam como a base
BASE = {"desfazer": "fazer", "refazer": "fazer", "satisfazer": "fazer", "contradizer": "dizer", "predizer": "dizer",
        "bendizer": "dizer", "maldizer": "dizer", "manter": "ter", "deter": "ter", "reter": "ter", "conter": "ter",
        "obter": "ter", "entreter": "ter", "suster": "ter", "compor": "pôr", "propor": "pôr", "dispor": "pôr", "expor": "pôr",
        "depor": "pôr", "impor": "pôr", "opor": "pôr", "repor": "pôr", "supor": "pôr", "transpor": "pôr", "convir": "vir",
        "intervir": "vir", "sobrevir": "vir", "rever": "ver", "prever": "ver", "antever": "ver", "desdizer": "dizer"}
PARTICIPIO = {"feito": "fazer", "dito": "dizer", "visto": "ver", "posto": "pôr", "escrito": "escrever", "aberto": "abrir",
              "coberto": "cobrir", "descoberto": "descobrir", "vindo": "vir", "morto": "morrer", "ganho": "ganhar",
              "gasto": "gastar", "pago": "pagar", "aceito": "aceitar", "entregue": "entregar", "preso": "prender",
              "eleito": "eleger", "desfeito": "desfazer", "satisfeito": "satisfazer", "bendito": "bendizer",
              "maldito": "maldizer", "predito": "predizer", "proposto": "propor", "disposto": "dispor", "exposto": "expor",
              "imposto": "impor", "deposto": "depor", "previsto": "prever", "revisto": "rever", "acendido": "acender",
              "sido": "ser", "ido": "ir", "tido": "ter", "estado": "estar", "havido": "haver", "dado": "dar"}


def _base(inf):
    b = BASE.get(inf)
    return (b, inf[:len(inf) - len(b.replace("ô", "o"))]) if b else (inf, "")


def _tabela(t, inf):
    b, pre = _base(inf)
    if b not in t:
        return None
    formas = t[b].split()
    if pre:   # "propor": propus, propôs; "manter", "convir": mantém, convém
        formas = [pre + {"tem": "tém", "tens": "téns", "vem": "vém", "vens": "véns"}.get(f, f) for f in formas]
    return formas


def _classe(inf):
    return "ir" if inf.endswith(("ir", "ír")) else "er" if inf.endswith("er") else "ar" if inf.endswith("ar") else "or"


def _antes_e(raiz):
    """raiz para terminação começada por e: fic -> fiqu, cheg -> chegu, começ -> comec"""
    return re.sub(r"c$", "qu", re.sub(r"g$", "gu", re.sub(r"ç$", "c", raiz)))


def preterito(inf):
    t = _tabela(PRET, inf)
    if t:
        return t
    r, c = inf[:-2], _classe(inf)
    if c == "ar":
        return [_antes_e(r) + "ei", r + "aste", r + "ou", r + "amos", r + "astes", r + "aram"]
    if c == "er":
        return [r + "i", r + "este", r + "eu", r + "emos", r + "estes", r + "eram"]
    if c == "ir":
        if r.endswith(("a", "u")) and not r.endswith(("gu", "qu")):         # sair, cair, destruir: saí, saíste, saiu
            return [r + "í", r + "íste", r + "iu", r + "ímos", r + "ístes", r + "íram"]
        return [r + "i", r + "iste", r + "iu", r + "imos", r + "istes", r + "iram"]
    return None


def presente(inf):
    t = _tabela(PRES, inf)
    if t:
        return t
    r, c = inf[:-2], _classe(inf)
    if c == "ar":
        return [r + "o", r + "as", r + "a", r + "amos", r + "ais", r + "am"]
    if c == "er":
        return [re.sub(r"c$", "ç", re.sub(r"g$", "j", r)) + "o", r + "es", r + "e", r + "emos", r + "eis", r + "em"]
    if c == "ir":
        if r.endswith(("a", "u")) and not r.endswith(("gu", "qu")):         # sair: saio, sais, sai, saímos, saís, saem
            return [r + "o", r + "is", r + "i", r + "ímos", r + "ís", r + "em"]
        return [re.sub(r"g$", "j", r) + "o", r + "es", r + "e", r + "imos", r + "is", r + "em"]
    return None


def imperfeito(inf):
    t = _tabela(IMPERF, inf)
    if t:
        return t
    r, c = inf[:-2], _classe(inf)
    if c == "ar":
        return [r + "ava", r + "avas", r + "ava", r + "ávamos", r + "áveis", r + "avam"]
    if c in ("er", "ir"):
        i = "í" if c == "ir" and r.endswith(("a", "u")) and not r.endswith(("gu", "qu")) else "i"
        return [r + i + "a", r + i + "as", r + i + "a", r + "íamos", r + "íeis", r + i + "am"]
    return None


def _raiz_futuro(inf):
    b, pre = _base(inf)
    if b in FUTURO:
        return pre + FUTURO[b]
    return inf.replace("ô", "o")


def futuro(inf):
    r = _raiz_futuro(inf)
    return [r + "ei", r + "ás", r + "á", r + "emos", r + "eis", r + "ão"]


def condicional(inf):
    r = _raiz_futuro(inf)
    return [r + "ia", r + "ias", r + "ia", r + "íamos", r + "íeis", r + "iam"]


def subjuntivo(inf):
    t = _tabela(SUBJ, inf)
    if t:
        return t
    pres = presente(inf)
    if not pres or not pres[0].endswith("o"):
        return None
    r, c = pres[0][:-1], _classe(_base(inf)[0])
    if c == "ar":
        r = _antes_e(r)
        return [r + "e", r + "es", r + "e", r + "emos", r + "eis", r + "em"]
    return [r + "a", r + "as", r + "a", r + "amos", r + "ais", r + "am"]


def imperativo(inf, pessoa):
    """"tomar", "2S" -> "toma"; "2P" -> "tomai" (ser: sê, sede; ir: vai, ide)"""
    esp = {"ser": ("sê", "sede"), "ir": ("vai", "ide"), "estar": ("está", "estai"), "ter": ("tem", "tende"),
           "vir": ("vem", "vinde"), "pôr": ("põe", "ponde"), "dizer": ("dize", "dizei"), "fazer": ("faze", "fazei"),
           "trazer": ("traze", "trazei")}
    if inf in esp:
        return esp[inf][0 if pessoa == "2S" else 1]
    pres = presente(inf)
    if not pres:
        return None
    return pres[2] if pessoa == "2S" else pres[4][:-1]


def participio(inf):
    for p, i in PARTICIPIO.items():
        if i == inf:
            return p
    c = _classe(inf)
    return inf[:-2] + ("ado" if c == "ar" else "ido") if c != "or" else None


TEMPOS = {"pret": preterito, "pres": presente, "imperf": imperfeito, "fut": futuro, "cond": condicional, "subj": subjuntivo}


# verbo fora da lista: só terminações que não deixam dúvida (futuro, imperfeito, condicional, pretérito regular)
TERMINACOES = [("rá", "3S", {"2S": "rás", "2P": "reis"}), ("rão", "3P", {"2P": "reis", "2S": "rás"}),
               ("ava", "3S", {"2S": "avas", "2P": "áveis"}), ("avam", "3P", {"2P": "áveis", "2S": "avas"}),
               ("ria", "3S", {"2S": "rias", "2P": "ríeis"}), ("riam", "3P", {"2P": "ríeis", "2S": "rias"}),
               ("ou", "3S", {"2S": "aste", "2P": "astes"}), ("aram", "3P", {"2P": "astes", "2S": "aste"}),
               ("iu", "3S", {"2S": "iste", "2P": "istes"}), ("iram", "3P", {"2P": "istes", "2S": "iste"})]


def _por_terminacao(forma, de, para):
    for fim, pessoa, troca in TERMINACOES:
        if de == pessoa and forma.endswith(fim) and len(forma) > len(fim) + 2:
            return forma[:-len(fim)] + troca[para]
    return None


def infinitivos(palavras):
    """Os infinitivos de uma lista de palavras (texto da Bíblia Livre): os que aparecem também conjugados
    (gerúndio, particípio ou pretérito), para não tomar "lugar" ou "mulher" por verbo."""
    pal = set(palavras)
    saida = set()
    for w in pal:
        c = _classe(w)
        if c == "or" or len(w) < 4 or not re.fullmatch(r"[a-zà-ú]+", w):
            continue
        r = w[:-2]
        if {r + ("ando" if c == "ar" else "endo" if c == "er" else "indo"), participio(w), (preterito(w) or [""] * 3)[2]} & pal:
            saida.add(w)
    return saida


class Verbos:
    """Índice forma -> conjugações possíveis, para uma lista de infinitivos."""

    def __init__(self, infinitivos):
        self.formas, self.part = {}, {}
        self.infs = set(infinitivos) | set(PRET) | set(PRES) | set(BASE)
        for inf in sorted(self.infs):
            for tempo, f in TEMPOS.items():
                fs = f(inf)
                if not fs:
                    continue
                for pessoa, forma in zip(P, fs):
                    self.formas.setdefault(forma, set()).add((inf, tempo, pessoa))
            pa = participio(inf)
            if pa:
                self.part.setdefault(pa, set()).add(inf)

    def trocar_pessoa(self, forma, de, para):
        """"fará" 3S -> "farás" 2S. Forma de dois tempos ("vão": presente ou subjuntivo de "ir") vale pelo primeiro
        de TEMPOS; None se não reconhece ou se dois verbos dão resultados diferentes no mesmo tempo."""
        por_tempo = {}
        for inf, tempo, pessoa in self.formas.get(forma, ()):
            if pessoa == de:
                por_tempo.setdefault(tempo, set()).add(TEMPOS[tempo](inf)[P.index(para)])
        for tempo in TEMPOS:
            if tempo in por_tempo:
                s = por_tempo[tempo]
                return s.pop() if len(s) == 1 else None
        return _por_terminacao(forma, de, para)

    def preterito_de(self, part, pessoa):
        """"falado", "3S" -> "falou"."""
        infs = self.part.get(part, set())
        saidas = {preterito(i)[P.index(pessoa)] for i in infs if preterito(i)}
        return saidas.pop() if len(saidas) == 1 else None

    def futuro_de(self, inf, pessoa):
        """"fazer", "2S" -> "farás" (o futuro só é irregular em fazer, dizer, trazer e pôr, que estão nas tabelas)."""
        return futuro(inf)[P.index(pessoa)] if re.fullmatch(r"[a-zà-ú]+(?:ar|er|ir|or|ôr)", inf) else None
