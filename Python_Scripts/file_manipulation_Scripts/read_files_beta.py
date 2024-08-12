#!/usr/bin/env python3
import os

def search_txt_file(filename):
    # Get the current working directory
    current_directory = os.getcwd()

    # Search for the file with the specified name
    for file in os.listdir(current_directory):
        if file.endswith(".txt") and file == filename:
            return os.path.join(current_directory, file)
    return None

def read_txt_file(file_path):
    if file_path is not None:
        values = []
        with open(file_path, "r") as file:
            for line in file:
                values.append(line.strip())  # Add the stripped line to the list of values
        return values
    else:
        return None  # Return None if the file is not found

def compare_files_content(fileA, fileB):
    fileA_path = search_txt_file(fileA)
    fileB_path = search_txt_file(fileB)

    contentA = read_txt_file(fileA_path)
    contentB = read_txt_file(fileB_path)

    if contentA is None or contentB is None:
        print("Unable to read file content.")
        return

    # Extracting and comparing first comma-separated strings of each line
    lines_A = [line.strip() for line in contentA]
    lines_B = [line.strip() for line in contentB]
  

    # Iterate over lines in A and print them based on matching or non-matching values
    print("Do not add the following content:")
    for line_A in lines_A:
        first_value_A = line_A.split(',')[0].strip()
        if first_value_A in set(line.split(',')[0].strip() for line in lines_B):
            print(line_A)

    print("\nAdd the following content:")
    for line_A in lines_A:
        first_value_A = line_A.split(',')[0].strip()
        if first_value_A not in set(line.split(',')[0].strip() for line in lines_B):
            print(line_A)


# Example usage:
fileA = "add_to_stock.txt"
fileB = "movies_in_stock.txt"
compare_files_content(fileA, fileB)