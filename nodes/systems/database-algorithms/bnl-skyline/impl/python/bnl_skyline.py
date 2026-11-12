# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bnl-skyline/. The authors are listed in prov/E97Y5D.jsonl.

"""Block-nested-loop (BNL) skyline of Borzsonyi, Kossmann and Stocker.

The input is a sequence of tuples of numbers, all of the same length d.
Smaller is better in every dimension (negate a dimension to maximize it).
Tuple p dominates q if p[i] <= q[i] for all i and p[i] < q[i] for some i.
The skyline is the set of tuples that no tuple dominates. Equal tuples do
not dominate each other, so duplicates of a skyline tuple are all kept.

BNL keeps a window of at most `window` incomparable tuples in memory and
scans the input. A tuple dominated by a window tuple is dropped. A tuple
that dominates window tuples removes them. A tuple that is incomparable
with the whole window enters the window if there is room, else it is
written to a temporary file, which the next pass reads.

Each window entry and each temporary entry gets a timestamp from a counter.
A window tuple q has been compared with every other tuple once the scan of
the next pass reaches a temporary tuple written after q entered the window;
q is then output. At the end of a pass, the window tuples that entered
before the first write to the new temporary file are output.

Tuples are identified by their position in the input. The function returns
the positions of the skyline tuples in the order BNL outputs them.

stats gets "passes", "comparisons" (dominance tests) and "writes".
"""

from collections.abc import Sequence

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


def bnl_skyline(points: Sequence[Point], window: int,
                stats: dict | None = None) -> list[int]:
    """Return the input positions of the skyline tuples, in output order."""
    if window < 1:
        raise ValueError("the window must hold at least one tuple")
    win: list[tuple[int, int]] = []          # (timestamp, position)
    temp: list[tuple[int, int]] = [(-1, i) for i in range(len(points))]
    clock = 0
    out: list[int] = []
    passes = comparisons = writes = 0  # @line L1
    while temp:  # @line L2
        passes += 1
        source, temp = temp, []  # @line L3
        first_write = None
        for ts, i in source:  # @line L4
            p = points[i]
            keep = []
            for q_ts, j in win:  # @line L5
                if q_ts < ts:
                    out.append(j)    # q has now met every other tuple
                else:
                    keep.append((q_ts, j))
            win = keep
            dominated = False
            survivors = []
            for q_ts, j in win:  # @line L6
                comparisons += 1
                if dominates(points[j], p):
                    dominated = True
                    break
                if not dominates(p, points[j]):  # @line L7
                    survivors.append((q_ts, j))
            if dominated:
                continue
            win = survivors
            if len(win) < window:  # @line L8
                win.append((clock, i))
            else:
                temp.append((clock, i))
                writes += 1
                if first_write is None:
                    first_write = clock
            clock += 1
        keep = []
        for q_ts, j in win:  # @line L9
            if first_write is None or q_ts < first_write:
                out.append(j)
            else:
                keep.append((q_ts, j))
        win = keep
    if stats is not None:
        stats.update(passes=passes, comparisons=comparisons, writes=writes)
    return out  # @line L10
