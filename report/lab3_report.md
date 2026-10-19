# CIS 343 Lab 3: Quill Parser

## 1. Introduction

For this lab, I created a parser for my programming language, Quill. The parser takes the tokens from my scanner in Lab 1 and uses them to create an Abstract Syntax Tree (AST) using the classes from Lab 2.

I also updated Quill so the scanner, parser, and AST printer work together. I added error handling for invalid expressions and wrote tests to make sure everything works correctly.

## 2. Expression Grammar

I used the same expression grammar from Lab 2:

    expression → equality ;
    equality → comparison ( ( "==" | "!=" ) comparison )* ;
    comparison → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
    term → factor ( ( "+" | "-" ) factor )* ;
    factor → unary ( ( "*" | "/" ) unary )* ;
    unary → ( ( "!" | "-" ) unary ) | primary ;
    primary → NUMBER | STRING | "yes" | "no" | "(" expression ")" ;

Quill supports arithmetic operators (+, -, *, /), comparison operators (>, >=, <, <=), equality operators (==, !=), and unary operators (!, -).

It also supports numbers, strings, and Boolean values (`yes` and `no`). Parentheses can be used to group expressions.

The grammar follows the order of operations. Unary operators have the highest precedence, followed by multiplication and division, addition and subtraction, comparisons, and equality.

Binary operators at the same precedence level are grouped from left to right. Unary operators can be nested and are grouped from right to left.

I did not make any changes to the expression grammar from Lab 2.

## 3. Differences From Lox

Quill's expression grammar is similar to Lox, but Quill uses `yes` and `no` instead of `true` and `false`.

I also did not include `nil` because it is not a keyword in my scanner.

Quill has other keywords like `let`, `show`, `if`, and `else`, but I did not add statement parsing for this lab.

## 4. Parser Implementation

I created `parser.py` with a `Parser` class.

The parser takes a list of tokens and keeps track of which token it is reading. I used recursive-descent parsing, so each grammar rule has its own method.

The methods I created are:

- `parse()`: Starts parsing and checks for extra tokens.
- `expression()`: Starts parsing an expression.
- `equality()`: Handles `==` and `!=`.
- `comparison()`: Handles `>`, `>=`, `<`, and `<=`.
- `term()`: Handles addition and subtraction.
- `factor()`: Handles multiplication and division.
- `unary()`: Handles `!` and negative expressions.
- `primary()`: Handles numbers, strings, Boolean values, and parentheses.

I also added helper methods like `peek()`, `advance()`, `check()`, and `match()` to move through the tokens.

For example, this is my `term()` method:

    def term(self):
        expression = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.factor()
            expression = Binary(expression, operator, right)

        return expression

This method handles addition and subtraction. It calls `factor()` first so multiplication and division are grouped before addition and subtraction.

The `while` loop allows the parser to handle multiple operators and group them from left to right.

## 5. Connecting the Scanner, Parser, and AST Printer

I updated `quill.py` so all three parts work together.

The scanner reads the source code and creates tokens. The parser takes those tokens and builds an AST. Then the AST printer turns the AST into a string.

I changed my `run()` method to:

    def run(source):
        try:
            scanner = Scanner(source)
            tokens = scanner.scan_tokens()

            parser = Parser(tokens)
            expression = parser.parse()

            printer = AstPrinter()
            print(printer.to_string(expression))

        except SyntaxError as error:
            print(f"Syntax Error: {error}")

For example:

Input:

    3 + 4 * 2

Output:

    (+ 3.0 (* 4.0 2.0))

This shows that the parser groups multiplication before addition.

I kept the file and interactive modes from Lab 1, so I can enter expressions in the terminal or read them from a `.quill` file.

## 6. Error Handling

I added error handling so the parser can recognize invalid expressions.

The parser checks for missing operands, missing parentheses, and extra tokens. I also updated the scanner to handle unexpected characters, unterminated strings, and invalid decimal numbers.

