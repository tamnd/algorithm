# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/segmented-sieve/. The authors are listed in prov/ZW0DHJ.jsonl.

from math import isqrt


def _small_primes(n: int) -> list[int]:
    """Primes up to n by the sieve of Eratosthenes. Cost: O(n log log n)."""
    if n < 2:
        return []
    flags = bytearray([1]) * (n + 1)
    flags[0] = flags[1] = 0
    p = 2
    while p * p <= n:
        if flags[p]:
            flags[p * p :: p] = bytes(len(range(p * p, n + 1, p)))
        p += 1
    return [m for m in range(2, n + 1) if flags[m]]


def segmented_sieve(low: int, high: int, block: int = 1 << 15) -> list[int]:
    """Return the increasing list of all primes p with low <= p <= high.

    Precondition: block >= 1; low and high are integers (an empty interval gives []).
    Cost: O(D log log high + (D / block + 1) * pi(high^(1/2)) + high^(1/2) log log high)
    word operations for D = high - low + 1, and O(high^(1/2) / log high + block) memory.
    """
    if block < 1:
        raise ValueError("block must be at least 1")
    low = max(low, 2)  # @line L1
    if low > high:
        return []
    base = _small_primes(isqrt(high))  # @line L2
    out: list[int] = []  # @line L3
    lo = low
    while lo <= high:  # @line L4
        hi = min(lo + block - 1, high)  # @line L5
        flags = bytearray([1]) * (hi - lo + 1)  # @line L6
        for p in base:  # @line L7
            if p * p > hi:
                break
            s = max(p * p, (lo + p - 1) // p * p)  # @line L8
            for m in range(s, hi + 1, p):  # @line L9
                flags[m - lo] = 0
        out.extend(lo + j for j in range(hi - lo + 1) if flags[j])  # @line L10
        lo = hi + 1  # @line L11
    return out  # @line L12
