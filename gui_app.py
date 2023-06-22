import tkinter as tk
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

'''GUI RENDERING'''

window = tk.Tk()
window.title("Project Blackbox")
window.geometry("800x800")

simulator = Simulator()  # create an instance of simulator
register_labels = {}
create_register_display()

bottom_right_frame = tk.Frame(width=400, height=200) #create bottom right frame

open_file_button = tk.Button(
    bottom_right_frame, text="Open File", command=open_file #packing open file button into the bottom right frame, it calls open_file when clicked
)
open_file_button.pack(side=tk.BOTTOM, padx=10, pady=10) 

run_file_button = tk.Button(
    bottom_right_frame, text="Run File", command=run_file #packed run file button into bottom right frame. calls run_file when clicked.
)
run_file_button.pack(side=tk.BOTTOM, padx=10, pady=10)

bottom_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

top_right_frame = tk.Frame(width = 400, height = 200) #create top right frame
top_right_frame.pack(side=tk.RIGHT, fill = tk.BOTH, padx=10, pady=10)

input_label = tk.Label(top_right_frame, text = "INPUT") #make input label, pack it in top right frame
input_label.pack(padx=10,pady=5) #pack input lable into main window

user_input_box = tk.Entry(top_right_frame) #make user input entry , pack into top right frame
user_input_box.pack(padx=10, pady=10) #Pack into main window

submit_user_input_button = tk.Button(top_right_frame, text="SUBMIT", command=submit)
submit_user_input_button.pack(padx=10, pady=5)

system_output = tk.Label(top_right_frame, text = "OUTPUT") #create output label packed into top right frame
system_output.pack(padx=10, pady=10) #pack into main window


window.mainloop()