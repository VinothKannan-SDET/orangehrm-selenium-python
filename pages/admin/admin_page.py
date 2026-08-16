from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AdminPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.admin_link = (By.XPATH, "//span[normalize-space()='Admin']")

    def navigate_to_admin(self):
        self.click(self.admin_link)
        self.wait_for_url("admin/viewSystemUsers")

    def is_admin_page_loaded(self):
        return self.get_current_url()


