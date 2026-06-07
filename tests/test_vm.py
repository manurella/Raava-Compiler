"""Tests for the Raava Virtual Machine.

These tests are written FIRST (TDD). Implement raava/vm.py
to make them pass.
"""
import pytest
from raava.lexer import Lexer
from raava.parser import Parser
from raava.typechecker import TypeChecker
from raava.ir_generator import IRGenerator
from raava.optimizer import Optimizer
from raava.codegen import CodeGenerator
from raava.vm import VirtualMachine


def run_program(source: str) -> list:
    """Helper: full pipeline — compile and run, capture printed output."""
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
    bytecode = codegen.generate(optimized)
    vm = VirtualMachine(bytecode)
    return vm.run()


class TestVMBasics:
    """Tests for basic VM execution."""

    def test_print_integer(self):
        output = run_program('print 42;')
        assert output == [42]

    def test_print_addition(self):
        output = run_program('let x: int = 10 + 20; print x;')
        assert output == [30]

    def test_print_subtraction(self):
        output = run_program('let x: int = 50 - 8; print x;')
        assert output == [42]

    def test_print_multiplication(self):
        output = run_program('let x: int = 6 * 7; print x;')
        assert output == [42]

    def test_print_boolean_true(self):
        output = run_program('let x: bool = true; print x;')
        assert output == [True]


class TestVMVariables:
    """Tests for variable operations."""

    def test_variable_assignment(self):
        output = run_program('let x: int = 10; let y: int = x + 5; print y;')
        assert output == [15]

    def test_variable_reassignment(self):
        output = run_program('let x: int = 10; x = 20; print x;')
        assert output == [20]


class TestVMControlFlow:
    """Tests for control flow execution."""

    def test_if_true_branch(self):
        output = run_program('if (true) { print 1; } else { print 0; }')
        assert output == [1]

    def test_if_false_branch(self):
        output = run_program('if (false) { print 1; } else { print 0; }')
        assert output == [0]

    def test_while_loop(self):
        source = """
            let i: int = 0;
            while (i < 3) {
                print i;
                i = i + 1;
            }
        """
        output = run_program(source)
        assert output == [0, 1, 2]


class TestVMFunctions:
    """Tests for function calls."""

    def test_simple_function_call(self):
        source = """
            fn add(a: int, b: int) -> int {
                return a + b;
            }
            let result: int = add(3, 4);
            print result;
        """
        output = run_program(source)
        assert output == [7]

    def test_recursive_function(self):
        source = """
            fn factorial(n: int) -> int {
                if (n <= 1) {
                    return 1;
                }
                return n * factorial(n - 1);
            }
            let result: int = factorial(5);
            print result;
        """
        output = run_program(source)
        assert output == [120]
