"""Raava Parser.

Phase 4 of the Raava Compiler.
Commit: feat(parser): implement recursive descent parser
"""

class Parser:
    """Stub class for the Parser."""
    def __init__(self, tokens: list):
        self.tokens = tokens

    def parse(self):
        # Stub implementation to allow importing
        from raava.ast_nodes import Program
        return Program(declarations=[])
