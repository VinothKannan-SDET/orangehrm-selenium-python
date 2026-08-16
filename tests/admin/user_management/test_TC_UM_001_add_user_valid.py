import pytest

@pytest.mark.smoke
def test_TC_UM_001_add_user_valid(logged_in, logged_in_admin,add_user_page, config, test_data):
    add_user_page.navigate_to_add_user()
    add_user_page.add_user(test_data)
    add_user_page.click_save_btn()
    assert add_user_page.is_user_creation_success(), "Expected success message after creating valid user"
    admin_page.navigate_to_admin()
    add_user_page.search_user()
    assert "(1) Record Found" in add_user_page.get_record_count(), "Expected (1) Records Found message in Search after creating valid user"