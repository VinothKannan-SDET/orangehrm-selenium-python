from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.username = (By.NAME, "username")
        self.password = (By.NAME, "password")
        self.login_btn = (By.CSS_SELECTOR, ".orangehrm-login-button")
        self.dashboard_link = (By.XPATH, "//span[normalize-space()='Dashboard']")
        self.invalid_credential = (By.XPATH, "//p[text()='Invalid credentials']")
        self.logout_dropdown = (By.CSS_SELECTOR, ".oxd-userdropdown-name")
        self.logout_btn = (By.XPATH, "//a[normalize-space()='Logout']")
        self.login_form = (By.CSS_SELECTOR, ".orangehrm-login-form")

    def login(self, login_URL, login_username, login_password):
        self.driver.get(login_URL)
        self.enter_text(self.username, login_username)
        self.enter_text(self.password, login_password)
        self.click(self.login_btn)

    def is_home_page_loaded(self):
        return self.is_visible(self.dashboard_link)

    def is_invalid_credentials_error_shown(self):
        return self.is_visible(self.invalid_credential)

    def is_empty_credentials_error_shown(self, field_name):
        return self.get_text((By.XPATH,
                       f"//label[normalize-space()='{field_name}']/following::span[contains(@class,'error')]"))

    def logout(self):
        self.click(self.logout_dropdown)
        self.click(self.logout_btn)

    def is_login_page_loaded(self):
        return self.is_visible(self.login_form)

