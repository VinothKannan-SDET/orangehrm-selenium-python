from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class NationalitiesPage(BasePage):
    """
    Page Object for Admin > Nationalities page.

    Handles actions related to adding, editing, searching,
    verifying, and managing nationalities.
    """

    def __init__(self, driver):
        """
        Initialise NationalitiesPage with the WebDriver
        and all locators required for the Nationalities module.
        """
        super().__init__(driver)
        self.driver = driver
        self.unique_name = ""

        # ── Nationality Form / Navigation Locators ──
        self.national_add_btn = (By.XPATH,
            "//button[@type='button' and normalize-space()='Add']")

        self.national_name = (By.XPATH,
            "//label[text()='Name']/following::input[contains(@class,'oxd-input')]")

        self.nationality_save_btn = (By.XPATH,
            "//button[@type='submit']")

        # ── Success / Search Result Locators ──
        self.confirm_nationality_creation = (By.XPATH,
            "//*[contains(@class,'oxd-toast')]")

        self.location_search_result = (By.XPATH,
            "//span[normalize-space()='(1) Record Found']")

        self.no_record_found = (By.XPATH,
            "//span[normalize-space()='No Records Found']")

        # ── Nationality Table Locators ──
        self.search_header_column = (By.XPATH,
            "//div[@class='oxd-table-header']/div/div")

        self.search_nationality_table = (By.XPATH,
            "//div[@class='oxd-table-card']")

        # ── Pagination Locator ──
        self.right_arrow = (By.XPATH,
            "//button[contains(@class,'pagination-page')]/i[contains(@class,'right')]")

        # ── Form Loader Locator ──
        self.loader = (By.CLASS_NAME,"oxd-form-loader")

    # ── Navigation / Page Helpers ──

    def get_current_page_url(self):
        """
        Return the current page URL.

        :return: Current browser URL
        """
        # Step 1: Get the current page URL
        logger.info("Getting current Nationalities page URL")
        return self.get_current_url()

    # ── Add Nationality ──

    def click_national_add_btn(self):
        """
        Click the Add button on the Nationalities page
        to open the nationality creation form.
        """
        # Step 1: Click the Add button
        logger.info("Clicking Add button on Nationalities page")
        self.click(self.national_add_btn)

    def enter_national_details(self, nationality):
        """
        Enter the nationality name into the Name input field.

        :param nationality: Nationality name to enter
        """
        # Step 1: Wait for the form loader to disappear
        self.wait_for_form_loader_to_disappear(
            (By.CSS_SELECTOR, ".oxd-loading-spinner-container")
        )

        # Step 2: Verify that the nationality name field is visible
        self.is_visible(self.national_name)

        # Step 3: Enter the nationality name
        logger.info(f"Entering nationality name: {nationality}")
        self.enter_text(
            self.national_name,
            nationality
        )

    def create_national_save_btn(self):
        """
        Click the Save button to submit the nationality form.

        Used for both Add and Edit nationality scenarios.
        """
        # Step 1: Click the Save button
        logger.info("Clicking Save button to submit nationality form")
        self.click(self.nationality_save_btn)

    # ── Success / Validation ──

    def is_nationality_creation_success(self):
        """
        Verify that the success toast message is displayed
        after creating or editing a nationality.

        :return: True if success toast is visible, otherwise False
        """
        # Step 1: Verify that the success toast is displayed
        logger.info("Verifying nationality success toast message")
        return self.is_visible(self.confirm_nationality_creation)

    # ── Search / Table Helpers ──

    def click_save_or_search_btn(self, btn_name):
        """
        Click a Save or Search submit button by its visible name.

        :param btn_name: Button name such as 'Save' or 'Search'
        """
        # Step 1: Wait for the form loader to disappear
        self.wait_for_form_loader_to_disappear(self.loader)

        # Step 2: Locate and click the requested button
        logger.info(f"Clicking '{btn_name}' button")
        self.click(
            (
                By.XPATH,
                f"//button[@type='submit' and normalize-space()='{btn_name}']"
            )
        )

    def get_searched_location(self, index):
        """
        Return the nationality value from the specified table column.

        :param index: Table column index
        :return: Nationality text from the first matching row
        """
        # Step 1: Locate the nationality table cell
        logger.info(f"Getting nationality value from table column: {index}")

        # Step 2: Return the cell text
        return self.get_text(
            (
                By.XPATH,
                f"//div[@class='oxd-table-card']/div/div[{index}]/div"
            )
        )

    def get_nationality_column_value(self, column_index):
        """
        Get the value from a specified column in the nationality table.

        :param column_index: Table column index
        :return: First column value if available, otherwise None
        """
        # Step 1: Get all nationality table rows
        user_table = self.is_all_presence(self.search_nationality_table)

        values = []

        # Step 2: Read the requested column value from each row
        for role in user_table:
            value = role.find_element(By.XPATH,f"div/div[{str(column_index)}]/div").text
            values.append(value)

        # Step 3: Return the first value if available
        logger.info(f"Retrieved {len(values)} nationality column values")

        return values[0] if values else None

    def get_nationality_list(self, national_index):
        """
        Return a list of all nationality names displayed
        in the current table page.

        :param national_index: Table column index containing nationality
        :return: List of nationality names
        """
        national_list = []

        # Step 1: Locate all nationality cells in the specified column
        national_title_row = self.driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'oxd-table-row')]"
            f"/div[{national_index}]/div"
        )

        # Step 2: Collect nationality names from each row
        for national_title in national_title_row:
            national_list.append(national_title.text)

        logger.info(
            f"Total nationalities found on current page: "
            f"{len(national_list)}"
        )

        # Step 3: Return the nationality list
        return national_list

    # ── Nationality Verification / Pagination ──

    def is_nationality_present(self, national_header_index, national_name):
        """
        Search all available nationality table pages and verify
        whether the specified nationality exists.

        :param national_header_index: Column index containing nationality name
        :param national_name: Nationality name to search for
        :return: Matching nationality name if found, otherwise None
        """
        national_xpath = (
            By.XPATH,
            f"//div[@class='oxd-table-card']"
            f"/div/div[{national_header_index}]/div"
        )

        # Step 1: Continue searching until the nationality is found
        # or there are no more pagination pages.
        while True:

            # Step 2: Get all nationality elements from the current page
            logger.info(f"Checking current page for nationality: {national_name}")

            national_list = self.is_all_presence(national_xpath)

            # Step 3: Compare each nationality with the expected name
            for national in national_list:
                if national.text == national_name:
                    logger.info(f"Nationality '{national_name}' found in table")
                    return national.text

            # Step 4: If the next-page arrow is available,
            # move to the next page and continue searching.
            if self.is_element_visible(self.right_arrow):
                logger.info("Nationality not found on current page. Moving to next page.")
                self.click(self.right_arrow)

            else:
                # Step 5: No more pages are available
                logger.warning(f"Nationality '{national_name}' not found in any table page")
                return None

    # ── Edit Nationality ──

    def edit_nationality(self, national_name):
        """
        Click the Edit icon for the specified nationality
        and generate the expected updated nationality name.

        :param national_name: Existing nationality name to edit
        :return: Expected updated nationality name
        """
        # Step 1: Locate the edit button for the specified nationality row
        logger.info(f"Editing nationality: {national_name}")

        national_edit = self.driver.find_element(
            By.XPATH,
            f"//div[contains(@class,'oxd-table-row')]"
            f"[.//div[normalize-space()='{national_name}']]"
            f"//button[.//i[contains(@class,'bi-pencil-fill')]]"
        )

        # Step 2: Wait until the Edit button is clickable
        self.wait_for_element_clickable(national_edit)

        # Step 3: Click the Edit button
        national_edit.click()

        # Step 4: Wait for the edit form to become visible
        self.is_visible(self.national_name)

        # Step 5: Generate a random suffix for the edited nationality
        random_num = self.get_random_number(2, 999)
        edited_national_name = national_name + random_num

        # Step 6: Enter the updated nationality value
        self.enter_national_details(random_num)

        logger.info(f"Updated nationality name will be: {edited_national_name}")

        # Step 7: Return the expected updated nationality name
        return edited_national_name