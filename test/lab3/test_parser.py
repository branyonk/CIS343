
import sys
import unittest
from pathlib import Path
"""// --- start AI code ---"""
# Allow the tests to import files from the src folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
"""// --- end AI code ---"""
from scanner import Scanner
from parser import Parser
from printer import AstPrinter

class TestParser(unittest.TestCase):
    def parse_expression(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        printer = AstPrinter()
        return printer.to_string(expression)

    def test_addition(self):
        result = self.parse_expression("3 + 4")
        self.assertEqual(result, "(+ 3.0 4.0)")

    def test_multiplication(self):
        result = self.parse_expression("3 * 4")
        self.assertEqual(result, "(* 3.0 4.0)")

    def test_operator_precedence(self):
        result = self.parse_expression("3 + 4 * 2")
        self.assertEqual(result, "(+ 3.0 (* 4.0 2.0))")

    def test_parentheses(self):
        result = self.parse_expression("(3 + 4) * 2")
        self.assertEqual(result, "(* (group (+ 3.0 4.0)) 2.0)")

    def test_left_associativity(self):
        result = self.parse_expression("10 - 5 - 2")
        self.assertEqual(result, "(- (- 10.0 5.0) 2.0)")

    def test_division(self):
        result = self.parse_expression("10 / 2")
        self.assertEqual(result, "(/ 10.0 2.0)")

    def test_comparison(self):
        result = self.parse_expression("5 >= 3")
        self.assertEqual(result, "(>= 5.0 3.0)")

    def test_equality(self):
        result = self.parse_expression("3 + 4 == 7")
        self.assertEqual(result, "(== (+ 3.0 4.0) 7.0)")

    def test_not_equal(self):
        result = self.parse_expression("5 != 3")
        self.assertEqual(result, "(!= 5.0 3.0)")

    def test_negative_number(self):
        result = self.parse_expression("-5")
        self.assertEqual(result, "(- 5.0)")

    def test_not_operator(self):
        result = self.parse_expression("!yes")
        self.assertEqual(result, "(! yes)")

    def test_string(self):
        result = self.parse_expression('"Harry Potter"')
        self.assertEqual(result, "Harry Potter")

    def test_boolean(self):
        result = self.parse_expression("yes == no")
        self.assertEqual(result, "(== yes no)")

    def test_decimal(self):
        result = self.parse_expression("3.14 * 2")
        self.assertEqual(result, "(* 3.14 2.0)")

    def test_nested_parentheses(self):
        result = self.parse_expression("((2 + 3) * 4)")
        self.assertEqual(result, "(group (* (group (+ 2.0 3.0)) 4.0))")

    def test_missing_right_parenthesis(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression("(3 + 4")

    def test_extra_right_parenthesis(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression("3 + 4)")

    def test_missing_operand(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression("3 +")

    def test_extra_number(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression("3 + 4 5")

    def test_empty_expression(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression("")

    def test_invalid_operator(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression("3 * / 2")

    def test_unterminated_string(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression('"Harry Potter')

    def test_invalid_character(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression("3 @ 4")

    def test_invalid_decimal(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression("3.")

    def test_multiple_decimal_points(self):
        with self.assertRaises(SyntaxError):
            self.parse_expression("12.34.56")

if __name__ == "__main__":
    unittest.main()
