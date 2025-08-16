from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

#print(get_files_info("calculator", "."))
#print(get_files_info("calculator", "pkg"))
#print(get_files_info("calculator", "/bin"))
#print(get_files_info("calculator", "../"))
#print(get_files_info("calculator", "main.py"))


get_file_content("calculator", "main.py")
get_file_content("calculator", "pkg/calculator.py")
get_file_content("calculator", "/bin/cat")
get_file_content("calculator", "pkg/does_not_exist.py")
