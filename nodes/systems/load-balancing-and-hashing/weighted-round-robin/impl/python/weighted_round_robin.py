# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weighted-round-robin/. The authors are listed in prov/CCH3Y5.jsonl.

"""Weighted round robin: smooth (nginx), gcd-based (LVS) and classic block order.

SmoothWRR is the main algorithm. At each pick it adds w[j] to current[j] for
every backend, takes the backend with the largest current value (the first one
on a tie), and subtracts the total weight W from it. Over every W consecutive
picks, backend j is picked exactly w[j] times. Precondition: integer weights
w[j] >= 0 with W > 0. Cost: Theta(n) time per pick, Theta(n) space.
"""

from math import gcd
from typing import Iterator, List, Sequence


class SmoothWRR:
    """Smooth weighted round robin, as in nginx's ngx_http_upstream_round_robin.c."""

    def __init__(self, weights: Sequence[int]) -> None:
        if any(w < 0 for w in weights) or sum(weights) <= 0:
            raise ValueError("weights must be >= 0 with a positive sum")
        self.w = list(weights)
        self.c = [0] * len(weights)

    def pick(self) -> int:
        total = 0  # @line L1
        best = -1
        for j in range(len(self.w)):  # @line L2
            self.c[j] += self.w[j]  # @line L3
            total += self.w[j]  # @line L4
            if best < 0 or self.c[j] > self.c[best]:  # @line L5
                best = j
        self.c[best] -= total  # @line L6
        return best  # @line L7


def smooth_sequence(weights: Sequence[int], m: int) -> List[int]:
    """The first m picks of smooth weighted round robin."""
    s = SmoothWRR(weights)
    return [s.pick() for _ in range(m)]


def lvs_wrr(weights: Sequence[int]) -> Iterator[int]:
    """The gcd-based weighted round robin of LVS (ip_vs_wrr.c), as an endless stream.

    cw starts at the maximum weight and steps down by the gcd of the weights;
    one scan of the list returns each backend with weight >= cw.
    """
    n = len(weights)
    mw = max(weights) if n else 0
    di = 0
    for w in weights:
        di = gcd(di, w)
    if mw <= 0:
        return
    i, cw = -1, 0
    while True:
        i = (i + 1) % n
        if i == 0:
            cw -= di
            if cw <= 0:
                cw = mw
        if weights[i] >= cw:
            yield i


def lvs_sequence(weights: Sequence[int], m: int) -> List[int]:
    """The first m picks of LVS weighted round robin."""
    g = lvs_wrr(weights)
    return [next(g) for _ in range(m)]


def classic_sequence(weights: Sequence[int], m: int) -> List[int]:
    """Classic weighted round robin: w[j] picks of backend j in a row, then the next backend."""
    period = [j for j, w in enumerate(weights) for _ in range(w)]
    return [period[k % len(period)] for k in range(m)]


def max_run(seq: Sequence[int]) -> int:
    """The longest run of equal values in seq read as a cycle."""
    if not seq:
        return 0
    if len(set(seq)) == 1:
        return len(seq)
    best = run = 0
    for x, y in zip(seq + seq, (seq + seq)[1:]):
        run = run + 1 if x == y else 0
        best = max(best, run + 1)
    return best


def max_gap(seq: Sequence[int], j: int) -> int:
    """The largest distance between consecutive picks of j in seq read as a cycle."""
    pos = [k for k, x in enumerate(seq) if x == j]
    if not pos:
        return 0
    m = len(seq)
    return max((pos[(a + 1) % len(pos)] - pos[a]) % m or m for a in range(len(pos)))
