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

source = 'pautas_virtuais_dados_processados.txt'
url = 'https://portal.stf.jus.br/pauta/services/lista-service.asp?lista='
url2 = 'https://sistemas.stf.jus.br/repgeral/votacao?oi='
url3 = 'https://sistemas.stf.jus.br/repgeral/votacao?sessaoVirtual='
# processa presenciais

listas = pd.read_csv(source, dtype={"teste": str}).values.tolist()

lista_buscar = []
dados_a_gravar = []
n = 0
start = 2000

for lista in listas:
    # if lista[0] == 'TP':
    if lista[0] == 'T1':
    # if lista[0] == 'T2':

        lista_buscar.append(lista)

for lista in lista_buscar[start:]:
    
    if n%500 == 0 and n != 0:
        print ('gravando')
        df = pd.DataFrame(dados_a_gravar, columns=[ 'identificador',
                                                      'identificacao',
                                                      'identCompleta',
                                                      'principal',
                                                      'pai',
                                                      'tipoOIncidente',  
                                                      'incidente',
                                                        'classe',
                                                        'numero',
                                                        'string',
                                                        'procedencia',
                                                        'partes',
                                                        'dados_julgamento',
                                                        'orgao',
                                                        'data_inicial',
                                                        'data_final',
                                                        'tipo',
                                                        'tipo_desc',
                                                        'relator',
                                                        'lista_id',
                                                        'lista_desc',
                                                        'lista_ordem',
                                                        'lista_quantidade'])
        df.to_csv('processos_julgados_virtual_TP' + str(n) +'.txt', index=False)
        dados_a_gravar = []
        
    time.sleep(1)
    n = n + 1
    
    lista_id=str(lista[6])
  
    dados = dsl.get(url+lista_id)

    if 'CAPTCHA' in dados:
        captcha = 'captcha'
        time.sleep(300)
        dados = dsl.get(url)
        if 'CAPTCHA' in dados:
            captcha = 'captcha'
            time.sleep(600)
            dados = dsl.get(url)
        
    else:
        captcha = 'nao-captcha'
        
    dsl.esperar(151,120,n)
    
    print (str(n) + ' de ' + str(len(lista_buscar) - start) + ' - ' + captcha + ' - ' + dados[:50])
    
    if dados == '[]':
        processos = ['lista vazia']
    else:    
        processos = dados.split('{"id":"')[1:]
    
    incidente = 'na'
    classe = 'na'
    numero = 'na'
    string = 'na'
    procedencia = 'na'
    partes = 'na'
    identificador   = 'na'
    identificacao   = 'na'
    identCompleta   = 'na'
    principal       = 'na'
    pai             = 'na'
    tipoOIncidente  = 'na'
    dados2 = 'na'
    dados3 = 'na'
    for processo in processos:
        incidente = dsl.extract(processo,'','"')
        classe = dsl.extract(processo,'"classe":"','"')
        numero = dsl.extract(processo,'"numero":"','"')
        string = dsl.extract(processo,'"cadeia":"','"')
        procedencia = dsl.extract(processo,'"procedencia":"','"')
        partes = dsl.extract(processo,'"partes":','')
        
        # busca dados de cada processo
        dados2 = dsl.get(url2+incidente)
    
        if 'CAPTCHA' in dados2:
            captcha = 'captcha'
            time.sleep(300)
            dados2 = dsl.get(url)
            if 'CAPTCHA' in dados2:
                captcha = 'captcha'
                time.sleep(600)
                dados2 = dsl.get(url)
            
        else:
            captcha = 'nao-captcha'
            
        identificador   = dsl.extract(dados2,'"id" : ',',')
        identificacao   = dsl.extract(dados2,'"identificacao" : "','"')
        identCompleta   = dsl.extract(dados2,'"identificacaoCompleta" : "','"')
        principal       = dsl.extract(dados2,'"principal" : ',',')
        pai             = dsl.extract(dados2,'""pai" : ','"')
        tipoOIncidente  = dsl.limpar(dsl.extract(dados2,'"tipoObjetoIncidente" : {','}'))
        
        # busca dados de cada julgamento
        if identificador == 'na':
            dados3 = 'na'
        else:
            dados3 = dsl.get(url3+identificador)
    
        if 'CAPTCHA' in dados3:
            captcha = 'captcha'
            time.sleep(300)
            dados3 = dsl.get(url)
            if 'CAPTCHA' in dados3:
                captcha = 'captcha'
                time.sleep(600)
                dados3 = dsl.get(url)
            
        else:
            captcha = 'nao-captcha'
            
    
        dados_processo = [identificador,
                          identificacao,
                          identCompleta,
                          principal,
                          pai,
                          tipoOIncidente,                          
                          incidente,
                          classe,
                          numero,
                          string,
                          procedencia,
                          partes, dados3] + lista
        
        dados_a_gravar.append(dados_processo)
        

    
df = pd.DataFrame(dados_a_gravar, columns=[ 'identificador',
                                              'identificacao',
                                              'identCompleta',
                                              'principal',
                                              'pai',
                                              'tipoOIncidente',  
                                              'incidente',
                                                'classe',
                                                'numero',
                                                'string',
                                                'procedencia',
                                                'partes',
                                                'dados_julgamento',
                                                'orgao',
                                                'data_inicial',
                                                'data_final',
                                                'tipo',
                                                'tipo_desc',
                                                'relator',
                                                'lista_id',
                                                'lista_desc',
                                                'lista_ordem',
                                                'lista_quantidade'])
df.to_csv('processos_julgados_virtual_T1_final.txt', index=False)
