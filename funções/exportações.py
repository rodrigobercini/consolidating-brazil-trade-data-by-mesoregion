import pandas as pd
import os
import wget

#############
### Extrai dados de exportações por município dos anos x à y e salva tabelas no sisema
#############


def scrape_exp_municip(x, y=''):
    if y == '':
        y = x
        
    if not os.path.exists('By Municip and HS4/EXP'):
        os.makedirs('By Municip and HS4/EXP')  # Cria pasta caso não exista
        
    for i in range(x, y+1):
        url = ''.join(('http://www.mdic.gov.br/balanca/bd/comexstat-bd/mun/EXP_', str(i), '_MUN.csv'))
        folder = 'By Municip and HS4/EXP'
        wget.download(url, folder)


#############
### Cria um dicionários com as exportações de municípios dos anos x à y
#############

def exp_municip(x,y=''):
    if y == '':
        y = x
    d={}
    for i in range(x,y+1):
        file = ''.join(('By Municip and HS4/EXP/EXP_', str(i),'_MUN.csv')) # Defines file with export data
        dummy = pd.read_csv(file, sep=';') # Lê dados de exportação
        municip_codes = pd.read_excel('1_County_Codes.xlsx') # Lê dados de municípios
        d['exp_municip_{0}'.format(i)] = dummy.merge(municip_codes, left_on= 'CO_MUN',
                                                     right_on='Código Município Completo (MDIC)') # Cruza dados de exportação com dados de municípios
        d['exp_municip_{0}'.format(i)].drop(['Município', 'CO_MUN', 'Nome_Microrregião',
                                            'Microrregião Geográfica',
                                            'Código Município Completo (MDIC)'], axis=1, inplace=True) # Deleta colunas desnecessárias
        print('exp_municip done for {0}'.format(i))
        
        
    return d


#############
### Chama exp_municip() e cria um dicionário com as exportações por mesorregião dos anos x à y
#############

def exp_meso(x, y=''):
    if y == '':
        y = x
    d = exp_municip(x,y)
    b={}
    for i in range(x,y+1):
        b['exp_meso_{0}'.format(i)] = d['exp_municip_{0}'.format(i)].groupby(['CO_ANO','Nome_Mesorregião','CD_GEOCME', 'CO_MES', 'CO_PAIS', 'SH4'],as_index=False).sum() # Consolida dados por mesorregião
        b['exp_meso_{0}'.format(i)].drop(['UF', 'Mesorregião Geográfica', 'Código Município Completo (IBGE)'], axis=1, inplace=True) # Deleta colunas desnecessárias
        print('exp_meso done for {0}'.format(i))
    return b

#############
### Chama exp_meso() e salva os dados por mesorregiões como CSV
### Os arquivos são separados por ano porque um arquivo único seria grande demais
#############

def save_meso_data_exports(x, y=''):
    if y == '':
        y = x   
        
    if not os.path.exists('By MesoRegion and HS4/EXP/'):
        os.makedirs('By MesoRegion and HS4/EXP/') # Cria pasta caso não exista
    
    for i in (range(x, y+1)):
        e = exp_meso(i)
        dummy = e['exp_meso_{0}'.format(i)]
        dummy.to_csv(''.join(('By MesoRegion and HS4/EXP/EXP_', str(i),'_MESO.csv')), encoding='UTF-8')
        print('Save exports done for {0}'.format(i))
