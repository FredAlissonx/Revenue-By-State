from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os


chrome_options = Options()

download_dir = r"C:\SchoolsBrazilEnem\data"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

prefs = {
    "download.default_directory": download_dir,  
    "download.prompt_for_download": False,  
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)

chrome_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

url = "https://dados.gov.br/dados/conjuntos-dados/resultado-da-arrecadacao"

driver.get(url)

driver.implicitly_wait(10)

button_resources = driver.find_element(by="css selector", value='button[data-v-55a04e1a][id="btnCollapse"]')

button_resources.click()

wait = WebDriverWait(driver=driver, timeout=10)

arrecadacao_div = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[h4[text()="Arrecadação por Estado"]]')))

download_button = arrecadacao_div.find_element(By.ID, 'btnDownloadUrl')
download_button.click()

time.sleep(5)
driver.quit()
