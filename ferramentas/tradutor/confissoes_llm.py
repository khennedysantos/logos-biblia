"""Tradução para o português dos símbolos de fé em data/confissoes/ (Confissão e Catecismos de Westminster, Cânones de
Dort), a partir do inglês do século XVII em domínio público. Tradução própria (automática, com aviso no site): não
reproduz nenhuma tradução portuguesa publicada, que tem direitos autorais.

Cada trecho vai ao modelo com os marcadores dos textos de prova ("[1]", "[2]"…), que precisam voltar nos mesmos
lugares; a tradução é recusada se faltar ou sobrar marcador, se ficar inglês ou se o tamanho destoar.

Chamada direta à API (são ~240 mil caracteres), em grupos, com retomada. Chave: ANTHROPIC_API_KEY (ambiente ou .env).
Uso:
  python ferramentas/tradutor/confissoes_llm.py preparar               # quantos trechos e custo estimado
  python ferramentas/tradutor/confissoes_llm.py amostra [--modelo M]   # Confissão cap. 1 e 11, Breve Catecismo 1-12
  python ferramentas/tradutor/confissoes_llm.py traduzir [--modelo M]  # tudo (retoma de onde parou)
  python ferramentas/tradutor/confissoes_llm.py aplicar                # grava os campos em português em data/confissoes/
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

PASTA = Path(__file__).resolve().parent
sys.path.insert(0, str(PASTA))
from calvino_llm import gravar_atomico, http_json, ler_json, obter_chave, pos_processar   # noqa: E402

DADOS = PASTA.parent.parent / "data" / "confissoes"
TRAB = PASTA / "trabalho"
SAIDA = TRAB / "confissoes_llm_saida.json"
MODELO_PADRAO = "claude-sonnet-5-5"
PRECOS = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.0, 10.0), "claude-opus-5-5": (4.0, 20.0)}
GRUPO_MAX = 7000

PROMPT = """Você traduz para o português do Brasil os símbolos de fé reformados — a Confissão de Fé de Westminster, o
Catecismo Maior e o Breve Catecismo de Westminster (1647) e os Cânones de Dort (1619) — a partir do texto inglês
antigo, de domínio público, para um site gratuito de estudo bíblico.

- Faça uma tradução PRÓPRIA, fiel e completa, frase por frase, sem resumir, omitir nem acrescentar. Não reproduza
  nenhuma tradução portuguesa publicada (têm direitos autorais): traduza você mesmo, a partir do inglês.
- Registro formal e reverente, em português atual e claro, no vocabulário teológico reformado consagrado em português:
  "covenant" = pacto (pacto das obras, pacto da graça), "justification" = justificação, "adoption" = adoção,
  "sanctification" = santificação, "effectual calling" = vocação eficaz, "decree" = decreto, "elect" = eleitos,
  "reprobate" = réprobos, "means of grace" = meios de graça, "sacrament" = sacramento, "Lord's Supper" = Ceia do
  Senhor, "the Lord's day" = dia do Senhor, "Christian Sabbath" = sábado cristão, "Godhead" = Divindade,
  "providence" = providência, "perseverance of the saints" = perseverança dos santos, "satisfaction" = satisfação.
- Inglês arcaico ("calleth", "doth", "thee") vira português atual; "he" referido a Deus ou a Cristo: "ele".
- Marcadores de textos de prova como [1], [2], [3]: copie CADA UM exatamente, no mesmo ponto da frase (logo depois da
  palavra ou pontuação onde estão no inglês). Não crie nem apague marcadores.
- Citações bíblicas dentro do texto (comuns nos Cânones de Dort): traduza-as das palavras inglesas dadas; nunca as
  substitua por uma Bíblia pronta (ARA, NAA, NVI etc. têm direitos). Referências em formato português: "(Rom. 3:19)"
  -> "(Rm 3:19)", "1 Cor. 2:14" -> "1Co 2:14".
