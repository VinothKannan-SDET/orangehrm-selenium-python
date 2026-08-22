import pytest


@pytest.mark.smoke
def test_TC_UM_002_add_user_duplicate_username(logged_in_admin, add_user_page, config, test_data):
    """
    Verify that creating a user with an existing username
    displays the duplicate username validation error.
    """

    # Step 1: Navigate to Admin > User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Get an existing username from the user list
    existing_username = add_user_page.get_existing_user()

    # Step 3: Navigate back to User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 4: Enter user details using the existing username
    add_user_page.add_user(test_data, existing_username)

    # Step 5: Click Save button to submit the user form
    add_user_page.click_save_btn()

    # Step 6: Verify that the duplicate username validation error is displayed
    assert add_user_page.is_duplicate_username_error_shown(), \
        "Expected duplicate username error message"