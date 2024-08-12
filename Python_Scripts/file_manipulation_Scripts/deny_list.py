#!/usr/bin/env python3
'''
Deny List Tool

User Experience:
- User fills text file.
- Compare text file against deny list.
- Report on which hosts are denied.
- Report on which hosts to add.
'''
import os

def read_file(filename):
    # Get the current working directory:
    current_directory = os.getcwd()

    # Search for a file by specified name (ie. 'inventory.txt'):
    file_found = False 
    # Create a boolean variable to set to 'True' if file is found.
    for file in os.listdir(current_directory): 
        # Loop through the current directory.
        if file.endswith(".txt") and file == filename: 
            # Verify the files is a .txt file and matches 'deniedList' provided.
            file_found = True 
            # If file is found, change boolean variable to True.
            file_path = os.path.join(current_directory, file) 
            # Set the file-path to the file.
            break
    
    if file_found:
        values = []
        with open(file_path, "r") as file:
            for line in file:
                values.append(line.strip())
        return values
    else:
        return None
    
# Specify filename/s in a variable:
deniedList = "deniedList.txt"
inventoryList = "inventoryList.txt"

# Check for file/s using 'read_file' function:
denied = read_file(deniedList)
inventory = read_file(inventoryList)

if denied is not None:
    print(f"These hosts are IN {deniedList} DO NOT ADD:")
    for value in inventory:
        if value in denied:
            print(value)

    print(f"\nThese hosts are NOT in {deniedList} PLEASE ADD TO MONITORING:")
    for value in inventory:
        if value not in denied:
            print(value)

else:
    print("File not found in the current directory.")