import pytest

@pytest.mark.smoke
def test_TC_LO_001_logout_successfully(logged_in, login_page,config):
    login_page.logout()
    assert "/auth/login" in login_page.get_current_url(),"Expected login page after logout"
    assert login_page.is_login_page_loaded(), "Expected login form visible after logout"