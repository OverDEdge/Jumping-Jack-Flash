from nose.tools import *
from Jumpy.main import *

def setup():
    print("SETUP!")

def teardown():
    print("TEAR DOWN!")

def test_game():
    g = Game()
    assert_equal(g.running_program, True)
