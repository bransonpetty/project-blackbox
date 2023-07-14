from tkinter import ttk
import tkinter as tk
from simulator import Simulator
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import *

class GUI_Controller:
    '''Controls most of the updates to the GUI.'''
    def open_file(self):
        '''Opens the file and triggers the functions to prepare GUI to run script.'''
        self.reset_memory() #Resets the memory so the new file's information can be loaded in.
        #Opens file browser to select a txt file for instruction input.
        file_path = filedialog.askopenfilename(filetypes=(("Text File (*.txt)", "*.txt"),))
        error = False #Holds boolean value that determines if file was successfully loaded or not.
        if file_path:
            with open(file_path) as input_file:
                addr = 0 #Current position in the register
                for line in input_file:
                    line = line.strip()
                    if addr > 99: #Makes sure that only 100 registers are read from input file
                        break
                    elif len(line) == 5: #Correct lenght for a value with operator sign
                        if line[0] == "+" or line[0] == "-": #Checks if operator sign is present
                            try:
                                _line_parse_test = int(line) #Tests if input if an integer
                                insta.registers[addr] = line #If no errors from parsing, input is valid
                            except: #If input is not an integer a ValueError will be triggered and an error is recorded
                                user_messages.config(text=f'Error: {line} in your file is not a valid instruction.')
                                error = True
                        else: #If the first character is not a operator sign and length is 5, input is invalid
                            user_messages.config(text=f'Error: {line} in your file is not a valid instruction.')
                            error = True
                    elif line == "-99999": #This means it's the end of the file.
                        break
                    else: #If none of the conditions above are met, the input is invalid
                        user_messages.config(text=f'Error: {line} in your file is not a valid instruction.')
                        error = True
                    addr += 1 #Increments the address
                
            if not error: # If not errors were triggered, register table is loaded and program becames ready to run.
                self.refresh_table()
                run_btn['state'] = tk.NORMAL
                reset_btn['state'] = tk.NORMAL
                user_messages.config(text="File successfully loaded.") #Informs the user that file loaded sucessfully.

    def clear_table(self):
        '''Deletes all of the rows in the register table.'''
        for item in reg_table.get_children():
            reg_table.delete(item)

    def update_table(self):
        '''Repopulates all of the items in the register table.'''
        for register, value in insta.registers.items():
            reg_table.insert("", 'end', text ="L1",
                        values =(register, value))
            
    def refresh_table(self):
        '''Updates the register table with the new values.'''
        self.clear_table()
        self.update_table()

    def refresh_accumulator(self):
        '''Updates the accumulator with new values.'''
        accumulator_box['state'] = 'normal' #Entry has to be enabled to be changed
        accumulator_box.delete(0, END) #Deletes previous value
        accumulator_box.insert(END, insta.accumulator) #Writes the new accumulator value
        accumulator_box['state'] = 'readonly' #Disables the entry box after modifications

    def reset_memory(self):
        '''Resets the simulator and the GUI.'''
        for i in range(100): #Sets all the registers back to "+0000"
            insta.registers[i] = "+0000"
        insta.accumulator = '+0000' #Sets accumulator back to "+0000"
        insta.cur_addr = 0 #Sets the memory pointer back to the first register
        insta.console_memory = "" #Clears the console memory
        insta.log = [] #Clears the logs
        self.refresh_table() #Resets the GUI register table back to default values
        self.refresh_accumulator() #Resets the GUI display of the accumulator back to default value
        run_btn['state'] = 'disabled' #Disables the run button since no value is loaded.

    def clear_console(self):
        '''Clears all the console outputs.'''
        console_box.config(state=tk.NORMAL) #Text had to be enabled to be changed.
        console_box.delete('1.0', 'end') #Deletes all of the text in the console box.
        console_box.config(state=tk.DISABLED) #Disables the text box after modifications.

    def show_input(self):
        '''Enables the user input box and the submit button.'''
        input_box['state'] = "normal"
        submit_input['state'] = 'normal'


    def hide_input(self):
        '''Disables the user input box and the submit button.'''
        input_box['state'] = "disabled"
        submit_input['state'] = 'disabled'

    def highlight_reg(self):
        '''Highlights the current isntruction being executed.'''
        cur_row = reg_table.get_children()[insta.cur_addr]
        reg_table.selection_set(cur_row)
        reg_table.focus_set()

    def change_all_colors(self, primarycolor, offcolor):
        function_frame.configure(bg=primarycolor)
        accumulator_frame.configure(bg=primarycolor)
        accumulator_label.configure(bg=primarycolor)
        accumulator_box.configure(bg=primarycolor)
        input_frame.configure(bg=primarycolor)
        button_frame.configure(bg=primarycolor)
        left_button_frame.configure(bg=primarycolor)
        right_button_frame.configure(bg=primarycolor)
        color_btn.configure(background=offcolor)
        run_btn.configure(background=offcolor)
        open_file_btn.configure(background=offcolor)
        clear_console_btn.configure(background=offcolor)
        reset_btn.configure(background=offcolor)
        input_label.configure(bg=primarycolor)
        console_label.configure(bg=primarycolor)
        newStyle.configure('My.TFrame', background=primarycolor)
        
       

    def choose_color(self):
        '''Function will be called when button is clicked in window'''
        user_color_primary = colorchooser.askcolor(title='choose a PRIMARY color')
        user_color_secondary = colorchooser.askcolor(title='choose a SECONDARY color')
        
        primarycolor = user_color_primary[1] #refers to the HEX value
        offcolor = user_color_secondary[1] #hex value


        self.change_all_colors(primarycolor, offcolor)


