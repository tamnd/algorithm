# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/newick-format/. The authors are listed in prov/TR7EXK.jsonl.

"""A Newick parser and printer.

The grammar follows Felsenstein's description of the 1986 standard and
Gary Olsen's 1990 interpretation of it:

    tree      ::= subtree ";"
    subtree   ::= leaf | "(" subtree ("," subtree)* ")" [label]  , both with [":" length]
    leaf      ::= [label]

Unquoted labels may not hold blanks, parentheses, square brackets, single
quotes, colons, semicolons or commas, and an underscore in them stands for a
blank. A quoted label is written between single quotes, and a single quote
inside it is written twice. Comments are in square brackets and may appear
between any two tokens. Both the parser and the printer use explicit stacks,
so a deep tree does not hit the recursion limit of Python.
"""

from __future__ import annotations

from typing import Optional

PUNCT = "()[]':;,"
WHITESPACE = " \t\r\n"


class Node:
    """A tree node: a label (possibly empty), an optional branch length, and children in order."""

    __slots__ = ("label", "length", "children")

    def __init__(self, label: str = "", length: Optional[float] = None, children: Optional[list["Node"]] = None):
        self.label = label
        self.length = length
        self.children = children if children is not None else []

    def is_leaf(self) -> bool:
        return not self.children

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        stack = [(self, other)]
        while stack:
            a, b = stack.pop()
            if a.label != b.label or a.length != b.length or len(a.children) != len(b.children):
                return False
            stack.extend(zip(a.children, b.children))
        return True

    def __repr__(self) -> str:
        return f"Node({to_newick(self)!r})"


def leaves(root: Node) -> list[str]:
    """The labels of the leaves, from left to right."""
    out = []
    stack = [root]
    while stack:
        v = stack.pop()
        if v.is_leaf():
            out.append(v.label)
        else:
            stack.extend(reversed(v.children))
    return out


class _Lexer:
    def __init__(self, text: str):
        self.text = text
        self.i = 0

    def skip(self) -> None:
        """Skip blanks and bracketed comments."""
        t = self.text
        while self.i < len(t):
            c = t[self.i]
            if c in WHITESPACE:
                self.i += 1
            elif c == "[":
                end = t.find("]", self.i + 1)
                if end < 0:
                    raise ValueError(f"unclosed comment at offset {self.i}")
                self.i = end + 1
            else:
                return

    def peek(self) -> str:
        self.skip()
        return self.text[self.i] if self.i < len(self.text) else ""

    def word(self) -> str:
        """Read an unquoted word: a run of characters that are not punctuation or blanks."""
        t = self.text
        j = self.i
        while j < len(t) and t[j] not in PUNCT and t[j] not in WHITESPACE:
            j += 1
        w = t[self.i:j]
        self.i = j
        return w

    def quoted(self) -> str:
        """Read a quoted label. The opening quote is at self.i."""
        t = self.text
        j = self.i + 1
        out = []
        while True:
            k = t.find("'", j)
            if k < 0:
                raise ValueError(f"unclosed quoted label at offset {self.i}")
            out.append(t[j:k])
            if k + 1 < len(t) and t[k + 1] == "'":
                out.append("'")
                j = k + 2
            else:
                self.i = k + 1
                return "".join(out)


# The state of the current node: what may still follow.
_FRESH, _CLOSED, _LABELED, _HAS_LENGTH = 0, 1, 2, 3


def parse(text: str) -> Node:
    """Parse one Newick tree that ends with a semicolon. Raise ValueError on bad input."""
    lx = _Lexer(text)
    root = Node()
    cur = root
    state = _FRESH
    stack: list[Node] = []  # the open ancestors of cur
    while True:
        c = lx.peek()
        if c == "":
            raise ValueError("missing ';' at the end of the tree")
        if c == "(":
            if state != _FRESH:
                raise ValueError(f"unexpected '(' at offset {lx.i}")
            lx.i += 1
            stack.append(cur)
            cur = Node()
            stack[-1].children.append(cur)
        elif c == ",":
            if not stack:
                raise ValueError(f"',' outside parentheses at offset {lx.i}")
            lx.i += 1
            cur = Node()
            stack[-1].children.append(cur)
            state = _FRESH
        elif c == ")":
            if not stack:
                raise ValueError(f"unbalanced ')' at offset {lx.i}")
            lx.i += 1
            cur = stack.pop()
            state = _CLOSED
        elif c == ":":
            if state == _HAS_LENGTH:
                raise ValueError(f"second branch length at offset {lx.i}")
            lx.i += 1
            lx.skip()
            w = lx.word()
            try:
                cur.length = float(w)
            except ValueError:
                raise ValueError(f"bad branch length {w!r}") from None
            state = _HAS_LENGTH
        elif c == ";":
            if stack:
                raise ValueError("unbalanced '(' at the end of the tree")
            lx.i += 1
            if lx.peek() != "":
                raise ValueError(f"text after ';' at offset {lx.i}")
            return root
        else:
            if state in (_LABELED, _HAS_LENGTH):
                raise ValueError(f"unexpected label at offset {lx.i}")
            if c == "'":
                cur.label = lx.quoted()
            elif c in PUNCT:
                raise ValueError(f"unexpected {c!r} at offset {lx.i}")
            else:
                cur.label = lx.word().replace("_", " ")
            state = _LABELED


def format_label(label: str) -> str:
    """Write a label so that parse() reads it back unchanged."""
    if label == "":
        return ""
    if any(ch in PUNCT or ch in "_\t\r\n" for ch in label):
        return "'" + label.replace("'", "''") + "'"
    return label.replace(" ", "_")


def to_newick(root: Node) -> str:
    """Print the tree in Newick format, with the trailing semicolon."""
    out: list[str] = []
    # Each stack item is (node, True) to open the node, or (node, False) to close it.
    stack: list[tuple[Node, bool]] = [(root, True)]
    while stack:
        v, opening = stack.pop()
        if v is None:
            out.append(",")
            continue
        if opening and v.children:
            out.append("(")
            stack.append((v, False))
            for k in range(len(v.children) - 1, -1, -1):
                stack.append((v.children[k], True))
                if k > 0:
                    stack.append((None, True))  # type: ignore[arg-type]  # a comma marker
            continue
        if not opening:
            out.append(")")
        out.append(format_label(v.label))
        if v.length is not None:
            out.append(":" + repr(v.length))
    out.append(";")
    return "".join(out)
