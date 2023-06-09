import pytest
import os
from main import *
# python -m pytest test.py 

def test_add(): #tests the adding use case
    with open ('file1.txt', 'w') as file:
        print('+1009', file=file)# read in num
        print('+1010', file=file) # read in num
        print('+2009', file=file) # load into accumulator
        print('+3010', file=file) # add a word in mem to accum
        print('+2106', file=file) # store a word from accum into memory
        print('+1106', file=file) # write word from mem onto screen
    main()
    os.remove('file1.txt')  










    
def test_incorrect_file(): #tests bad file handling
    insta = Simulator()
    assert insta.open_file('BADFILE') == False 

def test_correct_file(): #tests file handling
    insta = Simulator()
    assert insta.open_file('file1.txt') == True
    
test_add()