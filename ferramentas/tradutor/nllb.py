"""Tradutor NLLB-200 (Meta, licença CC-BY-NC — uso não comercial) en->pt, offline, via CTranslate2.

Mais lento que o Argos (~10x), mas bem mais fiel em prosa teológica longa (Calvino, Henry, Easton).
Por isso roda no GitHub Actions, dividido em várias máquinas, e não no notebook.

Correções sobre a saída do modelo:
- marcadores de tópico ("I.", "1.", "(2.)") são separados antes de traduzir — senão "I." vira "eu";
- o modelo converte "miles" em "quilômetros" sem converter o número: volta para "milhas";
- aspas curvas (“ ” ‘ ’) e travessão (—) NÃO existem no vocabulário do modelo: viram <unk>, que sai como
  "⁇" e ainda faz o modelo parar no meio da frase. Por isso entram como aspas retas e hífen (como nos
  dados de treino do NLLB) e voltam a ser curvas na saída;
- a frase que mesmo assim sai curta demais (texto engolido) é refeita em pedaços menores;
- frase em latim (o texto bíblico latino que acompanha os comentários de Calvino) fica como está: o modelo
  a "traduzia" inventando ("nihil haesitans" virava "nem os haitianos").
"""
import re
from pathlib import Path

import ctranslate2
import sentencepiece as spm

from tradutor import Tradutor, moderniza   # mesma divisão de frases e modernização do inglês arcaico

# marcadores de tópico ("I.", "II.", "1.", "(2.)", "[3.]"): ficam fora da tradução. Sozinhos, o modelo
# inventa ("I." vira "eu"; "1." vira "1. - O que é?").
ROMANO = re.compile(r"(?:(?<=^)|(?<=[,;:.!?)] ))([IVX]{1,5}\.|\d{1,2}\.|\(\d{1,2}\.?\)|\[\d{1,2}\.?\])(?=\s+[\"'“A-Z(])")


# pontuação que o modelo desconhece -> a equivalente que ele conhece
NORMAL = str.maketrans({"“": '"', "”": '"', "„": '"', "«": '"', "»": '"', "‘": "'", "’": "'", "‚": "'",
                        "…": "...", "\u00a0": " ", "\u2009": " ", "–": "-"})
DESC = "⁇"   # como o SentencePiece escreve um <unk>


def normaliza(f):
    return re.sub(r"\s*—\s*", " - ", f.translate(NORMAL))


def frases(texto):
    """Como Tradutor.frases, mas também corta depois de aspas ou parêntese de fechamento (.” Depois)
    e antes de número de versículo (. 6 But let him...), que separa o texto bíblico inglês do latino."""
    saida = []
    for p in re.split(r'(?:(?<=[.!?;])|(?<=[.!?][”"’\')\]]))\s+(?=[A-Z"“‘(\[]|\d{1,3}\.? [A-Za-z“"])', texto.strip()):
        saida.extend(Tradutor.frases(p))
    return saida


LATIM = set("""et est non qui quae quod autem enim sed ut cum eius ejus sunt vero ergo quia nec neque ad per ab ex si
sic atque etiam quam quis quid eum eos ei mihi tibi sibi nos vos deus dei deo dominus domini erat esse fuit hoc haec
hic ille illa illi ipse omnes omnia omnibus nam vel aut super sicut dum nihil ne de te se tu ego meum tuum suum
ipsi ipsis eorum quoniam propter contra apud inter ante post sine pro quoque tamen igitur itaque""".split())
INGLES = set("""the and of that he his for it with was be by this which they but have we are you shall will my from
to is not as on their them were has had what when who there or if all so""".split())


def latim(f):
    """Frase em latim: pelo menos 3 palavras latinas comuns e nenhuma inglesa comum."""
    pal = re.findall(r"[a-zæœ]+", f.lower())
    return sum(w in LATIM for w in pal) >= 3 and not any(w in INGLES for w in pal)


def aspas_curvas(pt):
    """Aspas retas -> curvas: abre no começo de palavra, fecha no resto."""
    pt = re.sub(r'(?:(?<=^)|(?<=[\s(\[—-]))"(?=\S)', "“", pt)
    return pt.replace('"', "”")


