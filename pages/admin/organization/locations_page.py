from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class LocationPage(BasePage):
    """
    Page Object for Admin > Locations page.

    Handles actions related to adding, searching, and
    verifying locations.
    """

    def __init__(self, driver):
        """
        Initialise LocationPage with the WebDriver
        and all locators required for the Locations module.
        """
        super().__init__(driver)
        self.driver = driver
        self.unique_name = ""

        # ── Location Form / Navigation Locators ──
        self.location_add_btn = (By.XPATH,
            "//button[@type='button' and normalize-space()='Add']")

        # ── Success / Search Result Locators ──
        self.confirm_location_creation = (By.XPATH,
            "//*[contains(@class,'oxd-toast')]")

        self.location_search_result = (By.XPATH,
            "//span[normalize-space()='(1) Record Found']")

        self.no_record_found = (By.XPATH,
            "//span[normalize-space()='No Records Found']")

        # ── Location Table Locators ──
        self.search_header_column = (By.XPATH,
            "//div[@class='oxd-table-header']/div/div")

        # ── Delete Confirmation Dialog Locators ──
        self.user_delete_msg_box = (By.XPATH,
            "//p[normalize-space()='Are you Sure?']")

        self.single_user_deletion = (By.XPATH,
            "//button[contains(normalize-space(),'Delete')]")

    # ── Navigation / Page Helpers ──

    def get_current_page_url(self):
        """
        Return the current page URL.

        :return: Current browser URL
        """
        # Step 1: Get the current page URL
        logger.info("Getting current Locations page URL")
        return self.get_current_url()

    # ── Add Location ──

    def click_location_add_btn(self):
        """
        Click the Add button on the Locations page
        to open the location creation form.
        """
        # Step 1: Click the Add button
        logger.info("Clicking Add button on Locations page")
        self.click(self.location_add_btn)

    # ── Success / Validation ──

    def is_location_creation_success(self):
        """
        Verify that the success toast message is displayed
        after creating or editing a location.

        :return: True if success toast is visible, otherwise False
        """
        # Step 1: Verify that the success toast is displayed
        logger.info("Verifying location success toast message")
        return self.is_visible(self.confirm_location_creation)

    def is_empty_location_error_shown(self, field_name):
        """
        Get the validation error message for a required field
        when the field is submitted empty.

        :param field_name: Form field label name
                           e.g. 'Name'
        :return: Validation error message text
        """
        # Step 1: Find the validation error associated with the field
        logger.info(f"Checking required field error for: {field_name}")

        return self.get_text(
            (
                By.XPATH,
                f"//label[normalize-space()='{field_name}']"
                f"/following::span[contains(@class,'error')]"
            )
        )

    # ── Search / Table Helpers ──

    def click_save_or_search_btn(self, btn_name):
        """
        Click a Save or Search submit button by its visible name.

        :param btn_name: Button name such as 'Save' or 'Search'
        """
        # Step 1: Locate and click the requested button
        logger.info(f"Clicking '{btn_name}' button")

        self.click(
            (
                By.XPATH,
                f"//button[@type='submit' and normalize-space()='{btn_name}']"
            )
        )

    def get_searched_location(self, index):
        """
        Return the location value from the specified table column.

        :param index: Table column index containing the location name
        :return: Location text from the first matching row
        """
        # Step 1: Locate the location value from the specified column
        logger.info(f"Getting location value from table column: {index}")

        # Step 2: Return the location text
        return self.get_text((By.XPATH,f"//div[@class='oxd-table-card']/div/div[{index}]/div"))