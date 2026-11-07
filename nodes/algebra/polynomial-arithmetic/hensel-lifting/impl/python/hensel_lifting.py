# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hensel-lifting/. The authors are listed in prov/ZKSCMK.jsonl.

"""Quadratic Hensel lifting of a factorization f = g h modulo p to modulo p^k.

A polynomial a_0 + a_1 x + ... + a_n x^n is the list [a_0, ..., a_n] of
Python ints, lowest degree first; the zero polynomial is []. Residues modulo
m are kept in the range 0 .. m - 1.

The input is f in Z[x], a prime p, factors g, h with f = g h mod p, h monic,
g mod p and h mod p coprime, and the leading coefficient of f prime to p.
Each Hensel step goes from modulus m to modulus m^2, so ceil(log2 k) steps
reach p^k. The step itself (hensel_step) is valid for any integer modulus
m >= 2, prime or not. All loops are iterative.
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

Poly = List[int]


def trim(a: Sequence[int]) -> Poly:
    """Return a copy of a without trailing zero coefficients."""
    out = list(a)
    while out and out[-1] == 0:
        out.pop()
    return out


def reduce_mod(a: Sequence[int], m: int) -> Poly:
    """Reduce every coefficient into 0 .. m - 1 and strip leading zeros."""
    return trim([c % m for c in a])


def symmetric(a: Sequence[int], m: int) -> Poly:
    """Map every coefficient into the symmetric range -m/2 < c <= m/2."""
    out = []
    for c in a:
        c %= m
        out.append(c - m if 2 * c > m else c)
    return trim(out)


def mul(a: Sequence[int], b: Sequence[int]) -> Poly:
    """Schoolbook product over Z."""
    if not a or not b:
        return []
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                c[i + j] += x * y
    return trim(c)


def add(a: Sequence[int], b: Sequence[int]) -> Poly:
    """Coefficientwise sum."""
    n = max(len(a), len(b))
    return trim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def sub(a: Sequence[int], b: Sequence[int]) -> Poly:
    """Coefficientwise difference a - b."""
    n = max(len(a), len(b))
    return trim([(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0) for i in range(n)])


def divmod_monic(a: Sequence[int], h: Sequence[int], m: int) -> Tuple[Poly, Poly]:
    """Divide a by the monic h with remainder, coefficients modulo m."""
    h = reduce_mod(h, m)
    if not h or h[-1] != 1:
        raise ValueError("the divisor must be monic modulo m")
    r = reduce_mod(a, m)
    e = len(h) - 1
    if len(r) <= e:
        return [], r
    q = [0] * (len(r) - e)
    for i in range(len(r) - 1, e - 1, -1):
        c = r[i] % m
        if c:
            q[i - e] = c
            for j in range(e + 1):
                r[i - e + j] = (r[i - e + j] - c * h[j]) % m
    return trim(q), reduce_mod(r[:e], m)


def cofactors_mod_p(g: Sequence[int], h: Sequence[int], p: int) -> Tuple[Poly, Poly]:
    """Return s, t with s g + t h = 1 mod p, deg s < deg h and deg t < deg g.

    Uses the extended Euclidean algorithm in (Z/pZ)[x]; p must be prime and
    g, h coprime modulo p.
    """
    r0, r1 = reduce_mod(g, p), reduce_mod(h, p)
    s0, s1 = [1], []
    t0, t1 = [], [1]
    while r1:
        inv = pow(r1[-1], -1, p)
        q = [0] * max(0, len(r0) - len(r1) + 1)
        r = list(r0)
        for i in range(len(r) - 1, len(r1) - 2, -1):
            c = r[i] * inv % p
            if c:
                q[i - len(r1) + 1] = c
                for j in range(len(r1)):
                    r[i - len(r1) + 1 + j] = (r[i - len(r1) + 1 + j] - c * r1[j]) % p
        q = trim(q)
        r0, r1 = r1, reduce_mod(r, p)
        s0, s1 = s1, reduce_mod(sub(s0, mul(q, s1)), p)
        t0, t1 = t1, reduce_mod(sub(t0, mul(q, t1)), p)
    if len(r0) != 1:
        raise ValueError("g and h are not coprime modulo p")
    inv = pow(r0[0], -1, p)
    return reduce_mod([c * inv for c in s0], p), reduce_mod([c * inv for c in t0], p)


def hensel_step(f, g, h, s, t, m):
    """One Hensel step: from f = g h, s g + t h = 1 mod m to the same mod m^2."""
    m2 = m * m
    e = reduce_mod(sub(f, mul(g, h)), m2)  # @line L4
    q, r = divmod_monic(mul(s, e), h, m2)  # @line L5
    g_new = reduce_mod(add(g, add(mul(t, e), mul(q, g))), m2)  # @line L6
    h_new = reduce_mod(add(h, r), m2)  # @line L6
    b = reduce_mod(sub(add(mul(s, g_new), mul(t, h_new)), [1]), m2)  # @line L7
    c, d = divmod_monic(mul(s, b), h_new, m2)  # @line L8
    s_new = reduce_mod(sub(s, d), m2)  # @line L9
    t_new = reduce_mod(sub(t, add(mul(t, b), mul(c, g_new))), m2)  # @line L9
    return g_new, h_new, s_new, t_new


def hensel_lift(f: Sequence[int], g: Sequence[int], h: Sequence[int], p: int, k: int,
                steps: list | None = None) -> Tuple[Poly, Poly]:
    """Lift f = g h mod p, with h monic and gcd(g, h) = 1 mod p, to f = g h mod p^k.

    Returns (g_k, h_k) with coefficients in 0 .. p^k - 1, h_k monic,
    g_k = g and h_k = h mod p. If steps is a list, the moduli and factors of
    every step are appended to it.
    """
    if k < 1:
        raise ValueError("k must be at least 1")
    f, g, h = trim(f), reduce_mod(g, p), reduce_mod(h, p)
    if not h or h[-1] != 1:
        raise ValueError("h must be monic modulo p")
    if reduce_mod(sub(f, mul(g, h)), p):
        raise ValueError("f is not g h modulo p")
    s, t = cofactors_mod_p(g, h, p)  # @line L1
    m = p  # @line L2
    pk = p ** k
    while m < pk:  # @line L3
        g, h, s, t = hensel_step(f, g, h, s, t, m)
        m = m * m  # @line L10
        if steps is not None:
            steps.append((m, list(g), list(h)))
    return reduce_mod(g, pk), reduce_mod(h, pk)  # @line L11


def lift_factors(f: Sequence[int], factors: Sequence[Sequence[int]], p: int, k: int) -> List[Poly]:
    """Lift f = lc(f) f_1 ... f_r mod p, all f_i monic and pairwise coprime mod p.

    Splits off one factor at a time (a linear factor tree). Returns monic
    f_1*, ..., f_r* with f = lc(f) f_1* ... f_r* mod p^k.
    """
    f = trim(f)
    pk = p ** k
    rest = reduce_mod(f, pk)
    lifted: List[Poly] = []
    for i, fi in enumerate(factors[:-1]):
        others = [f[-1] % p]
        for fj in factors[i + 1:]:
            others = reduce_mod(mul(others, fj), p)
        g_k, h_k = hensel_lift(rest, others, fi, p, k)
        lifted.append(h_k)
        rest = g_k
    if factors:
        inv = pow(rest[-1], -1, pk)
        lifted.append(reduce_mod([c * inv for c in rest], pk))
    return lifted


def lift_root(f: Sequence[int], a: int, p: int, k: int) -> int:
    """Lift a simple root a of f modulo p to the unique root modulo p^k congruent to a.

    This is the linear factor case h = x - a, done by the Newton step
    b <- b - f(b) / f'(b) modulo p^(2j).
    """
    f = trim(f)
    df = trim([i * c for i, c in enumerate(f)][1:])
    ev = lambda poly, x, m: _horner(poly, x, m)
    if ev(f, a, p) != 0 or ev(df, a, p) == 0:
        raise ValueError("a must be a simple root modulo p")
    b, m, pk = a % p, p, p ** k
    while m < pk:
        m = m * m
        b = (b - ev(f, b, m) * pow(ev(df, b, m), -1, m)) % m
    return b % pk


def _horner(a: Sequence[int], x: int, m: int) -> int:
    v = 0
    for c in reversed(a):
        v = (v * x + c) % m
    return v
