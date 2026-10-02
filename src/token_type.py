class TokenType:
    # Identifiers
    IDENTIFIER = "IDENTIFIER"

    # Keywords
    LET = "LET"
    SHOW = "SHOW"
    IF = "IF"
    ELSE = "ELSE"
    YES = "YES"
    NO = "NO"

    # Numeric and string literals
    NUMBER = "NUMBER"
    STRING = "STRING"

    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    STAR = "STAR"
    SLASH = "SLASH"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"

    # Punctuation
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    SEMICOLON = "SEMICOLON"

    # End of file
    EOF = "EOF"