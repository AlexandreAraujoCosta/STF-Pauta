# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 16:54:44 2023

@author: Alexandre Araújo Costa
"""

import dsl
import pandas as pd
import time

import urllib3
urllib3.disable_warnings()

# processa presenciais

presenciais = pd.read_csv('pautas_presenciais_urls.txt', dtype={"teste": str}).values.tolist()
virtuais = pd.read_csv('pautas_virtuais_urls.txt', dtype={"teste": str}).values.tolist()

presenciais_dados = []
n = 0
for url in presenciais[:10]:
    time.sleep(1)
    n = n + 1
    url=url[0]
    dados = dsl.get(url)
    # if 'CAPTCHA' in dados or 'The page cannot be displayed because an internal server error has occurred' in dados:
    if 'CAPTCHA' in dados:
        captcha = 'captcha'
        time.sleep(300)
        dados = dsl.get(url)
        if 'CAPTCHA' in dados or 'The page cannot be displayed because an internal server error has occurred' in dados:
            captcha = 'captcha'
            time.sleep(600)
            dados = dsl.get(url)
        
    else:
        captcha = 'nao-captcha'
        
    dsl.esperar(200,300,n)
    
    print (str(n) + ' de ' + str(len(presenciais)) + ' - ' + captcha + ' - ' + dados[:50])
    
    date = dsl.extract(dados,'"data":"','"')
    tipo = dsl.extract(dados,'"tipo":"','"')
    colegiados = dsl.extract(dados,'"colegiados":','')
    
    presenciais_dados.append([dados,
                              date,
                              tipo,
                              colegiados
                              ])
    
df = pd.DataFrame(presenciais_dados, columns=['dados',"data",'tipo','dados'])
df.to_csv('pautas_presenciais_dados.txt', index=False)
