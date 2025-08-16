import os

#                    "calculator"     , "pkg/calculator.py"
#                    "calculator"     , "main.py"
#                    "calculator"     , "/bin/cat"               <== error str
#                    "calculator"     , "pkg/does_not_exist.py"  <== error str
def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.join(abs_working_dir, file_path)
    print(abs_file_path)