# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gosper-algorithm/. The authors are listed in prov/CAVQHD.jsonl.

import random
from fractions import Fraction
from typing import List, Optional, Tuple

import pytest

from gosper_algorithm import P, Poly, RatFun, gosper

# Independent polynomial helpers for the oracles (dense lists, lowest degree first).


def trim(a: List[Fraction]) -> List[Fraction]:
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def pmul(a: List[Fraction], b: List[Fraction]) -> List[Fraction]:
    if not a or not b:
        return []
    c = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)


def padd(a: List[Fraction], b: List[Fraction], s: int = 1) -> List[Fraction]:
    n = max(len(a), len(b))
    return trim([(a[i] if i < len(a) else 0) + s * (b[i] if i < len(b) else 0) for i in range(n)])  # type: ignore[misc]


def pev(a: List[Fraction], x: Fraction) -> Fraction:
    s = Fraction(0)
    for c in reversed(a):
        s = s * x + c
    return s


def pshift(a: List[Fraction], s: int) -> List[Fraction]:
    # binomial expansion of sum a_i (n + s)^i
    out = [Fraction(0)] * len(a)
    for i, c in enumerate(a):
        binom = 1
        for j in range(i + 1):
            out[j] += c * binom * Fraction(s) ** (i - j)
            binom = binom * (i - j) // (j + 1)
    return trim(out)


def from_roots(z: Fraction, roots: List[Fraction]) -> List[Fraction]:
    p = [Fraction(z)]
    for u in roots:
        p = pmul(p, [Fraction(-u), Fraction(1)])
    return p


def property_holds(num: Poly, den: Poly, y: RatFun, rng: random.Random) -> bool:
    """r(n) y(n+1) - y(n) = 1, as polynomials and at random points."""
    p, q = y
    p1, q1 = pshift(p, 1), pshift(q, 1)
    # num p1 q - den q1 p = den q1 q
    lhs = padd(pmul(pmul(num, p1), q), pmul(pmul(den, q1), p), -1)
    rhs = pmul(pmul(den, q1), q)
    if lhs != rhs:
        return False
    for _ in range(3):
        x = Fraction(rng.randint(-40, 40), rng.randint(1, 5))
        if pev(den, x) != 0 and pev(q, x) != 0 and pev(q1, x) != 0:
            if pev(num, x) / pev(den, x) * pev(p1, x) / pev(q1, x) - pev(p, x) / pev(q, x) != 1:
                return False
    return True


def solve_any(M: List[List[Fraction]], v: List[Fraction]) -> Optional[List[Fraction]]:
    """Some solution of M u = v by row reduction, or None."""
    rows, cols = len(M), len(M[0]) if M else 0
    A = [M[i][:] + [v[i]] for i in range(rows)]
    r, piv = 0, []
    for c in range(cols):
        p = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        for i in range(rows):
            if i != r and A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        piv.append((r, c))
        r += 1
    if any(A[i][cols] != 0 for i in range(r, rows)):
        return None
    u = [Fraction(0)] * cols
    for i, c in piv:
        u[c] = A[i][cols] / A[i][c]
    return u


def ansatz_summable(num_roots: List[Fraction], den_roots: List[Fraction], num: Poly, den: Poly) -> bool:
    """Oracle: search y = p/q with q = prod_{i=1..h} num(n - i), h the largest integer
    difference of a denominator root and a numerator root, and a generous degree for p."""
    h = max([int(b - a) for a in num_roots for b in den_roots if (b - a).denominator == 1 and b >= a] + [0])
    q = [Fraction(1)]
    for i in range(1, h + 1):
        q = pmul(q, pshift(num, -i))
    q1 = pshift(q, 1)
    d = max(len(num), len(den)) - 1
    m = (len(q) - 1) + d + h + 3
    # num(n) p(n+1) q(n) - den(n) p(n) q(n+1) = den(n) q(n) q(n+1)
    cols = []
    for j in range(m + 1):
        e = [Fraction(0)] * j + [Fraction(1)]
        cols.append(padd(pmul(pmul(num, pshift(e, 1)), q), pmul(pmul(den, e), q1), -1))
    rhs = pmul(pmul(den, q), q1)
    n_rows = max([len(c) for c in cols] + [len(rhs)])
    M = [[(c[i] if i < len(c) else Fraction(0)) for c in cols] for i in range(n_rows)]
    return solve_any(M, [rhs[i] if i < len(rhs) else Fraction(0) for i in range(n_rows)]) is not None


