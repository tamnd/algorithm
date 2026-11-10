# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/floyd-sampling/. The authors are listed in prov/H5FM3F.jsonl.

import random


def floyd_sampling(n: int, k: int, rng: random.Random) -> set[int]:
    """Floyd's algorithm: a uniform random k-subset of {0, ..., n - 1}.

    Exactly k random integers are drawn and no draw is ever rejected. The
    subset is kept in a hash set, so the expected time is O(k) and the space
    is O(k), independent of n.
    """
    if not 0 <= k <= n:
        raise ValueError("need 0 <= k <= n")
    s: set[int] = set()  # @line L1
    for j in range(n - k, n):  # @line L2
        t = rng.randrange(j + 1)  # @line L3
        if t not in s:  # @line L4
            s.add(t)
        else:
            s.add(j)  # @line L5
    return s  # @line L6
