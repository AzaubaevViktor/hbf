class ArgumentType:
    def __init__(self, token: "Token"):
        self.token = token
        self.value = None


class TypeInt(ArgumentType):
    def __init__(self, token: "Token"):
        super().__init__(token)
        self.value = int(token.word)


