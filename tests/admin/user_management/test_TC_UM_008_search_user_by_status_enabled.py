import pytest
from utilities.logger import get_logger
logger = get_logger(__name__)


@pytest.mark.sanity
def test_TC_UM_008_search_user_by_status_enabled(logged_in, logged_in_admin,
                                                 add_user_page, config, test_data):
    #Get existing username
    add_user_page.navigate_to_add_user()

    add_user_page.search_user_with_status_base(test_data)
    # error_list = add_user_page.verify_role_based_search(test_data,test_data["status_header"])
    username_index = add_user_page.get_search_header_index(test_data["username_header"])
    status_index = add_user_page.get_search_header_index(test_data["status_header"])
    error_list = add_user_page.verify_search_user_list(
        username_index, status_index, test_data["status"])
    assert len(error_list) == 0,f"Listed username not in Enabled Status : {error_list}"