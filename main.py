'''
Future boilerplate
'''

class Simulator:
    '''Holds the list of commands and simulator functions'''
    def __init__(self):
        self.registers = {} #Initializes the registers
        self.accumulator = "0000" #Initializes the accumulator
        self.instructions = ["10", "11", "20", "21", "30", "31", "32", "33", "40", "41", "42", "43"] #Lists all the valid instructions

        for i in range(100): #Creates the registers using a dictionary
            self.registers[i] = "0000"

    def open_file(self, file_name):
        try:
            with open(file_name) as input_file:
                addr = 0 
                for line in input_file:
                    line = line.strip()
                    #make sure its a + or a -
                    if line[0] == '+' or line[0] == '-':
                        opcode = line[1:3]       #10
                        complete_code = line[1:] #1007
                        if len(complete_code) == 4: #CHECKS TO SEE IF THE TOTAL CODE IS LENGTH OF 4 (EX. 1007)
                            source = line[3:] #07
                            self.registers[addr] = complete_code
                            addr += 1
            return True
        except:
            return False
        
    def run(self):
        '''Runs each line of the simulator and calls the controller for the appropriate instructions'''
        curr_addr = 0 #The current address in the simulator
        choice = True #Stops while loop if user aborts or halts
        while curr_addr < 100 and choice:
            choice = self.controller(self.registers[curr_addr][:2], self.registers[curr_addr][:-2]) #Sends instruction code and address to controller
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
        print("read")
        return
    
    def write(self, addr):
        '''Writes a word from a specific location in memory to screen.'''
        print("write")
        return
    
    def load(self, addr):
        '''Loads a word from a specific location in memory into the accumulator.'''
        print("load")
        return
    
    def store(self, addr):
        '''Stores a word from the accumulator into a specific location in memory.'''
        print("store")
        return
    
    def add(self, addr):
        '''Adds a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator)'''
        print("add")
        return
    
    def subtract(self, addr):
        '''Subtracts a word from a specific location in memory from the word in the accumulator (leaves the result in the accumulator)'''
        print("subtract")
        return
    
    def divide(self, addr):
        '''Divides the word in the accumulator by a word from a specific location in memory (leaves the result in the accumulator).'''
        print("divide")
        return
    
    def multiply(self, addr):
        '''Multiplies a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator).'''
        print("multiply")
        return
    
    def branch(self, addr):
        '''Branches to a specific location in memory.'''
        print("branch")
        return
    
    def branch_neg(self, addr):
        '''Branches to a specific location in memory if the accumulator is negative.'''
        print("branch_neg")
        return
    
    def branch_zero(self, addr):
        '''Branches to a specific location in memory if the accumulator is zero.'''
        print("branch_zero")
        return
    
    def halt(self):
        '''Halts the program.'''
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
            print("Invalid input")

def main():
    '''Main function'''
    insta = Simulator()
    insta.open_file('file1.txt')
    insta.run()

if __name__ == "__main__":
    main()