# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frank-tardos-algorithm/. The authors are listed in prov/JSEDZ0.jsonl.

from collections.abc import Sequence
from fractions import Fraction

Num = int | Fraction


def dot(u: Sequence[Num], v: Sequence[Num]) -> Fraction:
    return sum((Fraction(p) * q for p, q in zip(u, v)), Fraction(0))


def lll(basis: list[list[Fraction]]) -> list[list[Fraction]]:
    """LLL reduction (delta = 3/4) of rational row vectors in the standard inner product."""
    b = [list(v) for v in basis]
    n = len(b)

    def gso():
        star, mu, norms = [], [[Fraction(0)] * n for _ in range(n)], []
        for i in range(n):
            v = list(b[i])
            for j in range(i):
                mu[i][j] = dot(b[i], star[j]) / norms[j]
                v = [x - mu[i][j] * y for x, y in zip(v, star[j])]
            star.append(v)
            norms.append(dot(v, v))
        return mu, norms

    k = 1
    while k < n:
        mu, norms = gso()
        for j in range(k - 1, -1, -1):
            r = round(mu[k][j])
            if r != 0:  # size reduction; b_k* and the norms do not change
                b[k] = [x - r * y for x, y in zip(b[k], b[j])]
                for i in range(j):
                    mu[k][i] -= r * mu[j][i]
                mu[k][j] -= r
        if norms[k] >= (Fraction(3, 4) - mu[k][k - 1] ** 2) * norms[k - 1]:
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]
            k = max(k - 1, 1)
    return b


def simultaneous_approximation(v: Sequence[Fraction], eps: Fraction) -> tuple[int, list[int]]:
    """Integers q >= 1 and p with max |q v_j - p_j| <= eps and q <= 2^k eps^(-n), k = ceil(n(n+1)/4)."""
    n = len(v)
    k = -(-n * (n + 1) // 4)
    delta = eps ** (n + 1) / 2**k
    rows = [[Fraction(int(i == j)) for j in range(n)] + [Fraction(0)] for i in range(n)]
    rows.append([-Fraction(x) for x in v] + [delta])
    first = lll(rows)[0]
    q = first[n] / delta
    if q < 0:
        first, q = [-x for x in first], -q
    p = [first[j] + q * v[j] for j in range(n)]
    assert q.denominator == 1 and all(x.denominator == 1 for x in p)
    return int(q), [int(x) for x in p]


def frank_tardos(w: Sequence[Num], big_n: int, trace: list | None = None) -> list[int]:
    """An integer vector u with sign(w b) = sign(u b) for every integer b with |b|_1 <= big_n - 1."""
    n = len(w)
    eps = Fraction(1, big_n)
    ps: list[list[int]] = []
    d = [Fraction(x) for x in w]  # @line L1
    while any(d):  # @line L2
        top = max(abs(x) for x in d)
        v = [x / top for x in d]  # @line L3
        q, p = simultaneous_approximation(v, eps)  # @line L4
        ps.append(p)  # @line L5
        d = [q * x - y for x, y in zip(v, p)]  # @line L6
        if trace is not None:
            trace.append((tuple(v), q, tuple(p), tuple(d)))
    if not ps:
        return [0] * n
    m = (big_n - 1) * max(abs(x) for p in ps for x in p) + 1  # @line L7
    t = len(ps)
    return [sum(m ** (t - 1 - i) * ps[i][j] for i in range(t)) for j in range(n)]  # @line L8
