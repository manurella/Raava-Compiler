# Imports
from enum import Enum, auto
from typing import Optional, Any

# IR OpCode enum
class IROpCode ( Enum ) :
    
    CONST = auto ( )
    COPY = auto ( )
    BINARY_OP = auto ( )
    UNARY_OP = auto ( )
    LABEL = auto ( )
    JUMP = auto ( )
    JUMP_IF_FALSE = auto ( )
    PRINT = auto ( )
    RETURN = auto ( )
    CALL = auto ( )
    
    # Action OpCodes
    SPAWN = auto ( )
    MOVE = auto ( )
    STANCE = auto ( )
    STRIKE = auto ( )
    BLOCK = auto ( )
    
    # Function OpCodes
    FUNC_START = auto ( )
    FUNC_END = auto ( )


# IR Instruction class
class IRInstruction:
    
    # IR Instruction constructor
    def __init__ ( self , opcode : IROpCode , result : Optional [ str ] = None , \
                   arg1 : Optional [ Any ] = None , arg2 : Optional [ Any ] = None , \
                   value : Optional [ Any ] = None ) :
                   
        self.opcode = opcode
        self.result = result
        self.arg1 = arg1
        self.arg2 = arg2
        self.value = value
        
    # Representation method for debugging
    def __repr__ ( self ) -> str :
        
        parts = [ f"opcode={ self.opcode.name }" ]
        
        if self.result is not None :
            
            parts.append ( f"result={ self.result }" )
            
        if self.arg1 is not None :
            
            parts.append ( f"arg1={ self.arg1 }" )
            
        if self.arg2 is not None :
            
            parts.append ( f"arg2={ self.arg2 }" )
            
        if self.value is not None :
            
            parts.append ( f"value={ repr ( self.value ) }" )
            
        return f"IRInstruction ( { ', '.join ( parts ) } )"
