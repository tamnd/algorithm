# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hessenberg-reduction/. The authors are listed in prov/H2T7HQ.jsonl.

import math
import random
from fractions import Fraction

from hessenberg_reduction import hessenberg

U = 2.0 ** -53


def fro(a):
    return math.sqrt(sum(abs(t) ** 2 for row in a for t in row))


def orth_error(q):
    n = len(q)
    return max(abs(sum(q[k][i].conjugate() * q[k][j] for k in range(n)) - (1 if i == j else 0)) for i in range(n) for j in range(n))


def recon_error(a, h, q):
    n = len(a)
    qh = [[sum(q[i][k] * h[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    m = [[sum(qh[i][k] * q[j][k].conjugate() for k in range(n)) for j in range(n)] for i in range(n)]
    return fro([[m[i][j] - a[i][j] for j in range(n)] for i in range(n)])


def is_hessenberg(h):
    return all(h[i][j] == 0 for i in range(len(h)) for j in range(len(h)) if i > j + 1)


def charpoly(a):
    n = len(a)
    a = [[Fraction(t) for t in row] for row in a]
    m = [[Fraction(0)] * n for _ in range(n)]
    c = [Fraction(1)]
    for k in range(1, n + 1):
        am = [[sum(a[i][l] * m[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        m = [[am[i][j] + (c[-1] if i == j else 0) for j in range(n)] for i in range(n)]
        am = [[sum(a[i][l] * m[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        c.append(-sum(am[i][i] for i in range(n)) / k)
    return c


def check(a, c=10):
    n = len(a)
    h, q = hessenberg(a)
    assert is_hessenberg(h)
    assert orth_error(q) <= c * n * U
    assert recon_error(a, h, q) <= c * n * n * U * max(fro(a), 1e-300) + 1e-300
    return h, q


def test_page_example():
    a = [[4.0, 1, 2, 3], [2, 3, 1, 1], [1, 2, 5, 1], [3, 1, 1, 2]]
    h, q = check(a)
    assert abs(h[1][0] + math.sqrt(14)) < 1e-14
    assert abs(sum(h[i][i] for i in range(4)) - 14) < 1e-13
    assert [q[0][j] for j in range(4)] == [1.0, 0.0, 0.0, 0.0]


def test_small_sizes():
    for a in ([[2.0]], [[1.0, 2.0], [3.0, 4.0]]):
        h, q = hessenberg(a)
        assert h == a and orth_error(q) == 0


def test_zero_and_already_hessenberg():
    z = [[0.0] * 5 for _ in range(5)]
    h, q = check(z)
    assert h == z
    t = [[1.0, 2, 3], [4, 5, 6], [0, 7, 8]]
    h, q = check(t)
    assert h == t


def test_zero_column_is_skipped():
    a = [[1.0, 2, 3, 4], [0, 5, 6, 7], [0, 8, 9, 1], [0, 2, 3, 4]]
    h, q = check(a)
    assert q[1][1] == 1.0  # the first step did nothing


def test_random_real():
    rng = random.Random(3141)
    for _ in range(40):
        n = rng.randint(1, 12)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        check(a)


def test_random_complex():
    rng = random.Random(2718)
    for _ in range(20):
        n = rng.randint(1, 8)
        a = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)] for _ in range(n)]
        check(a)


def test_symmetric_gives_tridiagonal():
    rng = random.Random(11)
    for _ in range(10):
        n = rng.randint(3, 10)
        b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        a = [[b[i][j] + b[j][i] for j in range(n)] for i in range(n)]
        h, _ = check(a)
        far = max([abs(h[i][j]) for i in range(n) for j in range(n) if j > i + 1] + [0.0])
        assert far <= 20 * n * U * fro(a)


def test_characteristic_polynomial_is_kept():
    rng = random.Random(77)
    for _ in range(10):
        n = rng.randint(2, 6)
        a = [[float(rng.randint(-4, 4)) for _ in range(n)] for _ in range(n)]
        h, _ = hessenberg(a)
        ca, ch = charpoly(a), charpoly(h)
        scale = max(1.0, fro(a)) ** n
        for x, y in zip(ca, ch):
            assert abs(float(x - y)) <= 1e3 * n * n * U * scale


def test_unreduced_subdiagonal_for_generic_input():
    rng = random.Random(5)
    a = [[rng.uniform(-1, 1) for _ in range(9)] for _ in range(9)]
    h, _ = hessenberg(a)
    assert all(abs(h[i + 1][i]) > 1e-8 for i in range(8))


def test_known_spectrum_trace_and_determinant():
    a = [[3.0, 1, -1], [-1, 5, 1], [-2, 2, 4]]  # S diag(2, 4, 6) S^-1
    h, _ = check(a)
    det = (h[0][0] * (h[1][1] * h[2][2] - h[1][2] * h[2][1]) - h[0][1] * (h[1][0] * h[2][2] - h[1][2] * h[2][0]) + h[0][2] * (h[1][0] * h[2][1] - h[1][1] * h[2][0]))
    assert abs(det - 48) < 1e-12 and abs(h[0][0] + h[1][1] + h[2][2] - 12) < 1e-13
