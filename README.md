# Project Blackbox

The purpose of this program is to create a functional assembly program that executes 6 bit instructions 
loaded from a file line by line or entered in the input box built-in the program. The program executes 
the instructions (known as words) in each register until the halt instruction is reached or the all of the
registers have been executed.

The program was designed to only run .txt files other than entering instructions directly to the built-in
input box. This decision was made to assure maximum accuracy and to prevent the user from crashing the 
program by running a file type that the program wouldn't be able to read accurately.

A past version of this program was made supporting 4 bit instructions, but it was decided to change the
instruction size to 6 bits to allow for a larger register memory. The new version of the program will
be able to convert the old 4 bit instructions to 6 bit instructions. Once the instructions are converted
and successfully loaded, the program will be able to run them as if they were 6 bit instructions, and any
further alterations to the instructions will be done to the newly converted 6 bit instructions.

## A few things to keep in mind while using the program:
- You must use a halt instruction at the end of the program routine you mean to run. That will prevent
unwanted instructions from being performed. If no halt instruction is present the program will run 
every register until it reaches register 249.
- If an invalid instruction is entered an error message will be displayed showing the location of the
bad instruction, then the program will be automatically halted.
- Any empty register (+000000) will be skipped by the compiler until the end is reached.
- After you done running a program file, you will be given the option of running another one.
- Any time you open a new file all of the memory will be reset in order to load the new instructions.

## How to run the program:

You may run the program by opening the command shell in the directory containing all of the python scripts, 
then running the command bellow:

```shell
python gui_app.py
```
Once you execute the command above, a GUI will be open to the screen that can be used to execute any amount
of BasicML scripts.
