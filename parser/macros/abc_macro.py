import abc
from typing import List

from lexer import Token
from parser.arg_types import  ArgumentType


class Macro(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        self.name = None
        self.arg_names = []
        self.arg_types = []

    def _check_args(self, args, namespace):
        for tp, arg in zip(self.arg_types, args):
            yield tp(arg, namespace=namespace)

    @abc.abstractmethod
    def _compile(self, namespace: "NameSpace", args: List[ArgumentType]):
        pass

    def compile(self, namespace: "NameSpace", args: List[Token]):
        args = list(self._check_args(args, namespace))
        return self._compile(namespace, args)
