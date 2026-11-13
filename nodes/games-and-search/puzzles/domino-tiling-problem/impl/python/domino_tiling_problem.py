# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/domino-tiling-problem/. The authors are listed in prov/YTYE25.jsonl.
"""Domino tilings of grid regions: decision by matching, counting by three methods.

A region is a set of (row, col) cells. A domino covers two cells that share a
side. A tiling covers every cell of the region exactly once.
"""

import math
from fractions import Fraction


def rectangle(m, n):
    """The cells of the m by n board."""
    return {(r, c) for r in range(m) for c in range(n)}


def colour_balance(region):
    """Number of black cells minus number of white cells, black when row + col is even."""
    return sum(1 if (r + c) % 2 == 0 else -1 for r, c in region)


def count_region(region):
    """Count the tilings of any finite region, cell by cell in row-major order.

    The state is the set of cells, among the next `width` cells in row-major
    order, that are already covered by a vertical domino from the row above.
    """
    if not region:
        return 1
    rows = [r for r, _ in region]
    cols = [c for _, c in region]
    r0, c0 = min(rows), min(cols)
    h, w = max(rows) - r0 + 1, max(cols) - c0 + 1
    inside = [[(r + r0, c + c0) in region for c in range(w)] for r in range(h)]
    ways = {0: 1}
    for r in range(h):
        for c in range(w):
            new = {}
            for mask, k in ways.items():
                covered = mask & 1
                rest = mask >> 1
                if not inside[r][c]:
                    if covered:
                        continue
                    new[rest] = new.get(rest, 0) + k
                    continue
                if covered:
                    new[rest] = new.get(rest, 0) + k
                    continue
                # vertical domino down to (r + 1, c)
                if r + 1 < h and inside[r + 1][c]:
                    key = rest | 1 << (w - 1)
                    new[key] = new.get(key, 0) + k
                # horizontal domino right to (r, c + 1)
                if c + 1 < w and inside[r][c + 1] and not rest & 1:
                    new[rest | 1] = new.get(rest | 1, 0) + k
            ways = new
    return ways.get(0, 0)


def count_transfer(m, n):
    """Count the tilings of the m by n board with a column-by-column transfer matrix."""
    if (m * n) % 2:
        return 0
    ways = {0: 1}
    for _ in range(n):
        new = {}

        def fill(row, cur, nxt, k):
            if row == m:
                new[nxt] = new.get(nxt, 0) + k
            elif cur >> row & 1:
                fill(row + 1, cur, nxt, k)
            else:
                fill(row + 1, cur | 1 << row, nxt | 1 << row, k)
                if row + 1 < m and not cur >> (row + 1) & 1:
                    fill(row + 2, cur | 3 << row, nxt, k)

        for mask, k in ways.items():
            fill(0, mask, 0, k)
        ways = new
    return ways.get(0, 0)


def kasteleyn_product(m, n):
    """The product formula of Kasteleyn and of Temperley and Fisher, in floating point."""
    p = 1.0
    for j in range(1, (m + 1) // 2 + 1):
        for k in range(1, (n + 1) // 2 + 1):
            p *= 4 * math.cos(math.pi * j / (m + 1)) ** 2 + 4 * math.cos(math.pi * k / (n + 1)) ** 2
    return p


def determinant(a):
    """Exact determinant of a square matrix of Fractions by Gaussian elimination."""
    a = [row[:] for row in a]
    size = len(a)
    det = Fraction(1)
    for i in range(size):
        p = next((r for r in range(i, size) if a[r][i] != 0), None)
        if p is None:
            return Fraction(0)
        if p != i:
            a[i], a[p] = a[p], a[i]
            det = -det
        det *= a[i][i]
        for r in range(i + 1, size):
            f = a[r][i] / a[i][i]
            if f:
                for c in range(i, size):
                    a[r][c] -= f * a[i][c]
    return det


def kasteleyn_matrix(region):
    """Signed biadjacency matrix: rows are black cells, columns are white cells.

    A horizontal edge gets +1; a vertical edge gets (-1) ** col. Every unit
    square then has an odd number of minus signs, the Kasteleyn condition for
    faces of length 4 in a bipartite plane graph.
    """
    black = sorted(x for x in region if sum(x) % 2 == 0)
    white = sorted(x for x in region if sum(x) % 2 == 1)
    col = {x: i for i, x in enumerate(white)}
    mat = [[Fraction(0)] * len(white) for _ in black]
    for i, (r, c) in enumerate(black):
        for (dr, dc) in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            y = (r + dr, c + dc)
            if y in col:
                mat[i][col[y]] = Fraction(1) if dr == 0 else Fraction((-1) ** c)
    return mat


def count_kasteleyn(region):
    """Count tilings of a simply connected region as |det| of the Kasteleyn matrix."""
    black = sum(1 for x in region if sum(x) % 2 == 0)
    if 2 * black != len(region):
        return 0
    if not region:
        return 1
    return abs(int(determinant(kasteleyn_matrix(region))))


def has_tiling(region):
    """Decide tilability by a maximum bipartite matching (augmenting paths)."""
    black = [x for x in region if sum(x) % 2 == 0]
    if 2 * len(black) != len(region):
        return False
    match = {}

    def augment(b, seen):
        r, c = b
        for y in ((r, c + 1), (r, c - 1), (r + 1, c), (r - 1, c)):
            if y in region and y not in seen:
                seen.add(y)
                if y not in match or augment(match[y], seen):
                    match[y] = b
                    return True
        return False

    return all(augment(b, set()) for b in black)


def brute_force(region):
    """Count tilings by covering the first free cell in every possible way."""
    free = set(region)

    def rec():
        if not free:
            return 1
        r, c = min(free)
        free.discard((r, c))
        total = 0
        for y in ((r, c + 1), (r + 1, c)):
            if y in free:
                free.discard(y)
                total += rec()
                free.add(y)
        free.add((r, c))
        return total

    return rec()
