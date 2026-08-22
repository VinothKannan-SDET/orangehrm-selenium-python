import pytest


@pytest.mark.smoke
def test_TC_UM_009_edit_user_change_role(logged_in_admin, add_user_page, admin_page, config, test_data):
    """
    Verify that an existing user's User Role can be changed
    successfully and the updated role is reflected in the search results.
    """

    # Step 1: Navigate to Admin > User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Select an existing username from the user list
    existing_username = add_user_page.get_existing_user()

    # Step 3: Search for the selected user
    add_user_page.search_user(existing_username)

    # Step 4: Verify that exactly one user record is found
    assert "(1) Record Found" in add_user_page.get_record_count(), \
        "Expected (1) Record Found for the selected username"

    # Step 5: Identify Username and User Role column indexes
    username_index = add_user_page.get_search_header_index(test_data["username_header"])
    user_role_index = add_user_page.get_search_header_index(test_data["user_role_header"])

    # Step 6: Get the user's current role
    user_role_value_before = add_user_page.get_user_column_value(user_role_index)

    # Step 7: Open the Edit User form
    add_user_page.click_edit_btn()

    # Step 8: Change the user's role to the opposite role
    if user_role_value_before == "Admin":
        add_user_page.edit_user_data(test_data["user_role_header"],"ESS")
    else:
        add_user_page.edit_user_data(test_data["user_role_header"],"Admin")

    # Step 9: Submit the updated user details
    add_user_page.click_save_btn()

    # Step 10: Verify that the user creation success message is displayed
    assert add_user_page.is_user_creation_success(), \
        "Expected success message after creating valid user"

    # Step 11: Navigate back to Admin > User Management > Users page
    admin_page.navigate_to_admin()

    # Step 12: Navigate back to User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 13: Search for the updated user
    add_user_page.search_user(existing_username)

    # Step 14: Verify that exactly one updated user record is found
    assert "(1) Record Found" in add_user_page.get_record_count(), \
        "Expected (1) Record Found after updating user role"

    # Step 15: Verify that the user's role was updated successfully
    error_list = add_user_page.verify_search_user_list(username_index, user_role_index,
        user_role_value_before)

    # Step 16: Assert that no users have an incorrect role
    assert len(error_list) == 0, \
        f"User '{existing_username}' is in existing " \
        f"'{user_role_value_before}' role: {error_list}"