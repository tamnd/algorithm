# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sudoku/. The authors are listed in prov/5N96QY.jsonl.
"""Sudoku of order n: an n^2 by n^2 grid with n by n boxes.

A grid is a list of rows. A cell holds 0 when it is empty, else a symbol in 1..n^2.
Two solvers: an exact cover model searched by Algorithm X, and a backtracking
search with candidate sets and the fewest-candidates rule. The module also has
the reduction from partial Latin square completion of order n to Sudoku of
order n (Yato and Seta).
"""


def box_of(n, r, c):
    """Index of the n by n box that holds cell (r, c)."""
    return n * (r // n) + c // n


def is_complete_solution(n, grid):
    """True when every row, column and box holds each symbol 1..n^2 once."""
    size = n * n
    full = set(range(1, size + 1))
    for r in range(size):
        if set(grid[r]) != full:
            return False
    for c in range(size):
        if {grid[r][c] for r in range(size)} != full:
            return False
    for b in range(size):
        r0, c0 = n * (b // n), n * (b % n)
        cells = {grid[r0 + i][c0 + j] for i in range(n) for j in range(n)}
        if cells != full:
            return False
    return True


def exact_cover_model(n, grid):
    """Return (items, options) of the exact cover form of a Sudoku instance.

    The items are ("cell", r, c), ("row", r, v), ("col", c, v) and ("box", b, v),
    4 N^2 in all for N = n^2. An option (r, c, v) covers four items. A given
    cell keeps only its own option, and an empty cell drops the symbols that a
    given cell of its row, column or box already uses.
    """
    size = n * n
    row_used = [set() for _ in range(size)]
    col_used = [set() for _ in range(size)]
    box_used = [set() for _ in range(size)]
    for r in range(size):
        for c in range(size):
            v = grid[r][c]
            if v:
                row_used[r].add(v)
                col_used[c].add(v)
                box_used[box_of(n, r, c)].add(v)
    items = []
    for r in range(size):
        for c in range(size):
            items.append(("cell", r, c))
    for kind in ("row", "col", "box"):
        for i in range(size):
            for v in range(1, size + 1):
                items.append((kind, i, v))
    options = {}
    for r in range(size):
        for c in range(size):
            b = box_of(n, r, c)
            if grid[r][c]:
                values = [grid[r][c]]
            else:
                values = [v for v in range(1, size + 1)
                          if v not in row_used[r] and v not in col_used[c] and v not in box_used[b]]
            for v in values:
                options[(r, c, v)] = (("cell", r, c), ("row", r, v), ("col", c, v), ("box", b, v))
    return items, options


def algorithm_x(items, options, limit=None):
    """All exact covers of the items by the options (Knuth's Algorithm X).

    items is a list of primary items. options maps a name to the items it covers.
    The search branches on an item with the fewest live options. The recursion
    depth is at most the number of options in one cover.
    """
    cols = {i: set() for i in items}
    for name, its in options.items():
        for i in its:
            cols[i].add(name)
    solutions = []
    partial = []

    def cover(name):
        removed = []
        for i in options[name]:
            for other in cols[i]:
                for j in options[other]:
                    if j != i:
                        cols[j].discard(other)
            removed.append(cols.pop(i))
        return removed

    def uncover(name, removed):
        for i in reversed(options[name]):
            cols[i] = removed.pop()
            for other in cols[i]:
                for j in options[other]:
                    if j != i:
                        cols[j].add(other)

    def search():
        if limit is not None and len(solutions) >= limit:
            return
        if not cols:
            solutions.append(list(partial))
            return
        item = min(cols, key=lambda i: len(cols[i]))
        for name in sorted(cols[item]):
            partial.append(name)
            removed = cover(name)
            search()
            uncover(name, removed)
            partial.pop()
            if limit is not None and len(solutions) >= limit:
                return

    search()
    return solutions


def solve_exact_cover(n, grid, limit=None):
    """All completions of the grid, found as exact covers."""
    items, options = exact_cover_model(n, grid)
    size = n * n
    result = []
    for cover in algorithm_x(items, options, limit):
        g = [[0] * size for _ in range(size)]
        for r, c, v in cover:
            g[r][c] = v
        result.append(g)
    return result


def solve_backtracking(n, grid, limit=None):
    """All completions of the grid by backtracking with candidate sets.

    The search keeps the used symbols of each row, column and box as bit masks.
    At each node it fills the empty cell with the fewest candidates.
    """
    size = n * n
    full = (1 << (size + 1)) - 2
    g = [list(row) for row in grid]
    rows = [0] * size
    cols = [0] * size
    boxes = [0] * size
    empty = []
    for r in range(size):
        for c in range(size):
            v = g[r][c]
            if v:
                bit = 1 << v
                b = box_of(n, r, c)
                if rows[r] & bit or cols[c] & bit or boxes[b] & bit:
                    return []
                rows[r] |= bit
                cols[c] |= bit
                boxes[b] |= bit
            else:
                empty.append((r, c, box_of(n, r, c)))  # @line L1
    solutions = []

    def search(k):
        if limit is not None and len(solutions) >= limit:
            return
        if k == len(empty):  # @line L2
            solutions.append([list(row) for row in g])
            return
        best = -1
        best_count = size + 1
        best_mask = 0
        for idx in range(k, len(empty)):
            r, c, b = empty[idx]
            mask = full & ~(rows[r] | cols[c] | boxes[b])  # @line L3
            count = bin(mask).count("1")
            if count < best_count:  # @line L4
                best, best_count, best_mask = idx, count, mask
                if count <= 1:
                    break
        if best_count == 0:  # @line L5
            return
        empty[k], empty[best] = empty[best], empty[k]
        r, c, b = empty[k]
        mask = best_mask
        while mask:  # @line L6
            bit = mask & -mask
            mask ^= bit
            g[r][c] = bit.bit_length() - 1  # @line L7
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            search(k + 1)  # @line L8
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[b] ^= bit
            g[r][c] = 0  # @line L9
            if limit is not None and len(solutions) >= limit:
                break
        empty[k], empty[best] = empty[best], empty[k]

    search(0)
    return solutions


def latin_to_sudoku(partial):
    """Map a partial Latin square of order n to a Sudoku instance of order n.

    partial is an n by n array with entries in 0..n-1 or None. The Sudoku grid
    has side n^2. With 0-based symbols, cell (i, j) holds
    ((i mod n) n + floor(i / n) + j) mod n^2, except the cells with i < n and
    j a multiple of n. Those cells form a copy of the Latin square: cell
    (i, k n) holds n L(i, k) when L(i, k) is given and is empty otherwise.
    The returned grid uses symbols 1..n^2 (the 0-based value plus 1).
    """
    n = len(partial)
    size = n * n
    grid = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i < n and j % n == 0:
                v = partial[i][j // n]
                grid[i][j] = 0 if v is None else n * v + 1
            else:
                grid[i][j] = ((i % n) * n + i // n + j) % size + 1
    return grid


def sudoku_to_latin(n, grid):
    """Read the Latin square of order n back from a solved reduction grid."""
    return [[(grid[i][k * n] - 1) // n for k in range(n)] for i in range(n)]
