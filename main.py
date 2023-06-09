'''
Project Blackbox

Designed and built by: Branson Petty, Connor Barry, Noah Potter, and Pedro Valente.

The purpose of this program is to create a functional assembly program that reads an instruction file
line by line. Executing commands and utilizing 100 registers as virtual memory that each store signed 
4 digit numbers, referred to as words, and the each of the operations.

The program was designed to only run .txt files. This decision was made to assure maximum accuracy
and to prevent the user from crashing the program by running a file type that the program wouldn't
be able to read accurately. To run your program file, make sure that the file containing the instructions
is located in the same folder as the python script. Enter the filename with the extension.

These are the instruction codes that can be used when designing your own assembly program:

I/O operations:
READ = 10 Read a word from the keyboard into a specific location in memory.
WRITE = 11 Write a word from a specific location in memory to screen.

Load/store operations:
LOAD = 20 Load a word from a specific location in memory into the accumulator.
STORE = 21 Store a word from the accumulator into a specific location in memory.

Arithmetic operations:
ADD = 30 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
SUBTRACT = 31 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
DIVIDE = 32 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
MULTIPLY = 33 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

Control operatios:
BRANCH = 40 Branch to a specific location in memory
BRANCHNEG = 41 Branch to a specific location in memory if the accumulator is negative.
BRANCHZERO = 42 Branch to a specific location in memory if the accumulator is zero.
HALT = 43 Pause the program
'''

import os
from sys import argv

'''Simulator Class'''

