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

presenciais = pd.read_csv(DATA_PATH/'pautas_presenciais_urls.txt', dtype={"teste": str}).values.tolist()

presenciais_dados = []
presenciais_vazias = []
n = 0
for url in presenciais:
    time.sleep(1)
    n = n + 1
    url=url[0]
    dados = dsl.get(url)
    
    print (str(n) + ' de ' + str(len(presenciais)) + ' - ' + check_for_captcha(dados) + ' - ' + dados[:50])
        
    dsl.esperar(200,300,n)
    
    
    date = dsl.extract(dados,'"data":"','"')
    tipo = dsl.extract(dados,'"tipo":"','"')
    colegiados = dsl.extract(dados,'"colegiados":','')
    
    dados_a_gravar  = ([dados,
                        date,
                        tipo,
                        colegiados
                        ])
    
    if '"colegiados":[]' in dados:
        presenciais_vazias.append(dados_a_gravar)
        print(dados)
    else:
        presenciais_dados.append(dados_a_gravar)
    
df = pd.DataFrame(presenciais_dados, columns=['dados',"data",'tipo','colegiados'])
df.to_csv(DATA_PATH/'pautas_presenciais_dados.txt', index=False)

df2 = pd.DataFrame(presenciais_vazias, columns=['dados',"data",'tipo','colegiados'])
df2.to_csv(DATA_PATH/'pautas_presenciais_vazias.txt', index=False)
