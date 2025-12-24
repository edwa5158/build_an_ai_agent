from typing import Callable

# I wanted to truncate this, but some of the test cases look for stuff in the middle of the file...
def append_test_case_result(case_num: int, result: str, case: tuple[str, str], actual: str)->str:
    new_result: str = result
    new_result = "\n".join([new_result, "\n" + "-"*10 + f"Test Case: {case_num}" + "-"*10])
    new_result = "\n".join([new_result, f"Inputs: {case}"])
    new_result = "\n".join([new_result, f"Actual: \n{actual}"])
    return new_result


def run_test_cases(test_cases:list[tuple], expect_to_find: list[str], func: Callable)->str:
    case_num:int = 0
    result: str = "\n\n" + "*"*30 + f" TESTING `{func.__name__}` " + "*"*30

    for case in test_cases:
        case_num += 1
        actual: str = func(*case)
        result = append_test_case_result(case_num, result, case, actual)
    
    max_width = 50  # Maximum width for each item
    things_found: list[str] = [
        f"{thing[:max_width].ljust(max_width)}| {thing in result}"
        for thing in expect_to_find
    ]
    
    num_true: int = len(list(filter(lambda thing: "| True" in thing, things_found)))
    num_cases: int = len(expect_to_find)

    header_str = f"{'Expected to Find'.ljust(max_width)}| Found"
    things_found_str = "\t" + header_str 
    things_found_str+= "\n\t" + "-"*len(header_str[:-7]) + "+" + "-"*6
    things_found_str+= "\n\t" + "\n\t".join(things_found)
    things_found_str += "\n\n\t" + f"{num_true} passed of {num_cases}"

    result += "\n\n" + "-"*30 + "RESULT SUMMARY" + "-"*30
    result = "\n".join([result, things_found_str])
    return result