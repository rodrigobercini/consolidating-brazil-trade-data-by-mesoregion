import pandas as pd
import os
import wget

#############
### Extrai dados de importações por município dos anos x à y e salva tabelas no sistema
#############

def scrape_imp_municip(x, y=''):
    if y == '':
        y = x
        
    if not os.path.exists('By Municip and HS4/IMP'):
        os.makedirs('By Municip and HS4/IMP')  # Cria pasta caso não exista
        
    for i in range(x, y+1):
        url = ''.join(('http://www.mdic.gov.br/balanca/bd/comexstat-bd/mun/IMP_', str(i), '_MUN.csv'))
        folder = 'By Municip and HS4/IMP'
        wget.download(url, folder)
        print('\n Scrape done for {0}'.format(i))
        
#############
### Cria um dicionários com as importações de municípios dos anos x à y
#############

def imp_municip(x,y=''):
    if y == '':
        y = x
    
    # Chama scrape_imp_municip() para fazer o download dos dados
    scrape_imp_municip(x, y)
        
    d={}
    for i in range(x,y+1):
        file = ''.join(('By Municip and HS4/IMP/IMP_', str(i),'_MUN.csv')) # Define arquivo com dados de importação
        dummy = pd.read_csv(file, sep=';') # Lê dados de importação
        municip_codes = pd.read_excel('1_County_Codes.xlsx') # Lê dados de municípios
        d['imp_municip_{0}'.format(i)] = dummy.merge(municip_codes, left_on= 'CO_MUN', right_on='Código Município Completo (MDIC)') # Cruza dados de importação com dados de municípios
        d['imp_municip_{0}'.format(i)].drop(['Município', 'CO_MUN', 'Nome_Microrregião',
                                            'Microrregião Geográfica',
                                            'Código Município Completo (MDIC)'], axis=1, inplace=True)  # Deleta colunas desnecessárias
        print('imp_municip done for {0}'.format(i))
    return d

#############
### Chama imp_municip() e cria um dicionário com as importações por mesorregião dos anos x à y
#############

def imp_meso(x, y=''):
    if y == '':
        y = x
    d = imp_municip(x,y)
    b={}
    for i in range(x,y+1):
        b['imp_meso_{0}'.format(i)] = d['imp_municip_{0}'.format(i)].groupby(['CO_ANO','Nome_Mesorregião','CD_GEOCME', 'CO_MES', 'CO_PAIS', 'SH4'],as_index=False).sum() # Consolida dados por mesorregião
        b['imp_meso_{0}'.format(i)].drop(['UF', 'Mesorregião Geográfica', 'Código Município Completo (IBGE)'], axis=1, inplace=True) # Deleta colunas desnecessárias
        print('imp_meso done for {0}'.format(i))
    return b


#############
### Chama imp_meso() e salva os dados por mesorregiões como CSV
### Os arquivos são separados por ano porque um arquivo único seria grande demais
#############

def imp_by_meso(x, y=''):
    if y == '':
        y = x
        
    if not os.path.exists('By MesoRegion and HS4/IMP/'):
        os.makedirs('By MesoRegion and HS4/IMP/')  # Cria pasta caso não exista
        
    for i in (range(x, y+1)):
        e = imp_meso(i)
        dummy = e['imp_meso_{0}'.format(i)]
        dummy.to_csv(''.join(('By MesoRegion and HS4/IMP/IMP_', str(i),'_MESO.csv')), encoding='UTF-8')
        print('Save imports done for {0}'.format(i))