def partial_sums_agree(num: Poly, den: Poly, y: RatFun, N: int) -> bool:
    """Brute force: sum_{k<n} t(k) = z(n) - z(0) with t(0) = 1, t(k+1) = r(k) t(k)."""
    p, q = y
    t, s = Fraction(1), Fraction(0)
    ts = []
    for k in range(N + 1):
        ts.append(t)
        if pev(den, Fraction(k)) == 0:
            return True  # the term is not defined further; nothing more to compare
        t = t * pev(num, Fraction(k)) / pev(den, Fraction(k))
    if any(pev(q, Fraction(k)) == 0 for k in range(N + 1)):
        return True
    z = [pev(p, Fraction(k)) / pev(q, Fraction(k)) * ts[k] for k in range(N + 1)]
    for n in range(N + 1):
        if s != z[n] - z[0]:
            return False
        s += ts[n]
    return True


def test_worked_examples() -> None:
    rng = random.Random(1)
    # t = binom(2k, k) / 4^k: r = (2k + 1) / (2k + 2), y = 2k
    y = gosper(P(1, 2), P(2, 2))
    assert y == (P(0, 2), P(1))
    # t = k * k!: r = (k + 1)^2 / k, y = 1/k, so z = k!
    y = gosper(P(1, 2, 1), P(0, 1))
    assert y == (P(1), P(0, 1)) and property_holds(P(1, 2, 1), P(0, 1), y, rng)
    # t = 1/(k(k+1)): r = k/(k+2), y = -(k+1), so z = -1/k
    assert gosper(P(0, 1), P(2, 1)) == (P(-1, -1), P(1))
    # t = 1: y = n
    assert gosper(P(1), P(1)) == (P(0, 1), P(1))
    # k! and the harmonic term 1/(k+1) have no hypergeometric antidifference
    assert gosper(P(1, 1), P(1)) is None
    assert gosper(P(1, 1), P(2, 1)) is None
    # t = 2^k: y = 1
    assert gosper(P(2), P(1)) == (P(1), P(1))


def test_edge_cases() -> None:
    rng = random.Random(2)
    with pytest.raises(ValueError):
        gosper([], P(1))
    with pytest.raises(ValueError):
        gosper(P(1), [])
    # alternating sign: t = (-1)^k, y = -1/2
    assert gosper(P(-1), P(1)) == (P(Fraction(-1, 2)), P(1))
    # polynomial term t = k + 1: r = (k + 2)/(k + 1), z = k(k + 1)/2
    y = gosper(P(2, 1), P(1, 1))
    assert y is not None and property_holds(P(2, 1), P(1, 1), y, rng)
    # many reduction steps: t = Delta of (k+6)!/k!-type terms, shift 6
    num, den = P(1, 1), P(7, 1)  # r = (k+1)/(k+7): t = 6!/((k+1)...(k+6)), summable
    y = gosper(num, den)
    assert y is not None and property_holds(num, den, y, rng)
    assert partial_sums_agree(num, den, y, 30)


def rand_roots(rng: random.Random, k: int) -> List[Fraction]:
    return [Fraction(rng.choice([-3, -2, -1, 0, 1, 2, 3, 4, 5]), rng.choice([1, 1, 1, 2])) for _ in range(k)]


def test_random_against_ansatz() -> None:
    rng = random.Random(4242)
    found = 0
    for _ in range(270):
        nr, dr = rand_roots(rng, rng.randint(0, 2)), rand_roots(rng, rng.randint(0, 2))
        z = Fraction(rng.choice([1, 1, 1, 1, -1, 2]))
        num, den = from_roots(z, nr), from_roots(Fraction(1), dr)
        y = gosper(num, den)
        assert (y is not None) == ansatz_summable(nr, dr, num, den)
        if y is not None:
            found += 1
            assert property_holds(num, den, y, rng)
            assert partial_sums_agree(num, den, y, 12)
    assert found >= 20


def test_random_constructed_summable() -> None:
    """t = z(n+1) - z(n) for a random hypergeometric z, so t is Gosper-summable."""
    rng = random.Random(77)
    for _ in range(250):
        while True:
            u, v = rand_roots(rng, rng.randint(0, 2)), rand_roots(rng, rng.randint(0, 2))
            zc = Fraction(rng.choice([1, 2, 3, -1, Fraction(1, 2)]))
            rn, rd = from_roots(zc, u), from_roots(Fraction(1), v)
            if rn != rd:
                break
        # rho = rn/rd, t(n) = z(n)(rho(n) - 1), r(n) = rho(n) (rho(n+1) - 1) / (rho(n) - 1)
        num = pmul(rn, padd(pshift(rn, 1), pshift(rd, 1), -1))
        den = pmul(padd(rn, rd, -1), pshift(rd, 1))
        # an unreduced input: multiply both by the same factor
        num, den = pmul(num, rd), pmul(den, rd)
        y = gosper(num, den)
        assert y is not None
        assert property_holds(num, den, y, rng)
