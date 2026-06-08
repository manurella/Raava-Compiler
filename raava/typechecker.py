# Imports
from typing import List, Dict, Optional
from raava import ast_nodes as ast
from raava.errors import (
    TypeMismatch,
    UndeclaredSpirit,
    DuplicateSpirit,
    ResourceLeak,
    UseAfterConsume,
    InvalidStanceTransition,
    InvalidBendingMove
)

# TypeChecker class
class TypeChecker:
    
    # TypeChecker constructor method
    def __init__ ( self ) :
        
        self.scopes : List [ Dict [ str , Dict ] ] = [ { } ]  # Scope stack (starts with global scope)
        self.functions : Dict [ str , Dict ] = { }            # Function environment
        self.current_return_type : Optional [ str ] = None    # Track current function's return type
        
    # Scope enter helper method
    def enter_scope ( self ) :
        
        self.scopes.append ( { } )
        
    # Scope exit helper method
    def exit_scope ( self ) :
        
        # Linear resource check: ensure all 'Element' variables in this scope were consumed
        innermost_scope = self.scopes [ -1 ]
        
        for name , info in innermost_scope.items ( ) :
            
            if info [ 'type' ] == 'Element' and not info [ 'consumed' ] :
                
                raise ResourceLeak ( f"Vaatu Corruption — Resource Leak: '{ name }' was never consumed." )
                
        self.scopes.pop ( )
        
    # Variable declaration helper method
    def declare ( self , name : str , type_str : str ) :
        
        innermost_scope = self.scopes [ -1 ]
        
        if name in innermost_scope :
            
            raise DuplicateSpirit ( f"Vaatu Corruption — Duplicate Spirit: '{ name }' is already declared in this scope." )
            
        innermost_scope [ name ] = {
            'type' : type_str ,
            'consumed' : False
        }
        
    # Variable lookup helper method
    def lookup ( self , name : str ) -> Optional [ Dict ] :
        
        for scope in reversed ( self.scopes ) :
            
            if name in scope :
                
                return scope [ name ]
                
        return None
        
    # Main check dispatcher method
    def check ( self , node : ast.ASTNode ) -> str :
        
        method_name = f"check_{ node.__class__.__name__ }"
        visitor = getattr ( self , method_name , self.generic_check )
        
        return visitor ( node )
        
    # Fallback check method
    def generic_check ( self , node : ast.ASTNode ) -> str :
        
        return 'void'
        
    # Program check method
    def check_Program ( self , node : ast.Program ) -> str :
        
        # First pass: collect all function declarations globally so functions can call each other
        for decl in node.declarations :
            
            if isinstance ( decl , ast.FunctionDeclaration ) :
                
                if decl.name in self.functions :
                    
                    raise DuplicateSpirit ( f"Vaatu Corruption — Duplicate Spirit: Function '{ decl.name }' already declared." )
                    
                self.functions [ decl.name ] = {
                    'params' : decl.parameters ,
                    'return_type' : decl.return_type
                }
                
        # Second pass: check all statements and declarations in order
        for decl in node.declarations :
            
            self.check ( decl )
            
        # Global scope exit check
        self.exit_scope ( )
        
        return 'void'
        
    # Function declaration check method
    def check_FunctionDeclaration ( self , node : ast.FunctionDeclaration ) -> str :
        
        self.enter_scope ( )
        
        # Declare all parameters in the new local scope
        for param in node.parameters :
            
            self.declare ( param.name , param.type_annotation )
            
        # Set target return type for return statement validation
        old_return_type = self.current_return_type
        self.current_return_type = node.return_type
        
        # Check function body statements
        for stmt in node.body.statements :
            
            self.check ( stmt )
            
        self.exit_scope ( )
        self.current_return_type = old_return_type
        
        return 'void'
        
    # Let statement check method
    def check_LetStatement ( self , node : ast.LetStatement ) -> str :
        
        val_type = self.check ( node.value )
        
        # Type validation (supporting implicit promotion from int to float)
        if node.type_annotation == 'float' and val_type == 'int' :
            
            pass
            
        elif node.type_annotation != val_type :
            
            raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Cannot assign '{ val_type }' to variable of type '{ node.type_annotation }'." )
            
        self.declare ( node.name , node.type_annotation )
        
        return 'void'
        
    # Assignment statement check method
    def check_AssignStatement ( self , node : ast.AssignStatement ) -> str :
        
        var_info = self.lookup ( node.name )
        
        if var_info is None :
            
            raise UndeclaredSpirit ( f"Vaatu Corruption — Undeclared Spirit: Variable '{ node.name }' is not defined." )
            
        if var_info [ 'type' ] == 'Element' and var_info [ 'consumed' ] :
            
            raise UseAfterConsume ( f"Vaatu Corruption — Use After Consume: Element '{ node.name }' has already been consumed." )
            
        val_type = self.check ( node.value )
        
        if var_info [ 'type' ] == 'float' and val_type == 'int' :
            
            pass
            
        elif var_info [ 'type' ] != val_type :
            
            raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Cannot assign '{ val_type }' to variable '{ node.name }' of type '{ var_info [ 'type' ] }'." )
            
        return 'void'
        
    # If statement check method
    def check_IfStatement ( self , node : ast.IfStatement ) -> str :
        
        cond_type = self.check ( node.condition )
        
        if cond_type != 'bool' :
            
            raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: If condition must be 'bool', got '{ cond_type }'." )
            
        self.enter_scope ( )
        self.check ( node.then_body )
        self.exit_scope ( )
        
        if node.else_body is not None :
            
            self.enter_scope ( )
            self.check ( node.else_body )
            self.exit_scope ( )
            
        return 'void'
        
    # While statement check method
    def check_WhileStatement ( self , node : ast.WhileStatement ) -> str :
        
        cond_type = self.check ( node.condition )
        
        if cond_type != 'bool' :
            
            raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: While condition must be 'bool', got '{ cond_type }'." )
            
        self.enter_scope ( )
        self.check ( node.body )
        self.exit_scope ( )
        
        return 'void'
        
    # Block statement check method
    def check_BlockStatement ( self , node : ast.BlockStatement ) -> str :
        
        for stmt in node.statements :
            
            self.check ( stmt )
            
        return 'void'
        
    # Expression statement check method
    def check_ExpressionStatement ( self , node : ast.ExpressionStatement ) -> str :
        
        self.check ( node.expression )
        
        return 'void'
        
    # Print statement check method
    def check_PrintStatement ( self , node : ast.PrintStatement ) -> str :
        
        self.check ( node.value )
        
        return 'void'
        
    # Return statement check method
    def check_ReturnStatement ( self , node : ast.ReturnStatement ) -> str :
        
        ret_type = 'void'
        
        if node.value is not None :
            
            ret_type = self.check ( node.value )
            
        # Validate against function's declared return type
        if self.current_return_type is None :
            
            raise TypeMismatch ( "Vaatu Corruption — Type Mismatch: Return statement outside function." )
            
        if self.current_return_type == 'float' and ret_type == 'int' :
            
            pass
            
        elif ret_type != self.current_return_type :
            
            raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Function declared return type '{ self.current_return_type }' but returned '{ ret_type }'." )
            
        return 'void'
        
    # Spawn action check method
    def check_SpawnAction ( self , node : ast.SpawnAction ) -> str :
        
        x_type = self.check ( node.x )
        y_type = self.check ( node.y )
        
        if x_type != 'int' or y_type != 'int' :
            
            raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Spawn coordinates must be 'int', got '{ x_type }' and '{ y_type }'." )
            
        return 'void'
        
    # Move action check method
    def check_MoveAction ( self , node : ast.MoveAction ) -> str :
        
        return 'void'
        
    # Stance action check method
    def check_StanceAction ( self , node : ast.StanceAction ) -> str :
        
        return 'void'
        
    # Strike action check method
    def check_StrikeAction ( self , node : ast.StrikeAction ) -> str :
        
        elem_type = self.check ( node.element )
        
        if elem_type != 'Element' :
            
            raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Strike expects 'Element', got '{ elem_type }'." )
            
        # Mark element variable as consumed
        if isinstance ( node.element , ast.Identifier ) :
            
            var_info = self.lookup ( node.element.name )
            
            if var_info is not None :
                
                if var_info [ 'consumed' ] :
                    
                    raise UseAfterConsume ( f"Vaatu Corruption — Use After Consume: Element '{ node.element.name }' has already been consumed." )
                    
                var_info [ 'consumed' ] = True
                
        return 'void'
        
    # Block action check method
    def check_BlockAction ( self , node : ast.BlockAction ) -> str :
        
        return 'void'
        
    # Int literal check method
    def check_IntLiteral ( self , node : ast.IntLiteral ) -> str :
        
        return 'int'
        
    # Float literal check method
    def check_FloatLiteral ( self , node : ast.FloatLiteral ) -> str :
        
        return 'float'
        
    # Boolean literal check method
    def check_BooleanLiteral ( self , node : ast.BooleanLiteral ) -> str :
        
        return 'bool'
        
    # String literal check method
    def check_StringLiteral ( self , node : ast.StringLiteral ) -> str :
        
        return 'string'
        
    # Element literal check method
    def check_ElementLiteral ( self , node : ast.ElementLiteral ) -> str :
        
        return 'Element'
        
    # Stance literal check method
    def check_StanceLiteral ( self , node : ast.StanceLiteral ) -> str :
        
        return 'Stance'
        
    # Identifier check method
    def check_Identifier ( self , node : ast.Identifier ) -> str :
        
        var_info = self.lookup ( node.name )
        
        if var_info is None :
            
            raise UndeclaredSpirit ( f"Vaatu Corruption — Undeclared Spirit: '{ node.name }' is not defined." )
            
        if var_info [ 'type' ] == 'Element' and var_info [ 'consumed' ] :
            
            raise UseAfterConsume ( f"Vaatu Corruption — Use After Consume: Element '{ node.name }' has already been consumed." )
            
        return var_info [ 'type' ]
        
    # Binary operation check method
    def check_BinaryOperation ( self , node : ast.BinaryOperation ) -> str :
        
        lt = self.check ( node.left )
        rt = self.check ( node.right )
        
        # Arithmetic operators
        if node.operator in [ '+' , '-' , '*' , '/' ] :
            
            if lt == 'int' and rt == 'int' :
                
                return 'int'
                
            elif lt == 'float' and rt == 'float' :
                
                return 'float'
                
            elif ( lt == 'int' and rt == 'float' ) or ( lt == 'float' and rt == 'int' ) :
                
                return 'float'  # Implicit coercion
                
            elif node.operator == '+' and lt == 'string' and rt == 'string' :
                
                return 'string'  # String concatenation
                
            else :
                
                raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Cannot apply '{ node.operator }' to '{ lt }' and '{ rt }'." )
                
        # Comparison operators
        elif node.operator in [ '<' , '>' , '<=' , '>=' ] :
            
            if ( lt == 'int' or lt == 'float' ) and ( rt == 'int' or rt == 'float' ) :
                
                return 'bool'
                
            else :
                
                raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Cannot apply '{ node.operator }' to '{ lt }' and '{ rt }'." )
                
        # Equality operators
        elif node.operator in [ '==' , '!=' ] :
            
            if lt == rt :
                
                return 'bool'
                
            elif ( lt == 'int' or lt == 'float' ) and ( rt == 'int' or rt == 'float' ) :
                
                return 'bool'  # Allow comparing int and float
                
            else :
                
                raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Cannot compare '{ lt }' and '{ rt }'." )
                
        # Logical operators
        elif node.operator in [ 'and' , 'or' ] :
            
            if lt == 'bool' and rt == 'bool' :
                
                return 'bool'
                
            else :
                
                raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Logical '{ node.operator }' expects booleans, got '{ lt }' and '{ rt }'." )
                
        raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Unknown operator '{ node.operator }'." )
        
    # Unary operation check method
    def check_UnaryOperation ( self , node : ast.UnaryOperation ) -> str :
        
        rt = self.check ( node.right )
        
        if node.operator == '-' :
            
            if rt in [ 'int' , 'float' ] :
                
                return rt
                
            else :
                
                raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Unary '-' expects numeric type, got '{ rt }'." )
                
        elif node.operator == 'not' :
            
            if rt == 'bool' :
                
                return 'bool'
                
            else :
                
                raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Unary 'not' expects 'bool', got '{ rt }'." )
                
        raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Unknown unary operator '{ node.operator }'." )
        
    # Function call check method
    def check_FunctionCall ( self , node : ast.FunctionCall ) -> str :
        
        if node.name not in self.functions :
            
            raise UndeclaredSpirit ( f"Vaatu Corruption — Undeclared Spirit: Function '{ node.name }' is not defined." )
            
        func = self.functions [ node.name ]
        
        if len ( node.arguments ) != len ( func [ 'params' ] ) :
            
            raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Function '{ node.name }' expects { len ( func [ 'params' ] ) } arguments, got { len ( node.arguments ) }." )
            
        for i , arg in enumerate ( node.arguments ) :
            
            arg_type = self.check ( arg )
            param = func [ 'params' ] [ i ]
            
            if param.type_annotation == 'float' and arg_type == 'int' :
                
                pass
                
            elif arg_type != param.type_annotation :
                
                raise TypeMismatch ( f"Vaatu Corruption — Type Mismatch: Argument { i + 1 } of function '{ node.name }' must be '{ param.type_annotation }', got '{ arg_type }'." )
                
        return func [ 'return_type' ]
