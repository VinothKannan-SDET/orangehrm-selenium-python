import pytest


@pytest.mark.smoke
def test_TC_OL_002_add_location_empty_name(logged_in_admin, admin_page, locations_page, config, test_data):
    """
    Verify that the Location Name mandatory field validation
    is displayed when the Location Name is submitted empty.
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

    # Step 5: Leave the Location Name field empty
    # and enter the remaining mandatory/required test data
    random_number = locations_page.get_random_number(111,999)

    locations_page.enter_field_input("Name", test_data["name"])

    # Step 6: Enter City
    locations_page.enter_field_input("City", test_data["city"])

    # Step 7: Enter Phone number with a unique suffix
    locations_page.enter_field_input("Phone", test_data["phone"] + random_number)

    # Step 8: Select the Country from the Country dropdown
    locations_page.click_dropdown_option("Country", test_data["country"])

    # Step 9: Click Save button to submit the form
    locations_page.click_save_or_search_btn("Save")

    # Step 10: Verify that the mandatory field validation
    # message is displayed for the Location Name field
    assert locations_page.get_field_validation_error(test_data["field_name"]), \
        f"Expected validation error for mandatory field " \
        f"'{test_data['field_name']}' when it is empty"