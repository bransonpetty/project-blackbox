# Design Documentation

The purpose of this program is to create a functional assembly program that reads an instruction file
line by line. Executing commands and utilizing 100 registers as virtual memory that each store signed 
4 digit numbers, referred to as words, and the each of the operations.

The program was designed to only run .txt files. This decision was made to assure maximum accuracy
and to prevent the user from crashing the program by running a file type that the program wouldn't
be able to read accurately. To run your program file, make sure that the file containing the instructions
is located in the same folder as the python script. Enter the filename with the extension.

A few things to keep in mind while using the program:
- You must use a halt instruction at the end of the program routine you mean to run. That will prevent
unwanted instructions from being performed. If no halt instruction is present the program will run 
every register until it reaches register 99.
- If an invalid instruction is entered you will be informed about the register containing the bad
instruction and given the option to continue from the next register. If you wish to stop the program
at that point, a report file is generated and contains a log of operations and the final state of the
registers.
- Any empty register will be skipped by the compiler until the end is reached.
- After you done running a program file, you will be given the option of running another one.
- After all the desired files are ran, report files will be generated on the program folder.
- If you decide to run the program again, your past reports will be overwritten. Make sure to save them
by moving them to a different location or renaming them if they are important to you.

How to run the program:

'''shell
python main.py (filename).txt
'''

User Stories:
Brian has taken an interest in computer science and wants to understand at a base level how assembly
instructions work. He is able to write short instruction files to learn how each of them work and 
eventually how to preform multiple successive functions.

Justin is designing a program on his raspberry pi. Because the raspberry pi doesn't have much in the
way of memory he needs to design a program at the lowest level to improve memory and preformance. 
For easier testing than running his long instruction programs on his raspberry pi he is able to run
this program from his computer and use the debugger to watch each register as a line of instruction
is read.

Use Cases: 

- ADD (30xx) - We load the number 8 from a register and add it to the accumulator which has the value
    6 in it previously. Once the operation has finished the accumulator will have the value of 14
- SUBTRACT (31xx) - We load the number 2 from a register and subract it from the accumulator value of
    5 leaving the accumulator with a value of 3.
- Using READ and MULTIPLY together the program can take a value from the user and load it into a 
    register that can then be multiplyed by the accumulator value.
- Using BRANCHNEG we can check the accumulator for a negative value. If the accumulator is negative
    value we can issue a HALT command to branch to so the program quits.
- Using READ and LOAD we can manually set the accumulator value by reading the user input into a 
    register that LOAD can then reference to manually set the accumulator value.
- The STORE operation can be used to copy the accumulator value into a register. This can be used to
    temporarily alter the value and revert back using LOAD.
- After preforming an arithmetic operation we want to return the value so we will use the LOAD and 
    WRITE functions to pull the value from the accumulator into a register and then write it to the console.
- Using READ and WRITE we can echo a users input by returning the value immediately following it's input.
- BRANCH, BRANCHNEG, and BRANCHZERO can be used for loops and conditionals by altering the accumulator
    value.
- Using READ and DIVIDE we can take the user input and divide the accumulator value by the user input.