class Simulator:
    '''Holds the list of commands and simulator functions'''
    def __init__(self):
        self.registers = {} #Initializes the registers
        self.accumulator = "+0000" #Initializes the accumulator
        self.cur_addr = 0 #Initializes the current address
        self.instructions = ["00", "10", "11", "20", "21", "30", "31", "32", "33", "40", "41", "42", "43"] #Lists all the valid instructions
        self.log = [] #Creates a log list of all the operations

        for i in range(100): #Creates the registers using a dictionary
            self.registers[i] = "+0000"

    '''Class management functions'''

    def open_file(self, file_name):
        '''Opens a file and loads the contents into the registers'''
        if os.path.exists(file_name):
            if file_name.endswith('.txt'):
                with open(file_name) as input_file:
                    addr = 0 
                    for line in input_file:
                        line = line.strip()
                        #make sure its a + or a -
                        if len(line) == 5:
                            self.registers[addr] = line
                        elif line == "-99999":
                            return True
                        else:
                            print(f"Invalid line in file: {line}")
                            return False
                        addr += 1
                return True
            else:
                print('Wrong file type. Must be a .txt file')
                return False
        else:
            print(f"File '{file_name}' does not exist")
            return False
        
    def run(self):
        '''Runs each line of the simulator and calls the controller for the appropriate instructions'''
        choice = True #Stops while loop if user aborts or halts
        while self.cur_addr < 100 and choice:
            choice = self.controller(self.registers[self.cur_addr][1:3], self.registers[self.cur_addr][3:]) #Sends instruction code and address to controller
            self.cur_addr += 1 #Moves to next address
        return
    
    def controller(self, instruction, addr):
        '''It directs the simulator along with the desired address to the appropriate function based on the instruction'''
        choice = True #True or false is returned by every function and stored in "choice" variable in order to determine if the program should continue or not.
        if instruction not in self.instructions: #If it's not a valid instruction, it either ends the program or continues from the next instruction
            choice = self.invalid_instruction(instruction)
        elif instruction == "00":
            choice = True
        elif instruction == "10":
            choice = self.read(addr)
        elif instruction == "11":
            choice = self.write(addr)
        elif instruction == "20":
            choice = self.load(addr)
        elif instruction == "21":
            choice = self.store(addr)
        elif instruction == "30":
            choice = self.add(addr)
        elif instruction == "31":
            choice = self.subtract(addr)
        elif instruction == "32":
            choice = self.divide(addr)
        elif instruction == "33":
            choice = self.multiply(addr)
        elif instruction == "40":
            choice = self.branch(addr)
        elif instruction == "41":
            choice = self.branch_neg(addr)
        elif instruction == "42":
            choice = self.branch_zero(addr)
        elif instruction == "43":
            choice = self.halt()

        return choice
    
    def report(self, report_num):
        '''Reports a log of operations and all of the instructions present in the registers and accumulator.'''
        with open(f"Report({report_num}).txt", "w") as report_file: #Creates a new file for the report
            report_file.write("PROGRAM REPORT:\n\n")
            report_file.write("Log of operations performed:\n\n") #Writes the log of operations to the file
            for op in self.log:
                report_file.write(f"{op}\n")
            
            reg_end = 99
            for i in reversed(range(100)): #Finds the last register that was used so we don't write all 100 registers to the file.
                if self.registers[i] != "+0000":
                    reg_end = i
                    break
            
            report_file.write("\nFinal state of the registry:\n\n") 
            for i in range(reg_end + 1): #Writes the final state of the registers to the file
                report_file.write(f"{str(i).zfill(2)}: {self.registers[i]}\n")

            report_file.write(f"\nFinal value of the accumulator: {self.accumulator}\n") #Writes the final value of the accumulator to the file
        return
    
    def invalid_instruction(self, instruction):
        '''If the instruction is invalid, it asks the user if they want to continue from the next instruction or end the program'''
        print(f"{instruction} is an invalid instruction")
        while True: #Loops until a valid instruction is reached or the user decides to finish the program.
            choice = input("Would you like to continue from the next instruction? (y/n): ").lower()
            if choice == "y":
                return True
            elif choice == "n":
                return False
            else:
                print("Invalid input, try again.")
    
    def format_input(self, user_input):
        '''Validates the input for the address'''
        try:
            if len(user_input) == 0:
                print("No input. Please enter a valid positive or negative 4 digit number.")
                return '-1' #-1 is the error code for an invalid input
            elif user_input[0] == "-" or user_input[0] == "+": #It first checks if a operation sign is present.
                if len(user_input) == 5: #If it is, it checks if the number is 4 digits long.
                    user_int = int(user_input) #If it can't parse, it's not a number. A ValueError is raised.
                    return user_input #If it parses successfully, it returns the input as is.
                else:
                    print("Invalid input. Please enter a valid positive or negative 4 digit number.")
                    return '-1' #-1 is the error code for an invalid input
            elif user_input == "0000": #If 0000 is entered without a sign, we return it with the + sign..
                return "+0000"
            elif len(user_input) == 4:
                user_int = int(user_input) #if it's 4 digits long and it can parse, it's a valid positive number.
                return f"+{user_input}" #We add the plus sign and return it.
            else:
                print("Invalid input. Please enter a valid positive or negative 4 digit number.")
                return '-1' #-1 is the error code for an invalid input
        except ValueError:
            print("Invalid input. Please enter a valid positive or negative 4 digit number.")
            return "-1" #-1 is the error code for an invalid input
        
        
    
    '''I/O operations'''
    
    def read(self, addr):
        '''Reads a word from the keyboard into a specific location in memory.'''
        user_input = input(f'Enter a positive or negative 4 digit number into memory register {addr} (ex: +1234 or -4321): ')
        #From this point down, we validate and format the user input to be stored properly in the registers.
        #If user entered a positive value or "0000" without a +, it will be added. And it will check if entered a 4 digit number.
        #Negative values must be entered with a - to be valid. Validated and formated input will be stored in formatted_input.
        formatted_input = ""
        success = False
        while not success:
            formatted_input = self.format_input(user_input)
            if formatted_input != "-1":
                success = True
            else:
                user_input = input(f'Enter a positive or negative 4 digit number into memory register {addr} (ex: +1234 or -4321): ')
        self.log.append(f"'{formatted_input}' was read from keyboard into address: {str(addr).zfill(2)}") #Logs the operation.
        self.registers[int(addr)] = formatted_input #Stores the formatted input into the desired register.
        return True
    
    def write(self, addr):
        '''Writes a word from a specific location in memory to screen.'''
        word = self.registers[int(addr)] #Gets the word from the register.
        self.log.append(f"{word} was written to screen from address: {str(addr).zfill(2)}") #Logs the operation.
        print(word) #Prints the word to the screen.
        return True
    
    '''Load/store operations'''
    
    def load(self, addr):
        '''Loads a word from a specific location in memory into the accumulator.'''
        word = self.registers[int(addr)] #Gets the word from the register.
        self.log.append(f"{word} was loaded to the accumulator from address: {str(addr).zfill(2)}") #Logs the operation.
        self.accumulator = word #Loads the word into the accumulator.
        return True
    
    def store(self, addr):
        '''Stores a word from the accumulator into a specific location in memory.'''
        self.log.append(f"{self.accumulator} was stored from the accumulator into address: {str(addr).zfill(2)}") #Logs the operation.
        self.registers[int(addr)] = self.accumulator #Stores the word from the accumulator into the register.
        return True
    
    '''Arithmetic operations'''
    
    def add(self, addr):
        '''Adds a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator)'''
        intial_acc = self.accumulator #Saves the initial value of the accumulator for the log.
        result = int(self.accumulator) + int(self.registers[int(addr)]) #Adds the word from the register to the word in the accumulator.
        if result > 9999 or result < -9999: #Checks if the result is too large to be stored in the accumulator.
            print(f"Overflow error on addition in address {addr}.\nThe result is too large to be stored in the accumulator. The program will now be terminated.")
            self.log.append(f"Overflow error on addition in address {addr}. The result is too large to be stored in the accumulator.")
            return False
        #The following elif and else statements format the result to be stored in the accumulator.
        elif result > 0: 
            self.accumulator = f"+{str(result).zfill(4)}"
        elif result == 0:
            self.accumulator = "+0000"
        else:
            self.accumulator = f"{str(result).zfill(5)}" 
        #It's a long log entry, but is usefull to see what happened.
        self.log.append(f"{intial_acc} from the accumulator was added to {self.registers[int(addr)]} from address: {str(addr).zfill(2)} and result ({self.accumulator}) was stored back in the accumulator")
        return True
    
    def subtract(self, addr):
        '''Subtracts a word from a specific location in memory from the word in the accumulator (leaves the result in the accumulator)'''
        intial_acc = self.accumulator #Saves the initial value of the accumulator for the log.
        result = int(self.accumulator) - int(self.registers[int(addr)]) #Subtracts the word from the register from the word in the accumulator.
        if result > 9999 or result < -9999: #Checks if the result is too large to be stored in the accumulator.
            print(f"Overflow error on subtraction in address {addr}.\nThe result is too large to be stored in the accumulator. The program will now be terminated.")
            self.log.append(f"Overflow error on subtraction in address {addr}. The result is too large to be stored in the accumulator.")
            return False
        #The following elif and else statements format the result to be stored in the accumulator.
        elif result > 0:
            self.accumulator = f"+{str(result).zfill(4)}"
        elif result == 0:
            self.accumulator = "+0000"
        else:
            self.accumulator = f"{str(result).zfill(5)}"
        #It's a long log entry, but is usefull to see what happened.
        self.log.append(f"{intial_acc} from the accumulator was subtracted by {self.registers[int(addr)]} from address: {str(addr).zfill(2)} and result ({self.accumulator}) was stored back in the accumulator")
        return True
    
    def divide(self, addr):
        '''Divides the word in the accumulator by a word from a specific location in memory (leaves the result in the accumulator).'''
        intial_acc = self.accumulator #Saves the initial value of the accumulator for the log.
        result = int(self.accumulator) // int(self.registers[int(addr)]) #Divides the word in the accumulator by the word from the register.
        #NO DIVISION OPERATION SHOULD RESULT IN OVERFLOW, I'M STILL LEAVING THIS HERE IN CASE THERE IS ANY ABNORMALITY I DIDN'T PREDICT.
        if result > 9999 or result < -9999: #Checks if the result is too large to be stored in the accumulator.
            print(f"Overflow error on division in address {addr}.\nThe result is too large to be stored in the accumulator. The program will now be terminated.")
            self.log.append(f"Overflow error on division in address {addr}. The result is too large to be stored in the accumulator.")
            return False
        #The following elif and else statements format the result to be stored in the accumulator.
        elif result > 0:
            self.accumulator = f"+{str(result).zfill(4)}"
        elif result == 0:
            self.accumulator = "+0000"
        else:
            self.accumulator = f"{str(result).zfill(5)}"
        #It's a long log entry, but is usefull to see what happened.
        self.log.append(f"{intial_acc} from the accumulator was divided by {self.registers[int(addr)]} from address: {str(addr).zfill(2)} and result ({self.accumulator}) was stored back in the accumulator")
        return True
    
    def multiply(self, addr):
        '''Multiplies a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator).'''
        intial_acc = self.accumulator #Saves the initial value of the accumulator for the log.
        result = int(self.accumulator) * int(self.registers[int(addr)]) #Multiplies the word in the accumulator by the word from the register.
        if result > 9999 or result < -9999: #Checks if the result is too large to be stored in the accumulator.
            print(f"Overflow error on multiplication in address {addr}.\nThe result is too large to be stored in the accumulator. The program will now be terminated.")
            self.log.append(f"Overflow error on multiplication in address {addr}. The result is too large to be stored in the accumulator.")
            return False
        #The following elif and else statements format the result to be stored in the accumulator.
        elif result > 0:
            self.accumulator = f"+{str(result).zfill(4)}"
        elif result == 0:
            self.accumulator = "+0000"
        else:
            self.accumulator = f"{str(result).zfill(5)}"
        #It's a long log entry, but is usefull to see what happened.
        self.log.append(f"{intial_acc} from the accumulator was multiplied by {self.registers[int(addr)]} from address: {str(addr).zfill(2)} and result ({self.accumulator}) was stored back in the accumulator")
        return True
    
    '''Control operations'''

    def branch(self, addr):
        '''Branches to a specific location in memory.'''
        #Sets the current address to the address specified in the instruction.
        #It subtracts 1 from the desired address since the program moves to next location upon returning.
        self.cur_addr = int(addr) - 1
        self.log.append(f"Program branched to address: {str(addr).zfill(2)}") #Logs the operation
        return True
    
    def branch_neg(self, addr):
        '''Branches to a specific location in memory if the accumulator is negative.'''
        #Sets the current address to the address specified in the instruction if accumulator is negative.
        #It subtracts 1 from the desired address since the program moves to next location upon returning.
        if int(int(self.accumulator)) < 0:
            self.cur_addr = int(addr) - 1
            self.log.append(f"Program branched to address: {str(addr).zfill(2)} since the accumulator was negative({self.accumulator})") #Logs the operation
        return True
    
    def branch_zero(self, addr):
        '''Branches to a specific location in memory if the accumulator is zero.'''
        #Sets the current address to the address specified in the instruction if accumulator is "+0000".
        #It subtracts 1 from the desired address since the program moves to next location upon returning.
        if self.accumulator == "+0000":
            self.cur_addr = int(addr) - 1
            self.log.append(f"Program branched to address: {str(addr).zfill(2)} since the accumulator was zero({self.accumulator})") #Logs the operation
        return True
    
    def halt(self):
        '''Halts the program.'''
        self.log.append(f"Program was halted")
        return False #Returns false to stop the program.
    

