# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mobius-sieve/. The authors are listed in prov/E7NA3A.jsonl.


def mobius_sieve(n: int) -> list[int]:
    """Return mu[0 .. n], where mu[m] is the Möbius function of m for m >= 1, and mu[0] = 0.

    Precondition: n >= 0.
    Cost: Theta(n) word operations; n + 1 words for lp, n + 1 entries for mu, pi(n) words for the primes.
    """
    mu = [0] * (n + 1)  # @line L1
    lp = [0] * (n + 1)
    primes: list[int] = []
    if n >= 1:
        mu[1] = 1
    for i in range(2, n + 1):  # @line L2
        if lp[i] == 0:  # @line L3
            lp[i] = i
            primes.append(i)
            mu[i] = -1
        for p in primes:  # @line L4
            if p > lp[i] or p * i > n:  # @line L5
                break
            lp[p * i] = p  # @line L6
            if p == lp[i]:  # @line L7
                mu[p * i] = 0
            else:
                mu[p * i] = -mu[i]  # @line L8
    return mu  # @line L9
