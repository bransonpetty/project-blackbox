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
- If an invalid instruction is entered an error message will be displayed showing the location of the
bad instruction, then the program will be automatically halted.
- Any empty register will be skipped by the compiler until the end is reached.
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

You can load the instructions buy pressing the "Load Instruction" button as shown bellow or in the "File" menu on the top of the program:

![Load Instruction(Button)](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Load%20instruction%20(button).png)

Once you select "Load Instructions", a new window will appear as shown bellow. In this new window you may load the instructions from a file or enter them manually buy entering all of the instructions in the text box in the window. If you decide to open a file, you will be given the change to modify the instructions before loading them to the registers by pressing "Process Entry":

![Load Instruction(Window)](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Load%20instruction%20(window).png)

Once the instructions successfully loaded, they will be displayed the table shown in the first image bellow. At this point, you may double click any of the register entry in the table to edit it. Once you double click it, the window shown in the second image bellow will appear and you may enter the new value to be stored in the register:

![Registers](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Registers.png)
![Registers (Double Click)](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Edit%20register.png)

Once the registers are loaded as desired you may execute the instructions by pressing the Run button as shown bellow:

![Run Button](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Run%20Button.png)

---CANCEL---

---RERUN---

In the top of the window you will find a "File" menu that can be used to load the instructions or save the register instructions to a txt file:

![File Menu](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/File%20menu.png)

Next to the "File" menu you will find the "Execution menu" that can be used to run/cancel/rerun program, reset all the register to 0, and clear the console:

![Execution Menu](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Execute%20menu.png)

---STYLE---

File should include a 4 digit operator on each line. The filename
argument can be placed immediately after the run statement, or
after the run statement a prompt will display.