For example, if I enter:

    (3 + 4

Quill prints:

    Syntax Error: Line 1: Missing closing parenthesis.

I used `try` and `except` in `quill.py` so the program prints an error message instead of crashing.

The error messages also include the line number to help show where the problem happened.

## 7. Concrete Syntax Tree for a Valid Expression

For my valid expression, I used:

    3 + 4 * 2

Here is the Concrete Syntax Tree (CST) showing how the expression follows my grammar:

    expression
    └── equality
        └── comparison
            └── term
                ├── factor
                │   └── unary
                │       └── primary
                │           └── NUMBER: 3
                ├── "+"
                └── factor
                    ├── unary
                    │   └── primary
                    │       └── NUMBER: 4
                    ├── "*"
                    └── unary
                        └── primary
                            └── NUMBER: 2

The AST printer output for this expression is:

    (+ 3.0 (* 4.0 2.0))

The CST shows how the parser follows the grammar rules. Since multiplication is handled by `factor()` and addition is handled by `term()`, `4 * 2` is grouped together first.

The AST printer shows the same grouping but leaves out the extra grammar rules. The multiplication expression is inside the addition expression.

The parser does not calculate the result. It only builds and prints the AST.

The CST leaves out empty repetitions in the grammar to make it easier to read.

## 8. Tests

I created `test_parser.py` using Python's `unittest` library.

The tests scan an expression, parse it, and compare the AST printer's output to the expected output.

I wrote 25 tests total. Fifteen test valid expressions, and ten test invalid expressions.

### Valid Expression Tests

**Test 1: Addition**

This checks basic addition.

Input: `3 + 4`

Expected: `(+ 3.0 4.0)`

Actual: `(+ 3.0 4.0)`

Result: Passed

**Test 2: Multiplication**

This checks basic multiplication.

Input: `3 * 4`

Expected: `(* 3.0 4.0)`

Actual: `(* 3.0 4.0)`

Result: Passed

**Test 3: Operator Precedence**

This checks that multiplication is grouped before addition.

Input: `3 + 4 * 2`

Expected: `(+ 3.0 (* 4.0 2.0))`

Actual: `(+ 3.0 (* 4.0 2.0))`

Result: Passed

**Test 4: Parentheses**

This checks that parentheses change how an expression is grouped.

Input: `(3 + 4) * 2`

Expected: `(* (group (+ 3.0 4.0)) 2.0)`

Actual: `(* (group (+ 3.0 4.0)) 2.0)`

Result: Passed

**Test 5: Left Associativity**

This checks that subtraction is grouped from left to right.

Input: `10 - 5 - 2`

Expected: `(- (- 10.0 5.0) 2.0)`

Actual: `(- (- 10.0 5.0) 2.0)`

Result: Passed

**Test 6: Division**

This checks the division operator.

Input: `10 / 2`

Expected: `(/ 10.0 2.0)`

Actual: `(/ 10.0 2.0)`

Result: Passed

**Test 7: Comparison**

This checks the `>=` operator.

Input: `5 >= 3`

Expected: `(>= 5.0 3.0)`

Actual: `(>= 5.0 3.0)`

Result: Passed

**Test 8: Equality**

This checks the `==` operator.

Input: `3 + 4 == 7`

Expected: `(== (+ 3.0 4.0) 7.0)`

Actual: `(== (+ 3.0 4.0) 7.0)`

Result: Passed

**Test 9: Not Equal**

This checks the `!=` operator.

Input: `5 != 3`

Expected: `(!= 5.0 3.0)`

Actual: `(!= 5.0 3.0)`

Result: Passed

**Test 10: Negative Number**

This checks the unary minus operator.

Input: `-5`

Expected: `(- 5.0)`

Actual: `(- 5.0)`

Result: Passed

**Test 11: NOT Operator**

This checks the unary `!` operator.

Input: `!yes`

Expected: `(! yes)`

Actual: `(! yes)`

Result: Passed

**Test 12: String**

This checks string literals.

Input: `"Harry Potter"`

Expected: `Harry Potter`

Actual: `Harry Potter`

Result: Passed

**Test 13: Boolean Values**

This checks the `yes` and `no` keywords.

Input: `yes == no`

Expected: `(== yes no)`

Actual: `(== yes no)`

Result: Passed

**Test 14: Decimal Numbers**

This checks decimal values.

Input: `3.14 * 2`

Expected: `(* 3.14 2.0)`

Actual: `(* 3.14 2.0)`

Result: Passed

**Test 15: Nested Parentheses**

This checks parentheses inside other parentheses.

Input: `((2 + 3) * 4)`

Expected: `(group (* (group (+ 2.0 3.0)) 4.0))`

Actual: `(group (* (group (+ 2.0 3.0)) 4.0))`

Result: Passed

### Invalid Expression Tests

These tests check that the scanner or parser reports an error when the input is invalid.

**Test 16: Missing Closing Parenthesis**

Input: `(3 + 4`

Expected: `Syntax Error: Line 1: Missing closing parenthesis.`

Actual: `Syntax Error: Line 1: Missing closing parenthesis.`

Result: Passed

The expression has an opening parenthesis but no closing parenthesis.

**Test 17: Extra Closing Parenthesis**

Input: `3 + 4)`

Expected: `Syntax Error: Line 1: Unexpected token ')'.`

Actual: `Syntax Error: Line 1: Unexpected token ')'.`

Result: Passed

There is an extra closing parenthesis after the expression.

**Test 18: Missing Operand**

Input: `3 +`

Expected: `Syntax Error: Line 1: Expected an expression.`

Actual: `Syntax Error: Line 1: Expected an expression.`

Result: Passed

The addition operator is missing the expression on its right side.

**Test 19: Extra Number**

Input: `3 + 4 5`

Expected: `Syntax Error: Line 1: Unexpected token '5'.`

Actual: `Syntax Error: Line 1: Unexpected token '5'.`

Result: Passed

The parser finds another number after the expression without an operator.

**Test 20: Empty Expression**

Input: An empty expression

Expected: `Syntax Error: Line 1: Expected an expression.`

Actual: `Syntax Error: Line 1: Expected an expression.`

Result: Passed

There is no expression for the parser to read.

**Test 21: Invalid Operator Sequence**

Input: `3 * / 2`

Expected: `Syntax Error: Line 1: Expected an expression.`

Actual: `Syntax Error: Line 1: Expected an expression.`

Result: Passed

The parser finds a division operator where an operand should be.

**Test 22: Unterminated String**

Input: `"Harry Potter`

Expected: `Syntax Error: Line 1: Unterminated string.`

Actual: `Syntax Error: Line 1: Unterminated string.`

Result: Passed

The string is missing its closing quotation mark.

**Test 23: Invalid Character**

Input: `3 @ 4`

Expected: `Syntax Error: Line 1: Unexpected character '@'.`

Actual: `Syntax Error: Line 1: Unexpected character '@'.`

Result: Passed

The scanner does not recognize `@` as a valid character in Quill.

**Test 24: Invalid Decimal**

Input: `3.`

Expected: `Syntax Error: Line 1: Invalid decimal number.`

Actual: `Syntax Error: Line 1: Invalid decimal number.`

Result: Passed

The decimal point does not have a digit after it.

**Test 25: Multiple Decimal Points**

Input: `12.34.56`

Expected: `Syntax Error: Line 1: Invalid decimal number.`

Actual: `Syntax Error: Line 1: Unexpected character '.'`

Result: Passed

The number contains another decimal point, so the scanner rejects it.

### Test Results

I ran the automated tests using:

    python -m unittest discover -s test/lab3 -p "test_parser.py" -v

All 25 tests passed.

## 9. Testing File and Interactive Input

I also tested reading expressions from a `.quill` file.

I created `test/lab3/parser_example.quill` with:

    (10 + 5) * 2 >= 25

I ran it using:

    python src/quill.py test/lab3/parser_example.quill

Expected:

    (>= (* (group (+ 10.0 5.0)) 2.0) 25.0)

Actual:

    (>= (* (group (+ 10.0 5.0)) 2.0) 25.0)

Result: Passed

I also tested an invalid expression:

    (10 + 5 * 2

Quill reported that the closing parenthesis was missing.

For interactive mode, I ran:

    python src/quill.py

I entered a valid expression:

    3 + 4 * 2

Output:

    (+ 3.0 (* 4.0 2.0))

I also checked how the program handles an invalid expression followed by another valid expression.

Input:

    3 +

Output:

    Syntax Error: Line 1: Expected an expression.

Next input:

    5 * 2

Output:

    (* 5.0 2.0)

This shows that the interactive shell can continue after a syntax error.

## 10. How to Run

I used Python and PyCharm for this lab. The program only uses Python's standard library, so I did not need to install any additional packages.

To run Quill:

1. Open the project in PyCharm.
2. Make sure the `src` folder contains the scanner, parser, AST classes, AST printer, token files, and `quill.py`.
3. Open the terminal in the main project folder.
4. To start interactive mode, run:

       python src/quill.py

5. To run a Quill source file, use:

       python src/quill.py test/lab3/parser_example.quill

6. To run the automated tests, use:

       python -m unittest discover -s test/lab3 -p "test_parser.py" -v

The project files are organized into `src`, `test/lab3`, and `report` folders.

## 11. Limitations

My parser currently only handles expressions. It does not support full statements using keywords like `let`, `show`, or `if`.

It also does not calculate the result of expressions. It only creates the AST and prints it.

I have not added variable expressions, assignments, function calls, or logical AND/OR operators.

The parser only handles one expression at a time instead of multiple statements in a file.

I also have not added separate automated tests for every comparison operator yet, although the parser supports them.

These are things I could add in future labs.

## 12. Conclusion

For this lab, I created a parser for Quill using recursive-descent parsing. I connected it to my scanner and AST printer from Labs 1 and 2.

I tested different operators, parentheses, literals, and invalid expressions. I also tested reading expressions from files and using the interactive shell.

All 25 automated tests passed, and the parser works for the expressions I included in my grammar.