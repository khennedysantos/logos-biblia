"""Relevo sombreado do Atlas -> mapa/relevo/{z}/{x}/{y}.png (azulejos do próprio site, em cinza).

A elevação vem dos Terrain Tiles do AWS Open Data (formato "terrarium": SRTM e GMTED da NASA/USGS, ETOPO1 da NOAA e
EU-DEM do Copernicus; registry.opendata.aws/terrain-tiles). Daqui sai só o sombreado calculado: luz do noroeste, como nos
atlas impressos. Cada azulejo é um PNG cinza com transparência: encosta na sombra = preto translúcido, encosta
iluminada = branco translúcido, mar e terra plana = transparente. Assim o mesmo arquivo serve aos temas claro e escuro
(o app só ajusta a opacidade da camada).

Níveis (zoom da web, projeção de Mercator, mesmos azulejos 256×256 do Leaflet):
- 3 a 5: da Espanha à Índia (elevação do zoom 5, reduzida para 4 e 3);
- 6 e 7: do Mediterrâneo à Mesopotâmia (zoom 7, reduzida para 6);
- 8: a Terra Santa, para a vista de perto.
Só Python padrão (PNG lido e gravado com zlib). Os azulejos baixados ficam em ferramentas/fontes/terrarium/, fora do git.
uso:  python3 ferramentas/gerar_relevo.py
Grava também data/mapa/relevo.json ({zoom: [x0, y0, x1, y1]}), para o app só pedir azulejos que existem."""
import json, math, shutil, struct, urllib.request, zlib
from array import array
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / "ferramentas" / "fontes" / "terrarium"
DESTINO = RAIZ / "mapa" / "relevo"
INDICE = RAIZ / "data" / "mapa" / "relevo.json"      # em data/: o app o pede com a versão no endereço
URL = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
# (zoom da elevação baixada, caixa [lon0, lat0, lon1, lat1], zooms gravados: o primeiro é o baixado, os outros reduzidos)
CAMADAS = [(5, (-14, 0, 92, 52), (5, 4, 3)),
           (7, (-12, 12, 62, 47), (7, 6)),
           (8, (33.0, 29.0, 37.6, 34.4), (8,))]
# lugares abaixo do nível do mar que são terra, não mar: o vale do Jordão (o piso −415 m deixa de fora a superfície
# do mar Morto, ~−430 m, que fica lisa como água)
DEPRESSOES = [(34.9, 29.4, 35.95, 33.1, -415)]
EXAGERO = {3: 9, 4: 7, 5: 5, 6: 3.5, 7: 2.5, 8: 2}      # exagero vertical: de longe o relevo precisa ser mais forte
R = 6378137.0


def tile_xy(lon, lat, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return int(x), int(y)


def lat_do_pixel(py, z):
    """latitude do centro da linha py (pixels de Mercator no zoom z)"""
    n = 256 * 2 ** z
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (py + .5) / n))))


