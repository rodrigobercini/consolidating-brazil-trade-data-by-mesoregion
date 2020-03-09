# Consolidating Brazilian Mesoregion trade data

The brazilian trade data is provided by Ministério da Indústria, Comércio Exterior e Serviços (MDIC) at their [official website](http://www.mdic.gov.br/index.php/comercio-exterior/estatisticas-de-comercio-exterior/base-de-dados-do-comercio-exterior-brasileiro-arquivos-para-download), where users can download trade data by municipality and state. There is no option to download trade data by [Mesoregion](https://en.wikipedia.org/wiki/Mesoregions_of_Brazil).

This repository contains a python code that scrapes MDIC website, merges raw municipalities trade data with municipalities names and codes, groups data by Mesoregion and finally outputs .csv files.

# Necessary libraries

```
pip install pandas
pip install wget
```

# Necessary file with municipalities mesoregions

There were mismatches for about 1.000 municipalities regarding MDIC and IBGE databases. Through a series of Vlookups and general feature engineering, the spreadsheet below contains matching codes for MDIC and IBGE.

[Municipalities/states codes and names](https://drive.google.com/open?id=1FU_1V7yYW-jILYy-KPW7UgvtYfYU7jRk)

## How to use

First of all, one has to download the file above and place it in the folder with the code. Then, just call exp_by_meso() with the desired years, the function will call the other functions (exp_municip() and exp_meso()), that will consolidate the data and save the files in the local system.

### Example

exports_by_meso(1997)

Output:
```
100% [........................................................................] 18727021 / 18727021
 Scrape done for 1997
Exp_municip done for 1997
Exp_meso done for 1997
Save exports done for 1997
```

# Other uses

Although the main goal of this repo is to consolidate mesoregion trade data, one could use the exp_municip() or imp_municip() functions to consolidate bulk municipality data with municipalities names and UFs, since the files provided by MDIC contains only their code.

Raw data:

![Raw data](https://i.imgur.com/CUe0ZEe.jpg)

After exp_municip()/imp_municip():

![After exp_municip()/imp_municip()](https://i.imgur.com/cMnLLJP.jpg)

