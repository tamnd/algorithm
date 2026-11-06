# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pratt-parsing/. The authors are listed in prov/G9PZT9.jsonl.

"""Pratt parsing (top-down operator precedence) with binding powers.

Operators are given by three tables:
  prefix[t]  = rbp          a prefix operator t and the binding power of its operand
  infix[t]   = (lbp, rbp)   a binary operator; rbp = lbp for left, lbp - 1 for right associativity
  postfix[t] = lbp          a postfix operator
A token may be prefix and infix (like "-"), but not both infix and postfix.
"(" and ")" group, "$" is reserved, and every other token is an operand.
Each lbp is at least 1 and each rbp at least 0.

Trees: an operand is the token itself; ("()", e) is a group, ("pre", t, e),
("post", t, e) and ("in", t, l, r) are operator nodes.

EXPR(rbp) is a Python generator: a recursive call is `yield rbp`, answered by
the driver with the subtree, so deep nesting does not use the Python stack.
"""

from typing import Generator, Mapping, Sequence

END = "$"


class ParseError(ValueError):
    """The token sequence is not a well-formed expression."""


class PrattParser:
    def __init__(
        self,
        prefix: Mapping[str, int],
        infix: Mapping[str, tuple[int, int]],
        postfix: Mapping[str, int],
    ) -> None:
        if set(infix) & set(postfix):
            raise ValueError("a token cannot be both infix and postfix")
        special = {"(", ")", END}
        if special & (set(prefix) | set(infix) | set(postfix)):
            raise ValueError("parentheses and $ are not operators")
        if any(l < 1 for l, _ in infix.values()) or any(l < 1 for l in postfix.values()):
            raise ValueError("left binding powers must be at least 1")
        if any(r < 0 for _, r in infix.values()) or any(r < 0 for r in prefix.values()):
            raise ValueError("right binding powers must be at least 0")
        self.prefix = dict(prefix)
        self.infix = dict(infix)
        self.postfix = dict(postfix)

    def lbp(self, t: str) -> int:
        if t in self.infix:
            return self.infix[t][0]
        return self.postfix.get(t, 0)  # 0 for ")", "$", operands and prefix-only tokens

    def is_operand(self, t: str) -> bool:
        return t not in ("(", ")", END) and t not in self.prefix and t not in self.infix and t not in self.postfix

    def parse(self, tokens: Sequence[str]):
        """Return the expression tree of tokens, or raise ParseError."""
        toks = list(tokens) + [END]
        if END in toks[:-1]:
            raise ParseError("$ is reserved")
        pos = 0

        def expr(rbp: int) -> Generator[int, object, object]:
            nonlocal pos
            t = toks[pos]  # @line L4
            pos += 1
            if self.is_operand(t):  # @line L5
                left = t
            elif t == "(":  # @line L6
                inner = yield 0
                if toks[pos] != ")":
                    raise ParseError(f"expected ')' at {pos}, found {toks[pos]!r}")
                pos += 1
                left = ("()", inner)
            elif t in self.prefix:  # @line L7
                left = ("pre", t, (yield self.prefix[t]))
            else:  # @line L8
                raise ParseError(f"expected an operand at {pos - 1}, found {t!r}")
            while self.lbp(toks[pos]) > rbp:  # @line L9
                o = toks[pos]  # @line L10
                pos += 1
                if o in self.postfix:  # @line L11
                    left = ("post", o, left)
                else:  # @line L12
                    left = ("in", o, left, (yield self.infix[o][1]))
            return left  # @line L13

        stack = [expr(0)]  # @line L1
        value = None
        result = None
        while stack:
            try:
                rbp = stack[-1].send(value)
            except StopIteration as done:
                stack.pop()
                value = result = done.value
                continue
            stack.append(expr(rbp))
            value = None
        if toks[pos] != END:  # @line L2
            raise ParseError(f"unexpected {toks[pos]!r} at {pos}")
        return result  # @line L3

    def recognize(self, tokens: Sequence[str]) -> bool:
        try:
            self.parse(tokens)
        except ParseError:
            return False
        return True


def leaves(tree) -> list[str]:
    """The tokens of a tree, from left to right (iterative)."""
    out: list[str] = []
    stack = [tree]
    while stack:
        t = stack.pop()
        if isinstance(t, str):
            out.append(t)
        elif t[0] == "()":
            stack.extend([")", t[1], "("])
        elif t[0] == "pre":
            stack.extend([t[2], t[1]])
        elif t[0] == "post":
            stack.extend([t[1], t[2]])
        else:
            stack.extend([t[3], t[1], t[2]])
    return out
