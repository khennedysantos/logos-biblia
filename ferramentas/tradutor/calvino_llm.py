"""Tradutor dos comentários de João Calvino via LLM (teste A/B + Batch API).

Regras de segurança deste script:
1. NUNCA altera os originais em inglês (data/commentaries/calvin/{USFM}/)
   nem sobrescreve a tradução atual em data/commentaries/calvin/pt/.
2. Toda saída final vai exclusivamente para data/commentaries/calvin/pt-v2/.
3. O prompt proíbe substituir citações bíblicas pela ARA (direitos da SBB)
   ou por qualquer tradução pronta: traduz fielmente a formulação do próprio Calvino.
4. Usa apenas a biblioteca padrão do Python 3 (roda direto no Windows 11 sem pip).

Configuração da chave de API (escolha uma):
  - Arquivo .env na raiz (ou ferramentas/tradutor/.env) com: ANTHROPIC_API_KEY=sk-ant-...
    (ou GEMINI_API_KEY=... / OPENAI_API_KEY=...)
  - PowerShell: $env:ANTHROPIC_API_KEY="sk-ant-..."
  - CMD:        set ANTHROPIC_API_KEY=sk-ant-...

Fluxo recomendado:
  1) Teste A/B nos 30 trechos difíceis (listas, latim/grego/hebraico, polêmica):
       python ferramentas/tradutor/calvino_llm.py amostra
     Gera ferramentas/tradutor/trabalho/relatorio_ab_calvino.html comparando
     Inglês × NLLB atual (pt/) × LLM novo (pt-v2).
     Para testar outros modelos da geração atual na mesma tabela:
       python ferramentas/tradutor/calvino_llm.py amostra --modelo claude-sonnet-5-5
       python ferramentas/tradutor/calvino_llm.py amostra --provedor gemini --modelo gemini-3.5-flash

  2) Tradução completa em lote (50% de desconto na Batch API — Anthropic e OpenAI):
       python ferramentas/tradutor/calvino_llm.py preparar
       python ferramentas/tradutor/calvino_llm.py enviar
       python ferramentas/tradutor/calvino_llm.py status
       python ferramentas/tradutor/calvino_llm.py baixar
       python ferramentas/tradutor/calvino_llm.py aplicar
     Obs.: no Gemini este script usa apenas o modo síncrono ('amostra' ou 'direto'),
     cobrado a preço cheio (sem Batch API).
"""
import argparse
import hashlib
import html
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

PASTA_SCRIPT = Path(__file__).resolve().parent
RAIZ = PASTA_SCRIPT.parent.parent
DATA = RAIZ / "data"
BASE_CALVINO = DATA / "commentaries" / "calvin"
DESTINO_PT_V2 = BASE_CALVINO / "pt-v2"
TRABALHO = PASTA_SCRIPT / "trabalho"
ARQ_AMOSTRA_META = PASTA_SCRIPT / "entradas" / "amostra_calvino_ab.json"
ARQ_AMOSTRA_SAIDA = TRABALHO / "amostra_ab_pt.json"
ARQ_RELATORIO_HTML = TRABALHO / "relatorio_ab_calvino.html"
ARQ_ENTRADAS_V2 = TRABALHO / "calvino_v2_entradas.json"
ARQ_SAIDA_V2 = TRABALHO / "calvino_v2_pt.json"
ARQ_LOTES_V2 = TRABALHO / "lotes_calvino_v2.json"

MODELOS_PADRAO = {
    "anthropic": "claude-haiku-5-5",
    "gemini": "gemini-3.5-flash",
    "openai": "gpt-6-luna",
}

VAR_CHAVE = {
    "anthropic": "ANTHROPIC_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "openai": "OPENAI_API_KEY",
}

MAX_CAR_PARTE = 9500  # fatia preleções muito longas em quebras de parágrafo para nunca truncar nem resumir

PROMPT_SISTEMA = """Você é um tradutor erudito especializado em teologia reformada clássica do século XVI, traduzindo os comentários bíblicos de João Calvino (edição inglesa da Calvin Translation Society) para o português brasileiro culto, natural, preciso e fiel.

Siga rigorosamente estas regras inegociáveis:

1. CITAÇÕES BÍBLICAS — PROIBIDO USAR A ARA OU TRADUÇÕES COM DIREITOS AUTORAIS:
   - NUNCA substitua as citações bíblicas do texto por versões prontas memorizadas (como Almeida Revista e Atualizada / ARA ou NAA da Sociedade Bíblica do Brasil, NVI, NVT ou NTLH).
   - Traduza toda citação bíblica DIRETAMENTE das palavras que Calvino escreveu no texto-fonte, preservando com exatidão as escolhas lexicais e sintáticas dele. Calvino traduzia diretamente do hebraico e do grego para o latim, e sua exegese logo em seguida depende das palavras exatas que ele usou (por exemplo: se ele escreveu "In the beginning was the Speech", traduza "No princípio era a Palavra" — jamais "o Verbo" nem "o Discurso"; se escreveu "Momentary lightness", traduza "Leveza momentânea"; se escreveu "I do not reject", traduza "Não rejeito").
   - Regra específica para "Speech" (o Sermo de Calvino para Λόγος, como em João 1): traduza "the Speech" como "a Palavra" (e não "o Discurso"). A concordância no feminino vale apenas para artigos e adjetivos ligados diretamente a "a Palavra" (ex.: "a Palavra eterna"); quando Calvino se refere ao Speech/Filho com pronomes pessoais (he, him, himself, his), mantenha o masculino ("ele", "dele", "si mesmo"), pois ele está tratando da pessoa de Cristo e da subsistência pessoal do Logos contra Serveto — e, se a frase ficar ambígua, prefira repetir "a Palavra" ou usar "o Filho" em vez do pronome. Exceção: nos trechos em que Calvino compara explicitamente Sermo com Verbum (ex.: João 1:1, "I wonder what induced the Latins to render ὁ λόγος by Verbum..."), mantenha os termos latinos e explique entre parênteses — Verbum (o Verbo, isto é, um vocábulo isolado) e Sermo (a Palavra, no sentido de fala/discurso) — para o argumento dele continuar fazendo sentido. NUNCA glose Verbum como "a Palavra": Verbum = o Verbo (vocábulo isolado); Sermo = a Palavra (fala/discurso). Exemplos obrigatórios de pronome: "he says that he was from the beginning" = "diz que ele existia desde o princípio"; "as if he did not exist before" = "como se ele não existisse antes"; "if he had not some kind of subsistence peculiar to himself" = "se ele não tivesse alguma espécie de subsistência própria" — nunca "ela" para a pessoa do Filho.

2. HEBRAICO, GREGO E LATIM INTACTOS:
   - Preserve exatamente como estão todos os vocábulos e caracteres em hebraico (ex.: תוהו, כפר, עלמה), grego politônico (ex.: Λόγος, προτίθεναι, ἱλαστήριον), transliterações entre parênteses e palavras/frases em latim citadas por Calvino (ex.: Sermo, Verbum, sacramentum, hoc est corpus meum, ex opere operato, liberum arbitrium, ac si diceret, citações da Vulgata, de Erasmo ou de Agostinho). Traduza apenas o texto inglês ao redor. Quando o texto traz um versículo em inglês seguido do mesmo versículo em latim (tradução latina do próprio Calvino, comum nos livros de Moisés), traduza o inglês e mantenha o bloco latino intacto logo depois — nunca o omita. Copie cada termo grego ou hebraico como aparece, sem transliterar nem trocar por "Jesus"/"Logos" em português (ex.: ᾿Ιησοῦς permanece ᾿Ιησοῦς).

3. LISTAS LONGAS, PONTUAÇÃO E INTEGRIDADE INTEGRAL:
   - NÃO resuma, não abrevie, não omita nenhuma oração, exemplo ou item de enumerações longas ("first... secondly... thirdly...", "(1.)", "I.", ou cadeias com ponto-e-vírgula).
   - Após ponto-e-vírgula (;), use letra minúscula em português (exceto nomes próprios), mantendo rigorosamente a concordância verbal e nominal até o fim de períodos extensos.

4. VOCABULÁRIO TEOLÓGICO REFORMADO E INGLÊS DO SÉCULO XIX:
   - Mantenha terminologia reformada clássica consistente: "the godly / pious" = os piedosos; "the faithful" = os fiéis; "the ungodly / wicked" = os ímpios; "covenant" = aliança; "propitiation" = propiciação; "mercy-seat" = propiciatório; "atonement / expiation" = expiação; "righteousness" = justiça; "imputation" = imputação; "free-will" = livre-arbítrio; "Papists" = papistas; "Sophists" = sofistas; "Schoolmen" = escolásticos; "Old Interpreter" = Antigo Intérprete (referência à Vulgata).
   - Atenção a falsos cognatos do inglês oitocentista: "solicitous" = preocupado / detido em minúcias (nunca "solicitante"); "subjoins" = acrescenta em seguida (nunca "subjunta"); "obtains" (intransitivo) = vigora / prevalece; "what he intends" = o que ele tem em vista / quer dizer.

5. FORMATO DE SAÍDA (TEXTO PURO):
   - Devolva APENAS texto puro, sem qualquer marcação Markdown (não use **negrito**, *itálico* com asteriscos nem cabeçalhos #), pois o site exibe o texto diretamente.
   - Preserve quebras de parágrafo existentes, use travessão (—) e aspas curvas (“ ”), e traduza os nomes de livros bíblicos nas referências para o português (ex.: Romanos 8:1, 1 Coríntios 11:24, Salmo 22:16).
   - Responda SOMENTE com a tradução, sem notas do tradutor, sem preâmbulo e sem comentários extras."""


