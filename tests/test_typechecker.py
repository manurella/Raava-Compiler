"""Tests for the Raava Type Checker.

These tests are written FIRST (TDD). Implement raava/typechecker.py
to make them pass.
"""
import pytest
from raava.lexer import Lexer
from raava.parser import Parser
from raava.typechecker import TypeChecker
from raava.errors import VaatuCorruption


def typecheck(source: str):
    """Helper: lex, parse, and type-check a source string."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    checker = TypeChecker()
    checker.check(program)


class TestTypeCheckerBasics:
    """Tests for basic type checking."""

    def test_valid_int_declaration(self):
        """Should not raise for valid int declaration."""
        typecheck('let x: int = 42;')

    def test_valid_bool_declaration(self):
        """Should not raise for valid bool declaration."""
        typecheck('let flag: bool = true;')

    def test_type_mismatch_int_bool(self):
        """Assigning a bool to an int should raise VaatuCorruption."""
        with pytest.raises(VaatuCorruption):
            typecheck('let x: int = true;')

    def test_type_mismatch_bool_int(self):
        """Assigning an int to a bool should raise VaatuCorruption."""
        with pytest.raises(VaatuCorruption):
            typecheck('let flag: bool = 42;')

    def test_arithmetic_type_mismatch(self):
        """Adding int and bool should raise VaatuCorruption."""
        with pytest.raises(VaatuCorruption):
            typecheck('let x: int = 5 + true;')


class TestTypeCheckerScoping:
    """Tests for variable scoping."""

    def test_undeclared_variable(self):
        """Using an undeclared variable should raise VaatuCorruption."""
        with pytest.raises(VaatuCorruption):
            typecheck('print x;')

    def test_duplicate_declaration(self):
        """Declaring a variable twice in the same scope should raise VaatuCorruption."""
        with pytest.raises(VaatuCorruption):
            typecheck('let x: int = 1; let x: int = 2;')


class TestTypeCheckerFunctions:
    """Tests for function type checking."""

    def test_valid_function(self):
        typecheck('fn add(a: int, b: int) -> int { return a + b; }')

    def test_wrong_return_type(self):
        with pytest.raises(VaatuCorruption):
            typecheck('fn bad() -> int { return true; }')

    def test_wrong_argument_type(self):
        with pytest.raises(VaatuCorruption):
            typecheck("""
                fn add(a: int, b: int) -> int { return a + b; }
                let x: int = add(1, true);
            """)


class TestLinearResourceSafety:
    """Tests for linear resource safety (the CV feature!)."""

    def test_consumed_element_is_valid(self):
        """An element that is consumed via strike() should be fine."""
        typecheck("""
            let fireball: Element = Fire;
            strike(fireball, Up);
        """)

    def test_unconsumed_element_raises_error(self):
        """An element that is never consumed should raise ResourceLeak."""
        with pytest.raises(VaatuCorruption):
            typecheck("""
                let rock: Element = Earth;
                print 0;
            """)

    def test_double_consume_raises_error(self):
        """Using an element twice should raise UseAfterConsume."""
        with pytest.raises(VaatuCorruption):
            typecheck("""
                let wave: Element = Water;
                strike(wave, Left);
                strike(wave, Right);
            """)