class Simulator_Controller:
    '''Holds all of the GUI simulator functions'''
    def __init__(self):
        self.current_addr = ''
        self.error = False
     
    def run_cancel_control(self):
            '''Controls behavior of the run/cancel button'''
            if run_btn["text"] == 'Run': #If the program is not running the button will have its text set to "Run".
                open_file_btn['state'] = tk.DISABLED #Disables the ability to open a new file while program is running
                reset_btn['state'] = tk.DISABLED #Disables the ability to reset the register while program is running
                clear_console_btn['state'] = tk.DISABLED #Disables the ability to clear the console while program is running
                run_btn['text'] = "Cancel" #Changes the run button to have the cancel functionality
                run_btn['bg'] = 'red' #Changes button color to red
                user_messages.config(text=f'Executing program...') #Informs the user that the program is running.
                self.run() #Triggers the simulator run
            else: #If the button text is not "Run", it's "Cancel".
                control.hide_input() #It will disable user input
                sim_op.halt_console() #Triggers the GUI halt operations
       
    def run(self):
        '''Runs each line of the simulator and calls the controller for the appropriate instructions'''
        choice = True #Stops while loop if user aborts or halts
        while insta.cur_addr < 100 and choice:
            control.highlight_reg() #Highlights the register that is currently being executed
            choice = self.controller(insta.registers[insta.cur_addr][1:3], insta.registers[insta.cur_addr][3:]) #Sends instruction code and address to controller
            insta.cur_addr += 1 #Moves to next address
        return

    def controller(self, instruction, addr):
        '''It directs the simulator along with the desired address to the appropriate function based on the instruction'''
        choice = True #True or false is returned by every function and stored in "choice" variable in order to determine if the program should continue or not.
        if instruction not in insta.instructions:
            #If it's not a valid instruction, it will inform the user then halt the program.
            user_messages.config(text=f"Instruction '{insta.registers[insta.cur_addr]}' on address {insta.cur_addr} is invalid. Program was halted.")
            self.error = True #Informs the GUI halt operations that the program wasn't executed properly
            self.halt_console() #Triggers the GUI halt operations
            choice = insta.halt() #Halts the program by setting choice to False
        elif instruction == "00":
            choice = True #Skips empty registers
        elif instruction == "10":
            choice = self.read_console(addr) 
        elif instruction == "11":
            choice = self.console_write(addr)
        elif instruction == "20":
            choice = insta.load(addr)
            control.refresh_accumulator() #Updates the accumulator after operation
        elif instruction == "21":
            choice = insta.store(addr)
            control.refresh_table()
        elif instruction == "30":
            choice = insta.add(addr)
            control.refresh_accumulator() #Updates the accumulator after operation
        elif instruction == "31":
            choice = insta.subtract(addr)
            control.refresh_accumulator() #Updates the accumulator after operation
        elif instruction == "32":
            choice = insta.divide(addr)
            control.refresh_accumulator() #Updates the accumulator after operation
        elif instruction == "33":
            choice = insta.multiply(addr)
            control.refresh_accumulator() #Updates the accumulator after operation
        elif instruction == "40":
            choice = insta.branch(addr)
        elif instruction == "41":
            choice = insta.branch_neg(addr)
        elif instruction == "42":
            choice = insta.branch_zero(addr)
        elif instruction == "43":
            choice = insta.halt()
            self.halt_console() #Triggers the GUI halt operations

        return choice
    
    def read_console(self, addr):
        '''Prepares GUI to accept user input.'''
        self.current_addr = addr #Stores the current address to be used by submit_input function
        console_box.config(state='normal') #Text had to be enabled to be changed.
        console_box.insert(END, f'Enter a positive or negative 4 digit number into memory register {addr}, then press the submit button (ex: +1234 or -4321): ')
        console_box.see(END) #Scrolls the console down
        console_box.config(state='disabled') #Disables the text box after modifications.
        control.show_input() #Enables the user input
        return False #Sets choice to false in order to wait for input submission before moving to next instruction.

    def submit_input(self):
        '''Submits the user input to be loaded into memory'''
        user_input = input_box.get() #Retrieves information from user input box
        #From this point down, we validate and format the user input to be stored properly in the registers.
        #If user entered a positive value or "0000" without a +, it will be added. And it will check if entered a 4 digit number.
        #Negative values must be entered with a - to be valid. Validated and formated input will be stored in formatted_input.
        success = False #Informs program if execution was successful in order to display appropriate user messages
        try:
            if len(user_input) == 0: #Error is displayed if no input is entered
                user_messages.config(text="No input. Please enter a valid positive or negative 4 digit number.")
                input_box.delete(0, END) #Clears the user input box
            elif user_input[0] == "-" or user_input[0] == "+": #It first checks if a operation sign is present.
                if len(user_input) == 5: #If it is, it checks if the number is 4 digits long.
                    user_int = int(user_input) #If it can't parse, it's not a number. A ValueError is raised.
                    insta.console_memory = user_int #Sets the console memory to be read by the simulator read function
                    insta.read(self.current_addr) #Triggers the simulator read function.
                    console_box.config(state='normal') #Text had to be enabled to be changed.
                    console_box.insert(END, f'{user_input}\n\n') #Records the user input in the console
                    console_box.see(END) #Scrolls the console down
                    console_box.config(state='disabled') #Disables the text box after modifications.
                    input_box.delete(0, END) #Clears the user input
                    success = True #Sets success to true to inform program that execution was sucessfull.
                else: #Triggers error if there's more than 4 digits after operator sign.
                    user_messages.config(text="Invalid input. Please enter a valid positive or negative 4 digit number.")
                    input_box.delete(0, END) #Clears the user input box
            elif user_input == "0000": #If 0000 is entered without a sign, we return it with the + sign..
                insta.console_memory = f"+0000" #We add the plus sign and add it to the console memory.
                insta.read(self.current_addr) #Triggers the simulator read function
                console_box.config(state='normal') #Text had to be enabled to be changed.
                console_box.insert(END, f'+0000\n\n') #Records the user input in the console
                console_box.see(END) #Scrolls the console down
                console_box.config(state='disabled') #Disables the text box after modifications.
                input_box.delete(0, END) #Clears the user input
                success = True #Sets success to true to inform program that execution was sucessfull.
            elif len(user_input) == 4:
                user_int = int(user_input) #if it's 4 digits long and it can parse, it's a valid positive number.
                insta.console_memory = f"+{user_input}" #We add the plus sign and add it to the console memory.
                insta.read(self.current_addr) #Triggers the simulator read function
                console_box.config(state='normal') #Text had to be enabled to be changed.
                console_box.insert(END, f'+{user_input}\n\n') #Records the user input in the console
                console_box.see(END) #Scrolls the console down
                console_box.config(state='disabled') #Disables the text box after modifications.
                input_box.delete(0, END) #Clears the user input
                success = True #Sets success to true to inform program that execution was sucessfull.
            else: #Triggers an error if none of the conditions above are met.
                user_messages.config(text="Invalid input. Please enter a valid positive or negative 4 digit number.")
                input_box.delete(0, END) #Clears the user input
        except ValueError: #If number fails to parse, it will trigger this error
            user_messages.config(text="Invalid input. Please enter a valid positive or negative 4 digit number.")
            input_box.delete(0, END)

        if success: #If operation is sucessfully executed, program continues to run
            control.hide_input() #Disables user input
            user_messages.config(text="Executing program...") #Informs the user that the program is running again.
            control.refresh_table() #Updates the GUI register table
            self.run() #Resumes the program execution
        #If it was not sucessfull, function returns and waits for another input after displaying error message.
    
    def console_write(self, addr):
        '''Writes to the console the value from the register specified.'''
        console_box.config(state='normal') #Text had to be enabled to be changed.
        console_box.insert(END, f"Value from register {addr}: {insta.registers[int(addr)]}\n\n") #Displays the value from the register to console
        console_box.see(END) #Scrolls the console down
        console_box.config(state='disabled') #Disables the text box after modifications.
        return True #Continues program execution
    
    def halt_console(self):
        '''Performs all of the GUI operations necessary after halting.'''
        console_box.config(state='normal') #Text had to be enabled to be changed.
        console_box.insert(END, f"-----------------------Program has halted----------------------\n\n")
        console_box.see(END) #Scrolls the console down
        console_box.config(state='disabled') #Disables the text box after modifications.
        #Enables the Open file, Reset Memory, and Clear Console buttons after program execution.
        open_file_btn['state'] = tk.NORMAL
        reset_btn['state'] = tk.NORMAL
        clear_console_btn['state'] = tk.NORMAL
        #Sets the "Cancel" button back to "Run" functionality
        run_btn["text"] = "Run"
        run_btn['bg'] = 'dodgerblue3'
        run_btn['state'] = 'disabled' #Keeps it disabled until new file is opened
        if self.error == False: #If not errors on halting, informs the user that program executed sucessfully
            user_messages.config(text="Program executed sucessfully.")
        #If there was an error, an error message will already be displaying.
        
        


