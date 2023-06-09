# Project Blackbox

The purpose of this program is to create a functional assembly program that reads an instruction file
line by line. Executing commands and utilizing 100 registers as virtual memory that each store signed 
4 digit numbers, referred to as words, and the each of the operations.

The program was designed to only run .txt files. This decision was made to assure maximum accuracy
and to prevent the user from crashing the program by running a file type that the program wouldn't
be able to read accurately. To run your program file, make sure that the file containing the instructions
is located in the same folder as the python script. Enter the filename with the extension.

## A few things to keep in mind while using the program:
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

## How to run the program:

You may run the program by opening the command shell in the directory containing both the program
python script and your instructions file and running the command bellow. Where (filename) is the
name of the file containing your instructions:

```shell
python main.py (filename).txt
```
Example: python main.pt file.txt

You may also opt to simply run the program without the file name. In this case, the program will
simply prompt you to input the file name with extension before running. Example bellow:

 ```shell
python main.py (filename).txt
```

File should include a 4 digit operator on each line. The filename
argument can be placed immediately after the run statement, or
after the run statement a prompt will display.