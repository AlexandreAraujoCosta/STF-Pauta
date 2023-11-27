# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 10:42:59 2023

@author: Alexandre Araújo Costa
"""

import urllib3
import pandas as pd


import dsl
from helpers import DATA_PATH
urllib3.disable_warnings()

origem = 'P1r pautas_dados.txt'
pautas_virtuais_lista = []
pautas_presenciais_lista = []
pautas_presenciais_urls = []
pautas_virtuais_urls = []

origem_lista = pd.read_csv(DATA_PATH/origem, dtype={"teste": str}).values.tolist()

# separa sessões virtuais e presenciais
for item in origem_lista:
    pauta_presencial = 'NA'
    pauta_virtual = 'NA'
    dados = 'NA'
    
    mes = item[1]
    if int(mes)<10:
        mes = '0'+ str(mes)
    ano = item[0]
    dados = item[3]
    
    dados = dados.split('"julgamentosVirtuais":')
    pauta_presencial = dados[0].strip('{"diasPresenciais":')[1:-2]
    pauta_virtual = dados[1][1:-2]
    # print (pauta_virtual)

    #  processa pautas presenciais
    if len(pauta_presencial) > 0:
        if ',' in pauta_presencial:
            pautas_presenciais = pauta_presencial.split(',')
        else:
            pautas_presenciais = [pauta_presencial]
                
        for dia in pautas_presenciais:
            if int(dia)<10:
                dia = '0'+dia
            tipo='sessao-presencial'
            data = str(dia) + '/' + str(mes)+ '/' +str(ano)
            
            pautas_presenciais_lista.append([tipo,data])
            
    # processa pautas virtuais
    if len(pauta_virtual) > 0 :
        pautas_virtuais = pauta_virtual.split('},')
        print (pautas_virtuais)
        
        for item in pautas_virtuais:
            tipo = 'sessao-virtual'
            data_inicial        = dsl.extract(item,'dataInicial":"','"')
            data_final          = dsl.extract(item,'"dataFinal":"','"')
            qtdPlenario         = dsl.extract(item,'qtdProcessosPlenario":"','"')
            qtdPrimeiraTurma    = dsl.extract(item,'qtdPrimeiraTurma":"','"')
            qtdSegundaTurma     = dsl.extract(item,'qtdSegundaTurma":"','"')
            
            pautas_virtuais_lista.append([tipo,
                                          data_inicial,
                                          data_final,
                                          qtdPlenario,
                                          qtdPrimeiraTurma,
                                          qtdSegundaTurma])
        
# gera urls pautas presenciais
for item in pautas_presenciais_lista:
    url = f'https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=sessao-presencial&data={item[1]}'
    pautas_presenciais_urls.append(url)
    
# gera urls pautas virtuais
for item in pautas_virtuais_lista:
    url = f'https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=sessao-virtual&inicio={item[1]}&fim={item[2]}'
    if url not in pautas_virtuais_urls:
        pautas_virtuais_urls.append(url)


# grava arquivos com listas de url
df = pd.DataFrame(pautas_virtuais_urls, columns=["url"])
df.to_csv(DATA_PATH/'pautas_virtuais_urls.txt', index=False)

df2 = pd.DataFrame(pautas_presenciais_urls, columns=["url"])
df2.to_csv(DATA_PATH/'pautas_presenciais_urls.txt', index=False)