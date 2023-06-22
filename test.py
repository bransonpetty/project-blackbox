'''
PROJECT BLACKBOX UNIT TESTS
All tests were performed through pytest. 
In order to run the tests open the terminal in this directory and enter the following command:

python -m pytest test.py

A few observations about the tests:
- The "controller" function is not tested as it is hard to test it by itself. However, controller is tested indirectly through the other tests.
- The "main" and "simulation_run" functions were not tested as they are part of the Terminal UI and they would be too complex to test.
'''
import pytest
import mock
import builtins
import os
from simulator import *
# python -m pytest test.py
 

'''TESTS FOR "open_file" FUNCTION'''

def test_file_success():
    '''Creates a mock file and tests with the Simulator class can read the lines
    correctly into the registers'''
    instructions = ['+1000', "\n+2000", "\n+3000", "\n+4000"] #Instructions to be stored in the file.
    with open("pytest_file.txt", "w") as test_file: #Creates the mock files
        test_file.writelines(instructions)
    
    temp = Simulator()
    temp.open_file("pytest_file.txt") #Test the open_file function
    #It passes if all the instructions are in the correct registers.
    assert temp.registers[0] == "+1000"
    assert temp.registers[1] == "+2000"
    assert temp.registers[2] == "+3000"
    assert temp.registers[3] == "+4000"

    os.remove("pytest_file.txt") #Deletes the mock file after tests are done

def test_no_file():
    '''Tests if open_file returns false if file doesn't exist'''
    temp = Simulator()
    assert temp.open_file("BADNAME.txt") == False

def test_incompatible_file():
    '''Tests with open_file returns false if file is an incompatible format'''
    with open('test.csv', 'w') as test_file: #Created fake file for test
        test_file.write("test") #Content doesn't matter since it shouldn't read it.
    
    temp = Simulator()
    assert temp.open_file("test.csv") == False

    os.remove("test.csv") #Deletes the mock file after tests are done

'''TESTS FOR "run" FUNCTION'''

def test_run_success():
    '''Tests if run function runs properly'''
    instructions = ["+2003", "\n+2104", "\n+4300", "\n+1234"] #Instructions to be stored in the file.
    with open("pytest_file.txt", "w") as test_file: #Creates the mock files
        test_file.writelines(instructions)
    
    temp = Simulator()
    temp.open_file("pytest_file.txt")
    temp.run()
    #Checks if all the registers and accumulator are what they are supposed to be after run.
    assert temp.registers[0] == "+2003"
    assert temp.registers[1] == "+2104"
    assert temp.registers[2] == "+4300"
    assert temp.registers[3] == "+1234"
    assert temp.registers[4] == "+1234"
    assert temp.accumulator == "+1234"

    os.remove("pytest_file.txt") #Deletes the mock file after tests are done

def test_run_bad_instruction_stop():
    '''Tests if user can cancel if an instruction is invalid (Register 01: "+8704" is invalid)'''
    instructions = ["+2003", "\n+8704", "\n+4300", "\n+1234"] #Instructions to be stored in the file.
    with open("pytest_file.txt", "w") as test_file: #Creates the mock files
        test_file.writelines(instructions)
    
    temp = Simulator()
    temp.open_file("pytest_file.txt")
    #This simulates the users inputing 'n' when they are asked if they want to continue or not.
    with mock.patch.object(builtins, 'input', lambda _: 'n'):
        temp.run()
    #Checks if all the registers and accumulator are what they are supposed to be after run is cancelled.
    assert temp.registers[0] == "+2003"
    assert temp.registers[1] == "+8704"
    assert temp.registers[2] == "+4300"
    assert temp.registers[3] == "+1234"
    assert temp.registers[4] == "+0000"
    assert temp.accumulator == "+1234"

    os.remove("pytest_file.txt") #Deletes the mock file after tests are done

