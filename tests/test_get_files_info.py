"""Tests for `functions.get_files_info.get_files_info`.

Validates the directory listing output for valid inputs and ensures error messages
are returned for invalid or out-of-bounds paths.
"""

from tests.test_utils import run_test_cases
from functions.get_files_info import get_files_info

def main()->str:
    """Run the test cases for `functions.get_files_info.get_files_info`.

    :return: A formatted results string that includes per-case output and a summary.
    :rtype: str
    """
    test_cases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
    ]
    expect_to_find = [
        "tests.py", 
        "main.py", 
        "is_dir=False", 
        "is_dir=True", 
        "render.py", 
        "calculator.py", 
        "Error:", 
    ]  

    return run_test_cases(test_cases, expect_to_find, get_files_info)

if __name__ == "__main__":
    print(main())