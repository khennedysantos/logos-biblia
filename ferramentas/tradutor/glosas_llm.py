"""Revisão das glosas do interlinear via LLM (Batch API da Anthropic), versículo por versículo.

As glosas são montadas palavra a palavra por regra (corrigir_glosas.py) e ainda escapam erros de sentido ("ἄρχων" =
"uma régua" em vez de "um líder"). Aqui cada versículo vai ao modelo com, para cada palavra, o Strong, a gramática, a
glosa inglesa da STEPBible e a glosa portuguesa atual, além do texto da Bíblia Livre como referência de sentido. O
modelo devolve SÓ as glosas que precisam mudar. As correções aceitas vão para ferramentas/glosas_llm.json
({"JHN|3|1|9": {"de": "uma régua", "para": "um líder"}}), versionado, que o corrigir_glosas.py aplica como último passo
(só onde a glosa atual ainda é a "de": idempotente e seguro se as regras mudarem depois).

Chave: ANTHROPIC_API_KEY no ambiente ou em ferramentas/tradutor/.env.

Uso:
  python ferramentas/tradutor/glosas_llm.py amostra [--n 40] [--modelo M]   # síncrono, relatório HTML
  python ferramentas/tradutor/glosas_llm.py preparar                        # mostra tamanho e custo
  python ferramentas/tradutor/glosas_llm.py enviar [--modelo M] [--limite N]
  python ferramentas/tradutor/glosas_llm.py status
  python ferramentas/tradutor/glosas_llm.py baixar
  python ferramentas/tradutor/glosas_llm.py aplicar   # grava ferramentas/glosas_llm.json e roda corrigir_glosas.py aplicar
"""
import argparse
import html
import json
import random
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

PASTA = Path(__file__).resolve().parent
FERR = PASTA.parent
sys.path.insert(0, str(PASTA))
sys.path.insert(0, str(FERR))
from calvino_llm import gravar_atomico, http_json, http_texto, ler_json, obter_chave    # noqa: E402
from stepbible import DATA, alinhar                                                     # noqa: E402

TRAB = PASTA / "trabalho"
SAIDA = TRAB / "glosas_llm_saida.json"
LOTES = TRAB / "glosas_llm_lotes.json"
FINAL = FERR / "glosas_llm.json"
MODELO_PADRAO = "claude-haiku-5-5"
PRECOS = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0)}
GRUPO_MAX = 7000

PROMPT = """Você revisa as glosas em português de um interlinear bíblico (hebraico no AT, grego no NT) de um site
gratuito de estudo bíblico. Cada palavra original tem uma glosa curta, palavra a palavra, que fica embaixo dela.
As glosas foram feitas por regra e tradução automática a partir das glosas inglesas da STEPBible (Tyndale House), e
algumas têm erro de SENTIDO (o inglês tinha outro sentido: "ruler" = governante/líder, não "régua"; "bowels" =
entranhas/compaixão; "meat" = comida; "quick" = vivo) ou de GRAMÁTICA grave (pessoa, número ou tempo verbal que não
batem com a análise gramatical; gênero do artigo/adjetivo que não bate com a palavra portuguesa).

Para cada versículo você recebe o texto da Bíblia Livre (só como referência de sentido e de grafia dos nomes) e, por
palavra: posição | Strong | gramática | glosa inglesa | glosa portuguesa atual.

Devolva SOMENTE um objeto JSON {"REF": {"posição": "glosa corrigida"}} com as glosas que estão ERRADAS — nunca
repita uma glosa que já está certa. A maioria dos versículos não tem erro nenhum e fica de fora; se nada estiver
errado, devolva {}. Não reescreva glosas corretas por gosto ou estilo, nem só para mexer no espaçamento.

Regras da glosa corrigida:
- Continua sendo glosa daquela palavra, curta e literal, no mesmo formato da atual — NÃO copie a frase da Bíblia
  Livre nem junte palavras vizinhas.
- Preserve as convenções: dois espaços separam as partes de uma palavra hebraica com prefixo/sufixo, como no inglês
  ("and  to  [the] house  his" -> "e  para  [a] casa  dele"); colchetes [ ] marcam palavra subentendida; < > marcam
  partícula sem tradução ("<obj.>") ou complemento; a pontuação final da glosa atual se mantém.
- Segunda pessoa do singular e do plural com "tu" e "vós" conjugados ("tu disseste", "vós ouvistes"), nunca "você".
- O nome divino YHWH é "SENHOR"; nomes próprios na grafia da Bíblia Livre.
- Português brasileiro, sem inglês."""


