import xlwings as xw  # type: ignore
import pyautogui  # type: ignore
import time
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support.ui import Select  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.common.exceptions import ElementClickInterceptedException  # type: ignore
from datetime import datetime

class Sidom():
    def __init__(self) -> None:
        self.url = "https://app.sidom.io/index.php/acceso"
        self.username = ""
        self.password = ""


    def get_credential(self, username, password) -> bool:
        if username != "" and password != "":
            self.username = username
            self.password = password
            return True
        else:
            return False

    def connection(self):
        driver = webdriver.Chrome()
        driver.get(self.url)
        time.sleep(2)

        try:
            login_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "user")))
            login_field.send_keys(self.username)

            password_field = driver.find_element(By.NAME, "pass")
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)

        except Exception as e:
            print(f"Erro ao fazer login: {str(e)}")
            driver.quit()

        try:
            WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.TAG_NAME, "select")))
        except Exception as e:
            print(f"Erro ao aguardar a resolução do CAPTCHA: {e}")
            driver.quit()
