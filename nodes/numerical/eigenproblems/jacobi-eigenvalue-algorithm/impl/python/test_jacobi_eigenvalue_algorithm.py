# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jacobi-eigenvalue-algorithm/. The authors are listed in prov/HTTEGG.jsonl.

import math
import random
from fractions import Fraction

from jacobi_eigenvalue_algorithm import U, jacobi, jacobi_classical, off


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(r) for r in zip(*a)]


def fro(a):
    return math.sqrt(sum(t * t for r in a for t in r))


def orth_error(v):
    n = len(v)
    g = matmul(transpose(v), v)
    return max(abs(g[i][j] - (1.0 if i == j else 0.0)) for i in range(n) for j in range(n))


def residual(a, lam, v):
    """max_i ||A v_i - lam_i v_i||_2."""
    n = len(a)
    worst = 0.0
    for i in range(n):
        col = [v[r][i] for r in range(n)]
        r = [sum(a[k][j] * col[j] for j in range(n)) - lam[i] * col[k] for k in range(n)]
        worst = max(worst, math.sqrt(sum(t * t for t in r)))
    return worst


def random_orthogonal(n, rng):
    """Product of n Householder reflectors with random vectors."""
    q = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(n):
        w = [rng.gauss(0, 1) for _ in range(n)]
        ww = sum(t * t for t in w)
        q = [[q[i][j] - 2.0 * sum(q[i][k] * w[k] for k in range(n)) * w[j] / ww for j in range(n)] for i in range(n)]
    return q


