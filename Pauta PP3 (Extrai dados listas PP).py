# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:11:17 2023

@author: Alexandre Araújo Costa
"""

import urllib3
import pandas as pd
import json

import dsl
urllib3.disable_warnings()

source = 'data\\dados_pautas_presenciais_processados.txt'
out= 'data\\processos_julgados_presencial_TP_'
url = 'https://portal.stf.jus.br/pauta/services/lista-service.asp?lista='
# processa presenciais

listas0 = pd.read_csv(source)


listas = listas0.values.tolist()

lista_buscar = []
dados_a_gravar = []
lista_vazia = []
n = 0


for lista in listas:
    if lista[2] == 'TP':
    # if lista[2] == '1T':
    # if lista[2] == '2T':

        lista_buscar.append(lista)

for lista in lista_buscar[n:]:


    lista_id = str(lista[15])
  
    incidentes0 = (dsl.get(url+lista_id))
    incidentes = json.loads(incidentes0)
    
    for incidente in incidentes:
        inc_cadeia = incidente['cadeia']
        inc_classe = incidente['classe']
        inc_id = incidente['id']
        inc_numero = incidente['numero']
        inc_procedencia = incidente['procedencia']
        inc_partes = incidente['partes']
        inc_polo_ativo_nome = inc_partes[0]['nome']
        inc_polo_ativo_tipo = inc_partes[0]['categoria'].replace('.(S)','')
        
        dados_a_acrescentar = [
                inc_cadeia,
                inc_classe,
                inc_id,
                inc_numero,
                inc_procedencia,
                inc_partes,
                inc_polo_ativo_nome,
                inc_polo_ativo_tipo]
        
        dados_incidente = lista + dados_a_acrescentar
        
        dados_a_gravar.append(dados_incidente)

colunas = list(listas0.columns)
colunas.extend(['inc_cadeia',
                'inc_classe',
                'inc_id',
                'inc_numero',
                'inc_procedencia',
                'inc_partes',
                'inc_polo_ativo_nome',
                'inc_polo_ativo_tipo'
    ])

df = pd.DataFrame(dados_a_gravar, columns = colunas)
df.to_csv(out+'final.csv', index=False)
df.to_excel(out+'final.xlsx', index=False)