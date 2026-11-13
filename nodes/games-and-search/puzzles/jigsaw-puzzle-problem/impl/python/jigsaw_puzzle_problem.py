# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jigsaw-puzzle-problem/. The authors are listed in prov/9JN0A4.jsonl.
"""Jigsaw puzzles as signed edge matching, with pieces in a fixed orientation.

A piece is (top, right, bottom, left), each an integer edge label. Label 0 is
a flat border edge. Two pieces fit along an edge when the labels are x and -x:
a tab of shape x meets a blank of shape x. A solution places all pieces in an
m by n rectangle with flat edges on the border and fitting edges inside.
"""

import random

TOP, RIGHT, BOTTOM, LEFT = range(4)


def make_puzzle(m, n, shapes, rng):
    """A random m by n puzzle with edge shapes 1..shapes; returns (pieces, solution grid).

    The returned pieces are shuffled; grid[r][c] is the index of the piece at (r, c).
    """
    horiz = [[rng.randint(1, shapes) * rng.choice((1, -1)) for _ in range(n - 1)] for _ in range(m)]
    vert = [[rng.randint(1, shapes) * rng.choice((1, -1)) for _ in range(n)] for _ in range(m - 1)]
    pieces = []
    for r in range(m):
        for c in range(n):
            top = -vert[r - 1][c] if r > 0 else 0
            bottom = vert[r][c] if r < m - 1 else 0
            left = -horiz[r][c - 1] if c > 0 else 0
            right = horiz[r][c] if c < n - 1 else 0
            pieces.append((top, right, bottom, left))
    order = list(range(m * n))
    rng.shuffle(order)
    shuffled = [pieces[i] for i in order]
    where = {old: new for new, old in enumerate(order)}
    grid = [[where[r * n + c] for c in range(n)] for r in range(m)]
    return shuffled, grid


def is_solution(pieces, grid):
    m, n = len(grid), len(grid[0])
    if sorted(x for row in grid for x in row) != list(range(len(pieces))):
        return False
    for r in range(m):
        for c in range(n):
            p = pieces[grid[r][c]]
            if (p[TOP] == 0) != (r == 0) or (p[LEFT] == 0) != (c == 0):
                return False
            if (p[BOTTOM] == 0) != (r == m - 1) or (p[RIGHT] == 0) != (c == n - 1):
                return False
            if c > 0 and pieces[grid[r][c - 1]][RIGHT] != -p[LEFT]:
                return False
            if r > 0 and pieces[grid[r - 1][c]][BOTTOM] != -p[TOP]:
                return False
    return True


def count_solutions(pieces, m, n, limit=None):
    """Backtracking in row-major order: try every unused piece that fits its left and top neighbors."""
    used = [False] * len(pieces)
    grid = [[None] * n for _ in range(m)]
    count = 0

    def place(k):
        nonlocal count
        if k == m * n:
            count += 1
            return limit is not None and count >= limit
        r, c = divmod(k, n)
        for i, p in enumerate(pieces):
            if used[i]:
                continue
            if (p[TOP] == 0) != (r == 0) or (p[LEFT] == 0) != (c == 0):
                continue
            if (p[BOTTOM] == 0) != (r == m - 1) or (p[RIGHT] == 0) != (c == n - 1):
                continue
            if c > 0 and pieces[grid[r][c - 1]][RIGHT] != -p[LEFT]:
                continue
            if r > 0 and pieces[grid[r - 1][c]][BOTTOM] != -p[TOP]:
                continue
            used[i] = True
            grid[r][c] = i
            if place(k + 1):
                return True
            used[i] = False
        return False

    place(0)
    return count


def has_unique_matches(pieces):
    """True when every inner edge shape occurs on exactly one tab and one blank."""
    seen = {}
    for p in pieces:
        for x in p:
            if x:
                seen[x] = seen.get(x, 0) + 1
    return all(seen.get(x, 0) == 1 and seen.get(-x, 0) == 1 for x in seen)


def assemble_unique(pieces, m, n):
    """Linear-time assembly when matches are unique: each piece is found from its neighbor by a table.

    Start from the one piece with flat top and left edges, then for each place
    look up the only piece whose left (or top) edge fits.
    """
    by_left, by_top = {}, {}
    corner = None
    for i, p in enumerate(pieces):
        if p[LEFT]:
            by_left[p[LEFT]] = i
        if p[TOP]:
            by_top[p[TOP]] = i
        if p[TOP] == 0 and p[LEFT] == 0:
            corner = i
    grid = [[None] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            if r == 0 and c == 0:
                grid[r][c] = corner
            elif c > 0:
                grid[r][c] = by_left.get(-pieces[grid[r][c - 1]][RIGHT])
            else:
                grid[r][c] = by_top.get(-pieces[grid[r - 1][c]][BOTTOM])
            if grid[r][c] is None:
                return None
    return grid if is_solution(pieces, grid) else None


def random_instance(seed, m, n, shapes):
    return make_puzzle(m, n, shapes, random.Random(seed))