- Títulos de capítulo ("Of Justification") viram "Da Justificação"; perguntas de catecismo continuam perguntas.
- Responda SOMENTE com um objeto JSON com as mesmas chaves e cada texto traduzido."""


def trechos():
    """[(id, texto inglês)] de todos os documentos"""
    saida = []
    for arq in sorted(DADOS.glob("*.json")):
        doc = json.loads(arq.read_text(encoding="utf-8"))
        d = doc["id"]
        for parte in doc.get("partes", []):
            if parte.get("titulo_en"):
                saida.append((f"{d}|{parte['n']}|titulo", parte["titulo_en"]))
            saida += [(f"{d}|{parte['n']}|{it['n']}", it["en"]) for it in parte["itens"]]
        for it in doc.get("itens", []):
            saida += [(f"{d}|{it['n']}|p", it["p_en"]), (f"{d}|{it['n']}|r", it["r_en"])]
    return saida


def grupos(lista):
    saida, atual, tam = [], [], 0
    for t in lista:
        if atual and tam + len(t[1]) > GRUPO_MAX:
            saida.append(atual)
            atual, tam = [], 0
        atual.append(t)
        tam += len(t[1])
    return saida + ([atual] if atual else [])


RE_MARCA = re.compile(r"\[\d+\]")
INGLES = re.compile(r"\b(?:the|of|and|which|that|unto|thereof|whereby|shall|hath|doth|his|their)\b")


def problemas(en, pt):
    if not pt.strip():
        return ["vazio"]
    p = []
    if Counter(RE_MARCA.findall(en)) != Counter(RE_MARCA.findall(pt)):
        p.append("marcadores de prova")
    sem_aspas = re.sub(r"[“\"][^”\"]*[”\"]", " ", pt)
    if len(INGLES.findall(sem_aspas)) >= 3:
        p.append("inglês")
    r = len(pt) / max(1, len(en))
    if len(en) > 120 and not 0.75 <= r <= 1.8:
        p.append(f"tamanho ({len(pt)} x {len(en)})")
    return p


def pedir(modelo, chave, grupo):
    corpo = {"model": modelo, "max_tokens": 16000,
             "system": [{"type": "text", "text": PROMPT, "cache_control": {"type": "ephemeral"}}],
             "messages": [{"role": "user", "content": json.dumps(dict(grupo), ensure_ascii=False, indent=0)}]}
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


def traduzir(lista, modelo, chave, est, arq_saida):
    uso = Counter()
    pendentes = [x for x in lista if x[0] not in est["pt"]]
    for g in grupos(pendentes):
        obj, u = pedir(modelo, chave, g)
        uso.update({k: v for k, v in u.items() if isinstance(v, int)})
        for id_, en in g:
            pt = pos_processar(obj.get(id_, "")) if isinstance(obj.get(id_), str) else ""
            pr = problemas(en, pt)
            if pr:
                est["recusas"][id_] = {"pt": pt, "motivos": pr}
            else:
                est["pt"][id_] = pt
                est["recusas"].pop(id_, None)
        print(f"  {len(est['pt'])} prontos, {len(est['recusas'])} recusados", flush=True)
        gravar_atomico(arq_saida, est, indent=None)
    entrada = uso["input_tokens"] + uso["cache_read_input_tokens"] + uso["cache_creation_input_tokens"]
    pe, ps = PRECOS.get(modelo, (0, 0))
    return (entrada * pe + uso["output_tokens"] * ps) / 1e6


def cmd_preparar(a):
    lista = trechos()
    chars = sum(len(t) for _, t in lista)
    print(f"[preparar] {len(lista)} trechos, {chars:,} caracteres, {len(grupos(lista))} pedidos")
    for m, (pe, ps) in PRECOS.items():
        ent, sai = chars / 3.4 + len(grupos(lista)) * 300, chars * 1.15 / 3.2
        print(f"  {m}: ~US$ {(ent * pe + sai * ps) / 1e6:.2f}")


def cmd_amostra(a):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    lista = [x for x in trechos() if re.match(r"westminster\|(1|11)\||breve-catecismo\|([1-9]|1[0-2])\||canones-de-dort\|1\|(titulo|A1|A7|R1)$", x[0])]
    est = {"pt": {}, "recusas": {}}
    gasto = traduzir(lista, modelo, chave, est, TRAB / "confissoes_llm_amostra.json")
    linhas = [f"## {i}\nEN: {en}\nPT: {est['pt'].get(i) or est['recusas'].get(i)}\n" for i, en in lista]
    (TRAB / "relatorio_confissoes.txt").write_text("\n".join(linhas), encoding="utf-8")
    total = gasto * sum(len(t) for _, t in trechos()) / max(1, sum(len(t) for _, t in lista))
    print(f"[amostra] {len(est['pt'])} trechos, {len(est['recusas'])} recusados; gasto US$ {gasto:.3f}; tudo ~US$ {total:.2f}")
    print(f"[amostra] relatório: {TRAB / 'relatorio_confissoes.txt'}")


def cmd_traduzir(a):
    modelo, chave = a.modelo or MODELO_PADRAO, obter_chave("anthropic", a.chave)
    est = ler_json(SAIDA, {"pt": {}, "recusas": {}})
    gasto = traduzir(trechos(), modelo, chave, est, SAIDA)
    if est["recusas"]:                                   # uma segunda tentativa, um por vez
        for id_, en in [x for x in trechos() if x[0] in est["recusas"]]:
            gasto += traduzir([(id_, en)], modelo, chave, est, SAIDA)
    print(f"[traduzir] {len(est['pt'])} prontos, {len(est['recusas'])} recusados {list(est['recusas'])[:10]}; gasto US$ {gasto:.2f}")


def cmd_aplicar(a):
    est = ler_json(SAIDA, {"pt": {}})
    pt, n = est["pt"], 0
    for arq in sorted(DADOS.glob("*.json")):
        doc = json.loads(arq.read_text(encoding="utf-8"))
        d = doc["id"]
        for parte in doc.get("partes", []):
            if f"{d}|{parte['n']}|titulo" in pt:
                parte["titulo"] = pt[f"{d}|{parte['n']}|titulo"]
            for it in parte["itens"]:
                if f"{d}|{parte['n']}|{it['n']}" in pt:
                    it["pt"] = pt[f"{d}|{parte['n']}|{it['n']}"]
                    n += 1
        for it in doc.get("itens", []):
            it["p"] = pt.get(f"{d}|{it['n']}|p", it.get("p", ""))
            it["r"] = pt.get(f"{d}|{it['n']}|r", it.get("r", ""))
            n += bool(it["r"])
        arq.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[aplicar] {n} trechos em português gravados em data/confissoes/")
    print("  agora rode: python3 ferramentas/gerar_doutrinas.py && python3 ferramentas/gerar_paginas.py")


def main():
    ap = argparse.ArgumentParser(description="Tradução dos símbolos de fé (data/confissoes/)")
    ap.add_argument("acao", choices=["preparar", "amostra", "traduzir", "aplicar"])
    ap.add_argument("--modelo", default=None)
    ap.add_argument("--chave", default=None)
    a = ap.parse_args()
    {"preparar": cmd_preparar, "amostra": cmd_amostra, "traduzir": cmd_traduzir, "aplicar": cmd_aplicar}[a.acao](a)


if __name__ == "__main__":
    main()
