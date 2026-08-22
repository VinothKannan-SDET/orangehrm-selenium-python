import pytest


@pytest.mark.sanity
def test_TC_UM_007_search_user_by_role_ess(logged_in_admin, add_user_page, config, test_data):
    """
    Verify that User Management search returns only users
    assigned to the ESS role.
    """

    # Step 1: Navigate to Admin > User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Search users using the configured ESS role
    add_user_page.search_user_with_role_base(test_data)

    # Step 3: Identify Username and User Role column indexes
    username_index = add_user_page.get_search_header_index(test_data["username_header"])
    user_role_index = add_user_page.get_search_header_index(test_data["user_role_header"])

    # Step 4: Verify that every returned user has the expected ESS role
    error_list = add_user_page.verify_search_user_list(username_index, user_role_index,
        test_data["user_role_not"])

    # Step 5: Verify that no users with an incorrect role are displayed
    assert len(error_list) == 0, \
        f"Users not assigned to ESS role: {error_list}"