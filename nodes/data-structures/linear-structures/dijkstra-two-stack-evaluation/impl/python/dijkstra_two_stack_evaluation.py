# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dijkstra-two-stack-evaluation/. The authors are listed in prov/9KN9AK.jsonl.

from fractions import Fraction
from typing import Callable

OPS: dict[str, Callable[[Fraction, Fraction], Fraction]] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def evaluate(tokens: list[str]) -> Fraction:
    """Evaluate a fully parenthesized expression given as a list of tokens.

    Tokens are "(", ")", one of + - * /, or a number. Left parentheses may
    be left out. Cost: O(n) time and O(d) space for nesting depth d.
    Precondition: the tokens form a fully parenthesized expression.
    Raises ValueError if the stacks show that the input is not well formed.
    """
    vals: list[Fraction] = []  # @line L1
    ops: list[str] = []
    for t in tokens:  # @line L2
        if t == "(":  # @line L3
            continue
        elif t in OPS:  # @line L4
            ops.append(t)
        elif t == ")":  # @line L5
            if not ops or len(vals) < 2:
                raise ValueError("unbalanced ')'")
            op, b, a = ops.pop(), vals.pop(), vals.pop()  # @line L6
            vals.append(OPS[op](a, b))  # @line L7
        else:
            vals.append(Fraction(t))  # @line L8
    if len(vals) != 1 or ops:
        raise ValueError("not a fully parenthesized expression")
    return vals.pop()  # @line L9
