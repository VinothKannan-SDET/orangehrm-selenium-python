import pytest


@pytest.mark.smoke
def test_TC_UM_012_delete_multiple_users(logged_in_admin, add_user_page, config, test_data):
    """
    Verify that multiple existing users can be deleted successfully
    and each deleted user is no longer available in the search results.
    """

    # Step 1: Initialize the list of users selected for deletion
    delete_user_list = []
    count = 0

    # Step 2: Navigate to Admin > User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 3: Collect unique existing usernames for deletion
    # excluding the default Admin user
    while count < test_data["user_deletion_count"]:
        existing_username = add_user_page.get_existing_user()

        if (
                existing_username not in delete_user_list
                and existing_username != "Admin"
        ):
            delete_user_list.append(existing_username)

        # Refresh the user list before selecting the next user
        add_user_page.click_search_btn()

        count += 1

    # Step 4: Identify the Username column index
    username_index = add_user_page.get_search_header_index(test_data["username_header"])

    # Step 5: Delete each selected user one by one
    for username in delete_user_list:
        # Step 6: Navigate back to User Management > Users page
        add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
        add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

        # Step 7: Search for the user to be deleted
        add_user_page.search_user(username)

        # Step 8: Verify that exactly one matching user record is found
        assert "(1) Record Found" in add_user_page.get_record_count(), \
            f"Expected (1) Record Found for user '{username}'"

        # Step 9: Verify that the correct username is displayed
        error_name_list = add_user_page.get_searched_username(username_index, username)

        assert len(error_name_list) == 0, \
            f"Expected username '{username}' " \
            f"but found incorrect usernames: {error_name_list}"

        # Step 10: Delete the selected user
        add_user_page.delete_single_user(username)

        # Step 11: Navigate back to User Management > Users page
        add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
        add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

        # Step 12: Search for the deleted user
        add_user_page.search_user(username)

        # Step 13: Verify that the deleted user is no longer present
        assert "No Records Found" in add_user_page.get_no_record_count(), \
            f"Expected No Records Found after deleting user '{username}'"