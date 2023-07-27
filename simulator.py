'''
Project Blackbox

Designed and built by: Branson Petty, Connor Barry, Noah Potter, and Pedro Valente.

The purpose of this program is to create a functional assembly program that reads an instruction file
line by line. Executing commands and utilizing 250 registers as virtual memory that each store signed 
6 digit numbers, referred to as words, and the each of the operations.

The program was designed to only run .txt files. This decision was made to assure maximum accuracy
and to prevent the user from crashing the program by running a file type that the program wouldn't
be able to read accurately. To run your program file, make sure that the file containing the instructions
is located in the same folder as the python script. Enter the filename with the extension.

These are the instruction codes that can be used when designing your own assembly program:

I/O operations:
READ = 010 Read a word from the keyboard into a specific location in memory.
WRITE = 011 Write a word from a specific location in memory to screen.

Load/store operations:
LOAD = 020 Load a word from a specific location in memory into the accumulator.
STORE = 021 Store a word from the accumulator into a specific location in memory.

Arithmetic operations:
ADD = 030 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
SUBTRACT = 031 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
DIVIDE = 032 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
MULTIPLY = 033 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

Control operatios:
BRANCH = 040 Branch to a specific location in memory
BRANCHNEG = 041 Branch to a specific location in memory if the accumulator is negative.
BRANCHZERO = 042 Branch to a specific location in memory if the accumulator is zero.
HALT = 043 Pause the program
'''

