# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/berlekamp-factorization/. The authors are listed in prov/T0YM2W.jsonl.

"""Berlekamp's algorithm: factor a monic square-free polynomial over Z/pZ.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n] of ints
in 0 .. p - 1, lowest degree first; the zero polynomial is []. p must be a
prime.

The Berlekamp algebra of f is the set of v with deg v < n and v^p = v mod f.
It is the left null space of Q - I, where row i of Q holds x^(p i) mod f, and
its dimension is the number of irreducible factors. For small p the factors
are split deterministically with gcd(v - s, h) for all s in Z/pZ; for large
p a random element of the algebra is raised to the power (p - 1)/2.
"""

from __future__ import annotations

import random
from typing import List, Optional, Sequence, Tuple

Poly = List[int]

SMALL_P = 50


def trim(a: Sequence[int]) -> Poly:
    """Return a copy of a without trailing zero coefficients."""
    out = list(a)
    while out and out[-1] == 0:
        out.pop()
    return out


def reduce_p(a: Sequence[int], p: int) -> Poly:
    """Reduce every coefficient into 0 .. p - 1 and strip leading zeros."""
    return trim([x % p for x in a])


def add(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    n = max(len(a), len(b))
    return trim([((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p for i in range(n)])


def sub(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    n = max(len(a), len(b))
    return trim([((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p for i in range(n)])


def mul(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    """Schoolbook product in (Z/pZ)[x]."""
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[i + j] += x * y
    return reduce_p(c, p)


def divmod_p(a: Sequence[int], b: Sequence[int], p: int) -> Tuple[Poly, Poly]:
    """Quotient and remainder of a by the nonzero b in (Z/pZ)[x]."""
    b = reduce_p(b, p)
    if not b:
        raise ZeroDivisionError("division by the zero polynomial")
    r = reduce_p(a, p)
    inv = pow(b[-1], -1, p)
    db = len(b) - 1
    if len(r) <= db:
        return [], r
    q = [0] * (len(r) - db)
    for i in range(len(r) - 1, db - 1, -1):
        c = r[i] * inv % p
        if c:
            q[i - db] = c
            for j in range(db + 1):
                r[i - db + j] = (r[i - db + j] - c * b[j]) % p
    return trim(q), trim(r[:db])


def rem(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    return divmod_p(a, b, p)[1]


def monic(a: Sequence[int], p: int) -> Poly:
    """a divided by its leading coefficient; the zero polynomial stays zero."""
    a = reduce_p(a, p)
    if not a:
        return []
    inv = pow(a[-1], -1, p)
    return [x * inv % p for x in a]


def gcd_p(a: Sequence[int], b: Sequence[int], p: int) -> Poly:
    """The monic gcd in (Z/pZ)[x], by the Euclidean algorithm."""
    a, b = reduce_p(a, p), reduce_p(b, p)
    while b:
        a, b = b, rem(a, b, p)
    return monic(a, p)


def powmod(a: Sequence[int], e: int, f: Sequence[int], p: int) -> Poly:
    """a^e mod f in (Z/pZ)[x], by binary exponentiation (a loop)."""
    result = rem([1], f, p)
    base = rem(a, f, p)
    while e > 0:
        if e & 1:
            result = rem(mul(result, base, p), f, p)
        base = rem(mul(base, base, p), f, p)
        e >>= 1
    return result


def derivative(a: Sequence[int], p: int) -> Poly:
    return reduce_p([i * a[i] for i in range(1, len(a))], p)


def berlekamp_matrix(f: Sequence[int], p: int) -> List[List[int]]:
    """The n x n matrix Q whose row i holds the coefficients of x^(p i) mod f."""
    n = len(f) - 1
    xp = powmod([0, 1], p, f, p)
    rows: List[List[int]] = []
    cur: Poly = [1]
    for _ in range(n):
        rows.append(cur + [0] * (n - len(cur)))
        cur = rem(mul(cur, xp, p), f, p)
    return rows


def left_null_space(a: Sequence[Sequence[int]], p: int) -> List[Poly]:
    """A basis of the vectors v with v a = 0 over Z/pZ, by Gauss-Jordan elimination.

    The basis vector for the free variable j has a 1 at position j and zeros
    at the other free positions; they are returned in increasing order of j.
    """
    n = len(a)
    m = [[a[i][j] % p for i in range(n)] for j in range(len(a[0]))]  # transpose: m v = 0
    pivots: List[int] = []
    row = 0
    for col in range(n):
        piv = next((r for r in range(row, len(m)) if m[r][col]), None)
        if piv is None:
            continue
        m[row], m[piv] = m[piv], m[row]
        inv = pow(m[row][col], p - 2, p)
        m[row] = [x * inv % p for x in m[row]]
        for r in range(len(m)):
            if r != row and m[r][col]:
                c = m[r][col]
                m[r] = [(x - c * y) % p for x, y in zip(m[r], m[row])]
        pivots.append(col)
        row += 1
    free = [j for j in range(n) if j not in pivots]
    basis: List[Poly] = []
    for j in free:
        v = [0] * n
        v[j] = 1
        for r, col in enumerate(pivots):
            v[col] = (-m[r][j]) % p
        basis.append(v)
    return basis


def berlekamp_factorization(f: Sequence[int], p: int, method: Optional[str] = None,
                            rng: Optional[random.Random] = None,
                            stats: Optional[dict] = None) -> List[Poly]:
    """Return the monic irreducible factors of a monic square-free f, sorted.

    method is "deterministic" (gcds with v - s for all s) or "random"
    (powers (p - 1)/2 of random elements of the algebra); the default is
    deterministic for p <= SMALL_P. If stats is a dict, it receives the
    matrix Q, the basis and the number r of factors.
    """
    f = reduce_p(f, p)
    if not f or f[-1] != 1:
        raise ValueError("f must be monic")
    if len(f) <= 1:
        return []
    if len(gcd_p(f, derivative(f, p), p)) > 1:
        raise ValueError("f must be square-free")
    if method is None:
        method = "deterministic" if p <= SMALL_P else "random"
    if method == "random" and p == 2:
        method = "deterministic"
    n = len(f) - 1  # @line L1
    q = berlekamp_matrix(f, p)  # @line L1
    a = [[(q[i][j] - (i == j)) % p for j in range(n)] for i in range(n)]  # @line L2
    basis = [trim(v) for v in left_null_space(a, p)]  # @line L2
    r = len(basis)  # @line L2
    if stats is not None:
        stats.update(q=q, basis=basis, r=r)
    if method == "random":
        return _random_split(f, p, basis, rng or random.Random(1))
    factors = [f]  # @line L3
    for v in basis[1:]:  # @line L4
        if len(factors) == r:  # @line L4
            break
        new: List[Poly] = []  # @line L5
        for h in factors:  # @line L6
            if len(h) == 2:
                new.append(h)
                continue
            for s in range(p):  # @line L7
                g = gcd_p(sub(v, [s], p), h, p)  # @line L8
                if len(g) > 1:  # @line L8
                    new.append(g)  # @line L8
        factors = new  # @line L9
    return sorted(factors, key=lambda g: (len(g), g))  # @line L10


def _random_split(f: Poly, p: int, basis: List[Poly], rng: random.Random) -> List[Poly]:
    """Split with gcd(a^((p - 1)/2) - 1, h) for random a in the Berlekamp algebra (odd p)."""
    r = len(basis)
    factors = [f]
    e = (p - 1) // 2
    rounds = 0
    while len(factors) < r:
        rounds += 1
        if rounds > 64 * (r + 4):
            raise RuntimeError("no split found")
        a: Poly = []
        for v in basis:
            c = rng.randrange(p)
            a = add(a, [c * x % p for x in v], p)
        new: List[Poly] = []
        for h in factors:
            if len(h) == 2:
                new.append(h)
                continue
            g = gcd_p(sub(powmod(a, e, h, p), [1], p), h, p)
            if 1 < len(g) < len(h):
                new.extend([g, divmod_p(h, g, p)[0]])
            else:
                new.append(h)
        factors = new
    return sorted(factors, key=lambda g: (len(g), g))
