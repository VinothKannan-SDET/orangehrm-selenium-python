from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utilities.logger import get_logger
logger = get_logger(__name__)

class AddUserPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.unique_name = ""
        self.top_menu_bar = (By.XPATH, "//nav[@role='navigation' and @aria-label='Topbar Menu']")
        self.nav_menu_bar = (By.XPATH, "./ul/li")
        self.top_menu_option = (By.XPATH, "span | a")
        self.user_link = (By.XPATH, "//a[normalize-space()='Users']")
        self.user_add_btn = (By.XPATH, "//button[normalize-space()='Add']")
        self.user_role_dropdown = (By.XPATH, "//label[normalize-space()='User Role']/following::div[contains(@class,'oxd-select-text')][1]")
        self.user_role_selection = (By.XPATH, "//div[contains(@class,'oxd-select-option')]//span[normalize-space()='Admin']")
        self.employee_name = (By.XPATH, "//input[@placeholder='Type for hints...']")
        self.status_dropdown = (By.XPATH, "//label[normalize-space()='Status']/following::div[contains(@class,'oxd-select-text')][1]")
        self.select_status = (By.XPATH, "//div[contains(@class,'oxd-select-option')]//span[normalize-space()='Enabled']")
        self.username = (By.XPATH, "//label[normalize-space()='Username']/../parent::div/div/input")
        self.password = (By.XPATH, "//label[normalize-space()='Password']/../parent::div/div/input")
        self.confirm_password = (By.XPATH,"//label[normalize-space()='Confirm Password']/../parent::div/div/input")
        self.create_user = (By.XPATH,"//div[contains(@class,'oxd-form-actions')]//button[normalize-space()='Save']")
        self.confirm_user_creation = (By.XPATH, "//*[contains(@class,'oxd-toast')]")
        self.user_search = (By.XPATH, "//label[text()='Username']/following::input[contains(@class,'input')]")
        self.search_btn = (By.XPATH, "//button[@type='submit']")
        self.user_search_result = (By.XPATH, "//span[normalize-space()='(1) Record Found']")
        self.no_record_found = (By.XPATH, "//span[normalize-space()='No Records Found']")
        self.user_already_exist = (By.XPATH, "//span[text()='Already exists']")
        self.existing_username = (By.XPATH, "(//div[@class='oxd-table-card'])[2]/div/div[2]/div")
        self.empty_fields_error = (By.XPATH, "//span[text()='Required']")
        self.password_not_match = (By.XPATH, "//span[normalize-space()='Passwords do not match']")
        self.search_first_row = (By.XPATH, "//div[@class='oxd-table-card']//div[@role='cell'][2]/div")
        self.search_admin_user = (By.XPATH, "//div[contains(@class,'oxd-select-option')]//span[normalize-space()='admin']")
        self.search_header_column = (By.XPATH, "//div[@class='oxd-table-header']/div/div")
        self.search_user_table = (By.XPATH,f"//div[@class='oxd-table-card']")
        #User edit xpath
        self.edit_btn = (By.CSS_SELECTOR, ".bi-pencil-fill")
        self.loader = (By.CSS_SELECTOR, ".oxd-form-loader")
        self.edit_user_role = (By.XPATH,
                        "(//label[normalize-space()='User Role']/ancestor::div[contains(@class,'oxd-input-group')]//div[contains(@class,'oxd-select-text')])[1]")
        # Delete User
        self.user_delete_msg_box = (By.XPATH, "//p[normalize-space()='Are you Sure?']")
        self.single_user_deletion = (By.XPATH, " //button[contains(normalize-space(),'Delete')]")


    def select_employee(self, employee_name):
        employee_locator = (By.XPATH, f"//*[normalize-space()='{employee_name}']")
        self.click(employee_locator)

    def navigate_to_add_user(self):
        # Admin Page Create new user
        logger.info("Navigating to User Management")
        top_menu = self.is_presence(self.top_menu_bar)
        nav_top_menu_bar = top_menu.find_elements(*self.nav_menu_bar)

        for top_menu_bar in nav_top_menu_bar:
            menu_name = top_menu_bar.find_element(*self.top_menu_option).text
            if menu_name.strip() == "User Management":
                top_menu_bar.find_element(*self.top_menu_option).click()
                break
        self.click(self.user_link)

    def add_user(self, test_data, existing_username=None):
        # Click new user add button
        self.click(self.user_add_btn)

        # Click User Role dropdown and select option
        if test_data["user_role"] != "":
            self.click(self.user_role_dropdown)
            self.click((By.XPATH,
                    f"//div[contains(@class,'oxd-select-option')]//span[normalize-space()='{test_data['user_role']}']"))

        # Enter employee name and select from dropdown list
        if test_data["employee_hint_name"] != "":
            self.enter_text(self.employee_name, test_data["employee_hint_name"][:3])
            self.select_employee(test_data["employee_hint_name"])

        # Click Status dropdown and select option
        if test_data["status"] != "":
            self.click(self.status_dropdown)
            self.click((By.XPATH,
                    f"//div[contains(@class,'oxd-select-option')]//span[normalize-space()='{test_data['status']}']"))

        # Enter Username
        if (test_data["scenario_type"].lower() == "positive"
                and test_data["username"] != ""):
            self.unique_name = test_data["username"] + self.get_random_number(1000, 9999)
        elif (test_data["scenario_type"].lower() == "negative"
              and test_data["username"] != ""):
            self.unique_name = existing_username
        self.enter_text(self.username, self.unique_name)

        # Enter password & confirm password
        if test_data["password"] != "":
            self.enter_text(self.password, test_data["password"])
            self.enter_text(self.confirm_password, test_data["password"])

    def click_save_btn(self):
        # Click Save button
        self.click(self.create_user)

    def password_mismatch(self, test_data):
        self.enter_text(self.password, test_data["password"]+"test")

    def is_user_creation_success(self):
        return self.is_visible(self.confirm_user_creation)

    def search_user(self, username=None):
        if username is None:
            username = self.unique_name
        self.enter_text(self.user_search, username)
        logger.info("Search Username input loaded")
        self.click_search_btn()

    def click_search_btn(self):
        self.wait_for_element_clickable(self.search_btn)
        self.click(self.search_btn)

    def search_user_with_role_base(self, test_data):
        # Click User Role dropdown and select option
        if test_data["user_role"] != "":
            self.click(self.user_role_dropdown)
            self.click((By.XPATH,
                        f"//div[contains(@class,'oxd-select-option')]//span[normalize-space()='{test_data['user_role']}']"))
        self.click_search_btn()

    def search_user_with_status_base(self, test_data):
        # Click Status dropdown and select option
        if test_data["status"] != "":
            self.click(self.status_dropdown)
            self.click((By.XPATH,
                        f"//div[contains(@class,'oxd-select-option')]//span[normalize-space()='{test_data['status']}']"))
        self.click_search_btn()

    def get_record_count(self):
        record_message = self.get_text(self.user_search_result)
        logger.info(record_message)
        return record_message

    def get_search_header_index(self, column_header):
        loop_incr = return_index = 0
        header_column = self.is_all_presence(self.search_header_column)
        for header in header_column:
            loop_incr +=1
            if header.text == column_header:
                return_index = loop_incr
                break
        return return_index

    def verify_search_user_list(self, username_index, column_index, expected_value):
        error_list = []
        user_table = self.is_all_presence(self.search_user_table)
        for role in user_table:
            value = role.find_element(By.XPATH, f"div/div[{str(column_index)}]/div").text
            if value != expected_value:
                error_list.append(role.find_element(By.XPATH, f"div/div[{str(username_index)}]/div").text)
        return error_list

    def get_searched_username(self, username_index, expected_value):
        error_list = []
        user_table = self.is_all_presence(self.search_user_table)
        for role in user_table:
            value = role.find_element(By.XPATH, f"div/div[{str(username_index)}]/div").text
            if value != expected_value:
                error_list.append(role.find_element(By.XPATH, f"div/div[{str(username_index)}]/div").text)
        return error_list

    def delete_single_user(self, username):
        self.is_presence((By.XPATH,
                          f"//div[text()='{username}']/following::div//i[contains(@class,'trash')]"))
        self.click((By.XPATH,
                          f"//div[text()='{username}']/following::div//i[contains(@class,'trash')]"))

        self.is_visible(self.user_delete_msg_box)
        self.click(self.single_user_deletion)

    def get_user_column_value(self, column_index):
        user_table = self.is_all_presence(self.search_user_table)
        values = []
        for role in user_table:
            value = role.find_element(By.XPATH, f"div/div[{str(column_index)}]/div").text
            values.append(value)
        return values[0] if values else None

    def verify_user_exact_search(self):
        return self.get_text(self.search_first_row)

    def get_existing_user(self):
        search_locator = self.is_all_presence((By.XPATH, "//div[@class='oxd-table-body']/div"))
        logger.info(len(search_locator))
        self.unique_name = self.get_random_number(1, len(search_locator))
        searched_text = self.get_text((By.XPATH,
                       f"(//div[@class='oxd-table-card'])[{self.unique_name}]/div/div[2]/div"))
        logger.info(f"Searching User Name: {searched_text}")
        return searched_text

    def is_duplicate_username_error_shown(self):
        return self.is_visible(self.user_already_exist)

    def get_empty_user_fields(self, test_data):
        empty_fields = []

        if test_data["user_role"] == "":
            empty_fields.append("User Role")

        if test_data["employee_hint_name"] == "":
            empty_fields.append("Employee Name")

        if test_data["status"] == "":
            empty_fields.append("Status")

        if test_data["username"] == "":
            empty_fields.append("Username")

        if test_data["password"] == "":
            empty_fields.append("Password")

        return empty_fields

    def get_validation_errors(self):
        error_list = []
        self.is_all_presence(self.empty_fields_error)
        error_fields = self.driver.find_elements(*self.empty_fields_error)
        logger.info(len(error_fields))
        for field in error_fields:
            empty_field_name = field.find_element(By.XPATH, "ancestor::div[contains(@class,'oxd-input-group')]/div/label").text
            error_list.append(empty_field_name)
        logger.info(f"Actual error list :{error_list}")
        return error_list

    def get_password_mismatch_error(self):
        return self.is_visible(self.password_not_match)

    def click_edit_btn(self):
        self.click(self.edit_btn)

    def edit_user_data(self, column_name, change_value):
        # Click User Role dropdown and select option
        self.wait_for_form_loader_to_disappear(self.loader)
        if change_value != "":
            if column_name == "User Role":
                self.click(self.user_role_dropdown)
            elif column_name == "Status":
                self.click(self.status_dropdown)
            self.click((By.XPATH,
                        f"//div[contains(@class,'oxd-select-option')]//span[normalize-space()='{change_value}']"))

    def get_no_record_count(self):
        record_message = self.get_text(self.no_record_found)
        logger.info(record_message)
        return record_message














