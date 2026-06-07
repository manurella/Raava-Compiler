# Raava Language Specification

> *"In the era before the Avatar, we bent not the elements, but the code itself."*

## 1. Overview

Raava is a statically-typed, imperative programming language with:
- Integer and boolean primitive types
- Element and Stance enum types for bending simulation
- Linear resource safety for Element values
- Functions with explicit type annotations
- Control flow (if/else, while)
- Grid-based bending simulation commands

## 2. Lexical Rules

### 2.1 Whitespace
Spaces, tabs, carriage returns, and newlines are ignored (they only separate tokens).

### 2.2 Comments
Single-line comments start with `//` and extend to the end of the line.
```raava
// This is a comment
let x: int = 42; // This is also a comment
```

### 2.3 Identifiers
An identifier starts with a letter or underscore, followed by letters, digits, or underscores.
```
IDENTIFIER = [a-zA-Z_][a-zA-Z0-9_]*
```

### 2.4 Integer Literals
A sequence of one or more digits.
```
INT_LITERAL = [0-9]+
```

### 2.5 Keywords
The following identifiers are reserved keywords and cannot be used as variable or function names:
```
let  fn  if  else  while  return  print
int  bool  Element  Stance
true  false
Water  Earth  Fire  Air
NeutralStance  OffensiveStance  DefensiveStance
spawn  move  stance  strike  block
Up  Down  Left  Right
and  or  not
```

### 2.6 Operators and Symbols
```
+  -  *  /  =  ==  !=  <  >  <=  >=
:  ;  ,  (  )  {  }  ->
```

## 3. Type System

### 3.1 Primitive Types
| Type | Description | Example |
|---|---|---|
| `int` | 64-bit signed integer | `42`, `-7`, `0` |
| `bool` | Boolean value | `true`, `false` |

### 3.2 Enum Types
| Type | Variants |
|---|---|
| `Element` | `Water`, `Earth`, `Fire`, `Air` |
| `Stance` | `NeutralStance`, `OffensiveStance`, `DefensiveStance` |

### 3.3 Type Compatibility Rules
| Operation | Left Type | Right Type | Result Type |
|---|---|---|---|
| `+`, `-`, `*`, `/` | `int` | `int` | `int` |
| `<`, `>`, `<=`, `>=` | `int` | `int` | `bool` |
| `==`, `!=` | `int` | `int` | `bool` |
| `==`, `!=` | `bool` | `bool` | `bool` |
| `and`, `or` | `bool` | `bool` | `bool` |
| `not` | — | `bool` | `bool` |
| `-` (unary) | — | `int` | `int` |

## 4. Linear Resource Safety

`Element` values follow linear type rules:

1. **Must Consume:** An `Element` variable must be consumed (via `strike()`) before its scope ends.
2. **No Double Spend:** An `Element` variable cannot be consumed more than once.
3. **No Implicit Copy:** Assigning an `Element` variable to another moves ownership (the original becomes invalid).

## 5. Bending Simulation Commands

| Command | Arguments | Description |
|---|---|---|
| `spawn(x, y)` | `int`, `int` | Place the bender at grid position (x, y) |
| `move(dir)` | `Direction` | Move one tile in the given direction |
| `stance(s)` | `Stance` | Transition to a new stance |
| `strike(elem, dir)` | `Element`, `Direction` | Consume element, attack in direction |
| `block()` | — | Raise a defensive shield |

## 6. Scoping

- Variables declared with `let` are visible from the point of declaration to the end of their enclosing block `{}`.
- Functions have their own local scope.
- Inner blocks can shadow variables from outer blocks (triggers a `DarkSpiritWarning`).
