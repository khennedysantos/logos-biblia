"""Nome em português, na grafia da Bíblia Livre, de cada lugar do atlas (campo "p" de data/places.json).

O atlas (openbible.info) só traz o nome em inglês e os versículos de cada lugar. Para o nome português:
- nome simples ("Beth-shemesh", "Ai 2"): o Strong da palavra hebraica/grega desse lugar nos seus versículos
  (stepbible.py) e o nome desse Strong na Bíblia Livre (nomes_pt.json); sem Strong, a palavra com maiúscula que
  mais aparece nos versículos do lugar e mais se parece com o nome inglês (nomes_pt.escolher);
- com termo geográfico ("Mount of Olives", "Valley of Hinnom", "Fish Gate"): a expressão como aparece no texto
  ("monte das Oliveiras", "vale de Hinom", "porta do Peixe"), com a primeira letra maiúscula.
O número de lugares homônimos ("Ai 2") é mantido. O que não se acha com segurança fica sem "p" (o app mostra o
nome inglês) — ou vai para MANUAL.
uso:  python3 ferramentas/gerar_atlas_pt.py [--conferir]   (mostra o que mudou em relação ao arquivo atual)"""
import collections, json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stepbible import DATA, alinhar, nome_proprio                                       # noqa: E402
from nomes_pt import candidatos, confiavel, escolher, nome_ingles, semelhanca, textos_blivre   # noqa: E402

