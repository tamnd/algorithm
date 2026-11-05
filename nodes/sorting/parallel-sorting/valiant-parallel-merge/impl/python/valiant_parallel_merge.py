# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/valiant-parallel-merge/. The authors are listed in prov/HPT34J.jsonl.

"""Valiant's merge in the parallel comparison model, simulated round by round.

All subproblems of one level run at the same time. The simulation counts
the comparisons of each round, to check that m + n processors suffice, and
the number of rounds. Ties go to A: an item a of A comes before an item b
of B unless b < a, so every comparison asks "b < a" for some a in A, b in B.
"""

import math
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)

# A subproblem: merge a[i0:i1] and b[j0:j1] into out[i0 + j0 : i1 + j1].
Task = tuple[int, int, int, int]


class Counter:
    def __init__(self) -> None:
        self.n = 0

    def b_before_a(self, bx: Ordered, ax: Ordered) -> bool:
        self.n += 1
        return bx < ax


def valiant_merge(a: list[T], b: list[T], stats: dict | None = None) -> list[T]:
    """Return the stable merge of the sorted lists a and b."""
    if stats is None:
        stats = {}
    m, n = len(a), len(b)
    out: list = [None] * (m + n)
    stats.update(rounds=0, max_per_round=0)
    tasks: list[Task] = [(0, m, 0, n)]
    while tasks:
        r1, r2 = Counter(), Counter()
        nxt: list[Task] = []
        sampled = False
        for i0, i1, j0, j1 in tasks:
            mm, nn = i1 - i0, j1 - j0
            if mm == 0 or nn == 0:  # @line L1
                for k in range(i0, i1):
                    out[k + j0] = a[k]
                for k in range(j0, j1):
                    out[i0 + k] = b[k]
                continue
            if mm * nn <= mm + nn:  # @line L2
                lt = {(i, j): r1.b_before_a(b[j], a[i]) for i in range(i0, i1) for j in range(j0, j1)}
                for i in range(i0, i1):
                    out[i + j0 + sum(lt[i, j] for j in range(j0, j1))] = a[i]
                for j in range(j0, j1):
                    out[j + i0 + sum(not lt[i, j] for i in range(i0, i1))] = b[j]
                continue
            sampled = True
            s, t = math.isqrt(mm - 1) + 1, math.isqrt(nn - 1) + 1  # @line L3
            sa = list(range(i0 + s - 1, i1, s))
            sb = list(range(j0 + t - 1, j1, t))
            # Round 1: block of each sample among the samples of the other list.  # @line L4
            lt = {(i, j): r1.b_before_a(b[j], a[i]) for i in sa for j in sb}
            blk_a = {i: sum(lt[i, j] for j in sb) for i in sa}
            blk_b = {j: sum(not lt[i, j] for i in sa) for j in sb}
            splits = [(i0, j0, ""), (i1, j1, "")]
            for i in sa:
                lo = j0 + blk_a[i] * t  # first index of the block of B
                hi = min(j1, lo + t - 1)
                rank = lo + sum(r2.b_before_a(b[j], a[i]) for j in range(lo, hi))  # @line L5
                out[i + rank] = a[i]  # @line L6
                splits.append((i, rank, "a"))
            for j in sb:
                lo = i0 + blk_b[j] * s
                hi = min(i1, lo + s - 1)
                rank = lo + sum(not r2.b_before_a(b[j], a[i]) for i in range(lo, hi))
                out[j + rank] = b[j]
                splits.append((rank, j, "b"))
            splits.sort(key=lambda p: p[0] + p[1])  # @line L7
            for (i, j, kind), (i2, j2, _) in zip(splits, splits[1:]):
                # The sample that starts a piece is already in place.
                i += kind == "a"
                j += kind == "b"
                if i < i2 or j < j2:
                    nxt.append((i, i2, j, j2))  # @line L8
        stats["rounds"] += 2 if sampled else (1 if r1.n else 0)
        stats["max_per_round"] = max(stats["max_per_round"], r1.n, r2.n)
        tasks = nxt
    return out
