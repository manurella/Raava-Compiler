
# Imports
from enum import Enum , auto

# Token type class
class TokenType ( Enum ) :
    
    # Special Tokens
    EOF = auto ( )
    
    IDENTIFIER = auto ( )
    
    INT_LITERAL = auto ( )
    FLOAT_LITERAL = auto ( )
    BOOLEAN_LITERAL = auto ( )
    STRING_LITERAL = auto ( )
    
    # General Tokens ( Keywords )
    LET = auto ( )
    FN = auto ( )
    
    IF = auto ( )
    ELSE = auto ( )
    WHILE = auto ( )
    
    RETURN = auto ( )
    PRINT = auto ( )
    
    TRUE = auto ( )
    FALSE = auto ( )
    
    # Types
    INT_TYPE = auto ( )
    FLOAT_TYPE = auto ( )
    BOOLEAN_TYPE = auto ( )
    STRING_TYPE = auto ( )
    
    # Element Literals
    FIRE = auto ( )
    AIR = auto ( )
    WATER = auto ( )
    EARTH = auto ( )
    
    # Stance Literals
    NEUTRALSTANCE = auto ( )
    OFFENSIVESTANCE = auto ( )
    DEFENSIVESTANCE = auto ( )
    
    # Action Keywords
    SPAWN = auto ( )
    MOVE = auto ( )
    STANCE = auto ( )
    STRIKE = auto ( )
    BLOCK = auto ( )
    
    # Directions
    UP = auto ( )
    DOWN = auto ( )
    LEFT = auto ( )
    RIGHT = auto ( )
    
    # Math Operators
    PLUS = auto ( )
    MINUS = auto ( )
    STAR = auto ( )
    SLASH = auto ( )
    EQUALS = auto ( )
    
    # Comparison Operators
    EQ_EQ = auto ( )
    BANG_EQ = auto ( )
    LESS_THAN = auto ( )
    GREATER_THAN = auto ( )
    LESS_THAN_EQ = auto ( )
    GREATER_THAN_EQ = auto ( )
    ARROW = auto ( )

    # Logical Operators
    AND = auto ( )
    OR = auto ( )
    NOT = auto ( )
    
    # Symbols
    COLON = auto ( )
    SEMICOLON = auto ( )
    COMMA = auto ( )
    LEFT_PAREN = auto ( )
    RIGHT_PAREN = auto ( )
    LEFT_BRACE = auto ( )
    RIGHT_BRACE = auto ( )
    
# Token class
class Token :
    
    # Token constructor method
    def __init__ ( self , type : TokenType , value : str , line : int , column : int ) :
        self.type = type
        self.value = value
        self.line = line
        self.column = column
        
    # Representation method to print the object
    def __repr__ ( self ) -> str :
        return f"Token ( { self.type.name } , { self.value } , { self.line } , { self.column } )"
