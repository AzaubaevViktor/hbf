from typing import List, Dict

from ..arg_types import TypeInt, ArgumentType, TypeName, TypeAddress
from .abc_macro import MacroBuiltin


class MacroBuiltinRegister(MacroBuiltin):
    def __init__(self):
        self.name = "reg"
        self.arg_names = ["name"]
        self.arg_types = [TypeName]

    def _compile(self, namespace: "NameSpace", args: Dict[str, ArgumentType]):
        reg_name = args["name"].value
        namespace.add_register(reg_name)
        return ""


class MacroBuiltinUnReg(MacroBuiltin):
    def __init__(self):
        self.name = "unreg"
        self.arg_names = ["name"]
        self.arg_types = [TypeName]

    def _compile(self, namespace: "NameSpace", args: Dict[str, ArgumentType]):
        reg_name = args["name"].value
        namespace.release_register(reg_name)
        return ""


class MacroBuiltinMoveTo(MacroBuiltin):
    def __init__(self):
        self.name = "move"
        self.arg_names = ["to", "from"]
        self.arg_types = [TypeAddress, TypeAddress]

    def _compile(self, namespace: "NameSpace", args: Dict[str, ArgumentType]):
        _to = args["to"].value.addr
        _from = args["from"].value.addr
        if _from > _to:
            return "<" * (_from - _to)
        else:
            return ">" * (_to - _from)


class MacroBuiltinAdd(MacroBuiltin):
    def __init__(self):
        self.name = "__add"
        self.arg_names = ["value"]
        self.arg_types = [TypeInt]

    def _compile(self, namespace: "NameSpace", args: Dict[str, ArgumentType]):
        count = args["value"].value

        if count >= 0:
            return "+" * count
        else:
            return "-" * -count


class MacroBuiltinCycleOpen(MacroBuiltin):
    def __init__(self):
        self.name = "__cycle_open"
        self.arg_names = []
        self.arg_types = []

    def _compile(self, namespace: "NameSpace", args: Dict[str, ArgumentType]):
        return "["


class MacroBuiltinCycleClose(MacroBuiltin):
    def __init__(self):
        self.name = "__cycle_close"
        self.arg_names = []
        self.arg_types = []

    def _compile(self, namespace: "NameSpace", args: Dict[str, ArgumentType]):
        return "]"


class MacroBuiltinPrint(MacroBuiltin):
    def __init__(self):
        self.name = "__print"
        self.arg_names = []
        self.arg_types = []

    def _compile(self,  namespace: "NameSpace", args: Dict[str, ArgumentType]):
        return "."


