"""Tipo e grau de certeza de cada lugar do Atlas (campos "t" e "c" de data/places.json), tirados dos dados do
openbible.info (Bible Geocoding Data, CC BY 4.0: github.com/openbibleinfo/Bible-Geocoding-Data).

- "t": como o lugar aparece no mapa — "cidade" (ponto), "regiao" (nome espaçado, sem ponto), "monte" (▲), "agua"
  (rios, fontes e mares, em azul) ou "outro" (portas, salas, altares, árvores…: só na busca, não no mapa);
- "c": a certeza da identificação segundo os estudiosos consultados pelo openbible.info (time_total da identificação
  mais aceita, de 0 a 1000; 500 ou mais é alta). Abaixo de 300 o lugar sai do mapa e a ficha avisa "localização incerta".
  Identificação que é só uma área ("a até 100 km de Dumá", 50 km ou mais) também conta como incerta (c = 299).

uso:  python3 ferramentas/atlas_openbible.py
(baixa data/ancient.jsonl do repositório para ferramentas/fontes/openbible/, fora do git, se ainda não estiver lá)"""
import json, re, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LUGARES = RAIZ / "data" / "places.json"
FONTE = RAIZ / "ferramentas" / "fontes" / "openbible" / "ancient.jsonl"
URL = "https://raw.githubusercontent.com/openbibleinfo/Bible-Geocoding-Data/main/data/ancient.jsonl"
TIPOS = {
    "cidade": {"settlement", "campsite", "island", "fortification"},
    "regiao": {"region", "people group", "natural area", "forest", "valley"},
    "monte": {"mountain", "mountain range", "mountain ridge", "hill", "mountain pass", "promontory", "cliff"},
    "agua": {"river", "body of water", "spring", "wadi", "pool", "well", "ford", "canal"},
}


def tipo(tipos):
    if "settlement" in tipos:                      # "Hazor 4" é monte e cidade: no mapa, cidade
        return "cidade"
    for t in tipos:
        for nome, grupo in TIPOS.items():
            if t in grupo:
                return nome
    return "outro"


def main():
    if not FONTE.exists():
        FONTE.parent.mkdir(parents=True, exist_ok=True)
        print("baixando ancient.jsonl…")
        urllib.request.urlretrieve(URL, FONTE)
    dados = {}
    for linha in FONTE.read_text(encoding="utf-8").splitlines():
        x = json.loads(linha)
        ids = x.get("identifications") or []
        c = ids[0]["score"]["time_total"] if ids else 0
        raio = re.match(r"within ([\d,.]+) km of", re.sub(r"<[^>]+>", "", ids[0]["description"])) if ids else None
        if raio and float(raio.group(1).replace(",", "")) >= 50:
            c = min(c, 299)
        dados[x["friendly_id"]] = (tipo(x.get("types") or []), c)
    lugares = json.loads(LUGARES.read_text(encoding="utf-8"))
    faltam = [l["n"] for l in lugares if l["n"] not in dados]
    assert not faltam, f"lugares sem dados no openbible: {faltam[:10]}"
    for l in lugares:
        l["t"], l["c"] = dados[l["n"]]
    LUGARES.write_text(json.dumps(lugares, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    conta = {}
    for l in lugares:
        conta[l["t"]] = conta.get(l["t"], 0) + 1
    print(f"{len(lugares)} lugares: {conta}; {sum(l['c'] < 300 for l in lugares)} com localização incerta (c < 300)")


if __name__ == "__main__":
    main()
