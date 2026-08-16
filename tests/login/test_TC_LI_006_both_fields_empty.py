import pytest

@pytest.mark.smoke
def test_TC_LI_006_both_fields_empty(login_page, config, test_data):
    login_page.login(config.base_url, test_data["invalid_username"], test_data["invalid_password"])
    username_error = login_page.is_empty_credentials_error_shown(test_data["field_username"])
    password_error = login_page.is_empty_credentials_error_shown(test_data["field_password"])

    assert username_error == "Required" and password_error == "Required", \
        "Expected Required field errors for both empty fields"