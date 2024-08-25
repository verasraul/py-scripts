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
        return f"An error occurred: {e.stderr}"

def git_pull():
    """Pull the latest changes for the denied.csv from the Git repository."""
    output = run_shell_command("git pull")
    print(output)  # Optionally, display the output in the GUI or log it.

def expand_fqdn_range(fqdn):
    """Expand FQDN patterns like varnish[09-11].voice.prod.co into a list of FQDNs."""
    match = re.search(r'\[(\d+)-(\d+)\]', fqdn)
    if match:
        start, end = int(match.group(1)), int(match.group(2))
        base = fqdn[:match.start()] + "{:0" + str(len(match.group(1))) + "d}" + fqdn[match.end():]
        return [base.format(i) for i in range(start, end + 1)]
    else:
        return [fqdn]

def submit_form():
    """Submit FQDNs and comments to denied.csv file."""
    fqdn_input = fqdn_text.get("1.0", tk.END).strip().split(',')
    comments = comments_text.get("1.0", tk.END).strip()
    
    # Expand FQDNs with ranges
    expanded_fqdns = []
    for fqdn in fqdn_input:
        expanded_fqdns.extend(expand_fqdn_range(fqdn.strip()))

    existing_fqdns = set()
    new_fqdns = []
    csv_file = "denied.csv"
    
    # Check if the FQDNs already exist in the file
    if os.path.isfile(csv_file):
        try:
            with open(csv_file, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header
                existing_fqdns = {row[0].strip().lower() for row in reader}
        except Exception as e:
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Error reading file: {e}")
            result_text.config(state='disabled')
            return

    # Separate new and existing FQDNs
    for fqdn in expanded_fqdns:
        if fqdn.lower() in existing_fqdns:
            continue
        else:
            new_fqdns.append((fqdn, comments))
    
    if new_fqdns:
        try:
            with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if os.path.getsize(csv_file) == 0:  # File is empty, write headers
                    writer.writerow(["FQDN", "Comments"])
                writer.writerows(new_fqdns)
            
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Successfully added {len(new_fqdns)} FQDN(s) to denied.csv.")
            
            # List the existing FQDNs
            if existing_fqdns:
                result_text.insert(tk.END, "\n\nThese FQDNs already exist:\n")
                for fqdn in expanded_fqdns:
                    if fqdn.lower() in existing_fqdns:
                        result_text.insert(tk.END, f"{fqdn}\n")
            
            result_text.config(state='disabled')
        except Exception as e:
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Error writing to file: {e}")
            result_text.config(state='disabled')
    else:
        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "No new FQDNs were added. All provided FQDNs already exist.")
        result_text.config(state='disabled')

def on_close():
    """Actions to perform when the GUI is closed."""
    commit_and_push()
    root.destroy()

def commit_and_push():
    """Commit and push the changes to the Git repository."""
    commands = [
        "git add denied.csv",
        "git commit -m 'Updated denied.csv with new FQDN entries'",
        "git push"
    ]
    for command in commands:
        output = run_shell_command(command)
        if "error" in output.lower():
            print(output)  # Display any errors encountered during the git operations

# -------------------- GUI Setup --------------------

root = tk.Tk()
root.title("Denied FQDN Manager")
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

# FQDN Input Section
fqdn_frame = ttk.LabelFrame(main_frame, text="Add FQDNs")
fqdn_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

fqdn_label = ttk.Label(fqdn_frame, text="Enter FQDN(s) (comma-separated):")
fqdn_label.pack(anchor=tk.W, pady=(5, 0))

fqdn_text = tk.Text(fqdn_frame, width=80, height=3, wrap=tk.WORD)
fqdn_text.pack(pady=5)

comments_label = ttk.Label(fqdn_frame, text="Comments:")
comments_label.pack(anchor=tk.W, pady=(5, 0))

comments_text = tk.Text(fqdn_frame, width=80, height=3, wrap=tk.WORD)
comments_text.pack(pady=5)

clear_add_button = ttk.Button(fqdn_frame, text="Clear Fields", command=clear_comments_and_fqdn)
clear_add_button.pack(side=tk.LEFT, padx=5, pady=5)

submit_button = ttk.Button(fqdn_frame, text="Submit", command=submit_form)
submit_button.pack(side=tk.RIGHT, padx=5, pady=5)

# Search and Remove Section
search_frame = ttk.LabelFrame(main_frame, text="Search / Remove FQDNs")
search_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

search_label = ttk.Label(search_frame, text="Search Pattern (supports wildcards '*', '?'):")
search_label.pack(anchor=tk.W, pady=(5, 0))

search_text = tk.Text(search_frame, width=80, height=2, wrap=tk.WORD)
search_text.pack(pady=5)

search_buttons_frame = ttk.Frame(search_frame)
search_buttons_frame.pack(fill=tk.X, pady=5)

search_button = ttk.Button(search_buttons_frame, text="Search", command=search_fqdn)
search_button.pack(side=tk.LEFT, padx=5)

remove_button = ttk.Button(search_buttons_frame, text="Remove", command=remove_fqdn)
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
