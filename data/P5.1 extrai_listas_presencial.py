# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:11:17 2023

@author: Alexandre Araújo Costa
"""

import urllib3
import pandas as pd

import dsl
urllib3.disable_warnings()

source = 'data\\dados_pautas_presenciais_processados.txt'
out= 'data\\processos_julgados_presencial_TP_'
url = 'https://portal.stf.jus.br/pauta/services/lista-service.asp?lista='
# processa presenciais

listas0 = pd.read_csv(source, dtype={"teste": str})
listas = listas0.values.tolist()

lista_buscar = []
dados_a_gravar = []
lista_vazia = []
n = 0
start = 1
# end = 520

for lista in listas:
    if lista[0] == 'TP':
    # if lista[0] == 'T1':
    # if lista[0] == 'T2':

        lista_buscar.append(lista)

# for lista in lista_buscar[start:end]:
for lista in lista_buscar:

    colunas =   [ 'incidente',
                  'classe',
                  'numero',
                  'string',
                  'procedencia',
                  'partes',
                  'autor_tipo',
                  'orgao',
                  'id_sessao',
                  'data_inicial',
                  'hora_inicial',
                  'data_final',
                  'sessao_tipo',
                  'sessao_n',
                  'lista_tipo',
                  'tipo_desc',
                  'relator',
                  'lista_id',
                  'lista_desc',
                  'lista_ordem',
                  'lista_quantidade']
    
    if n%500 == 0 and n != 0:
        print ('gravando')
        df = pd.DataFrame(dados_a_gravar, columns = colunas)
        df.to_csv(out + str(n+start) +'.txt', index=False)
        dados_a_gravar = []
    
    incidente = 'NA'
    classe = 'NA'
    numero = 'NA'
    string = 'NA'
    procedencia = 'NA'
    partes = 'NA'
    autor_tipo = 'NA'

    dados2 = 'NA'
    dados3 = 'NA'
    dados_oi = 'NA'
    dados_oi0 = 'NA'
    dados = 'NA'
    
#     time.sleep(1)
    n = n + 1
    
    lista_id = str(lista[10])
  
    dados = dsl.get(url+lista_id)
        
#     dsl.esperar(151,120,n)
    
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
        dados2 = 'NA'
        dados3 = 'NA'
        dados_julgamento = 'NA'
        dados_oi = 'NA'
        dados_oi0 = 'NA'
        dados = 'NA'


        incidente = dsl.extract(processo,'','"')
        classe = dsl.extract(processo,'"classe":"','"')
        numero = dsl.extract(processo,'"numero":"','"')
        string = dsl.extract(processo,'cadeia":"','"')
        procedencia = dsl.extract(processo,'"procedencia":"','"')
        partes = dsl.extract(processo,'"partes":','')
        autor_tipo = dsl.extract(partes,'[{"categoria":"','"')
    
        dados_processo = [incidente,
                          classe,
                          numero,
                          string,
                          procedencia,
                          partes, 
                          autor_tipo] + lista
        
        
        dados_a_gravar.append(dados_processo)
        

    
df = pd.DataFrame(dados_a_gravar, columns = [colunas])
df.to_csv(out+'final.txt', index=False)