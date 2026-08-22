import pytest


@pytest.mark.smoke
def test_TC_NT_002_edit_nationality(logged_in_admin, admin_page, nationalities_page, config, test_data):
    """
    Verify that an existing Nationality can be edited successfully
    and the updated Nationality appears in the Nationalities list.
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

    # Step 6: Click Edit for the selected Nationality
    # and enter the updated Nationality name
    expected_national_name = (nationalities_page.edit_nationality(national_name))

    # Step 7: Click Save button to submit the updated Nationality
    nationalities_page.click_save_or_search_btn("Save")

    # Step 8: Verify that the Nationality update success message
    # is displayed
    assert nationalities_page.is_nationality_creation_success(), \
        "Expected success message after updating Nationality"

    # Step 9: Search the Nationalities list for the updated record
    actual_national_name = (nationalities_page.is_nationality_present(national_index,
            expected_national_name))

    # Step 10: Verify that the updated Nationality is present
    # in the Nationalities list
    assert actual_national_name == expected_national_name, \
        f"Expected Nationality '{expected_national_name}' should be updated"