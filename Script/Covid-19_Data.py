# python 3.8.3
# pandas 1.0.4
import pandas as pd 
import requests

select = int(input("Se nome da cidade não tem acento, digite 1. Caso contrário digite 2: "))

if select == 1:
    state = input("Entre com o Estado (ex.: SP): ")
    city = input("Entre com a cidade (ex.: Campinas ou Rio+Branco): ")
    ibge = ""
else:
    ibge = input("Entre com o código do IBGE: ")
    state =""
    city =""

# Cidades com acento, usar código ibge do município: https://www.ibge.gov.br/explica/codigos-dos-municipios.php
# Exemplo = São Paulo - 3550308
url = "https://brasil.io/api/dataset/covid19/caso_full/data/?search=&epidemiological_week=&is_last=True&order_for_place=&state="+state+"&city="+city+"&city_ibge_code="+ibge+"&place_type=city&last_available_date=&is_last=True&is_repeated=False"
data = requests.get(url).json()
    
df = pd.DataFrame.from_dict(data)
df_2 = df['results']
fdata =pd.json_normalize(df_2)

cidade = fdata.loc[0, 'city'] + "-" + fdata.loc[0, 'state']
populacao = fdata.loc[0, 'estimated_population_2019']
semana = fdata.loc[0, 'epidemiological_week']
date = fdata.loc[0, 'date']
casos_conf = fdata.loc[0, 'last_available_confirmed']
casos_novos = fdata.loc[0, 'new_confirmed']
casos_100k = fdata.loc[0, 'last_available_confirmed_per_100k_inhabitants'].round(2)
taxa_contaminacao = round((casos_conf/populacao)*100, 2) 
mortes_conf = fdata.loc[0, 'last_available_deaths']
mortes_novas = fdata.loc[0, 'new_deaths']
mortes_ratio = fdata.loc[0, 'last_available_death_rate'].round(4)
taxa = round((float(mortes_ratio) * 100.00),2)

print("Cidade de: ", cidade)
print("População de: ", populacao)
print("Dados de", date, "estamos na semana epidemiológica: ", semana)
print("O número de casos confirmados é", casos_conf, "sendo que são", casos_novos, "novos.")
print("Temos uma taxa de contaminação ", taxa_contaminacao, "%, com", casos_100k, 'para cada 100mil habitantes.')
print("O número de mortes confirmados é", mortes_conf, "sendo que são", mortes_novas, "novas.")
print("A taxa de mortalidade é de: ", taxa, "%")