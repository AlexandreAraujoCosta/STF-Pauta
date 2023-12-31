# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 22:43:11 2023

@author: Alexandre Araújo Costa
"""

import urllib3
import pandas as pd

import dsl
from helpers import DATA_PATH
urllib3.disable_warnings()

inicio = 2003
fim = 2023
path = 'datas_pautas\\'
processos_pautados = []

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
        html = dsl.get(url)
        
        # grava apenas se houver dados
        if '"diasPresenciais":[]' in html and '"julgamentosVirtuais":[]' in html:
            processos = 0
        else:
            processos_pautados.append([ano,mes,url,html])

df = pd.DataFrame(processos_pautados, columns=['ano',
                                               'mes',
                                               'url',
                                               'dados'])
df.to_csv(DATA_PATH/'P1r pautas_dados.txt', index=False)