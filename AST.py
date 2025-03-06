from int import INTEGER, PLUS, EOF, SUB, MUL, DIV, LBRACK, RBRACK, Lexer, Token


class Parser:
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

    def term(self):
        node = self.factor()

        while self.cur_token.token_type in [MUL, DIV]:
            token = self.cur_token
            if token.token_type == MUL:
                self.eat(MUL)
            elif token.token_type == DIV:
                self.eat(DIV)
            node = BinaryOP(left=node, op=token, right=self.factor())
        return node
        
            

    
    def expr(self):

        node = self.term()

        while self.cur_token.token_type in [PLUS, SUB]:
            token = self.cur_token
            if token.token_type == PLUS:
                self.eat(PLUS)
            elif token.token_type == SUB:
                self.eat(SUB)
            node = BinaryOP(left=node, op=token, right=self.term())
        return node
    

    def parse(self):
        return self.expr()

class AST:
    pass

class BinaryOP(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = self.token = op
        self.right=right
    
class NUM(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

#Class for the Visitors Pattern : to separate the object and algorithm and could 
#therefore add new operations without chcannging the existing object structure
class NodeVisitor:
    def visit(self, node):
        met_name = type(node).__name__ + '_visit'
        visitor = getattr(self, met_name, self.generic_visit)
        return visitor(node)
    def generic_visit(self, node):
        raise Exception ("No visit method found".format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self,parser):
        self.parser=parser
    
    def BinaryOp_visit(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == SUB:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        else:
            return self.visit(node.left) / self.visit(node.right)
    
    def num_visit(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

