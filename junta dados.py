# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 18:16:55 2023

@author: Alexandre Araújo Costa
"""

import pandas as pd

from helpers import DATA_PATH

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
             'processos_julgados_virtual_TP_final.txt',
             
             ]

base = pd.read_csv(source_list[0], dtype={"teste": str})

for n in range(len(source_list)-1):
    item = source_list[n-1]
    dados = pd.read_csv(DATA_PATH/item, dtype={"teste": str})
    base = pd.concat([base,dados])


base.to_csv(DATA_PATH/arquivo_retornar, index=False)
