from tkinter import ttk
import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import *
from simulator import Simulator
from tkinter import filedialog

#window = tk.Tk()
class GUI(tk.Tk):
    def __init__(self):
        super().__init__() 
        self.title("Project Blackbox")
        self.geometry("800x800")
        self.simulator = Simulator()  # create an instance of simulator
        self.register_labels = {}
        
        self.register_frame = tk.Frame(self) # Create a frame to hold register labels
        self.register_frame.pack(side=tk.LEFT, fill=tk.Y) #pack inside main window

        # Create a canvas to hold register frame, and also a scrollbar
        self.canvas = tk.Canvas(self.register_frame)
        self.inner_frame = tk.Frame(self.canvas)
        self.create_register_display()

        bottom_right_frame = tk.Frame(self, width=400, height=200) #create bottom right frame

        self.open_file_button = tk.Button(
            bottom_right_frame, text="Open File", command=self.open_file #packing open file button into the bottom right frame, it calls open_file when clicked
        )
        self.open_file_button.pack(side=tk.BOTTOM, padx=10, pady=10) 

        self.run_file_button = tk.Button(
            bottom_right_frame, text="Run File", command=self.run_file #packed run file button into bottom right frame. calls run_file when clicked.
        )
        self.run_file_button.pack(side=tk.BOTTOM, padx=10, pady=10)

        bottom_right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

        top_right_frame = tk.Frame(self, width = 400, height = 200) #create top right frame
        top_right_frame.pack(side=tk.RIGHT, fill = tk.BOTH, padx=10, pady=10)

        input_label = tk.Label(top_right_frame, text = "INPUT") #make input label, pack it in top right frame
        input_label.pack(padx=10,pady=5) #pack input lable into main window

        self.user_input_box = tk.Entry(top_right_frame) #make user input entry , pack into top right frame
        self.user_input_box.pack(padx=10, pady=10) #Pack into main window

        submit_user_input_button = tk.Button(top_right_frame, text="SUBMIT", command=self.submit)
        submit_user_input_button.pack(padx=10, pady=5)

        self.system_output = tk.Label(top_right_frame, text = "OUTPUT") #create output label packed into top right frame
        self.system_output.pack(padx=10, pady=10) #pack into main window


    def create_register_display(self):
        registers = self.simulator.registers
        scrollbar = tk.Scrollbar(
            self.register_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.Y)

        # configure canvas to work with scrollbar
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))) #ensures whenever the size or position of canvas changes, scrollable area is updated

        # Create a frame inside the canvas to hold the register labels
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Create a label for each register and its value
        self.update_register_display()

    def update_register_display(self):
        registers = self.simulator.registers

        # Update the label for each register with its new value
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        # Create a label for each register and its value
        for register, value in registers.items():
            # reg_frame_1 = tk.Frame(self.inner_frame)
            # reg_frame_1.grid(row=int(register), column=0, sticky="NSEW")
            # reg_label_1 = tk.Label(master=reg_frame_1, text=f"{register}")
            # reg_label_1.pack()
            # reg_frame_2 = tk.Frame(self.inner_frame)
            # reg_frame_2.grid(row=int(register), column=1, sticky="NSEW")
            # reg_label_2 = tk.Label(master=reg_frame_2, text=f"{value}")
            # reg_label_2.pack()
            label = tk.Label(self.inner_frame, text=f"{register}: {value}")
            label.pack(anchor=tk.W)  # west
            self.register_labels[register] = label

    def open_file(self):
        # Function to open file
        file_path = filedialog.askopenfilename()

        if file_path: #file is selected
            self.system_output.config(text=f'Opening file {file_path}...')
            error = False
            with open(file_path) as input_file:
                addr = 0 
                for line in input_file:
                    line = line.strip()
                    #make sure its a + or a -
                    if len(line) == 5:
                        self.simulator.registers[addr] = line
                    elif line == "-99999":
                        break
                    else:
                        self.system_output.config(text=f'Error: {line} in your file is not a valid instruction.')
                        error = True
                    addr += 1
            if not error:
                for widgets in self.inner_frame.winfo_children():
                    widgets.destroy()
                self.register_frame = tk.Frame(self) # Create a frame to hold register labels
                self.register_frame.pack(side=tk.LEFT, fill=tk.Y) #pack inside main window
                self.update_register_display()
            #do more
        
        else: #no file selected
            self.system_output.config(text = "No file selected")

    def submit(self):
        user_input = self.user_input_box.get() #get the user input from entry box
        output = self.process_input(user_input)#Process input
        self.system_output.config(text=output) #update system output label with output

    def process_input(self, user_input):
        #REPLACE WITH PROCESSING LOGIC
        return f'Processed input: {user_input}'

if __name__ == "__main__":
    gui = GUI()
    gui.update_register_display()  # Start the update loop
    gui.mainloop()