'''Initial GUI render'''

#Initiates all of the class instances
insta = Simulator()
control = GUI_Controller()
sim_op = Simulator_Controller()

#Creates the window containing the program GUI
window = tk.Tk()
window.title("Project Blackbox")
window.geometry("1000x800")
window.resizable(False, False)
#window.configure(bg='green')
offcolor = "#FFFFFF" #UVU white
primarycolor='#4C721D' #UVU green

#Creates and populates the GUI register table
register_frame = ttk.Frame(window, border=20) #Frame containing the GUI register 
register_frame.pack(fill='y', side=tk.LEFT)
newStyle = ttk.Style()
newStyle.configure('My.TFrame', background=primarycolor)
register_frame.config(style='My.TFrame')

reg_table = ttk.Treeview(register_frame, selectmode ='browse', padding=2) #GUI register table

reg_table.pack(side ='left', fill="y")

reg_scroll = ttk.Scrollbar(register_frame,
						orient =tk.VERTICAL,
						command = reg_table.yview) #Scrollbar for the register table

reg_scroll.pack(side ='right', fill ="y")

reg_table.configure(yscrollcommand = reg_scroll.set)

reg_table["columns"] = ("1", "2")

reg_table['show'] = 'headings'

reg_table.column("1", width = 60, anchor ='c')
reg_table.column("2", width = 300, anchor ='c')

