import pytest


@pytest.mark.smoke
def test_TC_UM_001_add_user_valid(logged_in_admin, add_user_page, admin_page, config, test_data):
    """
    Verify that a valid user can be created successfully
    and the newly created user can be found using the username search.
    """

    # Step 1: Navigate to Admin > User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Enter valid user details
    add_user_page.add_user(test_data)

    # Step 3: Click Save button to create the user
    add_user_page.click_save_btn()

    # Step 4: Verify that the user creation success message is displayed
    assert add_user_page.is_user_creation_success(), \
        "Expected success message after creating valid user"

    # Step 5: Navigate back to Admin > User Management > Users page
    admin_page.navigate_to_admin()

    # Step 6: Search for the newly created user by username
    add_user_page.search_user()

    # Step 7: Verify that exactly one matching user record is found
    assert "(1) Record Found" in add_user_page.get_record_count(), \
        "Expected (1) Record Found message after creating valid user"