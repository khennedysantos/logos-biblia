"""Traduz pelo Gemini (cota gratuita) as obras dos Pais da Igreja em data/pais/<obra>.json (importadas por
ferramentas/pais_ccel.py): primeiro os títulos dos capítulos e os resumos dos livros, num pedido só, depois as seções,
em lotes de até ~24 mil caracteres por pedido (o mesmo esquema do gemini_calvino.py, de onde vêm pedir/chamar, a troca
de modelo quando a cota do dia acaba e os limites de pedidos).

Cada seção traduzida precisa manter os mesmos marcadores [n] das citações bíblicas do inglês, o tamanho perto do
original e nada de inglês sobrando ou de Markdown; senão vai sozinha mais duas vezes e, falhando sempre, fica na lista
de recusados (ferramentas/tradutor/entradas/gemini_pais_feitos.json) sem tradução. O que falta é o que não tem "pt":
a próxima execução continua de onde parou.

uso:  GEMINI_API_KEY=... python3 ferramentas/tradutor/gemini_pais.py [--obras agostinho-confissoes] [--minutos 60]
      python3 ferramentas/tradutor/gemini_pais.py --situacao
Roda no GitHub Actions antes do Calvino (.github/workflows/traduzir-gemini.yml)."""
import argparse, json, os, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gemini_calvino as gc                               # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
PAIS = RAIZ / "data" / "pais"
FEITOS = Path(__file__).resolve().parent / "entradas" / "gemini_pais_feitos.json"
MARCA = re.compile(r"\[(\d+)\]")

PROMPT_PAIS = """Você é um tradutor erudito de patrística, traduzindo para o português brasileiro culto, natural e fiel as obras dos Pais da Igreja a partir de traduções inglesas do século XIX em domínio público (Nicene and Post-Nicene Fathers, de Philip Schaff). O texto agora é das Confissões de Agostinho de Hipona.

Regras inegociáveis:

1. FIDELIDADE E INTEGRIDADE: traduza tudo, frase por frase, sem resumir, sem omitir nem acrescentar. Mantenha o tom de oração e louvor de Agostinho, as perguntas retóricas, as repetições e as antíteses, e a mesma divisão em parágrafos.

2. TRATAMENTO DE DEUS: quando Agostinho fala com Deus ("Thou", "Thee", "Thy"), use a segunda pessoa do singular com maiúscula: "Tu", "Te", "Ti", "Teu", "Tua" ("Grande és Tu, Senhor"; "fizeste-nos para Ti"). Os verbos concordam na 2ª pessoa ("Tu és", "Tu nos moves"). Para pessoas, use o tratamento natural do contexto.

3. CITAÇÕES BÍBLICAS: traduza as citações a partir das palavras do inglês que está no texto (que segue o latim de Agostinho). NUNCA substitua por versões prontas com direitos (Almeida Revista e Atualizada, NAA, NVI, NVT, NTLH).

4. MARCADORES DE CITAÇÃO: o texto tem marcadores como [1], [2] logo depois da citação bíblica a que se referem. Mantenha TODOS os marcadores, com os mesmos números, colados logo depois das palavras correspondentes na tradução. Não crie marcadores novos nem tire nenhum.

5. LATIM, GREGO E NOMES: preserve intactas as palavras e frases em latim ou grego que aparecem no texto. Use a forma portuguesa usual dos nomes próprios: Agostinho, Mônica, Ambrósio, Alípio, Adeodato, Patrício, Simpliciano, Ponticiano, Nebrídio, Fausto, Cartago, Milão, Roma, Tagaste, Óstia, Hipona, maniqueus, platônicos, Virgílio, Cícero, Hortênsio.

6. FORMATO: texto puro, sem Markdown (nada de ** ou #), parágrafos separados por linha em branco, aspas curvas (“ ”) e travessão (—). Responda SOMENTE com a tradução, sem notas nem comentários."""

INSTRUCAO_TITULOS = ("Traduza para o português os títulos e resumos do objeto JSON abaixo (são os títulos dos capítulos e os "
                     "resumos dos livros das Confissões de Agostinho; em títulos, use maiúscula só no começo e nos nomes "
                     "próprios, e ponha o verbo na 3ª pessoa: “Proclama a grandeza de Deus…”; os pronomes de 3ª pessoa ficam em "
                     "minúscula, mesmo quando o inglês escreve His/Him com maiúscula: “sua mãe”, “seus pecados”, "
                     "“despertado por ele”). Responda SOMENTE com um "
                     "objeto JSON com exatamente as mesmas chaves.\n\n")


def ler(p, padrao):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return padrao


def validar_secao(en, pt):
    prob = gc.validar(en, pt)
    if pt and sorted(MARCA.findall(en)) != sorted(MARCA.findall(pt)):
        prob.append("marcadores [n] diferentes do inglês")
    return prob


