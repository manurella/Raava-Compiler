# Contributing to Raava Compiler

## For Learners

1. **Fork** this repository
2. **Clone** your fork: `git clone https://github.com/<your-username>/Raava-Compiler.git`
3. **Switch** to the starter branch: `git checkout starter`
4. **Install** dev dependencies: `pip install -r requirements-dev.txt`
5. **Follow** the learning path: `.github/LEARNING_PATH.md`

## Conventional Commits

All commits must follow this format:
```
<type>(<scope>): <description>
```

**Types:** `feat`, `fix`, `test`, `docs`, `chore`, `refactor`

**Scopes:** `tokens`, `lexer`, `ast`, `parser`, `typechecker`, `ir`, `optimizer`, `opcodes`, `codegen`, `vm`, `cli`, `visualizer`, `errors`, `project`

**Examples:**
- `feat(lexer): implement tokenizer`
- `test(parser): add parser test suite`
- `fix(typechecker): handle nested scope correctly`
- `docs(readme): update installation instructions`

## Running Tests

```bash
pytest                         # Run all tests
pytest tests/test_lexer.py     # Run specific test file
pytest -v                      # Verbose output
pytest -k "test_addition"      # Run tests matching a pattern
```

## Code Style

- Use type hints on all function signatures
- Use `dataclass` for data-holding classes
- Keep functions short and focused
- Add docstrings to all public classes and functions
