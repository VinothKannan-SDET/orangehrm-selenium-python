import pytest

@pytest.mark.smoke
def test_TC_UM_012_delete_multiple_users(logged_in_admin, add_user_page, config, test_data):
    delete_user_list = []
    count = 0
    # Get existing username
    add_user_page.navigate_to_add_user()
    while count < test_data["user_deletion_count"]:
        existing_username = add_user_page.get_existing_user()
        if existing_username not in delete_user_list and existing_username != "Admin":
            delete_user_list.append(existing_username)
        add_user_page.click_search_btn()
        count += 1

    for delete in delete_user_list:
        add_user_page.search_user(delete)
        assert "(1) Record Found" in add_user_page.get_record_count(), "Expected (1) Records Found message in Search after creating valid user"
        username_index = add_user_page.get_search_header_index(test_data["username_header"])
        error_name_list = add_user_page.get_searched_username(username_index, delete)
        assert len(error_name_list) == 0, f"Username - {delete} to delete but searched username - {error_name_list}"
        add_user_page.delete_single_user(delete)
        # Get existing username
        add_user_page.navigate_to_add_user()
        add_user_page.search_user(existing_username)
        assert "No Records Found" in add_user_page.get_no_record_count(), "Expected No Records Found message in Search after creating valid user"


