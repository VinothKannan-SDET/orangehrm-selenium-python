import pytest


@pytest.mark.smoke
def test_TC_LI_001_valid_login(login_page, config):
    """
    Verify that the user can successfully log in with valid credentials
    and is redirected to the Dashboard page.
    """

    # Step 1: Open OrangeHRM login page and enter valid credentials
    login_page.login(config.base_url, config.username, config.password)

    # Step 2: Verify that the Dashboard page is displayed
    assert login_page.is_home_page_loaded(), \
        "Valid login failed — Dashboard not loaded"