import tkinter as tk
from tkinter import ttk
import csv
import os
import fnmatch
import re

def expand_fqdn_range(fqdn):
    """Convert FQDN range [01-11] patterns into a list of FQDNs."""
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
    
    # List FQDNs with ranges
    expanded_fqdns = []
    for fqdn in fqdn_input:
        expanded_fqdns.extend(expand_fqdn_range(fqdn.strip()))

    existing_fqdns = set()
    new_fqdns = []
    csv_file = "denied.csv"
    
    # Check if the FQDNs already exist
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

def search_fqdn():
    """Search for FQDNs with wildcard."""
    search_pattern = search_text.get("1.0", tk.END).strip().lower()
    csv_file = "denied.csv"
    
    if search_pattern:
        if os.path.isfile(csv_file):
            matches = []
            try:
                with open(csv_file, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    next(reader, None)  # Skip header
                    for row in reader:
                        fqdn = row[0].strip().lower()
                        comment = row[1].strip()
                        if fnmatch.fnmatch(fqdn, search_pattern):
                            matches.append(f"FQDN: {row[0]}, Comments: {comment}")
                
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
            result_text.insert(tk.END, "The denied.csv file does not exist.")
            result_text.config(state='disabled')
    else:
        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please enter a search pattern.")
        result_text.config(state='disabled')

def remove_fqdn():
    """Remove FQDNs with wildcard pattern."""
    search_pattern = search_text.get("1.0", tk.END).strip().lower()
    csv_file = "denied.csv"
    
    if search_pattern:
        if os.path.isfile(csv_file):
            updated_rows = []
            removed_entries = []
            try:
                with open(csv_file, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    headers = next(reader, None)
                    for row in reader:
                        fqdn = row[0].strip().lower()
                        if fnmatch.fnmatch(fqdn, search_pattern):
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
                    result_text.insert(tk.END, f"Removed {len(removed_entries)} FQDN(s) matching '{search_pattern}'.")
                else:
                    result_text.insert(tk.END, f"No FQDNs matching '{search_pattern}' were found to remove.")
                result_text.config(state='disabled')
            except Exception as e:
                result_text.config(state='normal')
                result_text.delete("1.0", tk.END)
                result_text.insert(tk.END, f"Error processing file: {e}")
                result_text.config(state='disabled')
        else:
            result_text.config(state='normal')
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "The denied.csv file does not exist.")
            result_text.config(state='disabled')
    else:
        result_text.config(state='normal')
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please enter a pattern to remove.")
        result_text.config(state='disabled')

def clear_comments_and_fqdn():
    """Clear both FQDN and Comments text fields."""
    fqdn_text.delete("1.0", tk.END)
    comments_text.delete("1.0", tk.END)

def clear_search():
    """Clear the Search text field."""
    search_text.delete("1.0", tk.END)

def clear_result():
    """Clear the Result text field."""
    result_text.config(state='normal')
    result_text.delete("1.0", tk.END)
    result_text.config(state='disabled')

# -------------------- GUI Setup --------------------

root = tk.Tk()
root.title("Removed FQDNs")
root.geometry("700x700")
root.resizable(False, False)

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

fqdn_label = ttk.Label(fqdn_frame, text="FQDN(s) (comma-separated):")
fqdn_label.pack(anchor=tk.W, pady=(5, 0))

fqdn_text = tk.Text(fqdn_frame, width=80, height=5, wrap=tk.WORD)
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
