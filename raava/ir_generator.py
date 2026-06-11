# Imports
from typing import List, Optional, Any
from raava import ast_nodes as ast
from raava.ir import IROpCode, IRInstruction

# IRGenerator class
class IRGenerator:
    
    # IRGenerator constructor method
    def __init__ ( self ) :
        
        self.instructions : List [ IRInstruction ] = [ ]
        self.temp_counter = 0
        self.label_counter = 0
        
    # Helper to generate a new temporary variable
    def new_temp ( self ) -> str :
        
        self.temp_counter += 1
        return f"t{ self.temp_counter }"
        
    # Helper to generate a new label name
    def new_label ( self ) -> str :
        
        self.label_counter += 1
        return f"L{ self.label_counter }"
        
    # Main generate entry method
    def generate ( self , program : ast.Program ) -> List [ IRInstruction ] :
        
        self.instructions = [ ]
        self.check ( program )
        return self.instructions
        
    # Main check dispatcher method
    def check ( self , node : ast.ASTNode ) -> Optional [ str ] :
        
        method_name = f"check_{ node.__class__.__name__ }"
        visitor = getattr ( self , method_name , self.generic_check )
        return visitor ( node )
        
    # Fallback check method
    def generic_check ( self , node : ast.ASTNode ) -> Optional [ str ] :
        
        return None
        
    # Program check method
    def check_Program ( self , node : ast.Program ) -> Optional [ str ] :
        
        for decl in node.declarations :
            
            self.check ( decl )
            
        return None
        
    # Function declaration check method
    def check_FunctionDeclaration ( self , node : ast.FunctionDeclaration ) -> Optional [ str ] :
        
        # We pass parameter details in value
        self.instructions.append ( IRInstruction ( IROpCode.FUNC_START , result = node.name , value = node.parameters ) )
        
        self.check ( node.body )
        
        self.instructions.append ( IRInstruction ( IROpCode.FUNC_END , result = node.name ) )
        
        return None
        
    # Let statement check method
    def check_LetStatement ( self , node : ast.LetStatement ) -> Optional [ str ] :
        
        val_temp = self.check ( node.value )
        
        # Copy the value from temporary to the variable name
        self.instructions.append ( IRInstruction ( IROpCode.COPY , result = node.name , arg1 = val_temp ) )
        
        return None
        
    # Assignment statement check method
    def check_AssignStatement ( self , node : ast.AssignStatement ) -> Optional [ str ] :
        
        val_temp = self.check ( node.value )
        
        self.instructions.append ( IRInstruction ( IROpCode.COPY , result = node.name , arg1 = val_temp ) )
        
        return None
        
    # If statement check method
    def check_IfStatement ( self , node : ast.IfStatement ) -> Optional [ str ] :
        
        cond_temp = self.check ( node.condition )
        
        else_label = self.new_label ( )
        end_label = self.new_label ( )
        
        # Jump to else block if condition is false
        self.instructions.append ( IRInstruction ( IROpCode.JUMP_IF_FALSE , arg1 = cond_temp , result = else_label ) )
        
        self.check ( node.then_body )
        
        self.instructions.append ( IRInstruction ( IROpCode.JUMP , result = end_label ) )
        
        self.instructions.append ( IRInstruction ( IROpCode.LABEL , result = else_label ) )
        
        if node.else_body is not None :
            
            self.check ( node.else_body )
            
        self.instructions.append ( IRInstruction ( IROpCode.LABEL , result = end_label ) )
        
        return None
        
    # While statement check method
    def check_WhileStatement ( self , node : ast.WhileStatement ) -> Optional [ str ] :
        
        start_label = self.new_label ( )
        end_label = self.new_label ( )
        
        self.instructions.append ( IRInstruction ( IROpCode.LABEL , result = start_label ) )
        
        cond_temp = self.check ( node.condition )
        
        self.instructions.append ( IRInstruction ( IROpCode.JUMP_IF_FALSE , arg1 = cond_temp , result = end_label ) )
        
        self.check ( node.body )
        
        self.instructions.append ( IRInstruction ( IROpCode.JUMP , result = start_label ) )
        
        self.instructions.append ( IRInstruction ( IROpCode.LABEL , result = end_label ) )
        
        return None
        
    # Block statement check method
    def check_BlockStatement ( self , node : ast.BlockStatement ) -> Optional [ str ] :
        
        for stmt in node.statements :
            
            self.check ( stmt )
            
        return None
        
    # Expression statement check method
    def check_ExpressionStatement ( self , node : ast.ExpressionStatement ) -> Optional [ str ] :
        
        self.check ( node.expression )
        
        return None
        
    # Print statement check method
    def check_PrintStatement ( self , node : ast.PrintStatement ) -> Optional [ str ] :
        
        val_temp = self.check ( node.value )
        
        self.instructions.append ( IRInstruction ( IROpCode.PRINT , arg1 = val_temp ) )
        
        return None
        
    # Return statement check method
    def check_ReturnStatement ( self , node : ast.ReturnStatement ) -> Optional [ str ] :
        
        val_temp = None
        
        if node.value is not None :
            
            val_temp = self.check ( node.value )
            
        self.instructions.append ( IRInstruction ( IROpCode.RETURN , arg1 = val_temp ) )
        
        return None
        
    # Spawn action check method
    def check_SpawnAction ( self , node : ast.SpawnAction ) -> Optional [ str ] :
        
        x_temp = self.check ( node.x )
        y_temp = self.check ( node.y )
        
        self.instructions.append ( IRInstruction ( IROpCode.SPAWN , arg1 = x_temp , arg2 = y_temp ) )
        
        return None
        
    # Move action check method
    def check_MoveAction ( self , node : ast.MoveAction ) -> Optional [ str ] :
        
        self.instructions.append ( IRInstruction ( IROpCode.MOVE , arg1 = node.direction ) )
        
        return None
        
    # Stance action check method
    def check_StanceAction ( self , node : ast.StanceAction ) -> Optional [ str ] :
        
        self.instructions.append ( IRInstruction ( IROpCode.STANCE , arg1 = node.stance ) )
        
        return None
        
    # Strike action check method
    def check_StrikeAction ( self , node : ast.StrikeAction ) -> Optional [ str ] :
        
        elem_temp = self.check ( node.element )
        
        self.instructions.append ( IRInstruction ( IROpCode.STRIKE , arg1 = elem_temp , arg2 = node.direction ) )
        
        return None
        
    # Block action check method
    def check_BlockAction ( self , node : ast.BlockAction ) -> Optional [ str ] :
        
        self.instructions.append ( IRInstruction ( IROpCode.BLOCK ) )
        
        return None
        
    # Int literal check method
    def check_IntLiteral ( self , node : ast.IntLiteral ) -> str :
        
        temp = self.new_temp ( )
        self.instructions.append ( IRInstruction ( IROpCode.CONST , result = temp , value = node.value ) )
        return temp
        
    # Float literal check method
    def check_FloatLiteral ( self , node : ast.FloatLiteral ) -> str :
        
        temp = self.new_temp ( )
        self.instructions.append ( IRInstruction ( IROpCode.CONST , result = temp , value = node.value ) )
        return temp
        
    # Boolean literal check method
    def check_BooleanLiteral ( self , node : ast.BooleanLiteral ) -> str :
        
        temp = self.new_temp ( )
        self.instructions.append ( IRInstruction ( IROpCode.CONST , result = temp , value = node.value ) )
        return temp
        
    # String literal check method
    def check_StringLiteral ( self , node : ast.StringLiteral ) -> str :
        
        temp = self.new_temp ( )
        self.instructions.append ( IRInstruction ( IROpCode.CONST , result = temp , value = node.value ) )
        return temp
        
    # Element literal check method
    def check_ElementLiteral ( self , node : ast.ElementLiteral ) -> str :
        
        temp = self.new_temp ( )
        self.instructions.append ( IRInstruction ( IROpCode.CONST , result = temp , value = node.value ) )
        return temp
        
    # Stance literal check method
    def check_StanceLiteral ( self , node : ast.StanceLiteral ) -> str :
        
        temp = self.new_temp ( )
        self.instructions.append ( IRInstruction ( IROpCode.CONST , result = temp , value = node.value ) )
        return temp
        
    # Identifier check method
    def check_Identifier ( self , node : ast.Identifier ) -> str :
        
        # Identifiers represent existing variables, so we just return their name
        return node.name
        
    # Binary operation check method
    def check_BinaryOperation ( self , node : ast.BinaryOperation ) -> str :
        
        left_temp = self.check ( node.left )
        right_temp = self.check ( node.right )
        
        result_temp = self.new_temp ( )
        
        self.instructions.append (
            IRInstruction (
                IROpCode.BINARY_OP ,
                result = result_temp ,
                arg1 = left_temp ,
                arg2 = right_temp ,
                value = node.operator
            )
        )
        
        return result_temp
        
    # Unary operation check method
    def check_UnaryOperation ( self , node : ast.UnaryOperation ) -> str :
        
        right_temp = self.check ( node.right )
        
        result_temp = self.new_temp ( )
        
        self.instructions.append (
            IRInstruction (
                IROpCode.UNARY_OP ,
                result = result_temp ,
                arg1 = right_temp ,
                value = node.operator
            )
        )
        
        return result_temp
        
    # Function call check method
    def check_FunctionCall ( self , node : ast.FunctionCall ) -> str :
        
        arg_temps = [ ]
        
        for arg in node.arguments :
            
            arg_temps.append ( self.check ( arg ) )
            
        result_temp = self.new_temp ( )
        
        self.instructions.append (
            IRInstruction (
                IROpCode.CALL ,
                result = result_temp ,
                arg1 = node.name ,
                arg2 = arg_temps
            )
        )
        
        return result_temp
