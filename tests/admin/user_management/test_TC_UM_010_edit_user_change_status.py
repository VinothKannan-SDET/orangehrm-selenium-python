import pytest

@pytest.mark.smoke
def test_TC_UM_010_edit_user_change_status(logged_in, logged_in_admin,
                                           add_user_page, config, test_data):
    # Get existing username
    add_user_page.navigate_to_add_user()
    existing_username = add_user_page.get_existing_user()

    # Edit the user role
    add_user_page.search_user(existing_username)
    assert "(1) Record Found" in add_user_page.get_record_count(), \
        "Expected (1) Records Found message in Search after creating valid user"

    username_index = add_user_page.get_search_header_index(test_data["username_header"])
    status_index = add_user_page.get_search_header_index(test_data["status_header"])

    status_value_before = add_user_page.get_user_column_value(status_index)

    add_user_page.click_edit_btn()
    if status_value_before == "Enabled":
        add_user_page.edit_user_data(test_data["status_header"], "Disabled")
    else:
        add_user_page.edit_user_data(test_data["status_header"], "Enabled")

    add_user_page.click_search_btn()

    # verify after update
    add_user_page.navigate_to_add_user()
    add_user_page.search_user(existing_username)
    assert "(1) Record Found" in add_user_page.get_record_count(), "Expected (1) Records Found message in Search after creating valid user"

    error_list = add_user_page.verify_search_user_list(
        username_index, status_index, test_data["status"])
    assert len(error_list) == 0, f"Listed username not in {test_data['status']} Status : {error_list}"