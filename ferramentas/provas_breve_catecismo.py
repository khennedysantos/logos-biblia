"""Textos de prova do Breve Catecismo de Westminster: as provas da própria Assembleia (1647/1648), por trecho da
resposta, como no Catecismo Maior ("glorificar a Deus[1] e gozá-lo para sempre[2]").

Fonte: a transcrição "The original text of 1647, with the Assembly's proof texts" (gist de lojic, na cópia corrigida
do repositório Sundar1205/westminster-catechism, sources/wsc-1647.txt; a correção da pergunta 93 está documentada
lá). As referências entre colchetes dessa transcrição são acréscimos modernos e ficam de fora. As provas foram
conferidas com a edição de Edimburgo de 1838 da Igreja da Escócia ("with the Scripture-proofs at large", escaneada no
Internet Archive: confessionoffait00chu).

O importador põe os marcadores [n] no inglês (r_en) alinhando as palavras com a transcrição e, no português (r), só
confere: nas respostas com uma prova só, no fim, ele mesmo a acrescenta no fim; nas outras, os marcadores foram postos
à mão na tradução (sessão do agente, nov/2026) e precisam bater com os do inglês.

Uso (o arquivo baixado fica em ferramentas/fontes/wsc/, fora do git). Rode depois de confissoes.py, que zera as provas:
    python3 ferramentas/provas_breve_catecismo.py
Depois: python3 ferramentas/gerar_paginas.py"""
import difflib, json, re, sys, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from confissoes import DESTINO, bl, converter                      # noqa: E402
from provas_wikisource import refs                                 # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
FONTE = RAIZ / "ferramentas" / "fontes" / "wsc" / "wsc-1647.txt"
URL = "https://raw.githubusercontent.com/Sundar1205/westminster-catechism/main/sources/wsc-1647.txt"
ARQUIVO = DESTINO / "breve-catecismo.json"
RE_MARCA = re.compile(r"\s*\((\d+)\)")


def baixar():
    if not FONTE.exists():
        FONTE.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Sola)"})
        FONTE.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    return FONTE.read_text(encoding="utf-8")


def ler_fonte(biblia, problemas):
    """{n: (resposta com (1), (2)…, {marca: [refs]})}"""
    saida = {}
    for bloco in re.split(r"\n(?=\d+\. )", baixar()):
        m = re.match(r"(\d+)\. ", bloco)
        if not m:
            continue
        partes = re.split(r"\n\s*\n", bloco.strip())[1:]
        resposta = " ".join(" ".join(p for p in partes if not p.lstrip().startswith("(")).split())
        provas = {}
        for linha in re.split(r"\n(?=\s*\(\d+\))", "\n".join(p for p in partes if p.lstrip().startswith("("))):
            if mm := re.match(r"\s*\((\d+)\)\s*(.*)", linha, re.S):
                texto = re.sub(r"\[.*?\]", "", mm.group(2), flags=re.S)        # acréscimos modernos entre colchetes
                texto = texto.replace("Ps. 67; 119:36", "Ps. 67:1-7; Ps. 119:36")   # o salmo 67 inteiro
                texto = re.sub(r"\b(I{1,3})\s+(?=[A-Z])", lambda r: f"{len(r.group(1))} ", texto)  # "II Tim." -> "2 Tim."
                provas[mm.group(1)] = refs(texto, biblia, problemas)
        saida[m.group(1)] = (resposta, provas)
    return saida


def palavras(s):
    return [re.sub(r"\W", "", w).lower() for w in s.split()]


def marcar_ingles(r_en, resposta):
    """põe em r_en os marcadores da resposta da fonte, depois da mesma palavra"""
    limpa = RE_MARCA.sub("", resposta)
    # índice (na fonte) da palavra depois da qual vem cada marcador
    marcas, pos = [], 0
    for m in RE_MARCA.finditer(resposta):
        marcas.append((len(RE_MARCA.sub("", resposta[:m.start()]).split()) - 1, m.group(1)))
    alvo = r_en.split()
    mapa = {}
    for bloco in difflib.SequenceMatcher(None, palavras(limpa), palavras(r_en), autojunk=False).get_matching_blocks():
        for k in range(bloco.size):
            mapa[bloco.a + k] = bloco.b + k
    for i, n in sorted(marcas, reverse=True):
        j = mapa.get(i, len(alvo) - 1 if i == len(limpa.split()) - 1 else None)
        if j is None:
            return None
        alvo[j] += f"[{n}]"
    return " ".join(alvo)


def main():
    biblia, problemas = bl(), []
    fonte = ler_fonte(biblia, problemas)
    doc = json.loads(ARQUIVO.read_text(encoding="utf-8"))
    faltam_pt = []
    for q in doc["itens"]:
        resposta, provas = fonte[q["n"]]
        en = RE_MARCA.sub("", q["r_en"].replace("[", "(").replace("]", ")"))   # sem marcadores antigos
        en = re.sub(r"\(\d+\)", "", en)
        marcado = marcar_ingles(en, resposta) if provas else en
        if marcado is None:
            problemas.append(f"pergunta {q['n']}: não consegui alinhar os marcadores no inglês")
            continue
        q["r_en"] = marcado
        marcas_en = re.findall(r"\[\d+\]", marcado)
        if not re.findall(r"\[\d+\]", q["r"]) and len(marcas_en) == 1 and marcado.endswith(marcas_en[0]):
            q["r"] = q["r"].rstrip() + marcas_en[0]                  # uma prova só, no fim da resposta
        if sorted(re.findall(r"\[\d+\]", q["r"])) != sorted(marcas_en):
            faltam_pt.append(q["n"])
        q["provas"] = {k: v for k, v in provas.items() if v}
    ARQUIVO.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    total = sum(len(v) for q in doc["itens"] for v in q["provas"].values())
    print(f"Breve Catecismo: {sum(1 for q in doc['itens'] if q['provas'])} perguntas com provas, {total} referências")
    if faltam_pt:
        print(f"  ⚠ marcadores do português a pôr à mão: {', '.join(faltam_pt)}")
    for p in problemas:
        print("  ⚠", p)


if __name__ == "__main__":
    main()
