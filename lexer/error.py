from error import HBFError


class HBFLexerError(HBFError):
    def __init__(self, line, token, msg, pos=None):
        self.line = line
        self.token = token
        self.msg = msg
        self.pos = pos

    def __str__(self):
        return "HBF `{}`:\n" \
               "on line `{}`, token `{}`, pos `{}`".format(
            self.msg, self.line, self.token, self.pos
        )