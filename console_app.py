from simulator import Simulator
import os
from sys import argv

class C_Controller:

    def __init__(self):
        self.simu_instance = Simulator()

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
                            self.simu_instance.registers[addr] = line
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
        while self.simu_instance.cur_addr < 100 and choice:
            choice = self.controller(self.simu_instance.registers[self.simu_instance.cur_addr][1:3], self.simu_instance.registers[self.simu_instance.cur_addr][3:]) #Sends instruction code and address to controller
            self.simu_instance.cur_addr += 1 #Moves to next address
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
            choice = self.simu_instance.load(addr)
        elif instruction == "21":
            choice = self.simu_instance.store(addr)
        elif instruction == "30":
            choice = self.simu_instance.add(addr)
        elif instruction == "31":
            choice = self.simu_instance.subtract(addr)
        elif instruction == "32":
            choice = self.simu_instance.divide(addr)
        elif instruction == "33":
            choice = self.simu_instance.multiply(addr)
        elif instruction == "40":
            choice = self.simu_instance.branch(addr)
        elif instruction == "41":
            choice = self.simu_instance.branch_neg(addr)
        elif instruction == "42":
            choice = self.simu_instance.branch_zero(addr)
        elif instruction == "43":
            choice = self.simu_instance.halt()

        return choice
    
    def report(self, report_num):
        '''Reports a log of operations and all of the instructions present in the registers and accumulator.'''
        with open(f"Report({report_num}).txt", "w") as report_file: #Creates a new file for the report
            report_file.write("PROGRAM REPORT:\n\n")
            report_file.write("Log of operations performed:\n\n") #Writes the log of operations to the file
            for op in self.simu_instance.log:
                report_file.write(f"{op}\n")
            
            reg_end = 99
            for i in reversed(range(100)): #Finds the last register that was used so we don't write all 100 registers to the file.
                if self.simu_instance.registers[i] != "+0000":
                    reg_end = i
                    break
            
            report_file.write("\nFinal state of the registry:\n\n") 
            for i in range(reg_end + 1): #Writes the final state of the registers to the file
                report_file.write(f"{str(i).zfill(2)}: {self.simu_instance.registers[i]}\n")

            report_file.write(f"\nFinal value of the accumulator: {self.simu_instance.accumulator}\n") #Writes the final value of the accumulator to the file
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
    
    def format_read(self, addr):
        '''Validates the input for the address'''
        user_input = input(f'Enter a positive or negative 4 digit number into memory register {addr} (ex: +1234 or -4321): ')
        #From this point down, we validate and format the user input to be stored properly in the registers.
        #If user entered a positive value or "0000" without a +, it will be added. And it will check if entered a 4 digit number.
        #Negative values must be entered with a - to be valid. Validated and formated input will be stored in formatted_input.
        success = False
        while not success:
            try:
                if len(user_input) == 0:
                    print("No input. Please enter a valid positive or negative 4 digit number.")
                    user_input = input(f'Enter a positive or negative 4 digit number into memory register {addr} (ex: +1234 or -4321): ')
                elif user_input[0] == "-" or user_input[0] == "+": #It first checks if a operation sign is present.
                    if len(user_input) == 5: #If it is, it checks if the number is 4 digits long.
                        user_int = int(user_input) #If it can't parse, it's not a number. A ValueError is raised.
                        self.simu_instance.console_memory = user_int
                        self.simu_instance.read(addr)
                        success = True
                    else:
                        print("Invalid input. Please enter a valid positive or negative 4 digit number.")
                        user_input = input(f'Enter a positive or negative 4 digit number into memory register {addr} (ex: +1234 or -4321): ')
                elif user_input == "0000": #If 0000 is entered without a sign, we return it with the + sign..
                    return "+0000"
                elif len(user_input) == 4:
                    user_int = int(user_input) #if it's 4 digits long and it can parse, it's a valid positive number.
                    self.simu_instance.console_memory = f"+{user_input}" #We add the plus sign and add it to the memory.
                    self.simu_instance.read(addr)
                    success = True
                else:
                    print("Invalid input. Please enter a valid positive or negative 4 digit number.")
                    user_input = input(f'Enter a positive or negative 4 digit number into memory register {addr} (ex: +1234 or -4321): ')
            except ValueError:
                print("Invalid input. Please enter a valid positive or negative 4 digit number.")
                user_input = input(f'Enter a positive or negative 4 digit number into memory register {addr} (ex: +1234 or -4321): ')
        
        return True

    def console_write(self, addr):
        self.simu_instance.write(addr)
        print(self.simu_instance.console_memory)

'''Main functions'''

def simulator_run(file_name, report_num):
    '''Runs all functions required from the simulator'''
    insta = C_Controller() #Creates a new instance of the simulator
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