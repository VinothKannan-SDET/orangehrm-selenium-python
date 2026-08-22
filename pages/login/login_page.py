from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """
    Page Object for the OrangeHRM Login page.

    Handles user login, logout, login page verification,
    dashboard verification, and login validation scenarios.
    """

    def __init__(self, driver):
        """
        Initialise LoginPage with the WebDriver
        and all locators required for the Login page.
        """
        super().__init__(driver)
        self.driver = driver

        # ── Login Form Locators ──
        self.username = (By.NAME,"username")

        self.password = (By.NAME,"password")

        self.login_btn = (By.CSS_SELECTOR,".orangehrm-login-button")

        self.login_form = (By.CSS_SELECTOR,".orangehrm-login-form")

        # ── Login Validation Locators ──
        self.invalid_credential = (By.XPATH,"//p[text()='Invalid credentials']")

        # ── Dashboard Locator ──
        self.dashboard_link = (By.XPATH,"//span[normalize-space()='Dashboard']")

        # ── Logout Locators ──
        self.logout_dropdown = (By.CSS_SELECTOR,".oxd-userdropdown-name")

        self.logout_btn = (By.XPATH,"//a[normalize-space()='Logout']")

    # ── Login ──

    def login(self, login_URL, login_username, login_password):
        """
        Login to OrangeHRM using the supplied credentials.

        :param login_URL: OrangeHRM login page URL
        :param login_username: Username to enter
        :param login_password: Password to enter
        """
        # Step 1: Navigate to the OrangeHRM login URL
        logger.info(f"Navigating to OrangeHRM login page: {login_URL}")
        self.driver.get(login_URL)

        # Step 2: Enter the username
        logger.info(f"Entering login username: {login_username}")
        self.enter_text(self.username,login_username)

        # Step 3: Enter the password
        logger.info("Entering login password")
        self.enter_text(self.password,login_password)

        # Step 4: Click the Login button
        logger.info("Clicking Login button")
        self.click(self.login_btn)

    # ── Page Verification ──

    def is_login_page_loaded(self):
        """
        Verify that the OrangeHRM Login page is displayed.

        :return: True if the login form is visible, otherwise False
        """
        # Step 1: Verify that the login form is visible
        logger.info("Verifying Login page is loaded")
        return self.is_visible(self.login_form)

    def is_home_page_loaded(self):
        """
        Verify that the OrangeHRM Dashboard page is displayed
        after successful login.

        :return: True if Dashboard is visible, otherwise False
        """
        # Step 1: Verify that the Dashboard link is visible
        logger.info("Verifying Dashboard page is loaded")
        return self.is_visible(self.dashboard_link)

    # ── Login Validation ──

    def is_invalid_credentials_error_shown(self):
        """
        Verify that the Invalid Credentials error message
        is displayed after an unsuccessful login attempt.

        :return: True if the error is visible, otherwise False
        """
        # Step 1: Verify the invalid credentials error message
        logger.info("Checking Invalid Credentials error message")
        return self.is_visible(self.invalid_credential)

    def is_empty_credentials_error_shown(self, field_name):
        """
        Get the validation error message displayed for an empty
        username or password field.

        :param field_name: Login field label name
                           e.g. 'Username' or 'Password'
        :return: Validation error message text
        """
        # Step 1: Locate the validation error for the specified field
        logger.info(f"Checking empty credential validation for: {field_name}")

        return self.get_text(
            (
                By.XPATH,
                f"//label[normalize-space()='{field_name}']"
                f"/following::span[contains(@class,'error')]"
            )
        )

    # ── Logout ──

    def logout(self):
        """
        Logout from OrangeHRM using the user profile dropdown.
        """
        # Step 1: Click the logged-in user's profile dropdown
        logger.info("Opening user profile dropdown")
        self.click(self.logout_dropdown)

        # Step 2: Click the Logout option
        logger.info("Clicking Logout")
        self.click(self.logout_btn)