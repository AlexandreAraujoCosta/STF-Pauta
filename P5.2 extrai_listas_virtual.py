# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 16:54:44 2023

@author: Alexandre Araújo Costa
"""

import time
import urllib3
import pandas as pd
import json

import dsl
from helpers import DATA_PATH
urllib3.disable_warnings()

source = DATA_PATH/'dados_pautas_virtual.csv'
url = 'https://portal.stf.jus.br/pauta/services/lista-service.asp?lista='
url2 = 'https://sistemas.stf.jus.br/repgeral/votacao?sessaoVirtual='
url3 = 'https://sistemas.stf.jus.br/repgeral/votacao?oi='
# processa presenciais

listas0 = pd.read_csv(source, dtype={"teste": str})
listas = listas0.values.tolist()

listas_a_consultar = []
lista_buscar = []
nao_processada = []
processos_a_gravar = []
votos_a_gravar = []
lista_vazia = []
completos_a_gravar = []
n = 0
if n == 0:
    gravar_header = True
else:
    gravar_header = False

orgao = 'TP'

for item in listas:
    if item[2] == orgao:
        listas_a_consultar.append(item)

colunas0 = list(listas0.columns)

for lista in listas_a_consultar[n:]:
    
    lista_id = str(lista[15])
    
    n = n + 1
    if gravar_header == True:
        print (str(n) + ' loops de ' + str(len(listas_a_consultar)) )
    else:
        print (str(n-1) + ' loops de ' + str(len(listas_a_consultar)) )
    

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
        
        if inc_cadeia is not None:
            inc_dados = dsl.get(url3+inc_id)
            if 'objetoIncidente' not in inc_dados:
                time.sleep(30)
                inc_dados = dsl.get(url3+inc_id)
                if 'objetoIncidente' not in inc_dados:
                    nao_processada.append([incidentes0])
                    print('1 incidente não processado')
                    break
            
            jinc_dados = json.loads(inc_dados)
            
            for item in jinc_dados:
                caracteres = len(inc_cadeia)
                if item['objetoIncidente']['identificacaoCompleta'][:caracteres] == inc_cadeia:
                    inc_id = item['objetoIncidente']['id']
                    break
                
        dados_julgamento0 = (dsl.get(url2+str(inc_id)))
        
        if 'objetoIncidente' not in dados_julgamento0:
            time.sleep(30)
            dados_julgamento0 = (dsl.get(url2+str(inc_id)))
            if 'objetoIncidente' not in dados_julgamento0:
                nao_processada.append([incidentes0])
                print('1 incidente não processado')
                break
        

        dados_julgamento = json.loads(dados_julgamento0)
        
        for julg in dados_julgamento:
        
            inc_sust_oral = julg['sustentacoesOrais']
            inc_julgamentos = julg['listasJulgamento']
            
            for inc_julgamento in inc_julgamentos:
                
                inc_lista_id = inc_julgamento['id']
                inc_lista_nome = inc_julgamento['nomeLista']
                inc_tipoListaJulgamento = inc_julgamento['tipoListaJulgamento']
                inc_lista_codigo = inc_tipoListaJulgamento['codigo']
                inc_lista_desc = inc_tipoListaJulgamento['descricao']
                inc_sessao = inc_julgamento['sessao']
                inc_sessao_numero = inc_sessao['numero']
                inc_sessao_tipo = inc_sessao['tipoSessao']['codigo']
                
                inc_admiteSustentacaoOral = inc_julgamento['admiteSustentacaoOral']
                inc_julgado = inc_julgamento['julgado']
                if inc_julgamento['tipoResultadoJulgamento'] != '':
                    inc_resultado_codigo = inc_julgamento['tipoResultadoJulgamento']['codigo']
                    inc_resultado_desc = inc_julgamento['tipoResultadoJulgamento']['descricao']
                else:
                    inc_resultado_codigo = None
                    inc_resultado_desc = None
                inc_cabecalho = inc_julgamento['cabecalho']
                inc_ministroRelator = inc_julgamento['ministroRelator']
                if inc_ministroRelator != '':
                    inc_ministroRelator = inc_julgamento['ministroRelator']['descricao']
                    
                if inc_julgamento['relatorioRelator'] != '':
                    inc_relatorioRelator = inc_julgamento['relatorioRelator']['link']
                else:
                    inc_relatorioRelator = None
                
                if inc_julgamento['votoRelator'] != '':
                    inc_votoRelator = inc_julgamento['votoRelator']['link']
                else:
                    inc_votoRelator = None
                    
                inc_complementoVotoRelator = inc_julgamento['complementoVotoRelator']
                inc_ministroVistor = inc_julgamento['ministroVistor']
                if inc_ministroVistor != '':
                    inc_ministroVistor = inc_julgamento['ministroVistor']['descricao']                
                inc_ministroVista = inc_julgamento['ministroVista']
                if inc_ministroVista != '':
                    inc_ministroVista = inc_julgamento['ministroVista']['descricao']
                inc_ministroDestaque = inc_julgamento['ministroDestaque']
                if inc_ministroDestaque != '':
                    inc_ministroDestaque = inc_julgamento['ministroDestaque']['descricao']
                inc_textoDecisao = inc_julgamento['textoDecisao']
                
                
                inc_ministroRelator = inc_ministroRelator.replace('MIN. ','')
                inc_ministroRelator = inc_ministroRelator.replace('MINISTRO','')
                
                inc_ministroVista = inc_ministroVista.replace('MIN. ','')
                inc_ministroVista = inc_ministroVista.replace('MINISTRO','')
                
                inc_ministroVistor = inc_ministroVistor.replace('MIN. ','')
                inc_ministroVistor = inc_ministroVistor.replace('MINISTRO','')
                
                inc_ministroDestaque = inc_ministroDestaque.replace('MIN. ','')
                inc_ministroDestaque = inc_ministroDestaque.replace('MINISTRO','')

                inc_votos = inc_julgamento['votos']
                
                dados_incidente = [
                        inc_cadeia,
                        inc_classe,
                        inc_id,
                        inc_numero,
                        inc_procedencia,
                        json.dumps(inc_partes, ensure_ascii=False),
                        inc_polo_ativo_nome,
                        inc_polo_ativo_tipo,
                        json.dumps(inc_sust_oral, ensure_ascii=False),
                        inc_lista_id,
                        inc_lista_nome,
                        inc_lista_codigo,
                        inc_lista_desc,
                        inc_sessao_numero,
                        inc_sessao_tipo,
                        inc_admiteSustentacaoOral,
                        inc_julgado,
                        inc_resultado_codigo,
                        inc_resultado_desc,
                        inc_cabecalho,
                        inc_ministroRelator,
                        inc_relatorioRelator,
                        inc_votoRelator,
                        inc_complementoVotoRelator,
                        inc_ministroVistor,
                        inc_ministroVista,
                        inc_ministroDestaque,
                        inc_textoDecisao,
                        json.dumps(inc_votos, ensure_ascii=False)
                        ]
                
                colunas_incidente = [
                        'inc_cadeia',
                        'inc_classe',
                        'inc_id',
                        'inc_numero',
                        'inc_procedencia',
                        'json.dumps(inc_partes)',
                        'inc_polo_ativo_nome',
                        'inc_polo_ativo_tipo',
                        'json.dumps(inc_sust_oral)',
                        'inc_lista_id',
                        'inc_lista_nome',
                        'inc_lista_codigo',
                        'inc_lista_desc',
                        'inc_sessao_numero',
                        'inc_sessao_tipo',
                        'inc_admiteSustentacaoOral',
                        'inc_julgado',
                        'inc_resultado_codigo',
                        'inc_resultado_desc',
                        'inc_cabecalho',
                        'inc_ministroRelator',
                        'inc_relatorioRelator',
                        'inc_votoRelator',
                        'inc_complementoVotoRelator',
                        'inc_ministroVistor',
                        'inc_ministroVista',
                        'inc_ministroDestaque',
                        'inc_textoDecisao',
                        'json.dumps(inc_votos)'
                        ]
                
                processos_a_gravar.append(lista + dados_incidente)
                
                
                votos_lista = []
                voto_index = 0
                if inc_votos != '':
                    for voto in inc_votos:
                        voto_index = voto_index + 1
                        voto_data = voto['dataVoto']
                        voto_data = voto_data[6:]+'-'+voto_data[3:5]+'-'+voto_data[:2]
                        voto_numero_ordem = voto['numeroOrdemVotoSessao']
                        voto_tipo = voto['tipoVoto']['codigo']
                        voto_acompanha = voto['acompanhandoMinistro']
                        voto_tipo_desc = voto['tipoVoto']['descricao']
                        voto_ministro = voto['ministro']['descricao']
                        voto_ministro = voto_ministro.replace('MIN. ','')
                        voto_ministro = voto_ministro.replace('MINISTRO ','')
                        voto_antecipado = voto['votoAntecipado']
                        voto_textos = voto['textos']
                        
                        dados_voto = [voto_index,
                                      voto_data,
                                      voto_numero_ordem,
                                      voto_ministro,
                                      voto_tipo,
                                      voto_tipo_desc,
                                      voto_acompanha,
                                      voto_antecipado,
                                      voto_textos
                                      ]
                        
                        colunas_voto = ['voto_index',
                                      'voto_data',
                                      'voto_numero_ordem',
                                      'voto_ministro',
                                      'voto_tipo',
                                      'voto_tipo_desc',
                                      'voto_acompanha',
                                      'voto_antecipado',
                                      'voto_textos'
                                      ]
                        
                        votos_lista.append(dados_voto)
                
                    voto1 = ''
                    voto2 = ''
                    voto3 = ''
                    voto4 = ''
                    voto5 = ''
                    voto6 = ''
                    voto7 = ''
                    voto8 = ''
                    voto9 = ''
                    voto10 = ''
                    voto11 = ''
                    voto12 = ''
                    voto13 = ''
                    voto14 = ''
                    voto15 = ''
    
                    if len(votos_lista) == 15:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
                        voto7 = votos_lista[6]
                        voto8 = votos_lista[7]
                        voto9 = votos_lista[8]
                        voto10 = votos_lista[9]
                        voto11 = votos_lista[10]
                        voto12 = votos_lista[11]
                        voto13 = votos_lista[12]
                        voto14 = votos_lista[13]
                        voto15 = votos_lista[14]
                        
                    if len(votos_lista) == 14:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
                        voto7 = votos_lista[6]
                        voto8 = votos_lista[7]
                        voto9 = votos_lista[8]
                        voto10 = votos_lista[9]
                        voto11 = votos_lista[10]
                        voto12 = votos_lista[11]
                        voto13 = votos_lista[12]
                        voto14 = votos_lista[13]
                        
                    if len(votos_lista) == 13:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
                        voto7 = votos_lista[6]
                        voto8 = votos_lista[7]
                        voto9 = votos_lista[8]
                        voto10 = votos_lista[9]
                        voto11 = votos_lista[10]
                        voto12 = votos_lista[11]
                        voto13 = votos_lista[12]
                    
                    if len(votos_lista) == 12:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
                        voto7 = votos_lista[6]
                        voto8 = votos_lista[7]
                        voto9 = votos_lista[8]
                        voto10 = votos_lista[9]
                        voto11 = votos_lista[10]
                        voto12 = votos_lista[11]
    
                    if len(votos_lista) == 11:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
                        voto7 = votos_lista[6]
                        voto8 = votos_lista[7]
                        voto9 = votos_lista[8]
                        voto10 = votos_lista[9]
                        voto11 = votos_lista[10]
    
                        
                    if len(votos_lista) == 10:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
                        voto7 = votos_lista[6]
                        voto8 = votos_lista[7]
                        voto9 = votos_lista[8]
                        voto10 = votos_lista[9]
    
                        
                    if len(votos_lista) == 9:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
                        voto7 = votos_lista[6]
                        voto8 = votos_lista[7]
                        voto9 = votos_lista[8]
                        
                    if len(votos_lista) == 8:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
                        voto7 = votos_lista[6]
                        voto8 = votos_lista[7]
    
            
                    if len(votos_lista) == 7:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
                        voto7 = votos_lista[6]
    
                    
                    if len(votos_lista) == 6:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
                        voto6 = votos_lista[5]
    
                    
                    if len(votos_lista) == 5:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
                        voto5 = votos_lista[4]
    
                    if len(votos_lista) == 4:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
                        voto4 = votos_lista[3]
        
                    if len(votos_lista) == 3:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
                        voto3 = votos_lista[2]
    
                        
                    if len(votos_lista) == 2:
                        voto1 = votos_lista[0]
                        voto2 = votos_lista[1]
    
                
                    if len(votos_lista) == 1:
                        voto1 = votos_lista[0]
                        
                    
                    votos_julgamento = [voto1,
                                        voto2,
                                        voto3,
                                        voto4,
                                        voto5,
                                        voto6,
                                        voto7,
                                        voto8,
                                        voto9,
                                        voto10,
                                        voto11,
                                        voto12,
                                        voto13,
                                        voto14,
                                        voto15
                                        ]
                    
                    votos_colunas = ['voto1',
                                        'voto2',
                                        'voto3',
                                        'voto4',
                                        'voto5',
                                        'voto6',
                                        'voto7',
                                        'voto8',
                                        'voto9',
                                        'voto10',
                                        'voto11',
                                        'voto12',
                                        'voto13',
                                        'voto14',
                                        'voto15'
                                        ]
                    
                    for voto_ind in votos_julgamento:
                        if voto_ind != '':
                            votos_a_gravar.append(lista + dados_incidente + voto_ind)
                    
                    completos_a_gravar.append(lista + dados_incidente + votos_julgamento)

                    if gravar_header == True:
                        gravar_header = False

                        df_processos = pd.DataFrame(processos_a_gravar, columns = [colunas0 + colunas_incidente])
                        
                        df_votos = pd.DataFrame(votos_a_gravar, columns = [colunas0 + colunas_incidente + colunas_voto])
                        
                        df_processos_com_votos = pd.DataFrame(completos_a_gravar, columns = [colunas0 + colunas_incidente + votos_colunas])
                        
                        df_np = pd.DataFrame(nao_processada)
                        
                        df_processos.to_csv(f'data\\processos_julgados_virtual_{orgao}.csv', index=False)
                        
                        
                        
                        df_votos.to_csv(f'data\\votos_virtual_{orgao}.csv', index=False)
                        # df_votos.to_excel(f'data\\votos_virtual_{orgao}.xlsx', index=False, sheet_name='Processos Julgados PV - votos')
                        
                        df_processos_com_votos.to_csv(f'data\\processos_julgados_virtual_comp_{orgao}.csv', index=False)
                        # df_processos_com_votos.to_excel(f'data\\processos_julgados_virtual_comp_{orgao}.xlsx', index=False)
                        
                        df_np.to_csv(f'data\\nao_processados_votos_virtual_{orgao}.csv', index=False)
                        
                        processos_a_gravar = []
                        votos_a_gravar = []
                        completos_a_gravar = []
                        nao_processada = []
                                                
                    else:
                        if n % 500 == 0:
                                df_processos = pd.DataFrame(processos_a_gravar, columns = [colunas0 + colunas_incidente])
                                
                                df_votos = pd.DataFrame(votos_a_gravar, columns = [colunas0 + colunas_incidente + colunas_voto])
                                
                                df_processos_com_votos = pd.DataFrame(completos_a_gravar, columns = [colunas0 + colunas_incidente + votos_colunas])
                                
                                df_np = pd.DataFrame(nao_processada)
                                
                                df_processos.to_csv(f'data\\processos_julgados_virtual_{orgao}.csv', index=False, mode = 'a', header = False)
                                
                                df_votos.to_csv(f'data\\votos_virtual_{orgao}.csv', index=False, mode = 'a', header = False)
                                
                                df_processos_com_votos.to_csv(f'data\\processos_julgados_virtual_comp_{orgao}.csv', index=False, mode = 'a', header = False)
                                
                                df_np.to_csv(f'data\\nao_processados_votos_virtual_{orgao}.csv', index=False, mode = 'a', header = False)
                                
                                processos_a_gravar = []
                                votos_a_gravar = []
                                completos_a_gravar = []
                                nao_processada = []


df_processos = pd.DataFrame(processos_a_gravar, columns = [colunas0 + colunas_incidente])

df_votos = pd.DataFrame(votos_a_gravar, columns = [colunas0 + colunas_incidente + colunas_voto])

df_processos_com_votos = pd.DataFrame(completos_a_gravar, columns = [colunas0 + colunas_incidente + votos_colunas])

df_np = pd.DataFrame(nao_processada)

df_processos.to_csv(f'data\\processos_julgados_virtual_{orgao}.csv', index=False, mode = 'a', header = False)

df_votos.to_csv(f'data\\votos_virtual_{orgao}.csv', index=False, mode = 'a', header = False)

df_processos_com_votos.to_csv(f'data\\processos_julgados_virtual_comp_{orgao}.csv', index=False, mode = 'a', header = False)

df_np.to_csv(f'data\\nao_processados_votos_virtual_{orgao}.csv', index=False, mode = 'a', header = False)


df_total = pd.read_csv(f'data\\processos_julgados_virtual_{orgao}.csv', dtype={"teste": str})
df_total.to_excel(f'data\\processos_julgados_virtual_{orgao}.xlsx', index=False, sheet_name='Processos Julgados PV')
