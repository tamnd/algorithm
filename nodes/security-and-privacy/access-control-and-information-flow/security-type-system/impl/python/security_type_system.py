# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/security-type-system/. The authors are listed in prov/8RQ898.jsonl.

"""The Volpano-Irvine-Smith security type system for a small while language.

Programs are nested tuples:

    expression: an int (a constant), a str (a variable), or (op, e1, e2)
                with op one of "+", "-", "*", "<", "=="
    command:    ("skip",)
                ("assign", x, e)
                ("seq", c1, c2)
                ("if", e, c1, c2)
                ("while", e, c)

A security level is a frozenset of category names, ordered by inclusion.
The empty set is the bottom level L (public). The two-point lattice is
L = frozenset() <= H = frozenset({"h"}). Join is set union.
"""

from typing import Union

Level = frozenset
Expr = Union[int, str, tuple]
Cmd = tuple

BOTTOM: Level = frozenset()


def expr_level(e: Expr, gamma: dict[str, Level]) -> Level:
    """Return the join of the levels of the variables in e (BOTTOM if none).

    Precondition: every variable of e is a key of gamma.
    Cost: O(size of e) joins. Uses an explicit stack, no recursion.
    """
    level: Level = BOTTOM
    stack: list[Expr] = [e]
    while stack:
        f = stack.pop()
        if isinstance(f, bool) or isinstance(f, int):
            continue
        if isinstance(f, str):
            level = level | gamma[f]
        else:
            stack.append(f[1])
            stack.append(f[2])
    return level


def typecheck(c: Cmd, gamma: dict[str, Level], pc: Level = BOTTOM) -> bool:
    """Return True if c is typable under the variable levels gamma at program counter pc.

    The rules are those of Volpano, Irvine and Smith in the program counter
    form: x := e needs level(e) join pc <= gamma(x); a branch or a loop on e
    checks its body at pc join level(e). Typable programs are
    termination-insensitive noninterferent.
    Precondition: every variable of c is a key of gamma.
    Cost: O(n) lattice operations for a program of n syntax nodes, and O(n)
    extra space for the explicit stack.
    """
    stack: list[tuple[Cmd, Level]] = [(c, pc)]  # @line L1
    while stack:  # @line L2
        d, p = stack.pop()  # @line L3
        tag = d[0]
        if tag == "skip":  # @line L4
            continue
        if tag == "assign":  # @line L5
            if not (expr_level(d[2], gamma) | p) <= gamma[d[1]]:  # @line L6
                return False
        elif tag == "seq":  # @line L7
            stack.append((d[2], p))
            stack.append((d[1], p))
        elif tag == "if":  # @line L8
            q = p | expr_level(d[1], gamma)  # @line L9
            stack.append((d[3], q))
            stack.append((d[2], q))
        elif tag == "while":  # @line L10
            stack.append((d[2], p | expr_level(d[1], gamma)))
        else:
            raise ValueError(f"unknown command {tag!r}")
    return True  # @line L11
