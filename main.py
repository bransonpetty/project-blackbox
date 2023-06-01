'''
Future boilerplate
'''

class Simulator:
    '''Holds the list of commands and simulator functions'''
    def __init__(self):
        self.registers = {};

        for i in range(100):
            self.registers[i] = 0;

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

def main():
    '''Main function'''
    print("Hello World!")

if __name__ == "__main__":
    main()