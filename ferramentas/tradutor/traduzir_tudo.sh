#!/bin/bash
# Traduz para português, de graça e offline, o que ainda está em inglês no Sola:
#   glosas  -> palavras do interlinear que faltavam      (minutos)
#   temas   -> subdivisões dos temas de Nave              (~10 min)
#   dicionario -> verbetes do dicionário de Easton        (~20 min)
#   calvino -> comentários de João Calvino                (algumas horas)
#
# Uso:   ./traduzir_tudo.sh                (todas as etapas, na ordem acima)
#        ./traduzir_tudo.sh temas calvino  (só as que você escolher)
#
# Pode interromper com Ctrl+C a qualquer momento: rode de novo e ele continua
# de onde parou. Cada etapa já grava o resultado nos arquivos do site ao terminar.
set -e
cd "$(dirname "$0")"

if [ ! -x venv/bin/python ]; then
  echo ">> Criando ambiente Python (uma vez só)..."
  python3 -m venv venv
  ./venv/bin/pip install -q ctranslate2 sentencepiece
fi
if [ ! -d modelo ]; then
  echo ">> Baixando o modelo de tradução inglês->português (66 MB, uma vez só)..."
  curl -L --fail -o modelo.zip https://argos-net.com/v1/translate-en_pb-1_9.argosmodel
  rm -rf modelo_tmp && unzip -q modelo.zip -d modelo_tmp
  mv modelo_tmp/*/ modelo && rm -rf modelo_tmp modelo.zip
fi

PY=./venv/bin/python
ETAPAS=${@:-glosas temas dicionario calvino}
for etapa in $ETAPAS; do
  echo
  echo "================ $etapa ================"
  [ -f "trabalho/$etapa.json" ] || $PY etapas.py preparar "$etapa"
  $PY lote.py "trabalho/$etapa.json" "trabalho/${etapa}_pt.json" modelo
  $PY etapas.py aplicar "$etapa"
done

echo
echo "Pronto. Para publicar:"
echo "  cd ../.. && git add data ferramentas/glosas_pt.json && git commit -m 'Traducao para portugues' && git push"
