# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bcnf-decomposition/. The authors are listed in prov/F3CVSY.jsonl.
"""BCNF decomposition: split a schema on a violating FD until every part is in BCNF.

Attributes are strings and attribute sets are frozensets. An FD X -> Y is a pair (X, Y).
The result is a list of attribute sets whose natural join is lossless for every relation
that satisfies the FDs. It may not preserve the FDs.
"""

from itertools import combinations

FD = tuple[frozenset, frozenset]


def closure(x: frozenset, fds: list[FD]) -> frozenset:
    """Return X+ under fds by the fixpoint of the attribute closure algorithm."""
    result = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= result and not rhs <= result:
                result |= rhs
                changed = True
    return frozenset(result)


def find_violation(s: frozenset, fds: list[FD]) -> tuple[frozenset, frozenset] | None:
    """Find X inside S with X -> A for some A in S - X, and X not a superkey of S.

    Returns (X, Y) with Y = (X+ & S) - X, for the first such X in order of size, then name.
    The search tries every subset of S, so it costs 2^|S| closures in the worst case.
    """
    attrs = sorted(s)
    for size in range(len(attrs)):
        for xs in combinations(attrs, size):
            x = frozenset(xs)
            c = closure(x, fds)
            y = (c & s) - x
            if y and not s <= c:
                return x, y
    return None


def bcnf_decomposition(r: frozenset, fds: list[FD]) -> list[frozenset]:
    """Decompose R into BCNF schemas.

    Precondition: the FDs use only attributes of R.
    Cost: the split tree has depth below |R|, so it has fewer than 2^|R| nodes; the test of a
    part S costs up to 2^|S| closures. The stack holds at most |R| parts.
    """
    done: list[frozenset] = []
    todo = [frozenset(r)]  # @line L1
    while todo:  # @line L2
        s = todo.pop()  # @line L3
        v = find_violation(s, fds)  # @line L4
        if v is None:  # @line L5
            done.append(s)  # @line L6
            continue
        x, y = v  # @line L7
        todo.append(s - y)  # @line L8
        todo.append(x | y)  # @line L8
    return done  # @line L9


def bcnf_decomposition_poly(r: frozenset, fds: list[FD]) -> list[frozenset]:
    """A polynomial-time variant with the pair test.

    If a part Y is not in BCNF, then some A, B in Y have A in (Y - A - B)+. So when no pair
    passes this test, Y is in BCNF. The loop removes such B until Y is in BCNF; the last A
    found satisfies Y - A -> A, so Z splits losslessly into Y and Z - A.
    Cost: O(n^4) closures for n = |R| attributes.
    """
    out: list[frozenset] = []
    z = frozenset(r)
    while True:
        y = z
        last_a = None
        found = True
        while found:
            found = False
            for a in sorted(y):
                for b in sorted(y - {a}):
                    if a in closure(y - {a, b}, fds):
                        y = y - {b}
                        last_a = a
                        found = True
                        break
                if found:
                    break
        if last_a is None:
            out.append(z)
            return out
        out.append(y)
        z = z - {last_a}
