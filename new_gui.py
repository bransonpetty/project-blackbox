# Python program to illustrate the usage of
# treeview scrollbars using tkinter


from tkinter import ttk
import tkinter as tk
from simulator import Simulator

insta = Simulator()

registers = insta.registers

# Creating tkinter window
window = tk.Tk()
window.geometry("800x800")
window.resizable(width = 1, height = 1)

register_frame = ttk.Frame(window, border=20)
register_frame.pack(fill='y', side=tk.LEFT)

# Using treeview widget
reg_table = ttk.Treeview(register_frame, selectmode ='browse', padding=2)

# Calling pack method w.r.to treeview
reg_table.pack(side ='left', fill="y")

# Constructing vertical scrollbar
# with treeview
reg_scroll = ttk.Scrollbar(register_frame,
						orient =tk.VERTICAL,
						command = reg_table.yview)

# Calling pack method w.r.to vertical
# scrollbar
reg_scroll.pack(side ='right', fill ="y")

# Configuring treeview
reg_table.configure(yscrollcommand = reg_scroll.set)

# Defining number of columns
reg_table["columns"] = ("1", "2")

# Defining heading
reg_table['show'] = 'headings'

# Assigning the width and anchor to the
# respective columns
reg_table.column("1", width = 60, anchor ='c')
reg_table.column("2", width = 300, anchor ='c')

# Assigning the heading names to the
# respective columns
reg_table.heading("1", text ="Register")
reg_table.heading("2", text ="Value")

# Inserting the items and their features to the
# columns built
for register, value in registers.items():
    reg_table.insert("", 'end', text ="L1",
                values =(register, value))

function_frame = tk.Frame(window)
function_frame.pack(side='right', fill='y')
    
console_box = tk.Text(function_frame, state='disabled')
console_box.pack(side='top', anchor='ne', padx = 20, pady = 20)

button_frame = tk.Frame(function_frame)
button_frame.pack(side='bottom', anchor='c', pady=140)

open_file_btn = tk.Button(button_frame, text="Open File").grid(row=0, column=0, padx=10, pady=10)
#open_file_btn.grid(row=0, column=0, padx=10, pady=10)
run_btn = tk.Button(button_frame, text="Run").grid(row=1, column=0, padx=10, pady=10)
#run_btn.grid(row=1, column=0, padx=10, pady=10)

# Calling mainloop
window.mainloop()
