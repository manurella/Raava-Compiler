"""Tests for the Raava Optimizer.

These tests are written FIRST (TDD). Implement raava/optimizer.py
to make them pass.
"""
import pytest
from raava.lexer import Lexer
from raava.parser import Parser
from raava.typechecker import TypeChecker
from raava.ir_generator import IRGenerator
from raava.optimizer import Optimizer
from raava.ir import IROpCode


def optimize(source: str):
    """Helper: full pipeline up to optimization."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    checker = TypeChecker()
    checker.check(program)
    generator = IRGenerator()
    instructions = generator.generate(program)
    optimizer = Optimizer()
    return optimizer.optimize(instructions)


class TestConstantFolding:
    """Tests for constant folding optimization."""

    def test_fold_addition(self):
        """2 + 3 should be folded to 5 at compile time."""
        instructions = optimize('let x: int = 2 + 3;')
        # After folding, there should be fewer instructions
        const_instructions = [i for i in instructions if i.opcode == IROpCode.CONST]
        # The folded result (5) should appear as a constant
        values = [i.value for i in const_instructions if i.value == 5]
        assert 5 in values

    def test_fold_multiplication(self):
        """3 * 4 should be folded to 12."""
        instructions = optimize('let x: int = 3 * 4;')
        const_instructions = [i for i in instructions if i.opcode == IROpCode.CONST]
        values = [i.value for i in const_instructions if i.value == 12]
        assert 12 in values
