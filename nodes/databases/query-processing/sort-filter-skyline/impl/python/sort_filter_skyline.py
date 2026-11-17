# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-filter-skyline/. The authors are listed in prov/6QMS6V.jsonl.

"""Sort-filter-skyline (SFS) of Chomicki, Godfrey, Gryz and Liang.

The input is a sequence of tuples of numbers, all of the same length d.
Smaller is better in every dimension (negate a dimension to maximize it).
Tuple p dominates q if p[i] <= q[i] for all i and p[i] < q[i] for some i.
The skyline is the set of tuples that no tuple dominates; equal tuples do
not dominate each other, so duplicates of a skyline tuple are all kept.

SFS first sorts the input by a score that is monotone for dominance: if p
dominates q then score(p) <= score(q), with ties broken by the tuples. The default score is
the entropy E(p) = sum of ln(1 + p[i]), which needs p[i] > -1; the sum of
the attributes also works for any numbers. After the sort, no tuple is
dominated by a later one, so a tuple that no window tuple dominates is in
the skyline. It is output at once and never leaves the window. Tuples that
do not fit go to a temporary file. They were compared with the full window
when written, so the next pass starts with an empty window.

The function returns the positions of the skyline tuples in output order.
stats gets "passes", "comparisons" (dominance tests), "writes" and
"order" (the input positions in presorted order).
"""

import math
from collections.abc import Callable, Sequence

Point = Sequence[float]


def dominates(p: Point, q: Point) -> bool:
    """True if p is no worse than q everywhere and better somewhere."""
    strict = False
    for a, b in zip(p, q):
        if a > b:
            return False
        if a < b:
            strict = True
    return strict


def entropy(p: Point) -> float:
    """The entropy score of SFS; strictly monotone for p[i] > -1."""
    return math.fsum(math.log1p(x) for x in p)


def sort_filter_skyline(points: Sequence[Point], window: int,
                        score: Callable[[Point], float] = entropy,
                        stats: dict | None = None) -> list[int]:
    """Return the input positions of the skyline tuples, in output order."""
    if window < 1:
        raise ValueError("the window must hold at least one tuple")
    # Ties in a rounded score are broken by the tuple itself: if p dominates
    # q then p < q in lexicographic order, so the sort stays topological.
    order = sorted(range(len(points)), key=lambda i: (score(points[i]), tuple(points[i])))  # @line L1
    temp = order
    out: list[int] = []
    passes = comparisons = writes = 0
    while temp:  # @line L2
        passes += 1
        source, temp, win = temp, [], []  # @line L3
        for i in source:  # @line L4
            p = points[i]
            dominated = False
            for j in win:  # @line L5
                comparisons += 1
                if dominates(points[j], p):
                    dominated = True
                    break
            if dominated:
                continue
            if len(win) < window:  # @line L6
                win.append(i)
                out.append(i)      # p is in the skyline: output it now
            else:
                temp.append(i)  # @line L7
                writes += 1
    if stats is not None:
        stats.update(passes=passes, comparisons=comparisons, writes=writes, order=order)
    return out  # @line L8
