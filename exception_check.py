import os
import importlib.util
import inspect
from tabulate import tabulate

def extract_functions(file_paths):
    print("extract_functions", file_paths)
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
    print("check_exceptions called", extract_functions)
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

# Get the list of file paths dynamically from the GitHub Actions workflow
file_paths_str = os.environ.get("ADDED_FILES", "")
file_paths = file_paths_str.split(',') if file_paths_str else []

functions_list = extract_functions(file_paths)
results = check_exceptions(functions_list)

table_headers = ["File Name", "Function Name", "File Path", "Exception Block"]
table_data = [(result["file_name"], result["function_name"], result["file_path"], result["has_exception_block"]) for result in results]
print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
