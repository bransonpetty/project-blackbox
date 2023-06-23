from tkinter import ttk
import tkinter as tk
from simulator import Simulator
from tkinter import filedialog
from tkinter import *

class GUI_Controller:
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=(("Text File (*.txt)", "*.txt"),))

        error = False
        if file_path:
            with open(file_path) as input_file:
                addr = 0 
                for line in input_file:
                    line = line.strip()
                    #make sure its a + or a -
                    if len(line) == 5:
                        insta.registers[addr] = line
                    elif line == "-99999":
                        break
                    else:
                        user_messages.config(text=f'Error: {line} in your file is not a valid instruction.')
                        error = True
                    addr += 1
                
            if not error:
                self.clear_table()
                self.update_table()
            
            user_messages.config(text="File successfully loaded.")

    def clear_table(self):
        for item in reg_table.get_children():
                    reg_table.delete(item)

    def update_table(self):
        for register, value in registers.items():
            reg_table.insert("", 'end', text ="L1",
                        values =(register, value))


class Simulator_Controller:

    def __init__(self):
        self.current_addr = ''
     
    def run_cancel_control(self):
            #function that runs file
            if run_btn["text"] == 'Run':
                open_file_btn['state'] = tk.DISABLED
                run_btn['text'] = "Cancel"
                user_messages.config(text=f'Executing program...')
                self.run()
            else:
                window.destroy()
       
    def run(self):
        '''Runs each line of the simulator and calls the controller for the appropriate instructions'''
        choice = True #Stops while loop if user aborts or halts
        while insta.cur_addr < 100 and choice:
            choice = self.controller(insta.registers[insta.cur_addr][1:3], insta.registers[insta.cur_addr][3:]) #Sends instruction code and address to controller
            insta.cur_addr += 1 #Moves to next address
        return

    def controller(self, instruction, addr):
        '''It directs the simulator along with the desired address to the appropriate function based on the instruction'''
        choice = True #True or false is returned by every function and stored in "choice" variable in order to determine if the program should continue or not.
        if instruction not in insta.instructions: #If it's not a valid instruction, it either ends the program or continues from the next instruction
            user_messages.config(text=f"{instruction} instruction on address {addr} is invalid. Program was halted.")
            insta.halt()
            choice = False
        elif instruction == "00":
            choice = True
        elif instruction == "10":
            choice = self.read_console(addr)
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
    
    def read_console(self, addr):
        self.current_addr = addr
        console_box.config(state='normal')
        console_box.insert(END, f'Enter a positive or negative 4 digit number into memory register {addr}, then press enter to submit (ex: +1234 or -4321): ')
        console_box.config(state='disabled')
        input_box.config(state="normal")
        submit_input['state'] = tk.NORMAL
        return False

    def submit_input(self):
        user_input = input_box.get()
        #From this point down, we validate and format the user input to be stored properly in the registers.
        #If user entered a positive value or "0000" without a +, it will be added. And it will check if entered a 4 digit number.
        #Negative values must be entered with a - to be valid. Validated and formated input will be stored in formatted_input.
        success = False
        while not success:
            try:
                if len(user_input) == 0:
                    user_messages.config(text="No input. Please enter a valid positive or negative 4 digit number.")
                    input_box.delete(0, END)
                elif user_input[0] == "-" or user_input[0] == "+": #It first checks if a operation sign is present.
                    if len(user_input) == 5: #If it is, it checks if the number is 4 digits long.
                        user_int = int(user_input) #If it can't parse, it's not a number. A ValueError is raised.
                        insta.console_memory = user_int
                        insta.read(self.current_addr)
                        console_box.config(state='normal')
                        console_box.insert(END, f'{user_input}\n')
                        console_box.config(state='disabled')
                        input_box.delete(0, END)
                        success = True
                    else:
                        user_messages.config(text="Invalid input. Please enter a valid positive or negative 4 digit number.")
                        input_box.delete(0, END)
                elif user_input == "0000": #If 0000 is entered without a sign, we return it with the + sign..
                    insta.console_memory = f"+0000" #We add the plus sign and add it to the memory.
                    insta.read(self.current_addr)
                    console_box.config(state='normal')
                    console_box.insert(END, f'+0000\n')
                    console_box.config(state='disabled')
                    input_box.delete(0, END)
                    success = True
                elif len(user_input) == 4:
                    user_int = int(user_input) #if it's 4 digits long and it can parse, it's a valid positive number.
                    insta.console_memory = f"+{user_input}" #We add the plus sign and add it to the memory.
                    insta.read(self.current_addr)
                    console_box.config(state='normal')
                    console_box.insert(END, f'+{user_input}\n')
                    console_box.config(state='disabled')
                    input_box.delete(0, END)
                    success = True
                else:
                    user_messages.config(text="Invalid input. Please enter a valid positive or negative 4 digit number.")
                    input_box.delete(0, END)
            except ValueError:
                user_messages.config(text="Invalid input. Please enter a valid positive or negative 4 digit number.")
                input_box.delete(0, END)
        
        control.clear_table()
        control.update_table()
        self.run()

insta = Simulator()
control = GUI_Controller()
sim_op = Simulator_Controller()

registers = insta.registers

window = tk.Tk()
window.title("Project Blackbox")
window.geometry("900x800")
window.resizable(False, False)

register_frame = ttk.Frame(window, border=20)
register_frame.pack(fill='y', side=tk.LEFT)

reg_table = ttk.Treeview(register_frame, selectmode ='browse', padding=2)

reg_table.pack(side ='left', fill="y")

reg_scroll = ttk.Scrollbar(register_frame,
						orient =tk.VERTICAL,
						command = reg_table.yview)

reg_scroll.pack(side ='right', fill ="y")

reg_table.configure(yscrollcommand = reg_scroll.set)

reg_table["columns"] = ("1", "2")

reg_table['show'] = 'headings'

reg_table.column("1", width = 60, anchor ='c')
reg_table.column("2", width = 300, anchor ='c')

reg_table.heading("1", text ="Register")
reg_table.heading("2", text ="Value")

control.update_table()

function_frame = tk.Frame(window)
function_frame.pack(side='right', fill='y')

input_frame = tk.Frame(function_frame)
input_frame.pack(side='top')

console_label = tk.Label(input_frame, text="Console:", font=("Arial", 10))
console_label.pack(side='top', padx = 20, pady = (10, 5), anchor="w")
console_box = tk.Text(input_frame, state='disabled', wrap="word") #so it wraps and breaks at the last word if the input is too long
console_box.pack(side='top', anchor='ne', padx = 20, pady = (0, 20))

input_label = tk.Label(input_frame, text="User input:", font=("Arial", 10))
input_label.pack(padx = 20, pady = (0, 10))
input_box = tk.Entry(input_frame, font=("Arial", 15), state="disabled")
input_box.pack(pady = (0, 10))
submit_input = tk.Button(input_frame, text="Submit Input", font=("Arial", 10), state='disabled', command=sim_op.submit_input)
submit_input.pack(pady = (0, 20))

user_messages = tk.Label(input_frame, font=("Arial", 15), text="Select a instruction file to execute.")
user_messages.pack()

button_frame = tk.Frame(function_frame)
button_frame.pack(side='bottom', anchor='c', fill='y', pady=(0, 40))

open_file_btn = tk.Button(button_frame, text="Open File", font=("Courier", 20), command=control.open_file, border=5)
open_file_btn.pack(pady=(0, 30))
run_btn = tk.Button(button_frame, font=("Courier", 20), command=sim_op.run_cancel_control, text="Run", border=5)
run_btn.pack()

window.mainloop()
