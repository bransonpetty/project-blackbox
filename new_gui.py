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
            counter = 0
            with open(file_path) as input_file:
                addr = 0 
                for line in input_file:
                    line = line.strip()
                    #make sure its a + or a -
                    if counter > 99:
                        break
                    elif len(line) == 5:
                        insta.registers[addr] = line
                    elif line == "-99999":
                        break
                    else:
                        user_messages.config(text=f'Error: {line} in your file is not a valid instruction.')
                        error = True
                    addr += 1
                    counter += 1
                
            if not error:
                self.clear_table()
                self.update_table()
                run_btn['state'] = tk.NORMAL
                reset_btn['state'] = tk.NORMAL
            
            user_messages.config(text="File successfully loaded.")

    def clear_table(self):
        for item in reg_table.get_children():
                    reg_table.delete(item)

    def update_table(self):
        for register, value in registers.items():
            reg_table.insert("", 'end', text ="L1",
                        values =(register, value))
            
    def refresh_table(self):
        self.clear_table()
        self.update_table()

    def refresh_accumulator(self):
        acumulator_box['state'] = 'normal'
        acumulator_box.delete(0, END)
        acumulator_box.insert(END, insta.accumulator)
        acumulator_box['state'] = 'readonly'

    def reset_memory(self):
        for i in range(100): #Creates the registers using a dictionary
            insta.registers[i] = "+0000"
        insta.accumulator = '+0000'
        insta.cur_addr = 0
        insta.console_memory = ""
        insta.log = []
        self.refresh_table()

    def clear_console(self):
        pass


class Simulator_Controller:

    def __init__(self):
        self.current_addr = ''
        self.error = False
     
    def run_cancel_control(self):
            #function that runs file
            if run_btn["text"] == 'Run':
                open_file_btn['state'] = tk.DISABLED
                reset_btn['state'] = tk.DISABLED
                clear_console_btn['state'] = tk.DISABLED
                run_btn['text'] = "Cancel"
                run_btn['bg'] = 'red'
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
            user_messages.config(text=f"Instruction '{insta.registers[insta.cur_addr]}' on address {insta.cur_addr} is invalid. Program was halted.")
            insta.halt()
            self.error = True
            self.halt_console()
            choice = False
        elif instruction == "00":
            choice = True
        elif instruction == "10":
            choice = self.read_console(addr)
            control.refresh_table()
        elif instruction == "11":
            choice = self.console_write(addr)
        elif instruction == "20":
            choice = insta.load(addr)
            control.refresh_accumulator()
        elif instruction == "21":
            choice = insta.store(addr)
            control.refresh_table()
        elif instruction == "30":
            choice = insta.add(addr)
            control.refresh_accumulator()
        elif instruction == "31":
            choice = insta.subtract(addr)
            control.refresh_accumulator()
        elif instruction == "32":
            choice = insta.divide(addr)
            control.refresh_accumulator()
        elif instruction == "33":
            choice = insta.multiply(addr)
            control.refresh_accumulator()
        elif instruction == "40":
            choice = insta.branch(addr)
        elif instruction == "41":
            choice = insta.branch_neg(addr)
        elif instruction == "42":
            choice = insta.branch_zero(addr)
        elif instruction == "43":
            choice = insta.halt()
            self.halt_console()

        return choice
    
    def read_console(self, addr):
        self.current_addr = addr
        console_box.config(state='normal')
        console_box.insert(END, f'Enter a positive or negative 4 digit number into memory register {addr}, then press enter to submit (ex: +1234 or -4321):')
        console_box.insert(END, "")
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
                    console_box.insert(END, f'{user_input}\n\n')
                    console_box.see(END)
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
                console_box.insert(END, f'+0000\n\n')
                console_box.see(END)
                console_box.config(state='disabled')
                input_box.delete(0, END)
                success = True
            elif len(user_input) == 4:
                user_int = int(user_input) #if it's 4 digits long and it can parse, it's a valid positive number.
                insta.console_memory = f"+{user_input}" #We add the plus sign and add it to the memory.
                insta.read(self.current_addr)
                console_box.config(state='normal')
                console_box.insert(END, f'+{user_input}\n\n')
                console_box.see(END)
                console_box.config(state='disabled')
                input_box.delete(0, END)
                success = True
            else:
                user_messages.config(text="Invalid input. Please enter a valid positive or negative 4 digit number.")
                input_box.delete(0, END)
        except ValueError:
            user_messages.config(text="Invalid input. Please enter a valid positive or negative 4 digit number.")
            input_box.delete(0, END)

        if success:
            user_messages.config(text="Executing program...")
            control.refresh_table()
            self.run()
    
    def console_write(self, addr):
        console_box.config(state='normal')
        console_box.insert(END, f"Value from register {addr}: {insta.registers[int(addr)]}\n\n")
        console_box.see(END)
        console_box.config(state='disabled')
        return True
    
    def halt_console(self):
        console_box.config(state='normal')
        console_box.insert(END, f"-----------------Program has halted-----------------\n\n")
        console_box.see(END)
        console_box.config(state='disabled')
        open_file_btn['state'] = tk.NORMAL
        reset_btn['state'] = tk.NORMAL
        clear_console_btn['state'] = tk.NORMAL
        run_btn["text"] = "Run"
        run_btn['bg'] = 'green'
        if self.error == False:
            user_messages.config(text="Program executed sucessfully.")


