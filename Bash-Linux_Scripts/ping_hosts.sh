#!/bin/bash

# Check if "inv.ini" file exists
if [ ! -e "inv.ini" ] && [ ! -e "inv.txt" ]; then
    echo "Error: Neither inv.ini nor inv.txt file found."
    exit 1
fi

# Use "inv.ini" if it exists; otherwise, use "inv.txt"
input_file="inv.ini"
if [ ! -e "inv.ini" ]; then
    input_file="inv.txt"
fi

# Loop through hosts in the chosen input file and perform ping tests
while read -r host; do
    # Check if the host name can be resolved
    if ! ping -c 1 "$host" &>/dev/null; then
        echo "$host: Unknown Host"
    else
        # Perform ping test three times
        if ping -c 3 "$host" &>/dev/null; then
            echo "$host: Ping OK"
        else
            echo "$host: Ping is Inconsistent"
        fi
    fi

    echo "--------------------------------------"
done < "$input_file"
