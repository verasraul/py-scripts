#!/usr/bin/env python3
def read_list_file(filename):
    # Try to open the file 'list.txt' in read mode
    try:
        with open(filename, 'r') as file:
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

def compare_files(add_to_stock, movies_in_stock):
    # Print values that are in  add_to_stock.txt but not in movies_in_stock.txt
    print("Add the following:")
    for title in add_to_stock:
        if title not in movies_in_stock:
            print(f"- {title}")

    # Print values that are in both files
    print("\nDo not add the following:")
    for title in add_to_stock:
        if title in movies_in_stock:
            print(f"- {title}")

# Read content of movies_in_stock.txt and add_to_stock.txt
movies_in_stock = read_list_file('movies_in_stock.txt')
add_to_stock = read_list_file('add_to_stock.txt')

# Compare values between the two files
if movies_in_stock and add_to_stock:
    compare_files(add_to_stock, movies_in_stock)