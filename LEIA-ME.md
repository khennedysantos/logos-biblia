# Logos — Estudo Bíblico

Site completo de estudo bíblico. Estático: não precisa de servidor, banco de dados
nem chave de API para funcionar. Custo de operação: **zero**.

## O que já está incluído

- **Bíblia completa** (31.102 versículos) em 3 traduções de domínio público:
  - Português — Bíblia Livre (BLIVRE)
  - Inglês — King James Version (1769)
  - Espanhol — Reina-Valera Antigua
- **Interlinear palavra por palavra** (425.454 palavras): cada palavra do grego
  (NT) e do hebraico (AT) com transliteração, tradução literal e número de
  Strong — clique na palavra para abrir o léxico completo (14.197 entradas).
  Dados: STEPBible/Tyndale House (CC BY) + Léxico de Strong (domínio público)
- **Comentário de João Calvino** (13.106 blocos, 47 livros, domínio público) —
  por enquanto em inglês; pipeline de tradução pronto (veja abaixo)
- Interface em português, inglês e espanhol
- Marcação de versículos em 4 cores, anotações pessoais, copiar versículo
- Comparação de traduções lado a lado
- Busca no livro atual ou na Bíblia toda (com acentos ignorados)
- Navegação pelos 66 livros, modo noturno, link direto por capítulo
  (ex.: `seusite.com/#/JHN/3`)
- Marcações e anotações ficam salvas no navegador do visitante (localStorage) —
  ninguém precisa criar conta e você não precisa manter banco de dados

## Como publicar (grátis)

**Opção A — GitHub Pages:**
1. Crie um repositório no GitHub (ex.: `logos-biblia`)
2. Envie todo o conteúdo desta pasta para o repositório
3. Em Settings → Pages, escolha "Deploy from a branch" → branch `main`, pasta `/`
4. Pronto: o site fica em `https://seuusuario.github.io/logos-biblia/`

**Opção B — Netlify ou Vercel:** arraste esta pasta no painel deles. Sem build.

Para domínio próprio (ex.: `logosbiblia.com.br`), registre no Registro.br e
aponte para o GitHub Pages/Netlify nas configurações de DNS.

## Traduzir o comentário de Calvino para português

Único passo que precisa da sua chave da API da Anthropic (console.anthropic.com).
Custo estimado: **~US$ 40, uma única vez** (Haiku 4.5 via Batch API, 50% de desconto).

```
cd ferramentas
pip install anthropic
export ANTHROPIC_API_KEY="sua-chave"

# 1. Teste primeiro com um lote pequeno (recomendado):
python -c "import json; d=json.load(open('entradas_calvin.json')); json.dump([x for x in d if x['livro']=='JHN' and x['capitulo']==3], open('teste.json','w'))"
python traduzir_comentarios.py enviar teste.json
python traduzir_comentarios.py baixar <batch_id>   # quando terminar
python mesclar_traducoes.py                        # revise o resultado no site

# 2. Se gostou do estilo, mande tudo:
python traduzir_comentarios.py enviar entradas_calvin.json
python traduzir_comentarios.py baixar <batch_id>   # um por lote impresso
python mesclar_traducoes.py

# 3. Léxico de Strong em português (~US$ 1, uma vez):
python traduzir_comentarios.py enviar entradas_strongs.json
python traduzir_comentarios.py baixar <batch_id>
python mesclar_strongs.py

# 4. Glosas do interlinear em português (~US$ 4, uma vez):
python extrair_glosas.py          # já vem pronto, mas pode regerar
python traduzir_comentarios.py enviar entradas_glosas.json
python traduzir_comentarios.py baixar <batch_id>
python mesclar_glosas.py
```

Depois de cada mesclagem: `git add . && git commit -m "traduções" && git push`
na pasta do site, e as mudanças vão ao ar em ~2 minutos.

Depois é só publicar a pasta de novo. O site detecta capítulos traduzidos
automaticamente e deixa de exibir o aviso "comentário em inglês".

## Fontes e licenças

- Textos bíblicos: scrollmapper/bible_databases (domínio público)
- Comentários: thefrenchpressed/pillar-commentary-data, origem CCEL/CrossWire
  (domínio público)
- O código deste site é seu — use e modifique à vontade.

## Próximos passos sugeridos

- Referências cruzadas (Treasury of Scripture Knowledge, domínio público)
- Páginas estáticas por capítulo para SEO
- Planos de leitura com progresso
- Mais traduções licenciadas via API.Bible (chave gratuita não comercial)
- Concordância (todas as ocorrências de cada palavra grega/hebraica)
