"""Nome próprio em português, na grafia da Bíblia Livre, para cada número de Strong de nome (pessoa ou lugar).

Como acha: para o Strong de "Elijah", junta todos os versículos em que a palavra aparece e conta, em cada um,
as palavras com maiúscula do texto da Bíblia Livre ("Elias", "Acabe", "SENHOR"...). O nome certo é o que
aparece em (quase) todos esses versículos; empate e nome raro se resolvem pela semelhança com o inglês
("Shechem" ~ "Siquém"). Palavra com maiúscula no começo da frase só conta se não for palavra comum ("Então").

Grava ferramentas/nomes_pt.json: {strong: [nome em inglês, nome em português]}, só com os confiáveis e os de
MANUAL. Usado por corrigir_glosas.py (glosas do interlinear) e gerar_atlas_pt.py (nomes do atlas).
uso:  python3 ferramentas/nomes_pt.py              (--relatorio mostra os duvidosos, que ficam de fora)"""
import collections, difflib, json, re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stepbible import DATA, RAIZ, alinhar, nome_proprio   # noqa: E402

SAIDA = RAIZ / "ferramentas" / "nomes_pt.json"
TOKEN = re.compile(r"[A-ZÀ-Ý][a-zà-ÿ]+(?:-[A-ZÀ-Ýa-zà-ÿ]+)*|[A-ZÀ-Ý]{2,}")
INICIO = re.compile(r"(?:^|[.;:!?]\s+|[\"“(]\s*)$")

# Conferidos à mão: os que a contagem errou ou deixou em dúvida. "" = deixar como está (não é nome a trocar).
MANUAL = {
    "H3069": "DEUS",   # Adonai YHWH: a Bíblia Livre escreve "Senhor DEUS"
    "H758": "Arã", "H763": "Arã", "H7157": "Quiriate-Jearim", "H3088": "Jeorão", "H3141": "Jorão",
    "H5018": "Nebuzaradã", "H3778": "caldeus", "H2975": "", "H5104": "", "H6160": "Arabá", "H4713": "",
    "H5045": "Neguebe", "H3050": "JAH", "H62": "Abel", "H883": "Beer", "H7025": "Quir", "H3645": "Camos",
    "H3810": "Lo-Debar", "H3573": "Cusã-Risataim", "H5297": "Mênfis", "H3412": "Jarmute", "H6429": "Filístia",
    "H7497": "Rafa", "H7526": "Rezim", "H1121": "",
}


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def _chave(s, trocas):
    s = sem_acento(s.lower())
    for a, b in trocas:
        s = s.replace(a, b)
    s = re.sub(r"[^a-z]", "", s.replace("h", ""))
    return re.sub(r"(.)\1+", r"\1", s)


def semelhanca(en, pt):
    """0 a ~1,1: as grafias inglesa e portuguesa de um nome bíblico ("Hezekiah" ~ "Ezequias")."""
    a = _chave(en, [("sh", "s"), ("ch", "c"), ("ph", "f"), ("th", "t"), ("kh", "c"), ("ck", "c"), ("k", "c"),
                    ("qu", "c"), ("q", "c"), ("y", "i"), ("w", "v"), ("z", "s"), ("ee", "i"), ("oo", "u")])
    b = _chave(pt, [("qu", "c"), ("gu", "g"), ("ç", "s"), ("lh", "l"), ("nh", "n"), ("ch", "c"), ("k", "c"),
                    ("y", "i"), ("z", "s"), ("w", "v")])
    b = re.sub(r"(?<=[^aeiou])e$", "", b)          # Acabe, Calebe: o -e final do português
    return difflib.SequenceMatcher(None, a, b).ratio() + (0.1 if a[:1] == b[:1] else 0)


def textos_blivre():
    textos, minusc = {}, collections.Counter()
    for arq in (DATA / "bibles" / "blivre").glob("*.json"):
        for c, caps in enumerate(json.loads(arq.read_text(encoding="utf-8")), 1):
            for v, t in enumerate(caps, 1):
                textos[(arq.stem, c, v)] = t
                minusc.update(re.findall(r"\b[a-zà-ÿ]+\b", t))
    return textos, minusc


