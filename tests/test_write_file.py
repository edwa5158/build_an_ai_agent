"""Tests for `functions.write_file.write_file`.

Validates that writes succeed for in-bounds paths and that attempts to write
outside the permitted working directory are rejected.
"""

from tests.test_utils import run_test_cases
from functions.write_file import write_file

def main()->str:
    """Run the test cases for `functions.write_file.write_file`.

    :return: A formatted results string that includes per-case output and a summary.
    :rtype: str
    """
    test_cases:list[tuple[str,str, str]] = [
        ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
        ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("calculator", "/tmp/temp.txt", "this should not be allowed")
    ]

    expect_to_find: list[str] = [
        "28 characters written",
        "26 characters written",
        "Error:",
    ]

    return run_test_cases(test_cases, expect_to_find, write_file)

if __name__ == "__main__":
    print(main())