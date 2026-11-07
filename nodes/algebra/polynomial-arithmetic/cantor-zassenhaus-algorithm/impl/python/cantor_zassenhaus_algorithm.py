# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cantor-zassenhaus-algorithm/. The authors are listed in prov/1P1SGK.jsonl.

"""The Cantor-Zassenhaus algorithm: factor a polynomial over Z/pZ completely.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n] of ints
in 0 .. p - 1, lowest degree first; the zero polynomial is []. p must be a
prime.

The pipeline is: make f monic; split it into square-free parts with gcds
and p-th roots; split each part by degree (distinct-degree factorization);
split each degree part into irreducibles with random gcds (equal-degree
factorization). For p = 2 the random power is replaced by a trace. All loops
are iterative.
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


def pth_root(a: Sequence[int], p: int) -> Poly:
    """Return r with r^p = a, for a whose exponents are all multiples of p.

    Over Z/pZ every coefficient c satisfies c^p = c, so r has the
    coefficients of a at the exponents 0, p, 2p, ...
    """
    if any(a[i] for i in range(len(a)) if i % p):
        raise ValueError("a is not a p-th power")
    return trim([a[i] for i in range(0, len(a), p)])


def distinct_degree(f: Sequence[int], p: int) -> List[Tuple[Poly, int]]:
    """Distinct-degree factorization of a monic square-free f: the pairs (g_i, i)."""
    out: List[Tuple[Poly, int]] = []
    h = rem([0, 1], f, p)
    r, i = list(f), 0
    while len(r) - 1 >= 2 * (i + 1):
        i += 1
        h = powmod(h, p, r, p)
        g = gcd_p(sub(h, [0, 1], p), r, p)
        if len(g) > 1:
            out.append((g, i))
            r = divmod_p(r, g, p)[0]
            h = rem(h, r, p)
    if len(r) > 1:
        out.append((r, len(r) - 1))
    return out


def splitting_element(a: Sequence[int], h: Sequence[int], d: int, p: int) -> Poly:
    """a^((p^d - 1)/2) mod h for odd p; the trace a + a^2 + ... + a^(2^(d-1)) mod h for p = 2."""
    if p == 2:
        b = rem(a, h, p)
        t = b
        for _ in range(d - 1):
            t = rem(mul(t, t, p), h, p)
            b = add(b, t, p)
        return b
    return powmod(a, (p ** d - 1) // 2, h, p)


def equal_degree(f: Sequence[int], d: int, p: int, rng: random.Random, stats: dict) -> List[Poly]:
    """Equal-degree factorization of a monic square-free f whose factors all have degree d."""
    out: List[Poly] = []
    stack = [list(f)]
    limit = 200 * (len(f) + 10)
    tries = 0
    while stack:
        h = stack.pop()
        if len(h) - 1 == d:
            out.append(h)
            continue
        while True:
            tries += 1
            stats["attempts"] = stats.get("attempts", 0) + 1
            if tries > limit:
                raise RuntimeError("no split found")
            a = trim([rng.randrange(p) for _ in range(len(h) - 1)])
            if len(a) <= 1:
                continue
            g = gcd_p(a, h, p)
            if len(g) > 1:
                break
            g = gcd_p(sub(splitting_element(a, h, d, p), [1], p), h, p)
            if 1 < len(g) < len(h):
                break
        stack.append(g)
        stack.append(divmod_p(h, g, p)[0])
    return out


def cantor_zassenhaus(f: Sequence[int], p: int, rng: Optional[random.Random] = None,
                      stats: Optional[dict] = None) -> Tuple[int, List[Tuple[Poly, int]]]:
    """Factor f over Z/pZ as c * q_1^e_1 * ... * q_k^e_k.

    Returns (c, [(q_1, e_1), ...]) with c the leading coefficient and the q_i
    distinct monic irreducibles, sorted by degree and then by coefficients.
    rng is the source of random elements (default: a fixed seed). If stats
    is a dict, it receives the number of splitting attempts and the pieces.
    """
    f = reduce_p(f, p)
    if not f:
        raise ValueError("the zero polynomial has no factorization")
    rng = rng or random.Random(1)
    stats = {} if stats is None else stats
    stats.setdefault("attempts", 0)
    stats["square_free"] = []
    stats["degree_parts"] = []
    c = f[-1]  # @line L1
    result: List[Tuple[Poly, int]] = []  # @line L1
    work = [(monic(f, p), 1)]  # @line L1
    while work:  # @line L2
        u, k = work.pop()  # @line L3
        v = gcd_p(u, derivative(u, p), p)  # @line L3
        w = divmod_p(u, v, p)[0]  # @line L3
        i = 1  # @line L3
        while len(w) > 1:  # @line L4
            y = gcd_p(w, v, p)  # @line L5
            s = divmod_p(w, y, p)[0]  # @line L5
            if len(s) > 1:  # @line L6
                stats["square_free"].append((s, i * k))
                for g, d in distinct_degree(s, p):  # @line L7
                    stats["degree_parts"].append((g, d))
                    for q in equal_degree(g, d, p, rng, stats):  # @line L8
                        result.append((q, i * k))  # @line L8
            w = y  # @line L9
            v = divmod_p(v, y, p)[0]  # @line L9
            i += 1  # @line L9
        if len(v) > 1:  # @line L10
            work.append((pth_root(v, p), p * k))  # @line L10
    result.sort(key=lambda t: (len(t[0]), t[0]))  # @line L11
    return c, result  # @line L11
