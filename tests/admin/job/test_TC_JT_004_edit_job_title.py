import pytest


@pytest.mark.smoke
def test_TC_JT_004_edit_job_title(logged_in_admin, add_job_page, admin_page, config, test_data):
    """
    Verify that an existing Job Title can be edited successfully
    and the updated Job Title is accepted by the application.
    """

    # Step 1: Navigate to Admin > Job > Job Titles page
    add_job_page.admin_top_menu_navigation(test_data["top_menu"])
    add_job_page.admin_top_submenu_navigation(test_data["sub_menu"])

    # Step 2: Identify the Job Title column in the table
    job_title_index = add_job_page.get_job_list_header_column(test_data["job_title_header"])

    # Step 3: Get all existing Job Titles from the table
    job_title_list = add_job_page.get_job_title_list(job_title_index)

    # Step 4: Select a random existing Job Title
    random_number = add_job_page.get_random_number(1, len(job_title_list))
    job_name = job_title_list[int(random_number) - 1]

    # Step 5: Click Edit and enter the updated Job Title
    edited_job_title_name = add_job_page.edit_job_title(job_name)

    # Step 6: Click Save button to submit the updated Job Title
    add_job_page.create_job_save_btn()

    # Step 7: Verify that the Job Title update was successful
    assert add_job_page.is_job_creation_success(), \
        f"Job Title '{edited_job_title_name}' was not updated successfully"