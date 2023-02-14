import json
from requests import get
from bs4 import BeautifulSoup
import pandas
import traceback


class vestibular:

    def __init__(self):
        with open("./infos/infos.json", "r") as f:
            self.infos = json.load(f)

    def get_base_html(self, link):
        '''
        Retorna a página inicial onde começará o parse.

        :param str vest: Link inicial do parse.
        :return: uma BS com o html do site.
        '''
        response = get(link)
        return BeautifulSoup(response.text, "html.parser")

    def get_lines(self, base_html):
        '''
        Retorna as tabelas disponívels no html.

        :param base_html: A html base onde ocorrerá a busca por tabelas.
        :return: as linhas da tabela
        '''
        ret_lines = []
        tables = base_html.findAll("table")
        lines = BeautifulSoup(f"{tables}", 'html.parser').findAll("tr")

        for line in lines:
            if str(line).startswith("<tr>"):
                ret_lines.append(line)
        return ret_lines

    def response_table(self, vest, line):
        base = self.infos["vestibulares"].get(vest, {}).get("link_base")

        if "https://" in str(line):
            return [get(f"{line.a['href']}"), f"{line.a['href']}"]

        if base:
            if "href" in str(line):
                return [get(f"{base}/{line.a['href']}"), f"{base}/{line.a['href']}"]

    def get_df(self, vest):
        df = self.infos["vestibulares"].get(vest, {}).get("colunas")
        return df

    def get_tables(self, link):
        html = self.get_base_html(link)

        return self.get_lines(html)

    def get_names(self, vest, link):
        html = self.get_base_html(link)
        lines = self.get_lines(html)

        for line in lines:
            response = self.response_table(vest, line)
            if response is None:
                continue

            else:
                tables = pandas.read_html(response[0].text, header=0)

                if "nome" not in str(tables) or "Nome" not in str(tables):
                    self.get_names(vest, response[1])

                for table in tables:
                    if "nome" in str(table.columns) or "Nome" in str(table.columns):
                        alunos = table
                        print("Foi!")
                        print(alunos)

    def extract(self, vest):
        link_base = self.infos["vestibulares"].get(vest, {}).get("link")
        lines = self.get_tables(link_base)
        dataframe = self.get_df(vest)

        self.get_names(vest, link_base)

        # for line in lines:
        #     response = self.response_table(vest, line)
        #
        #     try:
        #         dataframes = pandas.read_html(response[0].text)
        #     except:
        #         continue
        #
        #     for dataframe in dataframes:
        #         if "nome" in str(dataframe.columns) or "Nome" in str(dataframe.columns):
        #             alunos = dataframe
        #         else:
        #             next_level_lines = self.get_tables(response[1])
        #
        #             for line_2 in next_level_lines:
        #                 print(line_2)
        #
        #
        #             # lines_2 = self.get_lines()
        #             # next_response = self.response_table(vest, )
        #             print("precisa de outro nível")


if __name__ == "__main__":
    v = vestibular()
    # v.extract("UFPRVest")
    v.extract("UEPG")