'''Simulator  Class'''
class Simulator:
    def __init__(self):
        self.registers = {} #Initializes the registers
        self.accumulator = "+000000" #Initializes the accumulator
        self.cur_addr = 0 #Initializes the current address
        self.console_memory = ""
        self.instructions = ["000", "010", "011", "020", "021", "030", "031", "032", "033", "040", "041", "042", "043"] #Lists all the valid instructions

        for i in range(250): #Creates the registers using a dictionary
            self.registers[i] = "+000000"
            
    def read(self, addr):
        '''Reads a word from the keyboard into a specific location in memory.'''
        self.registers[int(addr)] = self.console_memory #Stores the formatted input into the desired register.
        return True
        
    def write(self, addr):
        '''Writes a word from a specific location in memory to screen.'''
        self.console_memory = self.registers[int(addr)] #Gets the word from the register.
        return True
        
    '''Load/store operations'''
    
    def load(self, addr):
        '''Loads a word from a specific location in memory into the accumulator.'''
        word = self.registers[int(addr)] #Gets the word from the register.
        self.accumulator = word #Loads the word into the accumulator.
        return True

    def store(self, addr):
        '''Stores a word from the accumulator into a specific location in memory.'''
        self.registers[int(addr)] = self.accumulator #Stores the word from the accumulator into the register.
        return True
    
    '''Arithmetic operations'''
    
    def add(self, addr):
        '''Adds a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator)'''
        result = int(self.accumulator) + int(self.registers[int(addr)]) #Adds the word from the register to the word in the accumulator.
        if result > 999999 or result < -999999: #Checks if the result is too large to be stored in the accumulator.
            return False
        #The following elif and else statements format the result to be stored in the accumulator.
        elif result > 0: 
            self.accumulator = f"+{str(result).zfill(6)}" #This could be wrong because it might add two zeros to the beginning of the number
        elif result == 0:
            self.accumulator = "+000000"
        else:
            self.accumulator = f"{str(result).zfill(6)}" #changing this to be a 6, lets see what happens
        return True

    def subtract(self, addr):
        '''Subtracts a word from a specific location in memory from the word in the accumulator (leaves the result in the accumulator)'''
        result = int(self.accumulator) - int(self.registers[int(addr)]) #Subtracts the word from the register from the word in the accumulator.
        if result > 999999 or result < -999999: #Checks if the result is too large to be stored in the accumulator.
            print(f"Overflow error on subtraction in address {addr}.\nThe result is too large to be stored in the accumulator. The program will now be terminated.")
            return False
        #The following elif and else statements format the result to be stored in the accumulator.
        elif result > 0:
            self.accumulator = f"+{str(result).zfill(6)}"#This could be wrong because it might add two zeros to the beginning of the number
        elif result == 0:
            self.accumulator = "+000000"
        else:
            self.accumulator = f"{str(result).zfill(6)}"#changing this to be a 6, lets see what happens
        return True

    def divide(self, addr):
        '''Divides the word in the accumulator by a word from a specific location in memory (leaves the result in the accumulator).'''
        result = int(self.accumulator) // int(self.registers[int(addr)]) #Divides the word in the accumulator by the word from the register.
        #NO DIVISION OPERATION SHOULD RESULT IN OVERFLOW, I'M STILL LEAVING THIS HERE IN CASE THERE IS ANY ABNORMALITY I DIDN'T PREDICT.
        if result > 999999 or result < -999999: #Checks if the result is too large to be stored in the accumulator.
            return False
        #The following elif and else statements format the result to be stored in the accumulator.
        elif result > 0:
            self.accumulator = f"+{str(result).zfill(6)}"#This could be wrong because it might add two zeros to the beginning of the number
        elif result == 0:
            self.accumulator = "+000000"
        else:
            self.accumulator = f"{str(result).zfill(6)}"#changing this to be a 6, lets see what happens
        return True

    def multiply(self, addr):
        '''Multiplies a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator).'''
        result = int(self.accumulator) * int(self.registers[int(addr)]) #Multiplies the word in the accumulator by the word from the register.
        if result > 999999 or result < -999999: #Checks if the result is too large to be stored in the accumulator.
            return False
        #The following elif and else statements format the result to be stored in the accumulator.
        elif result > 0:
            self.accumulator = f"+{str(result).zfill(6)}" #This could be wrong because it might add two zeros to the beginning of the number
        elif result == 0:
            self.accumulator = "+000000"
        else:
            self.accumulator = f"{str(result).zfill(6)}" #changing this to be a 6, lets see what happens
        return True
    
    
    '''Control operations'''

    def branch(self, addr):
        '''Branches to a specific location in memory.'''
        #Sets the current address to the address specified in the instruction.
        #It subtracts 1 from the desired address since the program moves to next location upon returning.
        self.cur_addr = int(addr) - 1
        return True
    
    def branch_neg(self, addr):
        '''Branches to a specific location in memory if the accumulator is negative.'''
        #Sets the current address to the address specified in the instruction if accumulator is negative.
        #It subtracts 1 from the desired address since the program moves to next location upon returning.
        if int(int(self.accumulator)) < 0:
            self.cur_addr = int(addr) - 1
        return True
    
    def branch_zero(self, addr):
        '''Branches to a specific location in memory if the accumulator is zero.'''
        #Sets the current address to the address specified in the instruction if accumulator is "+000000".
        #It subtracts 1 from the desired address since the program moves to next location upon returning.
        if self.accumulator == "+000000":
            self.cur_addr = int(addr) - 1
        return True
    
    def halt(self):
        '''Halts the program.'''
        return False #Returns false to stop the program.

# class Simulator:
#     '''Holds the list of commands and simulator functions'''
#     def __init__(self):
#         self.registers = {} #Initializes the registers
#         self.accumulator = "+0000" #Initializes the accumulator
#         self.cur_addr = 0 #Initializes the current address
#         self.console_memory = ""
#         self.instructions = ["00", "10", "11", "20", "21", "30", "31", "32", "33", "40", "41", "42", "43"] #Lists all the valid instructions
#         self.log = [] #Creates a log list of all the operations

#         for i in range(250): #Creates the 250 registers using a dictionary
#             self.registers[i] = "+0000"
        
#     '''I/O operations'''
    
#     def read(self, addr):
#         '''Reads a word from the keyboard into a specific location in memory.'''
#         self.log.append(f"'{self.console_memory}' was read from keyboard into address: {str(addr).zfill(2)}") #Logs the operation.
#         self.registers[int(addr)] = self.console_memory #Stores the formatted input into the desired register.
#         return True
    
