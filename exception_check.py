import os
import importlib.util
import inspect
import sys
from tabulate import tabulate

def extract_functions(file_paths):
    functions = []
    for file_path in file_paths:
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
    print("List print from Python:", file_list)
    
    # List of file paths
    # file_list = ['./__pycache__/a.cpython-310.pyc', './a.py', './dag/dag_file_1.py', './dag/dag_file_2.py', './dag/dag_file_3.py', './dag/test/demo/demo_dag_1.py', './dag/test/demo/demo_dag_file_2.py', './dag/test/test_dag_1.py', './dag/test/test_dag_file_2.py']
    
    # Filter out file paths starting with '__pycache__'
    file_list = [file_path for file_path in file_list if not file_path.startswith('./__pycache__')]

    # Extract functions from the provided file paths
    functions_list = extract_functions(file_list)

    # Check for exception blocks in the extracted functions
    results = check_exceptions(functions_list)

    # Create the result table
    table_headers = ["File Name", "Function Name", "File Path", "Exception Block"]
    table_data = [(result["file_name"], result["function_name"], result["file_path"], result["has_exception_block"]) for result in results]

    # Print the result table
    print(tabulate(table_data, headers=table_headers, tablefmt="grid"))

if __name__ == "__main__":
    main()