def refs_versos():
    """[(ref, livro, cap, v, texto_bl, [(i, palavra, lista_do_site)])] na ordem do cânon"""
    caps, palavras = alinhar()
    por_verso = defaultdict(list)
    for w, p in palavras:
        por_verso[(w.livro, w.cap, w.v)].append((w.i, w, p))
    livros = [b["id"] for b in ler_json(DATA / "books.json")["books"]]
    bl = {}
    saida = []
    for (livro, cap, v), ps in sorted(por_verso.items(), key=lambda k: (livros.index(k[0][0]) if k[0][0] in livros
                                                                      else 99, k[0][1], k[0][2])):
        if livro not in bl:
            bl[livro] = ler_json(DATA / "bibles" / "blivre" / f"{livro}.json", [])
        try:
            texto = bl[livro][cap - 1][v - 1]
        except IndexError:
            texto = ""
        saida.append((f"{livro} {cap}:{v}", livro, cap, v, texto, sorted(ps, key=lambda x: x[0])))
    return saida


def bloco_verso(ref, texto, ps):
    linhas = [f"## {ref}", f"BL: {texto}"]
    linhas += [f"{i} | {w.strong} | {w.gram} | {w.en} | {p[3]}" for i, w, p in ps]
    return "\n".join(linhas)


def grupos(versos):
    saida, atual, tam = [], [], 0
    for vs in versos:
        n = len(bloco_verso(vs[0], vs[4], vs[5]))
        if atual and tam + n > GRUPO_MAX:
            saida.append(atual)
            atual, tam = [], 0
        atual.append(vs)
        tam += n
    if atual:
        saida.append(atual)
    return [(f"g{i:05d}", g) for i, g in enumerate(saida)]


def payload(modelo, grupo):
    msg = "\n\n".join(bloco_verso(r, t, ps) for r, _, _, _, t, ps in grupo)
    corpo = {"model": modelo, "max_tokens": 8192,
             "system": [{"type": "text", "text": PROMPT, "cache_control": {"type": "ephemeral"}}],
             "messages": [{"role": "user", "content": msg}]}
    if "haiku-5" in modelo:
        corpo["thinking"] = {"type": "disabled"}
    else:
        corpo["output_config"] = {"effort": "low"}
    return corpo


# ---------------- leitura e validação das correções ----------------
INGLES = re.compile(r"\b(?:the|of|and|which|that|with|from|shall|unto|you|your|he|she|they|is|are|was|were|will|"
                    r"have|has|to|in|on|for|his|her|its|their|my|him|them|not|be)\b")
PONT = re.compile(r"[.,;:!?·]+$")


def avaliar(atual, nova, en):
    """(glosa final, motivo da recusa ou "")"""
    nova = re.sub(r"\s+$", "", nova.replace("\n", " "))
    if not nova.strip():
        return nova, "vazia"
    pa = PONT.search(atual)
    if pa and not PONT.search(nova):
        nova += pa.group(0)                                  # devolve a pontuação final da glosa atual
    if nova == atual or nova.split() == atual.split():     # só o espaçamento mudou
        return atual, "igual"
    if INGLES.search(nova.lower()) and not INGLES.search(atual.lower()):
        return nova, "inglês"
    if len(nova) > max(28, 3 * len(atual)):
        return nova, "longa demais"
    if ("<" in atual) != ("<" in nova) or ("[" in atual) != ("[" in nova):
        return nova, "marcação"
    if atual.count("  ") != nova.count("  ") and en.count("  ") == atual.count("  "):
        return nova, "partes"
    if "você" in nova.lower():
        return nova, "você"
    return nova, ""


