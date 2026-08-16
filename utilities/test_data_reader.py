import json
from pathlib import Path

class TestDataReader:

    @staticmethod
    def read_test_data(test_file_path):

        # Convert string path to Path object
        test_file_path = Path(test_file_path)

        # Find the 'tests' directory dynamically
        tests_dir = next(
            (
                parent for parent in test_file_path.parents
                if parent.name == "tests"
            ),
            None
        )

        # Validate that 'tests' directory was found
        if tests_dir is None:
            raise ValueError(
                f"Could not find 'tests' directory in test path: "
                f"{test_file_path}"
            )

        # Project root is the parent of 'tests'
        project_root = tests_dir.parent

        # Get test file path relative to tests/
        relative_path = test_file_path.relative_to(tests_dir)

        # Remove 'test_' from filename
        json_file_name = relative_path.name.replace(
            "test_", "", 1
        )

        # Change .py to .json
        json_file_name = Path(json_file_name).with_suffix(".json")

        # Build corresponding test-data path
        json_path = (
            project_root
            / "test_data"
            / relative_path.parent
            / json_file_name
        )

        # Validate test data file exists
        if not json_path.exists():
            raise FileNotFoundError(
                f"Test data file not found: {json_path}"
            )

        # Read JSON
        with open(json_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in {json_path}: {e}")