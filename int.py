INTEGER, PLUS, EOF, SUB = 'INTEGER', 'PLUS', 'EOF', 'SUB'
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
            token = Token(PLUS, cur_char)
            self.pos+=1
            return token
        if cur_char == '-':
            token = Token(SUB, cur_char)
            self.pos+=1
            return token
        self.error()

    def eat(self, token_type):
        if self.cur_token.token_type == token_type:
            self.cur_token = self.get_next_token()
        else:
            self.error()
    
    def expr(self):
        self.cur_token = self.get_next_token()

        left = self.cur_token
        self.eat(INTEGER)

        op = self.cur_token
        if op.token_type == PLUS:
            self.eat(PLUS)
        else:
            self.eat(SUB)
    
        right = self.cur_token
        self.eat(INTEGER)
        result=0
        if op.token_type == SUB:
            result = left.value - right.value
        else:
            result = left.value + right.value
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

