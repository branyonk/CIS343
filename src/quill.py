import sys
from scanner import Scanner

def run(source):
    """Scan the source code and print each token."""
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(f"{token.token_type} {token.lexeme} {token.literal}")


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