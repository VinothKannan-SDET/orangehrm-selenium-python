import random
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator, text):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()

    def is_presence(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def is_all_presence(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_url(self, url_part):
        return self.wait.until(EC.url_contains(url_part))

    def wait_for_element_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def get_current_url(self):
        return self.driver.current_url

    @staticmethod
    def get_random_number(start_num, end_num):
        return str(random.randint(start_num, end_num))

    def wait_for_form_loader_to_disappear(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator))
