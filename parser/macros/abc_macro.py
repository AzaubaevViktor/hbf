import abc
from typing import List, Dict

from lexer import Token
from parser.arg_types import  ArgumentType


class Macro(metaclass=abc.ABCMeta):
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

    @abc.abstractmethod
    def _compile(self, namespace: "NameSpace", args: Dict[str, ArgumentType]):
        pass

    def compile(self, namespace: "NameSpace", args: List[Token]):
        args_by_names = self._check_args(namespace, args)
        return self._compile(namespace, args_by_names)
