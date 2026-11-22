"""Alinha o roteiro de um vídeo narrado com a voz gravada: acha as pausas do áudio e dá o tempo de cada frase.

A voz vem de fora (ElevenLabs, gravação própria…); o roteiro é texto puro, um bloco por cena, separados por linha em
branco. Dentro do texto, {mostrado|falado} separa o que a legenda mostra do que a voz lê ("{129|cento e vinte e nove}"),
porque vozes sintéticas leem mal números e endereços. Linhas começadas por # são comentários.

    python3 ferramentas/video/narrado/alinhar.py <episódio> --texto   texto para colar no gerador de voz
    python3 ferramentas/video/narrado/alinhar.py <episódio>           grava episodios/<episódio>/tempos.json

Entrada: episodios/<episódio>/roteiro.txt e entrada/<episódio>/voz.mp3 (fora do git).
Como alinha: o texto é cortado em frases nos sinais de pontuação, e as pausas que o ffmpeg acha (silencedetect) são
casadas com os fins de frase por programação dinâmica: fim de período, dois-pontos e troca de bloco quase sempre têm
pausa, vírgula às vezes, e a velocidade da fala (caracteres por segundo) deve ser parecida entre um trecho e outro.
Confira a tabela que sai na tela; se um limite cair errado, ajuste o tempos.json à mão."""
import json, math, re, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
LIMITE_LEGENDA = 64          # caracteres por legenda


def ler_roteiro(ep):
    texto = (AQUI / "episodios" / ep / "roteiro.txt").read_text(encoding="utf-8")
    linhas = [l for l in texto.splitlines() if not l.lstrip().startswith("#")]
    return [b.strip().replace("\n", " ") for b in re.split(r"\n\s*\n", "\n".join(linhas)) if b.strip()]


def mostrado(t):
    return re.sub(r"\{([^|}]*)\|[^}]*\}", r"\1", t)


def falado(t):
    return re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", t)


def frases(blocos):
    """[(bloco, texto marcado, forte)]: cortes depois de . ! ? : ; (fortes) e de vírgula (fracos), fora das chaves."""
    saida = []
    for b, bloco in enumerate(blocos):
        partes = re.findall(r"(?:\{[^}]*\}|[^,.;:!?{])+[,.;:!?]*", bloco)
        partes = [p.strip() for p in partes if p.strip()]
        for i, p in enumerate(partes):
            forte = i == len(partes) - 1 or p[-1] in ".;:!?"
            saida.append((b, p, forte))
    return saida


def pausas(mp3):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(mp3), "-af", "silencedetect=noise=-38dB:d=0.3", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    h, mi, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r).groups()
    dur = int(h) * 3600 + int(mi) * 60 + float(s)
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    fim = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    ps = list(zip(ini, fim + [dur] * (len(ini) - len(fim))))
    comeco = ps[0][1] if ps and ps[0][0] < 0.05 else 0.0
    if ps and ps[0][0] < 0.05:
        ps = ps[1:]
    final = ps[-1][0] if ps and ps[-1][1] >= dur - 0.05 else dur
    if ps and ps[-1][1] >= dur - 0.05:
        ps = ps[:-1]
    return dur, comeco, final, ps


