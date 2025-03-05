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

        

class Interpreter:
    def __init__(self, lexer):
        self.lexer=lexer
        self.cur_token = self.lexer.get_next_token()
        
    def error(self):
        raise Exception("Error parsing input")


    def eat(self, token_type):
        """ compare the current token type with the passed token
         type and if they match then "eat" the current token
         and assign the next token to the self.current_token,
         otherwise raise an exception(calls error)."""
        
        if self.cur_token.token_type == token_type:
            self.cur_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        token = self.cur_token
        if token.token_type == INTEGER:
            self.eat(INTEGER)
            return token.value
        elif token.token_type == LBRACK:
            self.eat(LBRACK)
            result = self.expr()
            self.eat(RBRACK)
            return result

    def terms(self):
        result = self.factor()

        while self.cur_token.token_type in [MUL, DIV]:
            if self.cur_token.token_type == MUL:
                self.eat(MUL)
                result*=self.factor()
            elif self.cur_token.token_type == DIV:
                self.eat(DIV)
                result/=self.factor()
        return result
        
            

    
    def expr(self):
        """
        Arithmetic expression parser / interpreter.

        calc> 7 + 3 * (10 / (12 / (3 + 1) - 1))
        22

        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*
        factor : INTEGER | LPAREN expr RPAREN
        """
        result = self.terms()

        while self.cur_token.token_type in [PLUS, SUB]:
            token = self.cur_token
            if token.token_type == PLUS:
                self.eat(PLUS)
                result+=self.terms()
            elif token.token_type == SUB:
                self.eat(SUB)
                result-=self.terms()
        return result
    

def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        lex = Lexer(text)
        Interp=Interpreter(lex)
        result=Interp.expr()
        return result

if __name__ == '__main__':
    main()