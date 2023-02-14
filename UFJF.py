from requests import get
from bs4 import BeautifulSoup
import pandas
import json
import re

print("Iniciando...")

link_base = "http://www4.vestibular.ufjf.br/2023/resultadofinalpism3/"

with open("./infos/infos.json", "r") as f:
    infos = json.load(f)

link = infos["vestibulares"].get("UFJF", {}).get("link")
response = get(link)

home = BeautifulSoup(response.text, 'html.parser')
tables = home.findAll("table")[-1]
linhas = BeautifulSoup(f"{tables}", 'html.parser').findAll('tr')

curso_df = pandas.DataFrame(
    columns=["nome", "universidade", "curso", "local", "pontos", "classificacao", "link"])
final = []
find_course = re.compile(r'<td><a.*?\.html">(.*?)<\/a><\/td>')

for local in linhas[1:]:
    localization = local.text
    infos_curso = BeautifulSoup(f"{local}", 'html.parser').findAll('td')

    cursos = get(f"{link_base}/{infos_curso[0].a['href']}")

    pagina_cursos = BeautifulSoup(cursos.text, 'html.parser')
    tables_cursos = pagina_cursos.findAll("table")[-1]
    linhas_cursos = BeautifulSoup(f"{tables_cursos}", 'html.parser').findAll('tr')

    for curso_especifico in linhas_cursos[1:]:
        curso = curso_especifico.text

        infos_grupos = BeautifulSoup(f"{curso_especifico}", 'html.parser').findAll('td')

        grupos = get(f"{link_base}/{infos_grupos[0].a['href']}")

        pagina_grupos = BeautifulSoup(grupos.text, 'html.parser')
        tables_grupos = pagina_grupos.findAll("table")[-1]
        linhas_grupos = BeautifulSoup(f"{tables_grupos}", 'html.parser').findAll('tr')

        for grupo in linhas_grupos:
            if "Selecione o grupo" in grupo:
                pass

            grouping = grupo.text
            infos_alunos = BeautifulSoup(f"{grupo}", 'html.parser').findAll('td')
            if not infos_alunos:
                continue

            alunos = get(f"{link_base}/{infos_alunos[0].a['href']}")

            pagina_alunos = BeautifulSoup(alunos.text, 'html.parser')
            tables_alunos = pagina_alunos.findAll("script")[-1].string
            linhas_alunos = BeautifulSoup(f"{tables_alunos}", 'html.parser')

            names = re.findall('("data": \[.*\])', str(linhas_alunos))

            names = names[0].split('"nome":')

            for nome in names:
                if '"data": [' in nome:
                    nome = ""
                nome = nome.encode('latin1').decode('utf8')
                nome = nome.replace('"', "")
                nome = localization + "|" + curso + "|" + grouping + "|" + nome + "|" + f"{link_base}/{infos_alunos[0].a['href']}"
                final.append(nome)

print(final)
file = open('resultado_ufjf.txt', 'w')
for i in final:
    file.write(str(i) + "\n")
file.close()

'''
Este código realiza a extração de informações de resultados de vestibular da UFJF e salva os dados em um arquivo de texto.
Ele usa a biblioteca requests para fazer solicitações HTTP para as páginas da web, a biblioteca BeautifulSoup para analisar
e extrair informações da página da web em HTML, a biblioteca pandas para manipulação de dados em forma de tabela e a biblioteca
re para manipulação de expressões regulares. 
A saída do código é uma lista de strings que contém informações sobre os alunos, seus respectivos cursos, locais e grupos
e o link de suas informações. 
'''