# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tp1-tp2-conditions/. The authors are listed in prov/21VA27.jsonl.

"""Checkers for the transformation properties TP1 and TP2 on string operations.

Operations are ("ins", p, ch, uid), ("del", p) and ("nop",), with 0-based
positions. A transform T(a, b) returns a to run after b, when a and b were made
on the same state.

TP1: for a and b on the same state s, s.a.T(b, a) = s.b.T(a, b).
TP2: for a, b and c on the same state, T(c, a then T(b, a)) equals
T(c, b then T(a, b)), where T(c, x then y) = T(T(c, x), y).

The search walks small documents and operations in a fixed order and returns
the first counterexample, so the result is reproducible.
"""

import itertools
from collections.abc import Callable, Iterator

Op = tuple
Transform = Callable[[Op, Op], Op]


def apply(doc: str, op: Op) -> str:
    if op[0] == "ins":
        return doc[: op[1]] + op[2] + doc[op[1]:]
    if op[0] == "del":
        return doc[: op[1]] + doc[op[1] + 1:]
    return doc


def _rest(a: Op, b: Op) -> Op:
    """The cases shared by both transforms below: insert against delete, and deletes."""
    if a[0] == "ins":
        return a if a[1] <= b[1] else ("ins", a[1] - 1, a[2], a[3])
    if b[0] == "ins":
        return a if a[1] < b[1] else ("del", a[1] + 1)
    if a[1] < b[1]:
        return a
    if a[1] > b[1]:
        return ("del", a[1] - 1)
    return ("nop",)


def naive(a: Op, b: Op) -> Op:
    """Positions only: an insert moves right when the other insert is at or before it."""
    if a[0] == "nop" or b[0] == "nop":
        return a
    if a[0] == "ins" and b[0] == "ins":
        return a if a[1] < b[1] else ("ins", a[1] + 1, a[2], a[3])
    return _rest(a, b)


def ressel(a: Op, b: Op) -> Op:
    """As naive, but two inserts at one position are ordered by uid (Ressel et al. 1996)."""
    if a[0] == "nop" or b[0] == "nop":
        return a
    if a[0] == "ins" and b[0] == "ins":
        if a[1] < b[1] or (a[1] == b[1] and a[3] < b[3]):
            return a
        return ("ins", a[1] + 1, a[2], a[3])
    return _rest(a, b)


def tp1_holds(t: Transform, doc: str, a: Op, b: Op) -> bool:
    return apply(apply(doc, a), t(b, a)) == apply(apply(doc, b), t(a, b))  # @line L1


def tp2_holds(t: Transform, a: Op, b: Op, c: Op) -> bool:
    left = t(t(c, a), t(b, a))  # @line L2
    right = t(t(c, b), t(a, b))  # @line L3
    return left == right  # @line L4


def ops(doc: str, uid: int, ch: str) -> Iterator[Op]:
    for p in range(len(doc) + 1):
        yield ("ins", p, ch, uid)
    for p in range(len(doc)):
        yield ("del", p)


def docs(max_len: int, alphabet: str = "ab") -> Iterator[str]:
    for length in range(max_len + 1):
        yield from map("".join, itertools.product(alphabet, repeat=length))


def find_tp1(t: Transform, max_len: int = 3):
    for doc in docs(max_len):
        for a in ops(doc, 1, "x"):
            for b in ops(doc, 2, "y"):
                if not tp1_holds(t, doc, a, b):
                    return doc, a, b
    return None


def find_tp2(t: Transform, max_len: int = 3, visible: bool = False):
    """The first TP2 counterexample. With visible=True, the two results must differ as text."""
    for doc in docs(max_len):
        for a in ops(doc, 1, "x"):
            for b in ops(doc, 2, "y"):
                for c in ops(doc, 3, "z"):
                    if tp2_holds(t, a, b, c):
                        continue
                    s = apply(apply(doc, a), t(b, a))
                    left = apply(s, t(t(c, a), t(b, a)))
                    right = apply(apply(apply(doc, b), t(a, b)), t(t(c, b), t(a, b)))
                    if not visible or left != right:
                        return doc, a, b, c, left, right
    return None
