from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

app = Flask(__name__)

class Registro():
    def __init__(self, registro, fila):
        self.registro = registro
        self.fila = fila

def get_text_from_css_selector(urls, css_selector):
    # Configurar opções do Chrome
    options = Options()
    options.page_load_strategy = 'eager'
    # options.add_argument("--start-minimized")  # Iniciar minimizado
    
    # Caminho para o chromedriver (ajuste conforme necessário)
    service = Service('chromedriver.exe')  # Substitua pelo caminho real do chromedriver
    # Inicializa o driver do Chrome
    driver = webdriver.Chrome(service=service, options=options)
    driver.minimize_window()

    registros = []
    try:
        #Admin

        #Local
        
        time.sleep(2)

        login = driver.find_element(By.CSS_SELECTOR, "input")
        login.send_keys("")
        avancar = driver.find_element(By.CSS_SELECTOR, "button")
        avancar.click()

        senha = driver.find_element(By.CSS_SELECTOR, "input")
        senha.send_keys("")
        avancar = driver.find_element(By.CSS_SELECTOR, "button")
        avancar.click()
        
        # Espera um tempo para que o JavaScript seja executado (ajuste conforme necessário)
        time.sleep(2)
        for url in urls:
            driver.get(url)
            insert_registro(css_selector, driver, registros, url)
    finally:
        # Fecha o driver do Chrome
        driver.quit()
        return registros

def insert_registro(css_selector, driver, registros, url):
    try:
        # aguarda até que o elemento com o seletor CSS seja encontrado
        element = WebDriverWait(driver, 1).until(
            # Captura pelo XPATH, o elemento
            EC.visibility_of_element_located((By.XPATH, css_selector))
        )
        print("Elemento.Text: ", element.text)
        split = element.text.split()
        registros.append(Registro(split[1], url.split('/')[-1]))
    except TimeoutException:
        # Caso haja timeout, registra "TimeOut"
        registros.append(Registro('0', url.split('/')[-1]))

@app.route('/')
def index():
    # Caminho do site
    urls = [
        #Local
        

        #Admin
        
            ]
    
    css_selector = "//*[@id='root']/div/section/div/div[2]/div[1]/label[2]"

    registros = get_text_from_css_selector(urls, css_selector)

    return render_template('index.html', registros=registros)

if __name__ == '__main__':
    app.run(debug=True)