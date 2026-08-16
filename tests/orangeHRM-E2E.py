import pytest

@pytest.mark.smoke
def test_e2e_scenario(login_page, admin_page, add_user_page, config, add_user_data):
    login_page.login(config.base_url,config.username, config.password)
    assert login_page.is_home_page_loaded(),"Login page was not loaded"

    admin_page.navigate_to_admin()
    assert "/admin/viewSystemUsers" in admin_page.is_admin_page_loaded(),"Admin page was not loaded"

    #Get existing username
    add_user_page.navigate_to_add_user()
    existing_username = add_user_page.get_existing_user()

    add_user_page.navigate_to_add_user()
    add_user_page.add_user(add_user_data["employee_Name"],add_user_data["employee_Hint_Name"],
                           add_user_data["password"], "negative", existing_username)
    assert add_user_page.is_duplicate_username_error_shown(), "Expected duplicate username error message"



