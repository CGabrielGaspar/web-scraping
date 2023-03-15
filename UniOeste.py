from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time
from selenium import webdriver

# Var onde será salvo texto final
text = ""


def wait_loading(driver, loader):
    """
    Verifica se a pagina está carregando
    :return:
    """
    try:
        if loader.is_displayed():
            print("Loading page...")
            time.sleep(1)
            wait_loading(driver, loader)
        else:
            return
    except NoSuchElementException:
        return


def scroll_into_view(driver, element):
    """
    Posiciona o elemento no meio da tela para que se possa interagir com ele sem dificuldades.
    :param element:
    :return:
    """
    size = element.size
    location = element.location

    viewport_width = driver.execute_script("return document.documentElement.clientWidth;")
    viewport_height = driver.execute_script("return document.documentElement.clientHeight;")

    x = location['x'] + size['width'] / 2 - viewport_width / 2
    y = location['y'] + size['height'] / 2 - viewport_height / 2

    driver.execute_script(f"window.scrollTo({x}, {y});")


# Inicia o webdriver. Webdriver é um saco e precisa ser atualizado toda vez que o navegador atualiza.
url = "https://www4.unioeste.br/vestibular/vestibular2023/resultados_vestibular.php"
driver = webdriver.Chrome()

# Acessa o Site
driver.get(url)

# Espera um pouco e clica no botão
driver.implicitly_wait(10)
driver.find_elements(By.CLASS_NAME, "botaoResultado")[0].click()
driver.implicitly_wait(10)

# Encontra a caixa para interagir
box1 = driver.find_elements(By.CLASS_NAME, "labelInput")
# Define o objeto de "Carregando"
loader = driver.find_element(By.XPATH, "/html/body/div/section[2]/div/div/div/div/div[1]/div[1]")

# Pra cada elemento na primeira caixa, tudo a partir daqui será repetido para cada elemento. (Campus)
for element in box1:
    print(f"Pegando: {element.text}")
    time.sleep(1)
    scroll_into_view(driver, element)  # Bota o elemento na tela
    element.click()
    wait_loading(driver, loader)
    print(element.text)

    box2 = driver.find_elements(By.CLASS_NAME, "resultadoFiltroWrapper")[1]  # Encontra a caixa 2
    box2_1 = box2.find_elements(By.TAG_NAME, "label")  # Encontra cada elemento na caixa 2

    # Pra cada elemento na segunda caixa, tudo a partir daqui será repetido para cada elemento. (Curso)
    for element2 in box2_1:
        print(f"Pegando: {element2.text}")
        scroll_into_view(driver, element2)
        element2.click()
        wait_loading(driver, loader)

        print(f"Pegando Lista...")
        table = driver.find_element(By.ID, "lista")

        text = text + table.text

text.encode("utf-8")  # Define o encoding para UFT-8 para não dar problema na extração.
with open("./resultados/UniOeste.txt", "w", encoding="utf-8") as f:
    f.write(text)

# Fecha o webdriver quando tiver acabado.
driver.quit()

'''
Esse código automatiza a extração de resultados de um site de vestibular. Ele usa o Selenium para acessar o site,
interagir com os elementos da página, clicar em botões, rolar a página, esperar o carregamento e extrair informações
da tabela de resultados. O resultado final é salvo em um arquivo de texto UTF-8, estilo CSV.
'''