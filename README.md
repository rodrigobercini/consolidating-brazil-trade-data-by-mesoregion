# Consolidating Brazilian Mesoregion trade data

The brazilian trade data is provided by Ministério da Indústria, Comércio Exterior e Serviços (MDIC) at their [official website](http://www.mdic.gov.br/index.php/comercio-exterior/estatisticas-de-comercio-exterior/base-de-dados-do-comercio-exterior-brasileiro-arquivos-para-download), where users can download trade data by municipality and state. There is no option to download trade data by [Mesoregion](https://en.wikipedia.org/wiki/Mesoregions_of_Brazil).

This repository contains a python code that downloads files from the MDIC website, merges raw municipalities trade data with municipalities names and codes, groups data by Mesoregion and finally outputs .csv files.

# Necessary file with municipalities mesoregions

There were mismatches for about 1.000 municipalities regarding MDIC and IBGE databases. Through a series of Vlookups and general feature engineering, the spreadsheet named `municipalities_lookup.xlsx` contains matching codes for MDIC and IBGE.

## How to use

First of all, install the requirements via `pip install -r requirements.txt`. After that, initiate a ExportsByMesoregion instance with the desired parameters and then call the download_data_and_aggregate_by_meso() method.

### Example

ExportsObject = ExportsByMesoregion(start_year=2020, end_year=2020, transaction_type='imports')
ExportsObject.download_data_and_aggregate_by_meso()

Output:
```
2020 - Municipalities imports finished downloading
2020 - Mesoregions info added to municipalities data
2020 - Mesoregions data aggregated
2020 - Mesoregions data saved
```

# Other uses

Although the main goal of this repo is to consolidate mesoregion trade data, one could use the exp_municip() or imp_municip() functions to consolidate bulk municipality data with municipalities names and UFs, since the files provided by MDIC contains only their code.

Raw data:

![Raw data](https://i.imgur.com/CUe0ZEe.jpg)

After exp_municip()/imp_municip():

![After exp_municip()/imp_municip()](https://i.imgur.com/cMnLLJP.jpg)

