import pytest

@pytest.mark.smoke
def test_TC_LI_001_valid_login(login_page, config):
    login_page.login(config.base_url, config.username, config.password)
    assert login_page.is_home_page_loaded(), "Valid login failed — Dashboard not loaded"