def alinhar(fr, comeco, final, ps):
    """Programação dinâmica: casa fins de frase (0..n-2) com pausas, em ordem. Devolve [ini, fim] de cada frase."""
    n, m = len(fr), len(ps)
    tam = [len(falado(t)) for _, t, _ in fr]
    acum = [0]
    for t in tam:
        acum.append(acum[-1] + t)
    fala_total = (final - comeco) - sum(b - a for a, b in ps)
    r0 = acum[-1] / fala_total
    # pontos: (-1, início) ... (n-1, fim); custo de ir de (i, ponto a) a (j, ponto b) = frases i+1..j num trecho só
    pontos = [(comeco, comeco)] + ps + [(final, final)]
    INF = float("inf")
    melhor = {(-1, 0): (0.0, None)}

    def custo_trecho(i, j, a, b):
        chars = acum[j + 1] - acum[i + 1]
        t = pontos[b][0] - pontos[a][1]
        if t <= 0.2:
            return INF
        c = 4 * math.log((chars / t) / r0) ** 2
        for k in range(i + 1, j):                           # fins de frase sem pausa no meio do trecho
            c += 3.0 if fr[k][2] or fr[k + 1][0] != fr[k][0] else 0.25
        c += 2.5 * (b - a - 1)                              # pausas puladas (sem pontuação)
        return c

    for j in range(n):
        for b in range(1, m + 2):
            if (j == n - 1) != (b == m + 1):
                continue
            best = (INF, None)
            for (i, a), (c0, _) in melhor.items():
                if i < j and a < b:
                    c = c0 + custo_trecho(i, j, a, b)
                    if c < best[0]:
                        best = (c, (i, a))
            if best[1] is not None:
                melhor[(j, b)] = best
    # volta pelo caminho
    caminho, no = [], (n - 1, m + 1)
    while no and no[0] >= 0:
        caminho.append(no)
        no = melhor[no][1]
    caminho.append((-1, 0))
    caminho.reverse()
    tempos = [None] * n
    for (i, a), (j, b) in zip(caminho, caminho[1:]):
        t0, t1 = pontos[a][1], pontos[b][0]
        total = acum[j + 1] - acum[i + 1]
        for k in range(i + 1, j + 1):
            ini = t0 + (t1 - t0) * (acum[k] - acum[i + 1]) / total
            fim = t0 + (t1 - t0) * (acum[k + 1] - acum[i + 1]) / total
            tempos[k] = [round(ini, 2), round(fim, 2)]
    return tempos


def legendas(fr, tempos):
    """junta frases seguidas do mesmo bloco até ~LIMITE_LEGENDA caracteres"""
    saida = []
    for (b, t, _), (ini, fim) in zip(fr, tempos):
        txt = mostrado(t)
        if saida and saida[-1]["bloco"] == b and len(saida[-1]["texto"]) + len(txt) + 1 <= LIMITE_LEGENDA \
                and not saida[-1]["texto"].endswith((".", "?", "!")):
            saida[-1]["texto"] += " " + txt
            saida[-1]["fim"] = fim
        else:
            saida.append({"ini": ini, "fim": fim, "texto": txt, "bloco": b})
    return saida


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ep = sys.argv[1]
    blocos = ler_roteiro(ep)
    if "--texto" in sys.argv:
        print("\n\n".join(falado(b) for b in blocos))
        return
    mp3 = AQUI / "entrada" / ep / "voz.mp3"
    dur, comeco, final, ps = pausas(mp3)
    fr = frases(blocos)
    tempos = alinhar(fr, comeco, final, ps)
    saida = {
        "duracao": round(dur, 2),
        "blocos": [{"ini": next(t[0] for (b, _, _), t in zip(fr, tempos) if b == i),
                    "fim": [t[1] for (b, _, _), t in zip(fr, tempos) if b == i][-1],
                    "texto": mostrado(blocos[i])} for i in range(len(blocos))],
        "frases": [{"ini": t[0], "fim": t[1], "texto": mostrado(x), "bloco": b} for (b, x, _), t in zip(fr, tempos)],
    }
    saida["legendas"] = legendas(fr, tempos)
    (AQUI / "episodios" / ep / "tempos.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(ps)} pausas em {dur:.1f} s; fala de {comeco:.2f} a {final:.2f} s")
    for i, bl in enumerate(saida["blocos"]):
        print(f"bloco {i + 1}: {bl['ini']:6.2f} – {bl['fim']:6.2f}  {bl['texto'][:60]}")
    for f in saida["frases"]:
        print(f"   {f['ini']:6.2f} – {f['fim']:6.2f}  {f['texto']}")


if __name__ == "__main__":
    main()
