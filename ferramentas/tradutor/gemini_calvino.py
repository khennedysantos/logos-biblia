"""Retraduz pelo Gemini (API do Google, cota gratuita) os livros de Calvino que estão com a tradução provisória do NLLB.

Os livros são os do campo "provisorio" de data/commentaries/calvin/manifest.json (Salmos, 1 e 2 Timóteo, Tito, Zacarias e
Malaquias). Cada versículo vai com as mesmas regras de tradução do calvino_llm.py (PROMPT_SISTEMA: citações bíblicas
traduzidas das palavras do próprio Calvino, nunca da ARA; grego, hebraico e latim intactos; sem Markdown).

A cota gratuita limita PEDIDOS por dia (na 1ª execução, só ~20 no gemini-3-flash-preview), não o tamanho de cada um:
por isso os versículos vão em lotes de até ~24 mil caracteres num pedido só (um objeto JSON {chave: texto}, e a resposta
volta no mesmo formato), e quando a cota do dia de um modelo acaba o script passa ao seguinte de MODELOS (cada modelo tem
cota própria). Versículo que falha no lote é refeito sozinho; versículo maior que o lote vai em pedaços entre parágrafos.

Cada resposta passa pelas checagens (validar): tamanho perto do inglês, o número do versículo no começo, o grego e o
hebraico preservados, sem inglês sobrando e sem marcação. Se falhar, tenta de novo (outro modelo na 2ª vez); se falhar
sempre, o versículo fica com a tradução antiga e entra na lista de recusados.

Roda devagar, para caber na cota gratuita: espera entre pedidos, respeita o "tente de novo em N s" do Google e, quando a
cota do dia acaba (ou o tempo dado em --minutos), grava o que fez e sai; a próxima execução continua de onde parou.
O que já foi feito fica em ferramentas/tradutor/entradas/gemini_calvino_feitos.json (só as chaves), e as traduções vão
direto para data/commentaries/calvin/pt/<LIVRO>/<cap>.json. Quando um livro termina inteiro, ele sai do "provisorio".

uso:  GEMINI_API_KEY=... python3 ferramentas/tradutor/gemini_calvino.py [--livros PSA,1TI] [--minutos 330] [--max N]
      python3 ferramentas/tradutor/gemini_calvino.py --situacao        (quanto falta, sem chamar a API)
Roda sozinho no GitHub Actions: .github/workflows/traduzir-gemini.yml (o secret GEMINI_API_KEY guarda a chave)."""
import argparse, json, os, re, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from calvino_llm import PROMPT_SISTEMA                    # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]
CALVINO = RAIZ / "data" / "commentaries" / "calvin"
FEITOS = Path(__file__).resolve().parent / "entradas" / "gemini_calvino_feitos.json"
MODELOS = ["gemini-3-flash-preview", "gemini-3.5-flash", "gemini-3.8-flash"]
LOTE = 24000             # caracteres de inglês por pedido (a resposta cabe folgada no limite de saída do modelo)
PEDACO = LOTE
INTERVALO = 7            # segundos entre pedidos (a cota gratuita limita pedidos por minuto)
# erros que o modelo comete às vezes e que dá para consertar sem perguntar de novo
CORRECOES = [(re.compile(r"\bmalmente\b"), "mal"), (re.compile(r"\bMalmente\b"), "Mal")]
GREGO_HEBRAICO = re.compile(r"[Ͱ-Ͽἀ-῿֐-׿]+")
INGLES = re.compile(r"\b(the|and|which|that|of|is|with|from|this|they|were|have|been|shall|unto)\b", re.I)


class CotaDoDia(Exception):
    pass


ESGOTADOS = set()        # modelos cuja cota do dia já acabou nesta execução
PEDIDOS = {}             # pedidos aceitos pelo Google, por modelo

INSTRUCAO_LOTE = ("Traduza cada texto do objeto JSON abaixo seguindo todas as regras. Responda SOMENTE com um objeto JSON "
                  "com exatamente as mesmas chaves, em que cada valor é a tradução completa do texto daquela chave (texto "
                  "puro; parágrafos separados por linha em branco, como no original).\n\n")


def ler(p, padrao):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return padrao


def gravar(p, dados, compacto=True):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    txt = json.dumps(dados, ensure_ascii=False, separators=(",", ":")) if compacto else json.dumps(dados, ensure_ascii=False, indent=0)
    Path(p).write_text(txt, encoding="utf-8")


def pedacos(texto):
    """corta entre parágrafos em blocos de até PEDACO caracteres (um parágrafo maior que isso vai sozinho)"""
    blocos, atual = [], ""
    for par in texto.split("\n\n"):
        if atual and len(atual) + len(par) + 2 > PEDACO:
            blocos.append(atual); atual = par
        else:
            atual = f"{atual}\n\n{par}" if atual else par
    if atual:
        blocos.append(atual)
    return blocos


