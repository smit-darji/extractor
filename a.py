import os


# Added files obtained from the GitHub Actions workflow environment variable
added_files_str = os.environ.get("ADDED_FILES", "")
file_paths = added_files_str.split() if added_files_str else []

# Print the value of the ADDED_FILES environment variable
print("ADDED_FILES:", added_files_str)
