import abc


class ArgumentType(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, token: "Token", namespace=None):
        self.token = token
        self.value = None
        self.ns = namespace  # type: NameSpace


class TypeInt(ArgumentType):
    def __init__(self, token: "Token", namespace=None):
        super().__init__(token)
        self.value = int(token.word)


class TypeName(ArgumentType):
    def __init__(self, token: "Token", namespace=None):
        super().__init__(token)
        self.value = str(token.word)


class TypeAddress(ArgumentType):
    def __init__(self, token: "Token", namespace=None):
        super().__init__(token, namespace)
        try:
            if token.word[0] != ":":
                raise ValueError("Address should start with `:`, not `{}`".format(
                    token.word
                ))
            self.value = int(token.word[1:])
            self.register_name = None
        except Exception as e:
            cell = self.ns.find_register(token.word)
            self.value = cell.addr
            self.register_name = token.word



