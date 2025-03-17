from selenium.webdriver.chrome.webdriver import WebDriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as ws
from selenium.webdriver.support import expected_conditions as EC
import time




class LoginPage: 
  def __init__(self, driver: WebDriver):
        self.driver = driver

    
  def input_password_email_click(self):

        wait = ws(self.driver, 20)

        user_box = wait.until(EC.presence_of_element_located((By.ID, 'login-email-input')))
        user_box.send_keys("stw1232@naver.com")

        # 비밀번호 입력 필드 대기 후 입력
        password_box = wait.until(EC.presence_of_element_located((By.ID, 'login-password-input')))
        password_box.send_keys("qlalf1242@@")

        time.sleep(30)

        #로그인 버튼 클릭
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'login__button--submit')]"))).click()
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading-spinner")))

        
   