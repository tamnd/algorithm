# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-and-prune/. The authors are listed in prov/46M4XT.jsonl.

"""Sweep and prune for 2D axis-aligned boxes.

A box is a tuple (xlo, ylo, xhi, yhi) with xlo <= xhi and ylo <= yhi. Boxes are closed,
so two boxes that only touch overlap. The class keeps, for each axis, the list of the 2n
interval endpoints in sorted order, a counter per pair of boxes (the number of axes on which
the two intervals overlap) and the set of pairs whose counter is 2.

update() moves the boxes and repairs each list with insertion sort. Each swap of a lower
endpoint with an upper endpoint changes one counter by one. The cost of one update is
O(n + r) for r swaps. sort_and_sweep() is the one-shot version: O(n log n + q), where q is
the number of pairs whose intervals overlap on the sweep axis.
"""

from __future__ import annotations

Box = tuple[float, float, float, float]
Pair = tuple[int, int]

LO, HI = 0, 1


def _pair(i: int, j: int) -> Pair:
    return (i, j) if i < j else (j, i)


def sort_and_sweep(boxes: list[Box], axis: int = 0) -> set[Pair]:
    """All pairs of overlapping boxes: sort on one axis, sweep, test the other axis."""
    other = 1 - axis
    order = sorted(range(len(boxes)), key=lambda i: boxes[i][axis])
    active: list[int] = []
    out: set[Pair] = set()
    for i in order:
        lo = boxes[i][axis]
        active = [j for j in active if boxes[j][axis + 2] >= lo]  # drop the intervals that ended
        for j in active:  # j overlaps i on the sweep axis
            if boxes[i][other] <= boxes[j][other + 2] and boxes[j][other] <= boxes[i][other + 2]:
                out.add(_pair(i, j))
        active.append(i)
    return out


class SweepAndPrune:
    """Incremental sweep and prune over n boxes that keep their index."""

    def __init__(self, boxes: list[Box]) -> None:
        self.boxes: list[Box] = list(boxes)
        n = len(self.boxes)
        # endpoint = [value, kind, id]; kind LO sorts before HI at equal values
        self.ends: list[list[list]] = []
        for a in range(2):
            e = [[self.boxes[i][a], LO, i] for i in range(n)] + [[self.boxes[i][a + 2], HI, i] for i in range(n)]
            e.sort()
            self.ends.append(e)
        self.count: dict[Pair, int] = {}
        for a in range(2):
            active: set[int] = set()
            for v, kind, i in self.ends[a]:
                if kind == LO:
                    for j in active:
                        p = _pair(i, j)
                        self.count[p] = self.count.get(p, 0) + 1
                    active.add(i)
                else:
                    active.discard(i)
        self.pairs: set[Pair] = {p for p, c in self.count.items() if c == 2}

    def update(self, boxes: list[Box]) -> int:
        """Move the boxes to new positions and repair the state. Returns the number of swaps r."""
        self.boxes = list(boxes)
        r = 0  # @line L1
        for a in range(2):  # @line L2
            e = self.ends[a]
            for end in e:  # @line L3
                end[0] = self.boxes[end[2]][a + 2 * end[1]]
            for i in range(1, len(e)):  # @line L4
                j = i  # @line L5
                while j > 0 and e[j - 1] > e[j]:  # @line L6
                    x, y = e[j], e[j - 1]  # @line L7
                    if x[2] != y[2]:
                        p = _pair(x[2], y[2])
                        if x[1] == LO and y[1] == HI:  # @line L8
                            c = self.count.get(p, 0) + 1
                            self.count[p] = c
                            if c == 2:
                                self.pairs.add(p)
                        elif x[1] == HI and y[1] == LO:  # @line L9
                            c = self.count[p]
                            if c == 2:
                                self.pairs.discard(p)
                            if c == 1:
                                del self.count[p]
                            else:
                                self.count[p] = c - 1
                    e[j - 1], e[j] = x, y  # @line L10
                    j -= 1
                    r += 1
        return r  # @line L11

    def overlapping_pairs(self) -> set[Pair]:
        return set(self.pairs)

    def check_invariant(self) -> None:
        for a in range(2):
            e = self.ends[a]
            assert all(e[k] <= e[k + 1] for k in range(len(e) - 1))
        n = len(self.boxes)
        for i in range(n):
            for j in range(i + 1, n):
                c = sum(
                    1
                    for a in range(2)
                    if self.boxes[i][a] <= self.boxes[j][a + 2] and self.boxes[j][a] <= self.boxes[i][a + 2]
                )
                assert self.count.get((i, j), 0) == c
                assert ((i, j) in self.pairs) == (c == 2)
