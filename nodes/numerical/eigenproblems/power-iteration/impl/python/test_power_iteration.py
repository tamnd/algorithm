# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/power-iteration/. The authors are listed in prov/F8BB9Q.jsonl.

import math
import random
from fractions import Fraction

from power_iteration import matvec, norm2, power_iteration

U = 2.0**-53


def householder_orthogonal(n, rng, k=3):
    """An exactly orthogonal rational matrix: a product of k reflectors I - 2 v v^T / v^T v."""
    q = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for _ in range(k):
        v = [Fraction(rng.randint(-5, 5)) for _ in range(n)]
        vv = sum(t * t for t in v)
        if vv == 0:
            continue
        # q <- q (I - 2 v v^T / vv)
        qv = [sum(q[i][j] * v[j] for j in range(n)) for i in range(n)]
        q = [[q[i][j] - 2 * qv[i] * v[j] / vv for j in range(n)] for i in range(n)]
    return q


def conjugate_diag(q, lam, qinv):
    n = len(lam)
    return [[float(sum(q[i][k] * lam[k] * qinv[k][j] for k in range(n))) for j in range(n)] for i in range(n)]


def transpose(q):
    return [list(r) for r in zip(*q)]


def rational_inverse(m):
    n = len(m)
    a = [list(r) + [Fraction(int(i == j)) for j in range(n)] for i, r in enumerate(m)]
    for c in range(n):
        p = next(i for i in range(c, n) if a[i][c] != 0)
        a[c], a[p] = a[p], a[c]
        piv = a[c][c]
        a[c] = [t / piv for t in a[c]]
        for i in range(n):
            if i != c and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[c])]
    return [r[n:] for r in a]


def known_symmetric(lam, rng):
    q = householder_orthogonal(len(lam), rng)
    return conjugate_diag(q, [Fraction(x) for x in lam], transpose(q))


