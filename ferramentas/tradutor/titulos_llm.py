"""Títulos em português que faltam no Dicionário de Easton e nos Temas de Nave (data/{dictionary,topics}/titulos_pt.json).

Cerca de 2.200 verbetes do Easton e 3.000 temas do Nave não têm título em português e aparecem com o nome em inglês
("Ithamar", "Ahitub", "Rose"). Este script pede ao modelo só esses títulos, cada um com o começo do verbete já
traduzido (para saber se é pessoa, lugar ou coisa), e ACRESCENTA os que faltam: nunca troca um título que já existe.

Os nomes próprios propostos são conferidos contra o texto da Bíblia Livre (a grafia que o site usa): o relatório
mostra quais não aparecem lá, para revisão.

Chamada direta à API (são poucos milhares de títulos curtos; não precisa da Batch API), em grupos, com retomada.
Chave: ANTHROPIC_API_KEY no ambiente ou em ferramentas/tradutor/.env.

Uso:
  python ferramentas/tradutor/titulos_llm.py preparar                     # quantos faltam e custo estimado
  python ferramentas/tradutor/titulos_llm.py amostra [--n 80] [--modelo M] # relatório HTML, não grava nada em data/
  python ferramentas/tradutor/titulos_llm.py traduzir [--modelo M]        # todos (retoma de onde parou)
  python ferramentas/tradutor/titulos_llm.py aplicar                      # acrescenta nos titulos_pt.json
Depois de aplicar: python3 ferramentas/gerar_paginas.py (as páginas /dicionario/ e /temas/ usam os títulos).
"""
import argparse
import html
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA))
from calvino_llm import gravar_atomico, http_json, ler_json, obter_chave   # noqa: E402

DATA = PASTA.parent.parent / "data"
TRAB = PASTA / "trabalho"
SAIDA = TRAB / "titulos_llm_saida.json"
MODELO_PADRAO = "claude-sonnet-5-5"
PRECOS = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0)}
GRUPO = 100
TIPOS = {"dictionary": "Dicionário Bíblico de Easton", "topics": "Índice temático de Nave"}

PROMPT = """Você dá os títulos em português de verbetes de obras bíblicas clássicas (Dicionário de Easton e índice
temático de Nave) para um site gratuito de estudo bíblico. Cada item traz o título em inglês e o começo do verbete
já traduzido, só para você saber do que se trata.

Regras:
- Nome próprio (pessoa, lugar, povo): a grafia tradicional das Bíblias em português, a mesma da Bíblia Livre/Almeida
  ("Ithamar" -> "Itamar", "Ahitub" -> "Aitube", "Bath-sheba" -> "Bate-Seba", "Hezekiah" -> "Ezequias",
  "Kirjath-jearim" -> "Quiriate-Jearim"). Se o próprio verbete traduzido já usa uma forma portuguesa do nome, use-a.
  Quando o título tem uma variante entre parênteses ("BATH-SHEBA (BATHSHEBA)"), dê só o nome português.
- Palavra ou expressão comum: a tradução portuguesa usual em obras bíblicas ("Rose" -> "Rosa", "Ossifrage" ->
  "Quebrantosso", "Will" -> "Vontade", "Babbler" -> "Tagarela"). Plural ou singular como no original.
- Só a primeira letra maiúscula (e as dos nomes próprios), mesmo que o original esteja em MAIÚSCULAS.
- Curto: só o título, sem explicação, sem artigo inicial que o original não tenha, sem aspas.
- Responda SOMENTE com um objeto JSON {"id": "título em português", ...} com todos os ids recebidos."""


def faltando():
    """[(id, tipo, chave, contexto)] dos verbetes sem título em português"""
    itens = []
    for tipo in TIPOS:
        tit = ler_json(DATA / tipo / "titulos_pt.json")
        pt = {}
        for arq in sorted((DATA / tipo / "pt").glob("[A-Z].json")):
            pt.update({k: v for k, v in json.loads(arq.read_text(encoding="utf-8")).items() if k != "__pt"})
        for k in sorted(pt):
            if k in tit:
                continue
            ctx = re.sub(r"\s+", " ", " · ".join(x.lstrip("-").strip() for x in pt[k][:4]))[:240]
            itens.append((f"{tipo}|{k}", tipo, k, ctx))
    return itens


