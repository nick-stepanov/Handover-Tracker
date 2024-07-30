import os
import json
import argparse

def get_all_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append({
                "file_name": file,
                "file_path": file_path
            })
    return file_list

def main():
    parser = argparse.ArgumentParser(description="Generate a JSON file containing all files in a directory.")
    parser.add_argument("directory", help="The directory to scan for files")
    args = parser.parse_args()

    directory = args.directory
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        return

    file_list = get_all_files(directory)
    output_file = os.path.join(directory, "file_list.json")

    with open(output_file, 'w') as f:
        json.dump(file_list, f, indent=2)

    print(f"File list has been saved to {output_file}")

if __name__ == "__main__":
    main()