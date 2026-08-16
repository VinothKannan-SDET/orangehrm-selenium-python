import pytest
from utilities.logger import get_logger
logger = get_logger(__name__)


@pytest.mark.smoke
def test_TC_UM_005_search_user_exact_username(logged_in_admin, add_user_page, config):
    #Get existing username
    add_user_page.navigate_to_add_user()
    existing_username = add_user_page.get_existing_user()

    # Search User with name
    add_user_page.search_user(existing_username)
    assert (existing_username == add_user_page.verify_user_exact_search()),\
        "Expected user exact search result"