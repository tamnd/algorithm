# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/overmars-yap-algorithm/. The authors are listed in prov/6722KQ.jsonl.
"""Measure of a union of boxes by cell partition and trellis cells.

This is the cell-partition scheme of Overmars and Yap: split space into cells
until, inside each cell, every box either covers the cell or is a pile (it
covers the cell in all coordinates but one); the union of piles in a cell is
a trellis, whose measure has a closed form. The cut rule here is a simple
median rule (cut the coordinate depth mod d first, at the lower median of the
inner boundaries of the boxes that are not piles). It gives the same exact
answer as the Overmars-Yap partition; the O(n^(d/2) log n) time bound needs
their partition, not this rule.

A box is a tuple of d pairs (lo, hi) with lo <= hi, ints or Fractions.
"""

from math import prod


def union_length(intervals) -> int:
    total = 0
    cur_lo = cur_hi = None
    for lo, hi in sorted(intervals):
        if cur_hi is None or lo > cur_hi:
            if cur_hi is not None:
                total += cur_hi - cur_lo
            cur_lo, cur_hi = lo, hi
        elif hi > cur_hi:
            cur_hi = hi
    if cur_hi is not None:
        total += cur_hi - cur_lo
    return total


def _clip(box, cell):
    out = []
    for (a, b), (lo, hi) in zip(box, cell):
        a, b = max(a, lo), min(b, hi)
        if a >= b:
            return None
        out.append((a, b))
    return tuple(out)


def _free_coords(box, cell):
    """The coordinates in which the clipped box does not cover the cell."""
    return [j for j, ((a, b), (lo, hi)) in enumerate(zip(box, cell)) if a > lo or b < hi]


class KleeMeasure:
    def __init__(self, d: int):
        self.d = d
        self.cells = 0  # leaf cells visited
        self.max_depth = 0
        self.trace = []

    def measure(self, cell, boxes, depth=0, keep_trace=False):
        self.max_depth = max(self.max_depth, depth)
        s = [c for c in (_clip(b, cell) for b in boxes) if c is not None]  # @line L1
        vol = prod(hi - lo for lo, hi in cell)
        free = [_free_coords(b, cell) for b in s]
        if any(not f for f in free):  # @line L2
            self.cells += 1
            if keep_trace:
                self.trace.append((cell, "covered", vol))
            return vol
        if all(len(f) == 1 for f in free):  # @line L3
            u = [union_length([b[j] for b, f in zip(s, free) if f[0] == j]) for j in range(self.d)]  # @line L4
            self.cells += 1
            val = vol - prod((cell[j][1] - cell[j][0]) - u[j] for j in range(self.d))  # @line L5
            if keep_trace:
                self.trace.append((cell, "trellis", val))
            return val
        for step in range(self.d):  # @line L6
            j = (depth + step) % self.d
            lo, hi = cell[j]
            cand = sorted({v for b, f in zip(s, free) if len(f) >= 2 for v in b[j] if lo < v < hi})
            if cand:
                m = cand[(len(cand) - 1) // 2]
                break
        left = tuple((lo, m) if k == j else cell[k] for k, (lo, hi) in enumerate(cell))  # @line L7
        right = tuple((m, hi) if k == j else cell[k] for k, (lo, hi) in enumerate(cell))
        return (self.measure(left, s, depth + 1, keep_trace)  # @line L8
                + self.measure(right, s, depth + 1, keep_trace))


def klee_measure(boxes, keep_trace=False):
    """The volume of the union of the boxes, exactly, and the solver (for its counters)."""
    if not boxes:
        return 0, None
    d = len(boxes[0])
    if any(len(b) != d or any(lo > hi for lo, hi in b) for b in boxes):
        raise ValueError("boxes need the same dimension and lo <= hi")
    cell = tuple((min(b[j][0] for b in boxes), max(b[j][1] for b in boxes)) for j in range(d))
    solver = KleeMeasure(d)
    if any(lo == hi for lo, hi in cell):
        return 0, solver
    return solver.measure(cell, boxes, 0, keep_trace), solver
