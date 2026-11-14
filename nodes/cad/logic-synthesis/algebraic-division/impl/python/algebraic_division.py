# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/algebraic-division/. The authors are listed in prov/NKSP1R.jsonl.

"""Weak (algebraic) division of a sum of products by another one.

A literal is the integer 2 * v + c for the variable v and c = 1 for the
complement. A cube is a frozenset of literals with at most one literal of
each variable, and a sum of products (SOP) is a frozenset of cubes. The
empty cube is the constant 1 and the empty SOP is the constant 0.

WEAK_DIVIDE(F, D) returns the quotient Q and the remainder R with
F = Q D + R as sets of cubes, where Q D is the algebraic product (the
supports of Q and D are disjoint) and Q is the largest such set of cubes.
"""

Cube = frozenset
Sop = frozenset


def parse(text: str) -> Sop:
    """Parse a string such as "ab'c + d" over the letters a to z."""
    cubes = []
    for term in text.replace(" ", "").split("+"):
        if term == "":
            continue
        lits = set()
        if term != "1":
            i = 0
            while i < len(term):
                v = ord(term[i]) - ord("a")
                c = 1 if i + 1 < len(term) and term[i + 1] == "'" else 0
                lits.add(2 * v + c)
                i += 1 + c
        cubes.append(frozenset(lits))
    return frozenset(cubes)


def show(f: Sop) -> str:
    """The SOP as a string, cubes and literals in sorted order."""
    if not f:
        return "0"

    def cube(c: Cube) -> str:
        if not c:
            return "1"
        return "".join(chr(ord("a") + (l >> 1)) + ("'" if l & 1 else "") for l in sorted(c))

    return " + ".join(sorted(cube(c) for c in f))


def support(f: Sop) -> set:
    """The variables that occur in f."""
    return {l >> 1 for c in f for l in c}


def literals(f: Sop) -> int:
    """The number of literals of f."""
    return sum(len(c) for c in f)


def weak_divide(f: Sop, d: Sop) -> tuple:
    """Return (Q, R) with f = Q d + R, Q d algebraic and Q as large as possible."""
    if not d:
        raise ZeroDivisionError("division by the constant 0")
    q = None
    for di in d:  # @line L1
        vi = {c - di for c in f if di <= c}  # @line L2
        q = vi if q is None else q & vi  # @line L3
        if not q:
            break
    qd = {qc | dc for qc in q for dc in d}  # @line L4
    r = f - qd  # @line L5
    return frozenset(q), frozenset(r)


def algebraic_product(q: Sop, d: Sop) -> Sop:
    """The product of two SOPs with disjoint supports, as a set of cubes."""
    if support(q) & support(d):
        raise ValueError("the supports are not disjoint")
    return frozenset(a | b for a in q for b in d)


def evaluate(f: Sop, point: dict) -> int:
    """The value of f at a point that maps each variable to 0 or 1."""
    for c in f:
        if all(point[l >> 1] ^ (l & 1) for l in c):
            return 1
    return 0