LUGARES = DATA / "places.json"
GENERICO = {   # termo inglês -> palavras do texto em português
    "Valley": ("vale",), "Mount": ("monte",), "Mountain": ("monte",), "Mountains": ("montes", "monte"),
    "Gate": ("porta",), "Sea": ("mar",), "Tower": ("torre",), "River": ("rio",), "Brook": ("ribeiro", "torrente"),
    "City": ("cidade",), "Pool": ("tanque", "açude"), "Well": ("poço",), "Wall": ("muro",), "Field": ("campo",),
    "Spring": ("fonte",), "Plain": ("planície", "campina"), "Plains": ("planícies", "campinas"), "Hill": ("outeiro", "colina"),
    "Island": ("ilha",), "Wilderness": ("deserto",), "Desert": ("deserto",), "Cave": ("caverna", "cova"),
    "Rock": ("rocha", "penha"), "Forest": ("bosque",), "House": ("casa",), "Ascent": ("subida",), "Way": ("caminho",),
}
# lugares que não são um nome próprio da Bíblia Livre (portas, salas, construções) ou que a busca erra
MANUAL = {
    "Dead Sea": "Mar Morto", "Mediterranean Sea": "Mar Mediterrâneo", "Great Sea": "Mar Grande",
    "Beyond the River": "Além do Rio", "Areopagus": "Areópago", "Chaldea": "Caldeia", "Caesarea Philippi": "Cesareia de Filipe",
    "Mount Moriah": "Monte Moriá", "Horse Gate": "Porta dos Cavalos", "Corner Gate": "Porta da Esquina",
    "East Gate": "Porta Oriental", "City of Palms": "Cidade das Palmeiras", "Beautiful Gate": "Porta Formosa",
    "Broad Wall": "Muro Largo", "Brook of the Willows": "Ribeiro dos Salgueiros", "Diviners’ Oak": "Carvalho dos Adivinhos",
    "Dragon Spring": "Fonte do Dragão", "Fair Havens": "Bons Portos", "Forum of Appius": "Praça de Ápio",
    "Gate of the Guard": "Porta da Guarda", "Hall of Judgment": "Sala do Julgamento", "Hall of Pillars": "Sala das Colunas",
    "Hall of the Throne": "Sala do Trono", "Herod’s palace": "Palácio de Herodes", "Holy Place": "Lugar Santo",
    "Most Holy Place": "Santo dos Santos", "King’s Highway": "Estrada Real", "King’s Valley": "Vale do Rei",
    "Lower Pool": "Tanque de Baixo", "Upper Pool": "Tanque de Cima", "Gate of Yeshanah": "Porta Velha",
    "House of the Forest of Lebanon": "Casa do Bosque do Líbano", "Jordan Valley": "Vale do Jordão", "East": "Oriente",
    "East Square": "Praça Oriental", "Middle Gate": "Porta do Meio", "Gate of the Foundation": "Porta do Fundamento",
    "Angle": "Esquina", "Ethiopia": "Etiópia", "Heliopolis": "Heliópolis", "Adramyttium": "Adramítio",
    "Muster Gate": "Porta da Inspeção", "Sheep Gate": "Porta das Ovelhas", "Water Gate": "Porta das Águas",
    "Valley Gate": "Porta do Vale", "Fish Gate": "Porta do Peixe", "Dung Gate": "Porta do Esterco",
    "Fountain Gate": "Porta da Fonte", "Old Gate": "Porta Velha", "Prison Gate": "Porta da Prisão",
    "Gate of Ephraim": "Porta de Efraim", "Gate of Benjamin": "Porta de Benjamim", "Potsherd Gate": "Porta do Oleiro",
    "Tower of the Hundred": "Torre dos Cem", "Tower of Hananel": "Torre de Hananel", "Tower of the Ovens": "Torre dos Fornos",
    "Tower of Siloam": "Torre de Siloé", "Pool of Siloam": "Tanque de Siloé", "Salt Sea": "Mar Salgado",
    "Red Sea": "Mar Vermelho", "Sea of Galilee": "Mar da Galileia", "Mount of Olives": "Monte das Oliveiras",
    "Solomon’s Portico": "Pórtico de Salomão", "North Gate": "Porta do Norte", "South Gate": "Porta do Sul",
    "West Gate": "Porta do Ocidente", "People’s Gate": "Porta do Povo", "Old Pool": "Tanque Velho", "Thebes": "Nô (Tebas)",
    "Asshur": "Assur", "Beer-lahai-roi": "Beer-Laai-Roi", "Ramoth-gilead": "Ramote-Gileade",
    "Abel-beth-maacah": "Abel-Bete-Maaca", "Shephelah": "Sefelá", "Merom": "Merom", "Aenon": "Enom", "Tema": "Temá",
    "Ezem": "Ezém", "Mattanah": "Matana", "Salecah": "Salcá", "Jeshimon": "Jesimom", "Suph": "Sufe", "Zela": "Zela",
    "Magdala": "Magdala", "Gadara": "Gadara", "Gerasa": "Gerasa", "Gergesa": "Gergesa", "Lydia": "Lídia",
    "Lycia": "Lícia", "Rhodes": "Rodes", "Sparta": "Esparta", "Carthage": "Cartago", "Scythia": "Cítia",
    "Etruria": "Etrúria", "Tartessos": "Tartesso", "Goiim": "Goim", "Ur": "Ur", "Sela": "Selá", "Arbela": "Arbela",
    # nov/2026: os 95 que faltavam. Com versículo: a grafia da Bíblia Livre quando o nome aparece nela; quando ela
    # traduz o nome ("casa de tosa", "monte dos prepúcios"), a forma transliterada usual ou a expressão do texto
    "Allon": "Alom", "Amaw": "Amave", "Aphik": "Afeque", "Aroer": "Aroer", "Atroth-beth-joab": "Atarote-Bete-Joabe",
    "Baale-judah": "Baal de Judá", "Beth-eked": "Bete-Equede", "Beth-haggan": "Bete-Hagã", "Beth-haram": "Bete-Harã",
    "Bor-ashan": "Corasã", "Caleb Ephrathah": "Calebe de Efrata", "Eglath-shelishiyah": "Eglate-Selisia",
    "Elkosh": "Elcós", "Enaim": "Enaim", "Enam": "Enã", "Ephron": "Efrom", "Gamad": "Gamade", "Gederah": "Gederá",
    "Ge-harashim": "Vale dos Artesãos", "Gibeath-elohim": "Morro de Deus", "Gibeath-haaraloth": "Monte dos Prepúcios",
    "Gulloth-mayim": "Fontes de Águas", "Hakkephirim": "Quefirim", "Hamath-zobah": "Hamate de Zobá", "Harod": "Harode",
    "Hazar-susah": "Hazar-Susa", "Hazer-hatticon": "Hazer-Haticom", "Helech": "Heleque", "Ir-nahash": "Ir-Naás",
    "Kartah": "Cartá", "Kue": "Coa", "Lehem": "Leém", "Maareh-geba": "Prado de Gibeá", "Mahalab": "Maalabe",
    "Mahaneh-dan": "Maané-Dã", "Meronoth": "Meronote", "Mortar": "Mactés", "Parbar": "Parbar", "Pau": "Paú",
    "Sahar": "Saar", "Secu": "Socó", "Shaalim": "Saalim", "Shalishah": "Salisa", "Shen": "Sem", "Syrtis": "Sirte",
    "Tabbur-erez": "Tabur-Erez", "Uzzen-sheerah": "Uzém-Seerá", "Zaphon": "Zafom",
    # sem versículo (lugares da história e da arqueologia ao redor da Bíblia): a forma usual em português
    "Abila": "Ábila", "Abila Lysaniou": "Ábila de Lisânias", "Adasa": "Adasa", "Adulis": "Ádulis", "Ama": "Ama",
    "Amate": "Amate", "Arsinoe": "Arsínoe", "Batanea": "Bataneia", "Belamon": "Belamom", "Bether": "Beter",
    "Chalcis": "Cálcis", "Charmande": "Carmande", "Eridu": "Eridu", "Gath-padalla": "Gate-Padala", "Gutium": "Gútio",
    "Halahha": "Halaha", "Harhar": "Harhar", "Hatti": "Hati", "Heracleopolis Magna": "Heracleópolis Magna",
    "Heracleopolis Parva": "Heracleópolis Parva", "Hilakku": "Hilaku", "Janua": "Janua", "Kumidi": "Kumidi",
    "Laash": "Laash", "Madiama": "Madiama", "Magdalsenna": "Magdalsena", "Magdolum": "Magdolo", "Nahuru": "Nahuru",
    "Nuhashe": "Nuhaxe", "Pitru": "Pitru", "Punt": "Punt", "Ragmat": "Ragmate", "Salona": "Salona", "Saparda": "Saparda",
    "Saparre": "Sapare", "Sutu": "Sutu", "Tegarama": "Tegarama", "Thapsacus": "Tápsaco", "Thelme": "Telme",
    "Tjaru": "Tjaru", "Umman Manda": "Umman-Manda", "Upu": "Upu", "Uqnu": "Uqnu", "Ura": "Ura",
}
QUALIFICA = {"Lower": "de Baixo", "Upper": "de Cima"}
FRASE = r"\b((?i:{g}))\s+((?:(?:de|do|da|dos|das)\s+)?[A-ZÀ-Ý][\wÀ-ÿ'-]*(?:\s+[A-ZÀ-Ý][\wÀ-ÿ'-]*)?)"


