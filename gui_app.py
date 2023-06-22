from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import *
from simulator import Simulator
from tkinter import filedialog

def create_register_display():
    registers = simulator.registers

    
    register_frame = tk.Frame() # Create a frame to hold register labels
    register_frame.pack(side=tk.LEFT, fill=tk.Y) #pack inside main window

    # Create a canvas to hold register frame, and also a scrollbar
    canvas = tk.Canvas(register_frame)
    scrollbar = tk.Scrollbar(
        register_frame, orient=tk.VERTICAL, command=canvas.yview
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.Y)

    # configure canvas to work with scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) #ensures whenever the size or position of canvas changes, scrollable area is updated

    # Create a frame inside the canvas to hold the register labels
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    # Create a label for each register and its value
    for register, value in registers.items():
        label = tk.Label(inner_frame, text=f"{register}: {value}")
        label.pack(anchor=tk.W)  # west
        register_labels[register] = label

def update_register_display():
    registers = simulator.registers

    # Update the label for each register with its new value
    for register, value in registers.items():
        label = register_labels[register]
        label.config(text=f"{register}: {value}")

def open_file():
    # Function to open file
    file_path = filedialog.askopenfilename()

    if file_path: #file is selected
        system_output.config(text=f'Opening file {file_path}...')
        #do more
    
    else: #no file selected
        system_output.config(text = "No file selected")

def run_file(file_name = "default"):
    #function that runs file
    system_output.config(text=f'Running file {file_name}...')

def submit():
    user_input = user_input_box.get() #get the user input from entry box
    output = process_input(user_input)#Process input
    system_output.config(text=output) #update system output label with output

def process_input(user_input):
    #REPLACE WITH PROCESSING LOGIC
    return f'Processed input: {user_input}'

window = tk.Tk()
window.title("Project Blackbox")
window.geometry("800x800")
simulator = Simulator()  # create an instance of simulator
register_labels = {}
create_register_display()

accumulator_frame = tk.Frame(function_frame, background=win_style.primarycolor) #Frame containing the accumulator display
accumulator_frame.pack(side="top", pady=(20,0))

accumulator_label = tk.Label(accumulator_frame, text="Accumulator: ", font=("Arial", 20), bg=win_style.primarycolor) #Accumulator title
accumulator_label.pack(side="left")
accumulator_box = tk.Entry(accumulator_frame, font=("Arial", 20), width=8, bg=win_style.primarycolor) #Accumulator display
accumulator_box.pack(side="right")

accumulator_box.insert(END, insta.accumulator) #Populates the accumulator
accumulator_box['state'] = 'readonly'

input_frame = tk.Frame(function_frame, bg=win_style.primarycolor) #Frame containing console and user input
input_frame.pack(side='top')

console_label = tk.Label(input_frame, text="Console:", font=("Arial", 10), bg=win_style.primarycolor) #Console title
console_label.pack(side='top', padx = 20, pady = (10, 5), anchor="w")
console_box = tk.Text(input_frame, state='disabled', wrap="word", height=18) #Console box
console_box.pack(side='top', anchor='ne', padx = 20, pady = (0, 20))

input_label = tk.Label(input_frame, text="User input:", font=("Arial", 10), bg=win_style.primarycolor) #Input title
input_label.pack(padx = 20, pady = (0, 10))
input_box = tk.Entry(input_frame, font=("Arial", 15), state="disabled") #Input box
input_box.pack(pady = (0, 10))
submit_input = tk.Button(input_frame, text="Submit Input", font=("Arial", 10), state='disabled', command=sim_op.submit_input, fg='black', bg=win_style.offcolor) #Input submit button
submit_input.pack(pady = (0, 10))

user_messages = tk.Label(input_frame, font=("Arial", 15), text="Load instructions to execute.", wraplength="400", bg=win_style.primarycolor) #Text for messages directed to the user.
user_messages.pack(pady=(5, 10))

button_frame = tk.Frame(function_frame, background=win_style.primarycolor) #Frame containing all the buttons
button_frame.pack(side='bottom', anchor='c', fill='y', pady=(0, 70))

open_file_btn = tk.Button(button_frame, text="Load Instructions", font=("Courier", 20), command=sub_windows.load_instructions, border=5, width=20, bg=win_style.offcolor, fg='black') #Button to open file
open_file_btn.pack(side='top', pady=(0, 10))
run_btn = tk.Button(button_frame, font=("Courier", 20), command=sim_op.run_cancel_control, text="Run", border=5, width=20, bg=win_style.offcolor, fg='black') #Button to run and cancel the program execution, can use disabledforeground to make text more readable in needed
run_btn.pack(side='bottom', pady=(10, 0))

window.mainloop() #Triggers the GUI initialization