def ler_resposta(txt):
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt.strip())
    ini, fim = t.find("{"), t.rfind("}")
    try:
        obj = json.loads(t[ini:fim + 1]) if ini >= 0 else None
    except json.JSONDecodeError:
        return None
    return obj if isinstance(obj, dict) else None


def registrar(grupo, obj, est, modelo):
    """Grava as correções aceitas/recusadas do grupo; devolve (aceitas, recusadas)"""
    ok = rec = 0
    por_ref = {r: (livro, cap, v, {str(i): (w, p) for i, w, p in ps}) for r, livro, cap, v, _, ps in grupo}
    for ref, corr in obj.items():
        if ref not in por_ref or not isinstance(corr, dict):
            continue
        livro, cap, v, mapa = por_ref[ref]
        corr = {i: g for i, g in corr.items() if str(i) in mapa and isinstance(g, str)
                and avaliar(mapa[str(i)][1][3], g, mapa[str(i)][0].en)[1] != "igual"}
        if len(corr) > max(4, 0.6 * len(mapa)):              # reescreveu o versículo inteiro: não é revisão
            for i in corr:
                est["recusas"][f"{livro}|{cap}|{v}|{i}"] = {"motivo": "versículo inteiro", "modelo": modelo}
            rec += len(corr)
            continue
        for i, nova in corr.items():
            if str(i) not in mapa or not isinstance(nova, str):
                continue
            w, p = mapa[str(i)]
            final, motivo = avaliar(p[3], nova, w.en)
            chave = f"{livro}|{cap}|{v}|{i}"
            if motivo == "igual":
                continue
            if motivo:
                est["recusas"][chave] = {"de": p[3], "para": final, "en": w.en, "motivo": motivo}
                rec += 1
            else:
                est["correcoes"][chave] = {"de": p[3], "para": final, "en": w.en, "gram": w.gram, "modelo": modelo}
                est["recusas"].pop(chave, None)
                ok += 1
    return ok, rec


# ---------------- comandos ----------------
def custo_estimado(versos, modelo):
    msg = sum(len(bloco_verso(r, t, ps)) for r, _, _, _, t, ps in versos)
    ent = msg / 3.2 + len(grupos(versos)) * len(PROMPT) / 3.6 * 0.1   # o prompt fica em cache
    sai = sum(len(ps) for *_, ps in versos) * 0.08 * 12 / 3.2         # ~8% das palavras corrigidas
    pe, ps_ = PRECOS.get(modelo, (0, 0))
    return ent, sai, (ent * pe + sai * ps_) / 1e6 * 0.5


def cmd_preparar(a):
    versos = refs_versos()
    print(f"[preparar] {len(versos):,} versículos, {sum(len(x[5]) for x in versos):,} palavras, "
          f"{len(grupos(versos)):,} pedidos")
    for m in PRECOS:
        e, s, c = custo_estimado(versos, m)
        print(f"  {m}: ~{e / 1e6:.1f} M tokens de entrada, ~{s / 1e6:.2f} M de saída, ~US$ {c:.2f} no lote")


