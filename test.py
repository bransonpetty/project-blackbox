import pytest
from main import Simulator
# python -m pytest test.py 

def test_constructor(): #tests the creation of the class
    insta = Simulator()
    assert len(insta.registers) == 100
    assert insta.accumulator == "+0000"
    assert insta.cur_addr == 0
    assert len(insta.instructions) == 12
    assert len(insta.log) == 0
    
def test_incorrect_file(): #tests bad file handling
    insta = Simulator()
    assert insta.open_file('BADFILE') == False 

def test_correct_file(): #tests file handling
    insta = Simulator()
    assert insta.open_file('file1.txt') == True