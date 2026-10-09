"""Tradutor offline inglês -> português brasileiro, gratuito.
Usa o modelo do Argos Translate (en_pb 1.9) direto via CTranslate2 + SentencePiece."""
import re
import ctranslate2, sentencepiece as spm
from pathlib import Path


class Tradutor:
    def __init__(self, pasta, threads=0):
        pasta = Path(pasta)
        self.tr = ctranslate2.Translator(str(pasta / "model"), device="cpu",
                                         inter_threads=1, intra_threads=threads, compute_type="int8")
        self.sp = spm.SentencePieceProcessor(model_file=str(pasta / "sentencepiece.model"))

    @staticmethod
    def frases(texto):
        partes = re.split(r'(?<=[.!?;])\s+(?=[A-Z"“(\[])', texto.strip())
        saida = []
        for p in partes:
            # frases muito longas (comuns em Calvino) são quebradas para não truncar
            while len(p) > 700:
                corte = max(p.rfind('; ', 0, 700), p.rfind(': ', 0, 700), p.rfind(', ', 0, 700))
                if corte < 150:
                    break
                saida.append(p[:corte + 1])
                p = p[corte + 2:]
            if p:
                saida.append(p)
        return saida

    def _lote(self, frases, beam):
        toks = [self.sp.encode(f, out_type=str) for f in frases]
        res = self.tr.translate_batch(toks, beam_size=beam, max_batch_size=32,
                                      max_decoding_length=512, replace_unknowns=True)
        return [self.sp.decode(r.hypotheses[0]).replace("▁", " ").strip() for r in res]

    def traduzir(self, textos, beam=2):
        mapa, todas = [], []
        for t in textos:
            fs = self.frases(t) if t and t.strip() else []
            mapa.append((len(todas), len(fs)))
            todas.extend(fs)
        saida = self._lote(todas, beam) if todas else []
        return [" ".join(saida[a:a + n]) for a, n in mapa]
