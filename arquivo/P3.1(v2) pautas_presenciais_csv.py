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

presenciais = pd.read_csv('data\\pautas_presenciais_urls.txt', dtype={"teste": str}).values.tolist()

presenciais_dados = []
presenciais_vazias = []
colunas = ['data','tipo','colegiado','colegiado_desc','dados']


n = 0
for url in presenciais[9:12]:
# for url in presenciais:
    time.sleep(1)
    n = n + 1
    url=url[0]
    dados = dsl.get(url)
    
    dados_j = json.loads(dados)
    
    colegiados = dados_j['colegiados'][0]
    date = dados_j['data']
    tipo = dados_j['tipo']
    
    colegiado = colegiados['codigo']
    colegiado_desc = colegiados['descricao']
    sessoes = str(json.dumps(colegiados['sessoes'], ensure_ascii=False).encode('utf8'))
    
    
    # dsl.esperar(200,300,n)
    
    print (str(n) + ' de ' + str(len(presenciais)) + ' - ' + dados[:50])

    
    dados_a_gravar  = ([date,
                        tipo,
                        colegiado,
                        colegiado_desc,
                        dados
                        ])
    
    if '"colegiados":[]' in dados:
        presenciais_vazias.append(dados_a_gravar)
        print(dados)
    else:
        presenciais_dados.append(dados_a_gravar)
    
df = pd.DataFrame(presenciais_dados, columns=colunas)
df.to_csv('data\\pautas_presenciais_dados.txt', index=False)

df2 = pd.DataFrame(presenciais_vazias, columns= colunas)
df2.to_csv('data\\pautas_presenciais_vazias.txt', index=False)
