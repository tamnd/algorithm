# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/index-calculus/. The authors are listed in prov/C3H4Y5.jsonl.

import random
from math import exp, log, sqrt


def _prime_factors(m: int) -> dict[int, int]:
    """Factor m >= 1 by trial division; return {prime: exponent}."""
    out: dict[int, int] = {}
    d = 2
    while d * d <= m:
        while m % d == 0:
            out[d] = out.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        out[m] = out.get(m, 0) + 1
    return out


def _generator(p: int, factors: dict[int, int]) -> int:
    """Least generator of (Z/pZ)^* for a prime p, given the factors of p - 1."""
    for c in range(1, p):
        if all(pow(c, (p - 1) // q, p) != 1 for q in factors):
            return c
    raise ValueError("p is not prime")


def _smooth(y: int, base: list[int]) -> list[int] | None:
    """Exponent vector of y over the factor base, or None if y is not smooth."""
    e = [0] * len(base)
    for i, s in enumerate(base):
        while y % s == 0:
            y //= s
            e[i] += 1
    return e if y == 1 else None


def _solve(rels: list[tuple[list[int], int]], q: int, mod: int) -> list[int] | None:
    """Solve sum_j e_j lambda_j = k (mod mod) for all relations, mod = q^f.

    Gauss-Jordan elimination with pivots that are units modulo q. Return the
    unique solution, or None if some column has no unit pivot.
    """
    rows = [[x % mod for x in e] + [k % mod] for e, k in rels]
    t = len(rels[0][0])
    for j in range(t):  # @line L15
        piv = next((i for i in range(j, len(rows)) if rows[i][j] % q), None)
        if piv is None:
            return None
        rows[j], rows[piv] = rows[piv], rows[j]  # @line L16
        inv = pow(rows[j][j], -1, mod)
        rows[j] = [x * inv % mod for x in rows[j]]
        for i in range(len(rows)):
            if i != j and rows[i][j]:
                c = rows[i][j]
                rows[i] = [(x - c * y) % mod for x, y in zip(rows[i], rows[j])]
    return [rows[j][t] for j in range(t)]  # @line L17


def index_calculus(g: int, h: int, n: int, p: int, seed: int = 0) -> int | None:
    """Index calculus for log_g h in (Z/pZ)^* with the primes below B as factor base.

    Return the x in [0, n) with g^x = h (mod p), or None if h is not a power
    of g. Logarithms are taken to a generator of (Z/pZ)^* and are needed only
    modulo the parts of p - 1 belonging to primes that divide n.
    Precondition: p is prime, gcd(g, p) = 1 and n = ord(g) exactly.
    Raises ValueError if p < 2 or n < 1.
    Cost: with B about L_p(1/2, 1/2) = exp((1/2) (ln p ln ln p)^(1/2)), an
    expected exp((2 + o(1)) (ln p ln ln p)^(1/2)) bit operations for the
    relation search by trial division and the dense linear algebra, plus
    O(p^(1/2)) divisions to factor p - 1 and find a generator.
    """
    if p < 2 or n < 1:
        raise ValueError("need p >= 2 and n >= 1")
    g %= p
    h %= p
    if pow(h, n, p) != 1:  # @line L1
        return None
    if h == 1:  # @line L2
        return 0
    rng = random.Random(seed)
    fac = _prime_factors(p - 1)
    gamma = _generator(p, fac)  # @line L3
    parts = {q: q**f for q, f in fac.items() if n % q == 0}
    ell = 1
    for m in parts.values():
        ell *= m
    lp = log(p)
    bound = max(12, round(2 * exp(0.5 * sqrt(lp * log(max(lp, 2))))))
    base = [s for s in range(2, min(bound, p)) if all(s % d for d in range(2, s))]  # @line L4
    rels: list[tuple[list[int], int]] = []
    lam: list[int] | None = None
    while lam is None:  # @line L5
        k = rng.randrange(p - 1)  # @line L6
        e = _smooth(pow(gamma, k, p), base)  # @line L7
        if e is None:
            continue
        rels.append((e, k))
        if len(rels) < len(base) + 10 or len(rels) % 5:  # @line L8
            continue
        lam = [0] * len(base)
        modulus = 1
        for q, m in parts.items():
            sol = _solve(rels, q, m)
            if sol is None:  # @line L9
                lam = None
                break
            lam = [(a + modulus * ((s - a) * pow(modulus, -1, m) % m)) for a, s in zip(lam, sol)]
            modulus *= m
    logs = []
    for y in (g, h):  # @line L10
        while True:
            k = rng.randrange(p - 1)  # @line L11
            d = _smooth(y * pow(gamma, k, p) % p, base)
            if d is not None:
                break
        logs.append((sum(a * b for a, b in zip(d, lam)) - k) % ell)  # @line L12
    c = ell // n  # @line L13
    u = logs[0] // c
    return logs[1] // c * pow(u, -1, n) % n  # @line L14
