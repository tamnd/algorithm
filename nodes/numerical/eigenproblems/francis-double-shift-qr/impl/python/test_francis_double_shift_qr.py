# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/francis-double-shift-qr/. The authors are listed in prov/ADBYNC.jsonl.

import math
import random
from fractions import Fraction

import pytest

from francis_double_shift_qr import U, francis_step, hessenberg, schur


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return [list(r) for r in zip(*a)]


def fro(a):
    return math.sqrt(sum(x * x for r in a for x in r))


def close_to(found, expected, tol):
    pool = list(found)
    for lam in expected:
        best = min(range(len(pool)), key=lambda i: abs(pool[i] - lam))
        assert abs(pool[best] - lam) <= tol, (lam, pool[best])
        pool.pop(best)


def check_schur(a, t, q, c=20):
    n = len(a)
    r = mm(mm(q, t), tr(q))
    assert fro([[r[i][j] - a[i][j] for j in range(n)] for i in range(n)]) <= c * n * U * max(fro(a), 1.0)
    g = mm(tr(q), q)
    assert max(abs(g[i][j] - (i == j)) for i in range(n) for j in range(n)) <= c * n * U
    for i in range(n):
        for j in range(i - 1):
            assert t[i][j] == 0.0
    for i in range(n - 2):
        assert t[i + 1][i] == 0.0 or t[i + 2][i + 1] == 0.0  # 2x2 blocks do not overlap
    for i in range(n - 1):
        if t[i + 1][i] != 0.0:  # a 2x2 block holds a complex pair
            a2, b2, c2, d2 = t[i][i], t[i][i + 1], t[i + 1][i], t[i + 1][i + 1]
            assert (a2 - d2) ** 2 / 4 + b2 * c2 < 0


