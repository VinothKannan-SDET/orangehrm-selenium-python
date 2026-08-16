import pytest
from utilities.logger import get_logger
logger = get_logger(__name__)


@pytest.mark.sanity
def test_TC_UR_002_verify_ess_role(logged_in, logged_in_admin, add_user_page, config, test_data):
    #Get existing username
    add_user_page.navigate_to_add_user()

    add_user_page.search_user_with_role_base(test_data)
    # error_list = add_user_page.verify_role_based_search(test_data, test_data["user_role_header"])
    username_index = add_user_page.get_search_header_index(test_data["username_header"])
    user_role_index = add_user_page.get_search_header_index(test_data["user_role_header"])
    error_list = add_user_page.verify_search_user_list(
        username_index, user_role_index, test_data["user_role"])
    assert len(error_list) == 0,f"Listed username not in ESS role : {error_list}"