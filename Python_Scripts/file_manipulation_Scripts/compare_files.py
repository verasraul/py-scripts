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

def compare_files(fqdns_values, list_values):
    # Print values that are in fqdns.txt but not in list.txt
    print("Add the following:")
    for fqdn in fqdns_values:
        if fqdn not in list_values:
            print(f"- {fqdn}")

    # Print values that are in both files
    print("\nDo not add the following:")
    for fqdn in fqdns_values:
        if fqdn in list_values:
            print(f"- {fqdn}")

# Read content of list.txt and fqdns.txt
list_values = read_list_file('list.txt')
fqdns_values = read_list_file('fqdns.txt')

# Compare values between the two files
if list_values and fqdns_values:
    compare_files(list_values, fqdns_values)