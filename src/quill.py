import sys
from scanner import Scanner
from parser import Parser
from printer import AstPrinter


def run(source):
    """Scan, parse, and print the source code."""
    try:
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()
        printer = AstPrinter()
        print(printer.to_string(expression))
    except SyntaxError as error:
        print(f"Syntax Error: {error}")

def run_file(path):
    """Read and scan Quill code from a source file."""
    with open(path, "r") as file:
        source = file.read()
    run(source)

def run_prompt():
    """Run Quill in interactive terminal mode."""
    print("Quill Interactive Shell")
    while True:
        try:
            line = input("> ")
            run(line)
        except (EOFError, KeyboardInterrupt):
            print()
            break

def main():
    """Choose file mode or interactive mode based on command-line arguments."""
    if len(sys.argv) > 2:
        print("Usage: python src/quill.py [script]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()

if __name__ == "__main__":
    main()