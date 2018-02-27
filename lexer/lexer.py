from typing import List

from .error import HBFLexerError
from .line import Line


class Block:
    def __init__(self, line: Line):
        self.head = line
        self.children = None  # type: List
        self.parent = None

    def append(self, line: Line or "Block"):
        if self.children is None:
            self.children = [line]
        else:
            self.children.append(line)

        if isinstance(line, Block):
            line.parent = self

    def last_to_block(self) -> "Block":
        block = Block(self.children.pop())
        block.parent = self
        self.append(block)
        return block

    def __repr__(self):
        return "<Block|{}>".format(
            self.head
        )


class Lexer:
    def __init__(self, lines: List[str]):
        self.lines = []  # type: List[Line]
        for line_no, line in enumerate(lines):
            if line.strip() != "":
                self.lines.append(
                    Line(line_no, line)
                )

        self.tree = None
        self._to_levels()

    def _to_levels(self):
        cur_level = 0

        self.tree = cur = Block(None)

        for line in self.lines:
            if line.level == cur_level:
                cur.append(line)
            elif line.level == cur_level + 1:
                block = cur.last_to_block()
                block.append(line)
                cur = block
            elif line.level < cur_level:
                for i in range(cur_level - line.level):
                    cur = cur.parent
                cur.append(line)
            else:
                raise HBFLexerError(line, None, "Level error", pos=line.level * line.LEVEL_SPACES)
            cur_level = line.level





