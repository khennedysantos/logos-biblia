"""Tradutor NLLB-200 (Meta, licença CC-BY-NC — uso não comercial) en->pt, offline, via CTranslate2.

Mais lento que o Argos (~10x), mas bem mais fiel em prosa teológica longa (Calvino, Henry, Easton).
Por isso roda no GitHub Actions, dividido em várias máquinas, e não no notebook.

Correções sobre a saída do modelo:
- marcadores de tópico ("I.", "1.", "(2.)") são separados antes de traduzir — senão "I." vira "eu";
- o modelo converte "miles" em "quilômetros" sem converter o número: volta para "milhas".
"""
import re
from pathlib import Path

import ctranslate2
import sentencepiece as spm

from tradutor import Tradutor, moderniza   # mesma divisão de frases e modernização do inglês arcaico

# marcadores de tópico ("I.", "II.", "1.", "(2.)", "[3.]"): ficam fora da tradução. Sozinhos, o modelo
# inventa ("I." vira "eu"; "1." vira "1. - O que é?").
ROMANO = re.compile(r"(?:(?<=^)|(?<=[,;:.!?)] ))([IVX]{1,5}\.|\d{1,2}\.|\(\d{1,2}\.?\)|\[\d{1,2}\.?\])(?=\s+[\"'“A-Z(])")


class NLLB:
    def __init__(self, pasta, threads=0, beam=4):
        pasta = Path(pasta)
        self.tr = ctranslate2.Translator(str(pasta), device="cpu", compute_type="int8", intra_threads=threads)
        self.sp = spm.SentencePieceProcessor(model_file=str(pasta / "sentencepiece.bpe.model"))
        self.beam = beam

    def _lote(self, frases):
        src = [["eng_Latn"] + self.sp.encode(moderniza(f), out_type=str)[:380] + ["</s>"] for f in frases]
        res = self.tr.translate_batch(src, target_prefix=[["por_Latn"]] * len(src), beam_size=self.beam,
                                      max_batch_size=16, max_decoding_length=460, repetition_penalty=1.1)
        return [self.sp.decode([t for t in r.hypotheses[0] if t != "por_Latn"]).strip() for r in res]

    @staticmethod
    def _corrige(orig, pt):
        if re.search(r"\bmiles?\b", orig, re.I):
            pt = re.sub(r"\bquilômetros\b", "milhas", pt)
            pt = re.sub(r"\bquilômetro\b", "milha", pt)
            pt = re.sub(r"\b(\d+)\s*km\b", r"\1 milhas", pt)
        return pt

    def traduzir(self, textos):
        # cada texto vira uma sequência de pedaços: ("R", "II.") é tópico romano mantido; ("T", frase) é traduzido
        planos, frases = [], []
        for t in textos:
            plano = []
            for linha in (t or "").split("\n"):
                pecas = ROMANO.split(linha)
                for i, p in enumerate(pecas):
                    if i % 2 == 1:
                        plano.append(("R", p))
                    elif p.strip():
                        for f in Tradutor.frases(p):
                            plano.append(("T", len(frases)))
                            frases.append(f)
                plano.append(("N", "\n"))
            planos.append(plano[:-1] if plano else [])
        trad = self._lote(frases) if frases else []
        saida = []
        for plano in planos:
            partes = []
            for tipo, v in plano:
                if tipo == "R":
                    partes.append(v + " ")
                elif tipo == "N":
                    partes.append("\n")
                else:
                    partes.append(self._corrige(frases[v], trad[v]) + " ")
            saida.append(re.sub(r"[ \t]+\n", "\n", "".join(partes)).strip())
        return saida
