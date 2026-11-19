"""Nome em espanhol de cada lugar do atlas (campo "e" de data/places.json), para a interface em espanhol.

Não há uma Bíblia espanhola moderna em domínio público alinhada palavra por palavra (a Reina-Valera Antigua do site
usa grafias de 1602, como "Achâb" e "Naboth"), então o nome sai do português (campo "p", na grafia da Bíblia Livre)
por regras de correspondência entre as duas grafias ("Hebrom" -> "Hebrón", "Belém" -> "Belén", "Moabe" -> "Moab",
"Vale de Jezreel" -> "Valle de Jezreel"), mais a lista MANUAL com a forma usual em espanhol dos nomes que as regras
não acertam ("Gileade" -> "Galaad", "Egito" -> "Egipto"), sobretudo os mais citados, que são os que aparecem no mapa.
Em inglês o app usa o nome do próprio openbible.info (campo "n").
uso:  python3 ferramentas/gerar_atlas_es.py [--conferir]   (--conferir lista os 300 mais citados com o resultado)"""
import json, re, sys, unicodedata
from pathlib import Path

LUGARES = Path(__file__).resolve().parent.parent / "data" / "places.json"
MANUAL = {
    "Jerusalém": "Jerusalén", "Egito": "Egipto", "Sião": "Sion", "Monte Sião": "Monte Sion", "Canaã": "Canaán",
    "Gileade": "Galaad", "Jabes-Gileade": "Jabes de Galaad", "Ramote-Gileade": "Ramot de Galaad", "Midiã": "Madián",
    "Neguebe": "Neguev", "Gibeá": "Gabaa", "Gibeão": "Gabaón", "Siló": "Silo", "Mispá": "Mizpa", "Dã": "Dan",
    "Filístia": "Filistea", "Mar Salgado": "Mar Salado", "Mar Salgado (Morto)": "Mar Salado (Muerto)", "Elão": "Elam",
    "Susã": "Susa", "Cuxe": "Cus", "Quriate-Jearim": "Quiriat-jearim", "Sefelá": "Sefela", "Cafarnaum": "Capernaum",
    "Bete-Semes": "Bet-semes", "Além do Rio": "Al otro lado del río", "Maanaim": "Mahanaim", "Zobá": "Soba",
    "Ziclague": "Siclag", "Asquelom": "Ascalón", "Harã": "Harán", "Megido": "Meguido", "Arã": "Aram",
    "Padã-Arã": "Padan-aram", "Zorá": "Zora", "Acaia": "Acaya", "Ribeiro do Egito": "Torrente de Egipto", "Jaza": "Jahaza",
    "Quedar": "Cedar", "Suném": "Sunem", "Aijalom": "Ajalón", "Bete-Seã": "Bet-seán", "Maquedá": "Maceda",
    "Parã": "Parán", "Zim": "Zin", "Bete-Horom": "Bet-horón", "Bete-Horom de Baixo": "Bet-horón la de abajo",
    "Bete-Horom de Cima": "Bet-horón la de arriba", "Dedã": "Dedán", "Etiópia": "Etiopía", "Eziom-Geber": "Ezión-geber",
    "Lode": "Lod", "Zoã": "Zoán", "Abel-Bete-Maaca": "Abel-bet-maaca", "Arpade": "Arfad", "Elate": "Elat",
    "En-Gedi": "En-gadi", "Rogel": "En-rogel", "Giom": "Gihón", "Manre": "Mamre", "Pute": "Fut", "Temã": "Temán",
    "Nô (Tebas)": "No (Tebas)", "Trôade": "Troas", "Gozã": "Gozán", "Quisom": "Cisón", "Massá": "Masah",
    "Ramessés": "Ramesés", "Mar Grande": "Mar Grande", "Mar Grande (Mediterrâneo)": "Mar Grande (Mediterráneo)",
    "Monte das Oliveiras": "Monte de los Olivos", "Santo dos Santos": "Lugar Santísimo", "Sul": "Sur", "Oriente": "Oriente",
    "Casa do Bosque do Líbano": "Casa del bosque del Líbano", "Esquina": "Esquina", "Siloé": "Siloé", "Sarom": "Sarón",
    "Hesbom": "Hesbón", "Assíria": "Asiria", "Babilônia": "Babilonia", "Belém": "Belén", "Jope": "Jope", "Gate": "Gat",
    "Cades": "Cades", "Hamate": "Hamat", "Asdode": "Asdod", "Ecrom": "Ecrón", "Anatote": "Anatot", "Tecoa": "Tecoa",
    "Cedrom": "Cedrón", "Éden": "Edén", "Betânia": "Betania", "Gósen": "Gosén", "Sucote": "Sucot", "Adulão": "Adulam",
    "Beerote": "Beerot", "Meribá": "Meriba", "Tofete": "Tofet", "Netofá": "Netofa", "Astarote": "Astarot",
    "Jaboque": "Jaboc", "Nobe": "Nob", "Taanaque": "Taanac", "Hazerote": "Hazerot", "Jarmute": "Jarmut", "Naiote": "Naiot",
    "Admá": "Adma", "Amaleque": "Amalec", "Meseque": "Mesec", "Tafnes": "Tafnes", "Laodiceia": "Laodicea",
    "Caldeia": "Caldea", "Galileia": "Galilea", "Mar da Galileia": "Mar de Galilea", "Judeia": "Judea", "Cesareia": "Cesarea",
    "Cesareia de Filipe": "Cesarea de Filipo", "Bereia": "Berea", "Icônio": "Iconio", "Tessalônica": "Tesalónica",
    "Macedônia": "Macedonia", "Mênfis": "Menfis", "Siquém": "Siquem", "Gomorra": "Gomorra", "Berseba": "Beerseba",
    "Monte Horebe": "Monte Horeb", "Horebe": "Horeb", "Monte Hermom": "Monte Hermón", "Ribla": "Ribla", "Gesur": "Gesur",
    "Hormá": "Horma", "Maressa": "Maresa", "Husá": "Husa", "Moabe": "Moab", "Edom": "Edom", "Amom": "Amón", "Basã": "Basán",
    "Sidom": "Sidón", "Hebrom": "Hebrón", "Nínive": "Nínive", "Sabá": "Sabá", "Rabá": "Rabá", "Arabá": "Arabá",
    "Társis": "Tarsis", "Quir": "Kir", "Pisga": "Pisga", "Sinear": "Sinar", "Chipre": "Chipre", "Creta": "Creta",
    "Grande Mar": "Mar Grande", "Mar Vermelho": "Mar Rojo", "Mar Egeu": "Mar Egeo", "Mar Adriático": "Mar Adriático",
    "Golfo Pérsico": "Golfo Pérsico", "Mar Negro": "Mar Negro", "Mar Cáspio": "Mar Caspio", "Mar Morto": "Mar Muerto",
    "Mar Mediterrâneo": "Mar Mediterráneo", "Porta Formosa": "Puerta la Hermosa", "Bons Portos": "Buenos Puertos",
    "Praça de Ápio": "Foro de Apio", "Areópago": "Areópago", "Jordão": "Jordán", "Vale do Jordão": "Valle del Jordán",
    "Nilo": "Nilo", "Eufrates": "Éufrates", "Edom": "Edom", "Norte": "Norte", "Davi": "David", "Antioquia": "Antioquía",
    "Arnon": "Arnón", "Benjamim": "Benjamín", "Alexandria": "Alejandría", "Sinai": "Sinaí", "Ibleão": "Ibleam", "Etã": "Etam", "Tigre": "Tigris", "Patmos": "Patmos", "Nazaré": "Nazaret", "Jericó": "Jericó",
}
PALAVRAS = {   # termos geográficos e preposições, palavra por palavra
    "Vale": "Valle", "Monte": "Monte", "Montes": "Montes", "Deserto": "Desierto", "Porta": "Puerta", "Ribeiro": "Arroyo",
    "Rio": "Río", "Cidade": "Ciudad", "Tanque": "Estanque", "Poço": "Pozo", "Fonte": "Fuente", "Planície": "Llanura",
    "Planícies": "Llanuras", "Campina": "Llanura", "Outeiro": "Collado", "Ilha": "Isla", "Caverna": "Cueva", "Cova": "Cueva",
    "Rocha": "Peña", "Penha": "Peña", "Torre": "Torre", "Muro": "Muro", "Sala": "Sala", "Casa": "Casa", "Subida": "Cuesta",
    "Caminho": "Camino", "Campo": "Campo", "Mar": "Mar", "Terra": "Tierra", "Palácio": "Palacio", "Carvalho": "Encina",
    "Lugar": "Lugar", "Estrada": "Camino", "Torrente": "Torrente", "da": "de la", "do": "del", "das": "de las",
    "dos": "de los", "de": "de", "e": "y", "Baixo": "Abajo", "Cima": "Arriba", "Velha": "Vieja", "Oriental": "Oriental",
    "Peixe": "Pescado", "Ovelhas": "Ovejas", "Águas": "Aguas", "Cavalos": "Caballos", "Fonte,": "Fuente,",
}


