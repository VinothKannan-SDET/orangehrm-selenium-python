import pytest


@pytest.mark.smoke
def test_TC_UM_004_add_user_password_mismatch(logged_in_admin, add_user_page, config, test_data):
    """
    Verify that a password mismatch validation error is displayed
    when the Password and Confirm Password fields contain different values.
    """

    # Step 1: Navigate to Admin > User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Enter valid user details
    add_user_page.add_user(test_data)

    # Step 3: Modify the password to create a mismatch
    add_user_page.password_mismatch(test_data)

    # Step 4: Click Save button to submit the form
    add_user_page.click_save_btn()

    # Step 5: Verify that the password mismatch validation error is displayed
    assert add_user_page.get_password_mismatch_error(), \
        "Expected 'Passwords do not match' validation message"