# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:11:17 2023

@author: Alexandre Araújo Costa
"""

import pandas as pd
import dsl

teste =[]
sessoes_lista = []
dados_a_gravar = []
id_list = []
sem_lista = []
processos_sem_lista = []
listas_de_julgamento = []
com_lista = []
source = 'data\\pautas_presenciais_dados.txt'

            
def processar_sessao (sessao):
    # print (sessao)
    sessao_id                    = dsl.limpar(dsl.extract(sessao,'','"'))
    sessao_data                  = dsl.extract(sessao,'"dataInicio":"','"').split(' ')
    sessao_data_inicio           = dsl.date(sessao_data[0])
    sessao_hora_inicio           = sessao_data[1]
    sessao_data_fim              = sessao_data_inicio
    sessao_tipo                  = dsl.extract(sessao,'"tipo":"','"')
    sessao_numero                = dsl.extract(sessao,'numero":"','"') + '/' + dsl.extract(sessao,'ano":"','"')
    sessao_obs                   = dsl.extract(sessao,'"observacao":"','"')
    sessao_incidentes            = dsl.extract(sessao,'"incidentes":[{"','"listas":')
    sessao_listas                = dsl.extract(sessao,'"listas":','').strip('[]}]}]}')
    sessao_listas                = sessao_listas.strip(',{')
    if sessao_listas == '':
        sessao_listas = 'NA'
    dados_sessao = [orgao,sessao_id,sessao_data_inicio,sessao_hora_inicio,sessao_data_fim,sessao_tipo,sessao_numero,sessao_obs,sessao_incidentes,sessao_listas]
    return dados_sessao

def processar_sessoes (sessao_string):
    if sessao_string.upper() == 'NA':
        return ('NA')
    else:
        sessao_split = sessao_string.split('"id":"')[1:]

        sessao_item = []
        for item in sessao_split:
            if '"tipo":"' in item:
                sessao_item.append(item)
            else:
                sessao_item[-1] = sessao_item[-1] + 'id":"' + item
                
        for objeto in sessao_item:
            retornar = processar_sessao(objeto)
            sessoes_lista.append(retornar)
        

presenciais = pd.read_csv(source, dtype={"teste": str}).values.tolist()



presenciais_dados = []
# presenciais = presenciais [990:999]

for item in presenciais:

    tipo = item[2]
    dados = item[3]
    
    data_inicial = dsl.extract(item[0],'"data":"','"')
    data_final = data_inicial
    
    # processa T1
    dados_T1 = dsl.extract(dados,'"codigo":"1T",','"codigo":').replace('"descricao":"Primeira Turma","sessoes":[{','')
    orgao = 'T1'
    processar_sessoes(dados_T1)
    
    # processa T2
    dados_T2 = dsl.extract(dados,'"codigo":"2T",','"codigo":').replace('"descricao":"Segunda Turma","sessoes":[{','')
    orgao = 'T2'
    processar_sessoes(dados_T2)
    
    # processa TP
    dados_TP = dsl.extract(dados,'"codigo":"TP",','"codigo":').replace('"descricao":"Plenário","sessoes":[{','')
    orgao = 'TP'
    processar_sessoes(dados_TP)


for item in sessoes_lista:
    if item[-2] != "NA":
        sem_lista.append(item[:-1])

for item in sem_lista:
    processos = item[8].split('cadeia":')[1:]
    for it in processos:
        it = it.split(',')[:-1]
        incidente = item[:-1]+it
        incidente[8] = incidente[8].replace('null','NA')
        incidente[9] = dsl.extract(incidente[9],'"classe":"','"')
        incidente[10] = dsl.extract(incidente[10],'"numero":"','"')
        incidente[11] = dsl.extract(incidente[11],'"relator":"','"').replace('MIN. ','')
        incidente[12] = dsl.extract(incidente[12],'"ministroVista":"','"').replace('null','NA')
        incidente[13] = dsl.extract(incidente[13],'"materiaRelevante":"','"')
        incidente[14] = dsl.extract(incidente[14],'"repercussaoGeral":"','"').replace('null','NA')
        incidente[15] = dsl.extract(incidente[15],'"situacaoProcessoSessao":"','"')
        incidente[16] = dsl.extract(incidente[16],'"idInformacaoPautaProcesso":"','"')
        processos_sem_lista.append(incidente)



for item in sessoes_lista:
    if item[-1] != "NA":
        com_lista.append(item[:-2]+item[-1:])
        
for item in com_lista:
    processos = item[8].split('idTipo":"')[1:]
    for it in processos:
        lista_tipo = dsl.extrair(it,'','"')
        lista_desc = dsl.extract(it, '"descricao":"', '","')
        lista_dados = it.split('{"nome":"')[1:]
        # teste.append(lista_dados)
        
        for it2 in lista_dados:
            ministro = dsl.extrair(it2,'','"')
            listas = dsl.extrair(it2,'listaJulgamento":[','').split('id":"')[1:]
            for it3 in listas:
                lista_id = dsl.extrair(it3,'','"')
                lista_n = dsl.extract(it3, '"descricao":"', '","')
                lista_ordem = dsl.extract(it3, '"ordem":"', '","')
                lista_quantidade = dsl.extract(it3, '"quantidadeProcessos":"', '"')
                listas_de_julgamento.append(item[:7] +[lista_tipo, lista_desc, ministro,lista_id,lista_n,lista_ordem,lista_quantidade])


            
df1 = pd.DataFrame(processos_sem_lista, 
                   columns=['orgao',
                            'id_incidente',
                            'data_inicial',
                            'hora_inicial',
                            'data_final',
                            'tipo_sessão',
                            'lista_n_ano',
                            'sessao_observacao',
                            'incidente_desc',
                            'incidente_classe',
                            'incidente_numero',
                            'incidente_relator',
                            'incidente_ministro_vista',
                            'incidente_materia_relevante',
                            'incidente_rep_geral',
                            'incidente_situacao_proc',
                            'incidente_id'])
df1.to_csv('data\\processos_julgados_sem_lista_processados.txt', index=False)

df2 = pd.DataFrame(listas_de_julgamento, 
                   columns=['orgao',
                            'id_incidente',
                            'data_inicial',
                            'hora_inicial',
                            'data_final',
                            'tipo_sessão',
                            'lista_n_ano',
                            'lista_tipo',
                            'lista_desc',
                            'ministro',
                            'lista_id',
                            'lista_n/ano',
                            'lista_ordem',
                            'lista_quantidade'])
df2.to_csv('data\\dados_pautas_presenciais_processados.txt', index=False)

print('gravando excel')
df1.to_excel('data\\processos_julgados_sem_lista_processados.xlsx', index=False)
df2.to_excel('data\\dados_pautas_presenciais_processados.xlsx', index=False)