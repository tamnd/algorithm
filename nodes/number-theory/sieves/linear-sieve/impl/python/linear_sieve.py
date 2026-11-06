# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-sieve/. The authors are listed in prov/0C3CNA.jsonl.


def linear_sieve(n: int) -> tuple[list[int], list[int]]:
    """Return (lp, primes): lp[m] is the least prime factor of m for 2 <= m <= n, lp[0] = lp[1] = 0,
    and primes is the increasing list of primes up to n.

    Precondition: n >= 0.
    Cost: Theta(n) word operations; n + 1 words for lp and pi(n) words for the primes.
    """
    lp = [0] * (n + 1)  # @line L1
    primes: list[int] = []
    for i in range(2, n + 1):  # @line L2
        if lp[i] == 0:  # @line L3
            lp[i] = i  # @line L4
            primes.append(i)
        for p in primes:  # @line L5
            if p > lp[i] or p * i > n:  # @line L6
                break
            lp[p * i] = p  # @line L7
    return lp, primes  # @line L8


def factorize(m: int, lp: list[int]) -> list[tuple[int, int]]:
    """Return the prime factorization of m as (prime, exponent) pairs in increasing order.

    Precondition: 1 <= m < len(lp), and lp comes from linear_sieve.
    Cost: O(log m) lookups and divisions.
    """
    factors: list[tuple[int, int]] = []
    while m > 1:
        p, e = lp[m], 0
        while m % p == 0:
            m //= p
            e += 1
        factors.append((p, e))
    return factors
