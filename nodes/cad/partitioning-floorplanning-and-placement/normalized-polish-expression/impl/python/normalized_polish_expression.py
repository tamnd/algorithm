# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/normalized-polish-expression/. The authors are listed in prov/77DCRE.jsonl.

"""Normalized Polish expressions of slicing floorplans (Wong and Liu, 1986).

A token is an operand (a block, any int) or an operator, the string "H" or
"V". The convention of this module:

- ``a b V``: a is to the left of b (a vertical cut line). The width is the sum
  of the widths and the height is the larger height.
- ``a b H``: a is below b (a horizontal cut line). The width is the larger
  width and the height is the sum of the heights.

A Polish expression is the postorder of a slicing tree. It is normalized if no
two equal operators are next to each other. Normalized expressions and skewed
slicing trees (no right child with the operator of its parent) are in one to
one correspondence.
"""

from typing import Union

Token = Union[int, str]
Tree = Union[int, tuple]  # a leaf is an int, a node is (op, left, right)
OPERATORS = ("H", "V")


def is_operator(t: Token) -> bool:
    """Return True if t is one of the cut operators "H" and "V"."""
    return t == "H" or t == "V"


def is_normalized(tokens: list[Token], blocks: set[int] | None = None) -> bool:
    """Return True if tokens is a normalized Polish expression.

    If blocks is given, the operands must be exactly these blocks, each one
    time. Otherwise each operand must occur one time.
    """
    operands = [t for t in tokens if not is_operator(t)]
    n = len(operands)
    if n == 0 or len(tokens) != 2 * n - 1 or len(set(operands)) != n:  # @line L1
        return False
    if blocks is not None and set(operands) != set(blocks):
        return False
    c = 0  # @line L2
    for k, t in enumerate(tokens):  # @line L3
        if not is_operator(t):  # @line L4
            c += 1
        else:  # @line L5
            c -= 1  # @line L6
            if c < 1 or tokens[k - 1] == t:  # @line L7
                return False
    return True  # @line L8


def _build(tokens: list[Token], sizes: dict[int, tuple[int, int]] | None) -> list:
    """Build the slicing tree of a Polish expression with a stack.

    A node is a list [op, left, right, width, height]; a leaf is
    [block, None, None, width, height]. Sizes may be None (then 0 by 0).
    """
    stack: list[list] = []  # @line L9
    for t in tokens:  # @line L10
        if not is_operator(t):  # @line L11
            w, h = sizes[t] if sizes is not None else (0, 0)
            stack.append([t, None, None, w, h])
        else:
            if len(stack) < 2:
                raise ValueError("not a Polish expression")
            b = stack.pop()  # @line L12
            a = stack.pop()
            if t == "V":  # @line L13
                w, h = a[3] + b[3], max(a[4], b[4])
            else:  # @line L14
                w, h = max(a[3], b[3]), a[4] + b[4]
            stack.append([t, a, b, w, h])  # @line L15
    if len(stack) != 1:
        raise ValueError("not a Polish expression")
    return stack[0]


class NormalizedPolishExpression:
    """A normalized Polish expression, stored as a list of tokens."""

    def __init__(self, tokens: list[Token]) -> None:
        """Store a copy of tokens. Raise ValueError if they are not normalized."""
        if not is_normalized(tokens):
            raise ValueError("not a normalized Polish expression")
        self.tokens: list[Token] = list(tokens)

    def check_invariant(self) -> None:
        """Raise AssertionError if the stored word is not normalized."""
        assert is_normalized(self.tokens)

    def blocks(self) -> list[int]:
        """Return the operands in the order of the word."""
        return [t for t in self.tokens if not is_operator(t)]

    def evaluate(
        self, sizes: dict[int, tuple[int, int]]
    ) -> tuple[int, int, dict[int, tuple[int, int]]]:
        """Return (W, H, pos): the size of the floorplan and the lower-left corner of each block.

        sizes[b] = (w, h). Each block sits at the lower-left corner of its room.
        Time O(n).
        """
        root = _build(self.tokens, sizes)
        pos: dict[int, tuple[int, int]] = {}
        todo = [(root, 0, 0)]  # @line L16
        while todo:
            t, x, y = todo.pop()
            if t[1] is None:  # @line L18
                pos[t[0]] = (x, y)
                continue
            a, b = t[1], t[2]
            todo.append((a, x, y))  # @line L19
            if t[0] == "V":  # @line L20
                todo.append((b, x + a[3], y))
            else:
                todo.append((b, x, y + a[4]))
        return root[3], root[4], pos  # @line L17

    def to_tree(self) -> Tree:
        """Return the skewed slicing tree as nested tuples (op, left, right)."""
        return _as_tuple(_build(self.tokens, None))

    @staticmethod
    def normalize(tokens: list[Token]) -> "NormalizedPolishExpression":
        """Return the normalized expression of the floorplan of any Polish expression.

        Each maximal chain of equal operators is rebuilt as a left-deep chain,
        which keeps the left to right (or bottom to top) order of its parts, so
        the floorplan does not change. Time O(n).
        """
        root = _build(tokens, None)  # @line L21
        out: list[Token] = []
        work: list = [("emit", root)]  # @line L22
        while work:
            kind, t = work.pop()
            if kind == "op":
                out.append(t)
                continue
            if t[1] is None:  # @line L23
                out.append(t[0])
                continue
            o = t[0]
            parts: list = []  # @line L24
            chain = [t]
            while chain:
                u = chain.pop()
                if u[1] is not None and u[0] == o:
                    chain.append(u[2])
                    chain.append(u[1])
                else:
                    parts.append(u)
            seq: list = [("emit", parts[0]), ("emit", parts[1]), ("op", o)]  # @line L25
            for p in parts[2:]:
                seq.append(("emit", p))
                seq.append(("op", o))
            work.extend(reversed(seq))
        return NormalizedPolishExpression(out)

    @staticmethod
    def from_tree(tree: Tree) -> "NormalizedPolishExpression":
        """Return the normalized expression of the floorplan of a slicing tree."""
        return NormalizedPolishExpression.normalize(postorder(tree))


def _as_tuple(t: list) -> Tree:
    """Turn the list nodes of _build into nested tuples."""
    if t[1] is None:
        return t[0]
    return (t[0], _as_tuple(t[1]), _as_tuple(t[2]))


def postorder(tree: Tree) -> list[Token]:
    """Return the postorder word (Polish expression) of a slicing tree."""
    if not isinstance(tree, tuple):
        return [tree]
    op, a, b = tree
    return postorder(a) + postorder(b) + [op]
