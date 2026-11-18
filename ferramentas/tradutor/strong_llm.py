"""Nova tradução do léxico de Strong (data/strongs/{G,H}.json) via LLM: amostra comparativa + Batch API.

A tradução atual (`defpt`) é do Argos e tropeça no vocabulário do próprio Strong: "properly" virou "corretamente",
"(subject.)" virou "(sujeito)", "i.e." virou "ou seja.", referências como "G1614 (ἐκτείνω)" perderam a palavra
grega, e os nomes próprios ficaram na grafia inglesa ("Beth-Lebaoth", "Ziphron").

Este script segue o mesmo molde de calvino_llm.py (e usa as funções HTTP dele, só biblioteca padrão):
  - manda as entradas em grupos de 25 (lema, transliteração, definição inglesa, usos da KJV e, quando existe,
    o nome na grafia da Bíblia Livre tirado de ferramentas/nomes_pt.json);
  - pede de volta, para cada entrada, `defpt` (a definição) e `usopt` (a lista de usos da KJV em português);
  - confere cada resposta (referências G/H e palavras gregas/hebraicas preservadas, nada de inglês sobrando,
    tamanho razoável) e só aceita as que passam.
Nada é gravado em data/ antes do `aplicar`; o `aplicar` substitui `defpt` (o antigo fica no histórico do git)
e acrescenta `usopt`. As traduções recusadas mantêm o `defpt` atual e vão para a lista do relatório.

Chave: ANTHROPIC_API_KEY no ambiente ou em ferramentas/tradutor/.env (o mesmo arquivo do calvino_llm.py).

Uso:
  python ferramentas/tradutor/strong_llm.py amostra [--modelo claude-sonnet-5-5]   # ~45 entradas difíceis, síncrono
      -> ferramentas/tradutor/trabalho/relatorio_strong.html (inglês × atual × novo)
  python ferramentas/tradutor/strong_llm.py preparar
  python ferramentas/tradutor/strong_llm.py enviar [--modelo claude-sonnet-5-5]     # Batch API, 50% de desconto
  python ferramentas/tradutor/strong_llm.py status
  python ferramentas/tradutor/strong_llm.py baixar
  python ferramentas/tradutor/strong_llm.py reenviar                               # grupos com falha, de novo
  python ferramentas/tradutor/strong_llm.py aplicar [--conferir]
"""
import argparse
import html
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calvino_llm import gravar_atomico, http_json, http_texto, ler_json, obter_chave   # noqa: E402

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parent.parent
STRONGS = RAIZ / "data" / "strongs"
NOMES = RAIZ / "ferramentas" / "nomes_pt.json"
TRABALHO = PASTA / "trabalho"
ARQ_GRUPOS = TRABALHO / "strong_v2_grupos.json"
ARQ_SAIDA = TRABALHO / "strong_v2_pt.json"
ARQ_LOTES = TRABALHO / "lotes_strong_v2.json"
ARQ_AMOSTRA = TRABALHO / "strong_amostra_pt.json"
ARQ_RELATORIO = TRABALHO / "relatorio_strong.html"
MODELO_PADRAO = "claude-sonnet-5-5"
POR_GRUPO = 25

