from lexer import Lexer
from parser import Parser

simple_code_plus = """
__add 1
__print
"""

simple_code_minus = """
__add -1
__print
"""

simple_code_with_spaces = """

__add -222     \t


__print      


"""

registers_only = """
reg a
reg b
reg c
move c :0
move b c
__add 1
move c b
"""


reg_unreg = """
reg a # :0
reg b # :1
reg c # :2
reg d # :3
unreg b # kill :1
reg e # may be :1
move e :0  # return >
"""


def compile(s: str):
    l = Lexer(s.split("\n"))
    p = Parser(l.tree)
    return "".join(p.compile())


class TestParser:
    def test_simple(self):
        bc = compile(simple_code_plus)
        assert bc == "+."

        bc = compile(simple_code_minus)
        assert bc == "-."

        bc = compile(simple_code_with_spaces)
        assert bc == "-" * 222 + "."

    def test_move(self):
        bc = compile(registers_only)
        assert bc == ">><+>"

    def test_unreg(self):
        bc = compile(reg_unreg)
        assert bc == ">"
