import pytest


@pytest.mark.smoke
def test_TC_OL_001_add_location_valid(logged_in_admin, admin_page, locations_page, config, test_data):
    """
    Verify that a valid Location can be created successfully
    and the newly created Location can be found using the search.
    """

    # Step 1: Navigate to Admin > Organization > Locations page
    locations_page.admin_top_menu_navigation(test_data["top_menu_name"])
    locations_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Verify that the Locations page is loaded
    assert test_data["location_url"] in (locations_page.get_current_page_url()), \
        "Expected Location page should load"

    # Step 3: Click the Add button to open the Location creation form
    locations_page.click_location_add_btn()

    # Step 4: Verify that the Add Location page is loaded
    assert test_data["save_location_url"] in (locations_page.get_current_page_url()), \
        "Expected Add Location page should load"

    # Step 5: Generate a unique suffix for the Location name and phone
    random_number = locations_page.get_random_number(111, 999)

    # Step 6: Enter the Location name
    locations_page.enter_field_input("Name", test_data["name"] + random_number)

    # Step 7: Enter the City
    locations_page.enter_field_input("City", test_data["city"])

    # Step 8: Enter the Phone number with a unique suffix
    locations_page.enter_field_input("Phone", test_data["phone"] + random_number)

    # Step 9: Select the Country from the Country dropdown
    locations_page.click_dropdown_option("Country", test_data["country"])

    # Step 10: Click Save button to create the Location
    locations_page.click_save_or_search_btn("Save")

    # Step 11: Verify that the Location creation success message
    # is displayed
    assert locations_page.is_location_creation_success(), \
        "Expected success message after creating valid Location"

    # Step 12: Navigate back to Admin > Organization > Locations page
    admin_page.navigate_to_admin()
    locations_page.admin_top_menu_navigation(test_data["top_menu_name"])
    locations_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 13: Search for the newly created Location by name
    locations_page.enter_field_input("Name", test_data["name"] + random_number)

    # Step 14: Click Search button
    locations_page.click_save_or_search_btn("Search")

    # Step 15: Verify that exactly one matching Location record is found
    assert "(1) Record Found" in (locations_page.get_record_count()), \
        "Expected (1) Record Found message after searching for created Location"