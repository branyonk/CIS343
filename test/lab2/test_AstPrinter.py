from quill_ast import Binary, Unary, Literal, Grouping
from printer import AstPrinter
from token import Token
from token_type import TokenType

# Test 1
minus = Token(TokenType.MINUS, "-", None, 1)
multiply = Token(TokenType.STAR, "*", None, 1)

left = Unary(minus, Literal(123))
right = Grouping(Literal(45.67))

expression = Binary(left, multiply, right)

printer = AstPrinter()

expected = "(* (- 123) (group 45.67))"
actual = printer.to_string(expression)

print("Test 1:")
print("Expected:", expected)
print("Actual:", actual)

if expected == actual:
    print("Test Passed")
else:
    print("Test Failed")

# Test 2: Addition and subtraction

plus = Token(TokenType.PLUS, "+", None, 1)
minus = Token(TokenType.MINUS, "-", None, 1)

left = Binary(Literal(10), plus, Literal(5))
expression = Binary(left, minus, Literal(3))

expected = "(- (+ 10 5) 3)"
actual = printer.to_string(expression)

print()
print("Test 2:")
print("Expected:", expected)
print("Actual:", actual)

if expected == actual:
    print("Test Passed")
else:
    print("Test Failed")

# Test 3: Strings and Boolean values

expression1 = Literal("The Hunger Games")
expression2 = Literal(True)
expression3 = Literal(False)
expression4 = Literal(None)

expected1 = "The Hunger Games"
expected2 = "yes"
expected3 = "no"
expected4 = "nil"

actual1 = printer.to_string(expression1)
actual2 = printer.to_string(expression2)
actual3 = printer.to_string(expression3)
actual4 = printer.to_string(expression4)

print()
print("Test 3:")

if (expected1 == actual1 and expected2 == actual2 and expected3 == actual3 and expected4 == actual4):
    print("Test Passed")
else:
    print("Test Failed")

print("String:", actual1)
print("True:", actual2)
print("False:", actual3)
print("None:", actual4)

# Test 4: Testing the remaining operators

print()
print("Test 4:")

operators = [
    Token(TokenType.SLASH, "/", None, 1),
    Token(TokenType.EQUAL_EQUAL, "==", None, 1),
    Token(TokenType.BANG_EQUAL, "!=", None, 1),
    Token(TokenType.LESS, "<", None, 1),
    Token(TokenType.LESS_EQUAL, "<=", None, 1),
    Token(TokenType.GREATER, ">", None, 1),
    Token(TokenType.GREATER_EQUAL, ">=", None, 1)
]

for operator in operators:
    expression = Binary(Literal(10), operator, Literal(2))

    expected = "(" + operator.lexeme + " 10 2)"
    actual = printer.to_string(expression)

    print("Expected:", expected)
    print("Actual:", actual)

    if expected == actual:
        print("Test Passed")
    else:
        print("Test Failed")

    print()


# Testing the NOT operator

not_operator = Token(TokenType.BANG, "!", None, 1)
expression = Unary(not_operator, Literal(True))

expected = "(! yes)"
actual = printer.to_string(expression)

print("Expected:", expected)
print("Actual:", actual)

if expected == actual:
    print("Test Passed")
else:
    print("Test Failed")
