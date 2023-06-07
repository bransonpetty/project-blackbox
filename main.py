'''
Future boilerplate
'''

import os
from sys import argv


class Simulator:
    '''Holds the list of commands and simulator functions'''
    def __init__(self):
        self.registers = {} #Initializes the registers
        self.accumulator = "+0000" #Initializes the accumulator
        self.cur_addr = 0 #Initializes the current address
        self.instructions = ["10", "11", "20", "21", "30", "31", "32", "33", "40", "41", "42", "43"] #Lists all the valid instructions
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
                return
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
        if instruction not in self.instructions: #If it's not a valid instruction, it either ends the program or continues from the next instruction
            choice = invalid_instruction(instruction)
            return choice
        elif instruction == "10":
            self.read(addr)
        elif instruction == "11":
            self.write(addr)
        elif instruction == "20":
            self.load(addr)
        elif instruction == "21":
            self.store(addr)
        elif instruction == "30":
            self.add(addr)
        elif instruction == "31":
            self.subtract(addr)
        elif instruction == "32":
            self.divide(addr)
        elif instruction == "33":
            self.multiply(addr)
        elif instruction == "40":
            self.branch(addr)
        elif instruction == "41":
            self.branch_neg(addr)
        elif instruction == "42":
            self.branch_zero(addr)
        elif instruction == "43":
            return self.halt()

        return True
    
    def report(self, report_num):
        '''Reports a log of operations and all of the instructions present in the registers and accumulator.'''
        with open(f"Report({report_num}).txt", "w") as report_file: #Creates a new file for the report
            report_file.write("PROGRAM REPORT:\n\n")
            report_file.write("Log of operations performed:\n\n") #Writes the log of operations to the file
            for op in self.log:
                report_file.write(f"{op}\n")
            
            reg_end = 99
            for i in reversed(range(100)): #Finds the last register that was used
                if self.registers[i] != "+0000":
                    reg_end = i
                    break
            
            report_file.write("\nFinal state of the registry:\n\n") 
            for i in range(reg_end + 1): #Writes the final state of the registers to the file
                report_file.write(f"{str(i).zfill(2)}: {self.registers[i]}\n")

            report_file.write(f"\nFinal value of the accumulator: {self.accumulator}\n") #Writes the final value of the accumulator to the file
        return
    
    '''I/O operations'''
    
    def read(self, addr):
        '''Reads a word from the keyboard into a specific location in memory.'''
        self.log.append(f"Word was read from keyboard into address: {str(addr).zfill(2)}")
        print(f'ADDRESS IS {addr}')
        print("read")
        addr = int(addr)
        user_input = input('Enter a 4 digit number into memory: ')
        self.registers[addr] = user_input
        print(f'REGISTERS ARE {self.registers}')
        return
    
    def write(self, addr):
        '''Writes a word from a specific location in memory to screen.'''
        self.log.append(f"Word was written to screen from address: {str(addr).zfill(2)}")
        print(f'Address is {addr}')
        print("write")
        addr = int(addr)
        print(f'TO SCREEN: {self.registers[addr]}')
        return
    
    '''Load/store operations'''
    
    def load(self, addr):
        '''Loads a word from a specific location in memory into the accumulator.'''
        self.log.append(f"Word was loaded to the accumulator from address: {str(addr).zfill(2)}")
        print(f'addr is {addr}')
        print("load")
        addr = int(addr)
        self.accumulator = self.registers[addr]
        print(f'accumulator is now {self.accumulator}')
        return
    
    def store(self, addr):
        '''Stores a word from the accumulator into a specific location in memory.'''
        self.log.append(f"Word was stored from the accumulator into address: {str(addr).zfill(2)}")
        print(f'addr is {addr}')
        print("store")
        addr = int(addr)
        self.registers[addr] = self.accumulator
        print(f'accumulator is now {self.accumulator}')
        return
    
    '''Arithmetic operations'''
    
    def add(self, addr):
        '''Adds a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator)'''
        self.log.append(f"The word in the accumulator was added to the word in address: {str(addr).zfill(2)} and stored back in the accumulator")
        print("add")
        return
    
    def subtract(self, addr):
        '''Subtracts a word from a specific location in memory from the word in the accumulator (leaves the result in the accumulator)'''
        self.log.append(f"The word in the accumulator was subtracted with the word in address: {str(addr).zfill(2)} and stored back in the accumulator")
        print("subtract")
        return
    
    def divide(self, addr):
        '''Divides the word in the accumulator by a word from a specific location in memory (leaves the result in the accumulator).'''
        self.log.append(f"The word in the accumulator was divided by the word in address: {str(addr).zfill(2)} and stored back in the accumulator")
        print("divide")
        return
    
    def multiply(self, addr):
        '''Multiplies a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator).'''
        self.log.append(f"The word in the accumulator was multiplied by the word in address: {str(addr).zfill(2)} and stored back in the accumulator")
        print("multiply")
        return
    
    '''Control operations'''

    def branch(self, addr):
        '''Branches to a specific location in memory.'''
        self.log.append(f"Program branched to address: {str(addr).zfill(2)}")
        print("branch")
        return
    
    def branch_neg(self, addr):
        '''Branches to a specific location in memory if the accumulator is negative.'''
        if int(self.accumulator) < 0:
            self.log.append(f"Program branched to address: {str(addr).zfill(2)} since the accumulator was negative({self.accumulator})")
        print("branch_neg")
        return
    
    def branch_zero(self, addr):
        '''Branches to a specific location in memory if the accumulator is zero.'''
        if int(self.accumulator) == "0000":
            self.log.append(f"Program branched to address: {str(addr).zfill(2)} since the accumulator was zero({self.accumulator})")
        print("branch_zero")
        return
    
    def halt(self):
        '''Halts the program.'''
        self.log.append(f"Program was halted")
        print("halt")
        return False
    
def invalid_instruction(instruction):
    '''If the instruction is invalid, it asks the user if they want to continue from the next instruction or end the program'''
    print(f"{instruction} is an invalid instruction")
    while True:
        choice = input("Would you like to continue from the next instruction? (y/n): ").lower()
        if choice == "y":
            return True
        elif choice == "n":
            return False
        else:
            print("Invalid input, try again.")

def simulator_run(file_name, report_num):
    '''Runs all functions required from the simulator'''
    insta = Simulator() #Creates a new instance of the simulator
    success = False
    while not success: #Checks if file exists, and opens it. If it doesn't exist, it asks for a new file name.
        success = insta.open_file(file_name)
        if not success:
            file_name = input("Enter the name of the file: ")
    insta.run() #Runs the simulator
    insta.report(report_num) #Creates a report of the simulator run


def main():
    '''Main function'''
    report_num = 1 #Keep track of the number of reports so we don't overwrite previous reports
    if len(argv) < 2: #Checks if the user entered a file name, if not, it asks for one.
        file_name = input("Enter the name of the file: ")
    else:
        file_name = argv[1]
    simulator_run(file_name, report_num) #Runs the first simulator instance

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