# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/postfix-evaluation/. The authors are listed in prov/XVTXFV.jsonl.

from collections.abc import Callable, Mapping, Sequence
from fractions import Fraction

Op = tuple[int, Callable[..., Fraction]]

DEFAULT_OPS: Mapping[str, Op] = {
    "+": (2, lambda a, b: a + b),
    "-": (2, lambda a, b: a - b),
    "*": (2, lambda a, b: a * b),
    "/": (2, lambda a, b: a / b),
    "neg": (1, lambda a: -a),
}


class MalformedExpression(ValueError):
    """The token string is not a postfix expression."""


def postfix_eval(tokens: Sequence[str], ops: Mapping[str, Op] = DEFAULT_OPS) -> Fraction:
    """Return the exact value of the postfix expression given as a list of tokens.

    A token that is a key of ops is an operator with the given arity and
    function; every other token must be an integer literal such as "12" or
    "-3". Raises MalformedExpression if the tokens are not one postfix
    expression, and ZeroDivisionError on a division by zero.
    Cost: Theta(m) stack operations for m tokens, Theta(m) extra space worst case.
    """
    s: list[Fraction] = []  # @line L1
    for tok in tokens:  # @line L2
        if tok not in ops:
            try:
                value = Fraction(int(tok))
            except ValueError:
                raise MalformedExpression(f"unknown token {tok!r}") from None
            s.append(value)  # @line L3
        else:
            k, f = ops[tok]  # @line L4
            if len(s) < k:  # @line L5
                raise MalformedExpression(f"too few operands for {tok!r}")
            y = s[len(s) - k :]  # @line L6: y[0] is the first operand, y[-1] was the top
            del s[len(s) - k :]
            s.append(f(*y))  # @line L7
    if len(s) != 1:  # @line L8
        raise MalformedExpression(f"{len(s)} values left, not one")
    return s.pop()  # @line L9


def evaluate(text: str, ops: Mapping[str, Op] = DEFAULT_OPS) -> Fraction:
    """Split text on white space and evaluate it with postfix_eval."""
    return postfix_eval(text.split(), ops)
