import pytest

@pytest.mark.smoke
def test_TC_LI_005_empty_password(login_page, config, test_data):
    login_page.login(config.base_url, config.username, test_data["invalid_password"])
    assert login_page.is_empty_credentials_error_shown(test_data["field_name"]) == "Required", \
        "Expected Required field error for empty password"