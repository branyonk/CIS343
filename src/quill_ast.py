class Expression:
    pass

class Literal(Expression):
    def __init__(self, value):
        self.value = value

class Unary(Expression):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class Binary(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Grouping(Expression):
    def __init__(self, expression):
        self.expression = expression