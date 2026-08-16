import pytest

@pytest.mark.smoke
def test_TC_UM_011_delete_single_user(logged_in_admin, add_user_page, config, test_data):
    # Get existing username
    add_user_page.navigate_to_add_user()
    existing_username = add_user_page.get_existing_user()

    add_user_page.search_user(existing_username)
    assert "(1) Record Found" in add_user_page.get_record_count(), "Expected (1) Records Found message in Search after creating valid user"

    username_index = add_user_page.get_search_header_index(test_data["username_header"])
    error_name_list = add_user_page.get_searched_username(username_index, existing_username)
    assert len(error_name_list) == 0, f"Username - {existing_username} to delete but searched username - {error_name_list}"

    add_user_page.delete_single_user(existing_username)

    # Get existing username
    add_user_page.navigate_to_add_user()
    add_user_page.search_user(existing_username)
    assert "No Records Found" in add_user_page.get_no_record_count(), "Expected No Records Found message in Search after creating valid user"


