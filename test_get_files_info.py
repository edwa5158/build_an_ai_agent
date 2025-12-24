from functions.get_files_info import get_files_info
import re
tests_cases = [
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

def append_test_case_result(case_num, result, case, actual):
    new_result = result
    new_result = "\n".join([new_result, "\n" + "-"*10 + f"Test Case: {case_num}" + "-"*10])
    new_result = "\n".join([new_result, f"Inputs: {case}"])
    new_result = "\n".join([new_result, f"Actual: \n{actual}"])
    return new_result

def main():
    case_num = 0
    result = "\n\n" + "-"*30 + "starting testing" + "-"*30

    for case in tests_cases:
        case_num += 1
        actual = get_files_info(*case)
        result = append_test_case_result(case_num, result, case, actual)
 
    things_found = [] 
    for thing in expect_to_find:
        things_found.append(f"{thing}: {thing in result}")
    things_found_str = "\t" + "\n\t".join(things_found)
    
    result += "\n\n" + "-"*30 + "RESULT SUMMARY" + "-"*30
    result = "\n".join([result, things_found_str]) + "\n\n"

    print(result)

if __name__ == "__main__":
    main()