def palavra(w):
    if w in PALAVRAS:
        return PALAVRAS[w]
    s = w.replace("lh", "ll").replace("nh", "ñ").replace("ç", "z").replace("ss", "s")
    s = re.sub(r"ém$", "én", s)
    s = re.sub(r"ão$", "án", s)
    s = re.sub(r"om$", "ón", s)
    s = re.sub(r"eia$", "ea", s)
    s = re.sub(r"que$", "c", s)
    s = re.sub(r"(?<=[aeiouáéíóú])([bdtf])e$", r"\1", s)                  # Moabe -> Moab, Ramote -> Ramot (Derbe fica)
    s = unicodedata.normalize("NFC", unicodedata.normalize("NFD", s).replace("̂", ""))   # ê, ô, â -> e, o, a
    if s.endswith(("ia", "ias")):                                           # Síria, Pérsia: sem acento em espanhol
        s = unicodedata.normalize("NFC", re.sub(r"[́]", "", unicodedata.normalize("NFD", s)))
    s = re.sub(r"ã", "án", s) if s.endswith("ã") else s.replace("ã", "a")
    return s


def espanhol(pt):
    if pt in MANUAL:
        return MANUAL[pt]
    base, num = re.match(r"(.*?)( \d+)?$", pt).groups()
    if base in MANUAL:
        return MANUAL[base] + (num or "")
    partes = []
    for w in base.split(" "):
        if "-" in w and w not in PALAVRAS:                                  # Bete-Semes -> Bet-semes
            a, *resto = [MANUAL.get(x) or palavra(x) for x in w.split("-")]
            a = "Bet" if a == "Bete" else a
            partes.append("-".join([a] + [x[:1].lower() + x[1:] for x in resto]))
        else:
            partes.append(MANUAL.get(w) or palavra(w))
    s = " ".join(partes).replace("de el ", "del ")
    return s + (num or "")


def main():
    lugares = json.loads(LUGARES.read_text(encoding="utf-8"))
    for l in lugares:
        l["e"] = espanhol(l.get("p") or l["n"])
    if "--conferir" in sys.argv:
        vistos = []
        for l in sorted(lugares, key=lambda l: -l["tot"]):
            par = (re.sub(r" \d+$", "", l.get("p") or l["n"]), re.sub(r" \d+$", "", l["e"]))
            if par not in vistos:
                vistos.append(par)
        print(" | ".join(f"{a}→{b}" for a, b in vistos[:300]))
        return
    LUGARES.write_text(json.dumps(lugares, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(lugares)} lugares com nome em espanhol (campo e)")


if __name__ == "__main__":
    main()
