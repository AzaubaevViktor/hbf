from typing import List

from ..arg_types import TypeInt, ArgumentType, TypeName, TypeAddress
from .abc_macro import Macro


class MacroBuiltinRegister(Macro):
    def __init__(self):
        self.name = "reg"
        self.arg_names = ["name"]
        self.arg_types = [TypeName]

    def _compile(self, namespace: "NameSpace", args: List[ArgumentType]):
        reg_name = args[0].value
        namespace.add_register(reg_name)
        return ""


class MacroBuiltinUnReg(Macro):
    def __init__(self):
        self.name = "unreg"
        self.arg_names = ["name"]
        self.arg_types = [TypeName]

    def _compile(self, namespace: "NameSpace", args: List[ArgumentType]):
        reg_name = args[0].value
        namespace.release_register(reg_name)
        return ""


class MacroBuiltinMoveTo(Macro):
    def __init__(self):
        self.name = "move"
        self.arg_names = ["to", "from"]
        self.arg_types = [TypeAddress, TypeAddress]

    def _compile(self, namespace: "NameSpace", args: List[ArgumentType]):
        _to = args[0].value
        _from = args[1].value
        if _from > _to:
            return "<" * (_from - _to)
        else:
            return ">" * (_to - _from)


class MacroBuiltinAdd(Macro):
    def __init__(self):
        self.name = "__add"
        self.arg_names = ["value"]
        self.arg_types = [TypeInt]

    def _compile(self, namespace: "NameSpace", args: List[ArgumentType]):
        count = args[0].value

        if count >= 0:
            return "+" * count
        else:
            return "-" * -count


class MacroBuiltinPrint(Macro):
    def __init__(self):
        self.name = "__print"
        self.arg_types = []

    def _compile(self,  namespace: "NameSpace", args: List[ArgumentType]):
        return "."

