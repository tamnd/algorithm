# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sylvester-matrix/. The authors are listed in prov/NEATH6.jsonl.
import itertools
import random
from fractions import Fraction

import pytest

from sylvester_matrix import SylvesterMatrix


def leibniz_det(A):
    """Determinant by the permutation expansion (independent oracle)."""
    N = len(A)
    total = 0
    for perm in itertools.permutations(range(N)):
        inv = sum(1 for a in range(N) for b in range(a + 1, N) if perm[a] > perm[b])
        prod = 1
        for r in range(N):
            prod *= A[r][perm[r]]
        total += -prod if inv % 2 else prod
    return total


def gauss_rank(A):
    """Rank over Q by Gaussian elimination with Fractions."""
    M = [[Fraction(x) for x in row] for row in A]
    rank, row = 0, 0
    N = len(M)
    for col in range(N):
        p = next((r for r in range(row, N) if M[r][col] != 0), None)
        if p is None:
            continue
        M[row], M[p] = M[p], M[row]
        for i in range(row + 1, N):
            q = M[i][col] / M[row][col]
            for j in range(col, N):
                M[i][j] -= q * M[row][j]
        row += 1
        rank += 1
    return rank


def from_roots(lead, roots):
    """Coefficients, highest first, of lead * prod (x - r)."""
    c = [lead]
    for r in roots:
        c = [a - r * b for a, b in zip(c + [0], [0] + c)]
    return c


def poly_gcd_degree(f, g):
    """Degree of gcd(f, g) over Q by the Euclidean algorithm."""
    def strip(p):
        p = [Fraction(x) for x in p]
        while p and p[0] == 0:
            p.pop(0)
        return p
    a, b = strip(f), strip(g)
    while b:
        while len(a) >= len(b) and a:
            q = a[0] / b[0]
            a = strip([x - q * y for x, y in zip(a, b + [0] * (len(a) - len(b)))])
        a, b = b, a
    return len(a) - 1


def naive_combine(f, g, s, t):
    """s f + t g by direct multiplication, highest first, padded to m + n."""
    m, n = len(f) - 1, len(g) - 1
    out = [0] * (m + n)
    for i, si in enumerate(s):
        for k, a in enumerate(f):
            out[i + k] += si * a
    for j, tj in enumerate(t):
        for k, b in enumerate(g):
            out[j + k] += tj * b
    return out


def test_example():
    f = [1, -3, 2]  # x^2 - 3x + 2 = (x - 1)(x - 2)
    g = [1, 0, 1]   # x^2 + 1
    S = SylvesterMatrix(f, g)
    assert S.to_dense() == [[1, -3, 2, 0], [0, 1, -3, 2], [1, 0, 1, 0], [0, 1, 0, 1]]
    assert S.determinant() == 10
    assert S.rank() == 4
    S.check_invariant()
    h = SylvesterMatrix([1, -3, 2], [1, 1, -2])  # common root x = 1
    assert h.determinant() == 0 and h.rank() == 3


def test_edges():
    assert SylvesterMatrix([5], [7]).determinant() == 1  # empty matrix
    assert SylvesterMatrix([3], [1, 2, 3]).determinant() == 9  # a0^n
    assert SylvesterMatrix([1, 2, 3], [3]).determinant() == 9  # b0^m
    assert SylvesterMatrix([0, 1, 1], [0, 1, 2]).determinant() == 0  # both formal leads zero
    assert SylvesterMatrix([0, 0], [1, 0]).determinant() == 0  # f = 0 with formal degree 1
    with pytest.raises(ValueError):
        SylvesterMatrix([], [1])
    with pytest.raises(IndexError):
        SylvesterMatrix([1, 1], [1, 1]).entry(2, 0)


def test_random_against_leibniz_and_combine():
    rng = random.Random(59)
    for _ in range(500):
        m, n = rng.randint(0, 3), rng.randint(0, 3)
        f = [rng.randint(-4, 4) for _ in range(m + 1)]
        g = [rng.randint(-4, 4) for _ in range(n + 1)]
        S = SylvesterMatrix(f, g)
        S.check_invariant()
        A = S.to_dense()
        assert S.determinant() == leibniz_det(A)
        assert S.rank() == gauss_rank(A)
        if f[0] != 0 or g[0] != 0:
            # rank = m + n - deg gcd once one formal leading coefficient is nonzero
            assert S.rank() == m + n - poly_gcd_degree(f, g)
        s = [rng.randint(-3, 3) for _ in range(n)]
        t = [rng.randint(-3, 3) for _ in range(m)]
        assert S.combine(s, t) == naive_combine(f, g, s, t)
        # Res(g, f) = (-1)^(m n) Res(f, g)
        assert SylvesterMatrix(g, f).determinant() == (-1) ** (m * n) * S.determinant()


def test_product_formula_and_gcd_rank():
    rng = random.Random(7)
    for _ in range(300):
        m, n = rng.randint(1, 4), rng.randint(1, 4)
        ra = [rng.randint(-3, 3) for _ in range(m)]
        rb = [rng.randint(-3, 3) for _ in range(n)]
        a, b = rng.choice([1, -1, 2, 3]), rng.choice([1, -2, 5])
        f, g = from_roots(a, ra), from_roots(b, rb)
        S = SylvesterMatrix(f, g)
        expected = a ** n * b ** m
        for x in ra:
            for y in rb:
                expected *= x - y
        assert S.determinant() == expected
        assert (S.determinant() == 0) == (poly_gcd_degree(f, g) >= 1)
        assert S.rank() == m + n - poly_gcd_degree(f, g)


def test_fractions_and_large_sizes():
    rng = random.Random(11)
    for _ in range(40):
        m, n = rng.randint(3, 7), rng.randint(3, 7)
        f = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(m + 1)]
        g = [Fraction(rng.randint(-9, 9), rng.randint(1, 5)) for _ in range(n + 1)]
        f[0] = f[0] or Fraction(1)
        g[0] = g[0] or Fraction(1)
        S = SylvesterMatrix(f, g)
        d = S.determinant()
        # Scaling: Res(c f, g) = c^n Res(f, g)
        assert SylvesterMatrix([3 * x for x in f], g).determinant() == 3 ** n * d
        assert (d == 0) == (poly_gcd_degree(f, g) >= 1)
        assert S.rank() == m + n - poly_gcd_degree(f, g)
