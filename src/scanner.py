from quill_token import Token
from token_type import TokenType


class Scanner:
    """Scans Quill source code and turns it into a list of tokens."""

    # Words that have a special meaning in Quill
    keywords = {
        "let": TokenType.LET,
        "show": TokenType.SHOW,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "yes": TokenType.YES,
        "no": TokenType.NO
    }

    def __init__(self, source):
        """Set up the scanner with the source code."""
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def at_end(self):
        """Check if the scanner has reached the end of the source code."""
        return self.current >= len(self.source)

    def scan_tokens(self):
        """Scan the source code and return all of the tokens."""
        while not self.at_end():
            self.start = self.current
            self.scan_a_token()

        # Add an EOF token when scanning is finished
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def advance(self):
        """Read the current character and move to the next one."""
        character = self.source[self.current]
        self.current += 1
        return character

    def match(self, next_char):
        """Check if the next character matches the one we are looking for."""
        if self.at_end():
            return False

        if self.source[self.current] != next_char:
            return False

        self.current += 1
        return True

    def identifier(self):
        """Scan an identifier or keyword."""
        while not self.at_end():
            character = self.source[self.current]

            if character.isalnum() or character == "_":
                self.advance()
            else:
                break

        text = self.source[self.start:self.current]

        # Check if the word is a Quill keyword
        if text in self.keywords:
            self.add_token(self.keywords[text])
        else:
            self.add_token(TokenType.IDENTIFIER)

    def string(self):
        """Scan a string literal."""
        while not self.at_end() and self.source[self.current] != '"':
            if self.source[self.current] == "\n":
                self.line += 1

            self.advance()

        # The string never had a closing quotation mark
        if self.at_end():
            raise SyntaxError(f"Line {self.line}: Unterminated string.")

        # Move past the closing quotation mark
        self.advance()

        # Get the string value without the quotation marks
        value = self.source[self.start + 1:self.current - 1]
        self.add_token_with_value(TokenType.STRING, value)


    def number(self):
        """Scan a whole number or decimal number."""
        while not self.at_end() and self.source[self.current].isdigit():
            self.advance()
        if not self.at_end() and self.source[self.current] == ".":
            if (self.current + 1 >= len(self.source)
                    or not self.source[self.current + 1].isdigit()):
                raise SyntaxError(f"Line {self.line}: Invalid decimal number.")
            self.advance()
            while not self.at_end() and self.source[self.current].isdigit():
                self.advance()
        value = float(self.source[self.start:self.current])
        self.add_token_with_value(TokenType.NUMBER, value)

    def add_token(self, token_type):
        """Add a token that does not have a literal value."""
        text = self.source[self.start:self.current]
        token = Token(token_type, text, None, self.line)
        self.tokens.append(token)

    def add_token_with_value(self, token_type, value):
        """Add a token that has a literal value."""
        text = self.source[self.start:self.current]
        token = Token(token_type, text, value, self.line)
        self.tokens.append(token)

    def scan_a_token(self):
        """Scan one token from the source code."""
        character = self.advance()

        # Punctuation
        if character == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif character == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif character == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif character == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif character == ";":
            self.add_token(TokenType.SEMICOLON)

        # Operators
        elif character == "+":
            self.add_token(TokenType.PLUS)
        elif character == "-":
            self.add_token(TokenType.MINUS)
        elif character == "*":
            self.add_token(TokenType.STAR)
        elif character == "/":
            self.add_token(TokenType.SLASH)

        elif character == "=":
            if self.match("="):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)

        elif character == "!":
            if self.match("="):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)

        elif character == ">":
            if self.match("="):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)

        elif character == "<":
            if self.match("="):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)

        # Strings
        elif character == '"':
            self.string()

        # Ignore spaces, tabs, and carriage returns
        elif character == " " or character == "\t" or character == "\r":
            pass

        # Keep track of line numbers
        elif character == "\n":
            self.line += 1

        # Quill comments start with #
        elif character == "#":
            while not self.at_end() and self.source[self.current] != "\n":
                self.advance()

        # Numbers
        elif character.isdigit():
            self.number()

        # Identifiers and keywords
        elif character.isalpha() or character == "_":
            self.identifier()

        # Anything else is not valid in Quill
        else:
            raise SyntaxError(f"Line {self.line}: Unexpected character '{character}'.")