"""Tests for the Raava Parser.

These tests are written FIRST (TDD). Implement raava/ast_nodes.py and raava/parser.py
to make them pass.
"""
import pytest
from raava.lexer import Lexer
from raava.parser import Parser
from raava import ast_nodes as ast


def parse(source: str) -> ast.Program:
    """Helper: lex and parse a source string."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


class TestParserLetStatements:
    """Tests for parsing let declarations."""

    def test_let_int(self):
        program = parse('let x: int = 42;')
        assert len(program.declarations) == 1
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.LetStatement)
        assert stmt.name == 'x'
        assert stmt.type_annotation == 'int'
        assert isinstance(stmt.value, ast.IntLiteral)
        assert stmt.value.value == 42

    def test_let_bool(self):
        program = parse('let flag: bool = true;')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.LetStatement)
        assert stmt.type_annotation == 'bool'
        assert isinstance(stmt.value, ast.BooleanLiteral)
        assert stmt.value.value is True

    def test_let_element(self):
        program = parse('let fireball: Element = Fire;')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.LetStatement)
        assert stmt.type_annotation == 'Element'
        assert isinstance(stmt.value, ast.ElementLiteral)
        assert stmt.value.value == 'Fire'


class TestParserExpressions:
    """Tests for parsing expressions."""

    def test_addition(self):
        program = parse('let x: int = 1 + 2;')
        expr = program.declarations[0].value
        assert isinstance(expr, ast.BinaryOperation)
        assert expr.operator == '+'

    def test_operator_precedence(self):
        """Multiplication should bind tighter than addition."""
        program = parse('let x: int = 1 + 2 * 3;')
        expr = program.declarations[0].value
        assert isinstance(expr, ast.BinaryOperation)
        assert expr.operator == '+'
        assert isinstance(expr.right, ast.BinaryOperation)
        assert expr.right.operator == '*'

    def test_parenthesized_expression(self):
        program = parse('let x: int = (1 + 2) * 3;')
        expr = program.declarations[0].value
        assert isinstance(expr, ast.BinaryOperation)
        assert expr.operator == '*'
        assert isinstance(expr.left, ast.BinaryOperation)
        assert expr.left.operator == '+'

    def test_unary_negation(self):
        program = parse('let x: int = -5;')
        expr = program.declarations[0].value
        assert isinstance(expr, ast.UnaryOperation)
        assert expr.operator == '-'

    def test_comparison(self):
        program = parse('let flag: bool = x > 5;')
        expr = program.declarations[0].value
        assert isinstance(expr, ast.BinaryOperation)
        assert expr.operator == '>'

    def test_logical_and(self):
        program = parse('let flag: bool = true and false;')
        expr = program.declarations[0].value
        assert isinstance(expr, ast.BinaryOperation)
        assert expr.operator == 'and'


class TestParserControlFlow:
    """Tests for parsing if/else and while."""

    def test_if_statement(self):
        program = parse('if (x > 0) { print x; }')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.IfStatement)
        assert stmt.else_body is None

    def test_if_else_statement(self):
        program = parse('if (x > 0) { print 1; } else { print 0; }')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.IfStatement)
        assert stmt.else_body is not None

    def test_while_statement(self):
        program = parse('while (i < 10) { i = i + 1; }')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.WhileStatement)


class TestParserFunctions:
    """Tests for parsing function declarations."""

    def test_simple_function(self):
        program = parse('fn add(a: int, b: int) -> int { return a + b; }')
        decl = program.declarations[0]
        assert isinstance(decl, ast.FunctionDeclaration)
        assert decl.name == 'add'
        assert len(decl.parameters) == 2
        assert decl.return_type == 'int'

    def test_function_call(self):
        program = parse('let x: int = add(1, 2);')
        expr = program.declarations[0].value
        assert isinstance(expr, ast.FunctionCall)
        assert expr.name == 'add'
        assert len(expr.arguments) == 2


class TestParserActions:
    """Tests for parsing bending action statements."""

    def test_spawn(self):
        program = parse('spawn(5, 5);')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.SpawnAction)

    def test_move(self):
        program = parse('move(Up);')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.MoveAction)
        assert stmt.direction == 'Up'

    def test_stance(self):
        program = parse('stance(OffensiveStance);')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.StanceAction)

    def test_strike(self):
        program = parse('strike(fireball, Right);')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.StrikeAction)

    def test_block_action(self):
        program = parse('block();')
        stmt = program.declarations[0]
        assert isinstance(stmt, ast.BlockAction)


class TestParserErrors:
    """Tests that the parser reports syntax errors."""

    def test_missing_semicolon(self):
        with pytest.raises(Exception):
            parse('let x: int = 42')

    def test_missing_type_annotation(self):
        with pytest.raises(Exception):
            parse('let x = 42;')
