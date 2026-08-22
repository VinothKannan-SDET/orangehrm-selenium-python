import pytest

@pytest.mark.smoke
def test_TC_JT_001_add_job_title_valid(logged_in_admin,add_job_page, admin_page,config, test_data):
    """Verify that a valid job title can be added and appears in the list"""

    # Step 1: Navigate to Admin > Job > Job Titles page
    add_job_page.admin_top_menu_navigation(test_data["top_menu"])
    add_job_page.admin_top_submenu_navigation(test_data["sub_menu"])

    # Step 2: Click Add button to open job title form
    add_job_page.job_title_add_btn()

    # Step 3: Enter a unique job title using random number suffix
    job_title = test_data["job_title"] + add_job_page.get_random_number(2, 999)
    add_job_page.enter_job_title_details(job_title)

    # Step 4: Click Save and verify success toast message appears
    add_job_page.create_job_save_btn()
    add_job_page.is_job_creation_success()

    # Step 5: Navigate back to Job Titles list page
    admin_page.navigate_to_admin()
    add_job_page.admin_top_menu_navigation(test_data["top_menu"])
    add_job_page.admin_top_submenu_navigation(test_data["sub_menu"])

    # Step 6: Verify the newly created job title appears in the list
    job_title_index = add_job_page.get_job_list_header_column(
        test_data["job_title_header"])
    assert add_job_page.verify_new_job_creation(job_title_index, job_title), \
        f"Newly Created Job Title '{job_title}' not found in list"