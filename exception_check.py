import os
import importlib.util
import inspect
import sys
from tabulate import tabulate

def extract_functions(file_paths):
    functions = []
    for file_path in file_paths:
        if file_path.endswith('.pyc'):
            continue
        try:
            spec = importlib.util.spec_from_file_location("module_name", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            for func_name in dir(module):
                if callable(getattr(module, func_name)):
                    functions.append({"file_name": os.path.basename(file_path), "function_name": func_name, "file_path": file_path})
        except FileNotFoundError:
            pass

    return functions

def check_exceptions(functions):
    results = []
    for func_info in functions:
        file_name = func_info["file_name"]
        func_name = func_info["function_name"]
        file_path = func_info["file_path"]
        
        try:
            module_name = file_name.split('.')[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            func = getattr(module, func_name)
            source_code = inspect.getsource(func)
            has_exception_block = "try" in source_code and "except" in source_code
            results.append({"file_name": file_name, "function_name": func_name, "file_path": file_path, "has_exception_block": "Yes" if has_exception_block else "No"})
        except Exception as e:
            results.append({"file_name": file_name, "function_name": func_name, "file_path": file_path, "has_exception_block": "No"})

    return results

def main():
    file_list = []
    added_files = " ".join(sys.argv[1:]) 
    files_split = added_files.split()
    for file in files_split:
        file_list.append(file)

    # Filter out file paths starting with '__pycache__'
    file_list = [file_path for file_path in file_list if not file_path.startswith('./__pycache__')]

    print("List print from Python:", file_list)

    # Extract functions from the provided file paths
    functions_list = extract_functions(file_list)

    # Check for exception blocks in the extracted functions
    results = check_exceptions(functions_list)

    # Create the result table for all functions
    all_table_headers = ["File Name", "Function Name", "File Path", "Exception Block"]
    all_table_data = [(result["file_name"], result["function_name"], result["file_path"], result["has_exception_block"]) for result in results]
    
    # Create the result table for functions without exception blocks
    all_table_headers = ["File Name", "Function Name", "File Path", "Exception Block"]
    no_exception_results = [result for result in results if result["has_exception_block"] == "No"]
    no_exception_table_data = [(result["file_name"], result["function_name"], result["file_path"], result["has_exception_block"]) for result in no_exception_results]

    # Print the result table for all functions
    print(" ")
    print("All Functions:")
    print(tabulate(all_table_data, headers=all_table_headers, tablefmt="grid"))

    # Print the result table for functions without exception blocks
    print(" ")
    print("Functions without Exception Blocks:")
    print(tabulate(no_exception_table_data, headers=all_table_headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
