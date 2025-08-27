import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):

    def test_get_files_info_valid_1(self):
        dir = "."
        result = get_files_info("calculator", dir)
        print("Result for current directory:")
        print(result)

    def test_get_files_info_valid_2(self):
        dir = "pkg"
        result = get_files_info("calculator", dir)
        print(f"Result for '{dir}' directory:")
        print(result)

    def test_get_files_info_invalid_1(self):
        dir = "/bin"
        result = get_files_info("calculator", dir)
        print(f"Result for '{dir}' directory:")
        print(result)

    def test_get_files_info_invalid_2(self):
        dir = "../"
        result = get_files_info("calculator", dir)
        print(f"Result for '{dir}' directory:")
        print(result)


if __name__ == "__main__":
    unittest.main()
