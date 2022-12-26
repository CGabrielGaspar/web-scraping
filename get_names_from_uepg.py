from requests import get
from bs4 import BeautifulSoup
import pandas


print('Iniciando...')
url_base = "https://cps.uepg.br/inicio/uepg_2022/1"

dados_finais = list()

response = get(f"{url_base}/Resultado_UEPG.htm")

home = BeautifulSoup(response.text, 'html.parser')

tables = home.findAll('table')[1]

linhas = BeautifulSoup(f"{tables}", 'html.parser' ).findAll('tr')

curso_df = pandas.DataFrame(columns=["curso", "turno", "link", "nome"])

for curso in linhas[2:]:
    infos_curso = BeautifulSoup(f"{curso}", 'html.parser').findAll('td')

    print(f"Pegando informações do curso {infos_curso[0].text} do turno {infos_curso[2].text}")

    response = get(f"{url_base}/{infos_curso[0].a['href']}")

    cursos_todos_os_links = BeautifulSoup(response.text, 'html.parser').findAll('a')

    for curso_tag_link in cursos_todos_os_links:
        if curso_tag_link.text == "Lista de Espera" or curso_tag_link.text == "Retornar" or not curso_tag_link.get('href'):
            continue

        curso_dict = dict()
        curso_dict["curso"] = infos_curso[0].text
        curso_dict["turno"] = infos_curso[2].text
        curso_dict["link"] = f"{url_base}/{curso_tag_link.get('href')}"

        alunos_response = get(f"{url_base}/{curso_tag_link.get('href')}")

        dataframe = pandas.read_html(alunos_response.text)[1]

        for nome in dataframe[0][1:].tolist():
            curso_dict["nome"] = nome

            curso_df = pandas.concat([pandas.DataFrame(curso_dict, index=[-1]), curso_df.loc[:]]).reset_index(drop=True)


print("Salvando arquico xlsx")
curso_df.to_excel('resultado_uepg-2.xlsx')
print("Finalizado!")
