from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os


class FileHandlerArrecadacaoEstado:
    def __init__(self, download_dir):
        self.download_dir = download_dir
        self.chrome_options = self.define_options()
        self.driver = None

    def define_options(self) -> Options:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options

    def setup_driver(self):
        chrome_service = Service(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=chrome_service, options=self.chrome_options)
        self.driver.implicitly_wait(10)
        
    
    def download_file(self):
        try:
            self.setup_driver()
            url = "https://dados.gov.br/dados/conjuntos-dados/resultado-da-arrecadacao"

            self.driver.get(url)

            button_resources = self.driver.find_element(By.CSS_SELECTOR, 'button[data-v-55a04e1a][id="btnCollapse"]')
            button_resources.click()

            wait = WebDriverWait(self.driver, 10)
            arrecadacao_div = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[h4[text()="Arrecadação por Estado"]]'))
            )

            download_button = arrecadacao_div.find_element(By.ID, 'btnDownloadUrl')
            download_button.click()

            wait.until(lambda driver: any(fname.endswith('.csv') for fname in os.listdir(self.download_dir)))
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if self.driver:
                self.driver.quit()


