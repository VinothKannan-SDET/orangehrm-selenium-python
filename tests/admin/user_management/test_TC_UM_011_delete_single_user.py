import pytest


@pytest.mark.smoke
def test_TC_UM_011_delete_single_user(logged_in_admin, add_user_page, config, test_data):
    """
    Verify that an existing user can be deleted successfully
    and the deleted user is no longer available in the search results.
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

    # Step 5: Identify the Username column index
    username_index = add_user_page.get_search_header_index(test_data["username_header"])

    # Step 6: Verify that the correct username is displayed
    error_name_list = add_user_page.get_searched_username(username_index, existing_username)

    assert len(error_name_list) == 0, \
        f"Expected username '{existing_username}' " \
        f"but found incorrect usernames: {error_name_list}"

    # Step 7: Delete the selected user
    add_user_page.delete_single_user(existing_username)

    # Step 8: Navigate back to User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 9: Search for the deleted username
    add_user_page.search_user(existing_username)

    # Step 10: Verify that the deleted user is no longer present
    assert "No Records Found" in add_user_page.get_no_record_count(), \
        f"Expected No Records Found after deleting user '{existing_username}'"