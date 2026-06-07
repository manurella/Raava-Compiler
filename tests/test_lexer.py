"""Tests for the Raava Lexer.

These tests are written FIRST (TDD). Implement raava/tokens.py and raava/lexer.py
to make them pass.
"""
import pytest
from raava.tokens import TokenType, Token
from raava.lexer import Lexer


class TestTokenDefinitions:
    """Tests that TokenType and Token are defined correctly."""

    def test_token_type_has_let(self):
        """TokenType should have a LET member."""
        assert hasattr(TokenType, 'LET')

    def test_token_type_has_identifier(self):
        """TokenType should have an IDENTIFIER member."""
        assert hasattr(TokenType, 'IDENTIFIER')

    def test_token_type_has_int_literal(self):
        """TokenType should have an INT_LITERAL member."""
        assert hasattr(TokenType, 'INT_LITERAL')

    def test_token_type_has_eof(self):
        """TokenType should have an EOF member."""
        assert hasattr(TokenType, 'EOF')

    def test_token_stores_type_and_value(self):
        """A Token should store its type, value, line, and column."""
        token = Token(TokenType.LET, 'let', 1, 1)
        assert token.type == TokenType.LET
        assert token.value == 'let'
        assert token.line == 1
        assert token.column == 1

    def test_token_repr(self):
        """Token repr should include the type name and value."""
        token = Token(TokenType.LET, 'let', 1, 1)
        result = repr(token)
        assert 'LET' in result
        assert 'let' in result