# Número de versículo no início ("16. " ou "1, 2. ") fica fora da tradução e volta intacto ao aplicar
NUM_VERSO = re.compile(r"^\s*\d+(?:\s*[-,]\s*\d+)*\s*[\.:]?\s*")

# Apêndices e índices de fim de volume da edição CCEL que vieram colados ao último versículo de 40 arquivos
RE_CCEL_CAUDA = re.compile(
    r"\s*(?:"
    r"END OF (?:THE )?(?:COMMENTAR(?:Y|IES)|EPISTLE|BOOK|VOLUME|FIFTH|FOURTH|THIRD|SECOND|FIRST)\b.*|"
    r"End [Oo]f (?:the )?[Cc]ommentar(?:y|ies) on [A-Z].*|"
    r"End Of Volume [A-Z].*|"
    r"A [Tt][Rr]?[Aa][Nn][Ss][Ll][Aa][Tt][Ii][Oo][Nn] (?:of|OF) [Cc][Aa][Ll][Vv][Ii][Nn][’\x27][sS] [Vv][Ee][Rr][Ss][Ii][Oo][Nn] (?:of|OF)\b.*|"
    r"The (?:addenda to [A-Za-z]+|translation(?: of [A-Za-z0-9 —–-]+)?) (?:is|are) located here\..*|"
    r"(?<=[.!?\s])(?:Genesis|Exodus|Leviticus) \d+(?::\d+)? \d+(?::\d+)? \d+:\d+.*"
    r")$",
    re.S,
)

ERROS_OCR = [
    (re.compile(r"\bfiom\b"), "from"),
    (re.compile(r"\bSpirit The\b"), "Spirit. The"),
]

# Fórmulas típicas da ARA (SBB) ou desvios lexicais que indicam substituição indevida em vez de tradução direta
FORMULAS_ARA_GERAIS = [
    (
        re.compile(r"No princípio era o (?:Verbo|Discurso)", re.I),
        "Fórmula indevida ('era o Verbo' da ARA/Vulgata ou 'era o Discurso') — 'the Speech' (Sermo) de Calvino deve ser traduzido como 'a Palavra'.",
    ),
    (re.compile(r"leve e momentânea tribulação", re.I), "Fórmula exata da ARA em 2Co 4:17."),
    (re.compile(r"Não anulo a graça de Deus", re.I), "Fórmula exata da ARA em Gl 2:21."),
    (re.compile(r"Sabemos que todas as coisas cooperam para o bem", re.I), "Fórmula exata da ARA em Rm 8:28."),
    (re.compile(r"Justificados, pois, mediante a fé", re.I), "Fórmula exata da ARA em Rm 5:1."),
]

RE_HEBRAICO = re.compile(r"[\u0590-\u05FF]{2,}")
RE_GREGO = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]{2,}")


def ler_json(arq: Path, padrao=None):
    if not arq.exists():
        return {} if padrao is None else padrao
    return json.loads(arq.read_text(encoding="utf-8"))


def gravar_atomico(arq: Path, dados, indent=2):
    arq.parent.mkdir(parents=True, exist_ok=True)
    tmp = arq.with_suffix(arq.suffix + ".tmp")
    txt = json.dumps(dados, ensure_ascii=False, indent=indent)
    tmp.write_text(txt + ("\n" if indent else ""), encoding="utf-8")
    tmp.replace(arq)


def garantir_destino_seguro(caminho: Path):
    """Trava de segurança dupla: impede gravar fora de data/commentaries/calvin/pt-v2/."""
    resolvido = caminho.resolve()
    esperado = DESTINO_PT_V2.resolve()
    assert resolvido == esperado or esperado in resolvido.parents, (
        f"Abortado por segurança: destino inválido ({resolvido}) fora de {esperado}"
    )
    assert "pt-v2" in resolvido.parts, "Abortado: saída deve conter 'pt-v2'"


def carregar_dotenv() -> dict:
    achados = {}
    for arq in (PASTA_SCRIPT / ".env", TRABALHO / ".env", RAIZ / ".env"):
        if arq.exists():
            for linha in arq.read_text(encoding="utf-8").splitlines():
                linha = linha.strip()
                if not linha or linha.startswith("#") or "=" not in linha:
                    continue
                k, v = linha.split("=", 1)
                achados.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return achados


def obter_chave(provedor: str, chave_cli: str | None) -> str:
    if chave_cli:
        return chave_cli.strip()
    var = VAR_CHAVE[provedor]
    val = os.environ.get(var, "").strip() or carregar_dotenv().get(var, "").strip()
    if not val:
        sys.exit(
            f"Erro: chave {var} não encontrada.\n"
            f"Defina no ambiente ou crie {PASTA_SCRIPT / '.env'} com:\n"
            f"  {var}=sua-chave-aqui"
        )
    return val


def limpar_calvino(texto: str) -> tuple[str, str, bool]:
    """Separa o número do versículo inicial, remove apêndices de fim de volume do CCEL e corrige OCR."""
    m_num = NUM_VERSO.match(texto)
    prefixo = m_num.group(0) if m_num else ""
    corpo = texto[len(prefixo):] if prefixo else texto
    m_cauda = RE_CCEL_CAUDA.search(corpo)
    cortou = False
    if m_cauda:
        corpo = corpo[:m_cauda.start()].rstrip()
        cortou = True
    for padrao, subst in ERROS_OCR:
        corpo = padrao.sub(subst, corpo)
    return prefixo, corpo.strip(), cortou


def fatiar_com_sep(texto: str, limite: int = MAX_CAR_PARTE) -> list[tuple[str, str]]:
    """Divide preleções muito longas em quebras de parágrafo ou fim de período, guardando o separador."""
    if len(texto) <= limite:
        return [(texto, "")]
    pedacos = []
    restante = texto
    while len(restante) > limite:
        corte = restante.rfind("\n", 1000, limite)
        sep = "\n"
        if corte == -1:
            # Procura fim de frase antes do limite
            candidatos = [m.end() for m in re.finditer(r'[.!?][”"\')]?\s+(?=[A-Z"“(\[])', restante[:limite])]
            if candidatos and candidatos[-1] >= 1200:
                fim_frase = candidatos[-1]
                parte = restante[:fim_frase].rstrip()
                sep = " "
                restante = restante[fim_frase:].lstrip()
                pedacos.append((parte, sep))
                continue
            corte = restante.rfind(" ", 1000, limite)
            sep = " "
            if corte == -1:
                corte = limite
                sep = ""
        parte = restante[:corte].rstrip()
        restante = restante[corte:].lstrip("\n ")
        pedacos.append((parte, sep))
    if restante:
        pedacos.append((restante, ""))
    return pedacos


