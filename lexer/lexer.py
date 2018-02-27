from typing import List

from .line import Line


class Block:
    def __init__(self, line: Line):
        self.head = line
        self.children = None
        self.parent = None

    def append(self, line: Line or "Block"):
        if self.children is None:
            self.children = [line]
        else:
            self.children.append(line)

        if isinstance(line, Block):
            line.parent = self


class Lexer:
    def __init__(self, lines: List[str]):
        self.lines = []  # type: List[Line]
        for line_no, line in enumerate(lines):
            self.lines.append(
                Line(line_no, line)
            )

        self.tree = None
        self._to_levels()


    def _to_levels(self):
        cur_level = 0
        child = []

        self.tree = cur = Block(None)

        for line in self.lines:
            if line.level == cur_level:
                cur.append(line)
            elif line.level == cur_level + 1:
                block = Block(line)
                cur.append(block)
                cur = block
            elif line.level < cur_level:
                for i in range(cur_level - line.level):
                    cur = cur.parent
            else:
                HBFLexelError





