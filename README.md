# STF-Pauta: extração dos dados das pautas

## Etapa 1. extrator_datas_pautas.py

Este programa abre as páginas do STF que definem as datas das pautas presenciais e do Plenário Virtual.

Ele grava na pasta '/datas_pautas' (que deve ser criada para esse fim) os  dados acerca de quais são as datas em que houve pautas presenciais e também início e fim das pautas virtuais, informações que são necessárias para construir os urls para identificar os dados de julgamento de cada sessão pautada.
Este e outros programas utilizam funções do módulo dsl.py (Data Science and Law), que também está disponível (e que é uma atualização do módulo dsd.py, que está disponível em um repositório próprio).

## Etapa 2. urls_pautas.py

Depois de extraídos os dados das datas das pautas, este código lê as informações e constrói urls adequadas para acessar os dados contidos nas páginas relativas a cada uma das sessões realizadas.

Esse arquivo lê os dados contidos na pasta '/dadas_pautas' e gera dois arquivos com as urls, correspondentes aos formatos das sessões presenciais e virtuais, que têm modelos diferentes de construção.
Os arquivos gerados em 12/11/2023 estão neste repositório.

## Etapa 3. pautas_presenciais.py e pautas_virtuais.py
Estes arquivos processam os documentos gerados na fase anterior e produzem uma tabela com todos os dados relativos a cada data de sessão (nas quais pode haver uma ou várias sessões).
Processamos separadamente as sessões virtuais e as presenciais, cujas informações têm estruturas ligeiramente diversas, produzindo assim documentos com todos os dados relativos às sessões de julgamento.
Retornam: pautas_presenciais_dados.txt e pautas_presenciais_dados.txt

## Etapa 4. processa_listas_presenciais.py e processa_listas_virtuais.py
Nesta etapa, os dados das sessões são processados para extrair dele o conteúdo dos julgamentos.
No caso das sessões presenciais, há produção de dados de julgamentos de processos isolados e de listas.
No caso das sessões virtuias, há produção dos dados das listas de julgamento.
Retornam: dados_pautas_presencial.txt e dados_pautas_virtual.txt