#     def write(self, addr):
#         '''Writes a word from a specific location in memory to screen.'''
#         self.console_memory = self.registers[int(addr)] #Gets the word from the register.
#         self.log.append(f"{self.console_memory} was written to screen from address: {str(addr).zfill(2)}") #Logs the operation.
#         return True
     
#     '''Load/store operations'''
    
#     def load(self, addr):
#         '''Loads a word from a specific location in memory into the accumulator.'''
#         word = self.registers[int(addr)] #Gets the word from the register.
#         self.log.append(f"{word} was loaded to the accumulator from address: {str(addr).zfill(2)}") #Logs the operation.
#         self.accumulator = word #Loads the word into the accumulator.
#         return True
    
#     def store(self, addr):
#         '''Stores a word from the accumulator into a specific location in memory.'''
#         self.log.append(f"{self.accumulator} was stored from the accumulator into address: {str(addr).zfill(2)}") #Logs the operation.
#         self.registers[int(addr)] = self.accumulator #Stores the word from the accumulator into the register.
#         return True
    
#     '''Arithmetic operations'''
    
#     def add(self, addr):
#         '''Adds a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator)'''
#         intial_acc = self.accumulator #Saves the initial value of the accumulator for the log.
#         result = int(self.accumulator) + int(self.registers[int(addr)]) #Adds the word from the register to the word in the accumulator.
#         if result > 9999 or result < -9999: #Checks if the result is too large to be stored in the accumulator.
#             print(f"Overflow error on addition in address {addr}.\nThe result is too large to be stored in the accumulator. The program will now be terminated.")
#             self.log.append(f"Overflow error on addition in address {addr}. The result is too large to be stored in the accumulator.")
#             return False
#         #The following elif and else statements format the result to be stored in the accumulator.
#         elif result > 0: 
#             self.accumulator = f"+{str(result).zfill(4)}"
#         elif result == 0:
#             self.accumulator = "+0000"
#         else:
#             self.accumulator = f"{str(result).zfill(5)}" 
#         #It's a long log entry, but is usefull to see what happened.
#         self.log.append(f"{intial_acc} from the accumulator was added to {self.registers[int(addr)]} from address: {str(addr).zfill(2)} and result ({self.accumulator}) was stored back in the accumulator")
#         return True
    
#     def subtract(self, addr):
#         '''Subtracts a word from a specific location in memory from the word in the accumulator (leaves the result in the accumulator)'''
#         intial_acc = self.accumulator #Saves the initial value of the accumulator for the log.
#         result = int(self.accumulator) - int(self.registers[int(addr)]) #Subtracts the word from the register from the word in the accumulator.
#         if result > 9999 or result < -9999: #Checks if the result is too large to be stored in the accumulator.
#             print(f"Overflow error on subtraction in address {addr}.\nThe result is too large to be stored in the accumulator. The program will now be terminated.")
#             self.log.append(f"Overflow error on subtraction in address {addr}. The result is too large to be stored in the accumulator.")
#             return False
#         #The following elif and else statements format the result to be stored in the accumulator.
#         elif result > 0:
#             self.accumulator = f"+{str(result).zfill(4)}"
#         elif result == 0:
#             self.accumulator = "+0000"
#         else:
#             self.accumulator = f"{str(result).zfill(5)}"
#         #It's a long log entry, but is usefull to see what happened.
#         self.log.append(f"{intial_acc} from the accumulator was subtracted by {self.registers[int(addr)]} from address: {str(addr).zfill(2)} and result ({self.accumulator}) was stored back in the accumulator")
#         return True
    
