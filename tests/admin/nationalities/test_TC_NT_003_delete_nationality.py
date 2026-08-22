import pytest


@pytest.mark.smoke
def test_TC_NT_003_delete_nationality(logged_in_admin, admin_page, nationalities_page, config, test_data):
    """
    Verify that an existing Nationality can be deleted successfully
    and the deleted Nationality no longer appears in the list.
    """

    # Step 1: Navigate to Admin > Nationalities page
    nationalities_page.admin_top_menu_navigation(test_data["top_menu_name"])

    # Step 2: Verify that the Nationalities page is loaded
    assert test_data["nationalities_url"] in (nationalities_page.get_current_page_url()), \
        "Expected Nationalities page should load"

    # Step 3: Identify the Nationality column in the table
    national_index = nationalities_page.get_search_header_index(test_data["national_header"])

    # Step 4: Get all existing Nationalities from the table
    national_list = nationalities_page.get_nationality_list(national_index)

    # Step 5: Select a random existing Nationality
    random_number = nationalities_page.get_random_number(1, len(national_list))
    national_name = national_list[int(random_number) - 1]

    # Step 6: Delete the selected Nationality
    nationalities_page.delete_record(national_index, national_name)

    # Step 7: Verify that the deleted Nationality
    # is no longer present in the Nationalities list
    actual_national_name = (nationalities_page.is_nationality_present(national_index, national_name))

    # Step 8: Assert that the deleted Nationality is not found
    assert actual_national_name is None, \
        f"Expected Nationality '{national_name}' to be deleted but still found"