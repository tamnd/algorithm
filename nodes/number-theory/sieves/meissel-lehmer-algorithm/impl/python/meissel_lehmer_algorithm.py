# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/meissel-lehmer-algorithm/. The authors are listed in prov/2SPPAE.jsonl.

from math import isqrt


def icbrt(x: int) -> int:
    """Return the integer cube root, the largest y >= 0 with y^3 <= x. Precondition: x >= 0."""
    y = round(x ** (1.0 / 3.0)) if x > 0 else 0
    while y * y * y > x:
        y -= 1
    while (y + 1) ** 3 <= x:
        y += 1
    return y


def meissel_lehmer(x: int) -> int:
    """Return pi(x), the number of primes p <= x.

    Precondition: x is an integer (x < 2 gives 0).
    Cost: O(x^(2/3) log x) word operations and O(x^(2/3)) words of memory,
    for y = x^(1/3), z = x / y, the Fenwick tree over [1, z] and the sieve up to z.
    """
    if x < 2:  # @line L1
        return 0
    y = icbrt(x)  # @line L2
    z = x // y
    # @line L3: least prime factors and primes up to z, pi table, mu up to y
    lpf = [0] * (z + 1)
    primes: list[int] = []
    for i in range(2, z + 1):
        if lpf[i] == 0:
            lpf[i] = i
            primes.append(i)
        li = lpf[i]
        for p in primes:
            if p > li or i * p > z:
                break
            lpf[i * p] = p
    pi = [0] * (z + 1)
    count = 0
    for i in range(2, z + 1):
        if lpf[i] == i:
            count += 1
        pi[i] = count
    mu = [0] * (y + 1)
    mu[1] = 1
    for m in range(2, y + 1):
        p = lpf[m]
        k = m // p
        mu[m] = 0 if k % p == 0 else -mu[k]
    a = pi[y]
    phi = 0
    for m in range(1, y + 1):  # @line L4
        phi += mu[m] * (x // m)
    tree = [0] + [i & -i for i in range(1, z + 1)]  # @line L5
    alive = bytearray([1]) * (z + 1)
    for b in range(a):  # @line L6
        p = primes[b]  # p is p_(b+1); the tree now counts n <= z free of p_1, ..., p_b
        for m in range(y // p + 1, y + 1):  # @line L7
            if mu[m] != 0 and lpf[m] > p:
                n = x // (m * p)  # @line L8
                s = 0
                while n > 0:
                    s += tree[n]
                    n -= n & -n
                phi -= mu[m] * s
        for k in range(p, z + 1, p):  # @line L9
            if alive[k]:
                alive[k] = 0
                i = k
                while i <= z:
                    tree[i] -= 1
                    i += i & -i
    r = isqrt(x)  # @line L10
    p2 = 0
    for p in primes[a:]:
        if p > r:
            break
        p2 += pi[x // p] - pi[p] + 1
    return phi + a - 1 - p2  # @line L11