def frase_no_texto(en, gen, refs, textos):
    """"monte das Oliveiras": a expressão com o termo geográfico que mais aparece nos versículos do lugar."""
    especifico = " ".join(w for w in en.split() if w not in GENERICO and w not in ("of", "the", "The"))
    padrao = re.compile(FRASE.format(g="|".join(GENERICO[gen])))
    conta = collections.Counter()
    for r in refs:
        for m in padrao.finditer(textos.get(tuple(r), "")):
            conta[(m.group(1).lower(), m.group(2))] += 1
    if not conta:
        return None
    def pontos(item):
        (g, nome), n = item
        return n + (2 * semelhanca(especifico, nome.split()[-1]) if especifico else 0)
    (g, nome), n = max(sorted(conta.items()), key=pontos)
    if especifico and semelhanca(especifico, nome.split()[-1]) < 0.5 and n < 2:
        return None
    nome = re.sub(r"^de (?=[A-ZÀ-Ý])", "", nome) if g.startswith("monte") else nome   # "monte de Sinai": Monte Sinai
    return g[0].upper() + g[1:] + " " + nome


RUIM = re.compile(r"Cerveja|Portão|Salão|Loucos|Primavera|Brook|Pool|Havens|Aqui está|Porque|Mais-sete|Leste|!|\"|"
                  r"\bof\b|\bthe\b|Upper|Lower|Mais Baixo")