def known_nonsymmetric(lam, rng):
    n = len(lam)
    while True:
        v = [[Fraction(rng.randint(-3, 3)) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            v[i][i] += 7  # diagonally dominant, so nonsingular
        try:
            vi = rational_inverse(v)
            break
        except StopIteration:
            continue
    return conjugate_diag(v, [Fraction(x) for x in lam], vi)


def fro(a):
    return math.sqrt(sum(abs(t) ** 2 for row in a for t in row))


def test_page_example():
    # A = [[2,1],[1,2]], x0 = e1: rho_k = (3*9^k + 1)/(9^k + 1), error 2/(9^k + 1).
    a = [[2.0, 1.0], [1.0, 2.0]]
    res = power_iteration(a, [1.0, 0.0], tol=0.0, maxit=6)
    assert not res.converged
    for k, rho in enumerate(res.history):
        assert abs((3.0 - rho) - 2.0 / (9**k + 1)) <= 1e-14
    res = power_iteration(a, [1.0, 0.0])
    assert res.converged and abs(res.value - 3.0) <= 1e-12
    assert abs(abs(res.vector[0]) - math.sqrt(0.5)) <= 1e-6


def test_backward_error_bound_on_success():
    rng = random.Random(11)
    for _ in range(40):
        n = rng.randint(1, 7)
        a = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        a[0][0] += 4.0  # make one eigenvalue clearly dominant
        res = power_iteration(a, tol=1e-10, maxit=5000)
        assert res.converged
        q, rho = res.vector, res.value
        r = [x - rho * y for x, y in zip(matvec(a, q), q)]
        assert abs(norm2(q) - 1.0) <= 10 * n * U
        assert norm2(r) <= 1e-10 * fro(a) * 1.0000001


def test_symmetric_known_spectrum_and_squared_rate():
    rng = random.Random(5)
    for _ in range(10):
        n = rng.randint(3, 7)
        lam = [rng.randint(-10, 10) for _ in range(n - 2)] + [rng.choice([-1, 1]) * 18, rng.choice([-1, 1]) * 30]
        a = known_symmetric(lam, rng)
        res = power_iteration(a, tol=1e-13, maxit=10000)
        assert res.converged
        lam1 = lam[-1]
        assert abs(res.value - lam1) <= 1e-11 * abs(lam1)
        # The Rayleigh quotient error shrinks by about (lam2/lam1)^2 per step.
        ratio = (18 / 30) ** 2
        errs = [abs(h - lam1) for h in res.history]
        obs = [errs[k + 1] / errs[k] for k in range(len(errs) - 1) if errs[k] > 1e-9 * abs(lam1) and errs[k + 1] > 0]
        if len(obs) >= 3:
            assert abs(obs[-1] - ratio) <= 0.05 * ratio


def test_nonsymmetric_linear_rate():
    rng = random.Random(8)
    lam = [1, -2, 3, 5]
    a = known_nonsymmetric(lam, rng)
    res = power_iteration(a, tol=1e-13, maxit=2000)
    assert res.converged and abs(res.value - 5.0) <= 1e-10
    errs = [abs(h - 5.0) for h in res.history]
    obs = [errs[k + 1] / errs[k] for k in range(5, len(errs) - 1) if errs[k] > 1e-8]
    assert obs and all(abs(o - 0.6) <= 0.05 for o in obs[-3:])


def test_negative_dominant_eigenvalue_sign_flips():
    a = [[-3.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 2.0]]
    res = power_iteration(a, [1.0, 1.0, 1.0], tol=1e-12)
    assert res.converged and abs(res.value + 3.0) <= 1e-11


def test_one_by_one_zero_and_diagonal():
    res = power_iteration([[7.5]], [2.0])
    assert res.converged and res.value == 7.5 and res.iterations == 1
    res = power_iteration([[0.0, 0.0], [0.0, 0.0]], [1.0, 2.0])
    assert res.converged and res.value == 0.0
    res = power_iteration([[1.0, 0.0], [0.0, 4.0]], [1.0, 1.0])
    assert res.converged and abs(res.value - 4.0) <= 1e-11


def test_triangular_matrix():
    a = [[1.0, 5.0, -2.0], [0.0, 6.0, 3.0], [0.0, 0.0, 2.0]]
    res = power_iteration(a, tol=1e-12)
    assert res.converged and abs(res.value - 6.0) <= 1e-10


def test_start_orthogonal_to_dominant_vector_stays_there():
    # For a diagonal matrix the zero component stays exactly zero, so the iteration finds lambda_2.
    a = [[5.0, 0.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 1.0]]
    res = power_iteration(a, [0.0, 1.0, 1.0], tol=1e-12)
    assert res.converged and abs(res.value - 3.0) <= 1e-11


def test_complex_pair_does_not_converge():
    # Eigenvalues 1 +- 2i have equal modulus: no dominant eigenvalue.
    a = [[1.0, -2.0], [2.0, 1.0]]
    res = power_iteration(a, [1.0, 0.3], tol=1e-10, maxit=300)
    assert not res.converged


def test_plus_minus_pair_does_not_converge():
    a = [[0.0, 1.0], [1.0, 0.0]]
    res = power_iteration(a, [1.0, 0.0], tol=1e-10, maxit=100)
    assert not res.converged and res.residual >= 0.99


def test_defective_dominant_block_converges_slowly():
    # Jordan block for 2: the error decays like 1/k, not geometrically.
    a = [[2.0, 1.0], [0.0, 2.0]]
    res = power_iteration(a, [0.0, 1.0], tol=0.0, maxit=1000)
    e100, e1000 = abs(res.history[99] - 2.0), abs(res.history[999] - 2.0)
    assert 5.0 <= e100 / e1000 <= 15.0


def test_complex_hermitian():
    a = [[2.0, 1j], [-1j, 2.0]]  # eigenvalues 3 and 1
    res = power_iteration(a, [1.0, 0.5], tol=1e-12)
    assert res.converged and abs(res.value - 3.0) <= 1e-11


def test_stochastic_matrix_gives_perron_vector():
    p = [[0.5, 0.5, 0.0], [0.25, 0.5, 0.25], [0.0, 0.5, 0.5]]
    pt = [list(r) for r in zip(*p)]  # left eigenvector of P = stationary distribution
    res = power_iteration(pt, [1.0, 0.0, 0.0], tol=1e-13)
    assert res.converged and abs(res.value - 1.0) <= 1e-12
    s = sum(res.vector)
    pi = [t / s for t in res.vector]
    for got, want in zip(pi, [0.25, 0.5, 0.25]):
        assert abs(got - want) <= 1e-12


def test_iterations_follow_the_ratio():
    # Symmetric diag(10, 9, 1): residual ~ (0.9)^k, so about log(1e-12)/log(0.9) = 262 steps.
    a = [[10.0, 0.0, 0.0], [0.0, 9.0, 0.0], [0.0, 0.0, 1.0]]
    res = power_iteration(a, [1.0, 1.0, 1.0], tol=1e-12)
    assert res.converged and 230 <= res.iterations <= 290
