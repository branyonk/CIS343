from quill_ast import Binary, Unary, Literal, Grouping

class AstPrinter:
    def to_string(self, expression):
        if isinstance(expression, Binary):
            left = self.to_string(expression.left)
            right = self.to_string(expression.right)
            operator = expression.operator.lexeme
            return "(" + operator + " " + left + " " + right + ")"

        elif isinstance(expression, Unary):
            right = self.to_string(expression.right)
            operator = expression.operator.lexeme
            return "(" + operator + " " + right + ")"
        elif isinstance(expression, Grouping):
            inside = self.to_string(expression.expression)
            return "(group " + inside + ")"
        elif isinstance(expression, Literal):
            if expression.value is None:
                return "nil"
            elif expression.value is True:
                return "yes"
            elif expression.value is False:
                return "no"
            else:
                return str(expression.value)
        else:
            return "Unknown expression"