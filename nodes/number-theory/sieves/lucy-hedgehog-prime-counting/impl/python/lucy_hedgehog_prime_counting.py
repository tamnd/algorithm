# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lucy-hedgehog-prime-counting/. The authors are listed in prov/KWQ8J3.jsonl.

from math import isqrt


def lucy_hedgehog_prime_counting(x: int) -> int:
    """Return pi(x), the number of primes p <= x.

    Precondition: x is an integer (x < 2 gives 0).
    Cost: O(x^(3/4) / log x) word operations and O(x^(1/2)) words of memory.
    S(v) is stored in small[v] for v <= r = isqrt(x) and in large[k] for v = x // k, 1 <= k <= r.
    """
    if x < 2:  # @line L1
        return 0
    r = isqrt(x)  # @line L2
    small = [0] + [v - 1 for v in range(1, r + 1)]  # @line L3
    large = [0] + [x // k - 1 for k in range(1, r + 1)]
    for p in range(2, r + 1):  # @line L4
        if small[p] == small[p - 1]:  # @line L5
            continue  # p is composite
        c = small[p - 1]  # @line L6
        p2 = p * p
        for k in range(1, min(r, x // p2) + 1):  # @line L7
            kp = k * p
            u = large[kp] if kp <= r else small[x // kp]
            large[k] -= u - c  # @line L8
        for v in range(r, p2 - 1, -1):
            small[v] -= small[v // p] - c
    return large[1]  # @line L9


def lucy_prime_sum(x: int) -> int:
    """Return the sum of the primes p <= x, by the same recurrence with weights p.

    Precondition: x is an integer. Cost: as lucy_hedgehog_prime_counting.
    """
    if x < 2:
        return 0
    r = isqrt(x)
    small = [0] + [v * (v + 1) // 2 - 1 for v in range(1, r + 1)]
    large = [0] + [(x // k) * (x // k + 1) // 2 - 1 for k in range(1, r + 1)]
    for p in range(2, r + 1):
        if small[p] == small[p - 1]:
            continue
        c = small[p - 1]
        p2 = p * p
        for k in range(1, min(r, x // p2) + 1):
            kp = k * p
            u = large[kp] if kp <= r else small[x // kp]
            large[k] -= p * (u - c)
        for v in range(r, p2 - 1, -1):
            small[v] -= p * (small[v // p] - c)
    return large[1]
