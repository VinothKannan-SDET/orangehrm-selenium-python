import pytest

@pytest.mark.smoke
def test_TC_UM_004_add_user_password_mismatch(logged_in_admin,
                                              add_user_page, config, test_data):
    add_user_page.navigate_to_add_user()
    add_user_page.add_user(test_data)
    add_user_page.password_mismatch(test_data)
    add_user_page.click_save_btn()
    assert add_user_page.get_password_mismatch_error(), "Expected Password do not match message"