def aspas_curvas(pt: str) -> str:
    if '"' not in pt:
        return pt
    pt = re.sub(r'(?:(?<=^)|(?<=[\s(\[—-]))"(?=\S)', "“", pt)
    return pt.replace('"', "”")


def pos_processar(pt: str) -> str:
    if not pt:
        return pt
    # Remove eventuais marcações Markdown caso o modelo insista
    pt = re.sub(r"\*\*([^*\n]+)\*\*", r"\1", pt)
    pt = re.sub(r"(?m)^#{1,4}\s+", "", pt)
    pt = aspas_curvas(pt)
    pt = re.sub(r"[ \t]+\n", "\n", pt)
    pt = re.sub(r" {2,}", " ", pt)
    return pt.strip()


def max_tokens_para(texto: str) -> int:
    # Folga ampla para acomodar tokenizador do Claude 5.5 e eventual raciocínio adaptativo mínimo
    estimado = int(len(texto) * 0.6) + 4096
    return max(8192, min(32768, estimado))


# ---------------- Chamadas HTTP (stdlib pura) ----------------

def http_json(url: str, metodo: str = "GET", cabecalhos: dict | None = None,
              corpo: dict | bytes | None = None, tentativas: int = 4) -> dict:
    dados = None
    hdrs = dict(cabecalhos or {})
    if isinstance(corpo, dict):
        dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")
    elif isinstance(corpo, bytes):
        dados = corpo

    for t in range(tentativas):
        req = urllib.request.Request(url, data=dados, headers=hdrs, method=metodo)
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                bruto = resp.read().decode("utf-8")
                return json.loads(bruto) if bruto.strip() else {}
        except urllib.error.HTTPError as e:
            erro_txt = e.read().decode("utf-8", errors="replace")
            if e.code in (429, 500, 502, 503, 504, 529) and t + 1 < tentativas:
                espera = min(60, (2 ** t) * 3)
                print(f"  [HTTP {e.code}] aguardando {espera}s antes de tentar novamente...", flush=True)
                time.sleep(espera)
                continue
            raise RuntimeError(f"Erro HTTP {e.code} em {url}: {erro_txt[:600]}") from e
        except urllib.error.URLError as e:
            if t + 1 < tentativas:
                espera = (2 ** t) * 3
                print(f"  [Rede] falha ({e.reason}), tentando em {espera}s...", flush=True)
                time.sleep(espera)
                continue
            raise


def http_texto(url: str, cabecalhos: dict) -> str:
    req = urllib.request.Request(url, headers=cabecalhos, method="GET")
    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read().decode("utf-8")


