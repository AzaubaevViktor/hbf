import pytest

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
