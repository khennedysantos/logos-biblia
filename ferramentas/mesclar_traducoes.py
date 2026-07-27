"""
Mescla traducoes.json (saída do traduzir_comentarios.py) nos arquivos do site.
Rode a partir da pasta ferramentas/:  python mesclar_traducoes.py
Substitui o texto em inglês pelo português em data/commentaries/calvin/.
Pode rodar quantas vezes quiser — só troca o que já foi traduzido.
"""
import json
from pathlib import Path

AQUI = Path(__file__).parent
DESTINO = AQUI.parent / "data" / "commentaries" / "calvin"
TRAD = AQUI / "traducoes.json"

if not TRAD.exists():
    raise SystemExit("traducoes.json não encontrado nesta pasta. "
                     "Rode antes o traduzir_comentarios.py (enviar + baixar).")

traducoes = json.loads(TRAD.read_text(encoding="utf-8"))
por_capitulo = {}
for tid, texto in traducoes.items():
    # id no formato calvin-LIVRO-CAP-VERSO
    _, livro, cap, verso = tid.split("-")
    por_capitulo.setdefault((livro, cap), {})[verso] = texto

trocados = 0
for (livro, cap), versos in por_capitulo.items():
    arq = DESTINO / livro / f"{cap}.json"
    if not arq.exists():
        continue
    dados = json.loads(arq.read_text(encoding="utf-8"))
    for v, texto in versos.items():
        if v in dados:
            dados[v] = texto
            trocados += 1
    dados["__pt"] = True  # sinaliza ao site que este capítulo já está em português
    arq.write_text(json.dumps(dados, ensure_ascii=False, separators=(",", ":")),
                   encoding="utf-8")

print(f"{trocados} blocos de comentário atualizados para português.")
print("Pronto — publique a pasta do site novamente para as traduções irem ao ar.")
