#!/usr/bin/env python3
def read_list_file():
    # Try to open the file 'list.txt' in read mode
    try:
        with open('list.txt', 'r') as file:
            # Read the content of the file line by line
            lines = file.readlines()
            # Strip newline characters from each line and store them in a list
            values = [line.strip() for line in lines]
        return values
    # Handle the case where the file is not found or cannot be opened
    except FileNotFoundError:
        print("File 'list.txt' not found in the working directory.")
        return []
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

file_content = read_list_file()

print(file_content)

