# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frequency-moment-lower-bounds/. The authors are listed in prov/7C0H0K.jsonl.

"""The reductions from set disjointness to frequency moments, in code.

Each player's input set becomes one part of a stream. A streaming algorithm
with s bits of memory and q passes then gives a protocol in which the memory
state is passed from player to player: at most q * t messages of s bits.
"""

import math
from collections import Counter


def moment(stream, p: float) -> float:
    """F_p of the stream; p = math.inf gives the largest count."""
    counts = Counter(stream).values()
    if p == math.inf:
        return max(counts, default=0)
    return sum(c**p for c in counts)


def disj_via_f_inf(a: set[int], b: set[int]) -> bool:
    """True if A and B intersect: F_inf of the stream A then B is 2, else at most 1."""
    return moment(sorted(a) + sorted(b), math.inf) >= 2


def players_for(n: int, k: float) -> int:
    """The smallest t >= 2 with t^k > 2n."""
    t = 2
    while t**k <= 2 * n:
        t += 1
    return t


def promise_instance(n: int, t: int, common: int | None, sizes: list[int]) -> list[list[int]]:
    """t pairwise disjoint subsets of {0, ..., n-1}, plus one element common to all if given.

    sizes[j] is the number of private elements of player j.
    """
    pool = [x for x in range(n) if x != common]
    if sum(sizes) > len(pool):
        raise ValueError("not enough elements")
    sets, pos = [], 0
    for j in range(t):
        s = pool[pos : pos + sizes[j]]
        pos += sizes[j]
        sets.append(s + ([common] if common is not None else []))
    return sets


def decide_from_estimate(estimate: float, n: int, eps: float) -> bool:
    """YES (a common element) if a (1 +- eps) estimate of F_k exceeds (1 + eps) n."""
    return estimate > (1 + eps) * n


def message_bits(s: int, t: int, q: int) -> int:
    """Bits sent when t players pass an s-bit memory state for q passes.

    In each pass the state moves from player 1 to player t (t - 1 messages),
    and between passes player t sends it back to player 1.
    """
    return s * (q * (t - 1) + (q - 1))
