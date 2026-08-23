import pytest


@pytest.mark.smoke
def test_TC_NT_001_add_nationality(logged_in_admin, admin_page, nationalities_page, config, test_data):
    """
    Verify that a valid Nationality can be created successfully
    and the newly created Nationality appears in the Nationalities list.
    """

    # Step 1: Navigate to Admin > Nationalities page
    nationalities_page.admin_top_menu_navigation(test_data["top_menu_name"])

    # Step 2: Verify that the Nationalities page is loaded
    assert test_data["nationalities_url"] in (nationalities_page.get_current_page_url()), \
        "Expected Nationalities page should load"

    # Step 3: Click the Add button to open the Nationality creation form
    nationalities_page.click_national_add_btn()

    # Step 4: Verify that the Add Nationality page is loaded
    assert test_data["save_nationality_url"] in (nationalities_page.get_current_page_url()), \
        "Expected Add Nationality page should load"

    # Step 5: Generate a unique Nationality name using a random number
    random_number = nationalities_page.get_random_number(111, 999)
    expected_national_name = (test_data["name"] + random_number)

    # Step 6: Enter the Nationality name
    nationalities_page.enter_field_input("Name", expected_national_name)

    # Step 7: Click Save button to create the Nationality
    nationalities_page.click_save_or_search_btn("Save")

    # Step 8: Verify that the Nationality creation success message
    # is displayed
    assert nationalities_page.is_nationality_creation_success(), \
        "Expected success message after creating valid Nationality"

    # Step 9: Identify the Nationality column in the table
    national_index = nationalities_page.get_search_header_index(test_data["national_header"])

    # Step 10: Search the Nationalities list for the newly created record
    actual_national_name = (nationalities_page.is_nationality_present(national_index,
            expected_national_name))

    # Step 11: Verify that the newly created Nationality
    # is present in the list
    assert actual_national_name == expected_national_name, \
        f"Expected Nationality '{expected_national_name}' should be created"