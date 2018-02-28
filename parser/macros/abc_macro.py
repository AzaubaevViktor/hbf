import abc
from typing import List, Dict

from lexer import Token, Block
from parser.arg_types import ArgumentType


class AbstractMacro(metaclass=abc.ABCMeta):
    pass


class MacroBuiltin(AbstractMacro, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self.name = None
        self.arg_names = []
        self.arg_types = []

    def _check_args(self, namespace: "NameSpace", args: List[Token]):
        args_by_names = {}
        for tp, name, arg in zip(self.arg_types, self.arg_names, args):
            args_by_names[name] = tp(arg, namespace=namespace)
        return args_by_names

    def _compile(self, namespace: "NameSpace", args: Dict[str, ArgumentType]):
        raise NotImplementedError("Implement or not to call this function")

    def compile(self, namespace: "NameSpace", args: List[Token]):
        args_by_names = self._check_args(namespace, args)
        return self._compile(namespace, args_by_names)


class MacroBuiltinBlock(AbstractMacro, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self.name = None
        self.arg_names = []
        self.arg_types = []

    @abc.abstractmethod
    def compile(self, namespace: "Name", args: List[Token], block: Block):
        pass


class MacroFunction(AbstractMacro):
    def compile(self, namespace: "NameSpace", args: List[Token]):
        raise NotImplementedError("This macro function, can't compile themself")

    def __init__(self, name: str,
                 arg_types: List[ArgumentType],
                 arg_names: List[str],
                 source: Block):
        self.name = name
        self.arg_types = arg_types
        self.arg_names = arg_names
        self.code = source.children
        self.source = source
