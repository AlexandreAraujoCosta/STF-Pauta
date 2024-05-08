# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:11:17 2023

@author: Alexandre Araújo Costa
"""

import pandas as pd
import json
from helpers import DATA_PATH, check_for_captcha

teste = []
dados_a_gravar = []
id_list = []
sessao_numero = None
sessao_obs = None
sessao_id = None

source = DATA_PATH/'pautas_virtuais_dados.csv'

virtuais = pd.read_csv(source, dtype={"teste": str}).values.tolist()

presenciais_dados = []
for item in virtuais:

    data = item[0]
    sessao_tipo = item[1]
    colegiado = item[2]
    colegiado_desc = item[3]
    sessao_dados = json.loads(item[4])
    
    sessao_data_inicio = sessao_dados['inicio']
    sessao_data_fim = sessao_dados['fim']
    sessao_tipo2 = sessao_dados['tipo']
    colegiados = sessao_dados['colegiados']
    
    for cj in colegiados:
        
        colegiado2 = cj['codigo']
        colegiado_desc2 = cj['descricao']
        colegiado_sessoes = cj['sessoes']
        
        for sessao in colegiado_sessoes:
            sessao_data_inicio  = sessao['dataInicio']
            sessao_data_split   = sessao_data_inicio.split(' ')
            sessao_data_inicio  = sessao_data_split[0]
            sessao_data_inicio  = sessao_data_inicio[-4:]+'-'+sessao_data_inicio[3:5]+'-'+ sessao_data_inicio[:2]
            sessao_ano = sessao_data_inicio[:4]
            sessao_hora_inicio  = sessao_data_split[1]
            sessao_data_fim = sessao['dataFinal'].split(' ')[0]
            sessao_data_fim  = sessao_data_fim[-4:]+'-'+sessao_data_fim[3:5]+'-'+ sessao_data_fim[:2]
            sessao_listas       = sessao['listas']
            
            for lista in sessao_listas:
                lista_tipo = lista['idTipo']
                lista_desc = lista['descricao']
                lista_ministros = lista['ministros']
                
                for ministro in lista_ministros:
                    lista_ministro = ministro['nome']
                    if lista_ministro is not None:
                        lista_ministro = lista_ministro.replace('MIN. ','')
                    listas_julgamento = ministro['listaJulgamento']
                    
                    for lista_julgamento in listas_julgamento:
                        lista_min_id = lista_julgamento['id']
                        lista_min_desc= lista_julgamento['descricao']
                        lista_min_ordem = lista_julgamento['ordem']
                        lista_min_qtd = lista_julgamento['quantidadeProcessos']
            
    
                    dados_lista = [    data,
                                       sessao_tipo,
                                       colegiado,
                                       colegiado_desc,
                                       sessao_id,
                                       sessao_numero,
                                       sessao_ano,
                                       sessao_data_inicio,
                                       sessao_data_fim,
                                       sessao_hora_inicio,
                                       sessao_tipo,
                                       sessao_obs,
                                       lista_tipo,
                                       lista_desc,
                                       lista_ministro,
                                       lista_min_id,
                                       lista_min_desc,
                                       lista_min_ordem,
                                       lista_min_qtd
                                      ]
                    
                    colunas_lista = [ 'data',
                                      'sessao_tipo',
                                      'colegiado',
                                      'colegiado_desc',
                                      'sessao_id',
                                      'sessao_numero',
                                      'sessao_ano',
                                      'sessao_data_inicio',
                                      'sessao_data_fim',
                                      'sessao_hora_inicio',
                                      'sessao_tipo',
                                      'sessao_obs',
                                      'lista_tipo',
                                      'lista_desc',
                                      'lista_ministro',
                                      'lista_min_id',
                                      'lista_min_desc',
                                      'lista_min_ordem',
                                      'lista_min_qtd'
                                      ]

                    dados_a_gravar.append(dados_lista)


df = pd.DataFrame(dados_a_gravar, columns = colunas_lista)
df.to_csv('data\\dados_pautas_virtual.csv', index=False)
df.to_excel('data\\dados_pautas_virtual.xlsx', index=False)
