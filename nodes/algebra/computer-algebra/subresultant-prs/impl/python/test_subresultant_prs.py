# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subresultant-prs/. The authors are listed in prov/ESA0T9.jsonl.
import random
from fractions import Fraction

import pytest

from subresultant_prs import prem, subresultant_chain, subresultant_gcd


def det(M):
    M = [[Fraction(x) for x in r] for r in M]
    n, d = len(M), Fraction(1)
    for k in range(n):
        p = next((r for r in range(k, n) if M[r][k] != 0), None)
        if p is None:
            return 0
        if p != k:
            M[k], M[p] = M[p], M[k]
            d = -d
        d *= M[k][k]
        for i in range(k + 1, n):
            q = M[i][k] / M[k][k]
            for j in range(k, n):
                M[i][j] -= q * M[k][j]
    return d


def sres_det(f, g, j):
    """S_j from its definition by determinants of Sylvester submatrices."""
    m, n = len(f) - 1, len(g) - 1
    W = m + n - j
    rows = []
    for i in range(n - j):
        r = [0] * W
        for k, a in enumerate(f):
            r[i + k] = a
        rows.append(r)
    for i in range(m - j):
        r = [0] * W
        for k, b in enumerate(g):
            r[i + k] = b
        rows.append(r)
    base = [r[: m + n - 2 * j - 1] for r in rows]
    out = [det([b + [r[W - 1 - i]] for b, r in zip(base, rows)]) for i in range(j, -1, -1)]
    while out and out[0] == 0:
        out.pop(0)
    assert all(x.denominator == 1 for x in out)
    return [int(x) for x in out]


def q_gcd_monic(f, g):
    def strip(p):
        p = [Fraction(x) for x in p]
        while p and p[0] == 0:
            p.pop(0)
        return p
    a, b = strip(f), strip(g)
    while b:
        while a and len(a) >= len(b):
            q = a[0] / b[0]
            a = strip([x - q * y for x, y in zip(a, b + [0] * (len(a) - len(b)))])
        a, b = b, a
    return [x / a[0] for x in a] if a else []


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def rand_poly(rng, d, sparse):
    if sparse:
        p = [rng.choice([0, 0, 0, 1, -1, 2]) for _ in range(d + 1)]
    else:
        p = [rng.randint(-5, 5) for _ in range(d + 1)]
    p[0] = rng.choice([1, 2, -3])
    return p


def test_example():
    f = [1, -1, -1, -1, 0, 1]
    g = [1, -1, 0, -1, 0]
    S, last = subresultant_chain(f, g)
    assert S == [[-1], [], [-1], [-1, 0, 0, 1]]
    assert last == [-1]
    assert prem(f, g) == [-1, 0, 0, 1]
    assert prem(g, [-1, 0, 0, 1]) == [-1]
    for j in range(4):
        assert S[j] == sres_det(f, g, j)


def test_edges():
    with pytest.raises(ValueError):
        subresultant_chain([1, 2], [3])
    with pytest.raises(ValueError):
        subresultant_chain([1, 2], [1, 2, 3])
    assert subresultant_gcd([], []) == []
    assert subresultant_gcd([-2, 4], []) == [2, -4]
    assert subresultant_gcd([6, 3], [9]) == [3]
    assert subresultant_gcd([2, 4], [6, 0, -24]) == [2, 4]
    S, last = subresultant_chain([1, -3, 2], [1, -3, 2])  # f = g: equal degrees
    assert S == [[], []] and last == [1, -3, 2]
    S, _ = subresultant_chain([1, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1])  # one long first step
    assert S == [sres_det([1, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1], j) for j in range(2)]


def test_random_chain_against_determinants():
    rng = random.Random(1971)
    for t in range(500):
        m = rng.randint(1, 6)
        n = rng.randint(1, m)
        f, g = rand_poly(rng, m, t % 2 == 0), rand_poly(rng, n, t % 2 == 0)
        if t % 5 == 0:
            h = [1, rng.randint(-2, 2)]
            f, g = mul(f, h), mul(g, h)
        S, last = subresultant_chain(f, g)
        for j in range(len(g) - 1):
            assert S[j] == sres_det(f, g, j)
        # S_0 is the Sylvester determinant, the resultant.
        M = [[0] * (len(f) + len(g) - 2) for _ in range(len(f) + len(g) - 2)]
        for i in range(len(g) - 1):
            M[i][i:i + len(f)] = f
        for i in range(len(f) - 1):
            M[len(g) - 1 + i][i:i + len(g)] = g
        assert (S[0][0] if S[0] else 0) == det(M)


def test_gcd_against_euclid_over_q():
    rng = random.Random(1967)
    for t in range(500):
        h = rand_poly(rng, rng.randint(0, 3), False)
        a, b = rand_poly(rng, rng.randint(0, 4), t % 2), rand_poly(rng, rng.randint(0, 4), t % 3)
        f, g = mul(a, h), mul(b, h)
        G = subresultant_gcd(f, g)
        monic = q_gcd_monic(f, g)
        assert len(G) == len(monic) and G[0] > 0
        assert all(Fraction(x, G[0]) == y for x, y in zip(G, monic))
        for p in (f, g):  # G divides p in Z[x]
            p = list(p)
            while len(p) >= len(G):
                assert p[0] % G[0] == 0
                c = p[0] // G[0]
                for k in range(len(G)):
                    p[k] -= c * G[k]
                p.pop(0)
            assert not any(p)


def test_many_steps_with_bounded_size():
    f, g = [1], [1, 1]
    for _ in range(14):
        f, g = g, [a + b for a, b in zip(g + [0], [0] * (len(g) + 1 - len(f)) + f)]
    S, last = subresultant_chain([3 * x for x in g], f)
    norm = lambda p: sum(x * x for x in p)
    bound2 = norm([3 * x for x in g]) ** (len(f) - 1) * norm(f) ** (len(g) - 1)
    assert all(c * c <= bound2 for s in S for c in s)
    assert len(last) == 1
