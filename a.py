import sys

def main():
    file_list= []
    added_files = sys.argv[1:]  # Get command line arguments except the script name
    print("List of added files:")
    for file in added_files:
        file_list.append(file)
    print("List print from python", file_list)

if __name__ == "__main__":
    main()