def pedir(texto, modelo, chave, em_json=False):
    config = {"temperature": 0.2}
    if em_json:
        config["responseMimeType"] = "application/json"
    corpo = json.dumps({"systemInstruction": {"parts": [{"text": PROMPT_SISTEMA}]},
                        "contents": [{"parts": [{"text": texto}]}],
                        "generationConfig": config}).encode()
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
                                 data=corpo, headers={"Content-Type": "application/json", "x-goog-api-key": chave})
    for tentativa in range(6):
        try:
            r = json.load(urllib.request.urlopen(req, timeout=480))
            PEDIDOS[modelo] = PEDIDOS.get(modelo, 0) + 1
            partes = r.get("candidates", [{}])[0].get("content", {}).get("parts", [])
            return "".join(p.get("text", "") for p in partes).strip()
        except urllib.error.HTTPError as e:
            erro = json.loads(e.read().decode() or "{}").get("error", {})
            msg = erro.get("message", "")
            if e.code == 429:
                if re.search(r"per ?day|PerDay|daily", json.dumps(erro), re.I):
                    raise CotaDoDia(msg[:200])
                espera = 60
                for d in erro.get("details", []):
                    m = re.match(r"(\d+)", str(d.get("retryDelay", "")))
                    if m:
                        espera = int(m.group(1)) + 2
                print(f"    limite por minuto: espera {espera}s")
                time.sleep(espera)
            elif e.code in (500, 502, 503, 504):
                time.sleep(20 * (tentativa + 1))
            else:
                raise RuntimeError(f"HTTP {e.code}: {msg[:200]}")
        except (TimeoutError, OSError) as e:
            print(f"    {type(e).__name__}: tenta de novo")
            time.sleep(15)
    return None


