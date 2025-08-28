import unittest
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file import write_file

# class TestGetFilesInfo(unittest.TestCase):

#     def test_get_files_info_valid_1(self):
#         dir = "."
#         result = get_files_info("calculator", dir)
#         print("Result for current directory:")
#         print(result)

#     def test_get_files_info_valid_2(self):
#         dir = "pkg"
#         result = get_files_info("calculator", dir)
#         print(f"Result for '{dir}' directory:")
#         print(result)

#     def test_get_files_info_invalid_1(self):
#         dir = "/bin"
#         result = get_files_info("calculator", dir)
#         print(f"Result for '{dir}' directory:")
#         print(result)

#     def test_get_files_info_invalid_2(self):
#         dir = "../"
#         result = get_files_info("calculator", dir)
#         print(f"Result for '{dir}' directory:")
#         print(result)

# class TestGetFilesContent(unittest.TestCase):

#     def test_get_files_content_valid_1(self):
#         file_path = "main.py"
#         result = get_file_content("calculator", file_path)
#         print(result)

#     def test_get_files_content_valid_2(self):
#         file_path = "pkg/calculator.py"
#         result = get_file_content("calculator", file_path)
#         print(result)

#     def test_get_files_content_invalid_1(self):
#         file_path = "/bin/cat"
#         result = get_file_content("calculator", file_path)
#         print(result)

#     def test_get_files_content_invalid_2(self):
#         file_path = "pkg/does_not_exist.py"
#         result = get_file_content("calculator", file_path)
#         print(result)

# class TestWriteFile(unittest.TestCase):

#     def test_write_file_valid_1(self):
#         result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
#         print(result)

#     def test_write_file_valid_2(self):
#         result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
#         print(result)

#     def test_write_file_invalid(self):
#         result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
#         print(result)

class RunPythonFile(unittest.TestCase):

    def test_run_python_file_valid_1(self):
        result = run_python_file("calculator", "main.py")
        print(result)

    def test_run_python_file_valid_2(self):
        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)

    def test_run_python_file_valid_3(self):
        result = run_python_file("calculator", "tests.py")
        print(result)

    def test_run_python_file_invalid_1(self):
        result = run_python_file("calculator", "../main.py")
        print(result)

    def test_run_python_file_invalid_2(self):
        result = run_python_file("calculator", "nonexistent.py")
        print(result)

if __name__ == "__main__":
    unittest.main()
