from functions.get_file_content import get_file_content

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


def append_test_case_result(case_num: int, result: str, case: tuple[str, str], actual: str)->str:
    new_result: str = result
    new_result = "\n".join([new_result, "\n" + "-"*10 + f"Test Case: {case_num}" + "-"*10])
    new_result = "\n".join([new_result, f"Inputs: {case}"])
    new_result = "\n".join([new_result, f"Actual: \n{actual}"])
    return new_result


def main():
    case_num:int = 0
    result: str = "\n\n" + "-"*30 + "starting testing" + "-"*30

    for case in test_cases:
        case_num += 1
        actual: str = get_file_content(*case)
        result = append_test_case_result(case_num, result, case, actual)
        
    things_found = [] 
    for thing in expect_to_find:
        things_found.append(f"{thing}: {thing in result}")
    things_found_str = "\t" + "\n\t".join(things_found)
    num_true = things_found_str.count(": True")
    things_found_str += "\n\n\t" + f"{num_true} passed of {len(expect_to_find)}"

    result += "\n\n" + "-"*30 + "RESULT SUMMARY" + "-"*30
    result = "\n".join([result, things_found_str]) + "\n\n"

    print(result)

if __name__ == "__main__":
    main()