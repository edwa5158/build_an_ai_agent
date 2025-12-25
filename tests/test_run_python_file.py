"""Tests for `functions.run_python_file.run_python_file`.

Validates that Python files execute successfully within the allowed working
directory and that unsafe/invalid inputs return helpful error messages.
"""

from tests.test_utils import run_test_cases
from functions.run_python_file import run_python_file

def main()->str:
    """Run the test cases for `functions.run_python_file.run_python_file`.

    :return: A formatted results string that includes per-case output and a summary.
    :rtype: str
    """
    test_cases = [
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
    ("calculator", "lorem.txt"),
    ]
    expect_to_find = [
        "STDOUT:",
        "STDERR:",
        'Cannot execute "../main.py" as it is outside',
        '"nonexistent.py" does not exist',
        '"lorem.txt" is not a Python file',
    ]  

    return run_test_cases(test_cases, expect_to_find, run_python_file)

if __name__ == "__main__":
    print(main())