import pytest


@pytest.mark.sanity
def test_TC_UM_008_search_user_by_status_enabled(logged_in_admin, add_user_page, config, test_data):
    """
    Verify that User Management search returns only users
    with the Enabled status.
    """

    # Step 1: Navigate to Admin > User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Search users using the configured status
    add_user_page.search_user_with_status_base(test_data)

    # Step 3: Identify Username and Status column indexes
    username_index = add_user_page.get_search_header_index(test_data["username_header"])
    status_index = add_user_page.get_search_header_index(test_data["status_header"])

    # Step 4: Verify that every returned user has the expected status
    error_list = add_user_page.verify_search_user_list(username_index, status_index,
        test_data["status_not_display"])

    # Step 5: Verify that no users with an incorrect status are displayed
    assert len(error_list) == 0, \
        f"Users not having '{test_data['status']}' status: {error_list}"