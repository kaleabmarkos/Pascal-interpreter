INTEGER, PLUS, EOF, SUB, MUL, DIV, LBRACK, RBRACK = 'INTEGER', 'PLUS', 'EOF', 'SUB','MUL', 'DIV', '(', ')'
'''
EOF = end of file
'''

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return f"{self.token_type} with value of {self.value}"
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def Error(self):
        raise Exception("Invalid character")
    
    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos+=1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
        
    def skip_white_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        """ Gets the integers in one term(also if multi digit and returns it"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
        """ Tokenizer, responsible for breaking down the whole string into tokens, one at a time"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_white_space()
                continue
            
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS,'+')
            if self.current_char == '-':
                self.advance()
                return Token(SUB,'-')
            if self.current_char == '*':
                self.advance()
                return Token(MUL,'*')
            if self.current_char == '/':
                self.advance()
                return Token(DIV,'/')
            if self.current_char == '(':
                self.advance()
                return Token(LBRACK,')')
            if self.current_char == ')':
                self.advance()
                return Token(RBRACK,')')
            
            
            self.Error()
        return Token(EOF, None)
