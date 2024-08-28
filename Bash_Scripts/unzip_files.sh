#!/bin/bash

# Prompt the user for a directory path
read -p "Enter the directory path: " directory_path

# Check if the directory exists
if [ ! -d "$directory_path" ]; then
    echo "Error: Directory does not exist."
    exit 1
fi

# Change to the specified directory
cd "$directory_path" || exit 1

# Loop through each zip file and unzip
for zip_file in *.zip; do
    unzip "$zip_file" -d "${zip_file%.zip}"
done

echo "Unzipping completed."

