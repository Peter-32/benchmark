import subprocess
import sys
from glob import glob
import tqdm
import tkinter as tk
from tkinter import ttk, messagebox








import tkinter as tk
from tkinter import ttk, messagebox

# 1. Your actual main logic function
def my_main_function(replay_path, player_name):
    all_files = glob("*.py")
    files_of_interest = [y for (x, y) in sorted([(str(x.split("_")[0]).zfill(2), x) for x in all_files]) if 'get_data' not in y and 'pro' not in y and y not in ['main.py', 'utils.py']]
    subprocess.run([sys.executable, '1_get_data.py', replay_path, player_name])
    for script_name in tqdm.tqdm(files_of_interest):
        print(script_name)
        subprocess.run([sys.executable, script_name])

# 2. Wrapper function triggered when the GUI button is pressed
def on_button_click():
    # Retrieve text values from the input fields
    val1 = entry1.get()
    val2 = entry2.get()
    
    # Input validation check
    if not val1 or not val2:
        messagebox.showwarning("Input Error", "Please fill in both parameters.")
        return
    
    # Call your main function and capture the output
    try:
        result = my_main_function(val1, val2)
        result_label.config(text=f"Result: {result}")
    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred: {e}")

# 3. Build the GUI layout
root = tk.Tk()
root.title("Python Function Runner")
root.geometry("350x220")
root.resizable(False, False)

# Form Layout using grid
tk.Label(root, text="Parameter 1:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry1 = ttk.Entry(root, width=25)
entry1.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Parameter 2:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry2 = ttk.Entry(root, width=25)
entry2.grid(row=1, column=1, padx=10, pady=10)

# Action Button
action_btn = ttk.Button(root, text="Run Main Function", command=on_button_click)
action_btn.grid(row=2, column=0, columnspan=2, pady=15)

# Status/Result Label
result_label = tk.Label(root, text="Result: Waiting for input...", fg="gray")
result_label.grid(row=3, column=0, columnspan=2, pady=5)

# Start the application loop
root.mainloop()