reg_table.heading("1", text ="Register")
reg_table.heading("2", text ="Value")

control.update_table()

#Creates all the other GUI items to the right of the GUI register table
function_frame = tk.Frame(window, bg =primarycolor) 
function_frame.pack(side='right', fill='y')

color_btn = tk.Button(function_frame, text='Choose Color', font=("Courier", 20), command=control.choose_color, background=offcolor)
color_btn.pack(pady=3)

accumulator_frame = tk.Frame(function_frame, background=primarycolor) #Frame containing the accumulator display
accumulator_frame.pack(side="top", pady=(20,0))

accumulator_label = tk.Label(accumulator_frame, text="Accumulator: ", font=("Arial", 20), bg=primarycolor) #Accumulator title
accumulator_label.pack(side="left")
accumulator_box = tk.Entry(accumulator_frame, font=("Arial", 20), width=6, bg=primarycolor) #Accumulator display
accumulator_box.pack(side="right")

accumulator_box.insert(END, insta.accumulator) #Populates the accumulator
accumulator_box['state'] = 'readonly'

input_frame = tk.Frame(function_frame, bg=primarycolor) #Frame containing console and user input
input_frame.pack(side='top')

console_label = tk.Label(input_frame, text="Console:", font=("Arial", 10), bg=primarycolor) #Console title
console_label.pack(side='top', padx = 20, pady = (10, 5), anchor="w")
console_box = tk.Text(input_frame, state='disabled', wrap="word", height=18) #Console box
console_box.pack(side='top', anchor='ne', padx = 20, pady = (0, 20))

