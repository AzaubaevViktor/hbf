import abc
from typing import List

from lexer import Token
from .arg_types import TypeInt, ArgumentType


class Macro(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self.name = None
        self.arg_types = []

    def _check_args(self, args):
        for tp, arg in zip(self.arg_types, args):
            yield tp(arg)

    @abc.abstractmethod
    def _compile(self, namespace: "NameSpace", args: List[ArgumentType]):
        pass

    def compile(self, namespace: "NameSpace", args: List[Token]):
        args = list(self._check_args(args))
        return self._compile(namespace, args)


class MacroBuiltinAdd(Macro):
    def __init__(self):
        self.name = "__add"
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

