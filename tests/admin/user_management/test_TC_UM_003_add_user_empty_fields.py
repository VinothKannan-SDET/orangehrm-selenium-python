import pytest
from utilities.logger import get_logger
logger = get_logger(__name__)

@pytest.mark.smoke
def test_TC_UM_003_add_user_empty_fields(logged_in_admin, add_user_page, config, test_data):
    #Get empty user fields
    expected_error_list = add_user_page.get_empty_user_fields(test_data)
    logger.info(f"Expected error list :{expected_error_list}")

    add_user_page.navigate_to_add_user()
    add_user_page.add_user(test_data)
    add_user_page.click_save_btn()
    actual_error_list = add_user_page.get_validation_errors()
    assert expected_error_list == actual_error_list, "Error list not matching"