def ler_png_rgb(dados):
    """PNG 8 bits RGB (tipo 2) ou RGBA (tipo 6), sem entrelaçamento -> (largura, altura, canais, bytes)"""
    assert dados[:8] == b"\x89PNG\r\n\x1a\n"
    pos, idat, larg = 8, b"", 0
    while pos < len(dados):
        tam, = struct.unpack(">I", dados[pos:pos + 4]); tipo = dados[pos + 4:pos + 8]; corpo = dados[pos + 8:pos + 8 + tam]
        if tipo == b"IHDR":
            larg, alt, prof, cor, _, _, entrel = struct.unpack(">IIBBBBB", corpo)
            assert prof == 8 and cor in (2, 6) and not entrel, "PNG inesperado"
            canais = 3 if cor == 2 else 4
        elif tipo == b"IDAT":
            idat += corpo
        pos += 12 + tam
    bruto, passo = zlib.decompress(idat), larg * canais
    saida, ant = bytearray(alt * passo), bytearray(passo)
    for y in range(alt):
        f, linha = bruto[y * (passo + 1)], bytearray(bruto[y * (passo + 1) + 1:(y + 1) * (passo + 1)])
        if f == 1:
            for i in range(canais, passo):
                linha[i] = (linha[i] + linha[i - canais]) & 255
        elif f == 2:
            for i in range(passo):
                linha[i] = (linha[i] + ant[i]) & 255
        elif f == 3:
            for i in range(passo):
                linha[i] = (linha[i] + ((linha[i - canais] if i >= canais else 0) + ant[i]) // 2) & 255
        elif f == 4:
            for i in range(passo):
                a = linha[i - canais] if i >= canais else 0
                b, c = ant[i], (ant[i - canais] if i >= canais else 0)
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                linha[i] = (linha[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        saida[y * passo:(y + 1) * passo] = linha
        ant = linha
    return larg, alt, canais, saida


SOMBRA = bytes(b for v in range(256) for b in ((0, min(255, (128 - v) * 2)) if v < 128 else (255, min(255, (v - 128) * 3 // 2))))


def gravar_png_cinza(caminho, larg, alt, px):
    """PNG cinza com transparência (tipo 4): o valor 0–255 do sombreado vira preto ou branco translúcido"""
    linhas = b"".join(b"\x00" + b"".join(SOMBRA[2 * v:2 * v + 2] for v in px[y * larg:(y + 1) * larg]) for y in range(alt))
    def bloco(tipo, corpo):
        return struct.pack(">I", len(corpo)) + tipo + corpo + struct.pack(">I", zlib.crc32(tipo + corpo) & 0xffffffff)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(b"\x89PNG\r\n\x1a\n" + bloco(b"IHDR", struct.pack(">IIBBBBB", larg, alt, 8, 4, 0, 0, 0))
                        + bloco(b"IDAT", zlib.compress(linhas, 9)) + bloco(b"IEND", b""))


def mosaico(z, caixa, alinhar=1):
    """elevação (metros) dos azulejos que cobrem a caixa, num só quadro; devolve (x0, y0, largura, altura, valores).
    Com alinhar = 2^k, o quadro começa e termina em múltiplos de 2^k azulejos, para reduzir k vezes sem desalinhar."""
    x0, y1 = tile_xy(caixa[0], caixa[1], z)
    x1, y0 = tile_xy(caixa[2], caixa[3], z)
    x0, y0 = x0 - x0 % alinhar, y0 - y0 % alinhar
    x1, y1 = x1 + (alinhar - 1 - x1 % alinhar), y1 + (alinhar - 1 - y1 % alinhar)
    nx, ny = x1 - x0 + 1, y1 - y0 + 1
    larg, alt = nx * 256, ny * 256
    elev = array("f", bytes(4 * larg * alt))
    for ty in range(y0, y1 + 1):
        for tx in range(x0, x1 + 1):
            arq = CACHE / str(z) / str(tx) / f"{ty}.png"
            if not arq.exists():
                arq.parent.mkdir(parents=True, exist_ok=True)
                urllib.request.urlretrieve(URL.format(z=z, x=tx, y=ty), arq)
            w, h, canais, px = ler_png_rgb(arq.read_bytes())
            ox, oy = (tx - x0) * 256, (ty - y0) * 256
            for y in range(256):
                base, lin = (oy + y) * larg + ox, y * 256 * canais
                for x in range(256):
                    i = lin + x * canais
                    elev[base + x] = px[i] * 256 + px[i + 1] + px[i + 2] / 256 - 32768
    print(f"  zoom {z}: {nx * ny} azulejos de elevação ({larg}×{alt})")
    return x0, y0, larg, alt, elev


def reduzir(m):
    """metade da resolução (média de 2×2), para o zoom de baixo"""
    x0, y0, larg, alt, e = m
    nl, na = larg // 2, alt // 2
    saida = array("f", bytes(4 * nl * na))
    for y in range(na):
        a, b = 2 * y * larg, (2 * y + 1) * larg
        for x in range(nl):
            saida[y * nl + x] = (e[a + 2 * x] + e[a + 2 * x + 1] + e[b + 2 * x] + e[b + 2 * x + 1]) / 4
    return x0 // 2, y0 // 2, nl, na, saida


def sombrear(m, z):
    """cinza 0–255 (128 = plano; mar e terra plana ficam em 128)"""
    x0, y0, larg, alt, e = m
    exagero = EXAGERO[z]
    az, alt_sol = math.radians(315), math.radians(45)
    lx, ly, lz = math.sin(az) * math.cos(alt_sol), math.cos(az) * math.cos(alt_sol), math.sin(alt_sol)
    plano = lz
    n = 256 * 2 ** z
    deps = [(int((a + 180) / 360 * n) - x0 * 256, int((b + 180) / 360 * n) - x0 * 256, lat_a, lat_b, piso)
            for a, lat_a, b, lat_b, piso in DEPRESSOES]
    px = bytearray(b"\x80" * (larg * alt))
    for y in range(1, alt - 1):
        lat = lat_do_pixel(y0 * 256 + y, z)
        metros = 2 * math.pi * R * math.cos(math.radians(lat)) / (256 * 2 ** z)
        faixas = [(xa, xb, piso) for xa, xb, la, lb, piso in deps if la <= lat <= lb]
        k = exagero / (2 * metros)
        cima, linha, baixo = (y - 1) * larg, y * larg, (y + 1) * larg
        for x in range(1, larg - 1):
            h = e[linha + x]
            if h <= 0 and not any(xa <= x <= xb and h > piso for xa, xb, piso in faixas):
                continue
            dzdx = (e[linha + x + 1] - e[linha + x - 1]) * k
            dzdy = (e[cima + x] - e[baixo + x]) * k          # norte para cima
            luz = (lz - dzdx * lx - dzdy * ly) / math.sqrt(1 + dzdx * dzdx + dzdy * dzdy)
            v = 128 + (luz - plano) * 210
            px[linha + x] = max(8, min(248, int(v) & ~3))
    return px


def gravar(m, z, px, indice):
    x0, y0, larg, alt, _ = m
    indice[str(z)] = [x0, y0, x0 + larg // 256 - 1, y0 + alt // 256 - 1]     # azulejos que existem neste zoom
    n = 0
    for ty in range(alt // 256):
        for tx in range(larg // 256):
            bloco = bytearray(256 * 256)
            for y in range(256):
                ini = (ty * 256 + y) * larg + tx * 256
                bloco[y * 256:(y + 1) * 256] = px[ini:ini + 256]
            gravar_png_cinza(DESTINO / str(z) / str(x0 + tx) / f"{y0 + ty}.png", 256, 256, bloco)
            n += 1
    return n


def main():
    if DESTINO.exists():
        shutil.rmtree(DESTINO)
    total, indice = 0, {}
    for z_baixado, caixa, zooms in CAMADAS:
        m = mosaico(z_baixado, caixa, 2 ** (len(zooms) - 1))
        for z in zooms:
            if z != z_baixado:
                m = reduzir(m)
            n = gravar(m, z, sombrear(m, z), indice)
            total += n
            print(f"  relevo zoom {z}: {n} azulejos")
    INDICE.write_text(json.dumps(indice, sort_keys=True) + "\n", encoding="utf-8")
    tam = sum(f.stat().st_size for f in DESTINO.rglob("*.png"))
    print(f"{total} azulejos em {DESTINO.relative_to(RAIZ)} ({tam / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
