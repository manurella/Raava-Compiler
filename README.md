# 🌀 Raava Compiler

> *"In the era before the Avatar, we bent not the elements, but the code itself."*

**Raava** is a statically-typed, resource-safe programming language themed around *Avatar: The Last Airbender* and *The Legend of Korra*. It compiles through a full pipeline — Lexer → Parser → Type Checker → IR Generator → Optimizer → Code Generator → Stack-Based VM — and produces a visual bending simulation.

[![Raava CI](https://github.com/<your-username>/Raava-Compiler/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/Raava-Compiler/actions/workflows/ci.yml)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧊 **Static Typing** | `int`, `bool`, `Element`, `Stance` with compile-time type checking |
| 🔒 **Linear Resource Safety** | Element values must be consumed exactly once (Rust/Move-inspired) |
| 🌊 **Bending Simulation** | `spawn`, `move`, `stance`, `strike`, `block` commands on a 2D grid |
| 🔥 **Vaatu Error System** | Rust-style error messages with Avatar-themed names |
| ⚡ **Three-Address Code IR** | Intermediate representation with constant folding & dead code elimination |
| 🎯 **Custom Bytecode VM** | Stack-based virtual machine executing compiled bytecode |
| 🎨 **Visual Simulator** | HTML/CSS/JS bending grid visualizer with animations |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or later
- pip

### Setup
```bash
git clone https://github.com/<your-username>/Raava-Compiler.git
cd Raava-Compiler
pip install -r requirements-dev.txt
```

### Run a Program
```bash
python main.py run examples/01_hello.raava
```

### Run with Visual Output
```bash
python main.py run examples/05_bender_battle.raava --log output.json
# Then open visualizer/index.html in your browser and load output.json
```

### Run Tests
```bash
pytest -v
```

---

## 📝 Language Overview

### Hello World
```raava
// Print a number
print 42;
```

### Variables and Arithmetic
```raava
let x: int = 10;
let y: int = 20;
let sum: int = x + y;
print sum;
```

### Control Flow
```raava
let x: int = 10;

if (x > 5) {
    print 1;
} else {
    print 0;
}

let i: int = 0;
while (i < 5) {
    print i;
    i = i + 1;
}
```

### Functions
```raava
fn factorial(n: int) -> int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

let result: int = factorial(5);
print result;
```

### Bending Simulation
```raava
spawn(5, 5);
stance(OffensiveStance);

let fireball: Element = Fire;
move(Up);
strike(fireball, Right);

stance(DefensiveStance);
block();
```

### Linear Resource Safety
```raava
// This will compile successfully:
let wave: Element = Water;
strike(wave, Left);

// This will FAIL at compile time:
let rock: Element = Earth;
// Vaatu Corruption — Resource Leak: 'rock' was never consumed
```

---

## 🏗️ Compiler Architecture

```
Source Code (.raava)
    │
    ▼
┌─────────────┐
│    Lexer    │ ──→ Tokens
└─────────────┘
    │
    ▼
┌─────────────┐
│   Parser    │ ──→ Abstract Syntax Tree
└─────────────┘
    │
    ▼
┌──────────────┐
│ Type Checker │ ──→ Validated AST (+ linear resource safety)
└──────────────┘
    │
    ▼
┌──────────────┐
│ IR Generator │ ──→ Three-Address Code
└──────────────┘
    │
    ▼
┌──────────────┐
│  Optimizer   │ ──→ Optimized Three-Address Code
└──────────────┘
    │
    ▼
┌──────────────┐
│  Code Gen    │ ──→ Bytecode
└──────────────┘
    │
    ▼
┌──────────────┐
│   VM + Viz   │ ──→ Output + Bending Grid Simulation
└──────────────┘
```

---

## 🔥 Vaatu Error System

Compiler errors are themed as **Vaatu Corruptions** (fatal) and **Dark Spirit Warnings** (non-fatal):

```
🔥 Vaatu Corruption — ResourceLeak
  --> bender_battle.raava:3:5
   |
 3 | let rock: Element = Earth;
   |     ^^^^ Linear resource 'rock' was never consumed.
   |
   = help: Use 'strike(rock, <direction>)' to consume this element.
```

---

## 📚 Documentation

- [Language Specification](docs/language_spec.md)
- [BNF Grammar](docs/grammar.bnf)
- [Architecture](docs/architecture.md)
- [Bytecode Specification](docs/bytecode_spec.md)

---

## 🎓 Learning Path

Want to build this compiler yourself? Check out the [Learning Path](.github/LEARNING_PATH.md) for a step-by-step guide with test-driven exercises.

---

## 📜 License

This project is for educational and coursework purposes.
