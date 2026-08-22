import pytest


@pytest.mark.smoke
def test_TC_JT_003_add_job_title_duplicate(logged_in_admin, add_job_page, admin_page, config, test_data):
    """
    Verify that creating a Job Title with an existing name
    displays the 'Already exists' validation message.
    """

    # Step 1: Navigate to Admin > Job > Job Titles page
    add_job_page.admin_top_menu_navigation(test_data["top_menu"])
    add_job_page.admin_top_submenu_navigation(test_data["sub_menu"])

    # Step 2: Identify the Job Title column in the table
    job_title_index = add_job_page.get_job_list_header_column(test_data["job_title_header"])

    # Step 3: Get all existing Job Titles from the current page
    job_title_list = add_job_page.get_job_title_list(job_title_index)

    # Step 4: Select a random existing Job Title
    random_number = add_job_page.get_random_number(1, len(job_title_list))
    job_name = job_title_list[int(random_number) - 1]

    # Step 5: Click Add button to open the Job Title creation form
    add_job_page.job_title_add_btn()

    # Step 6: Enter the existing Job Title name
    # to intentionally create a duplicate
    add_job_page.enter_job_title_details(job_name)

    # Step 7: Click Save button to submit the duplicate Job Title
    add_job_page.create_job_save_btn()

    # Step 8: Verify that the 'Already exists' validation message
    # is displayed for the Job Title field
    assert add_job_page.get_field_validation_error(test_data["field_name"]) == "Already exists", \
        f"Expected Job Title '{job_name}' to show 'Already exists' validation"