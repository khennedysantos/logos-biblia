"""
Tradutor em lote de comentários bíblicos (inglês -> português brasileiro)
usando a Batch API da Anthropic (50% de desconto sobre o preço normal).

USO:
  1. pip install anthropic
  2. export ANTHROPIC_API_KEY="sua-chave"   (no Windows: set ANTHROPIC_API_KEY=...)
  3. Prepare um arquivo entradas.json — lista de objetos:
       [
         {
           "id": "mhenry-john-1-1",
           "fonte": "Matthew Henry (1706)",
           "livro": "John", "capitulo": 1,
           "verso_inicio": 1, "verso_fim": 5,
           "texto": "texto original em inglês..."
         },
         ...
       ]
  4. python traduzir_comentarios.py enviar entradas.json
     -> imprime o batch_id e salva em batches_pendentes.txt
  5. python traduzir_comentarios.py baixar <batch_id>
     -> quando o lote terminar, salva traducoes.json (acumula entre execuções)

  Lotes grandes: o script divide automaticamente em blocos de até
  MAX_POR_LOTE requisições e imprime um batch_id por bloco.

Docs: https://docs.claude.com/en/api/overview  (Message Batches)
"""

import json
import sys
import os
from pathlib import Path

import anthropic

MODELO = "claude-haiku-4-5"
MAX_POR_LOTE = 10_000          # limite prático de requisições por lote
MAX_TOKENS_SAIDA = 4096        # suficiente p/ blocos de comentário; aumente se cortar
ARQ_SAIDA = "traducoes.json"
ARQ_PENDENTES = "batches_pendentes.txt"

PROMPT_COMENTARIO = (
    "Você é um tradutor especializado em literatura teológica clássica. "
    "Traduza o comentário bíblico a seguir do inglês para português brasileiro. "
    "Regras: (1) mantenha o tom erudito, mas em português natural e fluente, "
    "não literal demais; (2) citações bíblicas dentro do texto devem soar como "
    "a Almeida clássica; (3) preserve termos em grego/hebraico transliterados "
    "como estão; (4) não resuma, não omita, não acrescente nada; "
    "(5) responda APENAS com a tradução, sem preâmbulo nem comentários seus."
)
PROMPT_LEXICO = (
    "Traduza esta definição de léxico bíblico (dicionário de Strong) do inglês "
    "para português brasileiro. Mantenha o estilo telegráfico de dicionário, "
    "os separadores (; , ||) e termos transliterados como estão. "
    "Responda APENAS com a tradução."
)
PROMPT_GLOSA = (
    "Traduza esta glosa interlinear bíblica do inglês para português brasileiro. "
    "É a tradução literal de UMA palavra grega ou hebraica, então seja o mais "
    "curto e literal possível. Preserve colchetes [], sinais <> e barras / "
    "exatamente onde estão (indicam palavras implícitas ou marcadores "
    "gramaticais). Não explique. Responda APENAS com a glosa traduzida."
)

def prompt_para(entrada_id: str) -> str:
    if entrada_id.startswith("glosa-"):
        return PROMPT_GLOSA
    if entrada_id.startswith("strong-"):
        return PROMPT_LEXICO
    return PROMPT_COMENTARIO


def carregar_traducoes() -> dict:
    if Path(ARQ_SAIDA).exists():
        return json.loads(Path(ARQ_SAIDA).read_text(encoding="utf-8"))
    return {}


def enviar(caminho_entradas: str) -> None:
    cliente = anthropic.Anthropic()
    entradas = json.loads(Path(caminho_entradas).read_text(encoding="utf-8"))
    ja_feitas = set(carregar_traducoes().keys())

    pendentes = [e for e in entradas if e["id"] not in ja_feitas]
    print(f"{len(entradas)} entradas no arquivo; {len(pendentes)} ainda sem tradução.")
    if not pendentes:
        print("Nada a enviar.")
        return

    for bloco_i in range(0, len(pendentes), MAX_POR_LOTE):
        bloco = pendentes[bloco_i : bloco_i + MAX_POR_LOTE]
        requisicoes = [
            {
                "custom_id": e["id"],
                "params": {
                    "model": MODELO,
                    "max_tokens": MAX_TOKENS_SAIDA,
                    "system": prompt_para(e["id"]),
                    "messages": [{"role": "user", "content": e["texto"]}],
                },
            }
            for e in bloco
        ]
        lote = cliente.messages.batches.create(requests=requisicoes)
        with open(ARQ_PENDENTES, "a", encoding="utf-8") as f:
            f.write(lote.id + "\n")
        print(f"Lote enviado: {lote.id} ({len(bloco)} requisições)")

    print(
        "\nOs lotes são processados em até 24h (geralmente bem menos). "
        f"Depois rode: python {Path(__file__).name} baixar <batch_id>"
    )


def baixar(batch_id: str) -> None:
    cliente = anthropic.Anthropic()
    lote = cliente.messages.batches.retrieve(batch_id)
    if lote.processing_status != "ended":
        print(f"Lote {batch_id} ainda em processamento ({lote.processing_status}). "
              "Tente novamente mais tarde.")
        return

    traducoes = carregar_traducoes()
    ok, falhas = 0, 0
    for resultado in cliente.messages.batches.results(batch_id):
        if resultado.result.type == "succeeded":
            texto = "".join(
                b.text for b in resultado.result.message.content if b.type == "text"
            )
            traducoes[resultado.custom_id] = texto.strip()
            ok += 1
        else:
            falhas += 1
            print(f"  Falhou: {resultado.custom_id} ({resultado.result.type})")

    Path(ARQ_SAIDA).write_text(
        json.dumps(traducoes, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\n{ok} traduções salvas em {ARQ_SAIDA} ({falhas} falhas).")
    if falhas:
        print("Rode 'enviar' de novo para reenviar apenas as que falharam.")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Defina a variável de ambiente ANTHROPIC_API_KEY antes de rodar.")
    if len(sys.argv) < 3 or sys.argv[1] not in ("enviar", "baixar"):
        sys.exit(
            "Uso:\n"
            "  python traduzir_comentarios.py enviar entradas.json\n"
            "  python traduzir_comentarios.py baixar <batch_id>"
        )
    if sys.argv[1] == "enviar":
        enviar(sys.argv[2])
    else:
        baixar(sys.argv[2])
