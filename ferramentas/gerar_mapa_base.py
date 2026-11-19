"""Base do Atlas sem nomes modernos -> data/mapa/base.json: terra, litoral, lagos e rios do Natural Earth (domínio
público, naturalearthdata.com), recortados para a região bíblica e simplificados. O app desenha essa base com as cores
do site e põe por cima só os nomes bíblicos em português (data/places.json) — nenhum azulejo de mapa vem de fora.

Dois níveis: "geral" (escala 1:50 milhões, da Espanha à Índia, para o zoom de longe) e "detalhe" (1:10 milhões, do
Mediterrâneo à Mesopotâmia, para o zoom de perto). Coordenadas em listas planas [lon, lat, lon, lat, …] com 3 casas;
"terra" e "lagos" são listas de polígonos, cada um com o contorno e os buracos; "costa" e "rios", listas de linhas.

uso:  python3 ferramentas/gerar_mapa_base.py
(baixa os arquivos do Natural Earth para ferramentas/fontes/natural-earth/, fora do git, se ainda não estiverem lá)"""
import json, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FONTES = RAIZ / "ferramentas" / "fontes" / "natural-earth"
DESTINO = RAIZ / "data" / "mapa" / "base.json"
URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/{}.geojson"
NIVEIS = {   # nome: (escala, caixa [lon0, lat0, lon1, lat1], tolerância da simplificação em graus, maior scalerank dos rios)
    "geral": ("50m", (-14, 0, 92, 52), 0.03, 6),
    "detalhe": ("10m", (-12, 12, 62, 47), 0.006, 9),
}


def ler(nome):
    arq = FONTES / f"{nome}.geojson"
    if not arq.exists():
        FONTES.mkdir(parents=True, exist_ok=True)
        print(f"baixando {nome}…")
        urllib.request.urlretrieve(URL.format(nome), arq)
    return json.loads(arq.read_text(encoding="utf-8"))["features"]


def partes(geom, tipo):
    """os polígonos (cada um: contorno e buracos, como o Cáspio na terra) ou as linhas de uma geometria GeoJSON"""
    if not geom:
        return []
    g, c = geom["type"], geom["coordinates"]
    if tipo == "poligono":
        return [c] if g == "Polygon" else c if g == "MultiPolygon" else []
    return [c] if g == "LineString" else c if g == "MultiLineString" else []


def recortar_anel(anel, caixa):
    """Sutherland–Hodgman contra o retângulo (a borda criada no corte não é desenhada: a terra não tem contorno)"""
    x0, y0, x1, y1 = caixa
    lados = [(lambda p: p[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
             (lambda p: p[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
             (lambda p: p[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
             (lambda p: p[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1))]
    pts = [tuple(p[:2]) for p in anel]
    for dentro, corte in lados:
        if not pts:
            break
        saida, ant = [], pts[-1]
        for p in pts:
            if dentro(p):
                if not dentro(ant):
                    saida.append(corte(ant, p))
                saida.append(p)
            elif dentro(ant):
                saida.append(corte(ant, p))
            ant = p
        pts = saida
    return pts


def recortar_linha(linha, caixa):
    """os trechos da linha dentro do retângulo"""
    x0, y0, x1, y1 = caixa
    trechos, atual = [], []
    for p in linha:
        if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
            atual.append(tuple(p[:2]))
        elif atual:
            trechos.append(atual)
            atual = []
    return trechos + ([atual] if atual else [])


def simplificar(pts, tol):
    """Douglas–Peucker iterativo"""
    if len(pts) < 3:
        return pts
    manter = [False] * len(pts)
    manter[0] = manter[-1] = True
    pilha = [(0, len(pts) - 1)]
    while pilha:
        a, b = pilha.pop()
        (ax, ay), (bx, by) = pts[a], pts[b]
        dx, dy = bx - ax, by - ay
        norma = (dx * dx + dy * dy) ** 0.5
        maior, idx = -1.0, -1
        for i in range(a + 1, b):
            px, py = pts[i]
            d = abs(dy * px - dx * py + bx * ay - by * ax) / norma if norma else ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5
            if d > maior:
                maior, idx = d, i
        if maior > tol:
            manter[idx] = True
            pilha += [(a, idx), (idx, b)]
    return [p for p, m in zip(pts, manter) if m]


def plano(pts):
    return [round(v, 3) for p in pts for v in p]


def nivel(escala, caixa, tol, rank_rios):
    saida = {"terra": [], "costa": [], "lagos": [], "rios": []}
    for camada, nome, t in (("terra", f"ne_{escala}_land", tol), ("lagos", f"ne_{escala}_lakes", tol / 2)):
        for f in ler(nome):
            for poligono in partes(f["geometry"], "poligono"):
                aneis = [simplificar(recortar_anel(anel, caixa), t) for anel in poligono]
                if len(aneis[0]) >= 4:                       # sem o contorno, o polígono está fora da caixa
                    saida[camada].append([plano(a) for a in aneis if len(a) >= 4])
    for camada, nome, tol_linha in (("costa", f"ne_{escala}_coastline", tol), ("rios", f"ne_{escala}_rivers_lake_centerlines", tol)):
        for f in ler(nome):
            if camada == "rios" and (f["properties"].get("scalerank") or 99) > rank_rios:
                continue
            for linha in partes(f["geometry"], "linha"):
                for trecho in recortar_linha(linha, caixa):
                    pts = simplificar(trecho, tol_linha)
                    if len(pts) >= 2:
                        saida[camada].append(plano(pts))
    return saida


def main():
    base = {"fonte": "Natural Earth (domínio público), naturalearthdata.com", "niveis": {}}
    for nome, (escala, caixa, tol, rank) in NIVEIS.items():
        base["niveis"][nome] = dict(nivel(escala, caixa, tol, rank), caixa=list(caixa))
        n = base["niveis"][nome]
        conta = lambda v: sum(len(x) if isinstance(x[0], (int, float)) else sum(len(a) for a in x) for x in v) // 2
        print(f"[{nome}] {', '.join(f'{k}: {len(v)} ({conta(v):,} pontos)' for k, v in n.items() if k != 'caixa')}")
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(json.dumps(base, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"{DESTINO.relative_to(RAIZ)}: {DESTINO.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
