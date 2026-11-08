# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-test/. The authors are listed in prov/81HMHG.jsonl.

from fractions import Fraction
from math import gamma, isqrt, pi


def dual_basis(a: int, m: int, t: int) -> list[list[int]]:
    """A basis of L*_t = {s in Z^t : s_1 + s_2 a + ... + s_t a^(t-1) = 0 mod m}."""
    rows = [[m] + [0] * (t - 1)]
    for j in range(1, t):
        row = [0] * t
        row[0] = -pow(a, j, m)
        row[j] = 1
        rows.append(row)
    return rows


def _dot(u, v):
    return sum(x * y for x, y in zip(u, v))


def _gram_schmidt(b):
    n = len(b)
    bstar, mu, norms = [], [[Fraction(0)] * n for _ in range(n)], []
    for i in range(n):
        v = [Fraction(x) for x in b[i]]
        for j in range(i):
            mu[i][j] = _dot(b[i], bstar[j]) / norms[j]
            v = [x - mu[i][j] * y for x, y in zip(v, bstar[j])]
        bstar.append(v)
        norms.append(_dot(v, v))
    return mu, norms


def lll_reduce(b: list[list[int]], delta: Fraction = Fraction(3, 4)) -> list[list[int]]:
    """Exact LLL reduction (Lenstra, Lenstra, Lovasz 1982) with rational arithmetic."""
    b = [list(r) for r in b]
    n, k = len(b), 1
    mu, norms = _gram_schmidt(b)
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                b[k] = [x - q * y for x, y in zip(b[k], b[j])]
                mu, norms = _gram_schmidt(b)
        if norms[k] >= (delta - mu[k][k - 1] ** 2) * norms[k - 1]:
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]
            mu, norms = _gram_schmidt(b)
            k = max(k - 1, 1)
    return b


def shortest_vector(b: list[list[int]]) -> tuple[int, list[int]]:
    """Squared length and a shortest non-zero vector of the lattice spanned by the rows of b.

    Exact enumeration (Fincke-Pohst): all coefficient vectors x with |sum x_i b_i|^2 <= R,
    where R starts at the shortest basis vector and shrinks whenever a shorter vector appears.
    """
    n = len(b)
    mu, norms = _gram_schmidt(b)
    best = min(range(n), key=lambda i: _dot(b[i], b[i]))
    best_len, best_vec = _dot(b[best], b[best]), list(b[best])
    x = [0] * n

    def search(k: int, partial: Fraction) -> None:
        nonlocal best_len, best_vec
        center = -sum((x[j] * mu[j][k] for j in range(k + 1, n)), Fraction(0))
        room = (best_len - partial) / norms[k]  # (x_k - center)^2 <= room
        if room < 0:
            return
        r = isqrt(room.numerator * room.denominator) // room.denominator + 1
        for xk in range(int(center) - r - 1, int(center) + r + 2):
            d = (xk - center) ** 2 * norms[k]
            if partial + d > best_len:
                continue
            x[k] = xk
            if k == 0:
                if any(x):
                    v = [sum(x[i] * b[i][c] for i in range(n)) for c in range(len(b[0]))]
                    length = _dot(v, v)
                    if 0 < length < best_len:
                        best_len, best_vec = length, v
            else:
                search(k - 1, partial + d)
        x[k] = 0

    search(n - 1, Fraction(0))
    return best_len, best_vec


def spectral_test(a: int, m: int, max_t: int = 6) -> dict[int, tuple[int, list[int], float]]:
    """For t = 2..max_t: (nu_t^2, a shortest dual vector s, mu_t).

    1/nu_t is the largest distance between adjacent parallel hyperplanes that cover
    all t-tuples (x_n, ..., x_(n+t-1))/m of the LCG x -> a x + c mod m.
    """
    out = {}
    for t in range(2, max_t + 1):  # @line L1
        basis = dual_basis(a, m, t)  # @line L2
        reduced = lll_reduce(basis)  # @line L3
        nu2, s = shortest_vector(reduced)  # @line L4
        mu = pi ** (t / 2) * nu2 ** (t / 2) / (gamma(t / 2 + 1) * m)  # @line L5
        out[t] = (nu2, s, mu)
    return out  # @line L6


def gauss_reduce_nu2(a: int, m: int) -> int:
    """nu_2^2 by Lagrange-Gauss reduction of the 2-dimensional dual lattice."""
    u, v = [m, 0], [-a % m, 1]
    if _dot(u, u) < _dot(v, v):
        u, v = v, u
    while True:
        # u is the longer vector; reduce it by the nearest multiple of v
        q = round(Fraction(_dot(u, v), _dot(v, v)))
        u = [x - q * y for x, y in zip(u, v)]
        if _dot(u, u) >= _dot(v, v):
            return _dot(v, v)
        u, v = v, u
