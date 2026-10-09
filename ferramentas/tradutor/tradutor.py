"""Tradutor offline inglês -> português brasileiro, gratuito.
Usa o modelo do Argos Translate (en_pb 1.9) direto via CTranslate2 + SentencePiece."""
import re
import ctranslate2, sentencepiece as spm
from pathlib import Path


# inglês arcaico (da KJV, comum em Calvino, Easton e Strong) que o modelo não conhece
ARCAICO = [(r"\bAsses\b", "Donkeys"), (r"\basses\b", "donkeys"), (r"\bass-colt\b", "donkey colt"),
           (r"\bAss\b", "Donkey"), (r"\bass\b", "donkey"),
           (r"\bthee\b", "you"), (r"\bThee\b", "You"), (r"\bthou\b", "you"), (r"\bThou\b", "You"),
           (r"\bthy\b", "your"), (r"\bThy\b", "Your"), (r"\bthine\b", "your"), (r"\bye\b", "you"), (r"\bYe\b", "You"),
           (r"\bhath\b", "has"), (r"\bdoth\b", "does"), (r"\bsaith\b", "says"), (r"\bart\b(?= (?:the|a|my|our|not|thou|you)\b)", "are"),
           (r"\bunto\b", "to"), (r"\bUnto\b", "To"), (r"\bspake\b", "spoke"), (r"\bshew\b", "show"), (r"\bshewed\b", "showed"),
           (r"\bcompact\b", "pact"), (r"\bspecially\b", "especially"), (r"\bassayal\b", "testing"),
           (r"\bwinnowing-fork\b", "winnowing shovel"), (r"\bdregs\b", "sediment")]


def moderniza(t):
    for a, b in ARCAICO:
        t = re.sub(a, b, t)
    return t


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
        toks = [self.sp.encode(moderniza(f), out_type=str) for f in frases]
        res = self.tr.translate_batch(toks, beam_size=beam, max_batch_size=32,
                                      max_decoding_length=512, replace_unknowns=True)
        return [self.sp.decode(r.hypotheses[0]).replace("▁", " ").strip() for r in res]

    @staticmethod
    def suspeita(orig, pt):
        """Tradução que provavelmente engoliu texto ou alucinou (ex.: virou 'O que é isso?')."""
        if len(orig) < 30:
            return False
        return len(pt) < 0.7 * len(orig) or (pt.rstrip().endswith("?") and not orig.rstrip().endswith("?"))

    @staticmethod
    def pedacos(frase):
        """Divide uma frase em orações menores (em ';', ':' e ',') para retraduzir."""
        partes = re.split(r"(?<=[;:,])\s+", frase)
        juntas, atual = [], ""
        for p in partes:
            atual = (atual + " " + p).strip() if atual else p
            if len(atual) >= 25:
                juntas.append(atual); atual = ""
        if atual:
            if juntas: juntas[-1] += " " + atual
            else: juntas.append(atual)
        return juntas

    def traduzir(self, textos, beam=2):
        mapa, todas = [], []
        for t in textos:
            fs = self.frases(t) if t and t.strip() else []
            mapa.append((len(todas), len(fs)))
            todas.extend(fs)
        saida = self._lote(todas, beam) if todas else []
        # segunda passada: frases com omissão são refeitas em pedaços menores
        ruins = [i for i, (o, p) in enumerate(zip(todas, saida)) if self.suspeita(o, p)]
        if ruins:
            pecas = [self.pedacos(todas[i]) for i in ruins]
            planas = [x for ps in pecas for x in ps]
            trad = iter(self._lote(planas, beam))
            for i, ps in zip(ruins, pecas):
                nova = " ".join(next(trad) for _ in ps)  # consome sempre, para não desalinhar
                if len(ps) > 1 and len(nova) > len(saida[i]):
                    saida[i] = nova
        return [" ".join(saida[a:a + n]) for a, n in mapa]
