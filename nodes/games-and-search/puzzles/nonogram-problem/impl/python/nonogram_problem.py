# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonogram-problem/. The authors are listed in prov/EV9FYH.jsonl.
"""Nonogram solver: an exact line solver and a full solver with branching.

A cell is 1 (filled), 0 (empty) or -1 (unknown). A clue is a list of block
lengths, all positive; the empty list means an empty line.

line_solve finds, for one line, the value of each cell over all fillings that
match the clue and the known cells. It runs an automaton for the pattern
0* 1^b1 0+ 1^b2 ... 0+ 1^bk 0* forward and backward over the line, in
O(L (B + k)) time for a line of length L and clue sum B.
"""


def clue_of(line):
    """The block lengths of a fully known line."""
    out = []
    run = 0
    for v in line:
        if v == 1:
            run += 1
        elif run:
            out.append(run)
            run = 0
    if run:
        out.append(run)
    return out


def _pattern(clue):
    """States as (symbol, loops) pairs, plus the start and accepting states."""
    states = [(0, True)]
    for i, b in enumerate(clue):
        states.extend([(1, False)] * b)
        if i + 1 < len(clue):
            # One looping gap state: it must be passed, so the gap has at least one cell.
            states.append((0, True))
    if clue:
        states.append((0, True))
        start = {0, 1}
        accept = {len(states) - 2, len(states) - 1}
    else:
        start = {0}
        accept = {0}
    return states, start, accept


def line_solve(clue, line):
    """Refine a line: return the list of forced values (-1 where both occur), or None.

    None means that no filling of the line matches the clue.
    """
    n = len(line)
    if n == 0:
        return [] if not clue else None
    states, start, accept = _pattern(clue)  # @line L1
    count = len(states)

    def succ(s):
        out = [s + 1] if s + 1 < count else []
        if states[s][1]:
            out.append(s)
        return out

    def allowed(s, i):
        return line[i] == -1 or line[i] == states[s][0]

    forward = [set() for _ in range(n)]
    forward[0] = {s for s in start if allowed(s, 0)}  # @line L2
    for i in range(1, n):
        cur = set()
        for s in forward[i - 1]:
            for t in succ(s):
                if allowed(t, i):
                    cur.add(t)
        forward[i] = cur  # @line L3
    backward = [set() for _ in range(n)]
    backward[n - 1] = {s for s in range(count) if s in accept and allowed(s, n - 1)}  # @line L4
    for i in range(n - 2, -1, -1):
        backward[i] = {s for s in range(count)
                       if allowed(s, i) and any(t in backward[i + 1] for t in succ(s))}  # @line L5
    result = []
    for i in range(n):
        values = {states[s][0] for s in forward[i] & backward[i]}  # @line L6
        if not values:
            return None  # @line L7
        result.append(values.pop() if len(values) == 1 else -1)  # @line L8
    return result  # @line L9


def propagate(rows, cols, grid):
    """Line solve all rows and columns until nothing changes. False on a contradiction."""
    h, w = len(rows), len(cols)
    dirty_rows = set(range(h))
    dirty_cols = set(range(w))
    while dirty_rows or dirty_cols:
        while dirty_rows:
            r = dirty_rows.pop()
            new = line_solve(rows[r], grid[r])
            if new is None:
                return False
            for c in range(w):
                if new[c] != grid[r][c]:
                    grid[r][c] = new[c]
                    dirty_cols.add(c)
        while dirty_cols:
            c = dirty_cols.pop()
            col = [grid[r][c] for r in range(h)]
            new = line_solve(cols[c], col)
            if new is None:
                return False
            for r in range(h):
                if new[r] != grid[r][c]:
                    grid[r][c] = new[r]
                    dirty_rows.add(r)
    return True


def line_solver_only(rows, cols):
    """The grid that line solving alone reaches from an empty grid, or None."""
    grid = [[-1] * len(cols) for _ in rows]
    return grid if propagate(rows, cols, grid) else None


def solve(rows, cols, limit=None):
    """All solutions: line propagation, then a branch on an unknown cell.

    The stack holds partial grids, so the depth of the search does not use the
    Python call stack.
    """
    h, w = len(rows), len(cols)
    out = []
    stack = [[[-1] * w for _ in range(h)]]
    while stack:
        grid = stack.pop()
        if not propagate(rows, cols, grid):
            continue
        unknown = next(((r, c) for r in range(h) for c in range(w) if grid[r][c] == -1), None)
        if unknown is None:
            out.append(grid)
            if limit is not None and len(out) >= limit:
                break
            continue
        r, c = unknown
        for v in (0, 1):
            child = [list(row) for row in grid]
            child[r][c] = v
            stack.append(child)
    return out
