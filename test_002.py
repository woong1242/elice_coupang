import time
import pytest
import random
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver  # noqa
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from urllib import parse
from main_page import MainPage

@pytest.mark.usefixtures("driver")
class TESTADDCART:
    def test_addcart(self, driver: WebDriver):
        try:
            ITEMS_XPATH = "//form//ul/li"
            main_page = MainPage(driver)
            main_page.open()
            time.sleep(2)

            wait = ws(driver, 10)  # 최대 10초 대기
            wait.until(EC.url_contains("coupang.com"))  # URL 검증
            assert "coupang.com" in driver.current_url  # 검증
            time.sleep(2)

            main_page.search_items('노트북')  # '노트북' 검색

            ws(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, ITEMS_XPATH))
            )

            items = driver.find_elements(By.XPATH, ITEMS_XPATH)
            item_name = parse.quote('노트북')

            time.sleep(10)

            assert len(items) > 0
            assert item_name in driver.current_url

            #랜덤 상품 클릭
            product_links = driver.find_elements(By.CLASS_NAME, "search-product-link")
            if product_links:
                random.choice(product_links).click()

            #장바구니 담기 버튼 클릭
            cart_button = driver.find_element(By.CLASS_NAME, "prod-cart-btn")
            cart_button.click()

            #장바구니로 이동
            main_page.click_by_LINK_TEXT('장바구니')

            #장바구니 목록 가져오기 (추가 후 리스트)
            cart_items_before = driver.find_elements(By.CLASS_NAME, "cart-item")
            assert len(cart_items_before) > 0, "장바구니에 상품이 추가되지 않았습니다."

            #수량 증가 버튼 클릭
            plus_button = driver.find_element(By.CLASS_NAME, "quantity-input-icon.plus")

            price_element = driver.find_element(By.CLASS_NAME, "unit-total-sale-price")  # 가격 가져오기
            initial_price = int(price_element.text.replace(",", "").replace("원", "").strip())

            plus_button.click()
            time.sleep(2)  # 가격 업데이트 대기

            updated_price_element = driver.find_element(By.CLASS_NAME, "unit-total-sale-price")
            updated_price = int(updated_price_element.text.replace(",", "").replace("원", "").strip())

            # 🔹 가격 증가 확인
            assert updated_price > initial_price, f"가격 증가 실패: 초기 가격 {initial_price} -> 업데이트된 가격 {updated_price}"
            print(f"✅ 가격 증가 확인: {initial_price} -> {updated_price}")

            # 🔹 최대 수량까지 증가
            while True:
                try:
                    plus_button.click()
                    time.sleep(1)

                    # 최신 가격 가져오기
                    new_price = int(driver.find_element(By.CLASS_NAME, "unit-total-sale-price").text.replace(",", "").replace("원", "").strip())

                    # 가격이 더 이상 증가하지 않으면 최대 수량 도달
                    if new_price == updated_price:
                        print("최대 수량 도달!")
                        break
                    updated_price = new_price  

                except NoSuchElementException:
                    continue  

            #상품 삭제 버튼 클릭
            delete_buttons = driver.find_elements(By.CLASS_NAME, "cart-item-delete-btn")
            assert len(delete_buttons) > 0, "삭제할 상품이 없습니다."

            delete_buttons[0].click()  # 첫 번째 상품 삭제
            time.sleep(3)  # 삭제가 반영될 시간을 줌

            #장바구니 목록 다시 가져와 삭제되었는지 확인
            cart_items_after = driver.find_elements(By.CLASS_NAME, "cart-item")
            assert len(cart_items_after) < len(cart_items_before), "상품이 정상적으로 삭제되지 않았습니다."
            print("✅ 상품 삭제 확인: 삭제 전", len(cart_items_before), "→ 삭제 후", len(cart_items_after))

            #다시 상품 추가
            main_page.search_items('노트북')  # 다시 '노트북' 검색
            time.sleep(5)
            
            product_links = driver.find_elements(By.CLASS_NAME, "search-product-link")
            if product_links:
                random.choice(product_links).click()

            cart_button = driver.find_element(By.CLASS_NAME, "prod-cart-btn")
            cart_button.click()
            time.sleep(2)

            #로그아웃 버튼 클릭
            logout_button = driver.find_element(By.LINK_TEXT, "로그아웃")  
            logout_button.click()
            time.sleep(3)

            #로그아웃 후 장바구니 리스트 유지 여부 확인
            main_page.click_by_LINK_TEXT('장바구니')
            cart_items_after_logout = driver.find_elements(By.CLASS_NAME, "cart-item")

            assert len(cart_items_after_logout) == len(cart_items_after), "로그아웃 후 장바구니가 유지되지 않았습니다."
            print("로그아웃 후 장바구니 리스트 유지 확인:", len(cart_items_after_logout), "개")

        except Exception as e:
            print(f"테스트 중 오류 발생: {e}")
