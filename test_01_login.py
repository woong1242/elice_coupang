import time

import pytest
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver # noqa
from selenium.common.exceptions import NoSuchElementException , TimeoutException
from main_page import MainPage
from selenium.webdriver.common.by import By
from urllib import parse
from login_page import LoginPage

@pytest.mark.usefixtures("driver")
class TestMainPage:
    def test_open_main_page(self, driver: WebDriver):
        try:
            login_page = LoginPage(driver)
            login_page.open()

            time.sleep(2)

            wait = ws(driver, 10) #최대 10초까지 기다림
            wait.until(EC.url_contains("https://login.coupang.com")) #URL 검증
            assert "login" in driver.current_url #검증 

            login_page.input_password_and_email(wait)
            login_page.click_login_button(wait)

            wait.until(EC.url_contains("https://coupang.com")) #URL 검증

            time.sleep(10)


        except NoSuchElementException as e:
            assert False