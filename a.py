import sys

def main():
    file_list = []
    added_files = " ".join(sys.argv[1:])  # Concatenate command line arguments into a single string
    print("List of added files:", added_files)
    files_split = added_files.split()  # Split the string by space to get individual file paths
    for file in files_split:
        file_list.append(file)
    print("List print from Python:", file_list)

if __name__ == "__main__":
    main()
