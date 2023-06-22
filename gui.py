import tkinter as tk
from main import Simulator
from tkinter import filedialog

class GUI(tk.Tk):
    def __init__(self):
        super().__init__() 
        self.title("Project Blackbox")
        self.geometry("800x800")
        self.simulator = Simulator()  # create an instance of simulator
        self.register_labels = {}
        self.create_register_display()

        bottom_right_frame = tk.Frame(self, width=400, height=200) #create bottom right frame

        self.open_file_button = tk.Button(
            bottom_right_frame, text="Open File", command=self.open_file #packing open file button into the bottom right frame, it calls open_file when clicked
        )
        self.open_file_button.pack(side=tk.BOTTOM, padx=10, pady=10) 

        self.run_file_button = tk.Button(
            bottom_right_frame, text="RUN FILE", command=self.run_file #packed run file button into bottom right frame. calls run_file when clicked.
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

     
        register_frame = tk.Frame(self) # Create a frame to hold register labels
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
            self.register_labels[register] = label

    def update_register_display(self):
        registers = self.simulator.registers

        # Update the label for each register with its new value
        for register, value in registers.items():
            label = self.register_labels[register]
            label.config(text=f"{register}: {value}")

        # Schedule the next update
        self.after(1000, self.update_register_display)

    def open_file(self):
        # Function to open file
        file_path = filedialog.askopenfilename()

        if file_path: #file is selected
            self.system_output.config(text=f'Opening file {file_path}...')
            #do more
        
        else: #no file selected
            self.system_output.config(text = "No file selected")
        

    def run_file(self, file_name = "default"):
        #function that runs file
        self.system_output.config(text=f'Running file {file_name}...')

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
