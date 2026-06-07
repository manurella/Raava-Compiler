# Raava VM — Bytecode Specification

## VM Architecture

The Raava VM is a **stack-based virtual machine**.

### Components
| Component | Description |
|---|---|
| **Stack** | Operand stack for pushing/popping values during computation |
| **Call Stack** | Stack of frames, each containing local variables and a return address |
| **Instruction Pointer (IP)** | Index of the current bytecode instruction |
| **Program** | Flat array of bytecode instructions |
| **Execution Log** | JSON log of grid actions for the visualizer |

### How a Stack Machine Works

Instead of using named registers (like `ADD r1, r2, r3`), a stack machine pushes values onto a stack and operations pop their inputs and push their result.

**Example:** Computing `2 + 3`
```
Instruction    Stack (top on right)
-----------    --------------------
PUSH 2         [2]
PUSH 3         [2, 3]
ADD            [5]          ← popped 2 and 3, pushed 2+3=5
```

## Opcode Reference

| Opcode | Operand | Stack Effect | Description |
|---|---|---|---|
| `PUSH_INT` | `int value` | → value | Push integer constant |
| `PUSH_BOOL` | `bool value` | → value | Push boolean constant |
| `PUSH_ELEMENT` | `Element value` | → value | Push element constant |
| `PUSH_STANCE` | `Stance value` | → value | Push stance constant |
| `POP` | — | value → | Discard top of stack |
| `ADD` | — | a, b → (a+b) | Integer addition |
| `SUB` | — | a, b → (a-b) | Integer subtraction |
| `MUL` | — | a, b → (a*b) | Integer multiplication |
| `DIV` | — | a, b → (a/b) | Integer division |
| `NEG` | — | a → (-a) | Integer negation |
| `EQ` | — | a, b → (a==b) | Equality comparison |
| `NEQ` | — | a, b → (a!=b) | Inequality comparison |
| `LT` | — | a, b → (a<b) | Less than |
| `GT` | — | a, b → (a>b) | Greater than |
| `LTE` | — | a, b → (a<=b) | Less than or equal |
| `GTE` | — | a, b → (a>=b) | Greater than or equal |
| `AND` | — | a, b → (a and b) | Logical AND |
| `OR` | — | a, b → (a or b) | Logical OR |
| `NOT` | — | a → (not a) | Logical NOT |
| `LOAD` | `int index` | → value | Push local variable onto stack |
| `STORE` | `int index` | value → | Pop stack into local variable |
| `JUMP` | `int addr` | — | Unconditional jump |
| `JUMP_IF_FALSE` | `int addr` | cond → | Pop; jump if false |
| `CALL` | `int addr, int argc` | args → retval | Call function |
| `RETURN` | — | retval → | Return from function |
| `PRINT` | — | value → | Pop and print value |
| `ACTION_SPAWN` | — | y, x → | Pop coords, spawn bender |
| `ACTION_MOVE` | `Direction dir` | — | Move bender |
| `ACTION_STANCE` | `Stance s` | — | Change stance |
| `ACTION_STRIKE` | `Direction dir` | elem → | Pop element, strike |
| `ACTION_BLOCK` | — | — | Block |
| `HALT` | — | — | Stop execution |
