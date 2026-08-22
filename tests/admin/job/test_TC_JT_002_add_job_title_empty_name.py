import pytest


@pytest.mark.smoke
def test_TC_JT_002_add_job_title_empty_name(logged_in_admin, add_job_page, config, test_data):
    """
    Verify that the Job Title mandatory field validation
    is displayed when the Job Title is submitted empty.
    """

    # Step 1: Navigate to Admin > Job > Job Titles page
    add_job_page.admin_top_menu_navigation(test_data["top_menu"])
    add_job_page.admin_top_submenu_navigation(test_data["sub_menu"])

    # Step 2: Click Add button to open the Job Title form
    add_job_page.job_title_add_btn()

    # Step 3: Leave Job Title field empty
    # and proceed with the form submission
    add_job_page.enter_job_title_details(test_data["job_title"])

    # Step 4: Click Save button to submit the form
    add_job_page.create_job_save_btn()

    # Step 5: Verify that the mandatory field validation
    # message is displayed for the Job Title field
    assert add_job_page.get_field_validation_error(test_data["field_name"]), \
        f"Mandatory field '{test_data['field_name']}' validation error not displayed"