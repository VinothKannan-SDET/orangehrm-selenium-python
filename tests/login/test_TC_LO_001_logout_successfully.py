import pytest


@pytest.mark.smoke
def test_TC_LO_001_logout_successfully(logged_in, login_page, config):
    """
    Verify that a logged-in user can successfully log out
    and is redirected to the OrangeHRM login page.
    """

    # Step 1: Click the user profile dropdown and logout
    login_page.logout()

    # Step 2: Verify that the browser is redirected to the login URL
    assert "/auth/login" in login_page.get_current_url(), \
        "Expected login page after logout"

    # Step 3: Verify that the login form is displayed
    assert login_page.is_login_page_loaded(), \
        "Expected login form visible after logout"