def traduzir_titulos(doc, chave):
    pedidos = {}
    for l in doc["livros"]:
        if not l.get("resumo"):
            pedidos[f"L{l['n']}"] = l["resumo_en"]
        for c in l["caps"]:
            if not c.get("titulo"):
                pedidos[f"{l['n']}.{c['n']}"] = c["titulo_en"]
    if not pedidos:
        return 0
    resposta = gc.chamar(INSTRUCAO_TITULOS + json.dumps(pedidos, ensure_ascii=False, indent=0), chave, em_json=True)
    try:
        dados = json.loads(resposta or "{}")
    except json.JSONDecodeError:
        dados = {}
    feitos = 0
    for l in doc["livros"]:
        r = dados.get(f"L{l['n']}")
        if isinstance(r, str) and r.strip() and not l.get("resumo"):
            l["resumo"] = r.strip(); feitos += 1
        for c in l["caps"]:
            t = dados.get(f"{l['n']}.{c['n']}")
            if isinstance(t, str) and t.strip() and not c.get("titulo"):
                c["titulo"] = t.strip().rstrip("."); feitos += 1
    return feitos


def traduzir_lote(itens, chave):
    """itens: [(uid, inglês)] -> {uid: português} só dos aprovados"""
    resposta = gc.chamar(gc.INSTRUCAO_LOTE + json.dumps(dict(itens), ensure_ascii=False, indent=0), chave, em_json=True)
    try:
        dados = json.loads(resposta or "{}")
    except json.JSONDecodeError:
        dados = {}
    certos = {}
    for uid, en in itens:
        pt = dados.get(uid) if isinstance(dados, dict) else None
        if isinstance(pt, str) and not validar_secao(en, pt.strip()):
            certos[uid] = pt.strip()
    return certos


def traduzir_sozinha(en, chave):
    motivos = []
    for tentativa in range(2):
        pt = gc.chamar(en, chave, outro=(tentativa == 1))
        pt = pt.strip() if pt else pt
        motivos = validar_secao(en, pt)
        if not motivos:
            return pt, []
    return None, motivos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--obras", default="")
    ap.add_argument("--minutos", type=float, default=60)
    ap.add_argument("--situacao", action="store_true")
    a = ap.parse_args()
    gc.SISTEMA = PROMPT_PAIS
    obras = [x for x in a.obras.split(",") if x] or sorted(p.stem for p in PAIS.glob("*.json"))
    feitos = ler(FEITOS, {"recusados": {}})
    docs = {o: ler(PAIS / f"{o}.json", None) for o in obras}
    faltam = [(o, l["n"], c["n"], s) for o, d in docs.items() for l in d["livros"] for c in l["caps"] for s in c["secoes"]
              if not s.get("pt") and f"{o}|{l['n']}|{s['n']}" not in feitos["recusados"]]
    total = sum(len(c["secoes"]) for d in docs.values() for l in d["livros"] for c in l["caps"])
    print(f"Pais da Igreja: {total - len(faltam)} de {total} seções feitas ou recusadas; faltam {len(faltam)} "
          f"({sum(len(s['en']) for *_, s in faltam) / 1e3:.0f} mil caracteres)")
    if a.situacao or not faltam and all(c.get("titulo") for d in docs.values() for l in d["livros"] for c in l["caps"]):
        return
    chave = os.environ.get("GEMINI_API_KEY", "").strip()
    if not chave:
        sys.exit("falta a variável GEMINI_API_KEY")
    fim = time.time() + a.minutos * 60
    agora = 0

    def gravar():
        for o, d in docs.items():
            (PAIS / f"{o}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        FEITOS.write_text(json.dumps(feitos, ensure_ascii=False, indent=0), encoding="utf-8")

    try:
        for o, d in docs.items():
            n = traduzir_titulos(d, chave)
            if n:
                print(f"  {o}: {n} títulos e resumos traduzidos")
        i = 0
        while i < len(faltam) and time.time() < fim:
            lote, tam = [], 0
            while i < len(faltam) and (not lote or tam + len(faltam[i][3]["en"]) <= gc.LOTE):
                lote.append(faltam[i]); tam += len(faltam[i][3]["en"]); i += 1
            uids = {f"{o}|{l}|{s['n']}": (o, l, c, s) for o, l, c, s in lote}
            certos = traduzir_lote([(u, x[3]["en"]) for u, x in uids.items()], chave) if len(lote) > 1 else {}
            for u, (o, l, c, s) in uids.items():
                pt, motivos = (certos[u], []) if u in certos else traduzir_sozinha(s["en"], chave)
                if pt:
                    s["pt"] = pt
                    print(f"  {u}: ok ({len(s['en'])} → {len(pt)} caracteres)")
                else:
                    feitos["recusados"][u] = motivos
                    print(f"  {u}: recusada ({'; '.join(motivos)})")
                agora += 1
            gravar()
    except gc.CotaDoDia as e:
        print(f"cota do dia esgotada ({e}); continua amanhã")
    finally:
        gravar()
    print(f"nesta execução: {agora} seções em {sum(gc.PEDIDOS.values())} pedidos {gc.PEDIDOS}; "
          f"recusadas até agora: {len(feitos['recusados'])}")


if __name__ == "__main__":
    main()
