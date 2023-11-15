# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 22:43:11 2023

@author: Alexandre Araújo Costa
"""

import dsl
import pandas as pd

import urllib3
urllib3.disable_warnings()

inicio = 2003
fim = 2023
path = 'datas_pautas\\'
processos_pautados = []

# cria urls para busca dos dados das pautas, que são gravados no STF com base em mês e ano.
for n in range (fim-inicio+1):

    ano = str(fim-n)
    
    for mes in range (12):
        
        if mes > 8:
            month = str(mes+1)
        else:
            month = '0' + str(mes+1)
            
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
df.to_csv('P1r pautas_dados.txt', index=False)