def test_page_example():
    a = [[5.0, -7.0, 5.0, -6.0], [1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
    trace = []
    t, q, eig, its = schur(a, trace=trace)
    assert its == 6
    close_to(eig, [3, 2, 1j, -1j], 1e-14)
    check_schur(a, t, q)
    h32 = [x[2] for x in trace]
    expected = [1.0, 0.263987, 0.0728072, 7.34319e-4, 5.10336e-8]
    for got, want in zip(h32, expected):
        assert got == pytest.approx(want, rel=1e-5)
    for e1, e2 in zip(h32[2:], h32[3:]):
        assert e2 <= 0.2 * e1 * e1 / min(h32[1:]) + 1e-15  # quadratic in the last steps


def test_random_schur_and_iteration_count():
    rng = random.Random(3)
    n = 40
    a = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    t, q, eig, its = schur(a)
    check_schur(a, t, q)
    assert abs(sum(eig).real - sum(a[i][i] for i in range(n))) <= 1e-12 * n
    assert all(abs(e.imag) == 0 or any(abs(f - e.conjugate()) <= 1e-12 for f in eig) for e in eig)
    assert its / n <= 4  # observed about 2 double steps per eigenvalue
    t2, q2, eig2, its2 = schur(a, want_q=False)
    assert q2 is None
    close_to(eig2, eig, 1e-10)


def det_frac(m):
    m = [row[:] for row in m]
    n = len(m)
    d = Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            d = -d
        d *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return d


def test_exact_trace_and_determinant():
    ai = [[2, -1, 3, 0, 1], [4, 1, -2, 5, 0], [0, 3, 1, -1, 2], [1, 0, 2, 3, -4], [-2, 1, 0, 1, 1]]
    exact_det = det_frac([[Fraction(x) for x in r] for r in ai])
    a = [[float(x) for x in r] for r in ai]
    t, q, eig, its = schur(a)
    check_schur(a, t, q)
    prod = 1.0 + 0j
    for e in eig:
        prod *= e
    assert abs(prod - float(exact_det)) <= 1e-11 * abs(float(exact_det))
    assert abs(sum(eig) - sum(ai[i][i] for i in range(5))) <= 1e-12


def test_known_spectra():
    n = 15
    toe = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    t, q, eig, _ = schur(toe)
    check_schur(toe, t, q)
    close_to(eig, [2 - 2 * math.cos(k * math.pi / (n + 1)) for k in range(1, n + 1)], 1e-13)
    s = [[1.0, 1.0, 0.0], [0.0, 1.0, 1.0], [1.0, 0.0, 1.0]]
    a = [[3.0, 1.0, -1.0], [-1.0, 5.0, 1.0], [-2.0, 2.0, 4.0]]  # S diag(2,4,6) S^-1
    assert mm(a, s) == [[2.0, 4.0, 0.0], [0.0, 4.0, 6.0], [2.0, 0.0, 6.0]]
    t, q, eig, _ = schur(a)
    close_to(eig, [2, 4, 6], 1e-13)
    coeffs = [1.0, -21.0, 175.0, -735.0, 1624.0, -1764.0, 720.0]  # (z-1)...(z-6)
    comp = [[0.0] * 6 for _ in range(6)]
    comp[0] = [-c for c in coeffs[1:]]
    for i in range(1, 6):
        comp[i][i - 1] = 1.0
    t, q, eig, _ = schur(comp)
    check_schur(comp, t, q, c=200)
    close_to(eig, [1, 2, 3, 4, 5, 6], 1e-8)


def test_trivial_and_structured_cases():
    for a, expected in (([[4.0]], [4]), ([[0.0] * 3 for _ in range(3)], [0, 0, 0]),
                        ([[3.0, 0, 0], [0, 1.0, 0], [0, 0, 2.0]], [3, 1, 2]),
                        ([[1.0, 5.0, -2.0], [0, 4.0, 7.0], [0, 0, -3.0]], [1, 4, -3])):
        t, q, eig, its = schur(a)
        assert its == 0
        close_to(eig, expected, 0.0)
    t, q, eig, _ = schur([[1.0, -2.0], [3.0, 1.0]])
    close_to(eig, [1 + math.sqrt(6) * 1j, 1 - math.sqrt(6) * 1j], 1e-15)
    a = [[2.0, 1.0], [1.0, 2.0]]
    t, q, eig, _ = schur(a)
    check_schur(a, t, q)
    assert t[1][0] == 0.0
    close_to(eig, [3, 1], 1e-15)


def test_complex_pairs_repeated_jordan_nearly_equal():
    rng = random.Random(8)
    n = 8
    v = [rng.uniform(-1, 1) for _ in range(n)]
    nv = math.sqrt(sum(x * x for x in v))
    p = [[(i == j) - 2 * v[i] * v[j] / nv ** 2 for j in range(n)] for i in range(n)]

    def hide(b):
        return mm(mm(p, b), p)

    base = [[0.0] * n for _ in range(n)]
    base[0][0], base[0][1], base[1][0], base[1][1] = 1.0, 2.0, -2.0, 1.0
    base[2][2], base[2][3], base[3][2], base[3][3] = -3.0, 0.5, -0.5, -3.0
    for i, d in zip(range(4, 8), (2.0, 2.0, 2.0, 0.5)):
        base[i][i] = d
    a = hide(base)
    t, q, eig, _ = schur(a)
    check_schur(a, t, q)
    close_to(eig, [1 + 2j, 1 - 2j, -3 + 0.5j, -3 - 0.5j, 2, 2, 2, 0.5], 1e-7)
    jb = [[0.0] * n for _ in range(n)]
    for i in range(4):
        jb[i][i] = 1.0
        if i < 3:
            jb[i][i + 1] = 1.0
    for i, d in zip(range(4, 8), (3.0, 1.0 + 1e-10, 1.0 - 1e-10, -1.0)):
        jb[i][i] = d
    a = hide(jb)
    t, q, eig, _ = schur(a)
    check_schur(a, t, q)
    near_one = [e for e in eig if abs(e - 1) < 0.1]
    assert len(near_one) == 6
    assert all(abs(e - 1) <= 1e-3 for e in near_one)  # about u^(1/4) for the Jordan block
    close_to([e for e in eig if abs(e - 1) >= 0.1], [3, -1], 1e-12)


def test_exceptional_shift_on_cyclic_permutation():
    n = 6
    c = [[0.0] * n for _ in range(n)]
    for i in range(1, n):
        c[i][i - 1] = 1.0
    c[0][n - 1] = 1.0
    h = [r[:] for r in c]
    francis_step(h, 0, n - 1, 0.0, 0.0)  # standard shifts of the trailing block are 0, 0
    # the step only changes signs (a diagonal similarity): no progress toward deflation
    assert max(abs(abs(h[i][j]) - c[i][j]) for i in range(n) for j in range(n)) <= 1e-15
    t, q, eig, its = schur(c)
    assert its > 10  # converges only after an exceptional shift
    check_schur(c, t, q)
    close_to(eig, [complex(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)], 1e-13)


def test_hessenberg_reduction_keeps_spectrum():
    rng = random.Random(1)
    n = 10
    a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    q = [[float(i == j) for j in range(n)] for i in range(n)]
    h = hessenberg(a, q)
    for i in range(n):
        for j in range(i - 1):
            assert h[i][j] == 0.0
    r = mm(mm(q, h), tr(q))
    assert fro([[r[i][j] - a[i][j] for j in range(n)] for i in range(n)]) <= 20 * n * U * fro(a)