PROMPT = """Você traduz para o português brasileiro o léxico de Strong (Strong's Exhaustive Concordance, 1890), \
dicionário de domínio público das palavras hebraicas, aramaicas e gregas da Bíblia, para um site gratuito de estudo \
bíblico de linha reformada. Cada entrada traz o lema original, a transliteração, a definição inglesa ("en") e a lista \
de palavras com que a King James traduz o termo ("kjv"). Às vezes vem também "nome_pt": a grafia do nome próprio na \
Bíblia Livre, que é a tradução usada no site.

Para cada entrada devolva:
- "defpt": a definição traduzida, fiel e completa, no estilo seco de dicionário do original. Não resuma, não explique, \
não acrescente nada, não omita nenhuma acepção.
- "usopt": a lista "kjv" em português, como palavras ou expressões curtas separadas por vírgula, na ordem do original, \
sem repetir sinônimos idênticos. Tire as marcas [idiom], [phrase], [obj.] e as remissões "Compare H3050 (...)"; \
mantenha os parênteses que indicam variação ("(fore-) father" -> "pai, antepassado").

Convenções do Strong (siga sempre):
- "properly" = "propriamente"; "i.e." = "isto é,"; "e.g." = "por exemplo,"; "by implication" = "por implicação"; \
"by extension" = "por extensão"; "figuratively" = "figuradamente"; "literally" = "literalmente"; "especially" = \
"especialmente"; "abstractly"/"abstract" = "abstratamente"; "concretely" = "concretamente"; "(subject.)" = \
"(subjetivamente)"; "(object.)" = "(objetivamente)"; "(genitive case)" = "(caso genitivo)"; "(as noun)" = \
"(como substantivo)"; "(adverbially)" = "(adverbialmente)"; "a primitive root" = "raiz primitiva"; \
"a primary verb" = "verbo primário"; "from" no começo de etimologia = "de"; "compare" = "compare".
- Copie exatamente, sem traduzir nem mudar: números de Strong (G906, H3050), palavras gregas e hebraicas, \
e chaves {} quando houver.
- Nomes próprios: use "nome_pt" quando vier. Sem ele, use a grafia tradicional das Bíblias em português \
(Almeida/Bíblia Livre): "Beth-lebaoth" -> "Bete-Lebaote", "Jehoshaphat" -> "Josafá", "Dioscuri" -> "Dióscuros". \
"Jehovah" -> "Jeová". "a place in Palestine" -> "um lugar na Palestina"; "an Israelite" -> "um israelita".
- Termos teológicos com o vocabulário clássico protestante: "righteousness" = "justiça", "atonement" = "expiação", \
"grace" = "graça", "sanctify" = "santificar", "propitiation" = "propiciação", "elect" = "eleito".
- Português brasileiro culto, sem artigos desnecessários no começo ("an ox" -> "boi"), sem aspas a mais.

Responda somente com um objeto JSON no formato {"G1016": {"defpt": "...", "usopt": "..."}, ...}, com todas as \
entradas recebidas e nada mais."""

# entradas difíceis para a amostra: as mais usadas e teológicas, remissões, nomes, gramática e as mais longas
AMOSTRA = ["H1", "H430", "H3068", "H5315", "H7307", "H2617", "H6662", "H3722", "H1285", "H1932", "H853", "H2202",
           "H1034", "H3091", "H4872", "H6944", "H8451", "H539", "G26", "G3056", "G4102", "G5485", "G1343", "G1344",
           "G2435", "G4151", "G1577", "G907", "G4496", "G164", "G1359", "G2424", "G5547", "G4561", "G3341", "G1588",
           "G2222", "G1515", "G266", "G3875"]


def carregar_lexico():
    lex = {}
    for letra in "GH":
        for k, e in json.loads((STRONGS / f"{letra}.json").read_text(encoding="utf-8")).items():
            lex[k] = e
    return lex


def ordem(k):
    return (k[0], int(re.sub(r"\D", "", k) or 0), k)


def entrada(k, e, nomes):
    item = {"id": k, "lema": e.get("lemma", ""), "translit": e.get("translit", ""), "en": e.get("def", ""),
            "kjv": e.get("kjv", "")}
    if k in nomes and nomes[k][1]:
        item["nome_pt"] = nomes[k][1]
    return item


def mensagem(itens):
    return json.dumps(itens, ensure_ascii=False, indent=0)


def payload(modelo, itens):
    tam = len(mensagem(itens))
    corpo = {"model": modelo, "max_tokens": max(8192, min(32000, int(tam * 1.6) + 4096)),
             "system": [{"type": "text", "text": PROMPT, "cache_control": {"type": "ephemeral"}}],
             "messages": [{"role": "user", "content": mensagem(itens)}]}
    m = modelo.lower()
    if "haiku-5" in m:
        corpo["thinking"] = {"type": "disabled"}
    else:
        corpo["output_config"] = {"effort": "low"}
    return corpo


def extrair_json(txt):
    """o objeto JSON da resposta (tolera ```json e texto em volta)"""
    txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt.strip())
    ini, fim = txt.find("{"), txt.rfind("}")
    if ini < 0 or fim < 0:
        return {}
    try:
        obj = json.loads(txt[ini:fim + 1])
    except json.JSONDecodeError:
        return {}
    return obj if isinstance(obj, dict) else {}


