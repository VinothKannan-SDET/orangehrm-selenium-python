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

    def login(self, login_URL, login_username, login_password):
        self.driver.get(login_URL)
        self.enter_text(self.username, login_username)
        self.enter_text(self.password, login_password)
        self.click(self.login_btn)

    def is_home_page_loaded(self):
        return self.is_visible(self.dashboard_link)