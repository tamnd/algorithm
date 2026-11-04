# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balas-additive-algorithm/. The authors are listed in prov/MXCW04.jsonl.
"""Balas's additive algorithm (implicit enumeration) for 0-1 linear programs.

Minimize c x subject to A x <= b and x in {0, 1}^n, with every c_j >= 0.
The search is depth-first with an explicit stack. It uses only additions,
subtractions and comparisons of the data.
"""

from __future__ import annotations

from typing import Optional, Sequence


def balas(
    c: Sequence[int],
    a: Sequence[Sequence[int]],
    b: Sequence[int],
    stats: Optional[dict[str, int]] = None,
    trace: Optional[list[tuple[tuple[int, ...], str]]] = None,
) -> tuple[Optional[int], Optional[list[int]]]:
    """Return (z, x) with x an optimal 0-1 vector and z = c x, or (None, None).

    a has one row per constraint; row i reads sum_j a[i][j] x_j <= b[i].
    """
    n, m = len(c), len(b)
    if any(cj < 0 for cj in c):
        raise ValueError("all costs must be nonnegative; complement x_j to 1 - x_j first")
    if stats is not None:
        stats.update(nodes=0)
    z: Optional[int] = None  # @line L1
    best: Optional[tuple[int, ...]] = None
    stack: list[tuple[tuple[int, ...], int, tuple[int, ...], tuple[int, ...]]] = [((), 0, tuple(b), tuple(range(n)))]
    while stack:  # @line L2
        ones, v, s, free = stack.pop()  # @line L3
        if stats is not None:
            stats["nodes"] += 1
        if all(si >= 0 for si in s):  # @line L4
            if z is None or v < z:  # @line L5
                z, best = v, ones
            if trace is not None:
                trace.append((ones, "feasible"))
            continue  # @line L6
        bad = [i for i in range(m) if s[i] < 0]
        useful = [  # @line L7
            j for j in free
            if (z is None or v + c[j] < z) and any(a[i][j] < 0 for i in bad)
        ]
        if not useful or any(  # @line L8
            s[i] - sum(a[i][j] for j in useful if a[i][j] < 0) < 0 for i in bad
        ):
            if trace is not None:
                trace.append((ones, "fathomed"))
            continue
        # Balas's choice: the variable that leaves the least total infeasibility.
        j = max(useful, key=lambda j: (sum(min(0, s[i] - a[i][j]) for i in range(m)), -j))  # @line L9
        if trace is not None:
            trace.append((ones, "branch %d" % j))
        rest = tuple(k for k in free if k != j)
        stack.append((ones, v, s, rest))  # @line L10
        stack.append((ones + (j,), v + c[j], tuple(s[i] - a[i][j] for i in range(m)), rest))  # @line L11
    if best is None:  # @line L12
        return None, None
    x = [0] * n
    for j in best:
        x[j] = 1
    return z, x
