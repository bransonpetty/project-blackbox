import tkinter as tk
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
        
        else: #no file selected
            self.system_output.config(text = "No file selected")

    def submit(self):
        user_input = self.user_input_box.get() #get the user input from entry box
        output = self.process_input(user_input)#Process input
        self.system_output.config(text=output) #update system output label with output

    def process_input(self, user_input):
        #REPLACE WITH PROCESSING LOGIC
        return f'Processed input: {user_input}'
    
    def run_file(self, file_name = "default"):
        #function that runs file
        self.system_output.config(text=f'Running file {file_name}...')
        self.run()
        
    def run(self):
        '''Runs each line of the simulator and calls the controller for the appropriate instructions'''
        choice = True #Stops while loop if user aborts or halts
        while self.simulator.cur_addr < 100 and choice:
            choice = self.controller(self.simulator.registers[self.simulator.cur_addr][1:3], self.simulator.registers[self.simulator.cur_addr][3:]) #Sends instruction code and address to controller
            self.simulator.cur_addr += 1 #Moves to next address
        return
    
    def controller(self, instruction, addr):
        '''It directs the simulator along with the desired address to the appropriate function based on the instruction'''
        choice = True #True or false is returned by every function and stored in "choice" variable in order to determine if the program should continue or not.
        if instruction not in self.simu_instance.instructions: #If it's not a valid instruction, it either ends the program or continues from the next instruction
            choice = self.simu_instance.invalid_instruction(instruction)
        elif instruction == "00":
            choice = True
        elif instruction == "10":
            choice = self.format_read(addr)
        elif instruction == "11":
            choice = self.console_write(addr)
        elif instruction == "20":
            choice = self.simulator.load(addr)
        elif instruction == "21":
            choice = self.simulator.store(addr)
        elif instruction == "30":
            choice = self.simulator.add(addr)
        elif instruction == "31":
            choice = self.simulator.subtract(addr)
        elif instruction == "32":
            choice = self.simulator.divide(addr)
        elif instruction == "33":
            choice = self.simulator.multiply(addr)
        elif instruction == "40":
            choice = self.simulator.branch(addr)
        elif instruction == "41":
            choice = self.simulator.branch_neg(addr)
        elif instruction == "42":
            choice = self.simulator.branch_zero(addr)
        elif instruction == "43":
            choice = self.simulator.halt()

        return choice

if __name__ == "__main__":
    gui = GUI()
    gui.mainloop()
