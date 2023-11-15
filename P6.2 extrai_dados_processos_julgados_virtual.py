# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:11:17 2023

@author: Alexandre Araújo Costa
"""

import pandas as pd
import dsl

dados_a_gravar = []
source = 'total.csv'

dados_df    = pd.read_csv(source, dtype={"teste": str})
dados_lista = dados_df.values.tolist()


processos_PV = []
votos_PV = []
sessoes_PV = []
notavailable = []
lista_vazia = []
available  = []
outros = []
votos_PV_relator = []
votos_info = []
teste =[]

# dados_lista = dados_lista[1023:1123]

# remove processos sem dados adequados
for n in range(len(dados_lista)):
# for index in range(2):
    dados_processo_pautado = dados_lista[n]
    processo_dados = []
    dados_PV = dados_processo_pautado[12]
    
    if dados_processo_pautado[6] == 'lista vazia':
        lista_vazia.append(dados_lista[n])
    
    elif dados_PV == 'na':
        notavailable.append(dados_lista[n])
        
    elif 'listasJulgamento' in dados_PV:
        available.append(dados_processo_pautado)

    else:
        outros.append(dados_lista[n])
        
for item in available:
    df_original = item
    pv = item[12].split('"listasJulgamento" : [ ')
    
    # ajusta parte inicial (especialmente cadeias)
    pv[0] = pv[0].split('"cadeia" : ')
    if 'id' not in pv[0][-1]:
        pv[0] = pv[0][0:-1]
    # if 'cadeia' not in pv[0][0]:
    #     pv[0] = pv[0][1:]
    for n in range(len(pv[0])):
        pv[0][n] = dsl.limpar(dsl.extract(pv[0][n], '"id" : ', ''))
    pv0 = pv[0][0]

    processo_id         = dsl.extract(pv0,'',',')
    processo_ident      = dsl.extract(pv0,'"identificacao" : "','"')
    processo_ident_comp = dsl.extract(pv0,'"identificacaoCompleta" : "','"')
    processo_principal  = dsl.extract(pv0,'"principal" : ','"')
    processo_pai        = dsl.extract(pv0,'"pai" : ','"')
    processo_tipo       = dsl.extract(dsl.extract(pv0,'"tipoObjetoIncidente" : {','}'),'"codigo" : "','"')
    
    # ajusta parte final das listas
    pv1 = pv[1]
    
    processo_listas = pv1.split('"id" : ')[1:]
    len_processo_listas = len(processo_listas)
    
    processo_dados = [processo_id,
                      processo_ident,
                      processo_ident_comp,
                      processo_principal,
                      processo_pai,
                      processo_tipo,
                      len_processo_listas]
    
    lista_ref = 0
    for lista in processo_listas:
        lista_ref = lista_ref+1
        lista_index = -1*len_processo_listas + lista_ref
    
        idLista = dsl.extract(lista,'',',')
        nomeLista = dsl.extract(lista,'"nomeLista" : "','"')
        julgado = dsl.extract(lista,'"julgado" : ',',')
        admiteSustentacaoOral = dsl.extract(lista,'"admiteSustentacaoOral" : ',',')
        
        relator = dsl.limpar(dsl.extract(lista,'ministroRelator" : {','}'))
        relator_codigo = dsl.extract(relator,'codigo" : "','"')
        relator_nome = dsl.extract(relator,'"descricao" : "','"').replace('MIN. ','')
        
        votoRelator = dsl.limpar(dsl.extract(lista,'"votoRelator" : {','}'))
        votoRelator = votoRelator.replace('", "descricao','')
        votoRelator = votoRelator.replace('", "link','')
        votoRelator = votoRelator.strip('"')
        votoRelator = votoRelator.split('" : "')[1:]
        
        relatorioRelator = dsl.limpar(dsl.extract(lista,'"relatorioRelator" : {','}'))
        relatorioRelator = relatorioRelator.replace('", "descricao','')
        relatorioRelator = relatorioRelator.replace('", "link','')
        relatorioRelator = relatorioRelator.strip('"')
        relatorioRelator = relatorioRelator.split('" : "')[1:]
    
        complementoVotoRelator = dsl.extract(lista,'complementoVotoRelator" : "','"')
        
        ministroDestaque = dsl.extract(lista,'ministroDestaque" : "','"')
        ministroVista = dsl.extract(lista,'ministroVista" : "','"')
        ministroVistor = dsl.extract(lista,'ministroVistor" : "','"')
        
        sessao                       = dsl.limpar(dsl.extract(lista,'"sessao" : ','"textoDecisao"'))
        sessao_tipo                  = dsl.extract(sessao,'"tipoSessao" : {  "codigo" : "','"')
        sessao_numero                = dsl.extract(sessao,'numero" : ',',')
        sessao_ano                   = dsl.extract(sessao,'ano" : ',',')
        sessao_colegiado             = dsl.extract(sessao,'"colegiado" : {  "codigo" : "','"')
        sessao_data_prevista_inicio  = dsl.extract(sessao,'"dataPrevistaInicio" : "','"')
        sessao_data_inicio           = dsl.extract(sessao,'"dataInicio" : "','"')
        sessao_data_prevista_fim     = dsl.extract(sessao,'"dataPrevistaFim" : "','"')
        sessao_data_fim              = dsl.extract(sessao,'"dataFim" : "','"')
        
        tipoJulgamentoVirtual = dsl.extract(sessao, '"tipoJulgamentoVirtual" : "', '"')
    
        textoDecisao = dsl.extract(lista,'"textoDecisao" : "','"')
        textoDecisao2 = dsl.extract(lista,'"cabecalho" : "','"tipoListaJulgamento"')
        
        lista_tipo = dsl.limpar(dsl.extract(lista,'"tipoListaJulgamento" : {','}')).replace('codigo" : "','')
        lista_tipo = lista_tipo.replace('", "descricao" : "',':')
        lista_tipo = lista_tipo.strip('"')
        
        
        tipoResultadoJulgamento = dsl.limpar(dsl.extract(lista,'"tipoResultadoJulgamento" : {','}'))
        tipoJulgamento = dsl.extract(tipoResultadoJulgamento,'codigo" : "','"')
        tipoJulgamento_desc = dsl.extract(tipoResultadoJulgamento,'"descricao" : "','"')
        
        sustentacoesOrais  = dsl.limpar(dsl.extract(lista,'"sustentacoesOrais" : ','}'))
        if sustentacoesOrais == '[ ]':
            sustentacoesOrais = 'NA'
            
        # define votos
        
        votos_complementares = dsl.limpar(dsl.extract(lista,'"votos" : ',''))
        if 'numeroOrdemVotoSessao' in votos_complementares:
            votos_complementares = votos_complementares.split('"numeroOrdemVotoSessao" : ')[1:]
        elif '"votos" : ""' in lista:
            votos_complementares = []
            
        len_votos_complementares = len(votos_complementares)

            
        lista_dados = [     lista_index, #
                            idLista,
                            nomeLista,
                            julgado,
                            len_votos_complementares,#
                            admiteSustentacaoOral,
                            relator_codigo,
                            relator_nome,
                            votoRelator,
                            relatorioRelator,
                            complementoVotoRelator,
                            ministroDestaque,
                            ministroVista,
                            ministroVistor,                            
                            sessao,
                            sessao_tipo,
                            sessao_numero,
                            sessao_ano,
                            sessao_colegiado,
                            sessao_data_prevista_inicio,
                            sessao_data_inicio,
                            sessao_data_prevista_fim,
                            sessao_data_fim,
                            tipoJulgamentoVirtual,
                            textoDecisao,
                            textoDecisao2,
                            lista_tipo,
                            tipoJulgamento,
                            tipoJulgamento_desc,
                            sustentacoesOrais
                            ]
            
        # processa votos
        votos_info = []
    
        n_voto = 'NA'
        votoAntecipado = 'NA'
        julgador = 'NA'
        dataVoto = 'NA'
        tipoVoto = 'NA'
        tipoVoto_codigo = 'NA'
        acompanhandoMinistro = 'NA'
        voto_texto = 'NA'
        vc_index = 0
        
        # define voto relator
        
        vRel_index = 0
        vRel_id = 0
        vRel_ant = 'NA'
        vRel_julg = relator_nome
        vRel_data = sessao_data_inicio
        vRel_tipo = 'Relator'
        vRel_tipo_codigo = '00'
        vRel_acompanha = 'NA'
        vRel_texto = votoRelator
        
        vRel_dados = [  vRel_index,
                        vRel_id,
                        vRel_ant,
                        vRel_julg,
                        vRel_data,
                        vRel_tipo,
                        vRel_tipo_codigo,
                        vRel_acompanha,
                        vRel_texto]
        

        votos_PV_relator.append(vRel_dados + 
                        df_original[:12] + 
                        df_original [13:] + 
                        lista_dados)
        
        # if len(votos_complementares) > 11:
        #     print (str(len(votos_complementares)) + ' - ' + str(votos_complementares)[:50] + '-'+str(item[:2]))
        #     teste.append(votos_complementares)
        
        if len_votos_complementares > 0:
            for voto in votos_complementares:
                vc_index = vc_index + 1
                n_voto = int(dsl.extract(voto,'',','))-1
                
                votoAntecipado = dsl.extract(voto,'votoAntecipado" : "','"')
                julgador = dsl.extract(voto,'"descricao" : "','"').replace('MIN. ','')
                dataVoto = dsl.extract(voto,'"dataVoto" : "','"')
                tipoVoto = dsl.limpar(dsl.extract(voto,'tipoVoto" : {','}'))
                tipoVoto_codigo = (dsl.extract(tipoVoto,'codigo" : "','"'))
                tipoVoto = dsl.extract(tipoVoto,'"descricao" : "','"')
                acompanhandoMinistro = dsl.extract(voto,'"acompanhandoMinistro" : "','"')
                voto_texto = dsl.limpar(dsl.extract(voto,'"textos" : ','}'))
                if voto_texto == '[ ]':
                    voto_texto = 'NA'
                else:
                    voto_texto = voto_texto.replace('",  "descricao','')
                    voto_texto = voto_texto.replace('",  "link','')
                    voto_texto = voto_texto.strip('"')
                    voto_texto = voto_texto.split('" : "')[1:]
                
                voto_complementar_dados =     [vc_index,
                                              n_voto,
                                              votoAntecipado,
                                              julgador,
                                              dataVoto,
                                              tipoVoto,
                                              tipoVoto_codigo,
                                              acompanhandoMinistro,
                                              voto_texto]
                
                votos_PV.append(voto_complementar_dados + 
                                vRel_dados + 
                                df_original[:12] + 
                                df_original [13:] + 
                                lista_dados)
                # define variáveis votos complementares
                        
                v1_index = 'na'
                v1_index = 'na'
                v1_id = 'na'
                v1_ant = 'na'
                v1_julg = 'na'
                v1_data = 'na'
                v1_tipo = 'na'
                v1_tipo_codigo = 'na'
                v1_acompanha = 'na'
                v1_texto = 'na'
                
                v2_index = 'na'
                v2_id = 'na'
                v2_ant = 'na'
                v2_julg = 'na'
                v2_data = 'na'
                v2_tipo = 'na'
                v2_tipo_codigo = 'na'
                v2_acompanha = 'na'
                v2_texto = 'na'
                
                v3_index = 'na'
                v3_id = 'na'
                v3_ant = 'na'
                v3_julg = 'na'
                v3_data = 'na'
                v3_tipo = 'na'
                v3_tipo_codigo = 'na'
                v3_acompanha = 'na'
                v3_texto = 'na'
                
                v4_index = 'na'
                v4_id = 'na'
                v4_ant = 'na'
                v4_julg = 'na'
                v4_data = 'na'
                v4_tipo = 'na'
                v4_tipo_codigo = 'na'
                v4_acompanha = 'na'
                v4_texto = 'na'
                
                v5_index = 'na'
                v5_id = 'na'
                v5_ant = 'na'
                v5_julg = 'na'
                v5_data = 'na'
                v5_tipo = 'na'
                v5_tipo_codigo = 'na'
                v5_acompanha = 'na'
                v5_texto = 'na'
                
                v6_index = 'na'
                v6_id = 'na'
                v6_ant = 'na'
                v6_julg = 'na'
                v6_data = 'na'
                v6_tipo = 'na'
                v6_tipo_codigo = 'na'
                v6_acompanha = 'na'
                v6_texto = 'na'
                
                v7_index = 'na'
                v7_id = 'na'
                v7_ant = 'na'
                v7_julg = 'na'
                v7_data = 'na'
                v7_tipo = 'na'
                v7_tipo_codigo = 'na'
                v7_acompanha = 'na'
                v7_texto = 'na'
                
                v8_index = 'na'
                v8_id = 'na'
                v8_ant = 'na'
                v8_julg = 'na'
                v8_data = 'na'
                v8_tipo = 'na'
                v8_tipo_codigo = 'na'
                v8_acompanha = 'na'
                v8_texto = 'na'
                
                v9_index = 'na'
                v9_id = 'na'
                v9_ant = 'na'
                v9_julg = 'na'
                v9_data = 'na'
                v9_tipo = 'na'
                v9_tipo_codigo = 'na'
                v9_acompanha = 'na'
                v9_texto = 'na'
                
                v10_index = 'na'
                v10_id = 'na'
                v10_ant = 'na'
                v10_julg = 'na'
                v10_data = 'na'
                v10_tipo = 'na'
                v10_tipo_codigo = 'na'
                v10_acompanha = 'na'
                v10_texto = 'na'
                
                v11_index = 'na'
                v11_id = 'na'
                v11_ant = 'na'
                v11_julg = 'na'
                v11_data = 'na'
                v11_tipo = 'na'
                v11_tipo_codigo = 'na'
                v11_acompanha = 'na'
                v11_texto = 'na'

                v12_index = 'na'
                v12_id = 'na'
                v12_ant = 'na'
                v12_julg = 'na'
                v12_data = 'na'
                v12_tipo = 'na'
                v12_tipo_codigo = 'na'
                v12_acompanha = 'na'
                v12_texto = 'na'
                
                if vc_index == 1:
                    [v1_index,
                      v1_id, 
                      v1_ant, 
                      v1_julg,
                      v1_data,
                      v1_tipo,
                      v1_tipo_codigo,
                      v1_acompanha,
                      v1_texto] = voto_complementar_dados
                if vc_index == 2:
                    [v2_index,
                      v2_id, 
                      v2_ant, 
                      v2_julg,
                      v2_data,
                      v2_tipo,
                      v2_tipo_codigo,
                      v2_acompanha,
                      v2_texto] = voto_complementar_dados
                if vc_index == 3:
                    [v3_index,
                      v3_id, 
                      v3_ant, 
                      v3_julg,
                      v3_data,
                      v3_tipo,
                      v3_tipo_codigo,
                      v3_acompanha,
                      v3_texto] = voto_complementar_dados
                if vc_index == 4:
                    [v4_index,
                      v4_id, 
                      v4_ant, 
                      v4_julg,
                      v4_data,
                      v4_tipo,
                      v4_tipo_codigo,
                      v4_acompanha,
                      v4_texto] = voto_complementar_dados
                if vc_index == 5:
                    [v5_index,
                      v5_id, 
                      v5_ant, 
                      v5_julg,
                      v5_data,
                      v5_tipo,
                      v5_tipo_codigo,
                      v5_acompanha,
                      v5_texto] = voto_complementar_dados
                if vc_index == 6:
                    [v6_index,
                      v6_id, 
                      v6_ant, 
                      v6_julg,
                      v6_data,
                      v6_tipo,
                      v6_tipo_codigo,
                      v6_acompanha,
                      v6_texto] = voto_complementar_dados
                if vc_index == 7:
                    [v7_index,
                      v7_id, 
                      v7_ant, 
                      v7_julg,
                      v7_data,
                      v7_tipo,
                      v7_tipo_codigo,
                      v7_acompanha,
                      v7_texto] = voto_complementar_dados
                if vc_index == 8:
                    [v8_index,
                      v8_id, 
                      v8_ant, 
                      v8_julg,
                      v8_data,
                      v8_tipo,
                      v8_tipo_codigo,
                      v8_acompanha,
                      v8_texto] = voto_complementar_dados
                if vc_index == 9:
                    [v9_index,
                      v9_id, 
                      v9_ant, 
                      v9_julg,
                      v9_data,
                      v9_tipo,
                      v9_tipo_codigo,
                      v9_acompanha,
                      v9_texto] = voto_complementar_dados
                if vc_index == 10:
                    [v10_index,
                      v10_id, 
                      v10_ant, 
                      v10_julg,
                      v10_data,
                      v10_tipo,
                      v10_tipo_codigo,
                      v10_acompanha,
                      v10_texto] = voto_complementar_dados
                if vc_index == 11:
                    [v11_index,
                      v11_id, 
                      v11_ant, 
                      v11_julg,
                      v11_data,
                      v11_tipo,
                      v11_tipo_codigo,
                      v11_acompanha,
                      v11_texto] = voto_complementar_dados
                if vc_index == 12:
                    [v12_index,
                      v12_id, 
                      v12_ant, 
                      v12_julg,
                      v12_data,
                      v12_tipo,
                      v12_tipo_codigo,
                      v12_acompanha,
                      v12_texto] = voto_complementar_dados
    
                votos_ordem = [
                            v1_index,
                            v1_id,
                            v1_ant,
                            v1_julg,
                            v1_data,
                            v1_tipo,
                            v1_tipo_codigo,
                            v1_acompanha,
                            v1_texto,
                            
                            v2_index,
                            v2_id,
                            v2_ant,
                            v2_julg,
                            v2_data,
                            v2_tipo,
                            v2_tipo_codigo,
                            v2_acompanha,
                            v2_texto,
                            
                            v3_index,
                            v3_id,
                            v3_ant,
                            v3_julg,
                            v3_data,
                            v3_tipo,
                            v3_tipo_codigo,
                            v3_acompanha,
                            v3_texto,
                            
                            v4_index,
                            v4_id,
                            v4_ant,
                            v4_julg,
                            v4_data,
                            v4_tipo,
                            v4_tipo_codigo,
                            v4_acompanha,
                            v4_texto,
                            
                            v5_index,
                            v5_id,
                            v5_ant,
                            v5_julg,
                            v5_data,
                            v5_tipo,
                            v5_tipo_codigo,
                            v5_acompanha,
                            v5_texto,
                            
                            v6_index,
                            v6_id,
                            v6_ant,
                            v6_julg,
                            v6_data,
                            v6_tipo,
                            v6_tipo_codigo,
                            v6_acompanha,
                            v6_texto,
                            
                            v7_index,
                            v7_id,
                            v7_ant,
                            v7_julg,
                            v7_data,
                            v7_tipo,
                            v7_tipo_codigo,
                            v7_acompanha,
                            v7_texto,
                            
                            v8_index,
                            v8_id,
                            v8_ant,
                            v8_julg,
                            v8_data,
                            v8_tipo,
                            v8_tipo_codigo,
                            v8_acompanha,
                            v8_texto,
                            
                            v9_index,
                            v9_id,
                            v9_ant,
                            v9_julg,
                            v9_data,
                            v9_tipo,
                            v9_tipo_codigo,
                            v9_acompanha,
                            v9_texto,
                            
                            v10_index,
                            v10_id,
                            v10_ant,
                            v10_julg,
                            v10_data,
                            v10_tipo,
                            v10_tipo_codigo,
                            v10_acompanha,
                            v10_texto,
                            
                            v11_index,
                            v11_id,
                            v11_ant,
                            v11_julg,
                            v11_data,
                            v11_tipo,
                            v11_tipo_codigo,
                            v11_acompanha,
                            v11_texto,
                            
                            v12_index,
                            v12_id,
                            v12_ant,
                            v12_julg,
                            v12_data,
                            v12_tipo,
                            v12_tipo_codigo,
                            v12_acompanha,
                            v12_texto
                                ]


        processos_PV.append(df_original[:12] + 
                            df_original[13:] + 
                            lista_dados+
                            vRel_dados+
                            votos_ordem)



dfvotos = pd.DataFrame(votos_PV , columns=[  
                                        'voto_index',
                                        'n_voto',
                                        'votoAntecipado',
                                        'julgador',
                                        'dataVoto',
                                        'tipoVoto',
                                        'tipoVoto_codigo',
                                        'acompanhandoMinistro',
                                        'voto_texto',
                                        'vRel_index',
                                        'vRel_id',
                                        'vRel_ant',
                                        'vRel_julg',
                                        'vRel_data',
                                        'vRel_tipo',
                                        'vRel_tipo_codigo',
                                        'vRel_acompanha',
                                        'vRel_texto',
                                        
                                        'identificador',
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
                                        'orgao',
                                        'data_inicial',
                                        'data_final',
                                        'tipo',
                                        'tipo_desc',
                                        'relator',
                                        'lista_id',
                                        'lista_desc',
                                        'lista_ordem',
                                        'lista_quantidade',
                                        
                                        'lista_index',
                                        'idLista',
                                        'nomeLista',
                                        'julgado',
                                        'len_votos',
                                        'admiteSustentacaoOral',
                                        'relator_codigo',
                                        'relator_nome',
                                        'votoRelator',
                                        'relatorioRelator',
                                        'complementoVotoRelator',
                                        'ministroDestaque',
                                        'ministroVista',
                                        'ministroVistor',                            
                                        'sessao',
                                        'sessao_tipo',
                                        'sessao_numero',
                                        'sessao_ano',
                                        'sessao_colegiado',
                                        'sessao_data_prevista_inicio',
                                        'sessao_data_inicio',
                                        'sessao_data_prevista_fim',
                                        'sessao_data_fim',
                                        'tipoJulgamentoVirtual',
                                        'textoDecisao',
                                        'textoDecisao2',
                                        'lista_tipo',
                                        'tipoJulgamento',
                                        'tipoJulgamento_desc',
                                        'sustentacoesOrais'

                                        ])

dfvotos.to_csv('votos_PV.txt', index=False)



dfprocessos = pd.DataFrame(processos_PV, columns=[ 'identificador',
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
                                            'orgao',
                                            'data_inicial',
                                            'data_final',
                                            'tipo',
                                            'tipo_desc',
                                            'relator',
                                            'lista_id',
                                            'lista_desc',
                                            'lista_ordem',
                                            'lista_quantidade',
                                            
                                            'lista_index',
                                            'idLista',
                                            'nomeLista',
                                            'julgado',
                                            'len_votos',
                                            'admiteSustentacaoOral',
                                            'relator_codigo',
                                            'relator_nome',
                                            'votoRelator',
                                            'relatorioRelator',
                                            'complementoVotoRelator',
                                            'ministroDestaque',
                                            'ministroVista',
                                            'ministroVistor',                            
                                            'sessao',
                                            'sessao_tipo',
                                            'sessao-numero',
                                            'sessao_ano',
                                            'sessao_colegiado',
                                            'sessao_data_prevista_inicio',
                                            'sessao_data_inicio',
                                            'sessao_data_prevista_fim',
                                            'sessao_data_fim',
                                            'tipoJulgamentoVirtual',
                                            'textoDecisao',
                                            'textoDecisao2',
                                            'lista_tipo',
                                            'tipoJulgamento',
                                            'tipoJulgamento_desc',
                                            'sustentacoesOrais',
                                            
                                            'vRel_index',
                                            'vRel_id',
                                            'vRel_ant',
                                            'vRel_julg',
                                            'vRel_data',
                                            'vRel_tipo',
                                            'vRel_tipo_codigo',
                                            'vRel_acompanha',
                                            'vRel_texto',
                                            
                                            'v1_index',
                                            'v1_id',
                                            'v1_ant',
                                            'v1_julg',
                                            'v1_data',
                                            'v1_tipo',
                                            'v1_tipo_codigo',
                                            'v1_acompanha',
                                            'v1_texto',
                                            'v2_index',
                                            'v2_id',
                                            'v2_ant',
                                            'v2_julg',
                                            'v2_data',
                                            'v2_tipo',
                                            'v2_tipo_codigo',
                                            'v2_acompanha',
                                            'v2_texto',
                                            'v3_index',
                                            'v3_id',
                                            'v3_ant',
                                            'v3_julg',
                                            'v3_data',
                                            'v3_tipo',
                                            'v3_tipo_codigo',
                                            'v3_acompanha',
                                            'v3_texto',
                                            'v4_index',
                                            'v4_id',
                                            'v4_ant',
                                            'v4_julg',
                                            'v4_data',
                                            'v4_tipo',
                                            'v4_tipo_codigo',
                                            'v4_acompanha',
                                            'v4_texto',
                                            'v5_index',
                                            'v5_id',
                                            'v5_ant',
                                            'v5_julg',
                                            'v5_data',
                                            'v5_tipo',
                                            'v5_tipo_codigo',
                                            'v5_acompanha',
                                            'v5_texto',
                                            'v6_index',
                                            'v6_id',
                                            'v6_ant',
                                            'v6_julg',
                                            'v6_data',
                                            'v6_tipo',
                                            'v6_tipo_codigo',
                                            'v6_acompanha',
                                            'v6_texto',
                                            'v7_index',
                                            'v7_id',
                                            'v7_ant',
                                            'v7_julg',
                                            'v7_data',
                                            'v7_tipo',
                                            'v7_tipo_codigo',
                                            'v7_acompanha',
                                            'v7_texto',
                                            'v8_index',
                                            'v8_id',
                                            'v8_ant',
                                            'v8_julg',
                                            'v8_data',
                                            'v8_tipo',
                                            'v8_tipo_codigo',
                                            'v8_acompanha',
                                            'v8_texto',
                                            'v9_index',
                                            'v9_id',
                                            'v9_ant',
                                            'v9_julg',
                                            'v9_data',
                                            'v9_tipo',
                                            'v9_tipo_codigo',
                                            'v9_acompanha',
                                            'v9_texto',
                                            'v10_index',
                                            'v10_id',
                                            'v10_ant',
                                            'v10_julg',
                                            'v10_data',
                                            'v10_tipo',
                                            'v10_tipo_codigo',
                                            'v10_acompanha',
                                            'v10_texto',
                                            'v11_index',
                                            'v11_id',
                                            'v11_ant',
                                            'v11_julg',
                                            'v11_data',
                                            'v11_tipo',
                                            'v11_tipo_codigo',
                                            'v11_acompanha',
                                            'v11_texto',
                                            'v12_index',
                                            'v12_id',
                                            'v12_ant',
                                            'v12_julg',
                                            'v12_data',
                                            'v12_tipo',
                                            'v12_tipo_codigo',
                                            'v12_acompanha',
                                            'v12_texto'])
dfprocessos.to_csv('processos_PV.txt', index=False)


print('gravando_excel')
dfprocessos.to_excel('processos_PV.xlsx', index=False)
dfvotos.to_excel('votos_PV.xlsx', index=False)