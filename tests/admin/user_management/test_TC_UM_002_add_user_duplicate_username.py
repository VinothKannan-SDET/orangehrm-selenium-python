import pytest

@pytest.mark.smoke
def test_TC_UM_002_add_user_duplicate_username(logged_in, logged_in_admin, add_user_page, config, test_data):
    add_user_page.navigate_to_add_user()
    existing_username = add_user_page.get_existing_user()

    add_user_page.navigate_to_add_user()
    add_user_page.add_user(test_data, existing_username)
    add_user_page.click_save_btn()
    assert add_user_page.is_duplicate_username_error_shown(), "Expected duplicate username error message"