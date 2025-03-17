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
            ITEMS_XPATH = "//form//ul/li"
            main_page = MainPage(driver)
            main_page.open()
            time.sleep(2)

            wait = ws(driver, 10)  #최대 10초 기다림
            wait.until(EC.url_contains("coupang.com")) #url 검증
            assert "coupang.com" in driver.current_url # 검증
            time.sleep(2)   

            main_page.search_items('노트북')   #노트북 검색

            ws(driver,10).until(
                EC.presence_of_element_located((By.XPATH, ITEMS_XPATH))
            )

            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            item_name = parse.quote('노트북')   

            time.sleep(10)

            assert len(items) > 0
            assert item_name in driver.current_url

            # 상위 10개 상품 출력
            top_items_loginX = items[:10]  # 상위 10개 아이템 가져오기  

            driver.save_screenshot('메인페이지-비로그인-검색-성공.jpg')
            time.sleep(2)


            main_page.click_by_LINK_TEXT('로그인')
            wait.until(EC.url_contains("https://login.coupang.com")) #URL 검증
            assert "login" in driver.current_url #검증 

            login_page = LoginPage(driver)
            time.sleep(2)
            login_page.input_password_and_email(wait)
            login_page.click_login_button(wait)
            time.sleep(10)

            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            item_name = parse.quote('노트북')   

            assert len(items) > 0
            assert item_name in driver.current_url

            # 상위 10개 상품 출력
            top_items_loginO = items[:10]  # 상위 10개 아이템 가져오기
            driver.save_screenshot('메인페이지-로그인-검색-성공.jpg')


            top_items_login_names = [item.text for item in top_items_loginO]
            top_items_loginx_names = [item.text for item in top_items_loginX]

            assert top_items_login_names == top_items_loginx_names, "로그인/비로그인 검색 결과가 다릅니다."





        except Exception as e:
            print(f"테스트 중 오류 발생: {e}")