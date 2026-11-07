# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ben-or-tiwari-algorithm/. The authors are listed in prov/RHYB1V.jsonl.

"""Ben-Or and Tiwari sparse interpolation over Q.

The black box f takes a tuple of n integers and returns the value of an unknown
polynomial f in Q[x_1, ..., x_n] with at most T terms, as an int or Fraction.
ben_or_tiwari(f, n, T) returns f as a dict from exponent tuples to nonzero
Fractions, using exactly 2T evaluations at the points (p_1^i, ..., p_n^i),
i = 0, ..., 2T - 1, where p_1, ..., p_n are the first n primes.

Cost model: operations in Q, plus 2T calls to the black box. Berlekamp-Massey
costs O(T^2), the transposed Vandermonde system O(t^2), and the integer roots
are found by brute force modulo a small prime q and Newton (Hensel) lifting,
O(q t + t^2 log(d T)) operations on integers of O(d T log p_n) digits, where t
is the true number of terms and d the total degree. Precondition: T >= t.
"""

from fractions import Fraction
from typing import Callable, Dict, List, Sequence, Tuple, Union

Number = Union[int, Fraction]
Mono = Tuple[int, ...]


def is_prime(c: int) -> bool:
    return c > 1 and all(c % p for p in range(2, int(c ** 0.5) + 1))


def first_primes(k: int, start: int = 2) -> List[int]:
    """The first k primes that are at least start."""
    out: List[int] = []
    c = start
    while len(out) < k:
        if is_prime(c):
            out.append(c)
        c += 1
    return out


def berlekamp_massey(a: Sequence[Fraction]) -> List[Fraction]:
    """Connection polynomial C (C[0] = 1) of the shortest recurrence for a, over Q."""
    C: List[Fraction] = [Fraction(1)]
    B: List[Fraction] = [Fraction(1)]
    L, m, b = 0, 1, Fraction(1)
    for N in range(len(a)):
        d = a[N]
        for i in range(1, L + 1):
            d += C[i] * a[N - i]
        if d == 0:
            m += 1
            continue
        coef = d / b
        T = list(C)
        C = C + [Fraction(0)] * (len(B) + m - len(C))
        for i, v in enumerate(B):
            C[i + m] -= coef * v
        if 2 * L <= N:
            L, B, b, m = N + 1 - L, T, d, 1
        else:
            m += 1
    return (C + [Fraction(0)] * (L + 1))[: L + 1]


def peval(P: Sequence[int], z: int, mod: int = 0) -> int:
    """Horner evaluation of P (low degree first), optionally modulo mod."""
    v = 0
    for c in reversed(P):
        v = v * z + c
        if mod:
            v %= mod
    return v


def integer_roots(P: List[int]) -> List[int]:
    """The t distinct integer roots of a monic P of degree t that splits over Z with simple roots."""
    t = len(P) - 1
    dP = [i * P[i] for i in range(1, t + 1)]
    bound = 1 + max(abs(c) for c in P[:-1])
    q = max(2 * t + 3, 101)
    while True:
        q += 1
        if not is_prime(q):
            continue
        roots = [r for r in range(q) if peval(P, r, q) == 0]
        if len(roots) != t or any(peval(dP, r, q) == 0 for r in roots):
            continue
        out = []
        for r in roots:
            mod = q
            while mod <= 2 * bound:
                mod = mod * mod
                inv = pow(peval(dP, r, mod), -1, mod)
                r = (r - peval(P, r, mod) * inv) % mod
            if r > mod // 2:
                r -= mod
            out.append(r)
        if all(peval(P, r) == 0 for r in out):
            return sorted(out)


def solve_transposed_vandermonde(Lam: List[int], nodes: List[int], rhs: List[Fraction]) -> List[Fraction]:
    """Solve sum_j c_j nodes[j]^i = rhs[i] for i < t in O(t^2) operations.

    Lam is the monic polynomial with the distinct roots nodes (low degree first).
    With Lam_j = Lam / (z - m_j) = sum_i q_i z^i, sum_i q_i rhs[i] = c_j Lam'(m_j).
    """
    t = len(nodes)
    dLam = [i * Lam[i] for i in range(1, t + 1)]
    out: List[Fraction] = []
    for m in nodes:
        q = [0] * t
        acc = 0
        for i in range(t, 0, -1):
            acc = acc * m + Lam[i]
            q[i - 1] = acc
        s = sum((Fraction(qi) * r for qi, r in zip(q, rhs)), Fraction(0))
        out.append(s / peval(dLam, m))
    return out


def ben_or_tiwari(f: Callable[[Tuple[int, ...]], Number], n: int, T: int) -> Dict[Mono, Fraction]:
    """Interpolate a polynomial with at most T terms from 2T black-box values.

    Precondition: f is a polynomial over Q in n variables with at most T terms.
    Cost: 2T evaluations, O(T^2) operations in Q, and the integer root finding.
    """
    primes = first_primes(n)  # @line L1
    a = [Fraction(f(tuple(p ** i for p in primes))) for i in range(2 * T)]  # @line L2
    C = berlekamp_massey(a)  # @line L3
    t = len(C) - 1
    if t == 0:  # @line L4
        return {}
    Lam = [C[t - i] for i in range(t + 1)]
    assert all(c.denominator == 1 for c in Lam)
    P = [int(c) for c in Lam]
    m = integer_roots(P)  # @line L5
    exps: List[Mono] = []
    for v in m:  # @line L6
        e = []
        for p in primes:
            k = 0
            while v % p == 0:
                v //= p
                k += 1
            e.append(k)
        if v != 1:
            raise ValueError("the black box is not a polynomial with at most T terms")
        exps.append(tuple(e))
    c = solve_transposed_vandermonde(P, m, a[:t])  # @line L7
    return {e: cj for e, cj in zip(exps, c) if cj}  # @line L8
