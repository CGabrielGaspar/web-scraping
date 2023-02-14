from requests import get
from bs4 import BeautifulSoup
import pandas
import json


print('Iniciando...')

with open("./infos/infos.json", "r") as f:
    infos = json.load(f)

link = infos["vestibulares"].get("UFPRVest", {}).get("link")
response = get(link)

home = BeautifulSoup(response.text, 'html.parser')
tables = home.findAll("table")[-1]
children = tables.findChildren("tr")
linhas = BeautifulSoup(f"{tables}", 'html.parser').findAll('tr')

curso_df = pandas.DataFrame(
    columns=["nome", "universidade", "curso", "local", "ação afirmativa", "número de inscrição", "link"])

for curso in linhas[1:]:
    infos_curso = BeautifulSoup(f"{curso}", 'html.parser').findAll('td')

    dados_curso = infos_curso[0].text.split(" - ")

    if dados_curso[0] == "Letras":
        dados_curso[0] = f"{dados_curso[0]} - {dados_curso[1]}"
    print(f"Pegando informações do curso {dados_curso[0]}")

    response = get(f"{infos_curso[1].a['href']}")

    dataframe = pandas.read_html(response.text)[0]
    dataframe = dataframe.reset_index()

    curso_dict = {"nome": "",
                  "universidade": "UFPR",
                  "curso": dados_curso[0].encode('latin1').decode('utf8'),
                  "local": dados_curso[-2].encode('latin1').decode('utf8'),
                  "ação afirmativa": "",
                  "número de inscrição": "",
                  "link": f"{infos_curso[1].a['href']}"}

    for index, row in dataframe.iterrows():
        if row[0] == "InscriÃ§Ã£o" or row[0] == "Inscrição":
            continue

        curso_dict["nome"] = str(row[2]).encode('latin1').decode('utf8')
        curso_dict["ação afirmativa"] = row[3].encode('latin1').decode('utf8')
        curso_dict["número de inscrição"] = row[1]

        curso_df = pandas.concat([pandas.DataFrame(curso_dict, index=[-1]), curso_df.loc[:]]).reset_index(drop=True)

print("Salvando arquico xlsx")
curso_df.to_excel('./resultados/resultado_ufprVest.xlsx', index=False)
print("Finalizado!")

'''
Esse código realiza uma web scraping do site de resultados da UFPR que apresenta informações sobre os resultados dos 
vestibulares. 
O código pega informações sobre cada curso, como nome, universidade, curso, local, ação afirmativa e número de inscrição,
e as armazena em um arquivo Excel.
'''