# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/warnsdorff-rule/. The authors are listed in prov/6DD0YJ.jsonl.
"""Warnsdorff's rule for open knight's tours on an m by n board.

Squares are (row, col) pairs. From the current square, move to the unvisited
square with the fewest unvisited onward squares. Ties go to the first such
square in the order of `moves`. The result is the path built; it is a full
tour exactly when its length is m * n.
"""

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def warnsdorff(m, n, start=(0, 0), moves=MOVES):
    """Return the path that Warnsdorff's rule builds from start."""
    seen = [[False] * n for _ in range(m)]

    def free(r, c):
        return [(r + dr, c + dc) for dr, dc in moves
                if 0 <= r + dr < m and 0 <= c + dc < n and not seen[r + dr][c + dc]]

    r, c = start  # @line L1
    seen[r][c] = True
    path = [start]
    for _ in range(m * n - 1):  # @line L2
        cand = free(r, c)  # @line L3
        if not cand:  # @line L4
            return path
        degree = [len(free(x, y)) for x, y in cand]  # @line L5
        r, c = cand[degree.index(min(degree))]  # @line L6
        seen[r][c] = True  # @line L7
        path.append((r, c))
    return path  # @line L8


def is_tour(m, n, path):
    """True when path visits every square of the m by n board once by knight moves."""
    if len(path) != m * n or len(set(path)) != m * n:
        return False
    if any(not (0 <= r < m and 0 <= c < n) for r, c in path):
        return False
    return all({abs(a[0] - b[0]), abs(a[1] - b[1])} == {1, 2} for a, b in zip(path, path[1:]))


def open_tour_from(m, n, start):
    """Exhaustive backtracking: an open tour that starts at start, or None (reference method).

    It tries every move, fewest onward squares first, and backs up on a dead
    end, so it finds a tour whenever one exists.
    """
    size = m * n
    seen = {start}
    path = [start]

    def free(v):
        return [(v[0] + dr, v[1] + dc) for dr, dc in MOVES
                if 0 <= v[0] + dr < m and 0 <= v[1] + dc < n and (v[0] + dr, v[1] + dc) not in seen]

    def rec(v):
        if len(path) == size:
            return True
        cand = free(v)
        for u in sorted(cand, key=lambda u: len(free(u))):
            seen.add(u)
            path.append(u)
            if rec(u):
                return True
            path.pop()
            seen.discard(u)
        return False

    return path if rec(start) else None
