from requests import get
from bs4 import BeautifulSoup
import pandas

print('Iniciando...')
url_base = "https://servicos.nc.ufpr.br/documentos/PS2022/aprovados/"

response = get(f"{url_base}")
home = BeautifulSoup(response.text, 'html.parser')

tables = home.findAll("table")[-1]

children = tables.findChildren("tr")

linhas = BeautifulSoup(f"{home}", 'html.parser').findAll('tr')

curso_df = pandas.DataFrame(
    columns=["nome", "universidade", "curso", "local", "semestre ingresso", "número de inscrição", "link"])

for curso in linhas[11:]:
    infos_curso = BeautifulSoup(f"{curso}", 'html.parser').findAll('td')

    dados_curso = infos_curso[0].text.split(" - ")
    if dados_curso[0] == "Letras":
        dados_curso[0] = f"{dados_curso[0]} - {dados_curso[1]}"
    print(f"Pegando informações do curso {dados_curso[0]}")

    response = get(f"{url_base}/{infos_curso[1].a['href']}")

    dataframe = pandas.read_html(response.text)[3]
    dataframe = dataframe.reset_index()

    curso_dict = {"nome": "",
                  "universidade": "UFPR",
                  "curso": dados_curso[0],
                  "local": dados_curso[-3],
                  "semestre ingresso": "",
                  "número de inscrição": "",
                  "link": f"{url_base}/{infos_curso[1].a['href']}"}

    for index, row in dataframe.iterrows():
        if row[0] == "Número de Inscrição" or row[0] == "Não há candidatos aprovados":
            continue

        curso_dict["nome"] = row[1]
        curso_dict["semestre ingresso"] = row[2]
        curso_dict["número de inscrição"] = row[0]

        curso_df = pandas.concat([pandas.DataFrame(curso_dict, index=[-1]), curso_df.loc[:]]).reset_index(drop=True)

print("Salvando arquico xlsx")
curso_df.to_excel('resultado_ufpr.xlsx')
print("Finalizado!")