def test_run_bad_instruction_continue():
    '''Tests if user can continue running the rest of the program if an instruction is invalid (Register 01: "+8704" is invalid)'''
    instructions = ["+2004", "\n+8704", "\n+2105", "\n+4300", "\n+1234"] #Instructions to be stored in the file.
    with open("pytest_file.txt", "w") as test_file: #Creates the mock files
        test_file.writelines(instructions)
    
    temp = Simulator()
    temp.open_file("pytest_file.txt")
    #This simulates the users inputing 'y' when they are asked if they want to continue or not.
    with mock.patch.object(builtins, 'input', lambda _: 'y'):
        temp.run()
    #Checks if all the registers and accumulator are what they are supposed to be after run is completed.
    assert temp.registers[0] == "+2004"
    assert temp.registers[1] == "+8704"
    assert temp.registers[2] == "+2105"
    assert temp.registers[3] == "+4300"
    assert temp.registers[4] == "+1234"
    assert temp.registers[5] == "+1234"
    assert temp.accumulator == "+1234"

    os.remove("pytest_file.txt") #Deletes the mock file after tests are done

def test_run_stops_at_halt():
    '''Tests if the run function stops when it reaches halt. If test 
    succeeds instruction +2104 won't run and register 4 will be empty'''
    instructions = ["+2003", "\n+4300", "\n+2104", "\n+1234"] #Instructions to be stored in the file.
    with open("pytest_file.txt", "w") as test_file: #Creates the mock files
        test_file.writelines(instructions)
    
    temp = Simulator()
    temp.open_file("pytest_file.txt")
    temp.run()
    #Checks if all the registers and accumulator are what they are supposed to be after run is completed.
    assert temp.registers[0] == "+2003"
    assert temp.registers[1] == "+4300"
    assert temp.registers[2] == "+2104"
    assert temp.registers[3] == "+1234"
    assert temp.registers[4] == "+0000"
    assert temp.accumulator == "+1234"

    os.remove("pytest_file.txt") #Deletes the mock file after tests are done

'''TEST FOR "report" FUNCTION'''

def test_report_success():
    '''Tests with report file is generated. It won't test what 
    is inside as that might be changed as the program evolves'''
    temp = Simulator()
    temp.report(99)
    assert os.path.isfile("Report(99).txt")
    os.remove("Report(99).txt")

'''TESTS FOR "invalid_instruction" function'''

def test_invalid_cancel():
    '''Tests if function returns False to terminate the program'''
    temp = Simulator()
    #Simulates user inputting "n" to terminate the program
    with mock.patch.object(builtins, 'input', lambda _: 'n'):
        assert temp.invalid_instruction("87") == False

def test_invalid_continue():
    '''Tests if function returns True to continue program from next line'''
    temp = Simulator()
    #Simulates user inputting "y" to continue the program
    with mock.patch.object(builtins, 'input', lambda _: 'y'):
        assert temp.invalid_instruction("87") == True

'''TESTS FOR "format_input" FUNCTION'''

def test_format_input_validation():
    '''Tests if function accounts for bad inputs correctly'''
    temp = Simulator()
    #Error Cases:
    assert temp.format_input("12345") == "-1" #Positive numbers with more than 5 digits
    assert temp.format_input("hello") == "-1" #Non numeric entries
    assert temp.format_input("-123") == "-1" #Negative numbers with only 3 digits
    assert temp.format_input("") == "-1" #No input
    #Successful Cases:
    assert temp.format_input("+1234") == "+1234" #Valid positive number
    assert temp.format_input("+0000") == "+0000" #Valid zero entry
    assert temp.format_input("-1234") == "-1234" #Valid negative entry

def test_format_input_formating():
    '''Tests with the function corrects user input if is valid but not formatted correctly'''
    temp = Simulator()
    #Cases:
    assert temp.format_input("1234") == "+1234" #Positive number without + sign
    assert temp.format_input("0000") == "+0000" #Zero without + sign

'''INSTRUCTION FUNCTION TESTS'''
'''TESTS FOR "read" INSTRUCTION FUNCTION'''

