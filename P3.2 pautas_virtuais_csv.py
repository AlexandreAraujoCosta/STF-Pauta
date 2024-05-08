# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 16:54:44 2023

@author: Alexandre Araújo Costa
"""

import time
import urllib3
import pandas as pd
import json
import dsl
from helpers import DATA_PATH, check_for_captcha

urllib3.disable_warnings()

# processa presenciais

virtuais = pd.read_csv(DATA_PATH/'pautas_virtuais_urls.csv', dtype={"teste": str}).values.tolist()

virtuais_dados = []

colunas = ['data','tipo','colegiado','colegiado_desc','dados']


n = 0
for url in virtuais:
    time.sleep(1)
    n = n + 1
    url=url[0]
    dados = dsl.get(url)

    print (str(n) + ' de ' + str(len(virtuais)) + ' - ' + check_for_captcha(dados) + ' - ' + dados[:50])
        
    # dsl.esperar(200,300,n)
    
    dados_j = json.loads(dados)
    
    for colegiados in dados_j['colegiados']:
        date = str(dados_j['inicio'] + '_' + dados_j['fim'])
        tipo = dados_j['tipo']
        
        colegiado = colegiados['codigo']
        colegiado_desc = colegiados['descricao']
        
        
        dados_a_gravar  = ([date,
                            tipo,
                            colegiado,
                            colegiado_desc,
                            dados
                            ])
        
        virtuais_dados.append(dados_a_gravar)
    
df = pd.DataFrame(virtuais_dados, columns = colunas)
df.to_csv(DATA_PATH/'pautas_virtuais_dados.csv', index=False)
