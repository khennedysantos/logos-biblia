"""Teste rápido do NLLB numa amostra, antes de traduzir uma etapa inteira (roda no GitHub Actions: workflow
"Traduzir (NLLB)" com amostra = N). Mostra no log, para cada trecho, o inglês preparado e a tradução sem e com a
proteção das referências (nllb.protege_refs), e no fim quantos grupos de referências cada jeito preservou.
uso: python3 teste_refs.py entrada.json pasta_modelo N"""
import json, random, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from nllb import NLLB, RE_UNIDADE, protege_refs   # noqa: E402

# verbetes conhecidos do Easton, para comparar com a tradução antiga (Argos)
FIXOS = ["A|Angel|0", "G|Grace|0", "G|Gospel|0", "F|Faith|0", "J|Justification|0", "A|Adoption|0", "C|Covenant|0"]


def main():
    entrada, modelo, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    itens = [i for i in json.loads(Path(entrada).read_text(encoding="utf-8")) if i["texto"].strip()]
    por_id = {i["id"]: i for i in itens}
    random.seed(7)
    com_ref = [i for i in itens if RE_UNIDADE.search(i["texto"]) and len(i["texto"]) < 1500]
    amostra = [por_id[k] for k in FIXOS if k in por_id]
    amostra += random.sample([i for i in com_ref if i["id"] not in FIXOS], max(0, n - len(amostra)))
    textos = [i["texto"] for i in amostra]
    T = NLLB(modelo)
    sem = T.traduzir(textos, proteger_refs=False)
    com = T.traduzir(textos, proteger_refs=True)
    intactos = total = 0
    for i, a, b in zip(amostra, sem, com):
        print("=" * 100)
        print("ID :", i["id"])
        print("EN :", i["texto"])
        print("SEM:", a)
        print("COM:", b)
        _, grupos = protege_refs(i["texto"])
        total += len(grupos)
        intactos += sum(g in a for g, _, _ in grupos)
    print("=" * 100)
    print(f"grupos de referências: {total}; intactos sem proteção: {intactos}; "
          f"com proteção, foram para o fim do texto: {T.refs[1]} de {T.refs[0]}")


if __name__ == "__main__":
    main()
