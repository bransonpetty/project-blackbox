'''
Future boilerplate
'''

import os


class Simulator:
    '''Holds the list of commands and simulator functions'''
    def __init__(self):
        self.registers = {} #Initializes the registers
        self.accumulator = "+0000" #Initializes the accumulator
        self.instructions = ["10", "11", "20", "21", "30", "31", "32", "33", "40", "41", "42", "43"] #Lists all the valid instructions
        self.log = [] #Creates a log list of all the operations

        for i in range(100): #Creates the registers using a dictionary
            self.registers[i] = "+0000"

    def open_file(self, file_name):
        if os.path.exists(file_name):
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
            print("File does not exist")
            return False
        
    def run(self):
        '''Runs each line of the simulator and calls the controller for the appropriate instructions'''
        curr_addr = 0 #The current address in the simulator
        choice = True #Stops while loop if user aborts or halts
        while curr_addr < 100 and choice:
            choice = self.controller(self.registers[curr_addr][1:3], self.registers[curr_addr][1:-3]) #Sends instruction code and address to controller
            curr_addr += 1 #Moves to next address
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
    
    def read(self, addr):
        '''Reads a word from the keyboard into a specific location in memory.'''
        self.log.append(f"Word was read from keyboard into address: {addr}")
        print("read")
        return
    
    def write(self, addr):
        '''Writes a word from a specific location in memory to screen.'''
        self.log.append(f"Word was written to screen from address: {addr}")
        print("write")
        return
    
    def load(self, addr):
        '''Loads a word from a specific location in memory into the accumulator.'''
        self.log.append(f"Word was loaded to the accumulator from address: {addr}")
        print("load")
        return
    
    def store(self, addr):
        '''Stores a word from the accumulator into a specific location in memory.'''
        self.log.append(f"Word was stored from the accumulator into address: {addr}")
        print("store")
        return
    
    def add(self, addr):
        '''Adds a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator)'''
        self.log.append(f"The word in the accumulator was added to the word in address: {addr} and stored back in the accumulator")
        print("add")
        return
    
    def subtract(self, addr):
        '''Subtracts a word from a specific location in memory from the word in the accumulator (leaves the result in the accumulator)'''
        self.log.append(f"The word in the accumulator was subtracted with the word in address: {addr} and stored back in the accumulator")
        print("subtract")
        return
    
    def divide(self, addr):
        '''Divides the word in the accumulator by a word from a specific location in memory (leaves the result in the accumulator).'''
        self.log.append(f"The word in the accumulator was divided by the word in address: {addr} and stored back in the accumulator")
        print("divide")
        return
    
    def multiply(self, addr):
        '''Multiplies a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator).'''
        self.log.append(f"The word in the accumulator was multiplied by the word in address: {addr} and stored back in the accumulator")
        print("multiply")
        return
    
    def branch(self, addr):
        '''Branches to a specific location in memory.'''
        self.log.append(f"Program branched to address: {addr}")
        print("branch")
        return
    
    def branch_neg(self, addr):
        '''Branches to a specific location in memory if the accumulator is negative.'''
        if int(self.accumulator) < 0:
            self.log.append(f"Program branched to address: {addr} since the accumulator was negative({self.accumulator})")
        print("branch_neg")
        return
    
    def branch_zero(self, addr):
        '''Branches to a specific location in memory if the accumulator is zero.'''
        if int(self.accumulator) == "0000":
            self.log.append(f"Program branched to address: {addr} since the accumulator was zero({self.accumulator})")
        print("branch_zero")
        return
    
    def halt(self):
        '''Halts the program.'''
        self.log.append(f"Program was halted")
        print("halt")
        return False
    
    def report(self):
        '''Reports a log of operations and all of the instructions present in the registers and accumulator.'''
        with open("report.txt", "w") as report_file:
            report_file.write("PROGRAM REPORT:\n\n")
            report_file.write("Log of operations performed:\n\n")
            for op in self.log:
                report_file.write(f"{op}\n")
            
            reg_end = 99
            for i in reversed(range(100)):
                if self.registers[i] != "+0000":
                    reg_end = i
                    break
            
            report_file.write("\nFinal state of the registry:\n\n")
            for i in range(reg_end + 1):
                report_file.write(f"{str(i).zfill(2)}: {self.registers[i]}\n")

            report_file.write(f"\nFinal value of the accumulator: {self.accumulator}\n")
        return
    
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
            print("Invalid input")

def main():
    '''Main function'''
    insta = Simulator()
    insta.open_file('file1.txt')
    insta.run()
    insta.report()

if __name__ == "__main__":
    main()