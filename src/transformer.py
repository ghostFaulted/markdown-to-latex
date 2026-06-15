import sys
import os
from lark import Transformer

# Ensure local module visibility on all operating systems
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ast_nodes import (
    DocumentNode, HeaderNode, UnorderedListNode, 
    ListItemNode, ParagraphNode, TextNode, BoldNode, ItalicNode
)

# Class representing the post-order AST generator from Lark's Parse Tree
class MarkdownTransformer(Transformer):
    def document(self, children):
        # Clean document children, ignoring none-values produced by blank lines
        blocks = [c for c in children if c is not None]
        return DocumentNode(blocks)

    def blank_line(self, args):
        # Ignore empty lines entirely during transformation
        return None

    def header1(self, args):
        # Map header 1 rule contents to HeaderNode
        return HeaderNode(1, args[0])

    def header2(self, args):
        # Map header 2 rule contents to HeaderNode
        return HeaderNode(2, args[0])

    def list_item(self, args):
        # List item bullet is discarded in grammar, args[0] is inline text
        return ListItemNode(args[0])

    def unordered_list(self, items):
        # Collect multiple list items into an UnorderedListNode
        return UnorderedListNode(items)

    def paragraph(self, args):
        # Map inline texts within paragraph rules to ParagraphNode
        return ParagraphNode(args[0])

    def inline_text(self, elements):
        # Return list of formatted or plain inline nodes
        return elements

    def bold(self, args):
        # Wrap content token into TextNode, then wrap in BoldNode
        text_val = str(args[0])
        return BoldNode(TextNode(text_val))

    def italic(self, args):
        # Wrap content token into TextNode, then wrap in ItalicNode
        text_val = str(args[0])
        return ItalicNode(TextNode(text_val))

    def plain_text(self, args):
        # Map a standard plaintext token to TextNode
        text_val = str(args[0])
        return TextNode(text_val)