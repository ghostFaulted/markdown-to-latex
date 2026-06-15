from typing import List

# Base class for all Abstract Syntax Tree (AST) nodes
class ASTNode:
    def to_latex(self) -> str:
        raise NotImplementedError()

# Base class for inline text elements (text, bold, italic)
class InlineNode(ASTNode):
    pass

# Node representing plain text, handles escaping of LaTeX special characters
class TextNode(InlineNode):
    def __init__(self, text: str):
        self.text = text

    def to_latex(self) -> str:
        # Escape character mapping to prevent LaTeX compilation errors
        special_chars = {
            "\\": "\\textbackslash{}",
            "&": "\\&",
            "%": "\\%",
            "$": "\\$",
            "#": "\\#",
            "_": "\\_",
            "{": "\\{",
            "}": "\\}",
            "~": "\\textasciitilde{}",
            "^": "\\textasciicircum{}"
        }
        escaped = "".join(special_chars.get(c, c) for c in self.text)
        return escaped

# Node representing bold text, wraps content in \textbf{...}
class BoldNode(InlineNode):
    def __init__(self, content: TextNode):
        self.content = content

    def to_latex(self) -> str:
        return f"\\textbf{{{self.content.to_latex()}}}"

# Node representing italic text, wraps content in \textit{...}
class ItalicNode(InlineNode):
    def __init__(self, content: TextNode):
        self.content = content

    def to_latex(self) -> str:
        return f"\\textit{{{self.content.to_latex()}}}"

# Base class for block-level elements (paragraphs, headers, lists)
class BlockNode(ASTNode):
    pass

# Node representing headings (level 1 or 2)
class HeaderNode(BlockNode):
    def __init__(self, level: int, content: List[InlineNode]):
        self.level = level
        self.content = content

    def to_latex(self) -> str:
        # Map Markdown header level to corresponding LaTeX section command
        command = "section" if self.level == 1 else "subsection"
        inner_text = "".join(node.to_latex() for node in self.content)
        return f"\\{command}{{{inner_text}}}\n"

# Node representing a single item in an unordered list
class ListItemNode(ASTNode):
    def __init__(self, content: List[InlineNode]):
        self.content = content

    def to_latex(self) -> str:
        inner_text = "".join(node.to_latex() for node in self.content)
        return f"  \\item {inner_text}\n"

# Node representing a complete unordered list container
class UnorderedListNode(BlockNode):
    def __init__(self, items: List[ListItemNode]):
        self.items = items

    def to_latex(self) -> str:
        latex_items = "".join(item.to_latex() for item in self.items)
        return f"\\begin{{itemize}}\n{latex_items}\\end{{itemize}}\n"

# Node representing a standard text paragraph
class ParagraphNode(BlockNode):
    def __init__(self, content: List[InlineNode]):
        self.content = content

    def to_latex(self) -> str:
        inner_text = "".join(node.to_latex() for node in self.content)
        return f"{inner_text}\n\n"

# Root node of the document, generates the complete LaTeX document structure
class DocumentNode(ASTNode):
    def __init__(self, blocks: List[BlockNode]):
        self.blocks = blocks

    def to_latex(self) -> str:
        body = "".join(block.to_latex() for block in self.blocks)
        return (
            "\\documentclass{article}\n"
            "\\usepackage[utf8]{inputenc}\n"
            "\\begin{document}\n\n"
            f"{body}"
            "\\end{document}\n"
        )