# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 16:54:44 2023

@author: Alexandre Araújo Costa
"""

import time
import urllib3
import pandas as pd

import dsl
from helpers import DATA_PATH
urllib3.disable_warnings()

source = DATA_PATH/'pautas_virtuais_dados_processados.txt'
url = 'https://portal.stf.jus.br/pauta/services/lista-service.asp?lista='
url2 = 'https://sistemas.stf.jus.br/repgeral/votacao?sessaoVirtual='
url3 = 'https://sistemas.stf.jus.br/repgeral/votacao?oi='
# processa presenciais

listas0 = pd.read_csv(source, dtype={"teste": str})
listas = listas0.values.tolist()

lista_buscar = []
dados_a_gravar = []
lista_vazia = []
n = 0
start = 500

for lista in listas:
    if lista[0] == 'TP':
    # if lista[0] == 'T1':
    # if lista[0] == 'T2':

        lista_buscar.append(lista)

for lista in lista_buscar[start:]:
# for lista in lista_buscar:

    colunas =   [ 'incidente',
                'identificador',
                'identificacao',
                'identCompleta',
                 'principal',
                 'pai',
                'incidente_tipo',  
                 'classe',
                 'numero',
                 'string',
                 'procedencia',
                 'partes',
                 'autor_tipo',
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
                 'lista_quantidade']
    
    if n%500 == 0 and n != 0:
        print ('gravando')
        df = pd.DataFrame(dados_a_gravar, columns = colunas)
        df.to_csv('processos_julgados_virtual_TP' + str(n+start) +'.txt', index=False)
        dados_a_gravar = []
    
    incidente = 'NA'
    classe = 'NA'
    numero = 'NA'
    string = 'NA'
    procedencia = 'NA'
    partes = 'NA'
    autor_tipo = 'NA'
    identificador   = 'NA'
    identificacao   = 'NA'
    identCompleta   = 'NA'
    principal       = 'NA'
    pai             = 'NA'
    incidente_tipo  = 'NA'
    dados2 = 'NA'
    dados3 = 'NA'
    dados_julgamento = 'NA'
    dados_oi = 'NA'
    dados_oi0 = 'NA'
    dados = 'NA'
    
    time.sleep(1)
    n = n + 1
    
    lista_id = str(lista[6])
  
    dados = dsl.get(url+lista_id)
        
    dsl.esperar(151,120,n)
    
    print (str(n) + ' de ' + str(len(lista_buscar) - start) + ' - ' + dados[:50])
    
    if dados == '[]':
        print('lista vazia')
        lista_vazia.append(url + lista_id)
        processos = ['lista vazia']
    else:    
        processos = dados.split('{"id":"')[1:]
    
    for processo in processos:

        incidente = 'NA'
        classe = 'NA'
        numero = 'NA'
        string = 'NA'
        procedencia = 'NA'
        partes = 'NA'
        autor_tipo = 'NA'
        identificador   = 'NA'
        identificacao   = 'NA'
        identCompleta   = 'NA'
        principal       = 'NA'
        pai             = 'NA'
        incidente_tipo  = 'NA'
        dados2 = 'NA'
        dados3 = 'NA'
        dados_julgamento = 'NA'
        dados_oi = 'NA'
        dados_oi0 = 'NA'
        dados = 'NA'

        # extrai dados do processo principal, que tem cadeia = 'null'
        if '"cadeia":null' in processo:
        
            incidente = dsl.extract(processo,'','"')
            classe = dsl.extract(processo,'"classe":"','"')
            numero = dsl.extract(processo,'"numero":"','"')
            string = ''
            procedencia = dsl.extract(processo,'"procedencia":"','"')
            partes = dsl.extract(processo,'"partes":','')
            autor_tipo = dsl.extract(partes,'[{"categoria":"','"')

            dados2 = dsl.get(url2+incidente)
        

                
            identificador   = dsl.extract(dados2,'"id" : ',',')
            identificacao   = dsl.extract(dados2,'"identificacao" : "','"')
            identCompleta   = dsl.extract(dados2,'"identificacaoCompleta" : "','"')
            principal       = dsl.extract(dados2,'"principal" : ',',')
            pai             = dsl.extract(dados2,'""pai" : ','"')
            incidente_tipo = dsl.limpar(dsl.extract(dados2,'"tipoObjetoIncidente" : {','}'))
            dados_julgamento = dados2
        
        # busca dados objeto incidente, que têm nomes específicos na cadeia
        else:
            
            incidente = dsl.extract(processo,'','"')
            classe = dsl.extract(processo,'"classe":"','"')
            numero = dsl.extract(processo,'"numero":"','"')
            string = dsl.extract(processo,'cadeia":"','"')
            procedencia = dsl.extract(processo,'"procedencia":"','"')
            partes = dsl.extract(processo,'"partes":','')
            autor_tipo = dsl.extract(partes,'[{"categoria":"','"')
            
            dados_oi0 = dsl.get(url3 + incidente)

            
            
            dados_oi= dados_oi0.split('"objetoIncidente" : ')[1:]
            for objetoIncidente in dados_oi:
                if '"'+string in objetoIncidente:
                    identificador   = dsl.extract(objetoIncidente,'"id" : ',',')
                    identificacao   = dsl.extract(objetoIncidente,'"identificacao" : "','"')
                    identCompleta   = dsl.extract(objetoIncidente,'"identificacaoCompleta" : "','"')
                    principal       = dsl.extract(objetoIncidente,'"principal" : ',',')
                    pai             = dsl.extract(objetoIncidente,'""pai" : ','"')
                    incidente_tipo = dsl.limpar(dsl.extract(objetoIncidente,'"tipoObjetoIncidente" : {','}'))
                    
                    dados_julgamento = dsl.get(url2+identificador)

    
        dados_processo = [incidente,
                          identificador,
                          identificacao,
                          identCompleta,
                          principal,
                          pai,
                          incidente_tipo,
                          classe,
                          numero,
                          string,
                          procedencia,
                          partes, 
                          autor_tipo,
                          dados_julgamento] + lista
        
        
        dados_a_gravar.append(dados_processo)
        

    
# df = pd.DataFrame(dados_a_gravar, columns = [colunas])
# df.to_csv('processos_julgados_virtual_TP_final.txt', index=False)
