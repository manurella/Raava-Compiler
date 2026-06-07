
# Imports
from raava.tokens import TokenType , Token

# Keyword dictionary 
KEYWORDS = {
    
    'let' : TokenType.LET,
    'fn' : TokenType.FN,
    
    'if' : TokenType.IF,
    'else' : TokenType.ELSE,
    'while' : TokenType.WHILE,
    
    'return' : TokenType.RETURN,
    'print' : TokenType.PRINT,
    
    'int' : TokenType.INT_TYPE,
    'float' : TokenType.FLOAT_TYPE,
    'bool' : TokenType.BOOLEAN_TYPE,
    'string' : TokenType.STRING_TYPE,
    
    'Element' : TokenType.ELEMENT_TYPE,
    'Stance' : TokenType.STANCE_TYPE,
    
    'true' : TokenType.TRUE,
    'false' : TokenType.FALSE,
    
    'Water' : TokenType.WATER,
    'Earth' : TokenType.EARTH,
    'Fire' : TokenType.FIRE,
    'Air' : TokenType.AIR,
    
    'NeutralStance' : TokenType.NEUTRALSTANCE,
    'OffensiveStance' : TokenType.OFFENSIVESTANCE,
    'DefensiveStance' : TokenType.DEFENSIVESTANCE,
    
    'spawn' : TokenType.SPAWN,
    'move' : TokenType.MOVE,
    'stance' : TokenType.STANCE,
    'strike' : TokenType.STRIKE,
    'block' : TokenType.BLOCK,
    
    'Up' : TokenType.UP,
    'Down' : TokenType.DOWN,
    'Left' : TokenType.LEFT,
    'Right' : TokenType.RIGHT,
    
    'and' : TokenType.AND,
    'or' : TokenType.OR,
    'not' : TokenType.NOT,
    
}

