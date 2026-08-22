import pytest


@pytest.mark.smoke
def test_TC_JT_006_verify_job_title_in_dropdown(logged_in_admin, add_job_page, config, test_data):
    """
    Verify that the Job Titles submenu is displayed
    under the selected Admin top menu.
    """

    # Step 1: Navigate to the configured Admin top menu
    add_job_page.admin_top_menu_navigation(test_data["top_menu"])

    # Step 2: Verify that the Job Titles submenu is visible
    assert add_job_page.verify_job_title_dropdown(test_data["sub_menu"]), \
        f"Sub Menu '{test_data['sub_menu']}' is not visible"