def test_read_success():
    '''Tests if function successfully reads user input into desired register'''
    #Simulates user inputing +1000 to be stored in register 0
    with mock.patch.object(builtins, 'input', lambda _: "+1000"):
        temp = Simulator()
        temp.read("00")
        assert temp.registers[0] == "+1000"

def test_read_one_invalid():
    temp = Simulator()
    inputs = ["hello", "+1000"]
    #First it simulates an invalid input ("hello"), than it inputs the valid word ("+1000")
    with mock.patch('builtins.input', side_effect=inputs):
        temp.read("00")
    assert temp.registers[0] == "+1000" #If it stores the second value ("+1000"), its successful

'''TEST FOR "write" INSTRUCTION UNCTION'''

def test_write_success(capfd):
    '''Tests if function successfully writes word to screen'''
    temp = Simulator()
    temp.registers[0] = "+1000"
    temp.write("00")
    out, err = capfd.readouterr() #Captures what is printed to the console
    assert out[:5] == "+1000" #Had to specify that it's the 5 first digits as it also captures the newline character (\n)

'''TEST FOR "load" INSTRUCTION FUNCTION'''

def test_load_success():
    '''Tests if function successfully loads word from register to the accumulator'''
    temp = Simulator()
    temp.registers[0] = "+1000"
    temp.load("00")
    assert temp.accumulator == "+1000"

'''TEST FOR "store" INSTRUCTION FUNCTION'''

def test_store_success():
    '''Tests if function successfully stores word from the accumulator to a location in the registers'''
    temp = Simulator()
    temp.accumulator = "+1000"
    temp.store("00")
    assert temp.registers[0] == "+1000"

'''TESTS FOR "add" INSTRUCTION FUNCTION'''

def test_add_success():
    '''Tests if function adds successfully'''
    temp = Simulator()
    temp.registers[0] = "+1234"
    temp.accumulator = "+4321"
    temp.add("00")
    assert temp.accumulator == "+5555"

def test_add_overflow():
    '''Tests if function returns false in case add results in overflow'''
    temp = Simulator()
    temp.registers[0] = "+5000"
    temp.accumulator = "+5000"
    assert temp.add("00") == False #Tests for positive overflow
    temp.registers[0] = "-5000"
    temp.accumulator = "-5000"
    assert temp.add("00") == False #Tests for negative overflow

def test_add_zero():
    '''Tests if function stores 0 in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "-1000"
    temp.accumulator = "+1000"
    temp.add("00")
    assert temp.accumulator == ("+0000")

def test_add_negative():
    '''Tests if function stores negative values in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "-1000"
    temp.accumulator = "-1000"
    temp.add("00")
    assert temp.accumulator == "-2000"

'''TESTS FOR "subtract" INSTRUCTION FUNCTION'''

def test_subtract_success():
    '''Tests if function subtracts successfully'''
    temp = Simulator()
    temp.registers[0] = "+1234"
    temp.accumulator = "+4321"
    temp.subtract("00")
    assert temp.accumulator == "+3087"

def test_subtract_overflow():
    '''Tests if function returns false in case subtract results in overflow'''
    temp = Simulator()
    temp.registers[0] = "-5000"
    temp.accumulator = "+5000"
    assert temp.subtract("00") == False #Tests for positive overflow
    temp.registers[0] = "+5000"
    temp.accumulator = "-5000"
    assert temp.subtract("00") == False #Tests for negative overflow

def test_subtract_zero():
    '''Tests if function stores 0 in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "+1000"
    temp.accumulator = "+1000"
    temp.subtract("00")
    assert temp.accumulator == ("+0000")

def test_subtract_negative():
    '''Tests if function stores negative values in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "+1000"
    temp.accumulator = "-1000"
    temp.subtract("00")
    assert temp.accumulator == "-2000"

'''TESTS FOR "divide" INSTRUCTION FUNCTION'''

