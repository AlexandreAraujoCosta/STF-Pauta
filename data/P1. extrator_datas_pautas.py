# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 22:43:11 2023

@author: Alexandre Araújo Costa
"""

import urllib3
import pandas as pd

import dsl
import json
from helpers import DATA_PATH
urllib3.disable_warnings()

inicio = 2003
fim = 2023
path = 'datas_pautas\\'
processos_pautados = []
pautas_presenciais_urls = []
pautas_virtuais_urls = []
dados_pautas_PV = []

# cria urls para busca dos dados das pautas, que são gravados no STF com base em mês e ano.
for n in range (fim-inicio+1):

    ano = str(fim-n)
    
    for mes in range (12):
        
        mes = mes+1
        if mes > 9:
            month = str(mes)
        else:
            month = '0' + str(mes)
            
        url = 'https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=calendarios&mes=' + month + '&ano=' + str(ano)
        
        print (url)

# busca os dados no modelo de url.
        dados_pautas0 = dsl.get(url)
        dados_pautas = json.loads(dados_pautas0)
        
        dias_presenciais = dados_pautas['diasPresenciais']

# gera urls das pautas presenciais
        for dia in dias_presenciais:
            dia = str(dia)
            if len(dia) == 1:
                dia = '0' + dia
            data = dia + '/' + month + '/' + ano
            url_presencial = f'https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=sessao-presencial&data={data}'
            pautas_presenciais_urls.append(url_presencial)
        
# gera urls das pautas virtuais
        julgamentos_virtuais = dados_pautas['julgamentosVirtuais']
        
        for sessao in julgamentos_virtuais:
            data_inicial = sessao['dataInicial']
            data_final = sessao['dataFinal']
            sessao_TP_qnt = sessao['qtdPrimeiraTurma']
            sessao_1T_qnt = sessao['qtdProcessosPlenario']
            sessao_2T_qnt = sessao['qtdSegundaTurma']
            
            url_PV = f'https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=sessao-virtual&inicio={data_inicial}&fim={data_final}'
            if url_PV not in pautas_virtuais_urls:
                pautas_virtuais_urls.append(url_PV)
                
                dados_pautas_PV.append([     data_inicial + '_' + data_final,
                                             sessao_TP_qnt, 
                                             sessao_1T_qnt, 
                                             sessao_2T_qnt
                                             ])
        
df = pd.DataFrame(dados_pautas_PV , columns = ['sessao',
                                                     'sessao_TP_qnt', 
                                                     'sessao_1T_qnt', 
                                                     'sessao_2T_qnt' ])
df.to_csv(DATA_PATH/'dados_pautas_PV.csv', index=False)
df.to_excel(DATA_PATH/'dados_pautas_PV.xlsx', index=False)


df = pd.DataFrame(pautas_virtuais_urls, columns = ['url_PV' ])
df.to_csv(DATA_PATH/'pautas_virtuais_urls.csv', index=False)
df.to_excel(DATA_PATH/'pautas_virtuais_urls.xlsx', index=False)

df2 = pd.DataFrame(pautas_presenciais_urls, columns=["url_presenciais"])
df2.to_csv(DATA_PATH/'pautas_presenciais_urls.csv', index=False)
df.to_excel(DATA_PATH/'pautas_virtuais_urls.xlsx', index=False)
