from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class AdminPage(BasePage):
    """
    Page Object for the Admin module.

    Handles navigation to the Admin page and provides
    verification for the Admin page URL.
    """

    def __init__(self, driver):
        """
        Initialise AdminPage with the WebDriver
        and locators required for the Admin module.
        """
        super().__init__(driver)
        self.driver = driver

        # ── Admin Navigation Locators ──
        self.admin_link = (By.XPATH,"//span[normalize-space()='Admin']")

    # ── Navigation ──

    def navigate_to_admin(self):
        """
        Navigate to the Admin page from the main navigation menu.

        Waits for the Admin menu item to become visible,
        clicks it, and verifies that the Admin URL is loaded.
        """
        # Step 1: Verify that the Admin menu item is visible
        logger.info("Verifying Admin menu item is visible")
        self.is_visible(self.admin_link)

        # Step 2: Click the Admin menu item
        logger.info("Clicking Admin menu item")
        self.click(self.admin_link)

        # Step 3: Wait for the Admin page URL to load
        logger.info("Waiting for Admin page to load")
        self.wait_for_url("admin/viewSystemUsers")

    # ── Page Verification ──

    def is_admin_page_loaded(self):
        """
        Return the current page URL to verify that the Admin page
        has been loaded successfully.

        :return: Current browser URL
        """
        # Step 1: Get the current page URL
        current_url = self.get_current_url()

        # Step 2: Log the current URL
        logger.info(f"Current Admin page URL: {current_url}")

        # Step 3: Return the current URL
        return current_url