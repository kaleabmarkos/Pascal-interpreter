INTEGER, PLUS, EOF, SUB, MUL, DIV = 'INTEGER', 'PLUS', 'EOF', 'SUB','MUL', 'DIV'
'''
EOF = end of file
'''

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"{self.token_type} with value of {self.value}"
    
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def Error(self):
        raise Exception("Invalid character")
    
    def advance(self):
        self.pos+=1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
        
    def skip_white_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result+=self.current_char
            self.advance()
        return int(result)
    
    def get_next_token(self):
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
            
            self.Error()
        return Token(EOF, None)

        

class Interpreter:
    def __init__(self, lexer):
        self.lexer=lexer
        self.cur_token = self.lexer.get_next_token()
        
    def error(self):
        raise Exception("Error parsing input")



    def eat(self, token_type):
        if self.cur_token.token_type == token_type:
            self.cur_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        token = self.cur_token
        self.eat(INTEGER)
        return token.value

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

