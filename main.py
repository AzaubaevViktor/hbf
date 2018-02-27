from lexer import Lexer
from parser import Parser

f = open("test.hbf", "rt")

lex = Lexer(f.readlines())
par = Parser(lex.tree)
bc = "".join(par.compile())

print(bc)
