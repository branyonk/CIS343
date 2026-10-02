# CIS 343 Lab 1: Quill Scanner

## About Quill

For this lab, I made a language called **Quill**. I chose the name Quill because I wanted the language to have a writing/book theme. Quill files use the `.quill` extension.

For this lab, Quill only scans code. It reads through the source code and separates it into tokens. Each token stores its type, lexeme, literal value, and line number.

## Quill's Lexical Rules

### Identifiers

Identifiers have to start with a letter or `_`. After that, they can also have numbers.

**Regex:** `[A-Za-z_][A-Za-z0-9_]*`

Examples:

- `book`
- `book2`
- `favorite_book`
- `_score`

I also tested `letter` because it starts with `let`. It is still an `IDENTIFIER` because it does not exactly match the `let` keyword.

### Numbers

Quill allows whole numbers and decimals.

**Regex:** `[0-9]+(\.[0-9]+)?`

Examples:

- `0`
- `95`
- `3.14`
- `100.25`

I used Python floats for the literal values. This is why `95` prints with a literal value of `95.0`.

The minus sign is its own token, so `-122` gets scanned as:

`MINUS - None`

`NUMBER 122 122.0`

### Strings

Strings use double quotes.

**Regex:** `"[^"]*"`

Examples:

- `"hello"`
- `"The Hunger Games"`
- `""`

The lexeme keeps the quotes, but the literal does not. For example, `"hello"` has a literal value of `hello`.

If there is no closing quote, Quill gives an unterminated string error.

## Quill Tokens

### Keywords

I chose these keywords for Quill:

| Keyword | Meaning |
| --- | --- |
| `let` | Variable declaration |
| `show` | Intended to display a value |
| `if` | Conditional |
| `else` | Else condition |
| `yes` | Boolean value |
| `no` | Boolean value |

The scanner reads the whole word before checking if it is a keyword. Because of this, `let` is a keyword but `letter` is an identifier.

### Operators and Punctuation

Quill supports these operators:

`+  -  *  /  =  ==  !  !=  >  >=  <  <=`

It also supports:

`(  )  {  }  ;`

For operators like `=` and `==`, the scanner checks the next character to figure out which token it should make.

### Comments and Whitespace

I decided to use `#` for comments.

Example:

`# This is a comment`

Anything after `#` on that line is ignored.

Spaces, tabs, and carriage returns are ignored. Newlines are not tokens, but I still keep track of them so errors can show the correct line number.

## Differences From Lox

I used the Lox scanner from *Crafting Interpreters* as a reference, but I changed parts of it for Quill.

Some differences are:

- My language is called Quill and uses `.quill` files.
- I use `let` for variable declarations.
- I use `show` as a keyword.
- I use `yes` and `no` instead of Lox's boolean keywords.
- Comments start with `#`.
- I only included the keywords and tokens I wanted Quill to have.

The basic scanning process is still similar to Lox because the scanner reads through the source and turns lexemes into tokens.

## Running Quill

I wrote Quill in Python 3.

To scan a file, I run:

`python src/quill.py test/lab1/test1.quill`

To use interactive mode, I run:

`python src/quill.py`

This opens the:

`Quill Interactive Shell`

I can then type Quill code after the `>` prompt. Ctrl+C exits the shell.

# Scanner Tests

I put my test files in `test/lab1/`. I made separate tests for the different types of tokens, errors, and some edge cases.

## Test 1: Basic Program

**Purpose:** Test a simple Quill program with keywords, a variable, assignment, a string, and semicolons.

**Source:**

```text
let book = "The Hunger Games";
show book;
```

**Expected:** `let` and `show` should be recognized as keywords. `book` should be an identifier, `"The Hunger Games"` should be a string, and the other symbols should get their correct tokens.

**Actual:**

```text
LET let None
IDENTIFIER book None
EQUAL = None
STRING "The Hunger Games" The Hunger Games
SEMICOLON ; None
SHOW show None
IDENTIFIER book None
SEMICOLON ; None
EOF  None
```

**Match:** Yes. The basic program was scanned correctly.

## Test 2: Operators and Punctuation

**Purpose:** Test all of the operators and punctuation I added to Quill.

**Source:**

```text
+ - * /
= == ! !=
> >= < <=
( ) { } ;
```

**Expected:** Each symbol should get the correct token. I also wanted to make sure things like `=` and `==` are treated as different tokens.

**Actual:**

```text
PLUS + None
MINUS - None
STAR * None
SLASH / None
EQUAL = None
EQUAL_EQUAL == None
BANG ! None
BANG_EQUAL != None
GREATER > None
GREATER_EQUAL >= None
LESS < None
LESS_EQUAL <= None
LEFT_PAREN ( None
RIGHT_PAREN ) None
LEFT_BRACE { None
RIGHT_BRACE } None
SEMICOLON ; None
EOF  None
```

**Match:** Yes. All of the operators and punctuation came out correctly.

## Test 3: Keywords and Identifiers

**Purpose:** Test all of my keywords and a few different identifier names.

**Source:**

```text
let show if else yes no
book book2 favorite_book _score
```

**Expected:** `let`, `show`, `if`, `else`, `yes`, and `no` should be keywords. The other names should be identifiers.