def validar(en, pt):
    """lista de problemas (vazia = aceita)"""
    if not pt:
        return ["resposta vazia"]
    prob = []
    razao = len(pt) / max(1, len(en))
    if not 0.8 <= razao <= 1.5:
        prob.append(f"tamanho {razao:.2f} do inglês")
    num_en = re.match(r"\s*(\d+(?:\s*[-,]\s*\d+)*)\s*\.", en)
    if num_en and not pt.lstrip().startswith(num_en.group(1)):
        prob.append("perdeu o número do versículo")
    falta = [w for w in set(GREGO_HEBRAICO.findall(en)) if len(w) > 2 and w not in pt]
    if len(falta) > max(1, len(set(GREGO_HEBRAICO.findall(en))) // 5):
        prob.append(f"grego/hebraico alterado: {falta[:3]}")
    palavras = len(pt.split())
    if palavras > 40 and len(INGLES.findall(pt)) / palavras > 0.03:
        prob.append("inglês sobrando")
    if re.search(r"\*\*|^#+ |Aqui está|tradução:", pt, re.M):
        prob.append("marcação ou comentário do modelo")
    return prob


def corrigir(pt):
    for rx, novo in CORRECOES:
        pt = rx.sub(novo, pt)
    return pt


def chamar(texto, chave, em_json=False, outro=False):
    """pede ao primeiro modelo com cota (ou ao segundo, se outro=True); sem cota em nenhum, CotaDoDia"""
    while True:
        livres = [m for m in MODELOS if m not in ESGOTADOS]
        if not livres:
            raise CotaDoDia("todos os modelos")
        modelo = livres[1] if outro and len(livres) > 1 else livres[0]
        try:
            resposta = pedir(texto, modelo, chave, em_json)
            time.sleep(INTERVALO)
            return resposta
        except CotaDoDia as e:
            ESGOTADOS.add(modelo)
            print(f"    cota do dia do {modelo} acabou ({str(e)[:60]}…); passa ao próximo modelo")


def traduzir_lote(itens, chave):
    """itens: [(uid, inglês)] -> {uid: português} só dos que passaram na validação"""
    resposta = chamar(INSTRUCAO_LOTE + json.dumps(dict(itens), ensure_ascii=False, indent=0), chave, em_json=True)
    try:
        dados = json.loads(resposta or "{}")
    except json.JSONDecodeError:
        dados = {}
    certos = {}
    for uid, en in itens:
        pt = dados.get(uid) if isinstance(dados, dict) else None
        if isinstance(pt, str):
            pt = corrigir(pt.strip())
            if not validar(en, pt):
                certos[uid] = pt
    return certos


def traduzir_verso(en, chave):
    """tradução inteira do versículo ou (None, motivos)"""
    saida = []
    for bloco in pedacos(en):
        pt, motivos = None, []
        for tentativa in range(3):
            resposta = chamar(bloco, chave, outro=(tentativa == 1))
            resposta = corrigir(resposta) if resposta else resposta
            motivos = validar(bloco, resposta)
            if not motivos:
                pt = resposta
                break
        if pt is None:
            return None, motivos
        saida.append(pt)
    return "\n\n".join(saida), []


def unidades(livros):
    for livro in livros:
        caps = sorted((int(p.stem) for p in (CALVINO / livro).glob("*.json")))
        for c in caps:
            en = ler(CALVINO / livro / f"{c}.json", {})
            for v in sorted(en, key=lambda k: int(k) if k.isdigit() else 0):
                yield livro, c, v, en[v]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--livros", default="")
    ap.add_argument("--minutos", type=float, default=330)
    ap.add_argument("--max", type=int, default=0, help="no máximo N versículos nesta execução (teste)")
    ap.add_argument("--situacao", action="store_true")
    a = ap.parse_args()
    manifesto = ler(CALVINO / "manifest.json", {})
    livros = [x for x in a.livros.split(",") if x] or list(manifesto.get("provisorio", []))
    feitos = ler(FEITOS, {"feitos": [], "recusados": {}})
    ja = set(feitos["feitos"])
    todas = list(unidades(livros))
    faltam = [u for u in todas if f"{u[0]}|{u[1]}|{u[2]}" not in ja]
    car = sum(len(u[3]) for u in faltam)
    print(f"{len(todas) - len(faltam)} de {len(todas)} versículos feitos; faltam {len(faltam)} ({car / 1e6:.2f} milhões de caracteres)")
    if a.situacao:
        return
    chave = os.environ.get("GEMINI_API_KEY", "").strip()
    if not chave:
        sys.exit("falta a variável GEMINI_API_KEY")
    fim = time.time() + a.minutos * 60
    feitos_agora = 0

    def guardar(livro, c, v, en, pt, motivos):
        nonlocal feitos_agora
        uid = f"{livro}|{c}|{v}"
        if pt is None:
            feitos["recusados"][uid] = motivos
            print(f"  {uid}: recusado ({'; '.join(motivos)}), fica a tradução antiga")
        else:
            arq = CALVINO / "pt" / livro / f"{c}.json"
            dados = ler(arq, {})
            dados[v] = pt
            dados["__pt"] = True
            gravar(arq, dados)
            feitos["recusados"].pop(uid, None)
            print(f"  {uid}: ok ({len(en)} → {len(pt)} caracteres)")
        feitos["feitos"].append(uid)
        feitos_agora += 1

    try:
        i = 0
        while i < len(faltam):
            if time.time() > fim or (a.max and feitos_agora >= a.max):
                print("tempo (ou --max) esgotado: continua na próxima execução")
                break
            # lote: versículos seguidos até LOTE caracteres (um versículo maior vai sozinho, em pedaços)
            lote, tam = [], 0
            while i < len(faltam) and (not lote or tam + len(faltam[i][3]) <= LOTE) \
                    and not (a.max and feitos_agora + len(lote) >= a.max):
                lote.append(faltam[i]); tam += len(faltam[i][3]); i += 1
                if tam > LOTE:
                    break
            if len(lote) == 1:
                livro, c, v, en = lote[0]
                guardar(livro, c, v, en, *traduzir_verso(en, chave))
            else:
                certos = traduzir_lote([(f"{l}|{c}|{v}", en) for l, c, v, en in lote], chave)
                for livro, c, v, en in lote:
                    uid = f"{livro}|{c}|{v}"
                    if uid in certos:
                        guardar(livro, c, v, en, certos[uid], [])
                    else:            # falhou no lote: refaz sozinho
                        guardar(livro, c, v, en, *traduzir_verso(en, chave))
            gravar(FEITOS, feitos, compacto=False)
    except CotaDoDia as e:
        print(f"cota do dia esgotada ({e}); continua amanhã")
    finally:
        gravar(FEITOS, feitos, compacto=False)
    # livro inteiro feito (sem recusados) sai da lista de provisórios
    ja = set(feitos["feitos"])
    prontos = [l for l in livros if all(f"{u[0]}|{u[1]}|{u[2]}" in ja for u in todas if u[0] == l)
               and not any(r.startswith(l + "|") for r in feitos["recusados"])]
    if prontos and manifesto.get("provisorio"):
        manifesto["provisorio"] = [l for l in manifesto["provisorio"] if l not in prontos]
        (CALVINO / "manifest.json").write_text(json.dumps(manifesto, ensure_ascii=False), encoding="utf-8")
        print("saem do provisório:", ", ".join(prontos))
    print(f"nesta execução: {feitos_agora} versículos em {sum(PEDIDOS.values())} pedidos {PEDIDOS}; "
          f"recusados até agora: {len(feitos['recusados'])}")


if __name__ == "__main__":
    main()