def mensagem(grupo):
    return json.dumps({i: {"obra": TIPOS[t], "titulo_en": k, "verbete": c} for i, t, k, c in grupo},
                      ensure_ascii=False, indent=0)


def pedir(modelo, chave, grupo):
    corpo = {"model": modelo, "max_tokens": 8192,
             "system": [{"type": "text", "text": PROMPT, "cache_control": {"type": "ephemeral"}}],
             "messages": [{"role": "user", "content": mensagem(grupo)}]}
    if "haiku-5" in modelo:
        corpo["thinking"] = {"type": "disabled"}
    else:
        corpo["output_config"] = {"effort": "low"}
    resp = http_json("https://api.anthropic.com/v1/messages", metodo="POST",
                     cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"}, corpo=corpo)
    txt = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt.strip())
    try:
        obj = json.loads(t[t.find("{"):t.rfind("}") + 1])
    except (json.JSONDecodeError, ValueError):
        obj = {}
    return obj, resp.get("usage", {})


# ---------------- conferência ----------------
_PALAVRAS_BL = set()


def palavras_bl():
    if not _PALAVRAS_BL:
        for arq in (DATA / "bibles" / "blivre").glob("*.json"):
            for cap in json.loads(arq.read_text(encoding="utf-8")):
                for v in cap:
                    _PALAVRAS_BL.update(re.findall(r"[A-ZÀ-Ú][\wÀ-ÿ'-]*", v or ""))
    return _PALAVRAS_BL


INGLES = re.compile(r"\b(?:the|of|and|in|to|for|with|by|from|his|their)\b", re.I)


def avaliar(chave, titulo):
    """(titulo limpo, motivo de recusa ou "", nome confirmado na Bíblia Livre?)"""
    t = re.sub(r'^["“”\']+|["“”\']+$', "", (titulo or "").strip()).strip()
    if not t:
        return t, "vazio", False
    if len(t) > max(40, int(len(chave) * 2.5)):
        return t, "longo demais", False
    if INGLES.search(t):
        return t, "inglês", False
    nomes = [w for w in re.findall(r"[A-ZÀ-Ú][\wÀ-ÿ'-]*", t) if len(w) > 2]
    confirmado = bool(nomes) and all(w in palavras_bl() or w.split("-")[0] in palavras_bl() for w in nomes)
    return t, "", confirmado


# ---------------- comandos ----------------
def cmd_preparar(a):
    itens = faltando()
    ent = sum(len(mensagem([x])) for x in itens) / 3.4
    sai = len(itens) * 12
    print(f"[preparar] {len(itens):,} títulos faltando: " +
          ", ".join(f"{TIPOS[t]} {n:,}" for t, n in Counter(x[1] for x in itens).items()))
    for m, (pe, ps) in PRECOS.items():
        print(f"  {m}: ~{ent / 1e6:.2f} M tokens de entrada, ~{sai / 1e6:.2f} M de saída, ~US$ {(ent * pe + sai * ps) / 1e6:.2f}")


def traduzir(itens, modelo, chave, est):
    uso = Counter()
    pendentes = [x for x in itens if x[0] not in est["titulos"]]
    for i in range(0, len(pendentes), GRUPO):
        grupo = pendentes[i:i + GRUPO]
        obj, u = pedir(modelo, chave, grupo)
        uso.update({k: v for k, v in u.items() if isinstance(v, int)})
        for id_, tipo, k, _ in grupo:
            t, motivo, conf = avaliar(k, obj.get(id_) if isinstance(obj.get(id_), str) else "")
            if motivo:
                est["recusas"][id_] = {"titulo": t, "motivo": motivo}
            else:
                est["titulos"][id_] = {"titulo": t, "confirmado": conf, "modelo": modelo}
                est["recusas"].pop(id_, None)
        print(f"  {min(i + GRUPO, len(pendentes))}/{len(pendentes)}", flush=True)
        gravar_atomico(SAIDA, est, indent=None)
    entrada = uso["input_tokens"] + uso["cache_read_input_tokens"] + uso["cache_creation_input_tokens"]
    pe, ps = PRECOS.get(modelo, (0, 0))
    return (entrada * pe + uso["output_tokens"] * ps) / 1e6


