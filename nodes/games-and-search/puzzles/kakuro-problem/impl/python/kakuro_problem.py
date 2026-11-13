# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kakuro-problem/. The authors are listed in prov/B6JK8Y.jsonl.
"""Kakuro (Cross Sum) solver.

A board is a list of strings. "." is a white cell and any other character is a
black cell. The entries (runs) are the maximal horizontal and vertical segments
of white cells; runs(board) lists them in a fixed order, and an instance gives
one clue sum for each run. The digits are 1..max_digit (9 in the usual puzzle).

solve is a backtracking search that fills the cell with the fewest candidates.
A digit is a candidate when it is new in both runs of the cell and each run can
still reach its sum with distinct unused digits.
"""
from functools import lru_cache


def runs(board, min_length=1):
    """The runs of the board, each a tuple of (row, column) cells.

    Horizontal runs come first, in row order, then vertical runs in column order.
    """
    h, w = len(board), len(board[0])
    out = []
    for r in range(h):
        c = 0
        while c < w:
            if board[r][c] == ".":
                start = c
                while c < w and board[r][c] == ".":
                    c += 1
                if c - start >= min_length:
                    out.append(tuple((r, x) for x in range(start, c)))
            else:
                c += 1
    for c in range(w):
        r = 0
        while r < h:
            if board[r][c] == ".":
                start = r
                while r < h and board[r][c] == ".":
                    r += 1
                if r - start >= min_length:
                    out.append(tuple((y, c) for y in range(start, r)))
            else:
                r += 1
    return out


@lru_cache(maxsize=None)
def reachable(total, k, available):
    """True when some k distinct digits of the bit set available sum to total."""
    if k == 0:
        return total == 0
    if total <= 0 or available == 0:
        return False
    top = available.bit_length() - 1
    rest = available & ~(1 << top)
    return reachable(total - top, k - 1, rest) or reachable(total, k, rest)


def is_solution(board, sums, filling, max_digit=9):
    """True when the filling satisfies all runs and uses digits 1..max_digit."""
    for cells, total in zip(runs(board), sums):
        digits = [filling[cell] for cell in cells]
        if len(set(digits)) != len(digits) or sum(digits) != total:
            return False
    return all(1 <= v <= max_digit for v in filling.values())


def solve(board, sums, max_digit=9, limit=None):
    """All solutions of the instance, as dicts from cell to digit."""
    rs = runs(board)
    if len(rs) != len(sums):
        raise ValueError("one sum per run")
    cells = sorted({cell for run in rs for cell in run})
    runs_of = {cell: [] for cell in cells}
    for idx, run in enumerate(rs):
        for cell in run:
            runs_of[cell].append(idx)
    used = [0] * len(rs)
    remaining_sum = list(sums)
    remaining_cells = [len(run) for run in rs]
    all_digits = ((1 << (max_digit + 1)) - 1) & ~1
    filling = {}
    out = []
    open_cells = list(cells)

    def candidates(cell):
        result = []
        for d in range(1, max_digit + 1):
            bit = 1 << d
            ok = True
            for idx in runs_of[cell]:
                if used[idx] & bit:
                    ok = False
                    break
                free = all_digits & ~used[idx] & ~bit
                if not reachable(remaining_sum[idx] - d, remaining_cells[idx] - 1, free):
                    ok = False
                    break
            if ok:
                result.append(d)
        return result

    def search():
        if limit is not None and len(out) >= limit:
            return
        if not open_cells:  # @line L1
            out.append(dict(filling))
            return
        best, best_cands = None, None
        for cell in open_cells:
            cands = candidates(cell)  # @line L2
            if best is None or len(cands) < len(best_cands):  # @line L3
                best, best_cands = cell, cands
                if len(cands) <= 1:
                    break
        if not best_cands:
            return
        open_cells.remove(best)
        for d in best_cands:  # @line L4
            filling[best] = d  # @line L5
            for idx in runs_of[best]:
                used[idx] |= 1 << d
                remaining_sum[idx] -= d
                remaining_cells[idx] -= 1
            search()  # @line L6
            for idx in runs_of[best]:
                used[idx] &= ~(1 << d)
                remaining_sum[idx] += d
                remaining_cells[idx] += 1
            del filling[best]  # @line L7
            if limit is not None and len(out) >= limit:
                break
        open_cells.append(best)

    search()
    return out


def digit_sets(length, total, max_digit=9):
    """The sets of distinct digits of the given size and sum (the Kakuro table)."""
    out = []

    def rec(start, k, t, chosen):
        if k == 0:
            if t == 0:
                out.append(tuple(chosen))
            return
        for d in range(start, max_digit + 1):
            if d > t:
                break
            chosen.append(d)
            rec(d + 1, k - 1, t - d, chosen)
            chosen.pop()

    rec(1, length, total, [])
    return out
