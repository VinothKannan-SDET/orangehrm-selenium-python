import pytest


@pytest.mark.smoke
def test_TC_OL_004_delete_location_by_name(logged_in_admin, admin_page, locations_page, config, test_data):
    """
    Verify that an existing Location can be deleted successfully
    and the deleted Location is no longer available in the search results.
    """

    # Step 1: Navigate to Admin > Organization > Locations page
    locations_page.admin_top_menu_navigation(test_data["top_menu_name"])
    locations_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Verify that the Locations page is loaded
    assert test_data["location_url"] in (locations_page.get_current_page_url()), \
        "Expected Location page should load"

    # Step 3: Click Search button to load the existing Location records
    locations_page.click_save_or_search_btn("Search")

    # Step 4: Identify the Location Name column in the table
    location_index = locations_page.get_search_header_index(test_data["location_header"])

    # Step 5: Select a random existing Location from the list
    existing_location = locations_page.get_existing_record(location_index)

    # Step 6: Delete the selected Location
    locations_page.delete_record(location_index,existing_location)

    # Step 7: Navigate back to the Admin page after deletion
    admin_page.navigate_to_admin()

    # Step 8: Navigate back to Admin > Organization > Locations page
    locations_page.admin_top_menu_navigation(test_data["top_menu_name"])
    locations_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 9: Search for the deleted Location by name
    locations_page.enter_field_input("Name",existing_location)

    # Step 10: Click Search button to search for the deleted Location
    locations_page.click_save_or_search_btn("Search")

    # Step 11: Verify that the deleted Location is not present
    # in the search results
    assert "No Records Found" in (locations_page.get_no_record_count()), \
        "Expected 'No Records Found' message after deleting the Location"