class NLLB:
    def __init__(self, pasta, threads=0, beam=4):
        pasta = Path(pasta)
        self.tr = ctranslate2.Translator(str(pasta), device="cpu", compute_type="int8", intra_threads=threads)
        self.sp = spm.SentencePieceProcessor(model_file=str(pasta / "sentencepiece.bpe.model"))
        self.beam = beam

    def _lote(self, frases):
        unk = self.sp.unk_id()
        src, soltos = [], []
        for f in frases:
            pecas = self.sp.encode(normaliza(moderniza(f)), out_type=str)[:380]
            # o que ainda for desconhecido (grego politônico raro) é devolvido na mesma ordem, se a conta fechar:
            # (letra, colada à esquerda?, colada à direita?)
            s = []
            for i, p in enumerate(pecas):
                if self.sp.piece_to_id(p) == unk:
                    esq = not p.startswith("▁") and not (i and pecas[i - 1] == "▁")
                    dir_ = i + 1 < len(pecas) and not pecas[i + 1].startswith("▁")
                    s.append((p.replace("▁", ""), esq, dir_))
            soltos.append(s)
            src.append(["eng_Latn"] + pecas + ["</s>"])
        res = self.tr.translate_batch(src, target_prefix=[["por_Latn"]] * len(src), beam_size=self.beam,
                                      max_batch_size=16, max_decoding_length=460, repetition_penalty=1.1)
        saida = []
        for r, s in zip(res, soltos):
            pt = self.sp.decode([t for t in r.hypotheses[0] if t != "por_Latn"]).strip()
            if DESC in pt:
                if pt.count(DESC) == len(s):
                    for c, esq, dir_ in s:
                        pt = re.sub(" ?" + DESC + " ?", lambda m: ("" if esq or not m.group(0).startswith(" ") else " ")
                                    + c + ("" if dir_ or not m.group(0).endswith(" ") else " "), pt, count=1)
                else:
                    pt = re.sub(r"\s*" + DESC + r"\s*", " ", pt).strip()
            saida.append(re.sub(r" {2,}", " ", pt))
        return saida

    @staticmethod
    def _curta(orig, pt):
        """Tradução que engoliu texto: o português quase nunca sai mais curto que 3/4 do inglês."""
        return len(orig) >= 60 and len(pt) < 0.72 * len(orig)

    def _lote_seguro(self, frases):
        saida = self._lote(frases)
        ruins = [i for i, (o, p) in enumerate(zip(frases, saida)) if self._curta(o, p)]
        if ruins:
            pecas = [Tradutor.pedacos(frases[i]) for i in ruins]
            trad = iter(self._lote([x for ps in pecas for x in ps]))
            for i, ps in zip(ruins, pecas):
                nova = " ".join(next(trad) for _ in ps)   # consome sempre, para não desalinhar
                if len(ps) > 1 and len(nova) > len(saida[i]):
                    saida[i] = nova
        return saida

    @staticmethod
    def _corrige(orig, pt):
        if re.search(r"\bmiles?\b", orig, re.I):
            pt = re.sub(r"\bquilômetros\b", "milhas", pt)
            pt = re.sub(r"\bquilômetro\b", "milha", pt)
            pt = re.sub(r"\b(\d+)\s*km\b", r"\1 milhas", pt)
        if "—" in orig:
            pt = re.sub(r"(?<=\S) - (?=\S)", " — ", pt)
        return aspas_curvas(pt)

    def traduzir(self, textos):
        # cada texto vira uma sequência de pedaços: ("R", "II.") é marcador de tópico e ("L", frase) é latim,
        # mantidos como estão; ("T", n) é a frase n da fila de tradução
        planos, fila = [], []
        for t in textos:
            plano = []
            for linha in (t or "").split("\n"):
                pecas = ROMANO.split(linha)
                for i, p in enumerate(pecas):
                    if i % 2 == 1:
                        plano.append(("R", p))
                    elif p.strip():
                        for f in frases(p):
                            if latim(f):
                                plano.append(("L", f))
                                continue
                            plano.append(("T", len(fila)))
                            fila.append(f)
                plano.append(("N", "\n"))
            planos.append(plano[:-1] if plano else [])
        trad = self._lote_seguro(fila) if fila else []
        saida = []
        for plano in planos:
            partes = []
            for tipo, v in plano:
                if tipo in ("R", "L"):
                    partes.append(v + " ")
                elif tipo == "N":
                    partes.append("\n")
                else:
                    partes.append(self._corrige(fila[v], trad[v]) + " ")
            saida.append(re.sub(r"[ \t]+\n", "\n", "".join(partes)).strip())
        return saida
