
# Imports
from dataclasses import dataclass
from typing import List , Optional

# Base data class
@dataclass
class ASTNode :
    
    pass

# Program data class
@dataclass
class Program ( ASTNode ) :
    
    declarations : List [ ASTNode ]
    
# Literals data class
@dataclass
class IntLiteral ( ASTNode ) :
    
    value : int
    
@dataclass
class FloatLiteral ( ASTNode ) :
    
    value : float
    
@dataclass
class BooleanLiteral ( ASTNode ) :
    
    value : bool
    
@dataclass
class StringLiteral ( ASTNode ) :
    
    value : str
    
@dataclass
class ElementLiteral ( ASTNode ) :
    
    value : str
    
@dataclass
class StanceLiteral ( ASTNode ) :
    
    value : str
    
# Expressions data class
@dataclass
class Identifier ( ASTNode ) :
    
    name : str
    
@dataclass
class BinaryOperation ( ASTNode ) :
    
    left : ASTNode
    operator : str
    right : ASTNode

@dataclass
class UnaryOperation ( ASTNode ) :
    
    operator : str
    right : ASTNode
    
@dataclass
class FunctionCall ( ASTNode ) :
    
    name : str
    arguments : List [ ASTNode ]
    
# Function parameter node data class
@dataclass
class FunctionParameter ( ASTNode ) :
    
    name : str
    type_annotation : str
    
# Statement data class
@dataclass
class LetStatement ( ASTNode ) :
    
    name : str
    type_annotation : str
    value : ASTNode
    
@dataclass
class AssignStatement ( ASTNode ) :
    
    name : str
    value : ASTNode
    
@dataclass
class IfStatement ( ASTNode ) :
    
    condition : ASTNode
    then_body : ASTNode
    else_body : Optional [ ASTNode ] = None
    
@dataclass
class WhileStatement ( ASTNode ) :
    
    condition : ASTNode
    body : ASTNode
    
@dataclass
class ReturnStatement ( ASTNode ) :
    
    value : Optional [ ASTNode ] = None
    
@dataclass
class PrintStatement ( ASTNode ) :
    
    value : ASTNode
    
@dataclass
class BlockStatement ( ASTNode ) :
    
    statements : List [ ASTNode ]

@dataclass
class ExpressionStatement ( ASTNode ) :
    
    expression : ASTNode
    
# Function declaration data class
@dataclass
class FunctionDeclaration ( ASTNode ) :
    
    name : str
    parameters : List [ FunctionParameter ]
    return_type : str
    body : BlockStatement
    

# Bending action nodes data class
@dataclass
class SpawnAction ( ASTNode ) :
    
    x : ASTNode
    y : ASTNode
    
@dataclass
class MoveAction ( ASTNode ) :
    
    direction : str
    
@dataclass
class StanceAction ( ASTNode ) :
    
    stance : str
    
@dataclass
class StrikeAction ( ASTNode ) :
    
    element : ASTNode
    direction : str
    
@dataclass
class BlockAction ( ASTNode ) :
    
    pass


    
