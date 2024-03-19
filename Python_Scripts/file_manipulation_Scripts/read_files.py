#!/usr/bin/env python3
import os

def find_and_read_file(filename):
    # Get the current working directory
    current_directory = os.getcwd()

    # Search for the file with the specified name
    file_found = False
    for file in os.listdir(current_directory):
        if file.endswith(".txt") and file == filename:
            file_found = True
            file_path = os.path.join(current_directory, file)
            break

    # If the file is found, read its content line by line and return the values
    if file_found:
        values = []
        with open(file_path, "r") as file:
            for line in file:
                values.append(line.strip())  # Add the stripped line to the list of values
        return values
    else:
        return None  # Return None if the file is not found

# Check for file:
filename = "list.txt"  # Specify the filename you want to search for
result = find_and_read_file(filename)
if result is not None:
    print(f"These are the values {filename} in the file:")
    for value in result:
        print(value)
else:
    print("File not found in the working directory.")