def limpo(nome):
    return not RUIM.search(nome)


def main():
    lugares = json.loads(LUGARES.read_text(encoding="utf-8"))
    mapa = json.loads((Path(__file__).resolve().parent / "nomes_pt.json").read_text(encoding="utf-8"))
    textos, minusc = textos_blivre()
    cand = {k: candidatos(t, minusc) for k, t in textos.items()}
    _, palavras = alinhar()
    por_verso = collections.defaultdict(list)
    for w, _ in palavras:
        if w.strong and nome_proprio(w.gram):
            por_verso[(w.livro, w.cap, w.v)].append(w)
    mudou, sem, novos = [], 0, 0
    for lug in lugares:
        m = re.match(r"^(.*?)(?: (\d+))?$", lug["n"])
        en, num = m.group(1), m.group(2)
        refs = [tuple(r) for r in lug.get("r", [])]
        pt = MANUAL.get(en)
        qualif = en.split()[0] if en.split()[0] in QUALIFICA else None
        base = en.split(" ", 1)[1] if qualif else en
        gen = None if pt else next((w for w in base.split() if w in GENERICO), None)
        if not pt and gen:
            pt = frase_no_texto(en, gen, refs, textos)
        if not pt and not gen:
            fortes, parecido = collections.Counter(), {}
            for r in refs:
                for w in por_verso.get(r, ()):
                    s = semelhanca(base, nome_ingles(w.en)) if nome_ingles(w.en) else 0
                    if s >= 0.8:
                        fortes[w.strong] += 1
                        parecido[w.strong] = max(parecido.get(w.strong, 0), s)
            melhor = max(sorted(fortes), key=lambda k: (parecido[k], fortes[k]), default=None)   # "Dalmatia" não é "Galatia"
            if melhor in mapa:
                pt = mapa[melhor][1]
                if refs and not any(pt in textos.get(r, "") for r in refs):
                    r = escolher(base, set(refs), cand)            # o nome do Strong não está nos versículos do
                    if r and r[2] >= 0.8:                           # lugar: vale a grafia deles ("Adã", não "Adão")
                        pt = r[0]
            elif refs:
                r = escolher(base, set(refs), cand)
                if r and confiavel(base, r[1], r[2], r[3], len(refs)):
                    pt = r[0]
            if pt and qualif:
                pt = f"{pt} {QUALIFICA[qualif]}"                   # "Lower Beth-horon": Bete-Horom de Baixo
        if not pt and lug.get("p") and limpo(lug["p"]):
            pt = re.sub(r" \d+$", "", lug["p"])                     # não achou: fica o nome que já existia
        if pt and num:
            pt = f"{pt} {num}"
        if pt != lug.get("p"):
            mudou.append((lug["n"], lug.get("p"), pt))
            novos += not lug.get("p")
        if pt:
            lug["p"] = pt
        else:
            lug.pop("p", None)
            sem += 1
    print(f"{len(lugares) - sem} de {len(lugares)} lugares com nome em português; {len(mudou)} mudaram ({novos} novos)")
    if "--conferir" in sys.argv:
        for n, antes, depois in mudou:
            if antes:
                print(f"   {n:28} {antes!r:28} -> {depois!r}")
    else:
        LUGARES.write_text(json.dumps(lugares, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
