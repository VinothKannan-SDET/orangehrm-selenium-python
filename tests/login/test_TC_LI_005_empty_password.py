import pytest


@pytest.mark.smoke
def test_TC_LI_005_empty_password(login_page, config, test_data):
    """
    Verify that the Password field displays a Required validation error
    when the password is left empty.
    """

    # Step 1: Open the login page and submit with an empty password
    login_page.login(config.base_url, config.username, test_data["invalid_password"])

    # Step 2: Verify that the Password field displays the Required error
    assert login_page.is_empty_credentials_error_shown(test_data["field_name"]) == "Required", \
        "Expected Required field error for empty password"