insta = Simulator()
control = GUI_Controller()
sim_op = Simulator_Controller()

registers = insta.registers

window = tk.Tk()
window.title("Project Blackbox")
window.geometry("1000x800")
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

acumulator_frame = tk.Frame(input_frame)
acumulator_frame.pack(pady=(20,0))

acumulator_label = tk.Label(acumulator_frame, text="Acumulator: ", font=("Arial", 20))
acumulator_label.pack(side="left")
acumulator_box = tk.Entry(acumulator_frame, font=("Arial", 20), width=6)
acumulator_box.pack(side="right")

acumulator_box.insert(END, insta.accumulator)
acumulator_box['state'] = 'readonly'

console_label = tk.Label(input_frame, text="Console:", font=("Arial", 10))
console_label.pack(side='top', padx = 20, pady = (10, 5), anchor="w")
console_box = tk.Text(input_frame, state='disabled', wrap="word", height=18) #so it wraps and breaks at the last word if the input is too long
console_box.pack(side='top', anchor='ne', padx = 20, pady = (0, 20))

input_label = tk.Label(input_frame, text="User input:", font=("Arial", 10))
input_label.pack(padx = 20, pady = (0, 10))
input_box = tk.Entry(input_frame, font=("Arial", 15), state="disabled")
input_box.pack(pady = (0, 10))
submit_input = tk.Button(input_frame, text="Submit Input", font=("Arial", 10), state='disabled', command=sim_op.submit_input)
submit_input.pack(pady = (0, 10))

user_messages = tk.Label(input_frame, font=("Arial", 15), text="Select a instruction file to execute.", wraplength="400")
user_messages.pack()

button_frame = tk.Frame(function_frame)
button_frame.pack(side='bottom', anchor='c', fill='y', pady=(0, 70))

left_button_frame = tk.Frame(button_frame)
left_button_frame.pack(side='left')
right_button_frame = tk.Frame(button_frame)
right_button_frame.pack(side='right')

open_file_btn = tk.Button(left_button_frame, text="Open File", font=("Courier", 20), command=control.open_file, border=5, width=15, bg='dodgerblue3', fg='white')
open_file_btn.pack(pady=(0,7.5), padx=(0,7.5), side='top')
reset_btn = tk.Button(left_button_frame, text="Reset Memory", font=("Courier", 20), command=control.reset_memory,border=5, width=15, bg='firebrick1', fg='white', state='disabled')
reset_btn.pack(side='bottom', pady=(7.5,0), padx=(0,7.5))
run_btn = tk.Button(right_button_frame, font=("Courier", 20), command=sim_op.run_cancel_control, text="Run", border=5, width=15, bg='green', fg='white', state='disabled')
run_btn.pack(pady=(0,7.5), side='top', padx=(7.5,0))
clear_console_btn = tk.Button(right_button_frame, font=("Courier", 20), text="Clear Console", border=5, width=15, bg='firebrick1', fg='white', state='disabled')
clear_console_btn.pack(side='bottom', pady=(7.5,0), padx=(7.5,0))

window['background'] = 'red'
window.mainloop()
