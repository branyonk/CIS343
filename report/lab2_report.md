
# CIS 343 Lab 2: Quill AST Printer

## 1. Introduction

For this lab, I created an Abstract Syntax Tree (AST) and an AST printer for my programming language, Quill. The AST stores different types of expressions, and the printer turns them into strings.


## 2. Expression Grammar

This is the expression grammar I used for Quill in Lab 2:

    expression → equality ;
    equality → comparison ( ( "==" | "!=" ) comparison )* ;
    comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    term → factor ( ( "+" | "-" ) factor )* ;
    factor → unary ( ( "*" | "/" ) unary )* ;
    unary → ( "!" | "-" ) unary | primary ;
    primary → NUMBER | STRING | "yes" | "no" | "(" expression ")" ;

Quill supports arithmetic operators (+, -, *, /), comparison operators (>, >=, <, <=), equality operators (==, !=), and unary operators (!, -).

The literal types are numbers, strings, and Boolean values (`yes` and `no`). Parentheses can also be used to group expressions.

The grammar follows the order of operations. For example, multiplication and division happen before addition and subtraction. Parentheses can be used to change the order of operations.

For this lab, I focused on the expression types supported by my AST classes.

## 3. Differences From Lox

Quill's expression grammar is similar to Lox, but Quill uses `yes` and `no` instead of `true` and `false`.

Lox also includes `nil`, but I did not include it in Quill's grammar because my scanner does not recognize it as a keyword.

Quill also has its own keywords, such as `let` and `show`. For this lab, I focused on expressions rather than statements.

## 4. AST Classes

I created `quill_ast.py` with these classes:

- `Expression`: Base class for expressions.
- `Binary`: Stores two expressions and an operator.
- `Unary`: Stores one expression and an operator.
- `Literal`: Stores a value.
- `Grouping`: Stores an expression inside parentheses.

I reused the Token class from Lab 1 for the operators.

## 5. AST Printer

I created `printer.py` with an `AstPrinter` class.

The `to_string()` method checks the expression type and turns it into a string. It calls itself when an expression contains another expression.

For example:

    (* (- 123) (group 45.67))

The printer does not calculate the result of an expression. It only prints the AST.

## 6. Tests

I created `test_AstPrinter.py` to test the AST printer. Each test creates an AST directly in Python and compares the expected output to the actual output.

### Test 1: Expression Types

This test checks Binary, Unary, Literal, and Grouping.

Code:

    minus = Token(TokenType.MINUS, "-", None, 1)
    multiply = Token(TokenType.STAR, "*", None, 1)

    left = Unary(minus, Literal(123))
    right = Grouping(Literal(45.67))
    expression = Binary(left, multiply, right)

Expected:

    (* (- 123) (group 45.67))

Actual:

    (* (- 123) (group 45.67))

Result: Passed

### Test 2: Addition and Subtraction

This test checks nested binary expressions.

Code:

    plus = Token(TokenType.PLUS, "+", None, 1)
    minus = Token(TokenType.MINUS, "-", None, 1)

    left = Binary(Literal(10), plus, Literal(5))
    expression = Binary(left, minus, Literal(3))

Expected:

    (- (+ 10 5) 3)

Actual:

    (- (+ 10 5) 3)

Result: Passed

### Test 3: Literals

This test checks strings, Boolean values, and None.

Code:

    expression1 = Literal("The Hunger Games")
    expression2 = Literal(True)
    expression3 = Literal(False)
    expression4 = Literal(None)

Expected:

    The Hunger Games
    yes
    no
    nil

Actual:

    The Hunger Games
    yes
    no
    nil

Result: Passed

### Test 4: Other Operators

This test checks division, equality, comparison, and NOT operators.

Code:

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

    not_operator = Token(TokenType.BANG, "!", None, 1)
    expression = Unary(not_operator, Literal(True))

Expected:

    (/ 10 2)
    (== 10 2)
    (!= 10 2)
    (< 10 2)
    (<= 10 2)
    (> 10 2)
    (>= 10 2)
    (! yes)

Actual:

    (/ 10 2)
    (== 10 2)
    (!= 10 2)
    (< 10 2)
    (<= 10 2)
    (> 10 2)
    (>= 10 2)
    (! yes)

Result: Passed

## 7. How to Run

1. Open the project in PyCharm.
2. Make sure the `src` folder is marked as a Sources Root.
3. Open `test/lab2/test_AstPrinter.py`.
4. Run the test file.
5. Check the output to see if the tests passed.

All four test groups passed.

## 8. Limitations

The AST printer only works with expressions created directly in Python. It does not read Quill source code, build an AST automatically, or evaluate expressions.

The printer can print `nil` when a literal has the value `None`, but `nil` is not currently a keyword in Quill.

The grammar only covers the expression types used for this lab. I did not add variable or assignment expressions to the AST.

## 9. Conclusion

For this lab, I created the AST classes and printer for Quill. I tested different expressions, literals, and operators, and all four test groups passed.
