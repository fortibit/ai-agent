from google.genai import types
from config import WORKING_DIR

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file_content import schema_write_file_content, write_file_content


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file_content,
    ]
)

functions_dict = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file_content": write_file_content,
}


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    
    # Manually add working directory to arguments, since LLM doesn't control it 
    function_args["working_directory"] = WORKING_DIR

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Call function
    functions_dict[function_name](**function_args)
