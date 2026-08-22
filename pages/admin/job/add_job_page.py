from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class AddJobPage(BasePage):
    """
    Page Object for Admin > Job > Job Titles page.
    Handles all actions related to adding, editing,
    deleting and verifying job titles.
    """

    def __init__(self, driver):
        """
        Initialise AddJobPage with all locators
        for the Job Titles module.
        """
        super().__init__(driver)
        self.driver = driver

        # ── Job Title Form Locators ──
        self.job_title_link = (By.XPATH,"//a[normalize-space()='Job Titles']")

        self.job_title_add_button = (By.XPATH,
            "//button[@type='button' and contains(normalize-space(),'Add')]")

        self.job_title_name = (By.XPATH,
            "//label[text()='Job Title']/following::input[contains(@class,'oxd-input')]")

        self.job_title_save_btn = (By.XPATH,"//button[@type='submit']")

        # ── Job Title List Locators ──
        self.job_list_header_column = (By.XPATH,
            "//div[@class='oxd-table-header']//div[@role='columnheader']")

        # ── Toast / Success Message Locator ──
        self.confirm_job_creation = (By.XPATH,"//*[contains(@class,'oxd-toast')]")

        # ── Form Loader Locator ──
        self.loader = (By.CLASS_NAME,"oxd-form-loader")

        # ── Delete Confirmation Dialog Locators ──
        self.job_delete_msg_box = (By.XPATH,"//p[normalize-space()='Are you Sure?']")

        self.single_job_deletion = (By.XPATH,"//button[contains(normalize-space(),'Delete')]")

    # ── Navigation ──

    def navigate_to_add_title(self):
        """
        Navigate to Admin > Job > Job Titles page
        using the top navigation menu.
        """
        # Step 1: Click 'Job' from Admin top menu bar
        logger.info("Navigating to Admin > Job > Job Titles")
        self.admin_top_menu_navigation("Job")

        # Step 2: Click 'Job Titles' from the dropdown sub-menu
        self.click(self.job_title_link)

    # ── Add Job Title ──

    def job_title_add_btn(self):
        """
        Click the Add button on the Job Titles list page
        to open the new job title form.
        """
        # Step 1: Click the Add button to open the create form
        logger.info("Clicking Add button on Job Titles page")
        self.click(self.job_title_add_button)

    def enter_job_title_details(self, job_title):
        """
        Enter the job title name into the form input field.

        :param job_title: The job title text to enter
        """
        # Step 1: Wait for the form loader to disappear before interacting
        self.wait_for_form_loader_to_disappear(self.loader)

        # Step 2: Type the job title into the input field
        logger.info(f"Entering job title: {job_title}")
        self.enter_text(self.job_title_name, job_title)

    def clear_job_title_text(self):
        """
        Clear the existing text in the job title input field.
        Used during edit scenarios to remove old value before typing new one.
        """
        # Step 1: Wait for the form loader to disappear
        self.wait_for_form_loader_to_disappear(self.loader)

        # Step 2: Verify the job title field is visible
        self.is_visible(self.job_title_name)

        # Step 3: Clear all text from the input field
        logger.info("Clearing job title input field")
        self.clear_text(self.job_title_name)

    def create_job_save_btn(self):
        """
        Click the Save button to submit the job title form.
        Used for both Add and Edit scenarios.
        """
        # Step 1: Click the Save/Submit button
        logger.info("Clicking Save button to submit job title form")
        self.click(self.job_title_save_btn)

    # ── Verification Helpers ──

    def get_job_list_header_column(self, expected_column_name):
        """
        Find and return the column index number by matching
        the column header text in the Job Titles table.

        :param expected_column_name: Header text to search for
                                     e.g. 'Job Title'
        :return: Column index (int) if found, None if not found
        """
        loop_incr = 0

        # Step 1: Get all header column elements from the table
        header_column_name = self.is_all_presence(self.job_list_header_column)

        # Step 2: Loop through headers and match by text
        for column in header_column_name:
            loop_incr += 1
            if column.text == expected_column_name:
                logger.info(
                    f"Column '{expected_column_name}' "
                    f"found at index {loop_incr}")
                return loop_incr

        # Step 3: Return None if column header not found
        logger.warning(f"Column header '{expected_column_name}' not found in table")
        return None

    def verify_new_job_creation(self, job_title_index, job_title_name):
        """
        Verify that the given job title exists in the Job Titles table.

        :param job_title_index: Column index where job title text appears
        :param job_title_name: The job title text to search for
        :return: True if found in table, False otherwise
        """
        # Step 1: Get all rows from the job title column
        job_title_row = self.driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'oxd-table-row')]"
            f"/div[{job_title_index}]/div")

        # Step 2: Loop through rows and match job title text
        for job_title in job_title_row:
            if job_title.text == job_title_name:
                logger.info(f"Job title '{job_title_name}' found in list")
                return True

        # Step 3: Return False if not found in any row
        logger.warning(f"Job title '{job_title_name}' NOT found in list")
        return False

    def get_job_title_list(self, job_title_index):
        """
        Return a list of all job title names from the table.
        Used to pick a random existing job title for edit/delete scenarios.

        :param job_title_index: Column index where job title text appears
        :return: List of job title name strings
        """
        job_title_list = []

        # Step 1: Get all rows from the job title column
        job_title_row = self.driver.find_elements(
            By.XPATH,
            f"//div[contains(@class,'oxd-table-row')]"
            f"/div[{job_title_index}]/div")

        # Step 2: Collect each row's text into the list
        for job_title in job_title_row:
            job_title_list.append(job_title.text)

        logger.info(f"Total job titles found in list: {len(job_title_list)}")
        return job_title_list

    # ── Edit Job Title ──

    def edit_job_title(self, job_title_name):
        """
        Click the Edit (pencil) icon for the given job title
        and append a random number to create an updated name.

        :param job_title_name: Existing job title name to edit
        :return: The expected updated job title name after edit
        """
        # Step 1: Find the edit button for the specific job title row
        logger.info(f"Editing job title: {job_title_name}")
        job_title_edit = self.driver.find_element(
            By.XPATH,
            f"//div[contains(@class,'oxd-table-row')]"
            f"[.//div[normalize-space()='{job_title_name}']]"
            f"//button[.//i[contains(@class,'bi-pencil-fill')]]")

        # Step 2: Click the edit button to open the edit form
        job_title_edit.click()

        # Step 3: Generate random suffix for the updated title
        random_num = self.get_random_number(2, 999)
        edited_job_title_name = job_title_name + random_num

        # Step 4: Enter the updated job title in the form
        self.enter_job_title_details(random_num)

        logger.info(f"Updated job title name will be: {edited_job_title_name}")
        return edited_job_title_name

    # ── Delete Job Title ──

    def delete_job_title(self, job_title_name):
        """
        Click the Delete (trash) icon for the given job title
        and confirm deletion in the confirmation dialog.

        :param job_title_name: The job title name to delete
        """
        # Step 1: Find the delete button for the specific job title row
        logger.info(f"Deleting job title: {job_title_name}")
        job_title_delete = self.driver.find_element(
            By.XPATH,
            f"//div[contains(@class,'oxd-table-row')]"
            f"[.//div[normalize-space()='{job_title_name}']]"
            f"//button[.//i[contains(@class,'trash')]]")

        # Step 2: Click the delete icon to trigger confirmation dialog
        job_title_delete.click()

        # Step 3: Verify the confirmation dialog is visible
        self.is_visible(self.job_delete_msg_box)

        # Step 4: Click the Delete button to confirm deletion
        self.click(self.single_job_deletion)
        logger.info(f"Job title '{job_title_name}' deleted successfully")

    # ── Success and Error Assertions ──

    def is_job_creation_success(self):
        """
        Verify that the success toast message appears
        after adding or editing a job title.

        :return: True if success toast is visible
        """
        # Step 1: Wait for and verify the toast message is displayed
        logger.info("Verifying job title success toast message")
        return self.is_visible(self.confirm_job_creation)