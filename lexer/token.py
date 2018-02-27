class Token:
    def __init__(self, line: "Line", pos: int, word: str):
        self.line = line
        self.pos = pos
        self.word = word

    def __repr__(self):
        return "<Token({}) `{}`>".format(
            self.pos,
            self.word
        )
