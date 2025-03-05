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

class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos=0
        self.cur_token = None
        
    def error(self):
        raise Exception("Error parsing input")

    def get_next_token(self):
        text = self.text
        if self.pos < len(text)-1 and text[self.pos] ==' ':
            self.pos+=1
        if self.pos >= len(text):
            return Token(EOF, None)
        
        cur_char = text[self.pos]

        if cur_char.isdigit():
            num_str = ''
            while self.pos < len(text) and text[self.pos].isdigit():
                num_str+=text[self.pos]
                self.pos+=1
            token = Token(INTEGER, int(num_str))
            return token
        
        if cur_char == '+':
            self.pos+=1
            return Token(PLUS, cur_char)
        elif cur_char == '-':
            self.pos+=1
            return Token(SUB, cur_char)
        elif cur_char == '*':
            self.pos+=1
            return Token(MUL, cur_char)
        elif cur_char == '/' or cur_char =='//':
            self.pos+=1
            return Token(DIV, cur_char)
        self.error()

    def eat(self, token_type):
        if self.cur_token.token_type == token_type:
            self.cur_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        self.cur_token = self.get_next_token()
        result = self.cur_token.value
        self.eat(INTEGER)

        while self.cur_token.token_type in [PLUS, SUB, MUL, DIV]:
            op = self.cur_token
            if op.token_type == PLUS:
                self.eat(PLUS)
                result += self.cur_token.value
            elif op.token_type == SUB:
                self.eat(SUB)
                result -= self.cur_token.value
            elif op.token_type == MUL:
                self.eat(MUL)
                result *= self.cur_token.value
            else:
                self.eat(DIV)
                result //= self.cur_token.value
            self.eat(INTEGER)
        return result
    

def main():
    while True:
        try:
            text = input("calc> ")
        except EOFError:
            break
        if not text:
            continue
        Interp=Interpreter(text)
        result=Interp.expr()
        return result

if __name__ == '__main__':
    main()

