# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/trial-division/. The authors are listed in prov/1TKFVE.jsonl.


def trial_division(n: int) -> list[int]:
    """Return the prime factors of n in non-decreasing order, with multiplicity.

    Precondition: n >= 1 (n = 1 gives the empty list). Raises ValueError otherwise.
    Cost: at most about sqrt(n) / 2 trial divisors, so O(sqrt(n)) arithmetic
    operations on integers of the size of n. The loop stops early when the
    unfactored part m has no factor below sqrt(m).
    """
    if n < 1:
        raise ValueError("n must be a positive integer")
    factors: list[int] = []
    m, d = n, 2  # @line L1
    while d * d <= m:  # @line L2
        while m % d == 0:  # @line L3
            factors.append(d)  # @line L4
            m //= d
        d = 3 if d == 2 else d + 2  # @line L5
    if m > 1:  # @line L6
        factors.append(m)
    return factors  # @line L7
