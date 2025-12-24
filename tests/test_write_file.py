from tests.test_utils import run_test_cases
from functions.write_file import write_file

def main()->str:
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