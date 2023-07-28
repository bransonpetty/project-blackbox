# Design Documentation

Designed and built by: Branson Petty, Connor Barry, Noah Potter, and Pedro Valente.

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

## Tecnical implementation:

More information on how the program was implemented, please refer to the Class definition document.

## Instructions available:

### I/O operations:
- READ = 010 Read a word from the keyboard into a specific location in memory.
- WRITE = 011 Write a word from a specific location in memory to screen.

### Load/store operations:
- LOAD = 020 Load a word from a specific location in memory into the accumulator.
- STORE = 021 Store a word from the accumulator into a specific location in memory.

### Arithmetic operations:
- ADD = 030 Add a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator)
- SUBTRACT = 031 Subtract a word from a specific location in memory from the word in the accumulator (leave the result in the accumulator)
- DIVIDE = 032 Divide the word in the accumulator by a word from a specific location in memory (leave the result in the accumulator).
- MULTIPLY = 033 multiply a word from a specific location in memory to the word in the accumulator (leave the result in the accumulator).

### Control operatios:
- BRANCH = 040 Branch to a specific location in memory
- BRANCHNEG = 041 Branch to a specific location in memory if the accumulator is negative.
- BRANCHZERO = 042 Branch to a specific location in memory if the accumulator is zero.
- HALT = 043 Pause the program

## Example of an valid instruction file:

The following is and example of the correct format of a file to be run through the program. 
Make sure all the instructions are stored on a *.txt file.

```
+010007
+010008
+020007
+020008
+021009
+011009
+043000
+000000
+000000
+000000
-99999
```

## User Stories:

- Brian has taken an interest in computer science and wants to understand at a base level how assembly
instructions work. He is able to write short instruction files to learn how each of them works and 
eventually how to perform multiple successive functions.

- Justin is designing a program on his raspberry pi. Because the raspberry pi doesn't have much in the
way of memory he needs to design a program at the lowest level to improve memory and performance. 
For easier testing than running his long instruction programs on his raspberry pi, he is able to run
this program from his computer and use the debugger to watch each register as a line of instruction
is read.

## Use Cases: 

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 393730b (Update design-doc.md)
- ADD (30xx) - We load the number 8 from a register and add it to the accumulator which has the value
    6 in it previously. Once the operation has finished the accumulator will have a value of 14
- SUBTRACT (31xx) - We load the number 2 from a register and subtract it from the accumulator value of
    5 leaving the accumulator with a value of 3.
- READ (10xx) - We load the inputted number from the user input. The number is then saved to the
  register specified in the second two digits of the command.
- WRITE (11xx) - We load the number specified in the given register. The value is then placed as
  the output in the console.
- DIVIDE (32xx) - We load the number 10 from the accumulator and divide it by (2) the number in the
  specified register. The result (5) is then stored in the accumulator.
- MULTIPLY (33xx) - We load the number 3 from the accumulator and divide it by (3) the number in the
  specified register. The result (9) is then stored in the accumulator.
- LOAD (20xx) - We load the given register value and copy it into the accumulator.
- STORE (21xx) - We load the value in the accumulator and copy it into the specified register.
- BRANCH (40xx) - The second two digits provide a location to jump to. So when the command is
  encountered the current register changes to whatever is specified by the two digits.
- HALT (43xx) - When encountered processes are paused and the program stops running
<<<<<<< HEAD
=======
- ADD (30xx) - Identify 2 digit function code. Reference register specified in the last two digits
    of the direction. Add that registers value to the accumulator's existing value.
- SUBTRACT (31xx) - Identify 2 digit function code. Reference register specified in the last two 
    digits. Subtract the accumulator's value by the register's value.
- DIVIDE (32xx) - Identify 2 digit function code. Reference register specified in the last two 
    digits. Divide the accumulator by the register's value.
- MULTIPLY (33xx) - Identify 2 digit function code. Reference register specified in the last two 
    digits. Multiply the two values together and store their value in the accumulator.
- Use READ and LOAD to store input in the accumulator. By first using READ to take and store the user's
    input in a specified register we can use LOAD to reference that same register and store that address 
    in the accumulator.
- We can use READ and MULTIPLY to create a single function calculator. We can read in any user input and 
    ,once stored, can be referenced to multiply one after the other.
- Using BRANCHNEG we can check the accumulator for a negative value. If the accumulator is negative
    value we can issue a HALT command to branch to so the program quits.
- The STORE operation can be used to copy the accumulator value into a register. This can be used to
    temporarily alter the value and revert back using LOAD.
- After preforming an arithmetic operation we want to return the value. We will use the LOAD and WRITE
    functions to pull the value from the accumulator into a register and then write it to the console.
- Using READ and WRITE we can echo a users input by returning the value immediately following it's input.
    We will store the value in a register and then use that register in the write command.
- BRANCHNEG can be used for conditionals by altering the accumulator value based off a logic statement.
=======

>>>>>>> 393730b (Update design-doc.md)

>>>>>>> 03ce6e1 (Fixed Design-Doc)
