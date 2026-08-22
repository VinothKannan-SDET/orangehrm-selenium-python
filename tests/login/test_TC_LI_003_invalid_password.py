import pytest


@pytest.mark.smoke
def test_TC_LI_003_invalid_password(login_page, config, test_data):
    """
    Verify that login fails and an Invalid credentials error is displayed
    when an invalid password is provided.
    """

    # Step 1: Open the login page and enter an invalid password
    login_page.login(config.base_url, config.username, test_data["invalid_password"])

    # Step 2: Verify that the Invalid credentials error is displayed
    assert login_page.is_invalid_credentials_error_shown(), \
        "Expected 'Invalid credentials' error for wrong password — error not shown"