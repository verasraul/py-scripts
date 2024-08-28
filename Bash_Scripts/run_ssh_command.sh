#!/bin/bash

# Check if "inv.ini" file exists
if [ ! -e "inv.ini" ]; then
    echo "Error: inv.ini file not found."
    exit 1
fi

# Loop through hosts in "inv.ini" and run the command
while read -r host; do
    echo "Running command on $host:"
    ssh "$host" "ip -4 -o a | grep -m 1 -i 'fe_bond0' | awk '{print \$2,\$4}'"
    echo "--------------------------------------"
done < "inv.ini"

