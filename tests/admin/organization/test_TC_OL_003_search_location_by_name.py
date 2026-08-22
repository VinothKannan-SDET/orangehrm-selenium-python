import pytest


@pytest.mark.smoke
def test_TC_OL_003_search_location_by_name(logged_in_admin, admin_page, locations_page, config, test_data):
    """
    Verify that an existing Location can be searched successfully
    using the Location Name and the matching record is displayed.
    """

    # Step 1: Navigate to Admin > Organization > Locations page
    locations_page.admin_top_menu_navigation(test_data["top_menu_name"])
    locations_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Verify that the Locations page is loaded
    assert test_data["location_url"] in (locations_page.get_current_page_url()), \
        "Expected Location page should load"

    # Step 3: Click Search button to load the existing Location records
    locations_page.click_save_or_search_btn("Search")

    # Step 4: Identify the Location Name column in the search results
    location_index = locations_page.get_search_header_index(test_data["location_header"])

    # Step 5: Select a random existing Location from the list
    existing_location = locations_page.get_existing_record(location_index)

    # Step 6: Navigate back to the Admin page
    # before navigating to the Locations submenu again
    admin_page.navigate_to_admin()

    # Step 7: Navigate back to Admin > Organization > Locations page
    locations_page.admin_top_menu_navigation(test_data["top_menu_name"])
    locations_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 8: Enter the existing Location Name in the search field
    locations_page.enter_field_input("Name", existing_location)

    # Step 9: Click Search button to perform the Location search
    locations_page.click_save_or_search_btn("Search")

    # Step 10: Verify that exactly one matching Location record is found
    assert "(1) Record Found" in (locations_page.get_record_count()), \
        "Expected (1) Record Found message after searching by Location Name"

    # Step 11: Get the Location Name displayed in the search result
    searched_location = locations_page.get_searched_location(location_index)

    # Step 12: Verify that the searched Location matches
    # the selected existing Location
    assert existing_location == searched_location, \
        f"Expected Location '{existing_location}' was not displayed in search results"