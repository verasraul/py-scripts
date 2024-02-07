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
        # Perform ping test and count successful responses
        ping_result=$(ping -c 5 "$host" 2>&1)
        successful_pings=$(echo "$ping_result" | grep -oE "[0-9]+ received" | cut -d' ' -f1)

        # Check if at least 3 pings are successful
        if [ "$successful_pings" -ge 3 ]; then
            echo "$host: Ping OK"
        else
            # Check if the host is unreachable
            if echo "$ping_result" | grep -q "100% packet loss"; then
                echo "$host: Unreachable..."
            else
                echo "$host: Ping is Inconsistent"
            fi
        fi
    fi

    echo "--------------------------------------"
done < "$input_file"

