# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tetris-legalization/. The authors are listed in prov/M7HMAC.jsonl.

"""Tetris legalization, the greedy method of Hill's patent in its common textbook form.

Rows r = 0 .. K-1 lie at y = r * row_height and hold the sites x = 0 .. S-1 of width 1.
Cell i has an integer width w[i] and a global position (xg[i], yg[i]) of its lower left corner.
Each row keeps a frontier: the right end of its last placed cell. A placed cell never moves.
The cost of a candidate is the Manhattan movement |x - xg| + |y - yg|, computed exactly.
"""

from fractions import Fraction
from math import floor


def nearest_site(v) -> int:
    """The site nearest to v; a tie goes to the left."""
    return -floor(-Fraction(v) + Fraction(1, 2))


def tetris(xg, yg, w, num_rows: int, sites: int, row_height=1):
    """Return (x, y) with integer site positions and row heights, or raise ValueError
    when some cell fits after the frontier of no row."""
    n = len(xg)
    frontier = [0] * num_rows
    x = [0] * n
    y = [0] * n
    order = sorted(range(n), key=lambda i: (Fraction(xg[i]), i))  # @line L1
    for i in order:  # @line L2
        best = None
        for r in range(num_rows):  # @line L3
            want = min(max(nearest_site(xg[i]), 0), sites - w[i])  # @line L4
            pos = max(frontier[r], want)  # @line L5
            if pos + w[i] > sites:  # @line L6
                continue
            cost = abs(pos - Fraction(xg[i])) + abs(Fraction(r * row_height) - Fraction(yg[i]))  # @line L7
            if best is None or cost < best[0]:
                best = (cost, r, pos)
        if best is None:
            raise ValueError(f"cell {i} fits in no row")  # @line L8
        _, r, pos = best
        x[i], y[i] = pos, r * row_height  # @line L9
        frontier[r] = pos + w[i]  # @line L10
    return x, y


def displacement(x, y, xg, yg) -> Fraction:
    """Total Manhattan movement."""
    return sum(abs(Fraction(a) - Fraction(b)) + abs(Fraction(c) - Fraction(d)) for a, b, c, d in zip(x, xg, y, yg))
