import pytest

@pytest.mark.smoke
def test_TC_LI_002_invalid_username(login_page, config, test_data):
    login_page.login(config.base_url, test_data["invalid_username"], config.password)
    assert login_page.is_invalid_credentials_error_shown(), \
        "Expected 'Invalid credentials' error for wrong username — error not shown"