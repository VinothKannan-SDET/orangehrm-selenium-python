import pytest


@pytest.mark.smoke
def test_TC_UM_005_search_user_exact_username(logged_in_admin, add_user_page, config, test_data):
    """
    Verify that a user can be searched successfully using
    the exact username.
    """

    # Step 1: Navigate to Admin > User Management > Users page
    add_user_page.admin_top_menu_navigation(test_data["top_menu_name"])
    add_user_page.admin_top_submenu_navigation(test_data["top_submenu_name"])

    # Step 2: Get an existing username from the user list
    existing_username = add_user_page.get_existing_user()

    # Step 3: Search for the user using the exact username
    add_user_page.search_user(existing_username)

    # Step 4: Verify that the displayed username exactly matches
    # the searched username
    assert existing_username == add_user_page.verify_user_exact_search(), \
        f"Expected exact username search result '{existing_username}'"