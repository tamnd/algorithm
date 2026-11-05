# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-quicksort/. The authors are listed in prov/X4M2NF.jsonl.

"""Parallel quicksort with a three-way partition by parallel pack.

The code runs the parallel steps one after the other, which is a legal
schedule. It also reports the recursion depth, and the work and span of
the computation with unit cost per key per pass and a scan of span
about lg n.
"""

import random
from dataclasses import dataclass
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


@dataclass
class Cost:
    work: int = 0
    span: int = 0
    depth: int = 0


def exclusive_scan(flags: list[int]) -> tuple[list[int], int]:
    """Exclusive prefix sums of flags, and their total."""
    out, total = [], 0
    for f in flags:
        out.append(total)
        total += f
    return out, total


def pack(a: list[T], flags: list[int]) -> list[T]:
    """Keep the items with flag 1, in their input order."""
    pos, total = exclusive_scan(flags)  # @line L10
    out: list[T] = [a[0]] * total if total else []
    for i, f in enumerate(flags):  # @line L11
        if f:
            out[pos[i]] = a[i]
    return out  # @line L12


def parallel_quicksort(a: list[T], rng: random.Random | None = None) -> tuple[list[T], Cost]:
    """Return a sorted copy of a (stable), and the cost of the run."""
    if rng is None:
        rng = random.Random(0)
    n = len(a)  # @line L1
    if n <= 1:  # @line L2
        return list(a), Cost(1, 1, 0)
    x = a[rng.randrange(n)]  # @line L3
    lt = [1 if v < x else 0 for v in a]  # @line L4
    gt = [1 if x < v else 0 for v in a]
    eq = [1 - p - q for p, q in zip(lt, gt)]
    less, equal, greater = pack(a, lt), pack(a, eq), pack(a, gt)  # @line L5
    left, c1 = parallel_quicksort(less, rng)  # @line L6
    right, c2 = parallel_quicksort(greater, rng)  # @line L7
    # sync: both parts are sorted here  # @line L8
    out = left + equal + right  # @line L9
    scan_span = n.bit_length()
    work = 5 * n + c1.work + c2.work
    span = 3 * scan_span + max(c1.span, c2.span)
    return out, Cost(work, span, 1 + max(c1.depth, c2.depth))
