# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:11:17 2023

@author: Alexandre Araújo Costa
"""

import pandas as pd
import dsl

dados_a_gravar = []
id_list = []
source = 'pautas_virtuais_dados.txt'

def processar_lista (listas_string):
    listas = listas_string.split('"idTipo":"')[1:]
    
    for lista in listas:
        tipo = lista[0]
        tipo_desc = dsl.extract(lista,'"descricao":"','"')
        
        # tipo_desc = tipo_desc.replace('Listas dos Relatores (incidentes e recursos - todas as classes)','incidentes&recursos')
        # tipo_desc = tipo_desc.replace('Listas dos Relatores (mérito, exceto controle concentrado)','geral')
        # tipo_desc = tipo_desc.replace('Listas de Devoluções de Vistas','vistasdevolução')
        # tipo_desc = tipo_desc.replace('Listas dos Relatores em ações de controle concentrado (mérito)','controleconcentradomérito')
        
        lista = dsl.extract(lista, '"ministros":[{','')
        lista = lista.replace('ministra','ministro')
        lista = lista.replace('ministro','MIN.')
        
        listasplit = lista.split('"nome":"MIN. ')[1:]
        print (listasplit)
        for elemento in listasplit:
            elementosplit = elemento.split('","listaJulgamento":[{')
            relator = dsl.remover_acentos(elementosplit[0].upper())
            dados_lista = elementosplit[1].split('"id":"')[1:]
            for objeto in dados_lista:
                objeto = objeto.split('}')[0].strip('"')
                lista_id = dsl.extract(objeto, '', '","')
                lista_desc = dsl.extract(objeto, '"descricao":"', '","')
                lista_ordem = dsl.extract(objeto, '"ordem":"', '","')
                lista_quantidade = dsl.extract(objeto, '"quantidadeProcessos":"', '"')
                lista_dados = [orgao,data_inicial,data_final,tipo,tipo_desc,relator,lista_id,lista_desc,lista_ordem,lista_quantidade]
                id_list.append([lista_id,orgao])
                dados_a_gravar.append(lista_dados)
        
    return ([listas])

virtuais = pd.read_csv(source, dtype={"teste": str}).values.tolist()

presenciais_dados = []
for item in virtuais:

    tipo = item[2]
    dados = item[3]
    
    data_inicial = dsl.extract(item[0],'"inicio":"','"')
    data_final = dsl.extract(item[0],'"fim":"','"')
    
    # processa T1
    dados_T1 = dsl.extract(dados,'"codigo":"1T",','"codigo":"2T"').replace('"descricao":"Primeira Turma","sessoes":[','')
    orgao = 'T1'
    retorno = processar_lista(dados_T1)    
    
    # processa T2
    dados_T2 = dsl.extract(dados,'"codigo":"2T",','"codigo":"TP",').replace('"descricao":"Segunda Turma","sessoes":[','')
    orgao = 'T2'
    
    # # processa TP
    dados_TP = dsl.extract(dados,'"codigo":"TP",','"codigo":"1T"').replace('"descricao":"Plenário","sessoes":[','')
    orgao = 'TP'

df = pd.DataFrame(id_list, columns=['id_lista',
                                    'orgão'])
df.to_csv('lista_id_pautas_virtual.txt', index=False)

df = pd.DataFrame(dados_a_gravar, columns=['orgao',
                                    'data_inicial',
                                    'data_final',
                                    'tipo',
                                    'tipo_desc',
                                    'relator',
                                    'lista_id',
                                    'lista_desc',
                                    'lista_ordem',
                                    'lista_quantidade'])
df.to_csv('dados_pautas_virtual.txt', index=False)

