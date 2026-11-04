# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/external-samplesort/. The authors are listed in prov/PAB348.jsonl.

import bisect
import math
import random
from typing import Protocol, TypeVar


class Ordered(Protocol):
    def __lt__(self, other: "Ordered", /) -> bool: ...


T = TypeVar("T", bound=Ordered)


def blocks(length: int, b: int) -> int:
    """The number of blocks of b items that hold a file of the given length."""
    return -(-length // b)


def choose_splitters(sample: list[T], a: int, s: int) -> list[T]:
    """The distinct items of ranks a, 2a, ..., (s - 1)a of the sorted sample, in order."""
    sample = sorted(sample)
    out: list[T] = []
    for r in range(a, min(s * a, len(sample) + 1), a):
        x = sample[r - 1]
        if not out or out[-1] < x:
            out.append(x)
    return out


def distribute(f: list[T], splitters: list[T]) -> list[list[T]]:
    """The buckets U_0, E_1, U_1, ..., E_k, U_k, each in the order of f.

    U_j holds the items strictly between s_j and s_(j+1), and E_j the items equal to s_j.
    """
    k = len(splitters)
    out: list[list[T]] = [[] for _ in range(2 * k + 1)]
    for x in f:
        j = bisect.bisect_left(splitters, x)
        if j < k and not x < splitters[j]:
            out[2 * j + 1].append(x)  # x equals s_(j+1)
        else:
            out[2 * j].append(x)
    return out


def external_samplesort(f: list[T], m: int = 16, b: int = 2, seed: int = 0, a: int = 0) -> int:
    """Sort f in place as an external samplesort with a memory of m items and blocks of b items.

    Returns the number of block I/Os. Precondition: b >= 1 and m >= 4 * b.
    A read or write of a file of length L costs ceil(L / b) I/Os, and the
    sample costs one read per distinct block that holds a sampled position.
    a is the oversampling factor; 0 means ceil(8 ln S). The sort is stable.
    With S = m / (2b) buckets per level the expected cost is O(n log_m n).
    """
    if b < 1 or m < 4 * b:
        raise ValueError("need b >= 1 and m >= 4 * b")
    rng = random.Random(seed)

    def sort(g: list[T]) -> tuple[list[T], int]:
        if len(g) <= m:  # @line L1
            return sorted(g), 2 * blocks(len(g), b)
        s = max(2, min(m // (2 * b), -(-4 * len(g) // m)))  # @line L2
        over = a if a > 0 else math.ceil(8 * math.log(s))
        pos = [rng.randrange(len(g)) for _ in range(over * s)]  # @line L3
        ios = len({p // b for p in pos})
        splitters = choose_splitters([g[p] for p in pos], over, s)  # @line L4
        buckets = distribute(g, splitters)  # @line L5
        ios += blocks(len(g), b) + sum(blocks(len(u), b) for u in buckets)
        out: list[T] = []
        for i, u in enumerate(buckets):  # @line L6
            if i % 2 == 0:
                u, c = sort(u)  # @line L7
                ios += c
            out.extend(u)  # @line L8
        return out, ios

    result, total = sort(list(f))
    f[:] = result
    return total