def cmd_amostra(a):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    versos = refs_versos()
    rnd = random.Random(11)
    n = a.n or 40
    escolha = sorted(rnd.sample(range(len(versos)), n))
    amostra = [versos[i] for i in escolha]
    est = {"correcoes": {}, "recusas": {}}
    uso = Counter()
    for cid, g in grupos(amostra):
        resp = http_json("https://api.anthropic.com/v1/messages", metodo="POST",
                         cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"}, corpo=payload(modelo, g))
        uso.update({k: v for k, v in resp.get("usage", {}).items() if isinstance(v, int)})
        txt = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")
        obj = ler_resposta(txt)
        if obj is None:
            print(f"  {cid}: resposta ilegível")
            continue
        registrar(g, obj, est, modelo)
        print(f"  {cid}: {len(est['correcoes'])} correções até agora", flush=True)
    entrada = uso["input_tokens"] + uso["cache_read_input_tokens"] + uso["cache_creation_input_tokens"]
    pe, ps_ = PRECOS.get(modelo, (0, 0))
    gasto = (entrada * pe + uso["output_tokens"] * ps_) / 1e6
    fator = len(versos) / n
    linhas = []
    for r, livro, cap, v, texto, ps in amostra:
        cel = []
        for i, w, p in ps:
            k = f"{livro}|{cap}|{v}|{i}"
            if k in est["correcoes"]:
                cel.append(f"<span class='c' title='{html.escape(w.en)} · {w.gram}'>{html.escape(p[3])} → "
                           f"<b>{html.escape(est['correcoes'][k]['para'])}</b></span>")
            elif k in est["recusas"]:
                rc = est["recusas"][k]
                cel.append(f"<span class='r' title='{html.escape(rc['motivo'])}'>{html.escape(p[3])} ✗ "
                           f"{html.escape(rc.get('para', ''))}</span>")
            else:
                cel.append(f"<span title='{html.escape(w.en)}'>{html.escape(p[3])}</span>")
        linhas.append(f"<tr><td><b>{r}</b><br><small>{html.escape(texto)}</small></td><td>{' · '.join(cel)}</td></tr>")
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Glosas: amostra</title>
<style>body{{font:14px/1.6 system-ui,sans-serif;margin:16px;background:#fbf8f1;color:#222}}table{{border-collapse:collapse}}
td{{border:1px solid #d8cfbd;padding:6px 8px;vertical-align:top}}td:first-child{{width:30%}}
.c{{background:#e4f2dc}}.r{{background:#f8dcdc}}</style></head><body>
<h1>Glosas — amostra com {html.escape(modelo)}</h1>
<p>{n} versículos, {len(est['correcoes'])} correções aceitas (verde), {len(est['recusas'])} recusadas (vermelho; passe
o mouse para o motivo). Esta amostra: US$ {gasto:.3f}. Estimativa do lote completo (Batch API, 50% de desconto):
US$ {gasto * fator / 2:.2f}.</p><table>{''.join(linhas)}</table></body></html>"""
    saida = TRAB / "relatorio_glosas.html"
    saida.write_text(doc, encoding="utf-8")
    print(f"[amostra] {len(est['correcoes'])} correções, {len(est['recusas'])} recusadas; gasto US$ {gasto:.3f}; "
          f"lote completo ~US$ {gasto * fator / 2:.2f}")
    print(f"[amostra] relatório: {saida}")


def cmd_enviar(a):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    versos = refs_versos()
    est = ler_json(SAIDA, {"correcoes": {}, "recusas": {}, "feitos": []})
    lotes = ler_json(LOTES, [])
    feitos = set(est.get("feitos", [])) | {r for lt in lotes if not lt.get("baixado") for g in lt["grupos"].values()
                                           for r in g}
    gs = grupos([x for x in versos if x[0] not in feitos])
    if a.limite:
        gs = gs[:a.limite]
    print(f"[enviar] {sum(len(g) for _, g in gs):,} versículos em {len(gs):,} pedidos ({len(est.get('feitos', [])):,} já feitos)")
    for i in range(0, len(gs), 5000):
        bloco = gs[i:i + 5000]
        cid0 = len(lotes)
        resp = http_json("https://api.anthropic.com/v1/messages/batches", metodo="POST",
                         cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"},
                         corpo={"requests": [{"custom_id": f"l{cid0}{cid}", "params": payload(modelo, g)}
                                             for cid, g in bloco]})
        lotes.append({"id": resp["id"], "modelo": modelo, "criado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
                      "grupos": {f"l{cid0}{cid}": [x[0] for x in g] for cid, g in bloco}, "baixado": False})
        gravar_atomico(LOTES, lotes, indent=None)
        print(f"  lote {resp['id']}: {len(bloco)} pedidos")


def cmd_status(a):
    chave = obter_chave("anthropic", a.chave)
    for lt in ler_json(LOTES, []):
        info = http_json(f"https://api.anthropic.com/v1/messages/batches/{lt['id']}",
                         cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"})
        c = info.get("request_counts", {})
        print(f"  {lt['id']} ({lt['modelo']}): {info.get('processing_status')} | ok={c.get('succeeded', 0)} "
              f"proc={c.get('processing', 0)} erro={c.get('errored', 0)} | baixado={lt.get('baixado')}")


def cmd_baixar(a):
    chave = obter_chave("anthropic", a.chave)
    cab = {"x-api-key": chave, "anthropic-version": "2023-06-01"}
    por_ref = {x[0]: x for x in refs_versos()}
    est = ler_json(SAIDA, {"correcoes": {}, "recusas": {}, "feitos": []})
    feitos = set(est.get("feitos", []))
    lotes = ler_json(LOTES, [])
    ok = rec = 0
    for lt in lotes:
        if lt.get("baixado"):
            continue
        info = http_json(f"https://api.anthropic.com/v1/messages/batches/{lt['id']}", cabecalhos=cab)
        if info.get("processing_status") != "ended":
            print(f"  {lt['id']}: ainda em '{info.get('processing_status')}'")
            continue
        bruto = http_texto(info.get("results_url") or f"https://api.anthropic.com/v1/messages/batches/{lt['id']}/results", cab)
        for linha in bruto.splitlines():
            if not linha.strip():
                continue
            o = json.loads(linha)
            res = o.get("result", {})
            if res.get("type") != "succeeded" or res["message"].get("stop_reason") == "max_tokens":
                continue
            txt = "".join(b.get("text", "") for b in res["message"].get("content", []) if b.get("type") == "text")
            obj = ler_resposta(txt)
            if obj is None:
                continue
            grupo = [por_ref[r] for r in lt["grupos"].get(o["custom_id"], []) if r in por_ref]
            a_, r_ = registrar(grupo, obj, est, lt["modelo"])
            ok, rec = ok + a_, rec + r_
            feitos.update(x[0] for x in grupo)
        lt["baixado"] = True
        est["feitos"] = sorted(feitos)
        gravar_atomico(SAIDA, est, indent=None)
        gravar_atomico(LOTES, lotes, indent=None)
    print(f"[baixar] +{ok:,} correções, +{rec:,} recusadas; {len(feitos):,} versículos feitos de {len(por_ref):,}; "
          f"total {len(est['correcoes']):,} correções")
    print("  recusas:", dict(Counter(r["motivo"] for r in est["recusas"].values())))


def cmd_aplicar(a):
    est = ler_json(SAIDA, {"correcoes": {}})
    final = {k: {"de": c["de"], "para": c["para"]} for k, c in sorted(est["correcoes"].items())}
    gravar_atomico(FINAL, final, indent=0)
    print(f"[aplicar] {len(final):,} correções em {FINAL.relative_to(FERR.parent)}")
    subprocess.run([sys.executable, str(FERR / "corrigir_glosas.py"), "aplicar"], check=True)


def main():
    ap = argparse.ArgumentParser(description="Revisão das glosas do interlinear via LLM (Batch API)")
    ap.add_argument("acao", choices=["amostra", "preparar", "enviar", "status", "baixar", "aplicar"])
    ap.add_argument("--modelo", default=None)
    ap.add_argument("--chave", default=None)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--limite", type=int, default=0)
    a = ap.parse_args()
    {"amostra": cmd_amostra, "preparar": cmd_preparar, "enviar": cmd_enviar, "status": cmd_status,
     "baixar": cmd_baixar, "aplicar": cmd_aplicar}[a.acao](a)


if __name__ == "__main__":
    main()
