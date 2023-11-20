# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 18:16:55 2023

@author: Alexandre Araújo Costa
"""

import pandas as pd

arquivo_retornar = 'total.csv'

source_list = ['processos_julgados_virtual_TP500.txt',
             'processos_julgados_virtual_TP1000.txt',
              'processos_julgados_virtual_TP1500.txt',
              'processos_julgados_virtual_TP2000.txt',
              'processos_julgados_virtual_TP2500.txt',
              'processos_julgados_virtual_TP3000.txt',
              'processos_julgados_virtual_TP3500.txt',
              'processos_julgados_virtual_TP4000.txt',
              'processos_julgados_virtual_TP4500.txt',
               'processos_julgados_virtual_TP5000.txt',
               'processos_julgados_virtual_TP5500.txt',
               'processos_julgados_virtual_TP6000.txt',
               'processos_julgados_virtual_TP6500.txt',
               'processos_julgados_virtual_TP7000.txt',
               'processos_julgados_virtual_TP7500.txt',
               'processos_julgados_virtual_TP8000.txt',
               'processos_julgados_virtual_TP_final.txt',
             
             ]

# colunas =   [ 'incidente',
#                 'identificador',
#                 'identificacao',
#                 'identCompleta',
#                  'principal',
#                  'pai',
#                 'incidente_tipo',  
#                  'classe',
#                  'numero',
#                  'incidente_nome',
#                  'procedencia',
#                  'partes',
#                  'autor_tipo',
#                  'dados_processo',
#                  'orgao',
#                  'data_inicial',
#                  'data_final',
#                  'tipo',
#                  'tipo_desc',
#                  'relator',
#                  'lista_id',
#                  'lista_desc',
#                  'lista_ordem',
#                  'lista_quantidade']

base = pd.read_csv(source_list.pop(0),dtype=str)

for item in (source_list):
    print (item)
    dados = pd.read_csv(item, dtype=str)
    base = pd.concat([base,dados])
    
# base.columns = [colunas]

base.to_csv(arquivo_retornar, index=False)
