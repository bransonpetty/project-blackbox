import pytest
import os
from main import *
# python -m pytest test.py 

def test_add(monkeypatch): #tests the adding use case
    print('\nThis is the add use case, input file1.txt, then +0008\
, then +0006, and finally n\n')
    with open ('file1.txt', 'w') as file:
        print('+1009', file=file)# read in num
        print('+1010', file=file) # read in num
        print('+2009', file=file) # load into accumulator
        print('+3010', file=file) # add a word in mem to accum
        print('+2111', file=file) # store a word from accum into memory
        print('+1111', file=file) # write word from mem onto screen
    main()
    test_bad_add()

def test_bad_add(): #tests failure in add use case
    print('\nThis is the failure add use case, input file1.txt, then +9999\
, then +0001, and finally n\n')
    with open ('file1.txt', 'w') as file:
        print('+1009', file=file)# read in num
        print('+1010', file=file) # read in num
        print('+2009', file=file) # load into accumulator
        print('+3010', file=file) # add a word in mem to accum
        print('+2111', file=file) # store a word from accum into memory
        print('+1111', file=file) # write word from mem onto screen
    main()
    test_sub()
    

def test_sub(): #tests the subtraction use case
    print('\nThis is the subtract use case, input file1.txt, +0005, then +0002,\
 and finally n\n')
    with open ('file1.txt', 'w') as file:
        print('+1009', file=file)# read in num
        print('+1010', file=file) # read in num
        print('+2009', file=file) # load into accumulator
        print('+3110', file=file) # subtract a word in mem to accum
        print('+2111', file=file) # store a word from accum into memory
        print('+1111', file=file) # write word from mem onto screen
    main()
    test_failure_sub()
    
def test_failure_sub(): #tests overflow scenario in a subtraction operation
    print('\nThis is the failure subtract use case, input file1.txt, -9995, then +0005,\
 and finally n\n')
    with open ('file1.txt', 'w') as file:
        print('+1009', file=file)# read in num
        print('+1010', file=file) # read in num
        print('+2009', file=file) # load into accumulator
        print('+3110', file=file) # subtract a word in mem to accum
        print('+2111', file=file) # store a word from accum into memory
        print('+1111', file=file) # write word from mem onto screen
    main()
    test_multiply()
    
def test_multiply(): #tests reading values and multiplying them together
    print('\nThis is the multiply use case, input file1.txt, then +0007, then +0013, and finally n \n')
    with open ('file1.txt', 'w') as file:
        print('+1009', file=file)# read in num
        print('+1010', file=file) # read in num
        print('+2009', file=file) # load into accumulator
        print('+3310', file=file) # subtract a word in mem to accum
        print('+2111', file=file) # store a word from accum into memory
        print('+1111', file=file) # write word from mem onto screen
    main()
    test_failure_multiply()
    
def test_failure_multiply():#tests reading in values and multiplying them together
    print('\nThis is the failure multiply use case, input file1.txt, then +0007, then +0013, and finally n \n')


    
def test_incorrect_file(): #tests bad file handling
    insta = Simulator()
    assert insta.open_file('BADFILE') == False 

def test_correct_file(): #tests file handling
    insta = Simulator()
    assert insta.open_file('file1.txt') == True
#test_add()
test_multiply()