#     def divide(self, addr):
#         '''Divides the word in the accumulator by a word from a specific location in memory (leaves the result in the accumulator).'''
#         intial_acc = self.accumulator #Saves the initial value of the accumulator for the log.
#         result = int(self.accumulator) // int(self.registers[int(addr)]) #Divides the word in the accumulator by the word from the register.
#         #NO DIVISION OPERATION SHOULD RESULT IN OVERFLOW, I'M STILL LEAVING THIS HERE IN CASE THERE IS ANY ABNORMALITY I DIDN'T PREDICT.
#         if result > 9999 or result < -9999: #Checks if the result is too large to be stored in the accumulator.
#             print(f"Overflow error on division in address {addr}.\nThe result is too large to be stored in the accumulator. The program will now be terminated.")
#             self.log.append(f"Overflow error on division in address {addr}. The result is too large to be stored in the accumulator.")
#             return False
#         #The following elif and else statements format the result to be stored in the accumulator.
#         elif result > 0:
#             self.accumulator = f"+{str(result).zfill(4)}"
#         elif result == 0:
#             self.accumulator = "+0000"
#         else:
#             self.accumulator = f"{str(result).zfill(5)}"
#         #It's a long log entry, but is usefull to see what happened.
#         self.log.append(f"{intial_acc} from the accumulator was divided by {self.registers[int(addr)]} from address: {str(addr).zfill(2)} and result ({self.accumulator}) was stored back in the accumulator")
#         return True
    
#     def multiply(self, addr):
#         '''Multiplies a word from a specific location in memory to the word in the accumulator (leaves the result in the accumulator).'''
#         intial_acc = self.accumulator #Saves the initial value of the accumulator for the log.
#         result = int(self.accumulator) * int(self.registers[int(addr)]) #Multiplies the word in the accumulator by the word from the register.
#         if result > 9999 or result < -9999: #Checks if the result is too large to be stored in the accumulator.
#             print(f"Overflow error on multiplication in address {addr}.\nThe result is too large to be stored in the accumulator. The program will now be terminated.")
#             self.log.append(f"Overflow error on multiplication in address {addr}. The result is too large to be stored in the accumulator.")
#             return False
#         #The following elif and else statements format the result to be stored in the accumulator.
#         elif result > 0:
#             self.accumulator = f"+{str(result).zfill(4)}"
#         elif result == 0:
#             self.accumulator = "+0000"
#         else:
#             self.accumulator = f"{str(result).zfill(5)}"
#         #It's a long log entry, but is usefull to see what happened.
#         self.log.append(f"{intial_acc} from the accumulator was multiplied by {self.registers[int(addr)]} from address: {str(addr).zfill(2)} and result ({self.accumulator}) was stored back in the accumulator")
#         return True
    
#     '''Control operations'''

#     def branch(self, addr):
#         '''Branches to a specific location in memory.'''
#         #Sets the current address to the address specified in the instruction.
#         #It subtracts 1 from the desired address since the program moves to next location upon returning.
#         self.cur_addr = int(addr) - 1
#         self.log.append(f"Program branched to address: {str(addr).zfill(2)}") #Logs the operation
#         return True
    
#     def branch_neg(self, addr):
#         '''Branches to a specific location in memory if the accumulator is negative.'''
#         #Sets the current address to the address specified in the instruction if accumulator is negative.
#         #It subtracts 1 from the desired address since the program moves to next location upon returning.
#         if int(int(self.accumulator)) < 0:
#             self.cur_addr = int(addr) - 1
#             self.log.append(f"Program branched to address: {str(addr).zfill(2)} since the accumulator was negative({self.accumulator})") #Logs the operation
#         return True
    
#     def branch_zero(self, addr):
#         '''Branches to a specific location in memory if the accumulator is zero.'''
#         #Sets the current address to the address specified in the instruction if accumulator is "+0000".
#         #It subtracts 1 from the desired address since the program moves to next location upon returning.
#         if self.accumulator == "+0000":
#             self.cur_addr = int(addr) - 1
#             self.log.append(f"Program branched to address: {str(addr).zfill(2)} since the accumulator was zero({self.accumulator})") #Logs the operation
#         return True
    
#     def halt(self):
#         '''Halts the program.'''
#         self.log.append(f"Program was halted")
#         return False #Returns false to stop the program.