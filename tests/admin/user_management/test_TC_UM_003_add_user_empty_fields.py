import pytest
from utilities.logger import get_logger

logger = get_logger(__name__)


@pytest.mark.smoke
def test_TC_UM_003_add_user_empty_fields(logged_in_admin, add_user_page, config, test_data):
    """
    Verify that mandatory field validation messages are displayed
    when the required User fields are submitted empty.
    """

    # Step 1: Identify the fields expected to show validation errors
    expected_error_list = add_user_page.get_empty_user_fields(test_data)
    logger.info(f"Expected error list: {expected_error_list}")

    # Step 2: Navigate to Admin > User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 3: Submit the user form with the configured empty fields
    add_user_page.add_user(test_data)

    # Step 4: Click Save button to trigger mandatory field validation
    add_user_page.click_save_btn()

    # Step 5: Get the actual validation errors displayed on the form
    actual_error_list = add_user_page.get_validation_errors()

    # Step 6: Verify that the expected and actual validation errors match
    assert expected_error_list == actual_error_list, \
        f"Expected validation errors {expected_error_list}, " \
        f"but found {actual_error_list}"