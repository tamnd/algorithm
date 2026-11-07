# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/equal-degree-factorization/. The authors are listed in prov/H77D0W.jsonl.

"""Equal-degree factorization over Z/pZ: split a product of irreducibles of one degree d.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n] of ints
in 0 .. p - 1, lowest degree first; the zero polynomial is []. p must be a
prime.

For odd p, a random a modulo f gives b = a^((p^d - 1)/2), which is 0, 1 or
-1 modulo each irreducible factor, and gcd(b - 1, f) is a proper factor with
probability at least 1/2 - 1/(2 p^d) or so. For p = 2 the trace
a + a^2 + ... + a^(2^(d-1)) takes the values 0 and 1 instead. Pieces are kept
on an explicit stack, so there is no recursion.
"""

from __future__ import annotations

import random
from typing import List, Optional, Sequence, Tuple

Poly = List[int]


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


def splitting_element(a: Sequence[int], h: Sequence[int], d: int, p: int) -> Poly:
    """b = a^((p^d - 1)/2) mod h for odd p, and the trace a + a^2 + ... + a^(2^(d-1)) mod h for p = 2."""
    if p == 2:
        b = rem(a, h, p)
        t = b
        for _ in range(d - 1):
            t = rem(mul(t, t, p), h, p)
            b = add(b, t, p)
        return b
    return powmod(a, (p ** d - 1) // 2, h, p)


def split_once(h: Sequence[int], d: int, p: int, rng: random.Random) -> Optional[Poly]:
    """One random splitting attempt; returns a proper monic factor of h, or None."""
    a = trim([rng.randrange(p) for _ in range(len(h) - 1)])  # @line L5
    if len(a) <= 1:  # @line L5
        return None
    g = gcd_p(a, h, p)  # @line L6
    if len(g) > 1:  # @line L6
        return g
    b = splitting_element(a, h, d, p)  # @line L7
    g = gcd_p(sub(b, [1], p), h, p)  # @line L8
    if 1 < len(g) < len(h):  # @line L9
        return g
    return None


def equal_degree_factorization(f: Sequence[int], d: int, p: int,
                               rng: Optional[random.Random] = None,
                               stats: Optional[dict] = None) -> List[Poly]:
    """Return the monic irreducible factors of f, sorted.

    f must be monic, square-free, and a product of irreducibles of degree d.
    rng is the source of random elements (default: a fixed seed). If stats is
    a dict, stats["attempts"] counts the splitting attempts.
    """
    f = reduce_p(f, p)
    if not f or f[-1] != 1:
        raise ValueError("f must be monic")
    if d < 1 or (len(f) - 1) % d:
        raise ValueError("the degree of f must be a multiple of d")
    rng = rng or random.Random(1)
    out: List[Poly] = []
    stack = [f] if len(f) > 1 else []  # @line L1
    attempts = 0
    while stack:  # @line L2
        h = stack.pop()  # @line L3
        if len(h) - 1 == d:  # @line L4
            out.append(h)  # @line L4
            continue
        while True:
            attempts += 1
            g = split_once(h, d, p, rng)
            if g is not None:
                break
            if attempts > 200 * (len(f) + 10):
                raise ValueError("no split found: f is not a product of distinct irreducibles of degree d")
        stack.append(g)  # @line L9
        stack.append(divmod_p(h, g, p)[0])  # @line L9
    if stats is not None:
        stats["attempts"] = attempts
    return sorted(out, key=lambda g: (len(g), g))  # @line L10
