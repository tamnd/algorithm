# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/selection-sampling/. The authors are listed in prov/2YMG5Q.jsonl.

import random
from typing import Sequence, TypeVar

T = TypeVar("T")


def selection_sampling(items: Sequence[T], n: int, rng: random.Random) -> list[T]:
    """Knuth's Algorithm S: a uniform random n-subset of items, in their order.

    The number of items N must be known. Item t + 1 (0-based index t) is
    selected with probability (n - m) / (N - t), where m items are already
    selected. One random integer per item looked at; the scan stops after
    the last selected item. Time O(N), extra space O(1) beyond the output.
    """
    big_n = len(items)
    if not 0 <= n <= big_n:
        raise ValueError("need 0 <= n <= len(items)")
    m = 0  # @line L1
    t = 0
    out: list[T] = []
    while m < n:  # @line L2
        if rng.randrange(big_n - t) < n - m:  # @line L3
            out.append(items[t])  # @line L4
            m += 1
        t += 1  # @line L5
    return out  # @line L6
