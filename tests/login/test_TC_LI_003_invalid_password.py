import pytest

@pytest.mark.smoke
def test_TC_LI_003_invalid_password(login_page, config, test_data):
    login_page.login(config.base_url, config.username, test_data["invalid_password"])
    assert login_page.is_invalid_credentials_error_shown(), \
        "Expected 'Invalid credentials' error for wrong password — error not shown"