def relatorio(itens, est, caminho, gasto, modelo):
    linhas = []
    for id_, tipo, k, ctx in itens:
        r = est["titulos"].get(id_)
        if r:
            marca = "" if r["confirmado"] else "<span class='p'>não aparece na Bíblia Livre</span>"
            novo = f"<b>{html.escape(r['titulo'])}</b> {marca}"
        else:
            rc = est["recusas"].get(id_, {})
            novo = f"<span class='p'>recusado ({html.escape(rc.get('motivo', '?'))}): {html.escape(rc.get('titulo', ''))}</span>"
        linhas.append(f"<tr><td>{html.escape(TIPOS[tipo].split()[-1])}</td><td>{html.escape(k)}</td><td>{novo}</td>"
                      f"<td><small>{html.escape(ctx)}</small></td></tr>")
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Títulos: amostra</title>
<style>body{{font:14px/1.5 system-ui,sans-serif;margin:16px;background:#fbf8f1;color:#222}}table{{border-collapse:collapse}}
td{{border:1px solid #d8cfbd;padding:5px 8px;vertical-align:top}}.p{{color:#a00;font-size:12px}}</style></head><body>
<h1>Títulos em português — {html.escape(modelo)}</h1><p>{len(itens)} títulos; gasto US$ {gasto:.3f}.</p>
<table><tr><th>Obra</th><th>Inglês</th><th>Português</th><th>Começo do verbete</th></tr>{''.join(linhas)}</table></body></html>"""
    caminho.write_text(doc, encoding="utf-8")


def cmd_amostra(a):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    itens = faltando()
    amostra = sorted(random.Random(5).sample(itens, min(a.n or 80, len(itens))))
    est = {"titulos": {}, "recusas": {}}
    global SAIDA
    SAIDA = TRAB / "titulos_llm_amostra.json"
    gasto = traduzir(amostra, modelo, chave, est)
    caminho = TRAB / "relatorio_titulos.html"
    relatorio(amostra, est, caminho, gasto, modelo)
    total = gasto * len(itens) / len(amostra)
    conf = sum(r["confirmado"] for r in est["titulos"].values())
    print(f"[amostra] {len(est['titulos'])} títulos ({conf} nomes confirmados na Bíblia Livre), {len(est['recusas'])} "
          f"recusados; gasto US$ {gasto:.3f}; todos ~US$ {total:.2f}")
    print(f"[amostra] relatório: {caminho}")


def cmd_traduzir(a):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    itens = faltando()
    est = ler_json(SAIDA, {"titulos": {}, "recusas": {}})
    gasto = traduzir(itens, modelo, chave, est)
    relatorio(itens, est, TRAB / "relatorio_titulos.html", gasto, modelo)
    print(f"[traduzir] {len(est['titulos']):,} títulos, {len(est['recusas'])} recusados; gasto US$ {gasto:.2f}")
    print(f"  recusas: {dict(Counter(r['motivo'] for r in est['recusas'].values()))}")


def cmd_aplicar(a):
    est = ler_json(SAIDA, {"titulos": {}})
    novos = Counter()
    for tipo in TIPOS:
        arq = DATA / tipo / "titulos_pt.json"
        tit = ler_json(arq)
        for id_, r in est["titulos"].items():
            t, k = id_.split("|", 1)
            if t == tipo and k not in tit:          # nunca troca um título que já existe
                tit[k] = r["titulo"]
                novos[tipo] += 1
        arq.write_text(json.dumps(dict(sorted(tit.items())), ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"[aplicar] títulos acrescentados: {dict(novos)}")
    print("  agora rode: python3 ferramentas/gerar_paginas.py")


def main():
    ap = argparse.ArgumentParser(description="Títulos em português que faltam no Easton e no Nave")
    ap.add_argument("acao", choices=["preparar", "amostra", "traduzir", "aplicar"])
    ap.add_argument("--modelo", default=None)
    ap.add_argument("--chave", default=None)
    ap.add_argument("--n", type=int, default=0)
    a = ap.parse_args()
    {"preparar": cmd_preparar, "amostra": cmd_amostra, "traduzir": cmd_traduzir, "aplicar": cmd_aplicar}[a.acao](a)


if __name__ == "__main__":
    main()
