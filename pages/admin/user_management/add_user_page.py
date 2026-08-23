import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger

logger = get_logger(__name__)


class AddUserPage(BasePage):
    """
    Page Object for Admin > User Management > Users page.

    Handles actions related to adding, editing, searching,
    validating, and deleting users.
    """

    def __init__(self, driver):
        """
        Initialise AddUserPage with the WebDriver
        and all locators required for the User Management module.
        """
        super().__init__(driver)
        self.driver = driver
        self.unique_name = ""

        # ── User Navigation Locators ──
        self.user_link = (By.XPATH,"//a[normalize-space()='Users']")

        self.user_add_btn = (By.XPATH,"//button[normalize-space()='Add']")

        # ── User Form Locators ──
        self.user_role_dropdown = (By.XPATH,
            "//label[normalize-space()='User Role']"
            "/following::div[contains(@class,'oxd-select-text')][1]"
        )

        self.user_role_selection = (By.XPATH,
            "//div[contains(@class,'oxd-select-option')]"
            "//span[normalize-space()='Admin']"
        )

        self.employee_name = (By.XPATH,"//input[@placeholder='Type for hints...']")

        self.status_dropdown = (By.XPATH,
            "//label[normalize-space()='Status']"
            "/following::div[contains(@class,'oxd-select-text')][1]"
        )

        self.select_status = (By.XPATH,
            "//div[contains(@class,'oxd-select-option')]"
            "//span[normalize-space()='Enabled']"
        )

        self.username = (By.XPATH,
            "//label[normalize-space()='Username']"
            "/../parent::div/div/input"
        )

        self.password = (By.XPATH,
            "//label[normalize-space()='Password']"
            "/../parent::div/div/input"
        )

        self.confirm_password = (By.XPATH,
            "//label[normalize-space()='Confirm Password']"
            "/../parent::div/div/input"
        )

        self.create_user = (By.XPATH,
            "//div[contains(@class,'oxd-form-actions')]"
            "//button[normalize-space()='Save']"
        )

        # ── Success / Validation Locators ──
        self.confirm_user_creation = (By.XPATH,"//*[contains(@class,'oxd-toast')]")

        self.user_already_exist = (By.XPATH,"//span[text()='Already exists']")

        self.empty_fields_error = (By.XPATH,"//span[text()='Required']")

        self.password_not_match = (By.XPATH,
            "//span[normalize-space()='Passwords do not match']"
        )

        # ── User Search Locators ──
        self.user_search = (
            By.XPATH,
            "//label[text()='Username']"
            "/following::input[contains(@class,'input')]"
        )

        self.search_btn = (By.XPATH,"//div[contains(@class,'oxd-form-actions')]"
                                    "//button[normalize-space()='Search']")

        self.no_record_found = (By.XPATH,"//span[normalize-space()='No Records Found']")

        self.search_first_row = (By.XPATH,
            "//div[@class='oxd-table-card']//div[@role='cell'][2]/div")

        self.search_admin_user = (By.XPATH,
            "//div[contains(@class,'oxd-select-option')]//span[normalize-space()='admin']")

        # ── User Table Locators ──
        self.search_header_column = (By.XPATH,"//div[@class='oxd-table-header']/div/div")

        self.search_user_table = (By.XPATH,"//div[@class='oxd-table-card']")

        self.existing_username = (By.XPATH,"(//div[@class='oxd-table-card'])[2]/div/div[2]/div")

        # ── User Edit Locators ──
        self.edit_btn = (By.CSS_SELECTOR,".bi-pencil-fill")

        self.loader = (By.CSS_SELECTOR,".oxd-form-loader")

        self.edit_user_role = (By.XPATH,
            "(//label[normalize-space()='User Role']"
            "/ancestor::div[contains(@class,'oxd-input-group')]"
            "//div[contains(@class,'oxd-select-text')])[1]"
        )

        # ── Delete User Locators ──
        self.user_delete_msg_box = (By.XPATH,"//p[normalize-space()='Are you Sure?']")

        self.single_user_deletion = (By.XPATH,"//button[contains(normalize-space(),'Delete')]")

    # ── User Form Helpers ──
    @allure.step("Select the employee: {employee_name}")
    def select_employee(self, employee_name):
        """
        Select an employee from the employee suggestion dropdown.

        :param employee_name: Employee name to select
        """
        # Step 1: Create a dynamic locator for the employee name
        employee_locator = (By.XPATH,f"//*[normalize-space()='{employee_name}']")

        # Step 2: Select the employee from the suggestion list
        logger.info(f"Selecting employee: {employee_name}")
        self.click(employee_locator)

    # ── Navigation ──
    @allure.step("Navigate to the add user page")
    def navigate_to_add_user(self):
        """
        Navigate to Admin > User Management > Users page.
        """
        # Step 1: Navigate to User Management from the Admin menu
        logger.info("Navigating to User Management")
        self.admin_top_menu_navigation("User Management")

        # Step 2: Click Users from the User Management menu
        self.click(self.user_link)

    # ── Add User ──
    @allure.step("Add user: {existing_username}")
    def add_user(self, test_data, existing_username=None):
        """
        Enter user details into the Add User form.

        Supports both positive and negative scenarios.
        For positive scenarios, a random suffix is appended
        to the username to make it unique.

        For negative duplicate-user scenarios, an existing
        username is used.

        :param test_data: Test data dictionary containing user details
        :param existing_username: Existing username used for duplicate
                                  username negative scenarios
        """
        # Step 1: Click the Add button to open the user form
        logger.info("Clicking Add button to create a new user")
        self.click(self.user_add_btn)

        # Step 2: Select User Role when provided
        if test_data["user_role"] != "":
            logger.info(f"Selecting User Role: {test_data['user_role']}")

            self.click(self.user_role_dropdown)

            self.click(
                (By.XPATH,
                    f"//div[contains(@class,'oxd-select-option')]"
                    f"//span[normalize-space()='{test_data['user_role']}']"
                )
            )

        # Step 3: Enter Employee Name and select employee
        if test_data["employee_hint_name"] != "":
            logger.info(f"Entering employee name: {test_data['employee_hint_name']}")

            self.enter_text(self.employee_name,test_data["employee_hint_name"][:3])

            self.select_employee(test_data["employee_hint_name"])

        # Step 4: Select Status when provided
        if test_data["status"] != "":
            logger.info(f"Selecting Status: {test_data['status']}")

            self.click(self.status_dropdown)

            self.click(
                (
                    By.XPATH,
                    f"//div[contains(@class,'oxd-select-option')]"
                    f"//span[normalize-space()='{test_data['status']}']"
                )
            )

        # Step 5: Generate username based on scenario type
        if (test_data["scenario_type"].lower() == "positive"
            and test_data["username"] != ""):
            self.unique_name = (test_data["username"]
                + self.get_random_number(1000, 9999)
            )

        elif (test_data["scenario_type"].lower() == "negative"
            and test_data["username"] != ""):
            self.unique_name = existing_username

        # Step 6: Enter username
        if self.unique_name:
            logger.info(f"Entering username: {self.unique_name}")
            self.enter_text(self.username,self.unique_name)

        # Step 7: Enter password and confirm password
        if test_data["password"] != "":
            logger.info("Entering user password")

            self.enter_text(self.password,test_data["password"])

            self.enter_text(self.confirm_password,test_data["password"])

    @allure.step("Click save button in User page")
    def click_save_btn(self):
        """
        Click the Save button to submit the Add User form.
        """
        # Step 1: Click the Save button
        logger.info("Clicking Save button to create user")
        self.click(self.create_user)

    # ── Password Validation ──
    @allure.step("Enter mismatch password")
    def password_mismatch(self, test_data):
        """
        Enter a different confirmation password to trigger
        the password mismatch validation.

        :param test_data: Test data dictionary containing password
        """
        # Step 1: Enter an intentionally different password
        logger.info("Entering mismatched password for validation")
        self.enter_text(self.password,test_data["password"] + "test")

    @allure.step("Verify the password match")
    def get_password_mismatch_error(self):
        """
        Verify whether the password mismatch validation message
        is displayed.

        :return: True if mismatch error is visible, otherwise False
        """
        # Step 1: Verify the password mismatch error
        logger.info("Checking password mismatch validation")
        return self.is_visible(self.password_not_match)

    # ── Success Validation ──
    @allure.step("Verify the new user creation success message")
    def is_user_creation_success(self):
        """
        Verify that the success toast message is displayed
        after creating or editing a user.

        :return: True if success toast is visible, otherwise False
        """
        # Step 1: Verify the success toast message
        logger.info("Verifying user creation success message")
        return self.is_visible(self.confirm_user_creation)

    @allure.step("Verify the duplicate username error")
    def is_duplicate_username_error_shown(self):
        """
        Verify that the duplicate username validation message
        is displayed.

        :return: True if duplicate username error is visible,
                 otherwise False
        """
        # Step 1: Verify duplicate username validation
        logger.info("Checking duplicate username validation")
        return self.is_visible(self.user_already_exist)

    # ── User Search ──
    @allure.step("Search user: {username}")
    def search_user(self, username=None):
        """
        Search for a user by username.

        If username is not provided, the unique username generated
        during user creation is used.

        :param username: Username to search for
        """
        # Step 1: Use generated username when no username is provided
        if username is None:
            username = self.unique_name

        # Step 2: Enter username in the search field
        logger.info(f"Searching for username: {username}")
        self.enter_text(self.user_search,username)

        # Step 3: Click Search button
        self.click_search_btn()

    @allure.step("Click Search button in user page")
    def click_search_btn(self):
        """
        Click the Search button on the User Management page.
        """
        # Step 1: Wait until Search button becomes clickable
        self.wait_for_element_clickable(self.search_btn)

        # Step 2: Click Search button
        logger.info("Clicking Search button")
        self.click(self.search_btn)

    @allure.step("Search user with user role: {test_data['user_role']}")
    def search_user_with_role_base(self, test_data):
        """
        Search users based on the selected User Role.

        :param test_data: Test data dictionary containing user role
        """
        # Step 1: Select User Role when provided
        if test_data["user_role"] != "":
            logger.info(f"Searching users with role: {test_data['user_role']}")

            dropdowns = {
                "User Role": self.user_role_dropdown,
                "Status": self.status_dropdown
            }

            if test_data["user_role_header"] not in dropdowns:
                raise ValueError(f"Unsupported field: {test_data["user_role_header"]}")

            logger.info(f"Changing {test_data["user_role_header"]} to: {test_data['user_role']}")

            # Wait for any loader before opening dropdown
            self.click_after_form_loader(dropdowns[test_data["user_role_header"]])

            # Select requested dropdown value
            option_locator = (
                By.XPATH,
                f"//div[contains(@class,'oxd-select-option')]"
                f"//span[normalize-space()='{test_data['user_role']}']"
            )

            self.click(option_locator)

        # Step 2: Click Search button
        self.click_search_btn()

    @allure.step("Search user with user status: {test_data['status']}")
    def search_user_with_status_base(self, test_data):
        """
        Search users based on the selected Status.

        :param test_data: Test data dictionary containing status
        """
        # Step 1: Select Status when provided
        if test_data["status"] != "":
            logger.info(f"Searching users with status: {test_data['status']}")

            dropdowns = {
                "User Role": self.user_role_dropdown,
                "Status": self.status_dropdown
            }

            if test_data["status_header"] not in dropdowns:
                raise ValueError(f"Unsupported field: {test_data["status_header"]}")

            logger.info(f"Changing {test_data["status_header"]} to: {test_data['status']}")

            # Wait for any loader before opening dropdown
            self.click_after_form_loader(dropdowns[test_data["status_header"]])

            # Select requested dropdown value
            option_locator = (
                By.XPATH,
                f"//div[contains(@class,'oxd-select-option')]"
                f"//span[normalize-space()='{test_data['status']}']"
            )

            self.click(option_locator)

        # Step 2: Click Search button
        self.click_search_btn()

    # ── Search Results ──
    @allure.step("Get the first row user name")
    def verify_user_exact_search(self):
        """
        Return the username displayed in the first search result row.

        :return: Username from the first search result
        """
        # Step 1: Get username from the first search result
        logger.info("Getting first user from search results")
        return self.get_text(self.search_first_row)

    # ── Table Helpers ──
    @allure.step("Verify the expected user list displayed")
    def verify_search_user_list(self, username_index, column_index, forbidden_value):
        """
        Verify that no row in the search results contains the forbidden value
        in the specified column.

        Used to confirm that a role/status filter is working correctly —
        pass the value that should NOT appear in the results.

        Example: After searching by role 'Admin', pass forbidden_value='ESS'
        to confirm no ESS user leaked into the results.

        :param username_index: Column index containing the username (for error reporting)
        :param column_index:   Column index to validate against the forbidden value
        :param forbidden_value: The role/status value that must NOT appear in results
        :return: List of usernames where the forbidden value was found (should be empty)
        """
        error_list = []

        # Step 1: Get all user table rows
        user_table = self.is_all_presence(self.search_user_table)

        # Step 2: Check each row for the forbidden value
        for role in user_table:
            value = role.find_element(By.XPATH, f"div/div[{str(column_index)}]/div").text

            if value == forbidden_value:
                error_list.append(
                    role.find_element(By.XPATH, f"div/div[{str(username_index)}]/div").text
                )

        # Step 3: Return list of violating usernames (expected to be empty)
        logger.info(f"Users with forbidden value '{forbidden_value}': {len(error_list)}")
        return error_list

    @allure.step("Get searched username")
    def get_searched_username(self, username_index, expected_value):
        """
        Return usernames from search results whose value does not
        match the expected value.

        :param username_index: Column index containing username
        :param expected_value: Expected username value
        :return: List of usernames that do not match
        """
        error_list = []

        # Step 1: Get all user table rows
        user_table = self.is_all_presence(self.search_user_table)

        # Step 2: Compare username values against expected value
        for role in user_table:
            value = role.find_element(By.XPATH, f"div/div[{str(username_index)}]/div").text

            if value != expected_value:
                error_list.append(
                    role.find_element(By.XPATH, f"div/div[{str(username_index)}]/div").text
                )

        # Step 3: Return users that do not match
        return error_list

    @allure.step("Get user column value")
    def get_user_column_value(self, column_index):
        """
        Get the value from a specified column in the User table.

        :param column_index: User table column index
        :return: First column value if available, otherwise None
        """
        # Step 1: Get all user table rows
        user_table = self.is_all_presence(self.search_user_table)

        values = []

        # Step 2: Read the requested column from each row
        for role in user_table:
            value = role.find_element(By.XPATH, f"div/div[{str(column_index)}]/div").text

            values.append(value)

        # Step 3: Return the first value if available
        logger.info(f"Retrieved {len(values)} values from column {column_index}")

        return values[0] if values else None

    # ── Existing User ──
    @allure.step("Get existing username")
    def get_existing_user(self):
        """
        Select and return a random existing username from
        the User Management table.

        :return: Existing username selected from the table
        """
        # Step 1: Get all user rows currently displayed
        search_locator = self.is_all_presence((By.XPATH,"//div[@class='oxd-table-body']/div"))

        logger.info(f"Total users available for selection: {len(search_locator)}")

        # Step 2: Generate a random row index
        random_index = self.get_random_number(1, len(search_locator))

        # Step 3: Get the username from the selected row
        searched_text = self.get_text((By.XPATH,
                f"(//div[@class='oxd-table-card'])"
                f"[{random_index}]/div/div[2]/div"
            )
        )

        logger.info(f"Existing user selected for search: {searched_text}")

        # Step 4: Return the selected username
        return searched_text

    # ── Validation Helpers ──
    @allure.step("Get the user field has empty value")
    def get_empty_user_fields(self, test_data):
        """
        Return a list of user fields that are empty in the
        supplied test data.

        :param test_data: Test data dictionary containing user details
        :return: List of empty field names
        """
        empty_fields = []

        # Step 1: Check User Role
        if test_data["user_role"] == "":
            empty_fields.append("User Role")

        # Step 2: Check Employee Name
        if test_data["employee_hint_name"] == "":
            empty_fields.append("Employee Name")

        # Step 3: Check Status
        if test_data["status"] == "":
            empty_fields.append("Status")

        # Step 4: Check Username
        if test_data["username"] == "":
            empty_fields.append("Username")

        # Step 5: Check Password
        if test_data["password"] == "":
            empty_fields.append("Password")

        logger.info(f"Expected empty fields: {empty_fields}")

        # Step 6: Return the list of empty fields
        return empty_fields

    @allure.step("Capture the error message")
    def get_validation_errors(self):
        """
        Get the field names for which Required validation
        errors are displayed.

        :return: List of field names with validation errors
        """
        error_list = []

        # Step 1: Wait for required validation messages to be present
        self.is_all_presence(self.empty_fields_error)

        # Step 2: Get all Required validation elements
        error_fields = self.driver.find_elements(*self.empty_fields_error)

        logger.info(f"Total validation errors displayed: {len(error_fields)}")

        # Step 3: Identify the field associated with each error
        for field in error_fields:
            empty_field_name = field.find_element(
                By.XPATH,
                "ancestor::div[contains(@class,'oxd-input-group')]"
                "/div/label"
            ).text

            error_list.append(empty_field_name)

        # Step 4: Log and return the actual validation error list
        logger.info(f"Actual error list: {error_list}")

        return error_list

    # ── Delete User ──
    @allure.step("Delete the user: {username}")
    def delete_single_user(self, username):
        """
        Delete a specific user from the User Management table.

        :param username: Username of the user to delete
        """
        # Step 1: Locate the Delete icon for the specified username
        delete_locator = (
            By.XPATH,
            f"//div[text()='{username}']"
            f"/following::div//i[contains(@class,'trash')]"
        )

        # Step 2: Verify that the Delete icon is present
        logger.info(f"Locating Delete button for user: {username}")
        self.is_presence(delete_locator)

        # Step 3: Click the Delete icon
        self.click(delete_locator)

        # Step 4: Verify the Delete confirmation dialog
        self.is_visible(self.user_delete_msg_box)

        # Step 5: Confirm user deletion
        self.click(self.single_user_deletion)

        logger.info(f"User '{username}' deleted successfully")

    # ── Edit User ──
    @allure.step("Click edit button of user details")
    def click_edit_btn(self):
        """
        Click the Edit icon for a user from the search result.
        """
        # Step 1: Click the Edit icon
        logger.info("Clicking Edit button for user")
        self.click(self.edit_btn)

    @allure.step("Edit the user details")
    def edit_user_data(self, column_name, change_value):
        """
        Update the selected user field with a new value.

        Supported fields:
        - User Role
        - Status

        :param column_name: Name of the field to edit.
        :param change_value: New value to select
        """

        if not change_value:
            return

        dropdowns = {
            "User Role": self.user_role_dropdown,
            "Status": self.status_dropdown
        }

        if column_name not in dropdowns:
            raise ValueError(f"Unsupported field: {column_name}")

        logger.info(f"Changing {column_name} to: {change_value}")

        # Wait for any loader before opening dropdown
        self.click_after_form_loader(dropdowns[column_name])

        # Select requested dropdown value
        option_locator = (
            By.XPATH,
            f"//div[contains(@class,'oxd-select-option')]"
            f"//span[normalize-space()='{change_value}']"
        )

        self.click(option_locator)