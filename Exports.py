import pandas as pd
import os
import wget

#############
### Scrapes MDIC official website for exports by municipalities and saves files in system
#############


def scrape_exp_municip(x, y=''):
    if y == '':
        y = x
        
    if not os.path.exists('By Municip and HS4/EXP'):
        os.makedirs('By Municip and HS4/EXP')  # Create directory if doesn't exist
        
    for i in range(x, y+1):
        url = ''.join(('http://www.mdic.gov.br/balanca/bd/comexstat-bd/mun/EXP_', str(i), '_MUN.csv'))
        folder = 'By Municip and HS4/EXP'
        wget.download(url, folder)


#############
### Creates a dictionary with municipalities Exports data and their mesoregions from years x to y
### Raw data has only municipalities codes and not their names/mesoregions
#############

def exp_municip(x,y=''):
    if y == '':
        y = x
    d={}
    for i in range(x,y+1):
        file = ''.join(('By Municip and HS4/EXP/EXP_', str(i),'_MUN.csv')) # Defines file with export data
        dummy = pd.read_csv(file, sep=';') # Imports export data
        municip_codes = pd.read_excel('1_County_Codes.xlsx') # Import municipalities codes and names
        d['exp_municip_{0}'.format(i)] = dummy.merge(municip_codes, left_on= 'CO_MUN',
                                                     right_on='Código Município Completo (MDIC)') # Merges trade data and municipalities names
        d['exp_municip_{0}'.format(i)].drop(['Município', 'CO_MUN', 'Nome_Microrregião',
                                            'Microrregião Geográfica',
                                            'Código Município Completo (MDIC)'], axis=1, inplace=True) # Drops unnecessary columns 
        print('exp_municip done for {0}'.format(i))
        
        
    return d


#############
### Calls exp_municip and creates a dictionary with Mesoregions Exports data from years x to y
#############

def exp_meso(x, y=''):
    if y == '':
        y = x
    d = exp_municip(x,y)
    b={}
    for i in range(x,y+1):
        b['exp_meso_{0}'.format(i)] = d['exp_municip_{0}'.format(i)].groupby(['CO_ANO','Nome_Mesorregião','CD_GEOCME', 'CO_MES', 'CO_PAIS', 'SH4'],as_index=False).sum() # Consolidates trade data by mesoregion
        b['exp_meso_{0}'.format(i)].drop(['UF', 'Mesorregião Geográfica', 'Código Município Completo (IBGE)'], axis=1, inplace=True) # Drops unnecessary columns 
        print('exp_meso done for {0}'.format(i))
    return b

#############
### Calls exp_meso and saves mesoregions export data data as .csv. 
### Saves as multiple files because a single file would be too large.
#############

def save_meso_data_exports(x, y=''):
    if y == '':
        y = x   
        
    if not os.path.exists('By MesoRegion and HS4/EXP/'):
        os.makedirs('By MesoRegion and HS4/EXP/') # Create directory if doesn't exist
    
    for i in (range(x, y+1)):
        e = exp_meso(i)
        dummy = e['exp_meso_{0}'.format(i)]
        dummy.to_csv(''.join(('By MesoRegion and HS4/EXP/EXP_', str(i),'_MESO.csv')), encoding='UTF-8')
        print('Save exports done for {0}'.format(i))