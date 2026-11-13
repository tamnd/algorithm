# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knights-tour-problem/. The authors are listed in prov/C2A3S2.jsonl.
"""Knight's tours on m by n boards: validity, exhaustive existence and counting.

A square is a pair (row, col). An open tour visits every square once by knight
moves. A closed tour is an open tour whose last square is a knight move from
its first square.
"""

MOVES = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def is_knight_move(a, b):
    return {abs(a[0] - b[0]), abs(a[1] - b[1])} == {1, 2}


def is_tour(m, n, path, closed=False):
    """True when path is an open (or closed) knight's tour of the m by n board."""
    if len(path) != m * n or set(path) != {(r, c) for r in range(m) for c in range(n)}:
        return False
    if any(not is_knight_move(path[i], path[i + 1]) for i in range(len(path) - 1)):
        return False
    return not closed or m * n == 1 or is_knight_move(path[-1], path[0])


def neighbours(m, n):
    adj = []
    for r in range(m):
        for c in range(n):
            adj.append([(r + dr) * n + c + dc for dr, dc in MOVES if 0 <= r + dr < m and 0 <= c + dc < n])
    return adj


def find_tour(m, n, closed=False):
    """Exhaustive depth-first search. Returns a tour as a list of squares, or None.

    The search tries the squares with fewest free neighbours first and cuts a
    branch when a free square adjacent to the current square has no free
    neighbour left and is not the last square. For a closed tour the start is
    fixed at (0, 0), since a closed tour can be rotated to start anywhere.
    """
    size = m * n
    adj = neighbours(m, n)
    seen = [False] * size
    deg = [len(a) for a in adj]
    path = []

    def dfs(v, start):
        if len(path) == size:
            return not closed or start in adj[v]
        if closed and not any(not seen[u] for u in adj[start]):
            return False
        free = [u for u in adj[v] if not seen[u]]
        for u in free:
            deg[u] -= 1
        zeros = [u for u in free if deg[u] == 0]
        found = False
        if len(zeros) <= 1:
            cand = zeros or sorted(free, key=lambda u: deg[u])
            for u in cand:
                seen[u] = True
                path.append(u)
                if dfs(u, start):
                    found = True
                    break
                path.pop()
                seen[u] = False
        for u in free:
            deg[u] += 1
        return found

    starts = [0] if closed else range(size)
    for s in starts:
        seen[s] = True
        path[:] = [s]
        if dfs(s, s):
            return [divmod(v, n) for v in path]
        seen[s] = False
    return None


def count_open_tours(m, n):
    """Count directed open tours (every start, every direction) by backtracking.

    A branch is cut when two free squares next to the current square have no
    other free neighbour: a path can end in only one of them.
    """
    size = m * n
    adj = neighbours(m, n)
    seen = [False] * size
    deg = [len(a) for a in adj]

    def rec(v, k):
        if k == size:
            return 1
        free = [u for u in adj[v] if not seen[u]]
        for u in free:
            deg[u] -= 1
        zeros = [u for u in free if deg[u] == 0]
        total = 0
        if len(zeros) <= 1:
            for u in zeros or free:
                seen[u] = True
                total += rec(u, k + 1)
                seen[u] = False
        for u in free:
            deg[u] += 1
        return total

    total = 0
    for s in range(size):
        seen[s] = True
        total += rec(s, 1)
        seen[s] = False
    return total


def schwenk_closed(m, n):
    """Schwenk (1991): does the m by n board have a closed tour?"""
    m, n = min(m, n), max(m, n)
    if m * n == 1:
        return True
    if m % 2 == 1 and n % 2 == 1:
        return False
    if m in (1, 2, 4):
        return False
    if m == 3 and n in (4, 6, 8):
        return False
    return True


def open_tour_exists_rule(m, n):
    """The classification of boards with an open tour (Conrad et al. 1994)."""
    m, n = min(m, n), max(m, n)
    if m == 1:
        return n == 1
    if m == 2:
        return False
    if m == 3:
        return n == 4 or n >= 7
    if m == 4:
        return n >= 5
    return True
