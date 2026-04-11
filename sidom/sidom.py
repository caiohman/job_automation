import time
from selenium import webdriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.common.keys import Keys  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support.ui import Select  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from sidom.sidom_argentina import SidomArgentina

class Sidom():
    def __init__(self, username, password) -> None:
        self.url = "https://app.sidom.io/index.php/acceso"
        self.username = username
        self.password = password

        self.country = None
        self.process = None

    def get_cases(self, country, process):
        self.country = country
        self.process = process

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
            print(e)
            driver.quit()

        try:
            select_country = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "select"))))
            argentina = SidomArgentina() # create selection to choose the country
            select_country.select_by_value(value = argentina.get_sidom_argentina_code())
            submit_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
            submit_button.click()
            popover_close = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "wt-btn-back"))
            )
            popover_close.click()
        except Exception as e:
            print(e)
            driver.quit()