# ---------------- validação ----------------
RE_REF = re.compile(r"\b[GH]\d+\b")
RE_ORIG = re.compile(r"[Ͱ-Ͽἀ-῿֐-׿][Ͱ-Ͽἀ-῿֐-׿̀-ͯ'’-]*")
INGLES = re.compile(r"\b(?:the|of|and|which|properly|especially|figuratively|implication|i\.e|place in|from|to be|"
                    r"or|with|that|by|is|it)\b")


def problemas(en, pt):
    """lista de motivos para recusar a tradução de uma definição"""
    if not pt or not pt.strip():
        return ["vazia"]
    p = []
    faltam = [r for r in set(RE_REF.findall(en)) if r not in pt]
    if faltam:
        p.append("referência perdida: " + ", ".join(sorted(faltam)))
    orig = [w for w in set(RE_ORIG.findall(en)) if len(w) > 1 and w not in pt]
    if orig:
        p.append("palavra original alterada: " + " ".join(sorted(orig)))
    sem_orig = RE_ORIG.sub(" ", RE_REF.sub(" ", pt))
    ingl = INGLES.findall(sem_orig)
    if len(ingl) >= 2:
        p.append("inglês na tradução: " + ", ".join(ingl[:4]))
    if len(en) > 40 and not 0.55 <= len(pt) / len(en) <= 2.6:
        p.append(f"tamanho suspeito ({len(pt)} x {len(en)} caracteres)")
    return p