def test_divide_success():
    '''Tests if function divide successfully'''
    temp = Simulator()
    temp.registers[0] = "+0002"
    temp.accumulator = "+2000"
    temp.divide("00")
    assert temp.accumulator == "+1000"

#THE "divide" FUNCTION ACCOUNTS FOR OVERFLOWS JUST TO BE OVERLY CAUTIOUS.
#HOWEVER, IT SHOULDN'T BE POSSIBLE TO HAVE AN OVERFLOW IN A DIVISION OPERATION.

def test_divide_zero():
    '''Tests if function stores 0 in the divide correctly'''
    temp = Simulator()
    temp.registers[0] = "+0001"
    temp.accumulator = "+0000"
    temp.divide("00")
    assert temp.accumulator == ("+0000")

def test_divide_negative():
    '''Tests if function stores negative values in the divide correctly'''
    temp = Simulator()
    temp.registers[0] = "+0001"
    temp.accumulator = "-0500"
    temp.divide("00")
    assert temp.accumulator == "-0500"

'''TESTS FOR "multiply" INSTRUCTION FUNCTION'''

def test_multiply_success():
    '''Tests if function multiplies successfully'''
    temp = Simulator()
    temp.registers[0] = "+0002"
    temp.accumulator = "+2000"
    temp.multiply("00")
    assert temp.accumulator == "+4000"

def test_multiply_overflow():
    '''Tests if function returns false in case multiply results in overflow'''
    temp = Simulator()
    temp.registers[0] = "+0002"
    temp.accumulator = "+5000"
    assert temp.multiply("00") == False #Tests for positive overflow
    temp.registers[0] = "+0002"
    temp.accumulator = "-5000"
    assert temp.multiply("00") == False #Tests for negative overflow

def test_multiply_zero():
    '''Tests if function stores 0 in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "+1000"
    temp.accumulator = "+0000"
    temp.multiply("00")
    assert temp.accumulator == ("+0000")

def test_multiply_negative():
    '''Tests if function stores negative values in the accumulator correctly'''
    temp = Simulator()
    temp.registers[0] = "+0002"
    temp.accumulator = "-1000"
    temp.multiply("00")
    assert temp.accumulator == "-2000"

'''TEST FOR "branch" INSTRUCTION FUNCTION'''

def test_branch_success():
    '''Tests if function successfully branches to a new register address'''
    temp = Simulator()
    temp.branch("90")
    #It's one less than the desired location since once the function returns cur_addr is incremented by 1.
    assert temp.cur_addr == 89 

'''TESTS FOR "branch_neg" INSTRUCTION FUNCTION'''

def test_branch_neg_move():
    '''Tests if the function moves when accumulator is negative'''
    temp = Simulator()
    temp.accumulator = "-1000"
    temp.branch_neg("90")
    #It's one less than the desired location since once the function returns cur_addr is incremented by 1.
    assert temp.cur_addr == 89

def test_branch_neg_stay():
    '''Tests if the function does not move to another address when accumulator is not negative'''
    temp = Simulator()
    temp.accumulator = "+1000"
    temp.branch_neg("90")
    assert temp.cur_addr == 0

'''TESTS FOR "branch_zero" INSTRUCTION FUNCTION'''

def test_branch_zero_move():
    '''Tests if the function moves when accumulator is zero'''
    temp = Simulator()
    #Accumulator is zero by default
    temp.branch_zero("90")
    #It's one less than the desired location since once the function returns cur_addr is incremented by 1.
    assert temp.cur_addr == 89

def test_branch_zero_stay():
    '''Tests if the function does not move to another address when accumulator is not zero'''
    temp = Simulator()
    temp.accumulator = "+1000"
    temp.branch_zero("90")
    assert temp.cur_addr == 0

'''TEST FOR "halt" INSTRUCTION FUNCTION'''

def test_halt_success():
    '''Tests if function returns False to terminate program'''
    temp = Simulator()
    assert temp.halt() == False