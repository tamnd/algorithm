# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zassenhaus-algorithm/. The authors are listed in prov/0Y712F.jsonl.
"""The Zassenhaus algorithm: factoring in Z[x] by factoring modulo p,
Hensel lifting, and recombination of the lifted factors over subsets.

Polynomials are lists of ints, lowest degree first; the zero polynomial is [].
"""

from __future__ import annotations

import random
from fractions import Fraction
from itertools import combinations
from math import gcd, isqrt
from typing import Sequence

Poly = list[int]


# ---------------------------------------------------------------- over Z


def _strip(a: list) -> list:
    while a and a[-1] == 0:
        a.pop()
    return a


def _mul(a: Sequence[int], b: Sequence[int]) -> Poly:
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[i + j] += x * y
    return _strip(c)


def _content(a: Sequence[int]) -> int:
    c = 0
    for x in a:
        c = gcd(c, x)
    return c


def _primitive(a: Poly) -> Poly:
    c = _content(a)
    if a[-1] < 0:
        c = -c
    return [x // c for x in a]


def _is_squarefree_over_q(f: Poly) -> bool:
    a = [Fraction(x) for x in f]
    b = _strip([Fraction(i * x) for i, x in enumerate(f)][1:])
    while b:
        r = list(a)
        while len(r) >= len(b):
            t = r[-1] / b[-1]
            k = len(r) - len(b)
            for j, y in enumerate(b):
                r[k + j] -= t * y
            r.pop()
            _strip(r)
        a, b = b, r
    return len(a) == 1


# ---------------------------------------------------------------- over F_p


def _red(a: Sequence[int], p: int) -> Poly:
    return _strip([x % p for x in a])


def _divmod_p(a: Sequence[int], b: Sequence[int], p: int) -> tuple[Poly, Poly]:
    r = _red(a, p)
    n = len(b) - 1
    if len(r) <= n:
        return [], r
    inv = pow(b[-1], -1, p)
    q = [0] * (len(r) - n)
    for k in range(len(r) - 1, n - 1, -1):
        t = r[k] * inv % p
        if t:
            q[k - n] = t
            for j in range(n + 1):
                r[k - n + j] = (r[k - n + j] - t * b[j]) % p
    return _strip(q), _strip(r[:n])


def _mulmod_p(a: Poly, b: Poly, f: Poly, p: int) -> Poly:
    return _divmod_p(_mul(a, b), f, p)[1]


def _powmod_p(a: Poly, e: int, f: Poly, p: int) -> Poly:
    result, base = _divmod_p([1], f, p)[1], _divmod_p(a, f, p)[1]
    while e:
        if e & 1:
            result = _mulmod_p(result, base, f, p)
        base = _mulmod_p(base, base, f, p)
        e >>= 1
    return result


def _monic_p(a: Poly, p: int) -> Poly:
    inv = pow(a[-1], -1, p)
    return [x * inv % p for x in a]


def _gcd_p(a: Poly, b: Poly, p: int) -> Poly:
    a, b = _red(a, p), _red(b, p)
    while b:
        a, b = b, _divmod_p(a, b, p)[1]
    return _monic_p(a, p) if a else []


def _sub_p(a: Poly, b: Poly, p: int) -> Poly:
    n = max(len(a), len(b))
    return _strip([((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p for i in range(n)])


def _equal_degree(f: Poly, d: int, p: int, rng: random.Random) -> list[Poly]:
    """Cantor-Zassenhaus splitting of a monic square-free f whose irreducible
    factors all have degree d. Iterative, with a work list."""
    out, work = [], [f]
    while work:
        g = work.pop()
        if len(g) - 1 == d:
            out.append(g)
            continue
        while True:
            a = [rng.randrange(p) for _ in range(len(g) - 1)]
            if len(_strip(list(a))) < 2:
                continue
            if p == 2:
                t, s = list(a), list(a)
                for _ in range(d - 1):
                    t = _mulmod_p(t, t, g, p)
                    s = _sub_p(s, [-x for x in t], p)
                h = _gcd_p(s, g, p)
            else:
                b = _powmod_p(a, (p ** d - 1) // 2, g, p)
                h = _gcd_p(_sub_p(b, [1], p), g, p)
            if 1 < len(h) < len(g):
                work.append(h)
                work.append(_divmod_p(g, h, p)[0])
                break
    return out


def factor_mod_p(f: Sequence[int], p: int, seed: int = 0) -> list[Poly]:
    """Monic irreducible factors of f in F_p[x].

    Precondition: p is prime, f mod p is square-free of degree at least 1.
    Cost: distinct-degree factorization, then Cantor-Zassenhaus splitting;
    expected O(n^3 log p) operations in F_p with the schoolbook products here.
    """
    g = _monic_p(_red(f, p), p)
    rng = random.Random(seed)
    out: list[Poly] = []
    h = [0, 1]
    d = 0
    while len(g) - 1 >= 2 * (d + 1):
        d += 1
        h = _powmod_p(h, p, g, p)
        c = _gcd_p(_sub_p(h, [0, 1], p), g, p)
        if len(c) > 1:
            out.extend(_equal_degree(c, d, p, rng))
            g = _divmod_p(g, c, p)[0]
            h = _divmod_p(h, g, p)[1]
    if len(g) > 1:
        out.append(g)
    return out


# ---------------------------------------------------------------- Hensel lifting


def _symmetric(a: Sequence[int], m: int) -> Poly:
    half = m // 2
    return _strip([(x % m) - m if (x % m) > half else (x % m) for x in a])


def _hensel_two(f: Poly, g: Poly, h: Poly, p: int, k: int) -> tuple[Poly, Poly]:
    """Lift f = g h (mod p), g monic, gcd(g, h) = 1 mod p, to f = g h (mod p^k)
    with g monic. Linear lifting: one power of p per step."""
    # t with t h = 1 (mod g, p): extended Euclid in F_p[x]
    r0, r1, t0, t1 = _red(g, p), _red(h, p), [], [1]
    while len(r1) > 1:
        q, r = _divmod_p(r0, r1, p)
        r0, r1 = r1, r
        t0, t1 = t1, _sub_p(t0, _mul(q, t1), p)
    inv = pow(r1[0], -1, p)
    t = [x * inv % p for x in t1]
    pj = p
    for _ in range(1, k):
        e = [x // pj for x in _sub_z(f, _mul(g, h))]
        a = _divmod_p(_mul(e, t), g, p)[1]
        b = _divmod_p(_sub_p(_red(e, p), _mul(a, h), p), g, p)[0]
        g = _add_z(g, [pj * x for x in a])
        h = _add_z(h, [pj * x for x in b])
        pj *= p
    return g, h


def _add_z(a: Poly, b: Poly) -> Poly:
    n = max(len(a), len(b))
    return _strip([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def _sub_z(a: Poly, b: Poly) -> Poly:
    return _add_z(a, [-x for x in b])


def hensel_lift(f: Poly, us: list[Poly], p: int, k: int) -> list[Poly]:
    """Monic v_i = u_i (mod p) with f = lc(f) v_1 ... v_r (mod p^k).

    Precondition: f = lc(f) u_1 ... u_r (mod p), the u_i monic and pairwise
    coprime modulo p, p not dividing lc(f).
    """
    m = p ** k
    lc = f[-1]
    out = []
    rest = list(f)
    for i in range(len(us) - 1):
        h = [lc % p]
        for u in us[i + 1:]:
            h = _red(_mul(h, u), p)
        g, rest = _hensel_two(rest, list(us[i]), h, p, k)
        out.append(_symmetric(g, m))
        rest = _symmetric(rest, m)
    inv = pow(lc, -1, m)
    out.append(_symmetric([x * inv for x in rest], m))
    return out


# ---------------------------------------------------------------- Zassenhaus


def _choose_prime(f: Poly) -> int:
    p = 2
    df = _strip([i * x for i, x in enumerate(f)][1:])
    while True:
        if all(p % d for d in range(2, isqrt(p) + 1)) and f[-1] % p:
            if len(_gcd_p(f, df, p)) == 1:
                return p
        p += 1


def _norm1(a: Poly) -> int:
    return sum(abs(x) for x in a)


def _lc_times(lc: int, vs: list[Poly], m: int) -> Poly:
    g = [lc]
    for v in vs:
        g = _symmetric(_mul(g, v), m)
    return g


def zassenhaus(f: Sequence[int]) -> list[Poly]:
    """The irreducible factors of f in Z[x], primitive with positive leading
    coefficients, whose product is f.

    Precondition: f is primitive, square-free, of degree n >= 1, with
    lc(f) > 0; a ValueError is raised otherwise.
    Cost: one factorization modulo a small prime p, Hensel lifting to
    p^k > 2 B with B = 2^n lc(f) ceil(||f||_2), and at most (r + 1) 2^r
    candidate pairs in the recombination for r factors modulo p, each
    costing two products modulo p^k. So it is exponential in r in the
    worst case and polynomial in n and the coefficient length otherwise.
    """
    f = _strip(list(f))
    if len(f) < 2 or f[-1] < 0 or _content(f) != 1 or not _is_squarefree_over_q(f):
        raise ValueError("f must be primitive, square-free, of degree >= 1, with lc(f) > 0")
    n = len(f) - 1
    p = _choose_prime(f)  # @line L1
    us = factor_mod_p(f, p)  # @line L2
    bound = (1 << n) * f[-1] * (isqrt(sum(c * c for c in f)) + 1)  # @line L3
    k = 1
    while p ** k <= 2 * bound:
        k += 1
    m = p ** k
    vs = hensel_lift(f, us, p, k)  # @line L4
    big_f, found, s = f, [], 1  # @line L5
    while 2 * s <= len(vs):  # @line L6
        hit = None
        for idx in combinations(range(len(vs)), s):  # @line L7
            g = _lc_times(big_f[-1], [vs[i] for i in idx], m)
            h = _lc_times(big_f[-1], [v for i, v in enumerate(vs) if i not in idx], m)
            if _norm1(g) * _norm1(h) <= bound:
                hit = (idx, g, h)
                break
        if hit is not None:  # @line L8
            idx, g, h = hit
            found.append(_primitive(g))
            big_f = _primitive(h)
            vs = [v for i, v in enumerate(vs) if i not in idx]
        else:
            s += 1  # @line L9
    return found + [big_f]  # @line L10
