import os

import allure
import pytest
from pages.admin.admin_page import AdminPage
from pages.admin.job.add_job_page import AddJobPage
from pages.admin.nationalities.nationalities_page import NationalitiesPage
from pages.admin.organization.locations_page import LocationPage
from pages.admin.user_management.add_user_page import AddUserPage
from pages.login.login_page import LoginPage
from utilities.config_reader import ConfigReader
from utilities.driver_factory import create_driver
from utilities.test_data_reader import TestDataReader



def pytest_addoption(parser):
    """
    Add custom command-line options for pytest.

    Adds the --browser option to allow the test execution browser
    to be selected from the command line.

    Example:
        pytest --browser firefox
        pytest --browser chrome

    :param parser: Pytest command-line argument parser.
    """

    # Step 1: Register the --browser command-line option
    parser.addoption(
        "--browser",
        action="store",
        default="Firefox",
        help="Browser to run tests: firefox or chrome"
    )


# ── Configuration Fixture ──

@pytest.fixture(scope="session")
def config():
    """
    Provide application configuration for the test session.

    Creates a single ConfigReader instance and reuses it across
    all tests in the session.

    :return: ConfigReader instance.
    """

    # Step 1: Load and return application configuration
    return ConfigReader()


# ── Browser / WebDriver Fixture ──

@pytest.fixture(scope="function")
def browser_Instance(request):
    """
    Create and manage a Selenium WebDriver instance for each test.

    A new browser instance is created before every test and closed
    after the test completes.

    :param request: Pytest request object used to read the browser option.
    :yield: Selenium WebDriver instance.
    """

    # Step 1: Read the browser name from pytest command-line option
    browser = request.config.getoption("--browser")

    # Step 2: Create the requested browser WebDriver
    driver = create_driver(browser)

    # Step 3: Provide the driver to the test
    yield driver

    # Step 4: Close the browser after test execution
    driver.quit()


# ── Login Fixtures ──

@pytest.fixture
def logged_in(login_page, config):
    """
    Log in to OrangeHRM using valid credentials.

    Verifies that the Dashboard page is loaded successfully
    before returning control to the test.

    :return: LoginPage instance after successful login.
    """

    # Step 1: Login using configured application credentials
    login_page.login(
        config.base_url,
        config.username,
        config.password
    )

    # Step 2: Verify that the Dashboard page is loaded
    assert login_page.is_home_page_loaded(), \
        "Login failed — Dashboard not loaded"

    # Step 3: Return the logged-in LoginPage instance
    return login_page


@pytest.fixture
def logged_in_admin(logged_in, admin_page):
    """
    Log in to OrangeHRM and navigate to the Admin page.

    Depends on the logged_in fixture to ensure the user is
    authenticated before navigating to Admin.

    :return: AdminPage instance with Admin page loaded.
    """

    # Step 1: Navigate to the Admin page
    admin_page.navigate_to_admin()

    # Step 2: Verify that the Admin page is loaded
    assert "/admin/viewSystemUsers" in admin_page.is_admin_page_loaded(), \
        "Admin page not loaded"

    # Step 3: Return the AdminPage instance
    return admin_page


# ── Page Object Fixtures ──

@pytest.fixture
def login_page(browser_Instance):
    """
    Provide LoginPage page object with the active WebDriver.

    :param browser_Instance: Active Selenium WebDriver.
    :return: LoginPage instance.
    """

    # Step 1: Create and return LoginPage object
    return LoginPage(browser_Instance)


@pytest.fixture
def admin_page(browser_Instance):
    """
    Provide AdminPage page object with the active WebDriver.

    :param browser_Instance: Active Selenium WebDriver.
    :return: AdminPage instance.
    """

    # Step 1: Create and return AdminPage object
    return AdminPage(browser_Instance)


@pytest.fixture
def add_user_page(browser_Instance):
    """
    Provide AddUserPage page object with the active WebDriver.

    :param browser_Instance: Active Selenium WebDriver.
    :return: AddUserPage instance.
    """

    # Step 1: Create and return AddUserPage object
    return AddUserPage(browser_Instance)


@pytest.fixture
def add_job_page(browser_Instance):
    """
    Provide AddJobPage page object with the active WebDriver.

    :param browser_Instance: Active Selenium WebDriver.
    :return: AddJobPage instance.
    """

    # Step 1: Create and return AddJobPage object
    return AddJobPage(browser_Instance)


@pytest.fixture
def locations_page(browser_Instance):
    """
    Provide LocationPage page object with the active WebDriver.

    :param browser_Instance: Active Selenium WebDriver.
    :return: LocationPage instance.
    """

    # Step 1: Create and return LocationPage object
    return LocationPage(browser_Instance)


@pytest.fixture
def nationalities_page(browser_Instance):
    """
    Provide NationalitiesPage page object with the active WebDriver.

    :param browser_Instance: Active Selenium WebDriver.
    :return: NationalitiesPage instance.
    """

    # Step 1: Create and return NationalitiesPage object
    return NationalitiesPage(browser_Instance)


# ── Test Data Fixture ──

@pytest.fixture
def test_data(request):
    """
    Load test data associated with the current pytest test file.

    Uses the current test file path to automatically locate
    and load the corresponding JSON test-data file.

    :param request: Pytest request object containing the test file path.
    :return: Dictionary containing test data from the JSON file.
    """

    # Step 1: Get the current pytest test file path
    test_file_path = request.node.fspath

    # Step 2: Load and return corresponding JSON test data
    return TestDataReader.read_test_data(test_file_path)


# ── Failure Screenshot Hook ──

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture a screenshot automatically when a test fails.

    Screenshots are captured only during the test call phase
    and stored under reports/screenshots.

    :param item: Pytest test item currently being executed.
    :param call: Pytest call information.
    """

    # Step 1: Execute the original pytest test report process
    outcome = yield

    # Step 2: Retrieve the test execution report
    report = outcome.get_result()

    # Step 3: Capture screenshots only when the test itself fails
    if report.when == "call" and report.failed:

        # Step 4: Get the WebDriver instance used by the test
        driver = item.funcargs.get("browser_Instance")

        if driver:

            # Step 5: Create screenshot directory if it does not exist
            os.makedirs(
                "reports/screenshots",
                exist_ok=True
            )

            # Step 6: Build screenshot file path using test name
            screenshot_path = (
                f"reports/screenshots/{item.name}.png"
            )

            try:
                # Step 7: Capture screenshot of the failed test
                driver.save_screenshot(screenshot_path)

                # step 8: Attach the screenshot to the allure report
                allure.attach.file(
                    screenshot_path,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception as e:
                # Step 9: Report screenshot capture failure
                print(
                    f"Unable to capture screenshot: {e}"
                )