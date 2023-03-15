from requests import get
from bs4 import BeautifulSoup
import pandas
import json

print('Iniciando...')

# Extrai as informações do Json
with open("./infos/infos.json", "r") as f:
    infos = json.load(f)

# Acessa o site
link = infos["vestibulares"].get("UFPRVest", {}).get("link")
response = get(link)

# Na página, encontra as tabelas. Na última tabela, seleciona as linhas.
home = BeautifulSoup(response.text, 'html.parser')
tables = home.findAll("table")[-1]
children = tables.findChildren("tr")
linhas = BeautifulSoup(f"{tables}", 'html.parser').findAll('tr')

# Cria o DF com os titulos das colunas.
curso_df = pandas.DataFrame(
    columns=["nome", "universidade", "curso", "local", "ação afirmativa", "número de inscrição", "link"])

# Pra cada curso encontrado, faça tudo isso:... (O [1:] é para ignorar a primeira linha, que é titulo)
for curso in linhas[1:]:
    infos_curso = BeautifulSoup(f"{curso}", 'html.parser').findAll('td')

    dados_curso = infos_curso[0].text.split(" - ")

    # Letras da um erro e precisa ser corrigido nessas linhas.
    if dados_curso[0] == "Letras":
        dados_curso[0] = f"{dados_curso[0]} - {dados_curso[1]}"
    print(f"Pegando informações do curso {dados_curso[0]}")

    # Encontra e acessa todos os links associdados a cada item da tabela.
    response = get(f"{infos_curso[1].a['href']}")

    # Dentro de cada link, lê o HTML.
    dataframe = pandas.read_html(response.text)[0]
    dataframe = dataframe.reset_index()

    # Preenche as informações que já foram encontradas. Informações que se repetem pra vários alunos.
    curso_dict = {"nome": "",
                  "universidade": "UFPR",
                  "curso": dados_curso[0].encode('latin1').decode('utf8'),
                  "local": dados_curso[-2].encode('latin1').decode('utf8'),
                  "ação afirmativa": "",
                  "número de inscrição": "",
                  "link": f"{infos_curso[1].a['href']}"}

    # Pra cada aluno, recupera as informação específicas e preenche pra cada aluno.
    for index, row in dataframe.iterrows():
        if row[0] == "InscriÃ§Ã£o" or row[0] == "Inscrição":
            continue

        # O encode e decode é um macete pra resolver os problema de letras não identificadas. Tipo "InscriÃ§Ã£o"
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
