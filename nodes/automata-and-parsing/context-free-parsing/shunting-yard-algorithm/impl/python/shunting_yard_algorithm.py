# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shunting-yard-algorithm/. The authors are listed in prov/2TMV07.jsonl.

"""Dijkstra's shunting-yard algorithm: infix tokens to postfix tokens.

A token is a string. "(" and ")" are parentheses, a key of the operator
table is a binary operator, and any other token is an operand. The operator
table maps each operator to (precedence, associativity), where a larger
precedence binds tighter and associativity is "left" or "right". All
operators of one precedence level must have the same associativity.
"""

from typing import Mapping, Sequence

DEFAULT_OPS: dict[str, tuple[int, str]] = {
    "+": (1, "left"),
    "-": (1, "left"),
    "*": (2, "left"),
    "/": (2, "left"),
    "^": (3, "right"),
}


def _pops(top: tuple[int, str], t: tuple[int, str]) -> bool:
    """True when the operator on the stack must be output before t is pushed."""
    return top[0] > t[0] or (top[0] == t[0] and t[1] == "left")


def shunting_yard(tokens: Sequence[str], ops: Mapping[str, tuple[int, str]] = DEFAULT_OPS) -> list[str]:
    """Return the postfix form of the infix expression `tokens`.

    Raises ValueError when the input is not a well-formed infix expression
    (unbalanced parentheses, two operands or two operators in a row, an
    operator at the start or the end, or an empty expression).
    Time and extra space Theta(n) for n tokens: each token is pushed and
    popped at most once.
    """
    out: list[str] = []
    stack: list[str] = []  # @line L1
    expect_operand = True  # the input check: operands and operators alternate
    for t in tokens:  # @line L2
        if t == "(":
            if not expect_operand:
                raise ValueError("an operand or '(' cannot follow an operand")
            stack.append(t)  # @line L4
        elif t == ")":  # @line L5
            if expect_operand:
                raise ValueError("')' must follow an operand")
            while stack and stack[-1] != "(":  # @line L6
                out.append(stack.pop())
            if not stack:
                raise ValueError("unbalanced ')'")
            stack.pop()  # @line L7
        elif t in ops:  # @line L8
            if expect_operand:
                raise ValueError(f"operator {t!r} needs a left operand")
            p = ops[t]
            while stack and stack[-1] != "(" and _pops(ops[stack[-1]], p):  # @line L9
                out.append(stack.pop())  # @line L10
            stack.append(t)  # @line L11
            expect_operand = True
        else:
            if not expect_operand:
                raise ValueError("two operands in a row")
            out.append(t)  # @line L3
            expect_operand = False
    if expect_operand:
        raise ValueError("the expression is empty or ends with an operator")
    while stack:  # @line L12
        if stack[-1] == "(":  # @line L13
            raise ValueError("unbalanced '('")
        out.append(stack.pop())  # @line L14
    return out  # @line L15


def evaluate_postfix(postfix: Sequence[str], ops: Mapping[str, tuple[int, str]] = DEFAULT_OPS) -> object:
    """Build the expression tree of a postfix sequence as nested tuples (op, left, right)."""
    st: list[object] = []
    for t in postfix:
        if t in ops:
            b, a = st.pop(), st.pop()
            st.append((t, a, b))
        else:
            st.append(t)
    if len(st) != 1:
        raise ValueError("not a postfix expression")
    return st[0]
