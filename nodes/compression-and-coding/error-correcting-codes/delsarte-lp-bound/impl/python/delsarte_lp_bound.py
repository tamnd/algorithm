# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/delsarte-lp-bound/. The authors are listed in prov/P5EAGN.jsonl.

"""Delsarte's linear programming bound for codes in the Hamming space, solved exactly
with a simplex method over Fractions (Bland's rule, so it cannot cycle).

LP (q-ary, length n, minimum distance d):
    maximize   sum_{i in I} A_i            with I = {d, ..., n}
    subject to sum_{i in I} A_i K_k(i) >= -K_k(0)   for k = 1, ..., n
               A_i >= 0.
Then A_q(n, d) <= 1 + the optimum. With even=True (binary, d even) I keeps only even i.
"""

from fractions import Fraction
from itertools import combinations
from math import comb


def krawtchouk(n: int, k: int, x: int, q: int = 2) -> int:
    """K_k(x) = sum_j (-1)^j (q - 1)^(k - j) C(x, j) C(n - x, k - j)."""
    return sum((-1) ** j * (q - 1) ** (k - j) * comb(x, j) * comb(n - x, k - j) for j in range(k + 1))


def simplex_max(c: list[Fraction], m: list[list[Fraction]], b: list[Fraction]):
    """Maximize c.x subject to m x <= b, x >= 0, with b >= 0, by the tableau simplex
    method with Bland's rule. Exact over Fractions.

    Returns (optimum, x, y) where y is an optimal dual solution (m^T y >= c, y >= 0,
    b.y = optimum). Raises ValueError if the LP is unbounded.
    """
    rows, nv = len(m), len(c)
    assert all(bi >= 0 for bi in b)
    # tableau columns: nv decision variables, rows slacks, then the right-hand side
    t = [[Fraction(x) for x in m[i]] + [Fraction(int(i == j)) for j in range(rows)] + [Fraction(b[i])]
         for i in range(rows)]
    obj = [-Fraction(x) for x in c] + [Fraction(0)] * rows + [Fraction(0)]
    basis = [nv + i for i in range(rows)]
    while True:
        enter = next((j for j in range(nv + rows) if obj[j] < 0), None)  # Bland: smallest index
        if enter is None:
            break
        best = None
        for i in range(rows):
            if t[i][enter] > 0:
                ratio = t[i][-1] / t[i][enter]
                if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                    best = (ratio, i)
        if best is None:
            raise ValueError("unbounded")
        r = best[1]
        piv = t[r][enter]
        t[r] = [x / piv for x in t[r]]
        for i in range(rows):
            if i != r and t[i][enter] != 0:
                f = t[i][enter]
                t[i] = [x - f * y for x, y in zip(t[i], t[r])]
        if obj[enter] != 0:
            f = obj[enter]
            obj = [x - f * y for x, y in zip(obj, t[r])]
        basis[r] = enter
    x = [Fraction(0)] * nv
    for i, v in enumerate(basis):
        if v < nv:
            x[v] = t[i][-1]
    y = obj[nv:nv + rows]
    return obj[-1], x, y


def delsarte_lp(n: int, d: int, q: int = 2, even: bool = False):
    """Solve the Delsarte LP. Returns (bound, A, f) with bound = 1 + optimum (a Fraction),
    A = {i: A_i} an optimal distance distribution, and f the dual coefficients
    [f_1, ..., f_n] of the polynomial 1 + sum_k f_k K_k(x)."""
    idx = [i for i in range(d, n + 1) if not (even and i % 2)]
    c = [Fraction(1)] * len(idx)
    m = [[Fraction(-krawtchouk(n, k, i, q)) for i in idx] for k in range(1, n + 1)]
    b = [Fraction(krawtchouk(n, k, 0, q)) for k in range(1, n + 1)]
    opt, x, y = simplex_max(c, m, b)
    return 1 + opt, dict(zip(idx, x)), y


def check_dual_certificate(n: int, d: int, f: list[Fraction], q: int = 2, even: bool = False) -> Fraction:
    """Delsarte's dual form: if f_k >= 0 and F(i) = 1 + sum_k f_k K_k(i) <= 0 for every i
    in the index set, then A_q(n, d) <= F(0). Returns F(0) after checking the conditions."""
    assert all(fk >= 0 for fk in f)
    def big_f(x: int) -> Fraction:
        return 1 + sum(fk * krawtchouk(n, k, x, q) for k, fk in enumerate(f, start=1))
    for i in range(d, n + 1):
        if even and i % 2:
            continue
        assert big_f(i) <= 0
    return big_f(0)


def distance_distribution(words: list[tuple[int, ...]], n: int) -> list[Fraction]:
    """A_i = (1/|C|) #{(x, y) in C^2 : d(x, y) = i}, for i = 0..n."""
    a = [0] * (n + 1)
    for x, y in combinations(words, 2):
        a[sum(u != v for u, v in zip(x, y))] += 2
    a[0] += len(words)
    return [Fraction(v, len(words)) for v in a]


def delsarte_inequalities(dist: list[Fraction], n: int, q: int = 2) -> list[Fraction]:
    """B_k = sum_i A_i K_k(i) for k = 0..n. Delsarte: all are >= 0 for every code."""
    return [sum(a * krawtchouk(n, k, i, q) for i, a in enumerate(dist)) for k in range(n + 1)]
