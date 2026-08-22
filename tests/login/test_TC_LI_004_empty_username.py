import pytest


@pytest.mark.smoke
def test_TC_LI_004_empty_username(login_page, config, test_data):
    """
    Verify that the Username field displays a Required validation error
    when the username is left empty.
    """

    # Step 1: Open the login page and submit with an empty username
    login_page.login(config.base_url, test_data["invalid_username"], config.password)

    # Step 2: Verify that the Username field displays the Required error
    assert login_page.is_empty_credentials_error_shown(test_data["field_name"]) == "Required", \
        "Expected Required field error for empty username"