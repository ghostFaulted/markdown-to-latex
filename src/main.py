import sys
import os

# Force the local directory to be in the search path for clean module imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from lark import Lark, exceptions
from transformer import MarkdownTransformer

def main():
    # Ensure correct command-line arguments are provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_markdown_file.md>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    # Read the Lark grammar file
    grammar_path = os.path.join(os.path.dirname(__file__), "grammar.lark")
    try:
        with open(grammar_path, "r", encoding="utf-8") as g_file:
            grammar = g_file.read()
    except IOError as e:
        print(f"Error: Could not read grammar file. Details: {e}")
        sys.exit(1)

    # Instantiate Lark parser using the Earley parsing algorithm
    parser = Lark(grammar, parser="earley", start="document")

    # Read the input Markdown file
    try:
        with open(filepath, "r", encoding="utf-8") as md_file:
            content = md_file.read()
    except IOError as e:
        print(f"Error: Could not read input file. Details: {e}")
        sys.exit(1)

    # Append newline if missing to guarantee correct line terminal parsing
    if not content.endswith("\n"):
        content += "\n"

    try:
        # Parse input and generate the concrete parse tree
        parse_tree = parser.parse(content)

        # Transform concrete parse tree into custom AST nodes
        transformer = MarkdownTransformer()
        ast = transformer.transform(parse_tree)

        # Generate LaTeX markup from AST
        latex_output = ast.to_latex()

        # Save the compiled LaTeX markup to output file
        output_filepath = os.path.splitext(filepath)[0] + ".tex"
        with open(output_filepath, "w", encoding="utf-8") as tex_file:
            tex_file.write(latex_output)

        print(f"Translation successful! Output saved to: {output_filepath}")

    # Catch and format syntactic exceptions
    except exceptions.UnexpectedToken as e:
        print(f"Syntax Error: Unexpected token '{e.token}' at line {e.line}, column {e.column}.")
        print("Context details:")
        print(e.get_context(content))
        sys.exit(1)
    # Catch and format lexical exceptions
    except exceptions.UnexpectedCharacters as e:
        print(f"Lexical Error: Unexpected characters at line {e.line}, column {e.column}.")
        sys.exit(1)
    # Catch other parser engine runtime exceptions
    except exceptions.LarkError as e:
        print(f"Parser Error: An error occurred during parsing. Details: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()