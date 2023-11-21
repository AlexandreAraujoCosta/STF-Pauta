# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 16:54:44 2023

@author: Alexandre Araújo Costa
"""

import time
import urllib3
import pandas as pd

import dsl
from helpers import DATA_PATH, check_for_captcha

urllib3.disable_warnings()

# processa presenciais

virtuais = pd.read_csv(DATA_PATH/'pautas_virtuais_urls.txt', dtype={"teste": str}).values.tolist()

virtuais_dados = []
n = 0
for url in virtuais:
    time.sleep(1)
    n = n + 1
    url=url[0]
    dados = dsl.get(url)
    if 'CAPTCHA' in dados:
        captcha = 'captcha'   
    else:
        captcha = 'nao-captcha'
    print (str(n) + ' de ' + str(len(virtuais)) + ' - ' + check_for_captcha(dados) + ' - ' + dados[:50])
        
    dsl.esperar(200,300,n)
    
    date = dsl.extract(dados,'"dataInicio":"','"')
    tipo = dsl.extract(dados,'"tipo":"','"')
    colegiados = dsl.extract(dados,'"colegiados":','')
    
    virtuais_dados.append([dados,
                              date,
                              tipo,
                              colegiados
                              ])
    
df = pd.DataFrame(virtuais_dados, columns=['dados',"data",'tipo','dados'])
df.to_csv(DATA_PATH/'pautas_virtuais_dados.txt', index=False)