# Lexer class
class Lexer:
    
    # Lexer constructor method
    def __init__ ( self , source : str ) :
        
        self.source = source
        self.position = 0 # Current Index
        self.read_position = 0 # Next Index
        self.chr = '' # Current Character
        self.line = 1 # Current Line
        self.column = 1 # Current Column
      
        # Read the first character to initialize the current character  
        self.read_chr ( )
        
    # Character read method
    def read_chr ( self ) :
        
        # Update the line and column based on the current character
        if self.chr == '\n' :
            self.line += 1
            self.column = 1 # Reset
        elif self.chr != '' :
            self.column += 1
            
        # Read the next character
        if self.read_position >= len ( self.source ) :
            self.chr = None 
        else :
            self.chr = self.source [ self.read_position ]

        # Advance pointers
        self.position = self.read_position
        self.read_position += 1
        
    # Character peak method
    def peek_chr ( self ) :
        
        if self.read_position >= len ( self.source ) :
            return None
        return self.source [ self.read_position ]
    
    # Whitespace skip method
    def skip_whitespace ( self ) :
        
        while self.chr in [ ' ' , '\t' , '\n' , '\r' ] :
            self.read_chr ( )
            
    # Comment skip method
    def skip_comment ( self ) :
        
        while self.chr != '\n' and self.chr is not None :
            self.read_chr ( )
            
    # Identifier read method
    def read_identifier ( self ) -> str :
        
        start_position = self.position
        
        while ( self.chr is not None ) and ( ( self.chr.isalnum ( ) ) or ( self.chr == '_' ) ) :
            self.read_chr ( )
            
        return self.source [ start_position : self.position ]
    
    # Number read method
    def read_number ( self ) :
        
        start_position = self.position
        is_float = False
        
        while ( self.chr is not None ) and ( ( self.chr.isdigit ( ) ) or ( self.chr == '.' ) ) :
            
            if self.chr == '.' :
                
                if is_float :
                    break
                is_float = True
                
            self.read_chr ( )
            
        value = self.source [ start_position : self.position ]
        token_type = TokenType.FLOAT_LITERAL if is_float else TokenType.INT_LITERAL
        
        return token_type , value 
    
    # String read method
    def read_string ( self ) :
        
        self.read_chr ( )
        start_position = self.position
        
        while ( self.chr is not None ) and ( self.chr != '"' ) :
            self.read_chr ( )
            
        if self.chr is None :
            raise Exception ( f"Vaatu Corruption - Unterminated string literal at line { self.line }" )
        
        value = self.source [ start_position : self.position ]
        
        self.read_chr ( )
        return value
    
    # Tokenize method
    def tokenize ( self ) -> list [ Token ] :
        
        tokens = []
        
        while self.chr is not None :
            
            # Skip whitespace
            self.skip_whitespace ( )
            
            if self.chr is None :
                break
            
            # Skip comments
            if ( self.chr == '/' ) and ( self.peek_chr ( ) == '/' ):
                self.skip_comment ( )
                continue
            
            token_line = self.line
            token_column = self.column
            
            if self.chr == '+' :
                tokens.append ( Token ( TokenType.PLUS , '+' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == '-' :
                if self.peek_chr ( ) == '>' :
                    self.read_chr ( )
                    self.read_chr ( )
                    tokens.append ( Token ( TokenType.ARROW , '->' , token_line , token_column ) )
                else :
                    tokens.append ( Token ( TokenType.MINUS , '-' , token_line , token_column ) )
                    self.read_chr ( )
            elif self.chr == '*' :
                tokens.append ( Token ( TokenType.STAR , '*' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == '/' :
                tokens.append ( Token ( TokenType.SLASH , '/' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == '=' :
                if self.peek_chr ( ) == '=' :
                    self.read_chr ( )
                    self.read_chr ( )
                    tokens.append ( Token ( TokenType.EQ_EQ , '==' , token_line , token_column ) )
                else : 
                    tokens.append ( Token ( TokenType.EQUALS , '=' , token_line , token_column ) )
                    self.read_chr ( )
            elif self.chr == '!' :
                if self.peek_chr ( ) == '=' :
                    self.read_chr ( )
                    self.read_chr ( )
                    tokens.append ( Token ( TokenType.BANG_EQ , '!=' , token_line , token_column ) )
                else :
                    raise Exception ( f"Vaatu Corruption - Unexpected character '!' at line { self.line }, column { self.column }. Did you mean '!-' ?" )
            elif self.chr == '<' :
                if self.peek_chr ( ) == '=' :
                    self.read_chr ( )
                    self.read_chr ( )
                    tokens.append ( Token ( TokenType.LESS_THAN_EQ , '<=' , token_line , token_column ) )
                else :
                    tokens.append ( Token ( TokenType.LESS_THAN , '<' , token_line , token_column ) )
                    self.read_chr ( )
            elif self.chr == '>' :
                if self.peek_chr ( ) == '=' :
                    self.read_chr ( )
                    self.read_chr ( )
                    tokens.append ( Token ( TokenType.GREATER_THAN_EQ , '>=' , token_line , token_column ) )
                else : 
                    tokens.append ( Token ( TokenType.GREATER_THAN , '>' , token_line , token_column ) )
                    self.read_chr ( )
            elif self.chr == ':' :
                tokens.append ( Token ( TokenType.COLON , ':' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == ';' :
                tokens.append ( Token ( TokenType.SEMICOLON , ';' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == ',' :
                tokens.append ( Token ( TokenType.COMMA , ',' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == '(' :
                tokens.append ( Token ( TokenType.LEFT_PAREN , '(' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == ')' :
                tokens.append ( Token ( TokenType.RIGHT_PAREN , ')' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == '{' :
                tokens.append ( Token ( TokenType.LEFT_BRACE , '{' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == '}' :
                tokens.append ( Token ( TokenType.RIGHT_BRACE , '}' , token_line , token_column ) )
                self.read_chr ( )
            elif self.chr == '"' :
                value = self.read_string ( )
                tokens.append ( Token ( TokenType.STRING_LITERAL , value , token_line , token_column ) )
            elif ( self.chr.isalpha ( ) ) or ( self.chr == '_' ) :
                word = self.read_identifier ( )
                token_type = KEYWORDS.get ( word , TokenType.IDENTIFIER )
                tokens.append ( Token ( token_type , word , token_line , token_column ) )
            elif self.chr.isdigit ( ) :
                token_type , value = self.read_number ( )
                tokens.append ( Token ( token_type , value , token_line , token_column ) )
                
            else : 
                raise Exception ( f"Vaatu Corruption - Invalid character '{ self.chr }' at line { self.line }, column { self.column }" )
            
        tokens.append ( Token ( TokenType.EOF , '' , self.line , self.column ) )
        return tokens
    

                