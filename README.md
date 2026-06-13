# Mini-Markdown to LaTeX Converter

A strict compiler-like translator that parses a lightweight Markdown subset and transpiles it into valid, compilable LaTeX documents. Built using Python 3 and the Lark parsing library (Earley engine).

## 1. Author
* Yaroslav Zamorskyi - Lexer design, Lark grammar specification, AST node architectures, and Error handling wrapper, transformer implementation, LaTeX code generation visitor logic, and testing suite.

## 2. Project Description
This command-line utility reads structured Markdown files, constructs an Abstract Syntax Tree (AST) using highly specialized Python classes, and generates a structured LaTeX output document. 

Supported Markdown features:
* Header 1 (`# Header`) and Header 2 (`## Header`)
* Paragraphs (separated by blank lines)
* Unordered lists (`-` or `*` markers)
* Bold (`**text**`) and Italic (`*text*`) inline formatting

## 3. Formal Grammar and Tokens
The parser implements a formal grammar classified under the Chomsky Hierarchy as a Context-Free Grammar (Type 2). This classification is guaranteed because every production rule maps a single non-terminal symbol on the left-hand side to a string of terminals and non-terminals on the right-hand side ($A \to \alpha$).

### EBNF Representation
```ebnf
?start         ::= document
document       ::= (block | blank_line)*
?block         ::= header2 | header1 | unordered_list | paragraph

header1        ::= "# " inline_text _NL
header2        ::= "## " inline_text _NL

unordered_list ::= list_item+
list_item      ::= _BULLET " " inline_text _NL
_BULLET        ::= "*" | "-"

paragraph      ::= inline_text _NL
inline_text    ::= inline_element+

?inline_element::= bold | italic | plain_text
bold           ::= "**" WORD_OR_SPACE "**"
italic         ::= "*" WORD_OR_SPACE "*"
plain_text     ::= WORD_OR_SPACE
blank_line     ::= _NL

WORD_OR_SPACE  ::= /[a-zA-Z0-9ąćęłńóśźżĄĆĘŁŃÓŚŹŻ ,.!?'-]+/
_NL            ::= /\r?\n/
```

## 4. Installation and Setup
Ensure you have Python 3.8+ installed on your system.

1. **Clone the repository and navigate to the project directory:**
   ```bash
   git clone <repository_url>
   cd markdown-to-latex
   ```

2. **Set up a virtual environment (recommended):**
   * On Windows:
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * On Linux/macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 5. Usage Examples

### Running a Successful Translation
To translate a valid Markdown file into LaTeX:
```bash
python src/main.py tests/valid_1.md
```
**Output Console message:**
`Translation successful! Output saved to: tests/valid_1.tex`

#### Generated LaTeX Sample Output:
```latex
\documentclass{article}
\usepackage[utf8]{inputenc}
\begin{document}

\section{Dokument Testowy}

To jest prosty akapit zawierajacy \textbf{pogrubienie} oraz \textit{kursywe}.

\begin{itemize}
  \item Pierwszy element listy
  \item Drugi element listy
\end{itemize}

\end{document}
```

### Error Handling Demonstration
To run the parser on a file containing syntax violations (such as unmatched inline tags):
```bash
python src/main.py tests/invalid_1.md
```
**Console Output (Syntax Error Catch):**
```text
Syntax Error: Unexpected token 'None' at line 3, column 23.
Context details:

Akapit zawierajacy **niezamkniety tag pogrubienia.
                      ^
```
```