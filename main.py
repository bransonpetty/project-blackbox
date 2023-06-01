'''
Future boilerplate
'''

class Simulator:
    '''Holds the list of commands and simulator functions'''
    def __init__(self):
        self.registers = {};

        for i in range(100):
            self.registers[i] = 0;

def main():
    '''Main function'''
    print("Hello World!")

if __name__ == "__main__":
    main()