from pytest import raises

from lexer.error import HBFLexerError
from .line import Line


class TestLine:
    def test_splitter(self):
        a_b = list(Line._split("a b"))
        assert a_b[0] == (0, "a")
        assert a_b[1] == (2, "b")

        aa_bb = list(Line._split("aa bb"))
        assert aa_bb[0] == (0, "aa")
        assert aa_bb[1] == (3, "bb")

        a_b_c = list(Line._split("  aa   bb   cc    "))
        assert len(a_b_c) == 3
        assert a_b_c[0] == (2, "aa")
        assert a_b_c[1] == (7, "bb")
        assert a_b_c[2] == (12, "cc")

        a_b_c = list(Line._split("  aa \t bb   cc   \t"))
        assert len(a_b_c) == 3
        assert a_b_c[0] == (2, "aa")
        assert a_b_c[1] == (7, "bb")
        assert a_b_c[2] == (12, "cc")

    def test_line_err(self):
        tabs_err = " \tfirst second"
        with raises(HBFLexerError, message="tabs"):
            Line(0, tabs_err)

        spaces_err = "   fuck"
        with raises(HBFLexerError, message="spaces"):
            Line(0, spaces_err)

        empty = "  "
        with raises(HBFLexerError, message="spaces"):
            Line(0, empty)

    def test_line_ok(self):
        level0 = "level 0 test"
        line = Line(0, level0)
        assert line.level == 0
        assert len(line.tokens) == 3
        assert line.tokens[0].word == "level"

        level1 = "    level 1 test"
        line = Line(0, level1)
        assert line.level == 1
        assert len(line.tokens) == 3
        assert line.tokens[0].word == "level"


class TestLexer:
    def test_lexer(self):
        pass
