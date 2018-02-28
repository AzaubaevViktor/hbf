import abc

from .mem import MemoryCell


class ArgumentType(metaclass=abc.ABCMeta):
    NAME = None

    @abc.abstractmethod
    def __init__(self, token: "Token", namespace=None):
        self.token = token
        self.value = None
        self.ns = namespace  # type: NameSpace


class TypeInt(ArgumentType):
    NAME = "int"

    def __init__(self, token: "Token", namespace=None):
        super().__init__(token)
        try:
            self.value = int(token.word)
        except ValueError:
            self.value = namespace.get(token.word, int)


class TypeName(ArgumentType):
    NAME = "name"

    def __init__(self, token: "Token", namespace=None):
        super().__init__(token)
        self.value = str(token.word)


class TypeAddress(ArgumentType):
    NAME = "addr"

    def __init__(self, token: "Token", namespace=None):
        super().__init__(token, namespace)
        try:
            if token.word[0] != ":":
                raise ValueError("Address should start with `:`, not `{}`".format(
                    token.word
                ))
            self.value = MemoryCell(int(token.word[1:]))
            self.register_name = None
        except Exception:
            cell = self.ns.get(token.word, MemoryCell)
            self.value = MemoryCell(cell.addr)
            self.register_name = token.word


_TYPES = [TypeInt, TypeAddress]
_TYPES = {tp.NAME: tp for tp in _TYPES}


class TypeType(ArgumentType):
    NAME = None

    def __init__(self, token: "Token", namespace=None):
        super().__init__(token)
        self.value = _TYPES[token.word]  # type: ArgumentType