def with_spectrum(lam, rng):
    n = len(lam)
    q = random_orthogonal(n, rng)
    a = [[sum(q[i][k] * lam[k] * q[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
    return [[0.5 * (a[i][j] + a[j][i]) for j in range(n)] for i in range(n)]


def charpoly(a):
    """Exact characteristic polynomial (Faddeev-LeVerrier in Fraction), leading coefficient first."""
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


def peval(c, x):
    p = Fraction(0)
    for t in c:
        p = p * x + t
    return p


def check(a, lam, v, k=50.0):
    n = len(a)
    assert orth_error(v) <= k * n * U
    assert residual(a, lam, v) <= k * n * U * max(fro(a), 1e-300)


def test_page_example():
    a = [[4.0, -2.0, 2.0], [-2.0, 3.0, 1.0], [2.0, 1.0, 5.0]]
    lam, v, sweeps, rotations, ok = jacobi(a)
    assert ok and sweeps == 4 and rotations == 10
    check(a, lam, v)
    assert abs(sum(lam) - 12.0) < 1e-13
    assert abs(lam[0] * lam[1] * lam[2] - 16.0) < 1e-12
    for want, got in zip([6.640023, 0.495336, 4.864641], lam):
        assert abs(want - got) < 1e-6
    c = charpoly(a)
    for x in lam:  # an exact sign change brackets each computed eigenvalue
        lo, hi = Fraction(x) * (1 - Fraction(1, 10 ** 13)), Fraction(x) * (1 + Fraction(1, 10 ** 13))
        assert peval(c, lo) * peval(c, hi) < 0


def test_small_and_trivial():
    lam, v, sweeps, rot, ok = jacobi([[7.5]])
    assert ok and lam == [7.5] and v == [[1.0]] and sweeps == 0
    lam, v, sweeps, rot, ok = jacobi([[0.0, 0.0], [0.0, 0.0]])
    assert ok and lam == [0.0, 0.0] and rot == 0
    lam, v, sweeps, rot, ok = jacobi([[3.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, 2.0]])
    assert ok and lam == [3.0, -1.0, 2.0] and rot == 0
    a = [[2.0, 1.0], [1.0, 2.0]]  # one rotation is exact for 2 by 2
    lam, v, sweeps, rot, ok = jacobi(a)
    assert ok and rot == 1 and sorted(lam) == [1.0, 3.0]
    check(a, lam, v)


def test_toeplitz_known_spectrum():
    n = 12
    a = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    lam, v, sweeps, rot, ok = jacobi(a)
    assert ok
    want = sorted(2.0 - 2.0 * math.cos(k * math.pi / (n + 1)) for k in range(1, n + 1))
    assert max(abs(x - y) for x, y in zip(sorted(lam), want)) < 20 * n * U * 4
    check(a, lam, v)


def test_random_known_spectra():
    rng = random.Random(20261108)
    for trial in range(25):
        n = rng.randint(2, 9)
        want = sorted(rng.uniform(-5, 5) for _ in range(n))
        a = with_spectrum(want, rng)
        lam, v, sweeps, rot, ok = jacobi(a)
        assert ok and sweeps <= 12
        check(a, lam, v)
        assert max(abs(x - y) for x, y in zip(sorted(lam), want)) < 200 * n * U * 5


def test_repeated_and_nearly_equal():
    rng = random.Random(7)
    for want in ([1.0, 1.0, 1.0, 4.0], [2.0, 2.0, -3.0, -3.0, 5.0], [1.0, 1.0 + 1e-9, 1.0 + 2e-9, 2.0]):
        a = with_spectrum(want, rng)
        lam, v, sweeps, rot, ok = jacobi(a)
        assert ok
        check(a, lam, v)
        assert max(abs(x - y) for x, y in zip(sorted(lam), sorted(want))) < 1e-13


def test_quadratic_convergence():
    """off(A) after each sweep: the ratio off_{k+1} / off_k^2 stays bounded (Henrici 1958)."""
    rng = random.Random(11)
    a = with_spectrum([1.0, 2.0, 3.5, 5.0, 7.0, 9.0], rng)
    n = len(a)
    a = [row[:] for row in a]
    from jacobi_eigenvalue_algorithm import rotate, rotation
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    offs = [off(a)]
    for _ in range(8):
        for p in range(n - 1):
            for q in range(p + 1, n):
                if a[p][q] != 0.0:
                    rotate(a, v, p, q, *rotation(a[p][p], a[q][q], a[p][q]))
        offs.append(off(a))
        if offs[-1] < 1e-200:
            break
    tail = [(offs[k + 1] / offs[k] ** 2) for k in range(len(offs) - 1) if offs[k + 1] > 1e-280 and offs[k] < 0.5]
    assert tail and max(tail) < 10.0
    assert len(offs) - 1 <= 8


def test_classical_rate():
    """Each classical rotation reduces off(A)^2 by at least the factor 1 - 1/N, N = n(n - 1)/2."""
    rng = random.Random(3)
    for n in (3, 5, 7):
        a = with_spectrum([rng.uniform(-3, 3) for _ in range(n)], rng)
        lam, v, hist = jacobi_classical(a)
        nn = n * (n - 1) / 2
        for k in range(len(hist) - 1):
            if hist[k] > 1e-8:
                assert hist[k + 1] ** 2 <= (1 - 1 / nn) * hist[k] ** 2 * (1 + 1e-12) + 1e-300
        check(a, lam, v)


def test_graded_relative_accuracy():
    """A = D H D with H well conditioned: tiny eigenvalues come out with small relative error."""
    h = [[1.0, 0.3, 0.2], [0.3, 1.0, 0.25], [0.2, 0.25, 1.0]]
    d = [1.0, 1e-4, 1e-8]
    a = [[d[i] * h[i][j] * d[j] for j in range(3)] for i in range(3)]
    lam, v, sweeps, rot, ok = jacobi(a)
    assert ok
    c = charpoly(a)
    for x in lam:
        assert x > 0
        lo, hi = Fraction(x) * (1 - Fraction(1, 10 ** 12)), Fraction(x) * (1 + Fraction(1, 10 ** 12))
        assert peval(c, lo) * peval(c, hi) < 0
    assert min(lam) < 1e-15


def test_indefinite_zero_diagonal():
    a = [[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]]
    lam, v, sweeps, rot, ok = jacobi(a)
    assert ok
    want = [-math.sqrt(2.0), 0.0, math.sqrt(2.0)]
    assert max(abs(x - y) for x, y in zip(sorted(lam), want)) < 1e-15
    check(a, lam, v)
