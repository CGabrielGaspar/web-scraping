from requests import get
from bs4 import BeautifulSoup
import pandas
import json
import os
import tabula

print("Iniciando...")

# Recupera informações do json.
with open("./infos/infos.json", "r") as f:
    infos = json.load(f)

# Acessa o site
link = infos["vestibulares"].get("UNB(PAS)", {}).get("link")
response = get(link)

files = os.listdir("./PDFs")
for file in files:
    if "UNB" in file:
        Pas_file = file

print(Pas_file)

extracted_tables = tabula.read_pdf(f"./PDFs/{Pas_file}", pages=f"1-{len(Pas_file)}")

table = pandas.concat(extracted_tables)

print(table)

table.to_excel('./resultados/resultado_unppas.xlsx', index=False)