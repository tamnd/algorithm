# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/arora-ge-algorithm/. The authors are listed in prov/SGHADM.jsonl.
"""The Arora-Ge linearization attack on LWE with errors from a small known set.

If every error lies in a known set E, each sample (a, b) satisfies
P(b - <a, s>) = 0 with P(t) = prod_{e in E} (t - e). This is a polynomial
equation of degree D = |E| in s. Replace each monomial s^alpha with
1 <= |alpha| <= D by a new unknown y_alpha; every sample gives one linear
equation in these N = C(n + D, D) - 1 unknowns. With enough samples the
linear system mod q has the unique solution y_alpha = s^alpha, and the
degree-1 unknowns are s.

For study only. The attack runs on toy sizes (n = 3 or 4, D = 3) and the
code is not constant time. To protect data use ML-KEM from a FIPS 140
validated module or a maintained library.
"""

import random
from math import comb, factorial
from typing import List, Optional, Sequence, Tuple

Monomial = Tuple[int, ...]


def poly_from_roots(E: Sequence[int], q: int) -> List[int]:
    """Coefficients p_0, ..., p_D of prod_{e in E} (t - e) mod q."""
    p = [1]
    for e in E:
        nxt = [0] * (len(p) + 1)
        for j, c in enumerate(p):
            nxt[j + 1] = (nxt[j + 1] + c) % q
            nxt[j] = (nxt[j] - e * c) % q
        p = nxt
    return p


def monomials(n: int, D: int) -> List[Monomial]:
    """All exponent vectors alpha in N^n with 1 <= |alpha| <= D, by degree."""
    out: List[Monomial] = []

    def build(prefix: List[int], left: int, i: int) -> None:
        if i == n - 1:
            out.append(tuple(prefix + [left]))
            return
        for x in range(left, -1, -1):
            build(prefix + [x], left - x, i + 1)

    for t in range(1, D + 1):
        build([], t, 0)
    return out


def multinomial(alpha: Monomial) -> int:
    r = factorial(sum(alpha))
    for x in alpha:
        r //= factorial(x)
    return r


def equation_row(a: Sequence[int], b: int, P: Sequence[int], mons: Sequence[Monomial], q: int) -> Tuple[List[int], int]:
    """Expand P(b - <a, s>) = c_0 + sum_alpha c_alpha s^alpha; return ([c_alpha], -c_0).

    With L = <a, s>: P(b - L) = sum_t c_t L^t, where
    c_t = (-1)^t sum_{j >= t} p_j C(j, t) b^(j - t), and the coefficient of
    s^alpha in L^t (|alpha| = t) is multinomial(alpha) prod_i a_i^alpha_i.
    """
    D = len(P) - 1
    c = [0] * (D + 1)
    for t in range(D + 1):
        acc = 0
        for j in range(t, D + 1):
            acc += P[j] * comb(j, t) * pow(b, j - t, q)
        c[t] = (-1) ** t * acc % q
    row = []
    for alpha in mons:
        term = c[sum(alpha)] * multinomial(alpha)
        for ai, k in zip(a, alpha):
            if k:
                term = term * pow(ai, k, q) % q
        row.append(term % q)
    return row, (-c[0]) % q


def solve_mod_prime(M: List[List[int]], rhs: List[int], q: int) -> Optional[List[int]]:
    """The unique solution of M y = rhs mod a prime q, or None.

    Gauss-Jordan elimination. Returns None if the system is inconsistent
    or if its solution is not unique (rank below the number of unknowns).
    """
    rows = [list(r) + [v] for r, v in zip(M, rhs)]
    ncols = len(M[0])
    r = 0
    pivots = []
    for col in range(ncols):
        piv = next((i for i in range(r, len(rows)) if rows[i][col] % q), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][col], -1, q)
        rows[r] = [x * inv % q for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][col]:
                f = rows[i][col]
                rows[i] = [(x - f * y) % q for x, y in zip(rows[i], rows[r])]
        pivots.append(col)
        r += 1
    if any(row[-1] for row in rows[r:]):
        return None  # inconsistent: some sample's error is outside E
    if r < ncols:
        return None  # not unique
    return [rows[i][-1] for i in range(ncols)]


def arora_ge(samples: Sequence[Tuple[Sequence[int], int]], E: Sequence[int], q: int) -> Optional[List[int]]:
    """Recover s from LWE samples whose errors all lie in E. None on failure."""
    n = len(samples[0][0])
    P = poly_from_roots(E, q)  # @line L1
    mons = monomials(n, len(E))  # @line L2
    M, rhs = [], []
    for a, b in samples:  # @line L3
        row, r = equation_row(a, b, P, mons, q)  # @line L4
        M.append(row)  # @line L5
        rhs.append(r)
    y = solve_mod_prime(M, rhs, q)  # @line L6
    if y is None:  # @line L7
        return None
    return [y[mons.index(tuple(1 if j == i else 0 for j in range(n)))] for i in range(n)]  # @line L8


def unknown_count(n: int, D: int) -> int:
    """N = C(n + D, D) - 1, the number of monomials of degree 1 to D."""
    return comb(n + D, D) - 1


def lwe_samples(n: int, m: int, q: int, E: Sequence[int], rng: random.Random, s: Optional[Sequence[int]] = None):
    """m samples (a, <a, s> + e mod q) with e uniform in E. Returns (samples, s)."""
    if s is None:
        s = [rng.randrange(q) for _ in range(n)]
    out = []
    for _ in range(m):
        a = [rng.randrange(q) for _ in range(n)]
        e = rng.choice(list(E))
        out.append((a, (sum(x * y for x, y in zip(a, s)) + e) % q))
    return out, list(s)
