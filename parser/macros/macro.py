from typing import Dict, List

from lexer import Token, Line, Block
from parser.arg_types import *
from .abc_macro import MacroBuiltin, MacroBuiltinBlock, MacroFunction


def _by_pair(it):
    _it = iter(it)
    while True:
        try:
            a = next(_it)
        except StopIteration:
            break
        b = next(_it)
        yield a, b


class MacroBuiltinMacro(MacroBuiltinBlock):
    def __init__(self):
        self.name = "macro"

    def _check_args(self, namespace: "NameSpace", args: List[Token]):
        args_by_names = {
            'name': TypeName(args[0]).value,
            'arg_types': [],
            'arg_names': []
        }

        for type_arg_name, arg_name in _by_pair(args[1:]):
            args_by_names['arg_types'].append(TypeType(type_arg_name).value)
            args_by_names['arg_names'].append(TypeName(arg_name).value)

        return args_by_names

    def compile(self, namespace: "NameSpace", args: List[Token], source: Block):
        args = self._check_args(namespace, args)
        func = MacroFunction(
            args['name'],
            args['arg_types'],
            args['arg_names'],
            source
        )
        namespace.add_macro(func)
        return ""
