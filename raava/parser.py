# Imports
from typing import List, Optional, NoReturn
from raava.tokens import TokenType, Token
from raava import ast_nodes as ast

# Parser class
class Parser:
    
    # Parser constructor method
    def __init__ ( self , tokens : List [ Token ] ) :
        
        self.tokens = tokens
        self.current_index = 0
        
    # Current token property
    @property
    def current_token ( self ) -> Token :
        
        if self.current_index >= len ( self.tokens ) :
            
            return Token ( TokenType.EOF , '' , 1 , 1 )
        
        return self.tokens [ self.current_index ]
    
    # Peek token property
    @property
    def peek_token ( self ) -> Token :
        
        if ( self.current_index + 1 ) >= ( len ( self.tokens ) ) :
            
            return Token ( TokenType.EOF , '' , self.line , self.column )
        
        return self.tokens [ self.current_index + 1 ]
    
    # Current line property
    @property
    def line ( self ) -> int :
        
        return self.current_token.line
    
    # Current column property
    @property 
    def column ( self ) -> int :
        
        return self.current_token.column
    
    # At end check method
    def is_at_end ( self ) -> bool :
        
        return self.current_token.type == TokenType.EOF
    
    # Token advance method
    def advance ( self ) -> Token :
        
        if not self.is_at_end ( ) :
            
            self.current_index += 1
            
        return self.tokens [ self.current_index - 1 ]
    
    # Token match to a given type check method
    def check ( self , token_type : TokenType ) -> bool :
        
        if self.is_at_end ( ) :
            
            return False
        
        return self.current_token.type == token_type
    
    # Token match to any type check, and advancement method
    def match ( self , *token_types : TokenType ) -> bool :
        
        for token_type in token_types :
            
            if self.check ( token_type ) :
                
                self.advance ( )
                
                return True
            
        return False
    
    # Consume method
    def consume ( self , token_type : TokenType , message : str ) -> Token :
        
        if self.check ( token_type ) :
            
            return self.advance ( )
        
        self.error ( message )
    
    # Error method
    def error ( self , message : str ) -> NoReturn:
        
        raise Exception (
            
            f"🔥 Vaatu Corruption — SyntaxCorruption at line { self.line } , column { self.column }\n"
            f"   Detail : { message }"
        
        )
    
    # Parse entry method
    def parse ( self ) -> ast.Program :
        
        declarations = [ ]
        
        while not self.is_at_end ( ) :
            
            declarations.append ( self.parse_declaration ( ) )
            
        return ast.Program ( declarations )
    
    # Declaration parsing method
    def parse_declaration ( self ) -> ast.ASTNode :
        
        if self.check ( TokenType.FN ) :
            
            return self.parse_function_declaration ( )
            
        return self.parse_statement ( )
    
    # Statement parsing method
    def parse_statement ( self ) -> ast.ASTNode :
        
        if self.match ( TokenType.LET ) :
            
            return self.parse_let_statement ( )
            
        elif self.match ( TokenType.IF ) :
            
            return self.parse_if_statement ( )
            
        elif self.match ( TokenType.WHILE ) :
            
            return self.parse_while_statement ( )
            
        elif self.match ( TokenType.RETURN ) :
            
            return self.parse_return_statement ( )
            
        elif self.match ( TokenType.PRINT ) :
            
            return self.parse_print_statement ( )
            
        elif self.check ( TokenType.LEFT_BRACE ) :
            
            return self.parse_block_statement ( )
            
        elif self.check ( TokenType.SPAWN ) or self.check ( TokenType.MOVE ) or \
             self.check ( TokenType.STANCE ) or self.check ( TokenType.STRIKE ) or \
             self.check ( TokenType.BLOCK ) :
             
            return self.parse_action_statement ( )
            
        return self.parse_expression_or_assignment_statement ( )
    
    # Let statement parsing method
    def parse_let_statement ( self ) -> ast.LetStatement :
        
        name_token = self.consume ( TokenType.IDENTIFIER , "Expect variable name after 'let'." )
        name = name_token.value
        
        self.consume ( TokenType.COLON , "Expect ':' after variable name." )
        
        if not ( self.check ( TokenType.INT_TYPE ) or self.check ( TokenType.FLOAT_TYPE ) or \
                self.check ( TokenType.BOOLEAN_TYPE ) or self.check ( TokenType.STRING_TYPE ) or \
                self.check ( TokenType.ELEMENT_TYPE ) or self.check ( TokenType.STANCE_TYPE ) ) :
                
            self.error ( "Expect type annotation (int, float, bool, string, Element, or Stance) after ':'." )
            
        type_token = self.advance ( )
        
        type_mapping = {
            TokenType.INT_TYPE : 'int' ,
            TokenType.FLOAT_TYPE : 'float' ,
            TokenType.BOOLEAN_TYPE : 'bool' ,
            TokenType.STRING_TYPE : 'string' ,
            TokenType.ELEMENT_TYPE : 'Element' ,
            TokenType.STANCE_TYPE : 'Stance' ,
        }
        type_annotation = type_mapping [ type_token.type ]
        
        self.consume ( TokenType.EQUALS , "Expect '=' after type annotation." )
        
        value = self.parse_expression ( )
        
        self.consume ( TokenType.SEMICOLON , "Expect ';' at the end of let statement." )
        
        return ast.LetStatement ( name = name , type_annotation = type_annotation , value = value )
    
    # Print statement parsing method
    def parse_print_statement ( self ) -> ast.PrintStatement :
        
        value = self.parse_expression ( )
        
        self.consume ( TokenType.SEMICOLON , "Expect ';' after print statement." )
        
        return ast.PrintStatement ( value = value )
    
    # Return statement parsing method
    def parse_return_statement ( self ) -> ast.ReturnStatement :
        
        value = None
        
        if not self.check ( TokenType.SEMICOLON ) :
            
            value = self.parse_expression ( )
            
        self.consume ( TokenType.SEMICOLON , "Expect ';' after return statement." )
        
        return ast.ReturnStatement ( value = value )
    
    # If statement parsing method
    def parse_if_statement ( self ) -> ast.IfStatement :
        
        self.consume ( TokenType.LEFT_PAREN , "Expect '(' after 'if'." )
        
        condition = self.parse_expression ( )
        
        self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after if condition." )
        
        then_body = self.parse_block_statement ( )
        
        else_body = None
        
        if self.match ( TokenType.ELSE ) :
            
            else_body = self.parse_block_statement ( )
            
        return ast.IfStatement ( condition = condition , then_body = then_body , else_body = else_body )
    
    # While statement parsing method
    def parse_while_statement ( self ) -> ast.WhileStatement :
        
        self.consume ( TokenType.LEFT_PAREN , "Expect '(' after 'while'." )
        
        condition = self.parse_expression ( )
        
        self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after while condition." )
        
        body = self.parse_block_statement ( )
        
        return ast.WhileStatement ( condition = condition , body = body )
    
    # Block statement parsing method
    def parse_block_statement ( self ) -> ast.BlockStatement :
        
        self.consume ( TokenType.LEFT_BRACE , "Expect '{' to start a block." )
        
        statements = [ ]
        
        while not self.check ( TokenType.RIGHT_BRACE ) and not self.is_at_end ( ) :
            
            statements.append ( self.parse_statement ( ) )
            
        self.consume ( TokenType.RIGHT_BRACE , "Expect '}' to close a block." )
        
        return ast.BlockStatement ( statements = statements )
    
    # Action statement parsing method
    def parse_action_statement ( self ) -> ast.ASTNode :
        
        if self.match ( TokenType.SPAWN ) :
            
            self.consume ( TokenType.LEFT_PAREN , "Expect '(' after 'spawn'." )
            
            x = self.parse_expression ( )
            
            self.consume ( TokenType.COMMA , "Expect ',' between spawn coordinates." )
            
            y = self.parse_expression ( )
            
            self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after spawn coordinates." )
            
            self.consume ( TokenType.SEMICOLON , "Expect ';' after spawn action." )
            
            return ast.SpawnAction ( x = x , y = y )
            
        elif self.match ( TokenType.MOVE ) :
            
            self.consume ( TokenType.LEFT_PAREN , "Expect '(' after 'move'." )
            
            if not ( self.check ( TokenType.UP ) or self.check ( TokenType.DOWN ) or \
                    self.check ( TokenType.LEFT ) or self.check ( TokenType.RIGHT ) ) :
                    
                self.error ( "Expect direction (Up, Down, Left, or Right) after 'move('." )
                
            dir_token = self.advance ( )
            direction = dir_token.value
            
            self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after move direction." )
            
            self.consume ( TokenType.SEMICOLON , "Expect ';' after move action." )
            
            return ast.MoveAction ( direction = direction )
            
        elif self.match ( TokenType.STANCE ) :
            
            self.consume ( TokenType.LEFT_PAREN , "Expect '(' after 'stance'." )
            
            if not ( self.check ( TokenType.NEUTRALSTANCE ) or self.check ( TokenType.OFFENSIVESTANCE ) or \
                    self.check ( TokenType.DEFENSIVESTANCE ) ) :
                    
                self.error ( "Expect stance state (NeutralStance, OffensiveStance, DefensiveStance) after 'stance('." )
                
            stance_token = self.advance ( )
            stance = stance_token.value
            
            self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after stance state." )
            
            self.consume ( TokenType.SEMICOLON , "Expect ';' after stance action." )
            
            return ast.StanceAction ( stance = stance )
            
        elif self.match ( TokenType.STRIKE ) :
            
            self.consume ( TokenType.LEFT_PAREN , "Expect '(' after 'strike'." )
            
            element = self.parse_expression ( )
            
            self.consume ( TokenType.COMMA , "Expect ',' between element and direction." )
            
            if not ( self.check ( TokenType.UP ) or self.check ( TokenType.DOWN ) or \
                    self.check ( TokenType.LEFT ) or self.check ( TokenType.RIGHT ) ) :
                    
                self.error ( "Expect direction (Up, Down, Left, or Right) after comma." )
                
            dir_token = self.advance ( )
            direction = dir_token.value
            
            self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after strike direction." )
            
            self.consume ( TokenType.SEMICOLON , "Expect ';' after strike action." )
            
            return ast.StrikeAction ( element = element , direction = direction )
            
        elif self.match ( TokenType.BLOCK ) :
            
            self.consume ( TokenType.LEFT_PAREN , "Expect '(' after 'block'." )
            
            self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after 'block('." )
            
            self.consume ( TokenType.SEMICOLON , "Expect ';' after block action." )
            
            return ast.BlockAction ( )
            
        self.error ( "Invalid action statement." )
        
    # Expression or assignment parsing method
    def parse_expression_or_assignment_statement ( self ) -> ast.ASTNode :
        
        if self.check ( TokenType.IDENTIFIER ) and self.peek_token.type == TokenType.EQUALS :
            
            name_token = self.advance ( )
            name = name_token.value
            
            self.consume ( TokenType.EQUALS , "Expect '=' after variable name." )
            
            value = self.parse_expression ( )
            
            self.consume ( TokenType.SEMICOLON , "Expect ';' at the end of assignment." )
            
            return ast.AssignStatement ( name = name , value = value )
            
        expr = self.parse_expression ( )
        
        self.consume ( TokenType.SEMICOLON , "Expect ';' after expression." )
        
        return ast.ExpressionStatement ( expression = expr )
        
    # Expression parsing entry method
    def parse_expression ( self ) -> ast.ASTNode :
        
        return self.parse_or ( )
        
    # Logical OR parsing method
    def parse_or ( self ) -> ast.ASTNode :
        
        expr = self.parse_and ( )
        
        while self.match ( TokenType.OR ) :
            
            right = self.parse_and ( )
            
            expr = ast.BinaryOperation ( left = expr , operator = 'or' , right = right )
            
        return expr
        
    # Logical AND parsing method
    def parse_and ( self ) -> ast.ASTNode :
        
        expr = self.parse_equality ( )
        
        while self.match ( TokenType.AND ) :
            
            right = self.parse_equality ( )
            
            expr = ast.BinaryOperation ( left = expr , operator = 'and' , right = right )
            
        return expr
        
    # Equality operators parsing method
    def parse_equality ( self ) -> ast.ASTNode :
        
        expr = self.parse_comparison ( )
        
        while self.match ( TokenType.EQ_EQ , TokenType.BANG_EQ ) :
            
            operator_token = self.tokens [ self.current_index - 1 ]
            
            operator = '==' if operator_token.type == TokenType.EQ_EQ else '!='
            
            right = self.parse_comparison ( )
            
            expr = ast.BinaryOperation ( left = expr , operator = operator , right = right )
            
        return expr
        
    # Comparison operators parsing method
    def parse_comparison ( self ) -> ast.ASTNode :
        
        expr = self.parse_additive ( )
        
        while self.match ( TokenType.LESS_THAN , TokenType.GREATER_THAN , \
                           TokenType.LESS_THAN_EQ , TokenType.GREATER_THAN_EQ ) :
                           
            operator_token = self.tokens [ self.current_index - 1 ]
            
            operator_map = {
                TokenType.LESS_THAN : '<' ,
                TokenType.GREATER_THAN : '>' ,
                TokenType.LESS_THAN_EQ : '<=' ,
                TokenType.GREATER_THAN_EQ : '>=' ,
            }
            operator = operator_map [ operator_token.type ]
            
            right = self.parse_additive ( )
            
            expr = ast.BinaryOperation ( left = expr , operator = operator , right = right )
            
        return expr
        
    # Additive operators parsing method
    def parse_additive ( self ) -> ast.ASTNode :
        
        expr = self.parse_multiplicative ( )
        
        while self.match ( TokenType.PLUS , TokenType.MINUS ) :
            
            operator_token = self.tokens [ self.current_index - 1 ]
            
            operator = '+' if operator_token.type == TokenType.PLUS else '-'
            
            right = self.parse_multiplicative ( )
            
            expr = ast.BinaryOperation ( left = expr , operator = operator , right = right )
            
        return expr
        
    # Multiplicative operators parsing method
    def parse_multiplicative ( self ) -> ast.ASTNode :
        
        expr = self.parse_unary ( )
        
        while self.match ( TokenType.STAR , TokenType.SLASH ) :
            
            operator_token = self.tokens [ self.current_index - 1 ]
            
            operator = '*' if operator_token.type == TokenType.STAR else '/'
            
            right = self.parse_unary ( )
            
            expr = ast.BinaryOperation ( left = expr , operator = operator , right = right )
            
        return expr
        
    # Unary operators parsing method
    def parse_unary ( self ) -> ast.ASTNode :
        
        if self.match ( TokenType.MINUS , TokenType.NOT ) :
            
            operator_token = self.tokens [ self.current_index - 1 ]
            
            operator = '-' if operator_token.type == TokenType.MINUS else 'not'
            
            right = self.parse_unary ( )
            
            return ast.UnaryOperation ( operator = operator , right = right )
            
        return self.parse_primary ( )
        
    # Primary expression parsing method
    def parse_primary ( self ) -> ast.ASTNode :
        
        if self.match ( TokenType.INT_LITERAL ) :
            
            return ast.IntLiteral ( value = int ( self.tokens [ self.current_index - 1 ].value ) )
            
        elif self.match ( TokenType.FLOAT_LITERAL ) :
            
            return ast.FloatLiteral ( value = float ( self.tokens [ self.current_index - 1 ].value ) )
            
        elif self.match ( TokenType.STRING_LITERAL ) :
            
            return ast.StringLiteral ( value = self.tokens [ self.current_index - 1 ].value )
            
        elif self.match ( TokenType.TRUE ) :
            
            return ast.BooleanLiteral ( value = True )
            
        elif self.match ( TokenType.FALSE ) :
            
            return ast.BooleanLiteral ( value = False )
            
        elif self.match ( TokenType.WATER , TokenType.EARTH , TokenType.FIRE , TokenType.AIR ) :
            
            return ast.ElementLiteral ( value = self.tokens [ self.current_index - 1 ].value )
            
        elif self.match ( TokenType.NEUTRALSTANCE , TokenType.OFFENSIVESTANCE , TokenType.DEFENSIVESTANCE ) :
            
            return ast.StanceLiteral ( value = self.tokens [ self.current_index - 1 ].value )
            
        elif self.match ( TokenType.IDENTIFIER ) :
            
            name = self.tokens [ self.current_index - 1 ].value
            
            if self.match ( TokenType.LEFT_PAREN ) :
                
                arguments = [ ]
                
                if not self.check ( TokenType.RIGHT_PAREN ) :
                    
                    arguments.append ( self.parse_expression ( ) )
                    
                    while self.match ( TokenType.COMMA ) :
                        
                        arguments.append ( self.parse_expression ( ) )
                        
                self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after arguments." )
                
                return ast.FunctionCall ( name = name , arguments = arguments )
                
            return ast.Identifier ( name = name )
            
        elif self.match ( TokenType.LEFT_PAREN ) :
            
            expr = self.parse_expression ( )
            
            self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after grouping expression." )
            
            return expr
            
        self.error ( f"Expect expression, got '{ self.current_token.value }'" )
        
    # Function parameter parsing method
    def parse_parameter ( self ) -> ast.FunctionParameter :
        
        name_token = self.consume ( TokenType.IDENTIFIER , "Expect parameter name." )
        name = name_token.value
        
        self.consume ( TokenType.COLON , "Expect ':' after parameter name." )
        
        if not ( self.check ( TokenType.INT_TYPE ) or self.check ( TokenType.FLOAT_TYPE ) or \
                self.check ( TokenType.BOOLEAN_TYPE ) or self.check ( TokenType.STRING_TYPE ) or \
                self.check ( TokenType.ELEMENT_TYPE ) or self.check ( TokenType.STANCE_TYPE ) ) :
                
            self.error ( "Expect parameter type annotation (int, float, bool, string, Element, or Stance)." )
            
        type_token = self.advance ( )
        
        type_mapping = {
            TokenType.INT_TYPE : 'int' ,
            TokenType.FLOAT_TYPE : 'float' ,
            TokenType.BOOLEAN_TYPE : 'bool' ,
            TokenType.STRING_TYPE : 'string' ,
            TokenType.ELEMENT_TYPE : 'Element' ,
            TokenType.STANCE_TYPE : 'Stance' ,
        }
        type_annotation = type_mapping [ type_token.type ]
        
        return ast.FunctionParameter ( name = name , type_annotation = type_annotation )
        
    # Function declaration parsing method
    def parse_function_declaration ( self ) -> ast.FunctionDeclaration :
        
        self.consume ( TokenType.FN , "Expect 'fn' to start function declaration." )
        
        name_token = self.consume ( TokenType.IDENTIFIER , "Expect function name." )
        name = name_token.value
        
        self.consume ( TokenType.LEFT_PAREN , "Expect '(' after function name." )
        
        parameters = [ ]
        
        if not self.check ( TokenType.RIGHT_PAREN ) :
            
            parameters.append ( self.parse_parameter ( ) )
            
            while self.match ( TokenType.COMMA ) :
                
                parameters.append ( self.parse_parameter ( ) )
                
        self.consume ( TokenType.RIGHT_PAREN , "Expect ')' after parameter list." )
        
        self.consume ( TokenType.ARROW , "Expect '->' before return type." )
        
        if not ( self.check ( TokenType.INT_TYPE ) or self.check ( TokenType.FLOAT_TYPE ) or \
                self.check ( TokenType.BOOLEAN_TYPE ) or self.check ( TokenType.STRING_TYPE ) or \
                self.check ( TokenType.ELEMENT_TYPE ) or self.check ( TokenType.STANCE_TYPE ) ) :
                
            self.error ( "Expect return type annotation (int, float, bool, string, Element, or Stance)." )
            
        type_token = self.advance ( )
        
        type_mapping = {
            TokenType.INT_TYPE : 'int' ,
            TokenType.FLOAT_TYPE : 'float' ,
            TokenType.BOOLEAN_TYPE : 'bool' ,
            TokenType.STRING_TYPE : 'string' ,
            TokenType.ELEMENT_TYPE : 'Element' ,
            TokenType.STANCE_TYPE : 'Stance' ,
        }
        return_type = type_mapping [ type_token.type ]
        
        body = self.parse_block_statement ( )
        
        return ast.FunctionDeclaration ( name = name , parameters = parameters , return_type = return_type , body = body )