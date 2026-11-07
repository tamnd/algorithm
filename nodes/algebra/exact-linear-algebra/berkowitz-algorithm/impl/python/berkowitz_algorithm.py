# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berkowitz-algorithm/. The authors are listed in prov/PM8CKR.jsonl.

from typing import Any, Sequence


def berkowitz(a: Sequence[Sequence[Any]], one: Any = 1) -> list[Any]:
    """Return the coefficients of det(xI - a), highest degree first, for a square matrix a.

    Uses only addition, subtraction and multiplication, so it works over every commutative ring
    (ints, residues modulo a composite number, polynomials, ...). `one` is the ring's unit.
    Cost: about n^4/2 ring operations.
    """
    n = len(a)
    if n == 0:  # @line L1
        return [one]
    p = [one, -a[n - 1][n - 1]]  # @line L2
    for r in range(n - 2, -1, -1):  # @line L3
        s = n - r - 1  # @line L4
        q = [one, -a[r][r]]  # @line L5
        v = list(a[r][r + 1:])
        for k in range(s):  # @line L6
            g = v[0] * a[r + 1][r]
            for t in range(1, s):
                g = g + v[t] * a[r + 1 + t][r]
            q.append(-g)  # @line L7
            if k < s - 1:  # @line L8
                w = []
                for c in range(s):
                    acc = v[0] * a[r + 1][r + 1 + c]
                    for t in range(1, s):
                        acc = acc + v[t] * a[r + 1 + t][r + 1 + c]
                    w.append(acc)
                v = w
        new = []
        for i in range(s + 2):  # @line L9
            acc = None
            for k in range(max(0, i - s - 1), min(i, s) + 1):
                term = q[i - k] * p[k]
                acc = term if acc is None else acc + term
            new.append(acc)
        p = new
    return p  # @line L10


def berkowitz_determinant(a: Sequence[Sequence[Any]], one: Any = 1) -> Any:
    """Return det a over a commutative ring, as (-1)^n times the constant coefficient."""
    c0 = berkowitz(a, one)[-1]
    return c0 if len(a) % 2 == 0 else -c0
