# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/guruswami-sudan/. The authors are listed in prov/S3KZM9.jsonl.
"""The Guruswami-Sudan list decoder for Reed-Solomon codes over a prime field GF(p).

The code is {(f(a_1), ..., f(a_n)) : deg f < k} for distinct points a_i in GF(p).
Given received values y_i and a multiplicity r >= 1, the decoder

1. finds a nonzero Q(x, y) of (1, k - 1)-weighted degree at most D with a zero
   of multiplicity r at every point (a_i, y_i), by linear algebra on the Hasse
   derivatives, and
2. finds every f with deg f < k and (y - f(x)) dividing Q(x, y), by the
   Roth-Ruckenstein recursion,

and returns those f that agree with y in at least t = floor(D / r) + 1 places.
Every f with that much agreement is found. With r = 1 this is Sudan's algorithm.

A bivariate polynomial Q is a list over j of lists over i: Q[j][i] is the
coefficient of x^i y^j. A univariate polynomial is a list, lowest degree first.
"""

from math import comb


def num_monomials(d: int, k: int) -> int:
    """N(D) = the number of (i, j) with i, j >= 0 and i + (k - 1) j <= D. Needs k >= 2."""
    return sum(d - (k - 1) * j + 1 for j in range(d // (k - 1) + 1))


def gs_parameters(n: int, k: int, r: int) -> tuple[int, int]:
    """(D, t): the least D with N(D) > n r (r + 1) / 2, and the guaranteed agreement t = D // r + 1."""
    constraints = n * r * (r + 1) // 2
    d = 0
    while num_monomials(d, k) <= constraints:
        d += 1
    return d, d // r + 1


def decoding_radius(n: int, k: int, r: int) -> int:
    """The number of errors the decoder corrects with multiplicity r: n - t."""
    return n - gs_parameters(n, k, r)[1]


def nullspace_vector(p: int, rows: list[list[int]], ncols: int) -> list[int]:
    """A nonzero x with rows * x = 0 over GF(p). Precondition: len(rows) < ncols."""
    m = [list(r) for r in rows]
    pivots: list[int] = []
    rk = 0
    for col in range(ncols):
        piv = next((i for i in range(rk, len(m)) if m[i][col]), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        inv = pow(m[rk][col], p - 2, p)
        prow = [v * inv % p for v in m[rk]]
        m[rk] = prow
        for i in range(len(m)):
            c = m[i][col]
            if i != rk and c:
                m[i] = [(v - c * w) % p for v, w in zip(m[i], prow)]
        pivots.append(col)
        rk += 1
    free = next(c for c in range(ncols) if c not in set(pivots))
    x = [0] * ncols
    x[free] = 1
    for i, col in enumerate(pivots):
        x[col] = (-m[i][free]) % p
    return x


def interpolate(p: int, xs: list[int], ys: list[int], k: int, r: int, d: int) -> list[list[int]]:
    """A nonzero Q of (1, k - 1)-weighted degree <= d with multiplicity >= r at every (x_i, y_i).

    The conditions are the Hasse derivatives
    Q^[u, v](a, b) = sum_{i, j} C(i, u) C(j, v) q_ij a^(i - u) b^(j - v) = 0 for u + v < r.
    """
    monos = [(i, j) for j in range(d // (k - 1) + 1) for i in range(d - (k - 1) * j + 1)]
    rows = []
    for a, b in zip(xs, ys):
        for u in range(r):
            for v in range(r - u):
                rows.append([comb(i, u) * comb(j, v) * pow(a, i - u, p) * pow(b, j - v, p) % p
                             if i >= u and j >= v else 0 for i, j in monos])
    sol = nullspace_vector(p, rows, len(monos))
    q = [[0] * (d + 1) for _ in range(d // (k - 1) + 1)]
    for (i, j), c in zip(monos, sol):
        q[j][i] = c
    return q


def _shift(p: int, q: list[list[int]], gamma: int) -> list[list[int]]:
    """Q(x, x y + gamma): the coefficient of y^l is x^l sum_{j >= l} C(j, l) gamma^(j - l) Q_j(x)."""
    width = max(len(row) for row in q)
    out = []
    for l in range(len(q)):
        acc = [0] * width
        for j in range(l, len(q)):
            c = comb(j, l) * pow(gamma, j - l, p) % p
            if c:
                for i, v in enumerate(q[j]):
                    acc[i] = (acc[i] + c * v) % p
        out.append([0] * l + acc)
    return out


def roth_ruckenstein(p: int, q: list[list[int]], k: int) -> list[list[int]]:
    """Every f with deg f < k such that y - f(x) divides Q(x, y), as k coefficients.

    The recursion fixes one coefficient of f per level: it divides Q by the
    highest power of x, takes the roots gamma of Q(0, y) (here by trying all
    of GF(p)), and goes on with Q(x, x y + gamma).
    """
    found: list[list[int]] = []

    def rec(cur: list[list[int]], prefix: list[int]) -> None:
        low = min((next(i for i, v in enumerate(row) if v) for row in cur if any(row)), default=None)
        if low is None:
            return  # Q = 0 cannot happen for the nonzero input
        cur = [row[low:] for row in cur]
        at_zero = [row[0] if row else 0 for row in cur]  # Q(0, y)
        for gamma in range(p):
            val = 0
            for c in reversed(at_zero):
                val = (val * gamma + c) % p
            if val:
                continue
            if len(prefix) + 1 == k:
                found.append(prefix + [gamma])
            else:
                rec(_shift(p, cur, gamma), prefix + [gamma])

    rec(q, [])
    return found


def peval(p: int, f: list[int], x: int) -> int:
    y = 0
    for c in reversed(f):
        y = (y * x + c) % p
    return y


def guruswami_sudan(p: int, xs: list[int], ys: list[int], k: int, r: int = 1) -> list[list[int]]:
    """All f with deg f < k that agree with (xs, ys) in at least t = D // r + 1 places.

    Precondition: p prime, the xs distinct elements of GF(p), 2 <= k <= n = len(xs), r >= 1.
    The radius n - t grows with r toward n - floor(sqrt(n (k - 1))) - 1.
    Cost: Gaussian elimination on about n r (r + 1) / 2 equations, O(n^3 r^6) field
    operations, and a root search with at most D / (k - 1) branches per level.
    """
    n = len(xs)
    d, _ = gs_parameters(n, k, r)  # @line L1
    t = d // r + 1  # @line L2
    q = interpolate(p, xs, ys, k, r, d)  # @line L3
    cands = roth_ruckenstein(p, q, k)  # @line L4
    out = []
    for f in cands:
        agree = sum(1 for a, b in zip(xs, ys) if peval(p, f, a) == b)
        if agree >= t and f not in out:  # @line L5
            out.append(f)
    return sorted(out)  # @line L6


def sudan(p: int, xs: list[int], ys: list[int], k: int) -> list[list[int]]:
    """Sudan's algorithm (1997): the case r = 1."""
    return guruswami_sudan(p, xs, ys, k, 1)
