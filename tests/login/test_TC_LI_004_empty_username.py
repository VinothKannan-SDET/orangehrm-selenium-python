import pytest

@pytest.mark.smoke
def test_TC_LI_004_empty_username(login_page, config, test_data):
    login_page.login(config.base_url, test_data["invalid_username"], config.password)
    assert login_page.is_empty_credentials_error_shown(test_data["field_name"]) == "Required", \
        "Expected Required field error for empty username"