# STF-Pauta: extração dos dados das pautas

## Etapa 1: P1 extrator_datas_pautas.py

Este programa abre as páginas do STF que definem as datas das pautas presenciais e do Plenário Virtual, identifica aquelas em que há pautas com processos indicados (virtuais e presenciais) e grava as informações necessárias para definir as urls onde estão gravados os dados de julgamento de cada sessão pautada.
Este e outros programas utilizam funções do módulo dsl.py (Data Science and Law), que também está disponível (e que é uma atualização do módulo dsd.py, que está disponível em um repositório próprio).
#### Retorna: P1r pautas_dados.txt

## Etapa 2: P2 urls_pautas.py

Depois de extraídos os dados das d das pautas, este código lê as informações e constrói urls adequadas para acessar os dados contidos nas páginas relativas a cada uma das sessões realizadas.

Esse arquivo lê os dados contidos no arquivo urls_pautas.py e gera dois arquivos com as urls, correspondentes aos formatos das sessões presenciais e virtuais, que têm modelos diferentes de construção.
Os arquivos gerados em 14/11/2023 estão neste repositório.
#### Retorna: pautas_presenciais_urls.txt e pautas_virtuais_urls.txt

## Etapa 3: P3.1 pautas_presenciais.py e P3.2 pautas_virtuais.py
Estes arquivos processam os documentos gerados na fase anterior e produzem uma tabela com todos os dados relativos a cada data de sessão (nas quais pode haver uma ou várias sessões).
Processamos separadamente as sessões virtuais e as presenciais, cujas informações têm estruturas ligeiramente diversas, produzindo assim documentos com todos os dados relativos às sessões de julgamento.
#### Retornam: pautas_presenciais_dados.txt, pautas_presenciais_vazias.txt e pautas_virtuais_dados.txt

## Etapa 4. P4.1 processa_listas_presenciais.py (em desenvolvimento) e P4.2 processa_listas_virtuais.py
Nesta etapa, os dados das sessões são processados para extrair dele o conteúdo dos julgamentos.
No caso das sessões presenciais, há produção de dados de julgamentos de processos isolados e de listas.
No caso das sessões virtuias, há produção dos dados das listas de julgamento.
#### Retornam: pautas_virtuais_dados_processados.txt

## Etapa 5. P5.2 extrai_pautas_virtuais.py
Nesta etapa, o código processa o arquivo pautas_virtuais_dados_processados.txt e busca no site do STF dados nas 3 urls que oferecem informações sobre pautas (https://portal.stf.jus.br/pauta/services/lista-service.asp?lista='), sobre votações (https://sistemas.stf.jus.br/repgeral/votacao?oi=') e sobre os votos individualizados ('https://sistemas.stf.jus.br/repgeral/votacao?sessaoVirtual=').
Esses dados são combinados para formar o arquivo processos_julgados_virtual.txt, que pode ser feito para todos os processos ou para um órgão específico (TP, T1 e T2).
Fiz, por enquanto, apenas a coleta do TP, pois esse é um processo bastante longo. Com a minha máquina e meu acesso, sáo várias horas de coleta, gerando arquivos muito grandes. Para evitar perdas com eventuais suspensões, os arquivos são gravados em lotes de 500 processos (que geram cerca de 800 entradas), e que podem ser posteriormente recombinados por meio do junta_dados.py.
#### Retorna: processos_julgados_virtual???.txt

## Etapa final. P6.2
Na última etapa, os dados catalogados são processados, gerando-se duas tabelas: uma que tem como unidade de análise (linha) os votos individualizados e outra com os processos (com informações sobre a ordem das votações).
#### Retorna: votos_PV.txt e processos_PV.txt; votos_PV.xlsx e processos_PV.xlsx

## Download arquivos finais: 
#### Processos_PV.txt (https://drive.google.com/file/d/16i1VJbrI6Ruu4OzhPkKkfz-LUdcGp7iT/view?usp=drive_web)
#### Votos_PV.txt (https://drive.google.com/file/d/1-FFupf5cBcm4hb-RO_5q8vpKpy_JUgrq/view?usp=drive_web)
