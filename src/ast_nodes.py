from typing import List

class ASTNode:
    def to_latex(self) -> str:
        raise NotImplementedError()

class InlineNode(ASTNode):
    pass

class TextNode(InlineNode):
    def __init__(self, text: str):
        self.text = text

    def to_latex(self) -> str:
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

class BoldNode(InlineNode):
    def __init__(self, content: TextNode):
        self.content = content

    def to_latex(self) -> str:
        return f"\\textbf{{{self.content.to_latex()}}}"

class ItalicNode(InlineNode):
    def __init__(self, content: TextNode):
        self.content = content

    def to_latex(self) -> str:
        return f"\\textit{{{self.content.to_latex()}}}"

class BlockNode(ASTNode):
    pass

class HeaderNode(BlockNode):
    def __init__(self, level: int, content: List[InlineNode]):
        self.level = level
        self.content = content

    def to_latex(self) -> str:
        command = "section" if self.level == 1 else "subsection"
        inner_text = "".join(node.to_latex() for node in self.content)
        return f"\\{command}{{{inner_text}}}\n"

class ListItemNode(ASTNode):
    def __init__(self, content: List[InlineNode]):
        self.content = content

    def to_latex(self) -> str:
        inner_text = "".join(node.to_latex() for node in self.content)
        return f"  \\item {inner_text}\n"

class UnorderedListNode(BlockNode):
    def __init__(self, items: List[ListItemNode]):
        self.items = items

    def to_latex(self) -> str:
        latex_items = "".join(item.to_latex() for item in self.items)
        return f"\\begin{{itemize}}\n{latex_items}\\end{{itemize}}\n"

class ParagraphNode(BlockNode):
    def __init__(self, content: List[InlineNode]):
        self.content = content

    def to_latex(self) -> str:
        inner_text = "".join(node.to_latex() for node in self.content)
        return f"{inner_text}\n\n"

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