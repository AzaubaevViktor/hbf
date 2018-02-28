from pytest import raises

from .error import HBFLexerError
from .lexer import Lexer, Block
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


simple_correct = """
level 0 1
    level 1 2
level 0 3
    level 1 4
"""


blocks_correct = """
level 0 1
    level 1 2
    level 1 3
        level 2 4
    level 1 5
        level 2 6

level 0 8
level 0 9
"""

blocks_incorrect = blocks_correct + """
        level 2
"""

comment = """

# test
level 0 # test
    level1_1 # test
#test
    # fkdsaflkfdsnj kj  k jn k #jk l
    level1_2
    
"""


class TestLexer:
    def test_lexer_simple(self):
        lexer = Lexer(simple_correct.split("\n"))
        assert isinstance(lexer.tree, Block)
        root = lexer.tree
        assert isinstance(root.children, list)
        assert len(root.children) == 2
        assert len(root.children[0].children) == 1
        assert len(root.children[1].children) == 1

    def test_lexer_correct(self):
        lexer = Lexer(blocks_correct.split("\n"))
        assert isinstance(lexer.tree, Block)
        root = lexer.tree
        assert isinstance(root.children, list)
        assert len(root.children) == 3

        assert isinstance(root.children[0], Block)
        assert isinstance(root.children[1], Line)
        assert isinstance(root.children[2], Line)

        assert len(root.children[0].children) == 3

    def test_lexer_incorrect(self):
        with raises(HBFLexerError, message="level error"):
            Lexer(blocks_incorrect.split("\n"))

    def test_comments(self):
        lexer = Lexer(comment.split("\n"))
        root_block = lexer.tree
        assert len(root_block.children) == 1
        block_cmd = root_block.children[0]

        assert block_cmd.head.first.word == "level"
        assert len(block_cmd.children) == 2
        assert block_cmd.children[0].first.word == "level1_1"
        assert block_cmd.children[1].first.word == "level1_2"

