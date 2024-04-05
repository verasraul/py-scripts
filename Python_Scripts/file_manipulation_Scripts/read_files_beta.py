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

    contentA = set(read_txt_file(fileA_path))
    contentB = set(read_txt_file(fileB_path))

    common_content = contentA.intersection(contentB)

    if common_content:
        print("Do not add the following content:")
        for content in common_content:
            print(content)
    else:
        print("Add the following content:")
        for content in contentA:
            print(content)

# Example usage:
fileA = "fileA.txt"
fileB = "fileB.txt"
compare_files_content(fileA, fileB)