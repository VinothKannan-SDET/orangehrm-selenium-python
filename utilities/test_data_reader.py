import json
from pathlib import Path


class TestDataReader:
    """
    Utility class for reading test data from JSON files.

    Automatically determines the corresponding JSON test-data file
    based on the location and name of the pytest test file.

    Example:

        tests/admin/job/test_job.py
        ->
        test_data/admin/job/job.json

    The class does not require object creation because the data-reading
    method is implemented as a static method.
    """

    @staticmethod
    def read_test_data(test_file_path):
        """
        Read and return JSON test data corresponding to a pytest test file.

        The method searches for the 'tests' directory in the supplied
        test file path, determines the project root, and maps the test
        file to its corresponding JSON file under the 'test_data' folder.

        :param test_file_path: Path of the pytest test file.
        :return: Test data loaded from the corresponding JSON file.
        :raises ValueError: If the 'tests' directory cannot be found
                            or the JSON file contains invalid JSON.
        :raises FileNotFoundError: If the corresponding test-data JSON
                                   file does not exist.
        """

        # Step 1: Convert the test file path string into a Path object
        test_file_path = Path(test_file_path)

        # Step 2: Find the 'tests' directory dynamically
        tests_dir = next(
            (
                parent
                for parent in test_file_path.parents
                if parent.name == "tests"
            ),
            None
        )

        # Step 3: Validate that the 'tests' directory was found
        if tests_dir is None:
            raise ValueError(
                f"Could not find 'tests' directory in test path: "
                f"{test_file_path}"
            )

        # Step 4: Determine the project root directory
        # The project root is the parent directory of 'tests'
        project_root = tests_dir.parent

        # Step 5: Get the test file path relative to the 'tests' directory
        relative_path = test_file_path.relative_to(tests_dir)

        # Step 6: Remove the 'test_' prefix from the test filename
        json_file_name = relative_path.name.replace(
            "test_", "", 1
        )

        # Step 7: Change the file extension from .py to .json
        json_file_name = Path(json_file_name).with_suffix(".json")

        # Step 8: Build the corresponding test-data JSON file path
        json_path = (
            project_root
            / "test_data"
            / relative_path.parent
            / json_file_name
        )

        # Step 9: Validate that the test-data JSON file exists
        if not json_path.exists():
            raise FileNotFoundError(
                f"Test data file not found: {json_path}"
            )

        # Step 10: Open the JSON test-data file
        with open(json_path, "r", encoding="utf-8") as file:
            try:
                # Step 11: Parse and return JSON test data
                return json.load(file)

            except json.JSONDecodeError as e:
                # Step 12: Raise a meaningful error when JSON is invalid
                raise ValueError(
                    f"Invalid JSON in {json_path}: {e}"
                ) from e