# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:11:17 2023

@author: Alexandre Araújo Costa
"""

import pandas as pd
import json

teste = []
dados_a_gravar_sem_lista = []
dados_a_gravar_lista = []
sessao_data_fim = None

source = 'data\\pautas_presenciais_dados.txt'


presenciais = pd.read_csv(source, dtype={"teste": str}).values.tolist()


presenciais_dados = []
# presenciais = presenciais [:498]

for item in presenciais:
    item_j = json.loads(item[4])
    
    data = item_j['data']
    sessao_tipo = item_j['tipo']
    
    colegiados = item_j['colegiados']
    
    for cj in colegiados:
        
        colegiado = cj['codigo']
        colegiado_desc = cj['descricao']
        colegiado_sessoes = cj['sessoes']
        
        
        for sessao in colegiado_sessoes:
            sessao_id           = sessao['id']
            sessao_numero        = sessao['numero']
            sessao_ano          = sessao['ano']
            sessao_data_inicio  = sessao['dataInicio']
            sessao_data_split   = sessao_data_inicio.split(' ')
            sessao_data_inicio  = sessao_data_split[0]
            sessao_data_inicio  = sessao_data_inicio[-4:]+'-'+sessao_data_inicio[3:5]+'-'+ sessao_data_inicio[:2]
            sessao_hora_inicio  = sessao_data_split[1]
            sessao_tipo         = sessao['tipo']
            sessao_obs          = sessao['observacao']
            sessao_incidentes   = sessao['incidentes']
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
                        
                        dados_lista = [         data,
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

                        dados_a_gravar_lista.append(dados_lista)
                
            
            
            for incidente in sessao_incidentes:
                
                inc_cadeia = incidente['cadeia']
                inc_classe = incidente['classe']
                inc_idInformacaoPautaProcesso = incidente['idInformacaoPautaProcesso']
                inc_materiaRelevante = incidente['materiaRelevante']
                inc_ministroVista  = incidente['ministroVista']
                inc_numero = incidente['numero']
                inc_relator = incidente['relator']
                if inc_relator is not None:
                    inc_relator = inc_relator.replace('MIN. ','')
                inc_repercussaoGeral = incidente['repercussaoGeral']
                inc_situacaoProcessoSessao = incidente['situacaoProcessoSessao']
                
                dados_sem_lista = [         data,
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
                                  inc_cadeia,
                                  inc_classe,
                                  inc_numero,
                                  inc_idInformacaoPautaProcesso,
                                  inc_materiaRelevante,
                                  inc_ministroVista,
                                  inc_relator,
                                  inc_repercussaoGeral,
                                  inc_situacaoProcessoSessao                                  
                                  ]
                
                colunas_sem_lista = ['data',
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
                                  'inc_cadeia',
                                  'inc_classe',
                                  'inc_numero',
                                  'inc_idInformacaoPautaProcesso',
                                  'inc_materiaRelevante',
                                  'inc_ministroVista',
                                  'inc_relator',
                                  'inc_repercussaoGeral',
                                  'inc_situacaoProcessoSessao'
                                  ]
                
                dados_a_gravar_sem_lista.append(dados_sem_lista)


df1 = pd.DataFrame(dados_a_gravar_sem_lista, columns = colunas_sem_lista)
df1.to_csv('data\\processos_julgados_sem_lista_processados.csv', index=False)

df2 = pd.DataFrame(dados_a_gravar_lista, columns = colunas_lista)
df2.to_csv('data\\dados_pautas_presenciais_processados.csv', index=False)

print('gravando excel')
df1.to_excel('data\\processos_julgados_sem_lista_processados.xlsx', index=False)
df2.to_excel('data\\dados_pautas_presenciais_processados.xlsx', index=False)