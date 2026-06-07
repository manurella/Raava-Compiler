"""Tests for the Raava IR Generator.

These tests are written FIRST (TDD). Implement raava/ir.py and raava/ir_generator.py
to make them pass.
"""
import pytest
from raava.lexer import Lexer
from raava.parser import Parser
from raava.typechecker import TypeChecker
from raava.ir_generator import IRGenerator
from raava.ir import IROpCode


def generate_ir(source: str):
    """Helper: lex, parse, type-check, and generate IR."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    checker = TypeChecker()
    checker.check(program)
    generator = IRGenerator()
    return generator.generate(program)


class TestIRGeneratorBasics:
    """Tests for basic IR generation."""

    def test_constant_assignment(self):
        """A simple constant assignment should produce a CONST + COPY instruction."""
        instructions = generate_ir('let x: int = 42;')
        opcodes = [inst.opcode for inst in instructions]
        assert IROpCode.CONST in opcodes

    def test_binary_operation(self):
        """An addition should produce a BINARY_OP instruction."""
        instructions = generate_ir('let x: int = 1 + 2;')
        opcodes = [inst.opcode for inst in instructions]
        assert IROpCode.BINARY_OP in opcodes

    def test_print_statement(self):
        """A print statement should produce a PRINT instruction."""
        instructions = generate_ir('let x: int = 42; print x;')
        opcodes = [inst.opcode for inst in instructions]
        assert IROpCode.PRINT in opcodes
