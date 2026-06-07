# Raava Compiler — Architecture

## Pipeline Overview

```
Source Code (.raava)
       │
       ▼
┌─────────────┐
│   Lexer     │  Converts characters → Tokens
│ (tokens.py  │
│  lexer.py)  │
└──────┬──────┘
       │ List[Token]
       ▼
┌─────────────┐
│   Parser    │  Converts Tokens → Abstract Syntax Tree
│ (ast_nodes  │
│  parser.py) │
└──────┬──────┘
       │ AST (tree of nodes)
       ▼
┌──────────────┐
│ Type Checker │  Validates types, scopes, linear resources
│(typechecker) │
└──────┬───────┘
       │ Validated AST
       ▼
┌──────────────┐
│ IR Generator │  Converts AST → Three-Address Code
│(ir_generator)│
└──────┬───────┘
       │ List[IRInstruction]
       ▼
┌─────────────┐
│  Optimizer  │  Constant folding, dead code elimination
│(optimizer)  │
└──────┬──────┘
       │ Optimized List[IRInstruction]
       ▼
┌──────────────┐
│Code Generator│  Converts 3AC → Bytecode
│ (codegen.py) │
└──────┬───────┘
       │ List[Bytecode]
       ▼
┌──────────────┐
│  Virtual     │  Executes bytecode, produces output
│  Machine     │  and JSON execution log
│  (vm.py)     │
└──────┬───────┘
       │ stdout + execution_log.json
       ▼
┌──────────────┐
│  Visualizer  │  Renders bending grid simulation
│  (HTML/JS)   │  from execution log
└──────────────┘
```

## Three-Address Code (3AC)

Three-Address Code is an intermediate representation where each instruction has at most three operands.

### Format
```
result = operand1 op operand2
```

### Example
Source:
```raava
let x: int = 2 + 3 * 4;
```

3AC:
```
t0 = 3 * 4
t1 = 2 + t0
x = t1
```

### Instruction Types
| Type | Format | Example |
|---|---|---|
| Binary Op | `result = left op right` | `t0 = a + b` |
| Unary Op | `result = op operand` | `t0 = -x` |
| Copy | `result = source` | `x = t0` |
| Constant | `result = value` | `t0 = 42` |
| Jump | `JUMP label` | `JUMP L2` |
| Conditional Jump | `JUMP_IF_FALSE cond label` | `JUMP_IF_FALSE t0 L1` |
| Label | `label:` | `L1:` |
| Call | `result = CALL func args` | `t0 = CALL add [a, b]` |
| Return | `RETURN value` | `RETURN t0` |
| Print | `PRINT value` | `PRINT x` |
| Action | `ACTION type args` | `ACTION spawn [5, 5]` |
