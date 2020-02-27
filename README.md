# Consolidation Brazilian Mesoregion trade data

The brazilian trade data is provided by Ministério da Indústria, Comércio Exterior e Serviços (MDIC) at their [official website] (http://www.mdic.gov.br/index.php/comercio-exterior/estatisticas-de-comercio-exterior/base-de-dados-do-comercio-exterior-brasileiro-arquivos-para-download), where users can download trade data by municipality and state. There is no option to download trade data by [Mesoregion](https://en.wikipedia.org/wiki/Mesoregions_of_Brazil).

This repository contains a python code that scrapes MDIC website, merges raw municipalities trade data with municipalities names and codes, groups data by Mesoregion and finally outputs .csv files.

# Needed libraries

```
pip install pandas
pip install wget
```

# Necessary file with municipalities mesoregions

There were mismatches for about 1.000 municipalities regarding MDIC and IBGE databases. Through a series of Vlookups and general feature engineering, the spreadsheet below contains matching codes for MDIC and IBGE.

[Municipalities/states codes and names](https://drive.google.com/open?id=1FU_1V7yYW-jILYy-KPW7UgvtYfYU7jRk)

# Other uses

Although the main goal of this repo is to consolidate mesoregion trade data, one could use the exp_municip() or imp_municip() functions to consolidate bulk municipality data with municipalities names and UFs, since the files provided by MDIC contains only their code.

Raw data:

![Raw data](https://raw.githubusercontent.com/rodrigobercinimartins/BR-meso-region-trade-data/master/Readme%20files/Raw%20data.jpg)

After exp_municip()/imp_municip():

![After exp_municip()/imp_municip()](https://raw.githubusercontent.com/rodrigobercinimartins/BR-meso-region-trade-data/master/Readme%20files/After%20functions.jpg)

