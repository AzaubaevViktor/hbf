from typing import List

from .error import HBFLexerError
from .line import Line, Block


class Lexer:
    def __init__(self, lines: List[str]):
        self.lines = []  # type: List[Line]
        for line_no, line in enumerate(lines):
            lexer_line = Line(line_no, line)
            if not lexer_line.empty:
                self.lines.append(lexer_line)

        self.tree = None  # type: Block
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
                raise HBFLexerError(line, None, "Level error",
                                    pos=line.level * line.LEVEL_SPACES)
            cur_level = line.level
