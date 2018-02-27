class Token:
    def __init__(self, line: "Line", pos: int, word: str):
        self.line = line
        self.pos = pos
        self.word = word
