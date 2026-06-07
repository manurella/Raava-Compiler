# 🌀 Raava Compiler — Learning Path

Welcome, young bender! Follow this path to build the Raava compiler from scratch.

## How to Use This Path

1. Fork this repository
2. Switch to the `starter` branch: `git checkout starter`
3. Work through each phase in order
4. After completing each phase, run the tests to verify your work
5. Commit using the conventional commit message provided
6. Push and check that GitHub CI passes ✅

---

## Phase 1: Token Definitions
- [ ] 📖 Read: `docs/language_spec.md` (Section: Keywords & Operators)
- [ ] 📖 Understand: What is an `Enum`? What is `auto()`?
- [ ] 💻 Implement: `raava/tokens.py` — Define `TokenType` enum and `Token` class
- [ ] ✅ Test: `pytest tests/test_lexer.py -k "test_token"` (if applicable)
- [ ] 📝 Commit: `feat(tokens): define TokenType enum and Token class`

## Phase 2: Lexer (Tokenizer)
- [ ] 📖 Read: `docs/language_spec.md` (Section: Lexical Rules)
- [ ] 📖 Understand: How does a scanner read characters one-by-one?
- [ ] 💻 Implement: `raava/lexer.py` — The `Lexer` class with a `tokenize()` method
- [ ] ✅ Test: `pytest tests/test_lexer.py`
- [ ] 📝 Commit: `feat(lexer): implement tokenizer`

## Phase 3: AST Node Definitions
- [ ] 📖 Read: `docs/grammar.bnf`
- [ ] 📖 Understand: What is an Abstract Syntax Tree? What is a `dataclass`?
- [ ] 💻 Implement: `raava/ast_nodes.py` — Define all AST node classes
- [ ] 📝 Commit: `feat(ast): define AST node classes`

## Phase 4: Parser
- [ ] 📖 Read: `docs/grammar.bnf` (each BNF rule = one parser function)
- [ ] 📖 Understand: What is Recursive Descent? What is operator precedence?
- [ ] 💻 Implement: `raava/parser.py` — The `Parser` class
- [ ] ✅ Test: `pytest tests/test_parser.py`
- [ ] 📝 Commit: `feat(parser): implement recursive descent parser`

## Phase 5: Type Checker
- [ ] 📖 Read: `docs/language_spec.md` (Section: Type Rules & Linear Resources)
- [ ] 📖 Understand: What is a Symbol Table? What are linear types?
- [ ] 💻 Implement: `raava/typechecker.py` — The `TypeChecker` class
- [ ] ✅ Test: `pytest tests/test_typechecker.py`
- [ ] 📝 Commit: `feat(typechecker): implement type checking and linear resource safety`

## Phase 6: IR Generator & Optimizer
- [ ] 📖 Read: `docs/architecture.md` (Section: Three-Address Code)
- [ ] 📖 Understand: What is an IR? What is constant folding?
- [ ] 💻 Implement: `raava/ir.py`, `raava/ir_generator.py`, `raava/optimizer.py`
- [ ] ✅ Test: `pytest tests/test_ir_generator.py tests/test_optimizer.py`
- [ ] 📝 Commit: `feat(ir): implement IR generator and optimizer`

## Phase 7: Code Generator & VM
- [ ] 📖 Read: `docs/bytecode_spec.md`
- [ ] 📖 Understand: What is a stack machine? What is an opcode?
- [ ] 💻 Implement: `raava/opcodes.py`, `raava/codegen.py`, `raava/vm.py`
- [ ] ✅ Test: `pytest tests/test_codegen.py tests/test_vm.py`
- [ ] 📝 Commit: `feat(vm): implement bytecode compiler and virtual machine`

## Phase 8: CLI & Visualizer
- [ ] 💻 Implement: `main.py` — CLI entry point
- [ ] 💻 Implement: `visualizer/index.html`, `visualizer/style.css`, `visualizer/script.js`
- [ ] ✅ Test: `pytest tests/test_integration.py`
- [ ] 📝 Commit: `feat(cli): implement CLI and visualizer`

## Final: Integration Testing
- [ ] ✅ Run: `pytest -v` (all tests should pass)
- [ ] 🎮 Run: `python main.py run examples/05_bender_battle.raava --log output.json`
- [ ] 👁️ Open: `visualizer/index.html` and load `output.json`
- [ ] 🎉 Celebrate!
