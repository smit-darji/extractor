import os
import importlib.util
import inspect
from tabulate import tabulate

def extract_functions(folder_path):
    # Initialize a list to store the function names along with their file names
    functions = []

    # Get all files and directories in the folder
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)
        
        if item == "__pycache__":
            continue

        if os.path.isdir(item_path):  # If item is a directory, recursively call extract_functions
            functions.extend(extract_functions(item_path))
        elif os.path.isfile(item_path):  # If item is a file, extract functions from it
            module_name = item.split('.')[0]  # Extract module name from file name
            try:
                spec = importlib.util.spec_from_file_location(module_name, item_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for func_name in dir(module):
                    if callable(getattr(module, func_name)):
                        functions.append({"file_name": item, "function_name": func_name, "file_path": item_path})
            except FileNotFoundError:
                pass

    return functions

def check_exceptions(functions):
    # Initialize a list to store the results
    results = []

    for func_info in functions:
        file_name = func_info["file_name"]
        func_name = func_info["function_name"]
        file_path = func_info["file_path"]
        
        try:
            module_name = file_name.split('.')[0]  # Extract module name from file name
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

# Get the path to the "dag" folder dynamically using the GITHUB_WORKSPACE environment variable
github_workspace = os.environ.get("GITHUB_WORKSPACE", "./")
dag_folder_path = os.path.join(github_workspace, "dag")

# Call the function to extract functions and store the results
functions_list = extract_functions(dag_folder_path)

# Call the function to check for exception blocks and store the results
results = check_exceptions(functions_list)

# Convert results to a tabular format and print the table
table_headers = ["File Name", "Function Name", "File Path", "Exception Block"]
table_data = [(result["file_name"], result["function_name"], result["file_path"], result["has_exception_block"]) for result in results]
print(tabulate(table_data, headers=table_headers, tablefmt="grid"))
