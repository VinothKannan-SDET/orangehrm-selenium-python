import pytest


@pytest.mark.smoke
def test_TC_LI_006_both_fields_empty(login_page, config, test_data):
    """
    Verify that both Username and Password fields display Required
    validation errors when both fields are left empty.
    """

    # Step 1: Open the login page and submit with both fields empty
    login_page.login(config.base_url, test_data["invalid_username"], test_data["invalid_password"])

    # Step 2: Capture the validation error displayed for the Username field
    username_error = login_page.is_empty_credentials_error_shown(test_data["field_username"])

    # Step 3: Capture the validation error displayed for the Password field
    password_error = login_page.is_empty_credentials_error_shown(test_data["field_password"])

    # Step 4: Verify that both fields display the Required validation error
    assert username_error == "Required" and password_error == "Required", \
        "Expected Required field errors for both empty fields"