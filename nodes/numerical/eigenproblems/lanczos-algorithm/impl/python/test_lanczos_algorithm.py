# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lanczos-algorithm/. The authors are listed in prov/GKZVXW.jsonl.

import math
import random

from lanczos_algorithm import U, dot, lanczos, norm2, ritz


def diag_op(d):
    return lambda x: [di * xi for di, xi in zip(d, x)]


def dense_op(a):
    return lambda x: [sum(r[j] * x[j] for j in range(len(x))) for r in a]


def orth_error(q):
    return max(abs(dot(q[i], q[j]) - (1.0 if i == j else 0.0)) for i in range(len(q)) for j in range(len(q)))


def chebyshev(m, x):
    return math.cosh(m * math.acosh(x)) if x >= 1 else math.cos(m * math.acos(x))


def test_page_example():
    n = 100
    d = [float(i) for i in range(1, n + 1)]
    want = {5: 4.205216, 10: 0.862128, 20: 0.050398, 30: 6.422876e-4, 40: 7.154212e-7}
    for k, err in want.items():
        al, be, q, br = lanczos(diag_op(d), [1.0] * n, k)
        th, ys, est = ritz(al, be, q)
        assert abs((100.0 - th[0]) - err) <= 1e-5 * err + 1e-12
        assert abs((th[-1] - 1.0) - err) <= 1e-5 * err + 1e-12  # the spectrum is symmetric about 50.5


def test_kaniel_paige_saad_bound():
    rng = random.Random(5)
    for trial in range(6):
        n = 60
        d = sorted((rng.uniform(0, 10) for _ in range(n)), reverse=True)
        b = [rng.gauss(0, 1) for _ in range(n)]
        cos2 = b[0] ** 2 / dot(b, b)
        tan2 = (1 - cos2) / cos2
        gamma = (d[0] - d[1]) / (d[1] - d[-1])
        for k in (5, 10, 15, 20):
            al, be, q, br = lanczos(diag_op(d), b, k)
            th = ritz(al, be, q)[0]
            bound = (d[0] - d[-1]) * tan2 / chebyshev(k - 1, 1 + 2 * gamma) ** 2
            err = d[0] - th[0]
            assert -1e-12 <= err <= bound * (1 + 1e-8) + 1e-12


def test_three_term_relation_and_residuals():
    rng = random.Random(9)
    n, k = 40, 15
    m = [[rng.gauss(0, 1) for _ in range(n)] for _ in range(n)]
    a = [[m[i][j] + m[j][i] for j in range(n)] for i in range(n)]
    op = dense_op(a)
    al, be, q, br = lanczos(op, [rng.gauss(0, 1) for _ in range(n)], k + 1)
    assert not br and orth_error(q) <= 10 * k * U * 10
    for j in range(k):  # A q_j = beta_{j-1} q_{j-1} + alpha_j q_j + beta_j q_{j+1}
        aq = op(q[j])
        rhs = [al[j] * q[j][i] + be[j] * q[j + 1][i] + (be[j - 1] * q[j - 1][i] if j else 0.0) for i in range(n)]
        assert norm2([x - y for x, y in zip(aq, rhs)]) <= 1e3 * n * U * 10
    al, be = al[:k], be[:k]
    th, ys, est = ritz(al, be, q[:k])
    for t, y, e in zip(th, ys, est):
        r = [x - t * yy for x, yy in zip(op(y), y)]
        assert abs(norm2(r) - e) <= 1e-10 * max(1.0, e) * 1e2
        assert abs(norm2(y) - 1.0) <= 1e-12


def test_ritz_values_inside_spectrum():
    rng = random.Random(13)
    d = [rng.uniform(-3, 7) for _ in range(50)]
    al, be, q, br = lanczos(diag_op(d), [1.0] * 50, 20)
    th = ritz(al, be, q)[0]
    assert min(d) - 1e-12 <= min(th) and max(th) <= max(d) + 1e-12
    assert all(th[i] >= th[i + 1] for i in range(len(th) - 1))


def test_exact_breakdown_with_few_distinct_eigenvalues():
    d = [1.0] * 5 + [2.0] * 7 + [5.0] * 3
    al, be, q, br = lanczos(diag_op(d), [1.0] * 15, 10)
    assert br and len(al) == 3
    th = ritz(al, be, q)[0]
    assert max(abs(x - y) for x, y in zip(th, [5.0, 2.0, 1.0])) < 1e-13


def test_full_n_steps_keep_trace_and_spectrum():
    n = 12
    a = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    al, be, q, br = lanczos(dense_op(a), [float(i + 1) for i in range(n)], n)
    assert len(al) == n
    assert abs(sum(al) - 2.0 * n) < 1e-12
    th = ritz(al, be, q)[0]
    want = sorted((2.0 - 2.0 * math.cos(k * math.pi / (n + 1)) for k in range(1, n + 1)), reverse=True)
    assert max(abs(x - y) for x, y in zip(th, want)) < 1e-12
    assert orth_error(q) <= 10 * n * U * 10


def test_start_vector_orthogonal_to_wanted_eigenvector():
    """The all-ones vector is orthogonal to the top eigenvector of the even-order Toeplitz matrix."""
    n = 10
    a = [[2.0 if i == j else (-1.0 if abs(i - j) == 1 else 0.0) for j in range(n)] for i in range(n)]
    al, be, q, br = lanczos(dense_op(a), [1.0] * n, n)
    th = ritz(al, be, q)[0]
    top = 2.0 - 2.0 * math.cos(n * math.pi / (n + 1))
    assert br and len(al) == n // 2
    assert abs(th[0] - top) > 1e-3


def test_loss_of_orthogonality_and_ghosts():
    """Without reorthogonalization, a converged Ritz value is copied again and again (Paige)."""
    n = 30
    d = [float(i) for i in range(1, n)] + [60.0]
    counts = []
    for k in (30, 60, 80):
        al, be, q, br = lanczos(diag_op(d), [1.0] * n, k, reorth=False)
        th = ritz(al, be, q)[0]
        counts.append(sum(1 for t in th if abs(t - 60.0) < 1e-8))
        if k == 60:
            assert orth_error(q) > 0.1
    assert counts[0] >= 2 and counts[-1] > counts[0]
    al, be, q, br = lanczos(diag_op(d), [1.0] * n, 30, reorth=True)
    th = ritz(al, be, q)[0]
    assert sum(1 for t in th if abs(t - 60.0) < 1e-8) == 1


def test_one_by_one_and_zero_matrix():
    al, be, q, br = lanczos(diag_op([3.0]), [2.0], 3)
    assert br and al == [3.0] and q == [[1.0]]
    al, be, q, br = lanczos(diag_op([0.0, 0.0, 0.0]), [1.0, 2.0, 2.0], 3)
    assert br and al == [0.0]
