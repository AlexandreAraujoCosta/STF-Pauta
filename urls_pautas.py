# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 10:42:59 2023

@author: Alexandre Araújo Costa
"""

import dsl
import os
import pandas as pd

import urllib3
urllib3.disable_warnings()

path = 'datas_pautas\\'
lista = os.listdir(path)
pautas_virtuais_urls = []
pautas_presenciais_urls = []


for file in lista:
    # Upload data
        
    mes = file[5:7]
    ano = file[7:11]
    
    arquivo = open(path + file, "r", encoding="utf-8")
    html = arquivo.read()#abre html
    arquivo.close()
    html = dsl.trim(html,'urlfim, ','')
    
    pautas = html.split('"julgamentosVirtuais":')
    pauta_presencial = pautas[0].strip('{"diasPresenciais":')[1:-2]
    pauta_virtual = pautas[1][1:-2]

    
# processa pautas virtuais
    pautas_virtuais_lista = []
    if len(pauta_virtual) > 0 :
        pautas_virtuais = pauta_virtual.split('},')
        
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
    #  processa pautas presenciais
    pautas_presenciais_lista = []
    if len(pauta_presencial) > 0:
        pautas_presenciais = pauta_presencial.split(',')
        for dia in pautas_presenciais:
            if int(dia)<10:
                dia = '0'+dia
            tipo='sessao-presencial'
            date = dia+'/'+mes+'/'+ano
            
            pautas_presenciais_lista.append([tipo,date])
        
    # gera urls pautas virtuais
    for item in pautas_virtuais_lista:
        url = f'https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=sessao-virtual&inicio={item[1]}&fim={item[2]}'
        pautas_virtuais_urls.append(url)
    
    # gera urls pautas presenciais
    for item in pautas_presenciais_lista:
        print (pautas_presenciais_lista)
        url = f'https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=sessao-presencial&data={item[1]}'
        pautas_presenciais_urls.append(url)
        
# grava arquivos com listas de url
df = pd.DataFrame(pautas_virtuais_urls, columns=["colummn"])
df.to_csv('pautas_virtuais_urls.txt', index=False)

df = pd.DataFrame(pautas_presenciais_urls, columns=["colummn"])
df.to_csv('pautas_presenciais_urls.txt', index=False)