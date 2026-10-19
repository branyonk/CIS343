
from token_type import TokenType
from quill_ast import Binary, Unary, Literal, Grouping


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        """Parse an expression and check for extra tokens."""
        expression = self.expression()
        if not self.at_end():
            raise SyntaxError(f"Line {self.peek().line}: Unexpected token '{self.peek().lexeme}'.")
        return expression

    def expression(self):
        return self.equality()

    def at_end(self):
        """Check if we reached the end of the tokens."""
        return self.peek().token_type == TokenType.EOF

    def peek(self):
        """Look at the current token without moving forward."""
        return self.tokens[self.current]

    def previous(self):
        """Return the last token we read."""
        return self.tokens[self.current - 1]

    def advance(self):
        """Move to the next token."""
        if not self.at_end():
            self.current += 1
        return self.previous()

    def check(self, token_type):
        """Check if the current token matches a type."""
        if self.at_end():
            return False
        return self.peek().token_type == token_type

    def match(self, *types):
        """Check for a matching token and move past it."""
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def primary(self):
        """Handle numbers, strings, yes, no, and parentheses."""
        if self.match(TokenType.YES):
            return Literal(True)
        if self.match(TokenType.NO):
            return Literal(False)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            value = self.previous().literal
            return Literal(value)
        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            if not self.match(TokenType.RIGHT_PAREN):
                raise SyntaxError(f"Line {self.peek().line}: Missing closing parenthesis.")
            return Grouping(expression)
        raise SyntaxError(f"Line {self.peek().line}: Expected an expression.")

    def unary(self):
        """Handle negative numbers and the ! operator."""
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def factor(self):
        """Handle multiplication and division."""
        expression = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self.previous()
            right = self.unary()
            expression = Binary(expression, operator, right)
        return expression

    def term(self):
        """Handle addition and subtraction."""
        expression = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)
        return expression

    def comparison(self):
        """Handle comparison operators."""
        expression = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expression = Binary(expression, operator, right)
        return expression

    def equality(self):
        """Handle equality operators."""
        expression = self.comparison()
        while self.match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expression = Binary(expression, operator, right)
        return expression