**Actual:**

```text
LET let None
SHOW show None
IF if None
ELSE else None
YES yes None
NO no None
IDENTIFIER book None
IDENTIFIER book2 None
IDENTIFIER favorite_book None
IDENTIFIER _score None
EOF  None
```

**Match:** Yes. The keywords and identifiers were recognized correctly.

## Test 4: Numbers

**Purpose:** Test whole numbers, decimals, a large number, and a negative number.

**Source:**

```text
0
95
3.14
100.25
42
22
10000000
5656
-122
```

**Expected:** All of the numbers should get `NUMBER` tokens. For `-122`, I expect `-` and `122` to be separate tokens.

**Actual:**

```text
NUMBER 0 0.0
NUMBER 95 95.0
NUMBER 3.14 3.14
NUMBER 100.25 100.25
NUMBER 42 42.0
NUMBER 22 22.0
NUMBER 10000000 10000000.0
NUMBER 5656 5656.0
MINUS - None
NUMBER 122 122.0
EOF  None
```

**Match:** Yes. The numbers worked the way I expected.

## Test 5: Strings, Comments, and Whitespace

**Purpose:** Test strings and make sure comments and extra whitespace are ignored.

**Source:**

```text
show "hello";

# This is a comment and should be ignored
show "The Hunger Games";

let author = "Suzanne Collins";
# Another comment
show author;
```

**Expected:** The strings should get `STRING` tokens. The comments and blank lines should not make any tokens.

**Actual:**

```text
SHOW show None
STRING "hello" hello
SEMICOLON ; None
SHOW show None
STRING "The Hunger Games" The Hunger Games
SEMICOLON ; None
LET let None
IDENTIFIER author None
EQUAL = None
STRING "Suzanne Collins" Suzanne Collins
SEMICOLON ; None
SHOW show None
IDENTIFIER author None
SEMICOLON ; None
EOF  None
```

**Match:** Yes. The strings worked and the comments and whitespace were ignored.

## Test 6: Unexpected Characters

**Purpose:** See what happens when Quill finds characters that are not part of the language.

**Source:**

```text
let book = "Quill";
@
$
show book;
```

**Expected:** `@` should give an error on line 2 and `$` should give an error on line 3. Quill should still scan the code after the errors.

**Actual:**

```text
Error on line 2: Unexpected character: @
Error on line 3: Unexpected character: $
LET let None
IDENTIFIER book None
EQUAL = None
STRING "Quill" Quill
SEMICOLON ; None
SHOW show None
IDENTIFIER book None
SEMICOLON ; None
EOF  None
```

**Match:** Yes. Both errors showed the correct line and the rest of the file was still scanned.

## Test 7: Unterminated String

**Purpose:** Test a string that is missing its ending quote.

**Source:**

```text
show "This string never ends
```

**Expected:** Quill should give an unterminated string error on line 1.

**Actual:**

```text
Error on line 1: Unterminated string.
SHOW show None
EOF  None
```

**Match:** Yes. Quill caught the error on the correct line.

## Test 8: Edge Cases

**Purpose:** Test a few cases that could cause problems, like an identifier starting with a keyword, `_` in an identifier, and an empty string.

**Source:**

```text
let letter = 0;
let book2 = 3.14;
let _score = 100;
show "";
show "hello world";
```

**Expected:** `letter`, `book2`, and `_score` should all be identifiers. The empty string and `"hello world"` should also work.

**Actual:**

```text
LET let None
IDENTIFIER letter None
EQUAL = None
NUMBER 0 0.0
SEMICOLON ; None
LET let None
IDENTIFIER book2 None
EQUAL = None
NUMBER 3.14 3.14
SEMICOLON ; None
LET let None
IDENTIFIER _score None
EQUAL = None
NUMBER 100 100.0
SEMICOLON ; None
SHOW show None
STRING ""
SEMICOLON ; None
SHOW show None
STRING "hello world" hello world
SEMICOLON ; None
EOF  None
```

**Match:** Yes. Everything was scanned the way I expected.

## Interactive Mode Test

I also tested the interactive shell to make sure it still works after an error.

I started it using:

`python src/quill.py`

First, I entered:

```text
let score = 95;
```

The result was:

```text
LET let None
IDENTIFIER score None
EQUAL = None
NUMBER 95 95.0
SEMICOLON ; None
EOF  None
```

Then I entered an invalid character:

```text
@
```

Quill gave:

```text
Error on line 1: Unexpected character: @
EOF  None
```

The shell stayed open after the error. I then entered:

```text
show "hello";
```

The result was:

```text
SHOW show None
STRING "hello" hello
SEMICOLON ; None
EOF  None
```

This showed that an error does not close the interactive shell and I can keep entering Quill code afterward.

# Known Limitations

Right now Quill is only a scanner, so it does not actually run the code. It only creates tokens.

Some other things I did not add are:

- Scientific notation for numbers
- Escape characters in strings
- Block or nested comments
- Syntax checking

These were not part of the lexical rules I chose for Quill.

## AI Use

I used AI to help format and organize this report. The code, testing, and language design were created, reviewed, and tested by me.