def candidatos(texto, minusc):
    saida = set()
    for m in TOKEN.finditer(texto):
        w = m.group(0)
        if not (w.isupper() and len(w) > 1) and INICIO.search(texto[:m.start()]) and minusc[w.lower()] >= 3:
            continue   # palavra comum no começo da frase
        saida.add(w)
    return saida


FUNCAO = re.compile(r"^(?:(?:O|The|And|To|Of|In|By|For|From|With|At|On|As|Like|Unto|Upon|Into|Against|Before|After|"
                    r"Toward|Towards|Behold|Then|But|So|Is|Are|Was|Were|Am)\s+)+")


def nome_ingles(glosa):
    """O nome dentro da glosa inglesa: "O Yahweh" -> "Yahweh", "and  Benaiah" -> "Benaiah"."""
    m = re.findall(r"[A-Z][\w'’-]*(?:[ -][A-Z][\w'’-]*)*", glosa)
    return FUNCAO.sub("", max(m, key=len)) if m else ""


def escolher(en, versos, cand):
    """(nome, fração dos versículos em que aparece, semelhança, margem para o segundo)"""
    n = len(versos)
    df = collections.Counter(c for v in versos for c in cand.get(v, ()))
    if not df:
        return None
    pont = {c: df[c] / n + 0.35 * semelhanca(en, c) for c in df}
    ordem = sorted(pont, key=pont.get, reverse=True)
    seg = pont[ordem[1]] if len(ordem) > 1 else 0
    return ordem[0], df[ordem[0]] / n, semelhanca(en, ordem[0]), pont[ordem[0]] - seg


GENTILICO = re.compile(r"(?:ites|ians|eans)$|^Medes$")   # "Persians", "Medes": em português é minúscula e plural


def confiavel(en, df, sim, margem, n):
    if GENTILICO.search(en):
        return False
    if n >= 3 and df >= 0.6 and margem >= 0.1:
        return True
    if n >= 2 and df >= 0.5 and sim >= 0.85 and margem > 0:
        return True
    return df == 1 and sim >= 0.75 and margem >= 0.1


def main():
    textos, minusc = textos_blivre()
    cand = {k: candidatos(t, minusc) for k, t in textos.items()}
    _, palavras = alinhar()
    por_strong = collections.defaultdict(lambda: [set(), collections.Counter(), 0])
    for w, _ in palavras:
        if w.strong and nome_proprio(w.gram) and nome_ingles(w.en):
            s = por_strong[w.strong]
            s[0].add((w.livro, w.cap, w.v)); s[1][nome_ingles(w.en)] += 1; s[2] += 1
    mapa, duvidosos, aceitos_pela_contagem = {}, [], []
    for strong, (versos, ens, n_pal) in por_strong.items():
        en = ens.most_common(1)[0][0]
        if strong in MANUAL:
            if MANUAL[strong]:
                mapa[strong] = [en, MANUAL[strong]]
            continue
        r = escolher(en, versos, cand)
        if not r:
            continue
        pt, df, sim, margem = r
        if confiavel(en, df, sim, margem, len(versos)):
            mapa[strong] = [en, pt]
            if sim < 0.6:
                aceitos_pela_contagem.append((n_pal, strong, en, pt, df, sim, margem))
        else:
            duvidosos.append((n_pal, strong, en, pt, df, sim, margem))
    SAIDA.write_text(json.dumps(dict(sorted(mapa.items())), ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"{len(mapa)} nomes gravados em {SAIDA.relative_to(RAIZ)}; {len(duvidosos)} duvidosos ficaram de fora "
          f"({sum(d[0] for d in duvidosos)} palavras)")
    if "--relatorio" in sys.argv:
        print("\naceitos pela contagem, com grafia pouco parecida (conferir):")
        for n, strong, en, pt, df, sim, margem in sorted(aceitos_pela_contagem, reverse=True):
            print(f"{n:5} {strong:7} {en:22} -> {pt:20} df={df:.2f} sim={sim:.2f} margem={margem:.2f}")
        print("\nduvidosos (ficaram de fora):")
        for n, strong, en, pt, df, sim, margem in sorted(duvidosos, reverse=True):
            print(f"{n:5} {strong:7} {en:22} -> {pt:20} df={df:.2f} sim={sim:.2f} margem={margem:.2f}")


if __name__ == "__main__":
    main()
