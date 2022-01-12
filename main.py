import pandas as pd
import os
import ssl 

# I'm getting SSL certificates issues when downloading files from MDIC.
# The code below is a hack to get around this issue.
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

class ExportsByMesoregion:
    def __init__(self
                , start_year:int
                , end_year:int = None
                , transaction_type:str='exports'):

        self.start_year = start_year
        
        if end_year is not None:
            self.end_year = end_year
        else:
            self.end_year = start_year

        self.TRANSACTION_TYPES = {
            'exports':'EXP'
            , 'imports':'IMP'
        }

        if transaction_type in self.TRANSACTION_TYPES:
            self.transaction_type = transaction_type
        else:
            raise ValueError(f"Invalid transaction type. Valid values are: {''.join(self.TRANSACTION_TYPES)}")

        self.BASE_URL = 'https://balanca.economia.gov.br/balanca/bd/comexstat-bd/mun/'
        self.REPO_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
        self.MUN_FOLDER_PATH = os.path.join(self.REPO_FOLDER_PATH, 'data', 'municipalities',"")
        self.MESO_FOLDER_PATH = os.path.join(self.REPO_FOLDER_PATH, 'data', 'mesoregions',"")
        self.MUN_LOOKUP_FILENAME = os.path.join(self.REPO_FOLDER_PATH, 'municipalities_lookup.xlsx')

    def create_folder_if_not_exists(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    def get_file_name(self, transaction_type, year, division_type):
        return f'{self.TRANSACTION_TYPES[transaction_type]}_{year}_{division_type}.csv'
    
    
    def download_mun_data(self):

        self.create_folder_if_not_exists(self.MUN_FOLDER_PATH)

        for year in range(self.start_year, self.end_year+1):
            file_name = self.get_file_name(self.transaction_type, year, 'MUN')
            file_path = f'{self.MUN_FOLDER_PATH}{file_name}'
            if os.path.isfile(file_path):
                print(f'{year} - Mun {self.transaction_type} already exists. Skipping download...')
                continue
            url = f'{self.BASE_URL}{file_name}'
            pd.read_csv(url, sep=';', encoding='UTF-8').to_csv(file_path, sep=';', encoding='UTF-8')
            print(f'{year} - Municipalities {self.transaction_type} finished downloading')

    def add_meso_to_mun_data(self, year):
        
        mun_exp_filename = self.get_file_name(self.transaction_type, year, 'MUN')
        mun_exports = pd.read_csv(f'{self.MUN_FOLDER_PATH}{mun_exp_filename}', sep=';')
        municip_codes = pd.read_excel(self.MUN_LOOKUP_FILENAME)
        mun_with_meso = mun_exports.merge(municip_codes, left_on= 'CO_MUN',
                                                    right_on='Código Município Completo (MDIC)')
        mun_with_meso.drop(['Município', 'CO_MUN', 'Nome_Microrregião',
                                            'Microrregião Geográfica',
                                            'Código Município Completo (MDIC)'], axis=1, inplace=True)
        print(f'{year} - Mesoregions info added to municipalities data')
        return mun_with_meso

    def aggregate_by_mesoregion(self, year, mun_with_meso):

        meso_aggregated = mun_with_meso.groupby(['CO_ANO','Nome_Mesorregião','CD_GEOCME', 'CO_MES', 'CO_PAIS', 'SH4'],as_index=False).sum() # Consolida dados por mesorregião
        meso_aggregated.drop(['UF', 'Mesorregião Geográfica', 'Código Município Completo (IBGE)'], axis=1, inplace=True)
        print(f'{year} - Mesoregions data aggregated')
        return meso_aggregated

    def download_data_and_aggregate_by_meso(self):
        
        self.create_folder_if_not_exists(self.MESO_FOLDER_PATH)
        self.download_mun_data()

        for year in (range(self.start_year, self.end_year+1)):
            
            mun_with_meso = self.add_meso_to_mun_data(year)
            meso_aggregated = self.aggregate_by_mesoregion(year, mun_with_meso)

            meso_exp_filename = self.get_file_name(self.transaction_type, year, 'MESO')
            
            meso_aggregated.to_csv(f'{self.MESO_FOLDER_PATH}{meso_exp_filename}', encoding='UTF-8')
            print(f'{year} - Mesoregions data saved')

    def download_data_and_add_meso_info(self):
        self.create_folder_if_not_exists(self.MUN_FOLDER_PATH)
        self.download_mun_data()

        final_df = pd.DataFrame()
        for year in (range(self.start_year, self.end_year+1)):
            mun_with_meso = self.add_meso_to_mun_data(year)
            final_df = final_df.append(mun_with_meso)

        return final_df
        

if __name__ == '__main__':
    ExportsObject = ExportsByMesoregion(start_year=2020, end_year=2020, transaction_type='imports')
    ExportsObject.download_data_and_aggregate_by_meso()