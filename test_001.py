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
    def test_login(self, driver:WebDriver ):
        try:
            ITEMS_XPATH = "//form//ul/li"
            main_page = MainPage(driver)
            main_page.open()
            time.sleep(2)

            wait = ws(driver, 10)
            wait.until(EC.url_contains("coupang.com"))
            assert "coupang.com" in driver.current_url
            time.sleep(2)

            main_page.search_items('노트북')

            ws(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ITEMS_XPATH))
            )

            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            item_name = parse.quote('노트북')

            assert len(items) > 0
            assert item_name in driver.current_url

            driver.save_screenshot('메인페이지-비로그인-검색-성공.jpg')
            time.sleep(2)

            main_page.click_by_LINK_TEXT('로그인')
            wait.until(EC.url_contains("https://login.coupang.com"))
            assert "login" in driver.current_url

            login_page = LoginPage(driver)
            time.sleep(2)
            login_page.input_password_and_email(wait)
            time.sleep(10)
            login_page.click_login_button(wait)

            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            assert len(items) > 0
            assert item_name in driver.current_url

            driver.save_screenshot('메인페이지-로그인-검색-성공.jpg')

        except Exception as e:
            print(f"테스트 중 오류 발생: {e}")