def payload_anthropic(modelo: str, texto: str) -> dict:
    m = modelo.lower()
    corpo: dict = {
        "model": modelo,
        "max_tokens": max_tokens_para(texto),
        "system": [
            {
                "type": "text",
                "text": PROMPT_SISTEMA,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        "messages": [{"role": "user", "content": texto}],
    }
    # Claude 4.7+ e 5.5 rejeitam temperature/top_p com HTTP 400.
    if any(v in m for v in ("claude-3", "4-5", "4-6")):
        corpo["temperature"] = 0.2
    # No Haiku 5.5 é possível desligar totalmente o thinking; no Sonnet/Opus 5.5 usa-se effort="low".
    if "haiku-5" in m:
        corpo["thinking"] = {"type": "disabled"}
    elif any(v in m for v in ("-5", "4-7")):
        corpo["output_config"] = {"effort": "low"}
    return corpo


def cfg_gemini(modelo: str) -> dict:
    m = modelo.lower()
    cfg: dict = {"maxOutputTokens": 32768}
    if "2.5" in m:
        cfg["temperature"] = 0.2
        cfg["thinkingConfig"] = {"thinkingBudget": 0}
    elif any(x in m for x in ("3.5-flash", "3.6-flash", "flash-lite", "3-flash")):
        cfg["thinkingConfig"] = {"thinkingLevel": "minimal"}
    elif any(m.startswith(p) for p in ("gemini-3", "gemini-4")):
        cfg["thinkingConfig"] = {"thinkingLevel": "low"}
    else:
        cfg["temperature"] = 0.2
    return cfg


def payload_openai(modelo: str, texto: str) -> dict:
    m = modelo.lower()
    corpo: dict = {
        "model": modelo,
        "max_completion_tokens": max_tokens_para(texto),
        "messages": [
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": texto},
        ],
    }
    if m.startswith(("gpt-5", "gpt-6", "o1", "o3", "o4")):
        corpo["reasoning_effort"] = "low"
    else:
        corpo["temperature"] = 0.2
    return corpo


def traduzir_um(provedor: str, modelo: str, chave: str, texto: str) -> str:
    """Traduz um bloco (fatiando automaticamente se ultrapassar MAX_CAR_PARTE)."""
    partes = fatiar_com_sep(texto, MAX_CAR_PARTE)
    saida = []
    for pedaco, sep in partes:
        if provedor == "anthropic":
            resp = http_json(
                "https://api.anthropic.com/v1/messages",
                metodo="POST",
                cabecalhos={
                    "x-api-key": chave,
                    "anthropic-version": "2023-06-01",
                },
                corpo=payload_anthropic(modelo, pedaco),
            )
            if resp.get("stop_reason") == "max_tokens":
                raise RuntimeError("Saída cortada por max_tokens na Anthropic.")
            txt = "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")

        elif provedor == "gemini":
            resp = http_json(
                f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
                metodo="POST",
                cabecalhos={"x-goog-api-key": chave},
                corpo={
                    "systemInstruction": {"parts": [{"text": PROMPT_SISTEMA}]},
                    "contents": [{"role": "user", "parts": [{"text": pedaco}]}],
                    "generationConfig": cfg_gemini(modelo),
                },
            )
            cands = resp.get("candidates") or []
            if not cands:
                raise RuntimeError(f"Gemini não retornou candidato: {resp}")
            txt = "".join(
                p.get("text", "")
                for p in cands[0].get("content", {}).get("parts", [])
                if not p.get("thought")
            )

        elif provedor == "openai":
            resp = http_json(
                "https://api.openai.com/v1/chat/completions",
                metodo="POST",
                cabecalhos={"Authorization": f"Bearer {chave}"},
                corpo=payload_openai(modelo, pedaco),
            )
            esc = (resp.get("choices") or [{}])[0]
            if esc.get("finish_reason") == "length":
                raise RuntimeError("Saída cortada por max_completion_tokens na OpenAI.")
            txt = esc.get("message", {}).get("content", "")
        else:
            raise ValueError(f"Provedor desconhecido: {provedor}")

        saida.append(pos_processar(txt) + sep)
    return "".join(saida).strip()


# ---------------- Diagnóstico de qualidade e armadilhas ARA ----------------

def diagnosticar_texto(en_limpo: str, pt: str, item_meta: dict | None = None) -> dict:
    if not pt:
        return {"vazio": True}
    razao = round(len(pt) / max(len(en_limpo), 1), 2)
    ponto_virg_maiusc = len(re.findall(r";\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ]", pt))

    heb_en = set(RE_HEBRAICO.findall(en_limpo))
    grk_en = set(RE_GREGO.findall(en_limpo))
    heb_faltando = sorted(w for w in heb_en if w not in pt)
    grk_faltando = sorted(w for w in grk_en if w not in pt)

    alertas_ara = []
    if item_meta and item_meta.get("alerta_ara"):
        al = item_meta["alerta_ara"]
        if re.search(al["padrao"], pt, re.I):
            alertas_ara.append(al["nota"])
    for rx, nota in FORMULAS_ARA_GERAIS:
        if rx.search(pt) and nota not in alertas_ara:
            alertas_ara.append(nota)

    avisos = []
    if razao < 0.78:
        avisos.append(f"Texto curto ({razao:.2f}x do inglês — possível omissão)")
    elif razao > 1.45:
        avisos.append(f"Texto longo ({razao:.2f}x — possível ruído/índice não limpo)")
    if ponto_virg_maiusc >= 2:
        avisos.append(f"{ponto_virg_maiusc}× maiúscula após ';'")
    if heb_faltando:
        avisos.append(f"Hebraico ausente: {', '.join(heb_faltando[:3])}")
    if grk_faltando:
        avisos.append(f"Grego ausente: {', '.join(grk_faltando[:3])}")
    if "**" in pt:
        avisos.append("Contém asteriscos Markdown (**)")

    return {
        "vazio": False,
        "razao": razao,
        "pv_maiusc": ponto_virg_maiusc,
        "heb_total": len(heb_en),
        "heb_ok": len(heb_en) - len(heb_faltando),
        "grk_total": len(grk_en),
        "grk_ok": len(grk_en) - len(grk_faltando),
        "alertas_ara": alertas_ara,
        "avisos": avisos,
    }


# ---------------- Relatório HTML lado a lado (Teste A/B) ----------------

def gerar_relatorio_html():
    amostra = ler_json(ARQ_AMOSTRA_META, [])
    salvos = ler_json(ARQ_AMOSTRA_SAIDA, {})
    modelos = sorted(salvos.keys())

    registros = []
    for it in amostra:
        livro, cap, verso = it["id"].split("|")
        arq_en = BASE_CALVINO / livro / f"{cap}.json"
        arq_pt = BASE_CALVINO / "pt" / livro / f"{cap}.json"
        bruto_en = ler_json(arq_en).get(verso, "")
        bruto_nllb = ler_json(arq_pt).get(verso, "")
        prefixo, en_limpo, cortou_cauda = limpar_calvino(bruto_en)
        # No NLLB atual tiramos só o prefixo numérico para comparar de igual para igual
        nllb_corpo = NUM_VERSO.sub("", bruto_nllb, count=1).strip()

        por_modelo = {}
        for m in modelos:
            txt_m = salvos.get(m, {}).get(it["id"], "")
            txt_m_corpo = NUM_VERSO.sub("", txt_m, count=1).strip() if txt_m else ""
            por_modelo[m] = {
                "texto": txt_m_corpo,
                "diag": diagnosticar_texto(en_limpo, txt_m_corpo, it),
            }

        registros.append({
            "id": it["id"],
            "grupo": it["grupo"],
            "ref": it["ref"],
            "foco": it["foco"],
            "prefixo": prefixo.strip(),
            "cortou_cauda": cortou_cauda,
            "en": en_limpo,
            "nllb": nllb_corpo,
            "diag_nllb": diagnosticar_texto(en_limpo, nllb_corpo, it),
            "modelos": por_modelo,
        })

    dados_js = json.dumps({"modelos": modelos, "itens": registros}, ensure_ascii=False)
    # Evita fechamento acidental de <script>
    dados_js = dados_js.replace("</", "<\\/")

    pagina = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sola — Teste A/B de Tradução de Calvino (30 Trechos Difíceis)</title>
<style>
  :root {{
    --papel: #FAF7F0; --cartao: #FFFFFF; --borda: #E2DAC9; --texto: #231F1A;
    --suave: #6A6256; --rubrica: #8C2D23; --ouro: #9A7626; --ouro-bg: #F6EFE0;
    --ok: #23613B; --ok-bg: #E7F3EC; --alerta: #92400E; --alerta-bg: #FEF3C7;
    --erro: #991B1B; --erro-bg: #FEE2E2;
  }}
  body.escuro {{
    --papel: #171613; --cartao: #201E1A; --borda: #343029; --texto: #ECE6DA;
    --suave: #A59D8E; --rubrica: #D86B5E; --ouro: #D4AF5A; --ouro-bg: #2B2518;
    --ok: #6EE7A0; --ok-bg: #173222; --alerta: #FCD34D; --alerta-bg: #36280E;
    --erro: #FCA5A5; --erro-bg: #3B1818;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--papel); color: var(--texto);
    font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif;
    line-height: 1.6; font-variant-numeric: lining-nums;
  }}
  header {{
    position: sticky; top: 0; z-index: 20; background: var(--papel);
    border-bottom: 1px solid var(--borda); padding: 0.85rem 1.25rem;
  }}
  .topo-linha {{
    max-width: 1680px; margin: 0 auto; display: flex; flex-wrap: wrap;
    gap: 0.75rem 1.25rem; align-items: center; justify-content: space-between;
  }}
  h1 {{ margin: 0; font-size: 1.15rem; font-weight: 700; color: var(--rubrica); }}
  .controles {{ display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center; }}
  button, select {{
    font: inherit; font-size: 0.85rem; color: inherit; background: var(--cartao);
    border: 1px solid var(--borda); border-radius: 6px; padding: 0.38rem 0.7rem; cursor: pointer;
  }}
  button.ativo {{ background: var(--rubrica); color: #fff; border-color: var(--rubrica); }}
  .resumo {{
    max-width: 1680px; margin: 0.9rem auto 0; padding: 0 1.25rem;
    display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 0.65rem;
  }}
  .kpi {{
    background: var(--cartao); border: 1px solid var(--borda); border-radius: 8px;
    padding: 0.65rem 0.85rem; font-size: 0.84rem;
  }}
  .kpi strong {{ display: block; font-size: 1.05rem; margin-bottom: 0.15rem; }}
  main {{ max-width: 1680px; margin: 1rem auto 3rem; padding: 0 1.25rem; display: flex; flex-direction: column; gap: 1.1rem; }}
  .cartao {{ background: var(--cartao); border: 1px solid var(--borda); border-radius: 10px; overflow: hidden; }}
  .cab-cartao {{
    padding: 0.75rem 1rem; border-bottom: 1px solid var(--borda); background: var(--ouro-bg);
    display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; align-items: center; justify-content: space-between;
  }}
  .ref {{ font-weight: 700; font-size: 1rem; color: var(--rubrica); }}
  .etiqueta {{
    display: inline-block; font-size: 0.74rem; font-weight: 600; padding: 0.14rem 0.5rem;
    border-radius: 999px; border: 1px solid var(--borda); background: var(--cartao);
  }}
  .etiqueta.ok {{ color: var(--ok); background: var(--ok-bg); border-color: transparent; }}
  .etiqueta.alerta {{ color: var(--alerta); background: var(--alerta-bg); border-color: transparent; }}
  .etiqueta.erro {{ color: var(--erro); background: var(--erro-bg); border-color: transparent; }}
  .foco {{ width: 100%; margin: 0.15rem 0 0; font-size: 0.84rem; color: var(--suave); }}
  .grade {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); }}
  @media (max-width: 1100px) {{ .grade {{ grid-template-columns: 1fr; }} }}
  .col {{ padding: 0.9rem 1rem; border-right: 1px solid var(--borda); min-width: 0; }}
  .col:last-child {{ border-right: none; }}
  .col-tit {{
    font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em;
    font-weight: 700; color: var(--suave); margin-bottom: 0.45rem;
    display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; justify-content: space-between;
  }}
  .texto {{
    font-family: Cardo, Georgia, "Times New Roman", serif; font-size: 1.02rem;
    line-height: 1.68; white-space: pre-wrap; word-break: break-word;
  }}
  .vazio {{ color: var(--suave); font-style: italic; font-family: inherit; font-size: 0.9rem; }}
  .votos button.escolhido {{ background: var(--ok); color: #fff; border-color: var(--ok); }}
</style>
</head>
<body>
<header>
  <div class="topo-linha">
    <h1>Sola — Teste A/B: Comentários de Calvino (30 Trechos Difíceis)</h1>
    <div class="controles">
      <label>Modelo LLM: <select id="selModelo"></select></label>
      <button type="button" data-filtro="todos" class="ativo">Todos (30)</button>
      <button type="button" data-filtro="listas">Listas longas (10)</button>
      <button type="button" data-filtro="linguas">Latim/Grego/Heb. (10)</button>
      <button type="button" data-filtro="polemica">Polêmica &amp; Citações (10)</button>
      <button type="button" data-filtro="alertas">Com avisos</button>
      <button type="button" id="btnTema">Tema escuro</button>
    </div>
  </div>
</header>
<section class="resumo" id="resumo"></section>
<main id="lista"></main>
<script>
const DADOS = {dados_js};
const GRUPOS = {{ listas: "Listas longas", linguas: "Latim / Grego / Hebraico", polemica: "Polêmica & Citações" }};
let filtro = "todos";
let modeloAtual = DADOS.modelos[DADOS.modelos.length - 1] || "";
const votos = JSON.parse(localStorage.getItem("sola_ab_calvino_votos") || "{{}}");

const sel = document.getElementById("selModelo");
if (!DADOS.modelos.length) {{
  sel.innerHTML = `<option value="">(rode 'calvino_llm.py amostra' para preencher o LLM)</option>`;
}} else {{
  sel.innerHTML = DADOS.modelos.map(m => `<option value="${{m}}" ${{m===modeloAtual?"selected":""}}>${{m}}</option>`).join("");
}}
sel.addEventListener("change", () => {{ modeloAtual = sel.value; renderizar(); }});

document.querySelectorAll("[data-filtro]").forEach(b => b.addEventListener("click", () => {{
  document.querySelectorAll("[data-filtro]").forEach(x => x.classList.remove("ativo"));
  b.classList.add("ativo");
  filtro = b.dataset.filtro;
  renderizar();
}}));

document.getElementById("btnTema").addEventListener("click", () => document.body.classList.toggle("escuro"));

function esc(s) {{
  return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}}

function badgesDiag(d) {{
  if (!d || d.vazio) return `<span class="etiqueta">pendente</span>`;
  const out = [`<span class="etiqueta">${{d.razao}}x tam.</span>`];
  if (d.heb_total || d.grk_total) {{
    const ok = d.heb_ok === d.heb_total && d.grk_ok === d.grk_total;
    out.push(`<span class="etiqueta ${{ok ? 'ok' : 'erro'}}">Originais ${{d.heb_ok+d.grk_ok}}/${{d.heb_total+d.grk_total}}</span>`);
  }}
  d.alertas_ara.forEach(a => out.push(`<span class="etiqueta erro" title="${{esc(a)}}">Alerta ARA/citação</span>`));
  d.avisos.forEach(a => out.push(`<span class="etiqueta alerta">${{esc(a)}}</span>`));
  if (!d.alertas_ara.length && !d.avisos.length) out.push(`<span class="etiqueta ok">Sem ressalvas</span>`);
  return out.join(" ");
}}

function votar(id, escolha) {{
  if (votos[id] === escolha) delete votos[id];
  else votos[id] = escolha;
  localStorage.setItem("sola_ab_calvino_votos", JSON.stringify(votos));
  renderizar();
}}

function renderizar() {{
  let nllbAvisos = 0, llmAvisos = 0, araAlertas = 0, feitos = 0;
  let vLlm = 0, vNllb = 0, vRev = 0;
  DADOS.itens.forEach(it => {{
    if (it.diag_nllb.avisos.length) nllbAvisos++;
    const m = it.modelos[modeloAtual];
    if (m && !m.diag.vazio) {{
      feitos++;
      if (m.diag.avisos.length) llmAvisos++;
      if (m.diag.alertas_ara.length) araAlertas++;
    }}
    if (votos[it.id] === "llm") vLlm++;
    if (votos[it.id] === "nllb") vNllb++;
    if (votos[it.id] === "revisar") vRev++;
  }});

  document.getElementById("resumo").innerHTML = `
    <div class="kpi"><strong>${{feitos}} / ${{DADOS.itens.length}}</strong>Trechos traduzidos no modelo selecionado (${{esc(modeloAtual || "nenhum")}})</div>
    <div class="kpi"><strong>NLLB: ${{nllbAvisos}} | LLM: ${{llmAvisos}}</strong>Trechos com avisos técnicos (omissão, ';' maiúsculo ou grego/hebraico perdido)</div>
    <div class="kpi"><strong>${{araAlertas}}</strong>Alertas de fórmula da ARA / desvio de citação própria do Calvino no LLM</div>
    <div class="kpi"><strong>LLM: ${{vLlm}} · NLLB: ${{vNllb}} · Revisar: ${{vRev}}</strong>Sua avaliação manual salva no navegador</div>
  `;

  const visiveis = DADOS.itens.filter(it => {{
    if (filtro === "todos") return true;
    if (filtro === "alertas") {{
      const m = it.modelos[modeloAtual];
      return it.diag_nllb.avisos.length || (m && (m.diag.avisos.length || m.diag.alertas_ara.length));
    }}
    return it.grupo === filtro;
  }});

  document.getElementById("lista").innerHTML = visiveis.map(it => {{
    const m = it.modelos[modeloAtual];
    const voto = votos[it.id] || "";
    const notasAra = (m && m.diag.alertas_ara.length)
      ? `<p class="foco" style="color:var(--erro)"><strong>Atenção (citação/ARA):</strong> ${{m.diag.alertas_ara.map(esc).join(" | ")}}</p>` : "";
    const notaCauda = it.cortou_cauda
      ? `<span class="etiqueta ok" title="Índice/apêndice CCEL de fim de volume removido antes de enviar ao LLM">Apêndice CCEL removido</span>` : "";
    return `<article class="cartao">
      <div class="cab-cartao">
        <div>
          <span class="ref">${{esc(it.ref)}}</span>
          <span class="etiqueta">${{esc(GRUPOS[it.grupo] || it.grupo)}}</span>
          <span class="etiqueta">${{esc(it.id)}}</span>
          ${{notaCauda}}
        </div>
        <div class="votos">
          <button type="button" class="${{voto==='llm'?'escolhido':''}}" onclick="votar('${{it.id}}','llm')">Preferi LLM</button>
          <button type="button" class="${{voto==='nllb'?'escolhido':''}}" onclick="votar('${{it.id}}','nllb')">Preferi NLLB</button>
          <button type="button" class="${{voto==='revisar'?'escolhido':''}}" onclick="votar('${{it.id}}','revisar')">Marcar p/ ajuste</button>
        </div>
        <p class="foco">${{esc(it.foco)}}</p>
        ${{notasAra}}
      </div>
      <div class="grade">
        <div class="col">
          <div class="col-tit"><span>1. Inglês original (CTS)</span><span class="etiqueta">${{it.en.length}} car.</span></div>
          <div class="texto">${{esc(it.en)}}</div>
        </div>
        <div class="col">
          <div class="col-tit"><span>2. NLLB atual (pt/)</span><span>${{badgesDiag(it.diag_nllb)}}</span></div>
          <div class="texto">${{esc(it.nllb)}}</div>
        </div>
        <div class="col">
          <div class="col-tit"><span>3. LLM novo (${{esc(modeloAtual || "pt-v2")}})</span><span>${{badgesDiag(m && m.diag)}}</span></div>
          ${{m && m.texto ? `<div class="texto">${{esc(m.texto)}}</div>` : `<p class="vazio">Ainda não traduzido neste modelo. Rode:<br><code>python ferramentas/tradutor/calvino_llm.py amostra</code></p>`}}
        </div>
      </div>
    </article>`;
  }}).join("");
}}
renderizar();
</script>
</body>
</html>
"""
    TRABALHO.mkdir(parents=True, exist_ok=True)
    ARQ_RELATORIO_HTML.write_text(pagina, encoding="utf-8")
    print(f"Relatório A/B gerado em: {ARQ_RELATORIO_HTML}")


# ---------------- Comando: amostra (30 trechos difíceis) ----------------

def cmd_amostra(args):
    provedor = args.provedor
    modelo = args.modelo or MODELOS_PADRAO[provedor]
    chave = obter_chave(provedor, args.chave)

    amostra = ler_json(ARQ_AMOSTRA_META, [])
    if args.limite:
        amostra = amostra[:args.limite]

    salvos = ler_json(ARQ_AMOSTRA_SAIDA, {})
    do_modelo = salvos.setdefault(modelo, {})

    pendentes = [it for it in amostra if args.refazer or it["id"] not in do_modelo]
    print(f"[amostra] Modelo: {modelo} ({provedor}) | {len(amostra)} trechos na amostra, {len(pendentes)} pendentes.")

    t0 = time.time()
    for idx, it in enumerate(pendentes, 1):
        livro, cap, verso = it["id"].split("|")
        bruto_en = ler_json(BASE_CALVINO / livro / f"{cap}.json").get(verso, "")
        prefixo, en_limpo, _ = limpar_calvino(bruto_en)
        print(f"  [{idx}/{len(pendentes)}] Traduzindo {it['ref']} ({it['id']}, {len(en_limpo)} car.)...", flush=True)
        pt_corpo = traduzir_um(provedor, modelo, chave, en_limpo)
        do_modelo[it["id"]] = prefixo + pt_corpo
        gravar_atomico(ARQ_AMOSTRA_SAIDA, salvos)

        diag = diagnosticar_texto(en_limpo, pt_corpo, it)
        if diag["alertas_ara"]:
            print(f"    ! ALERTA CITAÇÃO/ARA: {'; '.join(diag['alertas_ara'])}", flush=True)
        if diag["avisos"]:
            print(f"    ! Aviso técnico: {'; '.join(diag['avisos'])}", flush=True)

    if pendentes:
        print(f"[amostra] Concluído em {time.time() - t0:.1f}s.")

    if args.aplicar_amostra:
        aplicar_dicionario_em_pt_v2(do_modelo, origem=f"amostra:{modelo}")

    gerar_relatorio_html()


# ---------------- Preparação e deduplicação do Calvino completo ----------------

def hash_corpo(texto: str) -> str:
    return hashlib.sha1(texto.encode("utf-8")).hexdigest()[:16]


def cmd_preparar(args):
    manifesto = ler_json(BASE_CALVINO / "manifest.json")
    livros = manifesto.get("books", [])
    if args.livro:
        filtro = {x.strip().upper() for x in args.livro.split(",")}
        livros = [b for b in livros if b in filtro]

    unicos = {}       # hash -> {"hash": h, "partes": [{"cid": ..., "texto": ..., "sep": ...}]}
    mapa_versos = {}  # "LIVRO|cap|verso" -> {"hash": h, "prefixo": prefixo}
    total_bruto = caudas = 0

    for livro in livros:
        pasta_livro = BASE_CALVINO / livro
        if not pasta_livro.is_dir():
            continue
        for arq in sorted(pasta_livro.glob("*.json"), key=lambda a: int(a.stem)):
            dados = ler_json(arq)
            for verso, txt in dados.items():
                if not (verso.isdigit() and txt.strip()):
                    continue
                total_bruto += len(txt)
                prefixo, limpo, cortou = limpar_calvino(txt)
                if cortou:
                    caudas += 1
                if not limpo:
                    continue
                h = hash_corpo(limpo)
                mapa_versos[f"{livro}|{arq.stem}|{verso}"] = {"hash": h, "prefixo": prefixo}
                if h not in unicos:
                    fatias = fatiar_com_sep(limpo, MAX_CAR_PARTE)
                    unicos[h] = {
                        "hash": h,
                        "partes": [
                            {"cid": f"c_{h}_{i}", "texto": pedaco, "sep": sep}
                            for i, (pedaco, sep) in enumerate(fatias)
                        ],
                    }

    total_limpo = sum(len(p["texto"]) for u in unicos.values() for p in u["partes"])
    total_requisicoes = sum(len(u["partes"]) for u in unicos.values())
    # Contabiliza também ~50% do prompt de sistema por requisição (considerando hits parciais de cache)
    car_sys_medio = total_requisicoes * len(PROMPT_SISTEMA) * 0.5
    # Tokenizador BPE padrão (Gemini / OpenAI ~4,0 car./tok) vs. Claude 5.5 (~3,1 car./tok)
    tok_in_bpe = (total_limpo + car_sys_medio) / 4.0
    tok_out_bpe = (total_limpo / 4.0) * 1.15
    tok_in_c55 = (total_limpo + car_sys_medio) / 3.1
    tok_out_c55 = (total_limpo / 3.1) * 1.15

    pacote = {
        "versao": 2,
        "livros": livros,
        "unicos": list(unicos.values()),
        "mapa_versos": mapa_versos,
    }
    gravar_atomico(ARQ_ENTRADAS_V2, pacote)

    economia = 100.0 * (1.0 - total_limpo / max(total_bruto, 1))
    print(f"[preparar] Gravado em {ARQ_ENTRADAS_V2}")
    print(f"  Versículos/blocos mapeados : {len(mapa_versos):,}")
    print(f"  Textos únicos deduplicados : {len(unicos):,} (economia de {economia:.1f}% sobre {total_bruto:,} car. brutos)")
    print(f"  Apêndices CCEL removidos   : {caudas}")
    print(
        f"  Requisições totais         : {total_requisicoes:,} ({total_limpo:,} car. de texto | "
        f"~{tok_in_c55/1e6:.1f}M in / {tok_out_c55/1e6:.1f}M out no Claude 5.5; "
        f"~{tok_in_bpe/1e6:.1f}M in / {tok_out_bpe/1e6:.1f}M out em BPE)"
    )
    print("  Estimativa via Batch API (50% desc. — suportado em Anthropic e OpenAI):")
    print(f"    - claude-haiku-5-5  (Batch $0.05 / $0.25 MTok) : ~US$ {(tok_in_c55/1e6)*0.05 + (tok_out_c55/1e6)*0.25:.2f}")
    print(f"    - claude-sonnet-5-5 (Batch $1.00 / $5.00 MTok) : ~US$ {(tok_in_c55/1e6)*1.00 + (tok_out_c55/1e6)*5.00:.2f}")
    print(f"    - gpt-6-luna        (Batch $0.05 / $0.25 MTok) : ~US$ {(tok_in_bpe/1e6)*0.05 + (tok_out_bpe/1e6)*0.25:.2f}")
    print("  Estimativa no modo 'direto' síncrono (PREÇO CHEIO — Gemini não usa Batch neste script):")
    print(f"    - gemini-3.5-flash      (preço cheio $1.50 / $9.00 MTok) : ~US$ {(tok_in_bpe/1e6)*1.50 + (tok_out_bpe/1e6)*9.00:.2f}")
    print(f"    - gemini-3.5-flash-lite (preço cheio $0.30 / $2.50 MTok) : ~US$ {(tok_in_bpe/1e6)*0.30 + (tok_out_bpe/1e6)*2.50:.2f}")


# ---------------- Batch API (enviar / status / baixar) ----------------

def requisicoes_pendentes(pacote: dict, feitos_partes: dict) -> list[dict]:
    pend = []
    for u in pacote.get("unicos", []):
        for p in u["partes"]:
            if p["cid"] not in feitos_partes:
                pend.append(p)
    return pend


def upload_multipart_openai(chave: str, nome_arq: str, conteudo_jsonl: bytes) -> str:
    limite = f"----SolaBatch{uuid.uuid4().hex}"
    buf = io.BytesIO()
    buf.write(f"--{limite}\r\nContent-Disposition: form-data; name=\"purpose\"\r\n\r\nbatch\r\n".encode("utf-8"))
    buf.write(
        f"--{limite}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{nome_arq}\"\r\n"
        f"Content-Type: application/jsonl\r\n\r\n".encode("utf-8")
    )
    buf.write(conteudo_jsonl)
    buf.write(f"\r\n--{limite}--\r\n".encode("utf-8"))
    resp = http_json(
        "https://api.openai.com/v1/files",
        metodo="POST",
        cabecalhos={
            "Authorization": f"Bearer {chave}",
            "Content-Type": f"multipart/form-data; boundary={limite}",
        },
        corpo=buf.getvalue(),
    )
    return resp["id"]


def cmd_enviar(args):
    if not ARQ_ENTRADAS_V2.exists():
        sys.exit(f"Arquivo {ARQ_ENTRADAS_V2} não encontrado. Rode 'preparar' primeiro.")

    provedor = args.provedor
    if provedor not in ("anthropic", "openai"):
        sys.exit(
            "O modo Batch assíncrono ('enviar', 50% desc.) suporta apenas 'anthropic' e 'openai'. "
            "No Gemini este script roda apenas em 'amostra' ou 'direto' (preço cheio, sem Batch API)."
        )
    modelo = args.modelo or MODELOS_PADRAO[provedor]
    chave = obter_chave(provedor, args.chave)

    pacote = ler_json(ARQ_ENTRADAS_V2)
    estado_saida = ler_json(ARQ_SAIDA_V2, {"modelo": modelo, "partes": {}})
    feitos_partes = estado_saida.get("partes", {})
    lotes = ler_json(ARQ_LOTES_V2, [])

    ja_em_lote = {
        cid
        for lt in lotes
        if lt.get("status") not in ("canceled", "expired", "failed") and not lt.get("baixado")
        for cid in lt.get("cids", [])
    }
    pend = [p for p in requisicoes_pendentes(pacote, feitos_partes) if p["cid"] not in ja_em_lote]
    if args.limite:
        pend = pend[:args.limite]

    print(f"[enviar] {len(pend):,} requisições novas a enviar ({len(feitos_partes):,} já salvas, {len(ja_em_lote):,} em lotes ativos).")
    if not pend:
        return

    por_lote = args.por_lote
    for i in range(0, len(pend), por_lote):
        bloco = pend[i:i + por_lote]
        if provedor == "anthropic":
            reqs = [
                {"custom_id": p["cid"], "params": payload_anthropic(modelo, p["texto"])}
                for p in bloco
            ]
            resp = http_json(
                "https://api.anthropic.com/v1/messages/batches",
                metodo="POST",
                cabecalhos={
                    "x-api-key": chave,
                    "anthropic-version": "2023-06-01",
                },
                corpo={"requests": reqs},
            )
            batch_id = resp["id"]
            status_atual = resp.get("processing_status", "in_progress")
        else:
            linhas = [
                json.dumps({
                    "custom_id": p["cid"],
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": payload_openai(modelo, p["texto"]),
                }, ensure_ascii=False)
                for p in bloco
            ]
            arq_id = upload_multipart_openai(chave, f"calvino_{i // por_lote}.jsonl", ("\n".join(linhas) + "\n").encode("utf-8"))
            resp = http_json(
                "https://api.openai.com/v1/batches",
                metodo="POST",
                cabecalhos={"Authorization": f"Bearer {chave}"},
                corpo={
                    "input_file_id": arq_id,
                    "endpoint": "/v1/chat/completions",
                    "completion_window": "24h",
                },
            )
            batch_id = resp["id"]
            status_atual = resp.get("status", "in_progress")

        lotes.append({
            "id": batch_id,
            "provedor": provedor,
            "modelo": modelo,
            "criado_em": time.strftime("%Y-%m-%d %H:%M:%S"),
            "qtd": len(bloco),
            "status": status_atual,
            "baixado": False,
            "cids": [p["cid"] for p in bloco],
        })
        gravar_atomico(ARQ_LOTES_V2, lotes)
        print(f"  Lote enviado: {batch_id} ({len(bloco)} itens, status={status_atual})", flush=True)


def cmd_status(args):
    lotes = ler_json(ARQ_LOTES_V2, [])
    if not lotes:
        return print("[status] Nenhum lote registrado em trabalho/lotes_calvino_v2.json.")

    for lt in lotes:
        prov = lt["provedor"]
        chave = obter_chave(prov, args.chave)
        if prov == "anthropic":
            info = http_json(
                f"https://api.anthropic.com/v1/messages/batches/{lt['id']}",
                cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"},
            )
            st = info.get("processing_status", "?")
            cnt = info.get("request_counts", {})
            resumo = f"ok={cnt.get('succeeded', 0)}, proc={cnt.get('processing', 0)}, erro={cnt.get('errored', 0)}"
        else:
            info = http_json(
                f"https://api.openai.com/v1/batches/{lt['id']}",
                cabecalhos={"Authorization": f"Bearer {chave}"},
            )
            st = info.get("status", "?")
            cnt = info.get("request_counts", {})
            resumo = f"ok={cnt.get('completed', 0)}/{cnt.get('total', 0)}, erro={cnt.get('failed', 0)}"

        lt["status"] = st
        print(f"  {lt['id']} ({prov}/{lt['modelo']}): status={st} | {resumo} | baixado={lt.get('baixado', False)}")
    gravar_atomico(ARQ_LOTES_V2, lotes)


def cmd_baixar(args):
    lotes = ler_json(ARQ_LOTES_V2, [])
    if not lotes:
        return print("[baixar] Nenhum lote para baixar.")

    estado_saida = ler_json(ARQ_SAIDA_V2, {"modelo": "", "partes": {}})
    partes = estado_saida.setdefault("partes", {})
    novos = falhas = cortados = 0

    for lt in lotes:
        if lt.get("baixado") and not args.forcar:
            continue
        prov = lt["provedor"]
        chave = obter_chave(prov, args.chave)

        if prov == "anthropic":
            info = http_json(
                f"https://api.anthropic.com/v1/messages/batches/{lt['id']}",
                cabecalhos={"x-api-key": chave, "anthropic-version": "2023-06-01"},
            )
            lt["status"] = info.get("processing_status", "")
            if lt["status"] != "ended":
                print(f"  {lt['id']}: ainda em '{lt['status']}', pulando.")
                continue
            url_res = info.get("results_url") or f"https://api.anthropic.com/v1/messages/batches/{lt['id']}/results"
            bruto = http_texto(url_res, {"x-api-key": chave, "anthropic-version": "2023-06-01"})
            for linha in bruto.splitlines():
                if not linha.strip():
                    continue
                obj = json.loads(linha)
                cid = obj["custom_id"]
                res = obj.get("result", {})
                if res.get("type") == "succeeded":
                    msg = res.get("message", {})
                    if msg.get("stop_reason") == "max_tokens":
                        cortados += 1
                        continue
                    txt = "".join(b.get("text", "") for b in msg.get("content", []) if b.get("type") == "text")
                    partes[cid] = pos_processar(txt)
                    novos += 1
                else:
                    falhas += 1
            estado_saida["modelo"] = lt["modelo"]
            lt["baixado"] = True

        elif prov == "openai":
            info = http_json(
                f"https://api.openai.com/v1/batches/{lt['id']}",
                cabecalhos={"Authorization": f"Bearer {chave}"},
            )
            lt["status"] = info.get("status", "")
            if lt["status"] != "completed":
                print(f"  {lt['id']}: ainda em '{lt['status']}', pulando.")
                continue
            out_id = info.get("output_file_id")
            if not out_id:
                continue
            bruto = http_texto(
                f"https://api.openai.com/v1/files/{out_id}/content",
                {"Authorization": f"Bearer {chave}"},
            )
            for linha in bruto.splitlines():
                if not linha.strip():
                    continue
                obj = json.loads(linha)
                cid = obj["custom_id"]
                corpo_r = obj.get("response", {}).get("body", {})
                esc = (corpo_r.get("choices") or [{}])[0]
                if esc.get("finish_reason") == "length":
                    cortados += 1
                    continue
                txt = esc.get("message", {}).get("content", "")
                if txt:
                    partes[cid] = pos_processar(txt)
                    novos += 1
                else:
                    falhas += 1
            estado_saida["modelo"] = lt["modelo"]
            lt["baixado"] = True

        gravar_atomico(ARQ_SAIDA_V2, estado_saida, indent=None)
        gravar_atomico(ARQ_LOTES_V2, lotes)

    print(f"[baixar] +{novos:,} partes salvas (total acumulado: {len(partes):,}; falhas={falhas}; cortadas por max_tokens={cortados}).")


# ---------------- Execução síncrona retomável (para 1 livro ou Gemini) ----------------

def cmd_direto(args):
    if not ARQ_ENTRADAS_V2.exists():
        sys.exit(f"Rode 'preparar' antes de 'direto'.")
    provedor = args.provedor
    modelo = args.modelo or MODELOS_PADRAO[provedor]
    chave = obter_chave(provedor, args.chave)

    pacote = ler_json(ARQ_ENTRADAS_V2)
    estado_saida = ler_json(ARQ_SAIDA_V2, {"modelo": modelo, "partes": {}})
    partes = estado_saida.setdefault("partes", {})
    estado_saida["modelo"] = modelo

    pend = requisicoes_pendentes(pacote, partes)
    if args.limite:
        pend = pend[:args.limite]
    print(f"[direto] {len(pend):,} partes pendentes em {modelo} ({provedor}).")
    t0 = time.time()
    for i, p in enumerate(pend, 1):
        partes[p["cid"]] = traduzir_um(provedor, modelo, chave, p["texto"])
        if i % 10 == 0 or i == len(pend):
            gravar_atomico(ARQ_SAIDA_V2, estado_saida, indent=None)
            decorrido = max(time.time() - t0, 1e-6)
            ritmo = i / decorrido
            resta = (len(pend) - i) / max(ritmo, 1e-6) / 60
            print(f"  {i}/{len(pend)} salvas (~{resta:.1f} min restantes)", flush=True)


# ---------------- Aplicação exclusiva em data/commentaries/calvin/pt-v2/ ----------------

def aplicar_dicionario_em_pt_v2(mapa_id_texto: dict, origem: str = ""):
    """Grava um dicionário {'LIVRO|cap|verso': texto_com_prefixo} apenas em pt-v2/."""
    garantir_destino_seguro(DESTINO_PT_V2)
    por_cap = {}
    for k, texto_pt in mapa_id_texto.items():
        livro, cap, verso = k.split("|")
        por_cap.setdefault((livro, cap), {})[verso] = texto_pt

    for (livro, cap), novos_versos in sorted(por_cap.items()):
        alvo = DESTINO_PT_V2 / livro / f"{cap}.json"
        garantir_destino_seguro(alvo)
        atual = ler_json(alvo, {})
        atual.update(novos_versos)
        atual["__pt"] = True
        if origem:
            atual["__motor"] = origem
        gravar_atomico(alvo, atual, indent=2)

    print(f"[aplicar] {len(mapa_id_texto):,} versículos em {len(por_cap):,} capítulos gravados em {DESTINO_PT_V2.relative_to(RAIZ)}/")


def cmd_aplicar(_args):
    if not ARQ_ENTRADAS_V2.exists() or not ARQ_SAIDA_V2.exists():
        sys.exit("Arquivos trabalho/calvino_v2_entradas.json e trabalho/calvino_v2_pt.json são necessários.")

    pacote = ler_json(ARQ_ENTRADAS_V2)
    estado_saida = ler_json(ARQ_SAIDA_V2)
    partes = estado_saida.get("partes", {})
    modelo = estado_saida.get("modelo", "llm-v2")

    corpos_prontos = {}
    incompletos = 0
    for u in pacote.get("unicos", []):
        ps = u["partes"]
        if all(p["cid"] in partes for p in ps):
            corpos_prontos[u["hash"]] = "".join(partes[p["cid"]] + p["sep"] for p in ps).strip()
        else:
            incompletos += 1

    prontos_por_id = {}
    for id_verso, info in pacote.get("mapa_versos", {}).items():
        corpo_pt = corpos_prontos.get(info["hash"])
        if corpo_pt:
            prontos_por_id[id_verso] = info["prefixo"] + corpo_pt

    if not prontos_por_id:
        return print("[aplicar] Nenhum bloco completo disponível ainda.")

    aplicar_dicionario_em_pt_v2(prontos_por_id, origem=modelo)
    if incompletos:
        print(f"  (Nota: {incompletos:,} textos únicos ainda aguardam tradução nos lotes pendentes.)")


def main():
    ap = argparse.ArgumentParser(description="Tradutor seguro de Calvino (A/B + Batch API -> pt-v2/)")
    sub = ap.add_subparsers(dest="acao", required=True)

    def comuns_api(p):
        p.add_argument("--provedor", choices=["anthropic", "gemini", "openai"], default="anthropic")
        p.add_argument("--modelo", default=None, help="Ex.: claude-haiku-5-5, claude-sonnet-5-5, gemini-3.5-flash, gpt-6-luna")
        p.add_argument("--chave", default=None, help="Chave da API (opcional se estiver em .env ou variável de ambiente)")

    p_am = sub.add_parser("amostra", help="Roda o teste A/B nos 30 trechos difíceis e gera o relatório HTML")
    comuns_api(p_am)
    p_am.add_argument("--limite", type=int, default=0, help="Traduz apenas os primeiros N trechos da amostra")
    p_am.add_argument("--refazer", action="store_true", help="Retraduz mesmo os trechos já salvos deste modelo")
    p_am.add_argument("--aplicar-amostra", action="store_true", help="Grava também os trechos da amostra em data/commentaries/calvin/pt-v2/")

    sub.add_parser("relatorio", help="Regera o relatório HTML A/B a partir das traduções já salvas")

    p_pr = sub.add_parser("preparar", help="Prepara, limpa e deduplica todos os comentários de Calvino")
    p_pr.add_argument("--livro", default=None, help="Filtra por código(s) USFM separados por vírgula (ex.: JHN,ROM)")

    p_en = sub.add_parser("enviar", help="Envia requisições pendentes para a Batch API (50%% desc. — Anthropic e OpenAI)")
    comuns_api(p_en)
    p_en.add_argument("--por-lote", type=int, default=2500, help="Máximo de requisições por lote (padrão: 2500)")
    p_en.add_argument("--limite", type=int, default=0, help="Envia apenas as primeiras N requisições pendentes")

    p_st = sub.add_parser("status", help="Consulta o andamento dos lotes enviados")
    p_st.add_argument("--chave", default=None)

    p_bx = sub.add_parser("baixar", help="Baixa os lotes concluídos para trabalho/calvino_v2_pt.json")
    p_bx.add_argument("--chave", default=None)
    p_bx.add_argument("--forcar", action="store_true", help="Rebaixa mesmo lotes já marcados como baixados")

    p_di = sub.add_parser("direto", help="Traduz de forma síncrona a preço cheio (para 1 livro ou Gemini)")
    comuns_api(p_di)
    p_di.add_argument("--limite", type=int, default=0)

    sub.add_parser("aplicar", help="Grava as traduções prontas exclusivamente em data/commentaries/calvin/pt-v2/")

    args = ap.parse_args()
    if args.acao == "amostra":
        cmd_amostra(args)
    elif args.acao == "relatorio":
        gerar_relatorio_html()
    elif args.acao == "preparar":
        cmd_preparar(args)
    elif args.acao == "enviar":
        cmd_enviar(args)
    elif args.acao == "status":
        cmd_status(args)
    elif args.acao == "baixar":
        cmd_baixar(args)
    elif args.acao == "direto":
        cmd_direto(args)
    elif args.acao == "aplicar":
        cmd_aplicar(args)


if __name__ == "__main__":
    main()
