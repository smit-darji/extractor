import sys

def main():
    added_files = sys.argv[1:]  # Get command line arguments except the script name
    print("List of added files:")
    for file in added_files:
        print(file)

if __name__ == "__main__":
    main()
