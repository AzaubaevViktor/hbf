import pytest
from pytest import raises

from lexer import Lexer
from parser import Parser

sources = [
    ("""
__add 1
__print
""", "+.", "Simple check builtin"),

    ("""
__add -1
__print
""", "-.", "Simple check builtin"),

    ("""

__add -222     \t


__print      


""", "-" * 222 + ".", "Source with spaces"),

    ("""
reg a
reg b
reg c
move c :0
move b c
__add 1
move c b
""", ">><+>", "Check register allocation"),

    ("""
reg a # :0
reg b # :1
reg c # :2
reg d # :3
unreg b # kill :1
reg e # may be :1
move e :0  # return `>`
""", ">", "Check register release"),

    ("""
__cycle_open
__cycle_close
""", "[]", "Check cycle braces"),

    ("""
macro test  # define macros
    __add 1
    __print
    
test # call macros
""", "+.", "Simple macros test without arguments"),

    ("""
macro test int V
    __add V
    __print

test 2 
""", "++.", "Test macros with one argument"),

    ("""
macro test addr A int B
    move A :0
    __add B
    move :0 A
    
test :2 5
""", ">>+++++<<", "Test macros with two arguments"),

    ("""
macro test addr A int B
    move A :0
    __add B
    move :0 A

reg X
reg Y
reg Z  # :2
test Z 5
""", ">>+++++<<", "Test macros with two arguments + register"),

    ("""
reg A # :0

macro test int B
    reg A # :1
    move A :0
    __add B
    move :0 A

test 5
""", ">+++++<", "Test inherit register with macros"),

    ("""
macro first int A int B
    __add A
    macro second 
        move :1 :0
        __add B
    second

first 1 2    
""", "+>++", "Macros into macros"),

    ("""
macro first int A int B
    __add A
    macro second int B
        move :1 :0
        __add B
    second 3

first 1 2    
""", "+>+++", "Macros into macros with rewrite"),

    ("""
macro first int A int B int C
    __add A
    macro second int B
        move :1 :0
        __add B
        move :2 :1
        __add C
    second C

first 1 2 3   
""", "+>+++>+++", "Macros into macros with rewrite other variable"),

    ("""
reg A # :0
reg B # :1

macro test addr A addr C
    reg D # :2
    move A :0
    __add 1
    
    move B :0
    __add 1
    
    move C :0
    __add 1
    
    move D :0
    __add 1
    

test A B
    
""", "+>+>+>>+", "Macros with register one"),

]

negative = [
    ("""
reg A
reg A 
""", Exception, "already used"),
]


def compile(s: str):
    l = Lexer(s.split("\n"))
    p = Parser(l.tree)
    return "".join(p.compile())


class TestParser:
    @pytest.mark.parametrize("source, expect, msg", sources)
    def test_compile(self, source, expect, msg):
        bc = compile(source)
        assert bc == expect, msg

    @pytest.mark.parametrize("source, exc, msg", negative)
    def test_negative(self, source, exc, msg):
        with raises(exc, message=msg):
            bc = compile(source)
            print(bc)
