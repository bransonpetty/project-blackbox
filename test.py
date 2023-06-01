import pytest
from main import Simulator

def test_incorrect_file():
    insta = Simulator()
    assert insta.open_file('BADFILE') == False 

def test_correct_file():
    insta = Simulator()
    assert insta.open_file('file1.txt') == True