import random
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.logger import get_logger
from selenium.common.exceptions import (NoSuchElementException, StaleElementReferenceException,
    ElementClickInterceptedException)
logger = get_logger(__name__)


class BasePage:
    """
    Base Page Object containing common Selenium actions and
    reusable utilities shared across all OrangeHRM page objects.
    """

    def __init__(self, driver):
        """
        Initialise BasePage with the WebDriver and configure
        the explicit wait used by common page actions.

        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

        # ── Common Navigation Locators ──
        self.top_menu_bar = (By.XPATH,"//nav[@role='navigation' and @aria-label='Topbar Menu']")

        self.nav_menu_bar = (By.XPATH,"./ul/li")

        self.top_menu_option = (By.XPATH,"span | a")

        self.search_result = (By.XPATH,"//span[normalize-space()='(1) Record Found']")

        self.form_loader = (By.CSS_SELECTOR,".oxd-form-loader")

        # ── table header Locators ──
        self.search_header_column = (By.XPATH, "//div[@class='oxd-table-header']/div/div")

        # ── Delete Confirmation Dialog Locators ──
        self.delete_msg_box = (By.XPATH,"//p[normalize-space()='Are you Sure?']")

        self.single_record_deletion = (By.XPATH,"//button[contains(normalize-space(),'Delete')]")
    # ── Navigation ──

    def admin_top_menu_navigation(self, top_menu_name):
        """
        Navigate to a top-level menu option from the Admin
        navigation menu.

        :param top_menu_name: Name of the top-level menu option
                             e.g. 'User Management', 'Job'
        """
        # Step 1: Locate the top navigation menu
        logger.info(f"Navigating to top menu: {top_menu_name}")

        top_menu = self.is_presence(self.top_menu_bar)

        # Step 2: Get all top-level menu items
        nav_top_menu_bar = top_menu.find_elements(*self.nav_menu_bar)

        # Step 3: Loop through menu items and find the requested option
        for top_menu_bar in nav_top_menu_bar:
            menu_name = top_menu_bar.find_element(*self.top_menu_option).text

            # Step 4: Click the matching menu option
            if menu_name.strip() == top_menu_name:
                logger.info(f"Clicking top menu option: {top_menu_name}")

                top_menu_bar.find_element(*self.top_menu_option).click()

                break

    def admin_top_submenu_navigation(self, submenu_name):
        """
        Navigate to a submenu option from the Admin menu.

        :param submenu_name: Name of the submenu option
        """
        # Step 1: Locate and click the requested submenu
        logger.info(f"Navigating to submenu: {submenu_name}")

        self.click((By.XPATH,f"//a[normalize-space()='{submenu_name}']"))

    def verify_job_title_dropdown(self, submenu_name):
        """
        Verify that the specified submenu option is visible.

        :param submenu_name: Name of the submenu option
        :return: True if the submenu is visible, otherwise False
        """
        # Step 1: Check whether the submenu option is visible
        logger.info(f"Verifying submenu is visible: {submenu_name}")

        return self.is_visible((By.XPATH,f"//a[normalize-space()='{submenu_name}']"))

    # ── Common Selenium Actions ──

    def click(self, locator):
        """
        Wait until an element is clickable and click it.

        :param locator: Selenium locator tuple
                       e.g. (By.ID, 'username')
        """
        # Step 1: Wait until the loader disappear
        # Wait for OrangeHRM form loader to disappear
        loader = (By.CSS_SELECTOR, ".oxd-form-loader")

        self.wait.until(EC.invisibility_of_element_located(loader))
        # Step 2: Wait until the element is clickable
        element = self.wait.until(EC.element_to_be_clickable(locator))

        # Step 3: Click the element
        element.click()

    def enter_text(self, locator, text):
        """
        Clear an input field and enter the specified text.

        :param locator: Selenium locator tuple
        :param text: Text to enter into the field
        """
        # Step 1: Wait until the input field is clickable
        element = self.wait.until(EC.element_to_be_clickable(locator))

        # Step 2: Clear the existing input
        element.clear()

        # Step 3: Enter the specified text
        element.send_keys(text)

    def clear_text(self, locator):
        """
        Clear all text from an input field using keyboard actions.

        :param locator: Selenium locator tuple
        """
        # Step 1: Wait until the input field is clickable
        element = self.wait.until(EC.element_to_be_clickable(locator))

        # Step 2: Click the input field
        element.click()

        # Step 3: Select all existing text
        element.send_keys(Keys.CONTROL,"a")

        # Step 4: Delete the selected text
        element.send_keys(Keys.BACKSPACE)

    def get_text(self, locator):
        """
        Get the visible text from an element.

        :param locator: Selenium locator tuple
        :return: Text content of the element
        """
        # Step 1: Wait until the element is visible
        element = self.wait.until(EC.visibility_of_element_located(locator))

        # Step 2: Return the element text
        return element.text

    # ── Element Wait / Verification ──

    def is_visible(self, locator):
        """
        Wait for an element to become visible and verify that
        it is displayed.

        :param locator: Selenium locator tuple
        :return: True if the element is displayed
        """
        # Step 1: Wait until the element is visible
        element = self.wait.until(EC.visibility_of_element_located(locator))

        # Step 2: Return the visibility status
        return element.is_displayed()

    def is_presence(self, locator):
        """
        Wait for an element to be present in the DOM.

        :param locator: Selenium locator tuple
        :return: Located WebElement
        """
        # Step 1: Wait until the element is present in the DOM
        return self.wait.until(EC.presence_of_element_located(locator))

    def is_all_presence(self, locator):
        """
        Wait for all matching elements to be present in the DOM.

        :param locator: Selenium locator tuple
        :return: List of located WebElements
        """
        # Step 1: Wait until all matching elements are present
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def wait_for_url(self, url_part):
        """
        Wait until the current URL contains the specified text.

        :param url_part: URL fragment to wait for
        :return: True when the URL contains the expected text
        """
        # Step 1: Wait until the expected URL fragment is present
        logger.info(f"Waiting for URL to contain: {url_part}")

        return self.wait.until(EC.url_contains(url_part))

    def wait_for_element_clickable(self, locator):
        """
        Wait until the specified element becomes clickable.

        :param locator: Selenium locator tuple
        :return: Clickable WebElement
        """
        # Step 1: Wait for the element to become clickable
        return self.wait.until(EC.element_to_be_clickable(locator))

    def get_current_url(self):
        """
        Return the current browser URL.

        :return: Current browser URL
        """
        # Step 1: Get the current URL from the browser
        return self.driver.current_url

    def wait_for_form_loader_to_disappear(self, locator, timeout=40):
        """
        Wait until the specified form loader disappears.
        """

        WebDriverWait(self.driver,timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def click_after_form_loader(self, locator, timeout=40):
        """
        Wait for the form loader to disappear and click the element.
        Retries if the loader temporarily intercepts the click.
        """

        def click_when_ready(driver):
            try:
                # Check loader
                try:
                    loader = driver.find_element(*self.form_loader)

                    if loader.is_displayed():
                        return False
                except (NoSuchElementException,StaleElementReferenceException):
                    pass

                # Find target element
                element = driver.find_element(*locator)

                if not element.is_displayed() or not element.is_enabled():
                    return False

                element.click()
                return True

            except (
                    ElementClickInterceptedException,
                    StaleElementReferenceException,
                    NoSuchElementException
            ):
                return False

        WebDriverWait(self.driver,timeout,poll_frequency=0.2).until(click_when_ready)

    # ── Random Data Utilities ──

    @staticmethod
    def get_random_number(start_num, end_num):
        """
        Generate a random number within the specified range
        and return it as a string.

        :param start_num: Minimum random number
        :param end_num: Maximum random number
        :return: Random number as a string
        """
        # Step 1: Generate a random number
        random_number = random.randint(start_num,end_num)

        # Step 2: Convert the number to string
        return str(random_number)

    # ── Table Helpers ──

    def get_search_header_index(self, column_header):
        """
        Find the column index by matching the table header text.

        :param column_header: Table header name to search for
        :return: Column index if found, otherwise 0
        """
        loop_incr = 0
        return_index = 0

        # Step 1: Get all table header elements
        header_column = self.is_all_presence(self.search_header_column)

        # Step 2: Loop through headers and find the matching column
        for header in header_column:
            loop_incr += 1

            if header.text == column_header:
                return_index = loop_incr

                logger.info(f"Column '{column_header}' found at index {return_index}")

                break

        # Step 3: Log a warning if the column was not found
        if return_index == 0:
            logger.warning(f"Column '{column_header}' not found in table")

        # Step 4: Return the column index
        return return_index

    def get_no_record_count(self):
        """
        Return the 'No Records Found' message text.

        :return: No-record message text
        """
        # Step 1: Define the No Records Found locator
        no_record_found = (By.XPATH,"//span[normalize-space()='No Records Found']")

        # Step 2: Get the message text
        message = self.get_text(no_record_found)

        # Step 3: Log and return the message
        logger.info(message)
        return message

    def get_record_count(self):
        """
        Return the record count message displayed after a search.

        :return: Record count message text
        """
        # Step 1: Get the record count message
        record_message = self.get_text(self.search_result)

        # Step 2: Log and return the result
        logger.info(record_message)
        return record_message

    # ── Dropdown Helpers ──

    def click_dropdown_option(self, field_name, option_value):
        """
        Click a labelled dropdown and select an option by text.

        :param field_name: Label of the dropdown field
        :param option_value: Option value to select
        """
        # Step 1: Create a dynamic locator for the dropdown
        dropdown = (
            By.XPATH,
            f"//label[normalize-space()='{field_name}']"
            f"/ancestor::div[contains(@class,'oxd-input-group')]"
            f"//div[contains(@class,'oxd-select-text')]"
        )

        # Step 2: Open the dropdown
        logger.info(f"Opening '{field_name}' dropdown")

        self.click(dropdown)

        # Step 3: Create a dynamic locator for the option
        option = (
            By.XPATH,
            f"//div[contains(@class,'oxd-select-option')]"
            f"//span[normalize-space()='{option_value}']"
        )

        # Step 4: Select the requested option
        logger.info(f"Selecting '{option_value}' from '{field_name}' dropdown")

        self.click(option)

    # ── Form Helpers ──

    def enter_field_input(self, field_name, input_value):
        """
        Enter text into a form field identified by its label.

        :param field_name: Form field label
        :param input_value: Value to enter
        """
        # Step 1: Create a dynamic locator based on the field label
        field_locator = (
            By.XPATH,
            f"//label[normalize-space()='{field_name}']"
            f"/following::input[1]"
        )

        # Step 2: Enter the supplied value
        logger.info(f"Entering value into field: {field_name}")

        self.enter_text(field_locator, input_value)

    # ── Delete Helpers ──

    def confirm_deletion(self):
        """
        Confirm deletion using the Delete confirmation dialog.
        """
        # Step 1: Define the delete confirmation message locator
        delete_msg_box = (By.XPATH, "//p[normalize-space()='Are you Sure?']")

        # Step 2: Define the Delete confirmation button locator
        single_deletion_btn = (By.XPATH, "//button[contains(normalize-space(),'Delete')]")

        # Step 3: Verify the confirmation dialog is displayed
        logger.info("Verifying delete confirmation dialog")

        self.is_visible(delete_msg_box)

        # Step 4: Click the Delete button
        logger.info("Confirming record deletion")

        self.click(single_deletion_btn)

    # ── Existing Record Helpers ──

    def get_existing_record(self, column_index):
        """
        Select a random existing record from the current table
        and return the text from the specified column.

        :param column_index: Table column index to retrieve
        :return: Text of the selected existing record
        """
        # Step 1: Get all available table rows
        search_locator = self.is_all_presence((By.XPATH,"//div[@class='oxd-table-body']/div"))

        # Step 2: Generate a random row index
        random_index = self.get_random_number(1,len(search_locator))

        # Step 3: Get the value from the requested column
        text = self.get_text(
            (
                By.XPATH,
                f"(//div[@class='oxd-table-card'])"
                f"[{random_index}]/div/div[{column_index}]/div"
            )
        )

        # Step 4: Log the selected record
        logger.info(f"Selected existing record: {text}")

        # Step 5: Return the selected record
        return text

    def is_element_visible(self, locator):
        """
        Check whether an element is currently visible without waiting.

        :param locator: Selenium locator
        :return: True if visible, otherwise False
        """
        try:
            return self.driver.find_element(*locator).is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    def get_field_validation_error(self, field_name):
        """
        Get the validation error message for a form field.

        :param field_name: Form field label name
        :return: Validation error message text
        """
        logger.info(f"Checking validation error for field: {field_name}")

        error_locator = (
            By.XPATH,
            f"//label[normalize-space()='{field_name}']"
            f"/following::span[contains(@class,'error')][1]"
        )

        return self.get_text(error_locator)

    def delete_record(self, index, deletion_name):
        """Delete a location by matching its name."""

        name_list = (By.XPATH,f"//div[@class='oxd-table-card']/div/div[{index}]/div")

        name_presence = self.is_all_presence(name_list)

        for name in name_presence:
            if name.text.strip() == deletion_name.strip():
                # Find the delete button within the same table row
                delete_button = name.find_element(
                    By.XPATH,
                    "./ancestor::div[contains(@class,'oxd-table-row')]"
                    "//div[contains(@class,'oxd-table-cell-actions')]"
                    "//button[i[contains(@class,'bi-trash')]]"
                )

                delete_button.click()
                break

        # Verify confirmation dialog
        self.is_visible(self.delete_msg_box)

        # Confirm deletion
        self.click(self.single_record_deletion)