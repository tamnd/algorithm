# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/divide-and-conquer-eigensolver/. The authors are listed in prov/J2346G.jsonl.
import math
import random
from fractions import Fraction

from divide_and_conquer_eigensolver import U, eigh_tridiagonal


def check(a, b, c=10.0):
    """Assert residual and orthogonality bounds; return (lam, stats)."""
    lam, q, stats = eigh_tridiagonal(a, b)
    n = len(a)
    scale = max([abs(t) for t in a] + [abs(t) for t in b] + [1e-300])
    for col in range(n):
        for i in range(n):
            tq = a[i] * q[i][col]
            if i > 0:
                tq += b[i - 1] * q[i - 1][col]
            if i < n - 1:
                tq += b[i] * q[i + 1][col]
            assert abs(tq - lam[col] * q[i][col]) <= c * n * U * scale
    for i in range(n):
        for j in range(n):
            assert abs(sum(q[r][i] * q[r][j] for r in range(n)) - (i == j)) <= c * n * U
    assert all(lam[i] >= lam[i + 1] for i in range(n - 1))
    return lam, stats


def det_tridiagonal_exact(a, b):
    p0, p1 = Fraction(1), Fraction(a[0])
    for i in range(1, len(a)):
        p0, p1 = p1, Fraction(a[i]) * p1 - Fraction(b[i - 1]) ** 2 * p0
    return p1


def test_page_example():
    lam, stats = check([2.0] * 4, [1.0] * 3)
    for k in range(1, 5):
        assert abs(lam[k - 1] - (2 + 2 * math.cos(k * math.pi / 5))) <= 4 * 4 * U
    assert stats["merges"] == 3 and stats["deflated"] == 2  # equal poles at the top merge
    # the reduced secular equation of the page has the roots 1.381966 and 3.618034
    f = lambda x: 1 + 2 * (0.7236068 / (0.3819660 - x) + 0.2763932 / (2.6180340 - x))
    assert abs(f(lam[0])) < 1e-6 and abs(f(lam[2])) < 1e-6


def test_toeplitz_spectrum_and_deflation():
    n = 100
    lam, stats = check([2.0] * n, [-1.0] * (n - 1))
    exact = sorted((2 - 2 * math.cos(k * math.pi / (n + 1)) for k in range(1, n + 1)), reverse=True)
    assert max(abs(x - y) for x, y in zip(lam, exact)) <= 20 * n * U * 4
    assert stats["deflated"] > 0
    assert stats["secular_its"] <= 8 * stats["roots"]  # observed about 4.3 evaluations per root


def test_random_seeded_trace_det():
    rnd = random.Random(1)
    n = 128
    a = [rnd.gauss(0, 1) for _ in range(n)]
    b = [rnd.gauss(0, 1) for _ in range(n - 1)]
    lam, stats = check(a, b)
    assert abs(sum(lam) - float(sum(Fraction(t) for t in a))) <= 10 * n * U * 4
    assert stats["secular_its"] <= 8 * stats["roots"]
    a = [float(rnd.randint(-4, 4)) for _ in range(8)]
    b = [float(rnd.randint(1, 3)) for _ in range(7)]
    lam, _ = check(a, b)
    det = float(det_tridiagonal_exact(a, b))
    assert abs(math.prod(lam) - det) <= 1e-12 * max(1.0, abs(det)) * 8


def test_wilkinson_close_pair_orthogonal():
    n = 21
    a = [abs(10 - i) * 1.0 for i in range(n)]
    lam, _ = check(a, [1.0] * (n - 1))
    assert 0 < lam[0] - lam[1] < 1e-12  # the top pair of W21+ agrees to about 13 digits
    assert abs(lam[0] - 10.746194182903) < 1e-11


def test_trivial_and_structured():
    assert check([3.0], [])[0] == [3.0]
    lam, _ = check([1.0, 3.0], [1.0])
    assert abs(lam[0] - (2 + math.sqrt(2))) < 4 * U * 4 and abs(lam[1] - (2 - math.sqrt(2))) < 4 * U * 4
    lam, stats = check([5.0, -1.0, 2.0, 0.0], [0.0, 0.0, 0.0])  # diagonal
    assert lam == [5.0, 2.0, 0.0, -1.0] and stats["secular_its"] == 0
    lam, _ = check([0.0] * 5, [0.0] * 4)  # zero matrix
    assert lam == [0.0] * 5
    lam, _ = check([1.0] * 6, [0.0, 0.0, 0.0, 0.0, 0.0])  # repeated eigenvalue
    assert lam == [1.0] * 6
    lam, _ = check([1.0, 1.0], [1e-300])  # nearly equal, deflated
    assert lam == [1.0, 1.0]
    lam, _ = check([1.0, 1.0, 1.0], [1e-10, 1e-10])
    assert abs(lam[0] - 1 - math.sqrt(2) * 1e-10) < 4 * U and abs(lam[1] - 1) < 4 * U


def test_negative_coupling_and_equal_modulus():
    n = 9
    lam, _ = check([0.0] * n, [-1.0] * (n - 1))  # spectrum symmetric about 0: +-2cos(k pi/10)
    for k in range(1, n + 1):
        assert abs(lam[k - 1] - 2 * math.cos(k * math.pi / (n + 1))) <= 40 * U
    assert abs(lam[n // 2]) <= 40 * U
    rnd = random.Random(5)
    a = [rnd.uniform(-1, 1) for _ in range(33)]
    b = [-abs(rnd.uniform(0.1, 1)) for _ in range(32)]
    check(a, b)


def test_glued_blocks_deflate_heavily():
    block_a, block_b = [abs(5 - i) * 1.0 for i in range(11)], [1.0] * 10
    a, b = [], []
    for g in range(4):
        a += block_a
        b += block_b + ([1e-14] if g < 3 else [])
    lam, stats = check(a, b)
    assert stats["deflated"] >= 30
