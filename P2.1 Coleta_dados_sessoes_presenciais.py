# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 16:54:44 2023

@author: Alexandre Araújo Costa
"""

import dsl
import pandas as pd
import time
import json
import urllib3
urllib3.disable_warnings()

# processa presenciais

presenciais = pd.read_csv('data\\pautas_presenciais_urls.csv', dtype={"teste": str}).values.tolist()

presenciais_dados = []
presenciais_vazias = []
colunas = ['data','tipo','colegiado', 'colegiado_desc', 'dados']
n = 0
for url in presenciais:
    time.sleep(1)
    n = n + 1
    url=url[0]
    dados = dsl.get(url)
        
    print (str(n) + ' de ' + str(len(presenciais)) + ' - ' + dados[:100])
    
    dados_j = json.loads(dados)
    
    date = dados_j['data']
    tipo = dados_j['tipo']
    
    for item in dados_j['colegiados']:
    
        colegiado = item['codigo']
        colegiado_desc = item['descricao']
        
        dados_a_gravar  = ([date,
                            tipo,
                            colegiado,
                            colegiado_desc,
                            dados
                            ])
        
        presenciais_dados.append(dados_a_gravar)
    
df = pd.DataFrame(presenciais_dados, columns = colunas)
df.to_csv('data\\pautas_presenciais_dados.csv', index=False)

