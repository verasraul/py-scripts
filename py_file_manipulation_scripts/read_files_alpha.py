#!/usr/bin/env python3
import os

def find_file(filename):
    # Get the current working directory
    current_directory = os.getcwd()

    # Search for the file with the specified name
    # file_found = False
    for file in os.listdir(current_directory):
        if file.endswith(".txt") and file == filename:
            # file_found = True
            file_path = os.path.join(current_directory, file)
            return file_path
            # break
        elif file.endswith(".txt") and file == filename is False:
            return None  # Return None if the file is not found

def read_file(filepath):
    # If the file is found, read its content line by line and return the values
    if filepath is not None:
        values = []
    # try:
        with open(filepath, "r") as file:
            for line in file:
                values.append(line.strip())  # Add the stripped line to the list of values
        return values
    # except FileNotFoundError:
    else:
        # print(f"File {filepath} does not exist in current directory.")
        return None  # Return None if the file is not found
        # return values


# Create filename variables for files
movies_in_stock = "movies_in_stock.txt"
add_to_stock = "add_to_stock.txt"
vgt = "vgt.txt"
vym = "vym.txt"

# Check for file:
find_movies_in_stock = find_file(movies_in_stock)
find_add_to_stock = find_file(add_to_stock)
find_vgt = find_file(vgt)
find_vym = find_file(vym)

# Read file:
stock = read_file(find_movies_in_stock)
titles_to_add = read_file(find_add_to_stock)
vym_tickers = read_file(find_vym)
vgt_tickers = read_file(find_vgt)

def main():
    if stock and titles_to_add is not None:
        print(f"These items from {add_to_stock} file ARE IN {movies_in_stock}:")
        for value in titles_to_add:
            if value in stock:
                print(value)
            
        print(f"\nThese items from {add_to_stock} are NOT in {movies_in_stock}, please ADD to PORTFOLIO:")
        for value in titles_to_add:
            if value not in stock:
                print(value)

    elif titles_to_add is None:
        print(f"File {add_to_stock} does not exist in current directory.")
    else:
        print(f"File {movies_in_stock} is not found in the working directory.")


main()
