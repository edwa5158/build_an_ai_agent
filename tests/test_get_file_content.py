"""Tests for `functions.get_file_content.get_file_content`.

Validates expected content is returned for existing files and that an error message
is produced for invalid/unsafe paths.
"""
from tests.test_utils import run_test_cases
from functions.get_file_content import get_file_content
    
def main()->str:
    """Run the test cases for `functions.get_file_content.get_file_content`.

    :return: A formatted results string that includes per-case output and a summary.
    :rtype: str
    """
    test_cases: list[tuple[str, str]] = [
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py")
    ]

    expect_to_find: list[str] = [
        "def main():",
        "def _apply_operator(self, operators, values)",
        "Error:",
    ]
    return run_test_cases(test_cases, expect_to_find, get_file_content)

if __name__ == "__main__":
    print(main())