# ---------------- amostra ----------------
def traduzir_sincrono(modelo, chave, itens):
    resp = http_json("https://api.anthropic.com/v1/messages", metodo="POST",
                     cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"}, corpo=payload(modelo, itens))
    if resp.get("stop_reason") == "max_tokens":
        print("  aviso: resposta cortada por max_tokens")
    txt = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
    uso = resp.get("usage", {})
    return extrair_json(txt), uso


def cmd_amostra(args):
    modelo = args.modelo or MODELO_PADRAO
    chave = obter_chave("anthropic", args.chave)
    lex, nomes = carregar_lexico(), ler_json(NOMES)
    salvos = ler_json(ARQ_AMOSTRA, {})
    feitos = salvos.setdefault(modelo, {})
    pend = [k for k in AMOSTRA if k in lex and (args.refazer or k not in feitos)]
    entrada_tok = saida_tok = 0
    for i in range(0, len(pend), 10):
        bloco = pend[i:i + 10]
        print(f"[amostra] {modelo}: {', '.join(bloco)}", flush=True)
        obj, uso = traduzir_sincrono(modelo, chave, [entrada(k, lex[k], nomes) for k in bloco])
        entrada_tok += uso.get("input_tokens", 0) + uso.get("cache_read_input_tokens", 0) + uso.get("cache_creation_input_tokens", 0)
        saida_tok += uso.get("output_tokens", 0)
        for k in bloco:
            if k in obj:
                feitos[k] = obj[k]
        gravar_atomico(ARQ_AMOSTRA, salvos)
    if pend:
        print(f"[amostra] tokens: entrada {entrada_tok:,}, saída {saida_tok:,}")
    relatorio(lex, salvos)


def relatorio(lex, salvos):
    modelos = list(salvos)
    linhas = []
    for k in AMOSTRA:
        if k not in lex:
            continue
        e = lex[k]
        cel = [f"<td><b>{k}</b><br><span class='o'>{html.escape(e.get('lemma', ''))}</span><br>"
               f"<i>{html.escape(e.get('translit', ''))}</i></td>",
               f"<td>{html.escape(e.get('def', ''))}<div class='k'>KJV: {html.escape(e.get('kjv', ''))}</div></td>",
               f"<td>{html.escape(e.get('defpt', ''))}</td>"]
        for m in modelos:
            n = salvos[m].get(k) or {}
            pr = problemas(e.get("def", ""), n.get("defpt", ""))
            aviso = f"<div class='p'>{html.escape('; '.join(pr))}</div>" if pr else ""
            cel.append(f"<td>{html.escape(n.get('defpt', '—'))}<div class='k'>Usos: {html.escape(n.get('usopt', ''))}</div>{aviso}</td>")
        linhas.append("<tr>" + "".join(cel) + "</tr>")
    cab = "".join(f"<th>Novo — {html.escape(m)}</th>" for m in modelos)
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Strong: amostra</title>
<style>body{{font:14px/1.45 system-ui,sans-serif;margin:16px;background:#fbf8f1;color:#222}}
table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #d8cfbd;padding:6px 8px;vertical-align:top}}
th{{background:#efe6d3;position:sticky;top:0}}.o{{font-size:18px}}.k{{color:#666;font-size:12px;margin-top:4px}}
.p{{color:#a00;font-size:12px;margin-top:4px}}</style></head><body>
<h1>Léxico de Strong — amostra ({len(linhas)} entradas)</h1>
<table><tr><th>Strong</th><th>Inglês (original)</th><th>Atual (Argos)</th>{cab}</tr>{''.join(linhas)}</table></body></html>"""
    ARQ_RELATORIO.parent.mkdir(parents=True, exist_ok=True)
    ARQ_RELATORIO.write_text(doc, encoding="utf-8")
    print(f"[amostra] relatório: {ARQ_RELATORIO}")


# ---------------- lote ----------------
def cmd_preparar(args):
    lex, nomes = carregar_lexico(), ler_json(NOMES)
    chaves = sorted(lex, key=ordem)
    grupos = {}
    for i in range(0, len(chaves), POR_GRUPO):
        bloco = chaves[i:i + POR_GRUPO]
        grupos[f"{bloco[0]}-{bloco[-1]}"] = [entrada(k, lex[k], nomes) for k in bloco]
    gravar_atomico(ARQ_GRUPOS, grupos, indent=None)
    tam = sum(len(mensagem(g)) for g in grupos.values())
    print(f"[preparar] {len(chaves):,} entradas em {len(grupos)} grupos ({tam:,} caracteres) -> {ARQ_GRUPOS}")


def pendentes(grupos, saida, lotes):
    em_lote = {c for lt in lotes if not lt.get("baixado") and lt.get("status") not in ("canceled", "expired")
               for c in lt["cids"]}
    feitos = saida.get("entradas", {})
    return [cid for cid, itens in grupos.items()
            if cid not in em_lote and any(it["id"] not in feitos for it in itens)]


def enviar(args, so_falhas=False):
    modelo = args.modelo or MODELO_PADRAO
    chave = obter_chave("anthropic", args.chave)
    grupos = ler_json(ARQ_GRUPOS)
    if not grupos:
        sys.exit("Rode 'preparar' primeiro.")
    saida, lotes = ler_json(ARQ_SAIDA, {"entradas": {}}), ler_json(ARQ_LOTES, [])
    pend = pendentes(grupos, saida, lotes)
    if args.limite:
        pend = pend[:args.limite]
    print(f"[enviar] {len(pend)} grupos a enviar ({len(saida.get('entradas', {})):,} entradas já prontas).")
    if not pend:
        return
    reqs = []
    for cid in pend:
        itens = grupos[cid]
        if so_falhas:
            itens = [it for it in itens if it["id"] not in saida.get("entradas", {})]
        reqs.append({"custom_id": cid, "params": payload(modelo, itens)})
    resp = http_json("https://api.anthropic.com/v1/messages/batches", metodo="POST",
                     cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"}, corpo={"requests": reqs})
    lotes.append({"id": resp["id"], "modelo": modelo, "criado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "qtd": len(reqs),
                  "status": resp.get("processing_status", "in_progress"), "baixado": False, "cids": pend})
    gravar_atomico(ARQ_LOTES, lotes)
    print(f"  lote {resp['id']} enviado ({len(reqs)} grupos). Acompanhe com 'status'.")


def cmd_status(args):
    lotes = ler_json(ARQ_LOTES, [])
    chave = obter_chave("anthropic", args.chave)
    for lt in lotes:
        info = http_json(f"https://api.anthropic.com/v1/messages/batches/{lt['id']}",
                         cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"})
        lt["status"] = info.get("processing_status", "?")
        c = info.get("request_counts", {})
        print(f"  {lt['id']} ({lt['modelo']}): {lt['status']} | ok={c.get('succeeded', 0)} proc={c.get('processing', 0)} "
              f"erro={c.get('errored', 0)} | baixado={lt.get('baixado')}")
    gravar_atomico(ARQ_LOTES, lotes)


def cmd_baixar(args):
    lotes, saida = ler_json(ARQ_LOTES, []), ler_json(ARQ_SAIDA, {"entradas": {}})
    grupos, lex = ler_json(ARQ_GRUPOS), carregar_lexico()
    ent = saida.setdefault("entradas", {})
    recusas = saida.setdefault("recusas", {})
    chave = obter_chave("anthropic", args.chave)
    novos = 0
    for lt in lotes:
        if lt.get("baixado"):
            continue
        cab = {"x-api-key": chave, "anthropic-version": "2023-06-01"}
        info = http_json(f"https://api.anthropic.com/v1/messages/batches/{lt['id']}", cabecalhos=cab)
        if info.get("processing_status") != "ended":
            print(f"  {lt['id']}: ainda em '{info.get('processing_status')}'.")
            continue
        bruto = http_texto(info.get("results_url") or f"https://api.anthropic.com/v1/messages/batches/{lt['id']}/results", cab)
        for linha in bruto.splitlines():
            if not linha.strip():
                continue
            obj = json.loads(linha)
            res = obj.get("result", {})
            if res.get("type") != "succeeded" or res["message"].get("stop_reason") == "max_tokens":
                continue
            txt = "".join(b.get("text", "") for b in res["message"].get("content", []) if b.get("type") == "text")
            resposta = extrair_json(txt)
            for it in grupos.get(obj["custom_id"], []):
                n = resposta.get(it["id"])
                if not isinstance(n, dict):
                    continue
                pr = problemas(lex[it["id"]].get("def", ""), n.get("defpt", ""))
                if pr:
                    recusas[it["id"]] = {"novo": n, "motivos": pr}
                else:
                    ent[it["id"]] = {"defpt": n.get("defpt", "").strip(), "usopt": (n.get("usopt") or "").strip()}
                    recusas.pop(it["id"], None)
                    novos += 1
        lt["baixado"] = True
        saida["modelo"] = lt["modelo"]
        gravar_atomico(ARQ_SAIDA, saida, indent=None)
        gravar_atomico(ARQ_LOTES, lotes)
    print(f"[baixar] +{novos:,} entradas aceitas; total {len(ent):,} de {len(lex):,}; {len(recusas)} recusadas.")


def cmd_aplicar(args):
    saida = ler_json(ARQ_SAIDA, {"entradas": {}})
    ent = saida.get("entradas", {})
    if not ent:
        sys.exit("Nada baixado ainda.")
    total = 0
    for letra in "GH":
        arq = STRONGS / f"{letra}.json"
        dados = json.loads(arq.read_text(encoding="utf-8"))
        for k, e in dados.items():
            n = ent.get(k)
            if n and n["defpt"] and not problemas(e.get("def", ""), n["defpt"]):
                total += e.get("defpt") != n["defpt"]
                e["defpt"] = n["defpt"]
                if n.get("usopt"):
                    e["usopt"] = n["usopt"]
        if not args.conferir:
            arq.write_text(json.dumps(dados, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    recusas = saida.get("recusas", {})
    print(f"[aplicar] {total:,} definições {'mudariam' if args.conferir else 'atualizadas'}; "
          f"{len(recusas)} recusadas ficam com a tradução atual.")
    for k, r in list(recusas.items())[:30]:
        print(f"   {k}: {'; '.join(r['motivos'])}")


def main():
    ap = argparse.ArgumentParser(description="Nova tradução do léxico de Strong (amostra + Batch API)")
    sub = ap.add_subparsers(dest="acao", required=True)
    for nome in ("amostra", "enviar", "reenviar"):
        p = sub.add_parser(nome)
        p.add_argument("--modelo", default=None, help=f"padrão: {MODELO_PADRAO}")
        p.add_argument("--chave", default=None)
        p.add_argument("--limite", type=int, default=0)
        if nome == "amostra":
            p.add_argument("--refazer", action="store_true")
    sub.add_parser("preparar")
    for nome in ("status", "baixar"):
        sub.add_parser(nome).add_argument("--chave", default=None)
    sub.add_parser("aplicar").add_argument("--conferir", action="store_true")
    sub.add_parser("relatorio")
    args = ap.parse_args()
    if args.acao == "amostra":
        cmd_amostra(args)
    elif args.acao == "relatorio":
        relatorio(carregar_lexico(), ler_json(ARQ_AMOSTRA, {}))
    elif args.acao == "preparar":
        cmd_preparar(args)
    elif args.acao == "enviar":
        enviar(args)
    elif args.acao == "reenviar":
        enviar(args, so_falhas=True)
    elif args.acao == "status":
        cmd_status(args)
    elif args.acao == "baixar":
        cmd_baixar(args)
    elif args.acao == "aplicar":
        cmd_aplicar(args)


if __name__ == "__main__":
    main()
