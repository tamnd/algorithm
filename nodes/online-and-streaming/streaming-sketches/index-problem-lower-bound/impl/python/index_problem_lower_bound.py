# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/index-problem-lower-bound/. The authors are listed in prov/N46J3W.jsonl.

"""Streaming reductions from INDEX, and a brute-force check of the one-way bound.

In INDEX, Alice holds x in {0,1}^n, Bob holds i, and one message from Alice
must let Bob output x_i. Each reduction below turns a streaming algorithm
into such a protocol: Alice runs the algorithm on a stream built from x and
sends its memory state; Bob continues the run on a stream built from i and
reads x_i from the answer. So the memory is at least the message length.
"""

import math
from functools import lru_cache
from itertools import product


def binary_entropy(p: float) -> float:
    if p <= 0 or p >= 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


class ExactDistinct:
    """An exact F_0 algorithm (it stores the set of items it has seen)."""

    def __init__(self) -> None:
        self.seen: set[int] = set()

    def update(self, item: int) -> None:
        self.seen.add(item)

    def f0(self) -> int:
        return len(self.seen)


def index_via_exact_f0(x: list[int], i: int, algo: ExactDistinct) -> int:
    """Alice streams {j : x_j = 1}; Bob adds i and sees whether F_0 grew."""
    for j, bit in enumerate(x):
        if bit:
            algo.update(j)
    state = algo  # the message: the memory of the algorithm
    before = state.f0()
    state.update(i)
    return 1 if state.f0() == before else 0


def index_via_approx_f0(x: list[int], i: int, estimate_after, eps: float) -> int:
    """Alice sends |S| and the state; Bob adds i and rounds the F_0 estimate.

    estimate_after(true_f0) may return any value within a factor 1 +- eps of
    true_f0. The rounding is right when eps * (len(x) + 1) < 1/2.
    """
    s = sum(x)  # Alice also sends |S| in about log2(n + 1) bits
    true_after = s + (0 if x[i] else 1)
    est = estimate_after(true_after)
    return 1 if abs(est - s) < abs(est - (s + 1)) else 0


def index_via_exact_median(x: list[int], i: int) -> int:
    """Alice streams 2j + 2 + x_j for each j; Bob pads so the median is Alice's i-th item.

    Bob adds n - 1 - i copies of 0 and i copies of a value above every item
    (indices from 0). The stream has 2n - 1 items, and its median, the n-th
    smallest, is 2i + 2 + x_i.
    """
    n = len(x)
    stream = [2 * j + 2 + bit for j, bit in enumerate(x)]
    big = 2 * n + 10
    stream += [0] * (n - 1 - i) + [big] * i
    med = sorted(stream)[n - 1]
    return med % 2


@lru_cache(maxsize=None)
def best_deterministic_error(n: int, c: int) -> float:
    """The smallest average error of a deterministic one-way protocol with c-bit messages.

    The average is over x uniform in {0,1}^n and i uniform in [n]. For each
    map from inputs to the 2^c messages, Bob's best answer for a message and
    an index is the majority bit among the inputs with that message.
    """
    inputs = list(product((0, 1), repeat=n))
    k = 1 << c
    best = None
    # Renaming the messages changes nothing, so the first input can get message 0.
    for rest in product(range(k), repeat=len(inputs) - 1):
        msg = (0,) + rest
        ones = [[0] * n for _ in range(k)]
        size = [0] * k
        for x, m in zip(inputs, msg):
            size[m] += 1
            row = ones[m]
            for j in range(n):
                row[j] += x[j]
        err = sum(min(o, size[m] - o) for m in range(k) for o in ones[m])
        if best is None or err < best:
            best = err
    return best / (len(inputs) * n)
