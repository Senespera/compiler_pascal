from parse.node import IdentifierNode, RealNode, IntegerNode, BinaryOperationNode, UnaryOperationNode
class ParserException(Exception):
    pass
class ParserExpr:
    def __init__(self,lexer):
        self.lexer = lexer

    def parse_expr(self):
        lexem = self.lexer.get_current_lexem()
        if not lexem:
            raise ParserException("expression was expected")
        left = self.parse_term()
        operation = self.lexer.get_current_lexem()
        if operation:
            while operation.get_value() in {'+', '-'}:
                self.lexer.get_next_lexem()
                right = self.parse_term()
                left = BinaryOperationNode(operation, left, right)
                operation = self.lexer.get_current_lexem()
                if not operation:
                    break
        return left

    def parse_term(self):
        left = self.parse_factor()
        operation = self.lexer.get_current_lexem()
        if operation:
            while operation.get_value() in {'*','/'}:
                self.lexer.get_next_lexem()
                right = self.parse_factor()
                left = BinaryOperationNode(operation, left, right)
                operation = self.lexer.get_current_lexem()
                if not operation:
                    break
        return left

    def parse_factor(self):
        lexem = self.lexer.get_current_lexem()
        self.lexer.get_next_lexem()
        if lexem:
            if lexem.get_type() == "variable":
                return IdentifierNode(lexem)
            elif lexem.get_type() == "integer":
                return IntegerNode(lexem)
            elif lexem.get_type() == "real":
                return RealNode(lexem)
            if lexem.get_value() in {'+','-'}:
                operand = self.parse_factor()
                return UnaryOperationNode(lexem, operand)
            if lexem.get_value() == '(':
                left = self.parse_expr()
                lexem = self.lexer.get_current_lexem()
                if lexem.get_value() != ')':
                    raise ParserException(f"{lexem.get_coordinates()}        syntax error: '{lexem.get_code()}'")
                self.lexer.get_next_lexem()
                return left
            raise ParserException(f"{lexem.get_coordinates()}        syntax error: '{lexem.get_code()}'")
        raise ParserException("unexpected end of file")