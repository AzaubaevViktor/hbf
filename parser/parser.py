from lexer import Line
from .mem import Memory
from .namespace import NameSpace
from parser.macros.builtin import *


class Parser:
    def __init__(self, root_block: "Block"):
        self.root = root_block

        self.mem = Memory()

        self.ns = NameSpace(None, self.mem)
        self._init_ns()

    def _init_ns(self):
        self.ns.add_macro(MacroBuiltinAdd())
        self.ns.add_macro(MacroBuiltinPrint())
        self.ns.add_macro(MacroBuiltinRegister())
        self.ns.add_macro(MacroBuiltinMoveTo())

    @staticmethod
    def _compile(ns: NameSpace, lines: List[Line or "Block"]):
        for line in lines:
            if isinstance(line, Line):
                macro_name = line.first.word
                macro = ns.find_macro(macro_name)
                bytecode = macro.compile(ns, line.args)
                yield bytecode

    def compile(self):
        yield from self._compile(self.ns, self.root.children)
