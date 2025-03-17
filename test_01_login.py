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
    def test_login(self, driver: WebDriver):
        try:
            main_page = MainPage(driver)
            main_page.open()
            time.sleep(2)

            wait = ws(driver, 10)  #최대 10초 기다림
            wait.until(EC.url_contains("coupang.com")) #url 검증
            assert "coupang.com" in driver.current_url # 검증
            time.sleep(2)   #봇 안들킬려고 일부러 2초 기다림

            main_page.click_by_LINK_TEXT('로그인')

            login_page = LoginPage(driver)
            time.sleep(2)

            login_page.input_password_email_click()
            time.sleep(5)
            driver.save_screenshot('로그인-성공.jpg')

        except Exception as e:
            print(f"테스트 중 오류 발생: {e}")