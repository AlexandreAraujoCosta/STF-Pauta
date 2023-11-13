# STF-Pauta: extração dos dados das pautas

## Etapa 1. extrator_datas_pautas.py

Este programa abre as páginas do STF que definem as datas das pautas presenciais e do Plenário Virtual.

Ele grava na pasta '/datas_pautas' (que deve ser criada para esse fim) os  dados acerca de quais são as datas em que houve pautas presenciais e também início e fim das pautas virtuais, informações que são necessárias para construir os urls para identificar os dados de julgamento de cada sessão pautada.
Este e outros programas utilizam funções do módulo dsl.py (Data Science and Law), que também está disponível (e que é uma atualização do módulo dsd.py, que está disponível em um repositório próprio).

## Etapa 2. urls_pautas.py

Depois de extraídos os dados das datas das pautas, este código lê as informações e constrói urls adequadas para acessar os dados contidos nas páginas relativas a cada uma das sessões realizadas.

Esse arquivo lê os dados contidos na pasta '/dadas_pautas' e gera dois arquivos com as urls, correspondentes aos formatos das sessões presenciais e virtuais, que têm modelos diferentes de construção.
Os arquivos gerados em 12/11/2023 estão neste repositório.

## Etapa 3. 
