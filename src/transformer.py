import sys
import os
from lark import Transformer

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ast_nodes import (
    DocumentNode, HeaderNode, UnorderedListNode, 
    ListItemNode, ParagraphNode, TextNode, BoldNode, ItalicNode
)

class MarkdownTransformer(Transformer):
    def document(self, blocks):
        return DocumentNode(blocks)

    def header1(self, args):
        return HeaderNode(1, args[0])

    def header2(self, args):
        return HeaderNode(2, args[0])

    def list_item(self, args):
        return ListItemNode(args[0])

    def unordered_list(self, items):
        return UnorderedListNode(items)

    def paragraph(self, args):
        return ParagraphNode(args[0])

    def inline_text(self, elements):
        return elements

    def bold(self, args):
        text_val = str(args[0])
        return BoldNode(TextNode(text_val))

    def italic(self, args):
        text_val = str(args[0])
        return ItalicNode(TextNode(text_val))

    def plain_text(self, args):
        text_val = str(args[0])
        return TextNode(text_val)