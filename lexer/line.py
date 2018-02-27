from typing import Iterable, Tuple, List

from lexer.error import HBFLexerError
from .token import Token


class Line:
    LEVEL_SPACES = 4

    def __init__(self, line_no, line):
        self.line_no = line_no

        self.tokens = []  # type: List[Token]
        self.original = line
        self.level = -1

        self._checks()

        for pos, word in self._split(line):
            self.tokens.append(
                Token(self, pos, word)
            )

    def _checks(self):
        _level = 0
        for pos, ch in enumerate(self.original):
            if ch == " ":
                _level += 1
            elif ch == "\t":
                raise HBFLexerError(self, None, "Didn't use tabs!", pos=pos)
            else:
                break

        if _level % 4 == 0:
            self.level = _level // self.LEVEL_SPACES
        else:
            raise HBFLexerError(self, None,
                                "Use {} spaces for indent!".format(self.LEVEL_SPACES),
                                pos=_level)

    @staticmethod
    def _split(line: str) -> Iterable[Tuple[int, str]]:
        word = ""
        word_pos = 0
        for pos, ch in enumerate(line):
            if ch.isspace():
                if word:
                    yield word_pos, word
                word = ""
                word_pos = pos + 1
            else:
                word += ch

        if word:
            yield word_pos, word

    def __repr__(self):
        return "<Line({}) [{}]>".format(
            self.line_no,
            ", ".join(map(str, self.tokens))
        )


