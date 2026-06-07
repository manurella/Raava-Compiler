"""Integration tests for the Raava Compiler.

These tests run the full pipeline: source -> lexer -> parser -> typechecker
-> ir_generator -> optimizer -> codegen -> vm.
"""
import pytest
from raava.lexer import Lexer
from raava.parser import Parser
from raava.typechecker import TypeChecker
from raava.ir_generator import IRGenerator
from raava.optimizer import Optimizer
from raava.codegen import CodeGenerator
from raava.vm import VirtualMachine
from raava.errors import VaatuCorruption


def run_program(source: str) -> list:
    """Full pipeline: source to output."""
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


class TestIntegrationArithmetic:
    """End-to-end arithmetic tests."""

    def test_complex_expression(self):
        output = run_program('let x: int = (2 + 3) * (4 - 1); print x;')
        assert output == [15]

    def test_nested_arithmetic(self):
        source = """
            let a: int = 10;
            let b: int = 20;
            let c: int = a * b + 5;
            print c;
        """
        output = run_program(source)
        assert output == [205]


class TestIntegrationFibonacci:
    """End-to-end Fibonacci test."""

    def test_fibonacci_10(self):
        source = """
            fn fibonacci(n: int) -> int {
                if (n <= 1) {
                    return n;
                }
                return fibonacci(n - 1) + fibonacci(n - 2);
            }
            let result: int = fibonacci(10);
            print result;
        """
        output = run_program(source)
        assert output == [55]


class TestIntegrationLinearResources:
    """End-to-end linear resource safety tests."""

    def test_valid_bending_sequence(self):
        source = """
            spawn(5, 5);
            let fireball: Element = Fire;
            stance(OffensiveStance);
            strike(fireball, Up);
            print 1;
        """
        output = run_program(source)
        assert output == [1]

    def test_resource_leak_detected(self):
        source = """
            let rock: Element = Earth;
            print 0;
        """
        with pytest.raises(VaatuCorruption):
            run_program(source)


class TestIntegrationMultipleOutputs:
    """Tests with multiple print statements."""

    def test_countdown(self):
        source = """
            let i: int = 5;
            while (i > 0) {
                print i;
                i = i - 1;
            }
        """
        output = run_program(source)
        assert output == [5, 4, 3, 2, 1]
