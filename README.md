Find a english version of this README file [here](https://github.com/rodrigobercinimartins/export-import-por-mesorregiao-brasil/blob/master/EN_README.md).
# Consolidando exportações/importações de mesorregiões brasileiras

Os dados de comércio internacional do Brasil são fornecidos pelo Ministério da Indústria, Comércio Exterior e Serviços (MDIC) em seu [site oficial](http://www.mdic.gov.br/index.php/comercio-exterior/estatisticas-de-comercio-exterior/base-de-dados-do-comercio-exterior-brasileiro-arquivos-para-download), onde é possível fazer o download de dados por município e estado. Não há opção de download para comércio internacional por [Mesorregião](https://pt.wikipedia.org/wiki/Mesorregi%C3%B5es_e_microrregi%C3%B5es_do_Brasil).

Este repositório contém um código que extrai dados do MDIC, cruza dados brutos de municípios com seus nomes e regiões, agrupa os dados por mesorregião e exporta tabelas em arquivos CSV.

## Bibliotecas necessárias

```
pip install pandas
pip install wget
```

## Arquivo necessário com códigos de municípios e regiões

[Códigos e nomes de municípios e regiões](https://drive.google.com/open?id=1FU_1V7yYW-jILYy-KPW7UgvtYfYU7jRk) - Há cerca de 1.000 municípios com códigos inconsistentes ao cruzar as tabelas do MDIC e do IBGE. Através de uma série de Procvs e engenheria de recursos, esta contém os códigos corretos e atualizados.

## Como usar

Primeiramente, é preciso rodar a função scrape_exp_municip com os anos desejados, isso irá extrair dados do MDIC e salvar no sistema. Depois, chamar a função save_meso_data_imports novamente com os anos desejados, ela chamará as outras funções e salvará os dados consolidados no sistema.

### Exemplo

scrape_exp_municip(2018, 2019)

Dados extraídos do MDIC e salvos no sistema

save_meso_data_exports(2018, 2019)

Dados consolidados e salvos no sistema

```
imp_municip done for 2018
imp_meso done for 2018
Save imports done for 2018
imp_municip done for 2019
imp_meso done for 2019
Save imports done for 2019
```


## Outros usos

Embora o objetivo final deste repositório ser a consolidação de dados por mesorregião, as funções exp_municip() e imp_municip() consolidam valores comercializados por municípios com seus nomes, o que é útil já que os dados brutos providos pelo MDIC só possuem o código de município, impossibilitando sua análise.

Dados brutos:

![Dados brutos](https://i.imgur.com/CUe0ZEe.jpg)

Após exp_municip()/imp_municip():

![Após exp_municip()/imp_municip()](https://i.imgur.com/cMnLLJP.jpg)
