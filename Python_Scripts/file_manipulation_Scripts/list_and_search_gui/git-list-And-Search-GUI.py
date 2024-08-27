import tkinter as tk
from tkinter import ttk
import csv
import os
import fnmatch
import re
import subprocess

def run_shell_command(command):
    """Run shell commands and capture output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"

def git_pull():
    """Pull the latest changes for the list.csv from the Git repository."""
    output = run_shell_command("git pull")
    print(output)  # Optionally, display the output in the GUI or log it.

# def git_fetch():
#     """Fetch changes from the upstream repo and merge them into the local main branch."""
#     fetch_command = "git fetch upstream"
#     merge_command = "git merge upstream/main"
#     fetch_result = run_shell_command(fetch_command)
#     merge_result = run_shell_command(merge_command)
#     print(fetch_result)  # Optionally display the fetch result in the GUI or log it.
#     print(merge_result)

def expand_itemName_range(itemName):
    """Expand itemName patterns like varnish[09-11].voice.prod.co into a list of itemNames."""
    match = re.search(r'\[(\d+)-(\d+)\]', itemName)
    if match:
        start, end = int(match.group(1)), int(match.group(2))
        base = itemName[:match.start()] + "{:0" + str(len(match.group(1))) + "d}" + itemName[match.end():]
        return [base.format(i) for i in range(start, end + 1)]
    else:
        return [itemName]

def submit_form():
    """Submit itemNames and comments to list.csv file."""
    itemName_input = itemName_text.get("1.0", tk.END).strip().split(',')
    comments = comments_text.get("1.0", tk.END).strip()
    
    # Expand itemNames with ranges
    expanded_itemNames = []
    for itemName in itemName_input:
        expanded_itemNames.extend(expand_itemName_range(itemName.strip()))

    existing_itemNames = set()
    new_itemNames = []
    csv_file = "list.csv"
    
    # Check if the itemNames already exist in the file
    if os.path.isfile(csv_file):
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header
                existing_itemNames = {row[0].strip().lower() for row in reader}
        except Exception as e:
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Error reading file: {e}")
            result_text.config(state='disabled')
            return

    # Separate new and existing itemNames
    for itemName in expanded_itemNames:
        if itemName.lower() in existing_itemNames:
            continue
        else:
            new_itemNames.append((itemName, comments))
    
    if new_itemNames:
        try:
            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if os.path.getsize(csv_file) == 0:  # File is empty, write headers
                    writer.writerow(["itemName", "Comments"])
                writer.writerows(new_itemNames)
            
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Successfully added {len(new_itemNames)} itemName(s) to list.csv.")
            
            # List the existing itemNames
            if existing_itemNames:
                result_text.insert(tk.END, "\n\nThese itemNames already exist:\n")
                for itemName in expanded_itemNames:
                    if itemName.lower() in existing_itemNames:
                        result_text.insert(tk.END, f"{itemName}\n")
            
            result_text.config(state='disabled')
        except Exception as e:
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Error writing to file: {e}")
            result_text.config(state='disabled')
    else:
        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "No new itemNames were added. All provided itemNames already exist.")
        result_text.config(state='disabled')

def search_itemName():
    """Search for itemNames matching the wildcard pattern."""
    search_pattern = search_text.get("1.0", tk.END).strip().lower()
    csv_file = "list.csv"
    
    if search_pattern:
        if os.path.isfile(csv_file):
            matches = []
            try:
                with open(csv_file, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        itemName = row[0].strip().lower()
                        comment = row[1].strip()
                        if fnmatch.fnmatch(itemName, search_pattern):
                            matches.append(f"itemName: {row[0]}, Comments: {comment}")
                
                result_text.config(state='normal')
                result_text.delete("1.0", tk.END)
                if matches:
                    result_text.insert(tk.END, f"Found {len(matches)} match(es):\n\n")
                    result_text.insert(tk.END, "\n".join(matches))
                else:
                    result_text.insert(tk.END, f"No matches found for pattern '{search_pattern}'.")
                result_text.config(state='disabled')
            except Exception as e:
                result_text.config(state='normal')
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, f"Error reading file: {e}")
                result_text.config(state='disabled')
        else:
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "The list.csv file does not exist.")
            result_text.config(state='disabled')
    else:
        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please enter a search pattern.")
        result_text.config(state='disabled')

def remove_itemName():
    """Remove itemNames matching the wildcard pattern from list.csv."""
    search_pattern = search_text.get("1.0", tk.END).strip().lower()
    csv_file = "list.csv"
    
    if search_pattern:
        if os.path.isfile(csv_file):
            updated_rows = []
            removed_entries = []
            try:
                with open(csv_file, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    headers = next(reader, None)
                    for row in reader:
                        itemName = row[0].strip().lower()
                        if fnmatch.fnmatch(itemName, search_pattern):
                            removed_entries.append(row)
                        else:
                            updated_rows.append(row)
                
                with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if headers:
                        writer.writerow(headers)
                    writer.writerows(updated_rows)
                
                result_text.config(state='normal')
                result_text.delete("1.0", tk.END)
                if removed_entries:
                    result_text.insert(tk.END, f"Removed {len(removed_entries)} itemName(s) matching '{search_pattern}'.")
                else:
                    result_text.insert(tk.END, f"No itemNames matching '{search_pattern}' were found to remove.")
                result_text.config(state='disabled')
            except Exception as e:
                result_text.config(state='normal')
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, f"Error processing file: {e}")
                result_text.config(state='disabled')
        else:
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "The list.csv file does not exist.")
            result_text.config(state='disabled')
    else:
        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please enter a pattern to remove.")
        result_text.config(state='disabled')

def clear_comments_and_itemName():
    """Clear both itemName and Comments text fields."""
    itemName_text.delete("1.0", tk.END)
    comments_text.delete("1.0", tk.END)

def clear_search():
    """Clear the Search text field."""
    search_text.delete("1.0", tk.END)

def clear_result():
    """Clear the Result text field."""
    result_text.config(state='normal')
    result_text.delete("1.0", tk.END)
    result_text.config(state='disabled')

def on_close():
    """Actions to perform when the GUI is closed."""
    commit_and_push()
    root.destroy()

def commit_and_push():
    """Commit and push the changes to the Git repository."""
    add_command = "git add list.csv"
    commit_command = "git commit -m 'Updated list'"
    push_command = "git push"
    add_result = run_shell_command(add_command)
    commit_result = run_shell_command(commit_command)
    push_result = run_shell_command(push_command)
    print(add_result)
    print(commit_result)
    print(push_result)
    # commands = [
    #     "git add list.csv",
    #     "git commit -m 'Updated list.csv with new itemName entries'",
    #     "git push"
    # ]
    # for command in commands:
    #     output = run_shell_command(command)
    #     if "error" in output.lower():
    #         print(output)  # Display any errors encountered during the git operations

# -------------------- GUI Setup --------------------

root = tk.Tk()
root.title("Item Listing Manager")
root.geometry("700x700")
root.resizable(False, False)

# Initialize and pull changes at startup
git_pull()

# Bind the close event to the on_close function
root.protocol("WM_DELETE_WINDOW", on_close)

# Style Configuration
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 10))
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TFrame', padding=10)

# Main Frame
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# itemName Input Section
itemName_frame = ttk.LabelFrame(main_frame, text="Add itemNames")
itemName_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

itemName_label = ttk.Label(itemName_frame, text="Enter itemName(s) (comma-separated):")
itemName_label.pack(anchor=tk.W, pady=(5, 0))

itemName_text = tk.Text(itemName_frame, width=80, height=3, wrap=tk.WORD)
itemName_text.pack(pady=5)

comments_label = ttk.Label(itemName_frame, text="Comments:")
comments_label.pack(anchor=tk.W, pady=(5, 0))

comments_text = tk.Text(itemName_frame, width=80, height=3, wrap=tk.WORD)
comments_text.pack(pady=5)

clear_add_button = ttk.Button(itemName_frame, text="Clear Fields", command=clear_comments_and_itemName)
clear_add_button.pack(side=tk.LEFT, padx=5, pady=5)

submit_button = ttk.Button(itemName_frame, text="Submit", command=submit_form)
submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Search and Remove Section
search_frame = ttk.LabelFrame(main_frame, text="Search / Remove itemNames")
search_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

search_label = ttk.Label(search_frame, text="Search Pattern (supports wildcards '*', '?'):")
search_label.pack(anchor=tk.W, pady=(5, 0))

search_text = tk.Text(search_frame, width=80, height=2, wrap=tk.WORD)
search_text.pack(pady=5)

search_buttons_frame = ttk.Frame(search_frame)
search_buttons_frame.pack(fill=tk.X, pady=5)

search_button = ttk.Button(search_buttons_frame, text="Search", command=search_itemName)
search_button.pack(side=tk.LEFT, padx=5)

remove_button = ttk.Button(search_buttons_frame, text="Remove", command=remove_itemName)
remove_button.pack(side=tk.LEFT, padx=5)

clear_search_button = ttk.Button(search_buttons_frame, text="Clear Search", command=clear_search)
clear_search_button.pack(side=tk.LEFT, padx=5)

# Result Section
result_frame = ttk.LabelFrame(main_frame, text="Result")
result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

result_text = tk.Text(result_frame, width=80, height=10, wrap=tk.WORD, state='disabled')
result_text.pack(pady=5)

clear_result_button = ttk.Button(result_frame, text="Clear Result", command=clear_result)
clear_result_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Start the main event loop
root.mainloop()