class TestLexerBasics:
    """Tests for basic lexer functionality."""

    def test_empty_input(self):
        """An empty string should produce only an EOF token."""
        lexer = Lexer('')
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_whitespace_only(self):
        """Whitespace-only input should produce only EOF."""
        lexer = Lexer('   \n\t  ')
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_single_integer(self):
        """A single number should produce an INT_LITERAL token."""
        lexer = Lexer('42')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.INT_LITERAL
        assert tokens[0].value == '42'
        
    def test_single_float(self):
        """A decimal number should produce a FLOAT_LITERAL token."""
        lexer = Lexer('3.14')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.FLOAT_LITERAL
        assert tokens[0].value == '3.14'

    def test_single_string(self):
        """A quoted string should produce a STRING_LITERAL token."""
        lexer = Lexer('"Hello, Wan"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STRING_LITERAL
        assert tokens[0].value == 'Hello, Wan'

    def test_single_identifier(self):
        """A single name should produce an IDENTIFIER token."""
        lexer = Lexer('myVar')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.IDENTIFIER
        assert tokens[0].value == 'myVar'


class TestLexerKeywords:
    """Tests for keyword recognition."""

    def test_let_keyword(self):
        lexer = Lexer('let')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LET

    def test_fn_keyword(self):
        lexer = Lexer('fn')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.FN

    def test_if_keyword(self):
        lexer = Lexer('if')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.IF

    def test_else_keyword(self):
        lexer = Lexer('else')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.ELSE

    def test_while_keyword(self):
        lexer = Lexer('while')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.WHILE

    def test_return_keyword(self):
        lexer = Lexer('return')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.RETURN

    def test_print_keyword(self):
        lexer = Lexer('print')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.PRINT

    def test_true_keyword(self):
        lexer = Lexer('true')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TRUE

    def test_false_keyword(self):
        lexer = Lexer('false')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.FALSE

    def test_element_literals(self):
        for elem in ['Water', 'Earth', 'Fire', 'Air']:
            lexer = Lexer(elem)
            tokens = lexer.tokenize()
            assert tokens[0].type == TokenType[elem.upper()], f'{elem} should be recognized'

    def test_bending_keywords(self):
        for kw in ['spawn', 'move', 'stance', 'strike', 'block']:
            lexer = Lexer(kw)
            tokens = lexer.tokenize()
            assert tokens[0].type == TokenType[kw.upper()], f'{kw} should be recognized'

    def test_direction_keywords(self):
        for d in ['Up', 'Down', 'Left', 'Right']:
            lexer = Lexer(d)
            tokens = lexer.tokenize()
            assert tokens[0].type == TokenType[d.upper()], f'{d} should be recognized'


class TestLexerOperators:
    """Tests for operator and symbol recognition."""

    def test_plus(self):
        lexer = Lexer('+')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.PLUS

    def test_minus(self):
        lexer = Lexer('-')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.MINUS

    def test_star(self):
        lexer = Lexer('*')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.STAR

    def test_slash(self):
        lexer = Lexer('/')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.SLASH

    def test_equals(self):
        lexer = Lexer('=')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.EQUALS

    def test_eq_eq(self):
        lexer = Lexer('==')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.EQ_EQ

    def test_bang_eq(self):
        lexer = Lexer('!=')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.BANG_EQ

    def test_lt(self):
        lexer = Lexer('<')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LESS_THAN

    def test_gt(self):
        lexer = Lexer('>')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.GREATER_THAN

    def test_lte(self):
        lexer = Lexer('<=')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.LESS_THAN_EQ

    def test_gte(self):
        lexer = Lexer('>=')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.GREATER_THAN_EQ

    def test_arrow(self):
        lexer = Lexer('->')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.ARROW

    def test_symbols(self):
        source = ': ; , ( ) { }'
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        expected = [
            TokenType.COLON, TokenType.SEMICOLON, TokenType.COMMA,
            TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN,
            TokenType.LEFT_BRACE, TokenType.RIGHT_BRACE,
        ]
        for i, expected_type in enumerate(expected):
            assert tokens[i].type == expected_type


class TestLexerComments:
    """Tests for comment handling."""

    def test_single_line_comment(self):
        lexer = Lexer('// this is a comment')
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF

    def test_comment_before_code(self):
        lexer = Lexer('// comment\n42')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.INT_LITERAL
        assert tokens[0].value == '42'


class TestLexerLineTracking:
    """Tests for line and column tracking."""

    def test_first_token_is_line_1(self):
        lexer = Lexer('let')
        tokens = lexer.tokenize()
        assert tokens[0].line == 1
        assert tokens[0].column == 1

    def test_newline_increments_line(self):
        lexer = Lexer('let\nx')
        tokens = lexer.tokenize()
        assert tokens[0].line == 1  # 'let' on line 1
        assert tokens[1].line == 2  # 'x' on line 2


class TestLexerFullStatements:
    """Tests for tokenizing complete Raava statements."""

    def test_let_declaration(self):
        lexer = Lexer('let x: int = 10;')
        tokens = lexer.tokenize()
        expected = [
            TokenType.LET, TokenType.IDENTIFIER, TokenType.COLON,
            TokenType.INT_TYPE, TokenType.EQUALS, TokenType.INT_LITERAL,
            TokenType.SEMICOLON, TokenType.EOF,
        ]
        assert [t.type for t in tokens] == expected

    def test_function_declaration(self):
        lexer = Lexer('fn add(a: int, b: int) -> int { return a + b; }')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.FN
        assert tokens[1].type == TokenType.IDENTIFIER
        assert tokens[1].value == 'add'

    def test_bending_strike(self):
        lexer = Lexer('strike(fireball, Up);')
        tokens = lexer.tokenize()
        expected = [
            TokenType.STRIKE, TokenType.LEFT_PAREN, TokenType.IDENTIFIER,
            TokenType.COMMA, TokenType.UP, TokenType.RIGHT_PAREN,
            TokenType.SEMICOLON, TokenType.EOF,
        ]
        assert [t.type for t in tokens] == expected


class TestLexerErrors:
    """Tests that the lexer reports errors for invalid characters."""

    def test_invalid_character_raises_error(self):
        lexer = Lexer('@')
        with pytest.raises(Exception):
            lexer.tokenize()
