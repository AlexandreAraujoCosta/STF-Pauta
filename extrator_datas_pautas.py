# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 22:43:11 2023

@author: Alexandre Araújo Costa
"""

import dsl

import urllib3
urllib3.disable_warnings()

inicio = 2000
fim = 2021
path = 'datas_pautas\\'

for n in range (fim-inicio+1):

    ano = str(fim-n)
    
    for mes in range (12):
        
        if mes > 8:
            month = str(mes+1)
        else:
            month = '0' + str(mes+1)
        
        url = 'https://portal.stf.jus.br/pauta/services/calendario-service.asp?dados=calendarios&mes=' + month + '&ano=' + str(ano)
        
        print (url)

        html = dsl.get(url)
        
    
        file = open(path+'pauta'+str(month)+str(ano) + '.txt', "a+", encoding="utf-8")
        file.write(str(url) + ", urlfim, " + html)
        file.close()


            

        
    
