import pytest
from pages.admin.admin_page import AdminPage
from pages.admin.user_management.add_user_page import AddUserPage
from pages.login.login_page import LoginPage
from utilities.config_reader import ConfigReader
from utilities.driver_factory import create_driver
import os
from utilities.test_data_reader import TestDataReader


def pytest_addoption(parser):
    parser.addoption("--browser", action="store",
                     default="Firefox", help="Browser to run tests: firefox or chrome")
@pytest.fixture(scope="session")
def config():
    return ConfigReader()

@pytest.fixture(scope="function")
def browser_Instance(request):
    browser = request.config.getoption("--browser")
    driver = create_driver(browser)
    yield driver
    driver.quit()

@pytest.fixture
def logged_in(login_page, config):
    login_page.login(config.base_url, config.username, config.password)
    assert login_page.is_home_page_loaded(), "Login failed — Dashboard not loaded"
    return login_page

@pytest.fixture
def logged_in_admin(logged_in, admin_page):
    admin_page.navigate_to_admin()
    assert "/admin/viewSystemUsers" in admin_page.is_admin_page_loaded(), "Admin page not loaded"
    return admin_page

@pytest.fixture
def login_page(browser_Instance):
    return LoginPage(browser_Instance)

@pytest.fixture
def admin_page(browser_Instance):
    return AdminPage(browser_Instance)

@pytest.fixture
def add_user_page(browser_Instance):
    return AddUserPage(browser_Instance)

@pytest.fixture
def test_data(request):
    return TestDataReader.read_test_data(request.node.fspath)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("browser_Instance")
        if driver:
            os.makedirs("reports/screenshots", exist_ok=True)
            screenshot_path = (
                f"reports/screenshots/{item.name}.png"
            )
            try:
                driver.save_screenshot(screenshot_path)
            except Exception as e:
                print(f"Unable to capture screenshot: {e}")
