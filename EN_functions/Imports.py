#############
### Scrapes MDIC official website for imports by municipalities and saves files in system
#############

def scrape_imp_municip(x, y=''):
    if y == '':
        y = x
        
    if not os.path.exists('By Municip and HS4/IMP'):
        os.makedirs('By Municip and HS4/IMP')  # Create directory if doesn't exist
        
    for i in range(x, y+1):
        url = ''.join(('http://www.mdic.gov.br/balanca/bd/comexstat-bd/mun/IMP_', str(i), '_MUN.csv'))
        folder = 'By Municip and HS4/IMP'
        wget.download(url, folder)

#############
### Creates a dictionary with municipalities Imports data and their mesoregions from years x to y
### Raw data has only municipalities codes and not their names/mesoregions
#############

def imp_municip(x,y=''):
    if y == '':
        y = x
    d={}
    for i in range(x,y+1):
        file = ''.join(('By Municip and HS4/IMP/IMP_', str(i),'_MUN.csv')) # Defines file with import data
        dummy = pd.read_csv(file, sep=';') # Imports import data
        municip_codes = pd.read_excel('1_County_Codes.xlsx') # Import municipalities codes and names
        d['imp_municip_{0}'.format(i)] = dummy.merge(municip_codes, left_on= 'CO_MUN', right_on='Código Município Completo (MDIC)') # Merges trade data and municipalities names
        d['imp_municip_{0}'.format(i)].drop(['Município', 'CO_MUN', 'Nome_Microrregião',
                                            'Microrregião Geográfica',
                                            'Código Município Completo (MDIC)'], axis=1, inplace=True)  # Drops unnecessary columns
        print('imp_municip done for {0}'.format(i))
    return d

#############
### Calls imp_municip and creates a dictionary with Mesoregions Imports data from years x to y
### It's not possible to get this data via the Official MDIC website
#############

def imp_meso(x, y=''):
    if y == '':
        y = x
    d = imp_municip(x,y)
    b={}
    for i in range(x,y+1):
        b['imp_meso_{0}'.format(i)] = d['imp_municip_{0}'.format(i)].groupby(['CO_ANO','Nome_Mesorregião','CD_GEOCME', 'CO_MES', 'CO_PAIS', 'SH4'],as_index=False).sum() # Consolidates trade data by mesoregion
        b['imp_meso_{0}'.format(i)].drop(['UF', 'Mesorregião Geográfica', 'Código Município Completo (IBGE)'], axis=1, inplace=True) # Drops unnecessary columns
        print('imp_meso done for {0}'.format(i))
    return b


#############
### Calls imp_meso and saves mesoregions import data as .csv. 
### Saves as multiple files because a single file would be too large.
#############

def save_meso_data_imports(x, y=''):
    if y == '':
        y = x
        
    if not os.path.exists('By MesoRegion and HS4/IMP/'):
        os.makedirs('By MesoRegion and HS4/IMP/')  # Create directory if doesn't exist
        
    for i in (range(x, y+1)):
        e = imp_meso(i)
        dummy = e['imp_meso_{0}'.format(i)]
        dummy.to_csv(''.join(('By MesoRegion and HS4/IMP/IMP_', str(i),'_MESO.csv')), encoding='UTF-8')
        print('Save imports done for {0}'.format(i))
