from typing import Callable

def run_all_tests():
    import test_get_file_content
    import test_get_files_info
    import test_write_file

    test_modules: list[Callable] = [
        test_get_files_info.main,
        test_get_file_content.main,
        test_get_files_info.main,
    ]
    result: str = ""
    for func in test_modules:
        result += "\n\n" + func()
    
    print(result)

if __name__ == "__main__":
    run_all_tests()