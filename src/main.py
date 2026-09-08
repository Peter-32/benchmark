import subprocess
import sys
from glob import glob
import tqdm
import tkinter as tk
from tkinter import ttk, messagebox
import os
import json

def load_saved_params():
    if os.path.exists('config.json'):
        try:
            with open('config.json', "r") as f:
                return json.load(f)
        except Exception:
            pass  # Fallback to empty defaults if file reading fails
    return {"param1": "", "param2": ""}

def save_params(val1, val2):
    try:
        with open('config.json', "w") as f:
            json.dump({"param1": val1, "param2": val2}, f, indent=4)
    except Exception as e:
        print(f"Failed to save preferences: {e}")

def my_main_function(replay_path, player_name):
    all_files = glob("*.py")
    files_of_interest = [y for (x, y) in sorted([(str(x.split("_")[0]).zfill(2), x) for x in all_files]) if 'get_data' not in y and 'pro' not in y and y not in ['main.py', 'utils.py']]
    subprocess.run([sys.executable, '1_get_data.py', replay_path, player_name])
    for script_name in tqdm.tqdm(files_of_interest):
        print(script_name)
        subprocess.run([sys.executable, script_name])

def on_button_click():
    val1 = entry1.get()
    val2 = entry2.get()
    
    # Input validation check
    if not val1 or not val2:
        messagebox.showwarning("Input Error", "Please fill in both parameters.")
        return

    save_params(val1, val2)
    
    try:
        result = my_main_function(val1, val2)
        result_label.config(text=f"Result: {result}")
    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Python Function Runner")
root.geometry("350x220")
root.resizable(False, False)

saved_data = load_saved_params()

tk.Label(root, text="Path to Replays:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry1 = ttk.Entry(root, width=25)
entry1.grid(row=0, column=1, padx=10, pady=10)
entry1.insert(0, saved_data.get("param1", ""))

tk.Label(root, text="Your Player Name:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry2 = ttk.Entry(root, width=25)
entry2.grid(row=1, column=1, padx=10, pady=10)
entry1.insert(0, saved_data.get("param2", ""))

action_btn = ttk.Button(root, text="Compute Benchmarks", command=on_button_click)
action_btn.grid(row=2, column=0, columnspan=2, pady=15)

result_label = tk.Label(root, text="Result: Waiting for input...", fg="gray")
result_label.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()