input_label = tk.Label(input_frame, text="User input:", font=("Arial", 10), bg=primarycolor) #Input title
input_label.pack(padx = 20, pady = (0, 10))
input_box = tk.Entry(input_frame, font=("Arial", 15), state="disabled") #Input box
input_box.pack(pady = (0, 10))
submit_input = tk.Button(input_frame, text="Submit Input", font=("Arial", 10), state='disabled', command=sim_op.submit_input, fg='black', bg=offcolor) #Input submit button
submit_input.pack(pady = (0, 10))

user_messages = tk.Label(input_frame, font=("Arial", 15), text="Select a instruction file to execute.", wraplength="400", activebackground=primarycolor) #Text for messages directed to the user.
user_messages.pack(pady=(0, 10))

button_frame = tk.Frame(function_frame, background=primarycolor) #Frame containing all the buttons
button_frame.pack(side='bottom', anchor='c', fill='y', pady=(0, 70))

left_button_frame = tk.Frame(button_frame, background=primarycolor) #Frame for buttons on the left
left_button_frame.pack(side='left')
right_button_frame = tk.Frame(button_frame, background=primarycolor) #Frame for buttons on the right
right_button_frame.pack(side='right')

open_file_btn = tk.Button(left_button_frame, text="Open File", font=("Courier", 20), command=control.open_file, border=5, width=15, bg=offcolor, fg='black') #Button to open file
open_file_btn.pack(pady=(0,7.5), padx=(0,7.5), side='top')
reset_btn = tk.Button(left_button_frame, text="Reset Memory", font=("Courier", 20), command=control.reset_memory,border=5, width=15, bg=offcolor, fg='black') #Button to reset the memory
reset_btn.pack(side='bottom', pady=(7.5,0), padx=(0,7.5))
run_btn = tk.Button(right_button_frame, font=("Courier", 20), command=sim_op.run_cancel_control, text="Run", border=5, width=15, bg=offcolor, fg='black', state='disabled') #Button to run and cancel the program execution, can use disabledforeground to make text more readable in needed
run_btn.pack(pady=(0,7.5), side='top', padx=(7.5,0))
clear_console_btn = tk.Button(right_button_frame, font=("Courier", 20), command=control.clear_console,text="Clear Console", border=5, width=15, bg=offcolor, fg='black') #Button to clear the console
clear_console_btn.pack(side='bottom', pady=(7.5,0), padx=(7.5,0))




window.mainloop() #Triggers the GUI initialization
