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

![Load Instruction(Button)](https://github.com/bransonpetty/project-blackbox/blob/develop/readme%20images/Load%20Instructions%20(Button)%20v2.png)

Once you select "Load Instructions", a new window will appear as shown bellow. In this new window you may load the instructions from a file or enter them manually buy entering all of the instructions in the text box in the window. If you decide to open a file, you will be given the change to modify the instructions before loading them to the registers by pressing "Process Entry":

![Load Instruction(Window)](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Load%20Instructions%20(Window)%20v2.png)

Once the instructions successfully loaded, they will be displayed the table shown in the first image bellow. At this point, you may double click any of the register entry in the table to edit it. Once you double click it, the window shown in the second image bellow will appear and you may enter the new value to be stored in the register:

![Registers](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Registers%20v2.png)
![Registers (Double Click)](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Edit%20Register%20v2.png)

Once the registers are loaded as desired you may execute the instructions by pressing the Run button as shown bellow:

![Run Button](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Run%20(Button)%20v2.png)

While the program is executing, a new button will appear that will allow you to abort the execution:

![Cancel Button](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Cancel%20(Button)%20v2.png)

Once the program execution is completed, you will be given the option to rerun the program by pressing the button shown bellow (Just keep in mind that the program will run with all the modifications made during the previous execution):

![Rerun Button](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Rerun%20(Button)%20v2.png)

In the top of the window you will find a "File" menu that can be used to load the instructions or save the register instructions to a txt file:

![File Menu](https://github.com/bransonpetty/project-blackbox/blob/develop/readme%20images/File%20(Menu)%20v2.png)

Next to the "File" menu you will find the "Execution menu" that can be used to run/cancel/rerun program, reset all the register to 0, and clear the console:

![Execution Menu](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Execute%20(Menu)%20v2.png)

If you wish to change the color scheme of the program, you may click on the "Change Color Scheme" under the Style menu. 

![Style Menu](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Style%20(Menu).png)

Once you select the option, you will be able to choose a primary color (color of the background) as shown bellow:

![Primary Color](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Style%20(Primary).png)

Then you will be able to choose a secondary color (color of the buttons) as shown bellow:

![Seconday Color](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Style%20(Secondary).png)

After selecting both colors, the color scheme of the program will be modified as shown bellow:

![New Style](https://raw.githubusercontent.com/bransonpetty/project-blackbox/develop/readme%20images/Style%20result.png)
