"""Tests for the Raava Code Generator.

These tests are written FIRST (TDD). Implement raava/opcodes.py and raava/codegen.py
to make them pass.
"""
import pytest
from raava.lexer import Lexer
from raava.parser import Parser
from raava.typechecker import TypeChecker
from raava.ir_generator import IRGenerator
from raava.optimizer import Optimizer
from raava.codegen import CodeGenerator
from raava.opcodes import OpCode


def compile_to_bytecode(source: str):
    """Helper: full pipeline up to bytecode generation."""
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    checker = TypeChecker()
    checker.check(program)
    generator = IRGenerator()
    instructions = generator.generate(program)
    optimizer = Optimizer()
    optimized = optimizer.optimize(instructions)
    codegen = CodeGenerator()
    return codegen.generate(optimized)


class TestCodeGenBasics:
    """Tests for basic bytecode generation."""

    def test_push_constant(self):
        """A constant should generate a PUSH_INT instruction."""
        bytecode = compile_to_bytecode('let x: int = 42; print x;')
        opcodes = [instr.opcode for instr in bytecode]
        assert OpCode.PUSH_INT in opcodes

    def test_add_instruction(self):
        """Addition should generate an ADD instruction."""
        bytecode = compile_to_bytecode('let x: int = 1 + 2; print x;')
        opcodes = [instr.opcode for instr in bytecode]
        assert OpCode.ADD in opcodes

    def test_halt_at_end(self):
        """Program should end with a HALT instruction."""
        bytecode = compile_to_bytecode('print 42;')
        assert bytecode[-1].opcode == OpCode.HALT