'''Main functions'''

def simulator_run(file_name, report_num):
    '''Runs all functions required from the simulator'''
    insta = Simulator() #Creates a new instance of the simulator
    success = False
    while not success: #Checks if file exists, and opens it. If it doesn't exist, it asks for a new file name.
        success = insta.open_file(file_name)
        if not success:
            file_name = input("Enter the name of the file or type 'cancel' to abort the program: ")
        if file_name.lower() == "cancel":
            print("This operation was cancelled. Have a nice day!")
            return False
    insta.run() #Runs the simulator
    insta.report(report_num) #Creates a report of the simulator run
    return True


def main():
    '''Main function'''
    report_num = 1 #Keep track of the number of reports so we don't overwrite previous reports
    if len(argv) < 2: #Checks if the user entered a file name, if not, it asks for one.
        file_name = input("Enter the name of the file or type 'cancel' to abort the program: ")
        if file_name.lower() == "cancel":
            print("This operation was cancelled. Have a nice day!")
            return
    else:
        file_name = argv[1]
    simu_ran = simulator_run(file_name, report_num) #Runs the first simulator instance

    if not simu_ran: #If the user cancelled the program, it ends the program.
        return

    #This part of the code asks the user if they want to run the simulator again for another file, if not, it ends the program.
    again = True
    while again:
        user_again = input("Program finished running, do you wish to run another program? (y/n): ")
        if user_again.lower() == "y":
            report_num += 1
            file_name = input("Enter the name of the file: ")
            simulator_run(file_name, report_num)
        elif user_again.lower() == "n":
            print("Thank you for using the simulator! Check your program report(s) for more information on the program(s) you ran.")
            again = False
        else:
            print("Invalid input, try again!")
    

if __name__ == "__main__":
    main()