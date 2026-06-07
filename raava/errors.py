"""Raava Error System — Vaatu Corruptions and Dark Spirit Warnings.

This module defines the error hierarchy for the Raava compiler.
All compiler errors are themed around Avatar: The Last Airbender.

Error Hierarchy:
    RaavaError (base)
    ├── VaatuCorruption (fatal — compilation halts)
    │   ├── SyntaxCorruption        — Invalid syntax
    │   ├── TypeMismatch            — Incompatible types
    │   ├── UndeclaredSpirit        — Undefined variable/function
    │   ├── DuplicateSpirit         — Variable/function already declared
    │   ├── ResourceLeak            — Linear resource not consumed
    │   ├── UseAfterConsume         — Linear resource used twice
    │   ├── InvalidStanceTransition — Illegal stance change
    │   └── InvalidBendingMove      — Wrong action for current stance
    └── DarkSpiritWarning (non-fatal — compilation continues)
        ├── UnusedBinding           — Variable declared but never used
        └── ShadowedSpirit          — Variable shadows an outer scope
"""


class RaavaError(Exception):
    """Base class for all Raava compiler errors."""

    def __init__(self, message: str, line: int = 0, column: int = 0,
                 source_line: str = "", filename: str = "<stdin>"):
        self.message = message
        self.line = line
        self.column = column
        self.source_line = source_line
        self.filename = filename
        super().__init__(self.format_error())

    def format_error(self) -> str:
        """Format the error in Rust-style with code snippet and caret pointer."""
        header = f"\n🔥 {self.__class__.__name__} — {self.error_title()}"
        location = f"  --> {self.filename}:{self.line}:{self.column}"

        if self.source_line:
            line_num_str = str(self.line)
            padding = " " * len(line_num_str)
            snippet = (
                f"   {padding}|\n"
                f"   {line_num_str} | {self.source_line}\n"
                f"   {padding} | {' ' * (self.column - 1)}^^^^ {self.message}\n"
                f"   {padding}|"
            )
        else:
            snippet = f"   | {self.message}"

        help_text = self.help_text()
        help_section = f"\n   = help: {help_text}" if help_text else ""

        return f"{header}\n{location}\n{snippet}{help_section}\n"

    def error_title(self) -> str:
        """Return a short title for this error category. Override in subclasses."""
        return "Unknown Error"

    def help_text(self) -> str:
        """Return optional help text. Override in subclasses."""
        return ""


# =============================================================================
# VAATU CORRUPTIONS (Fatal Errors — compilation halts)
# =============================================================================

class VaatuCorruption(RaavaError):
    """Fatal compiler error. Compilation halts immediately."""

    def error_title(self) -> str:
        return "Vaatu Corruption"


class SyntaxCorruption(VaatuCorruption):
    """Raised when the parser encounters invalid syntax."""

    def error_title(self) -> str:
        return "Syntax Corruption"

    def help_text(self) -> str:
        return "Check the Raava grammar reference in docs/grammar.bnf"


class TypeMismatch(VaatuCorruption):
    """Raised when types are incompatible in an operation or assignment."""

    def error_title(self) -> str:
        return "Type Mismatch"

    def help_text(self) -> str:
        return "Ensure both sides of the operation have compatible types."


class UndeclaredSpirit(VaatuCorruption):
    """Raised when a variable or function is used before being declared."""

    def error_title(self) -> str:
        return "Undeclared Spirit"

    def help_text(self) -> str:
        return "Declare the variable with 'let name: type = value;' before using it."


class DuplicateSpirit(VaatuCorruption):
    """Raised when a variable or function is declared twice in the same scope."""

    def error_title(self) -> str:
        return "Duplicate Spirit"

    def help_text(self) -> str:
        return "Choose a different name, or remove the duplicate declaration."


class ResourceLeak(VaatuCorruption):
    """Raised when a linear Element resource is never consumed before its scope ends."""

    def error_title(self) -> str:
        return "Resource Leak"

    def help_text(self) -> str:
        return "Use 'strike(element, <direction>)' to consume this element before its scope ends."


class UseAfterConsume(VaatuCorruption):
    """Raised when a linear Element resource is used after it has already been consumed."""

    def error_title(self) -> str:
        return "Use After Consume"

    def help_text(self) -> str:
        return "A consumed element cannot be reused. Create a new element instead."


class InvalidStanceTransition(VaatuCorruption):
    """Raised when an invalid stance transition is attempted."""

    def error_title(self) -> str:
        return "Invalid Stance Transition"


class InvalidBendingMove(VaatuCorruption):
    """Raised when a bending action is invalid for the current stance."""

    def error_title(self) -> str:
        return "Invalid Bending Move"


# =============================================================================
# DARK SPIRIT WARNINGS (Non-Fatal — compilation continues)
# =============================================================================

class DarkSpiritWarning(RaavaError):
    """Non-fatal compiler warning. Compilation continues."""

    def format_error(self) -> str:
        """Warnings use a different emoji and tone."""
        header = f"\n👻 Dark Spirit Warning — {self.error_title()}"
        location = f"  --> {self.filename}:{self.line}:{self.column}"

        if self.source_line:
            line_num_str = str(self.line)
            padding = " " * len(line_num_str)
            snippet = (
                f"   {padding}|\n"
                f"   {line_num_str} | {self.source_line}\n"
                f"   {padding} | {' ' * (self.column - 1)}~~~~ {self.message}\n"
                f"   {padding}|"
            )
        else:
            snippet = f"   | {self.message}"

        help_text = self.help_text()
        help_section = f"\n   = note: {help_text}" if help_text else ""

        return f"{header}\n{location}\n{snippet}{help_section}\n"


class UnusedBinding(DarkSpiritWarning):
    """Raised when a variable is declared but never used."""

    def error_title(self) -> str:
        return "Unused Binding"

    def help_text(self) -> str:
        return "If this is intentional, prefix the variable name with an underscore: '_name'"


class ShadowedSpirit(DarkSpiritWarning):
    """Raised when a variable in an inner scope shadows a variable in an outer scope."""

    def error_title(self) -> str:
        return "Shadowed Spirit"

    def help_text(self) -> str:
        return "Consider renaming to avoid confusion with the outer variable."
