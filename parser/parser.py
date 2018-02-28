from lexer import Line
from .mem import Memory
from .namespace import NameSpace
from .macros import *


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
        self.ns.add_macro(MacroBuiltinUnReg())
        self.ns.add_macro(MacroBuiltinCycleOpen())
        self.ns.add_macro(MacroBuiltinCycleClose())
        self.ns.add_macro(MacroBuiltinMacro())

    @staticmethod
    def _compile(ns: NameSpace, lines: List[Line or "Block"]):
        for line in lines:
            if isinstance(line, Block):
                block = line
                macro_name = block.first.word
                macro = ns.get(macro_name, AbstractMacro)
                bytecode = macro.compile(ns, block.args, block)
                yield bytecode
            elif isinstance(line, Line):
                macro_name = line.first.word
                macro = ns.get(macro_name, AbstractMacro)

                if isinstance(macro, MacroBuiltin):
                    yield macro.compile(ns, line.args)
                elif isinstance(macro, MacroFunction):
                    child_ns = ns.create_child()
                    for tp, name, arg in zip(macro.arg_types, macro.arg_names,
                                             line.args):
                        child_ns[name] = tp(arg, namespace=ns).value
                    yield from Parser._compile(child_ns, macro.code)
                    child_ns.cleanup()

    def compile(self):
        yield from self._compile(self.ns, self.root.children)
