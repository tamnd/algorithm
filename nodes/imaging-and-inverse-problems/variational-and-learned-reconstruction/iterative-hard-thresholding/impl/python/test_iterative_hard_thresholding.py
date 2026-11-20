# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-hard-thresholding/. The authors are listed in prov/M2CY6N.jsonl.

import itertools
import math
import random

from imgla import matvec, norm2, svd, sym_eig
from iterative_hard_thresholding import hard_threshold, iht


def gauss_matrix(rng, m, n):
    return [[rng.gauss(0.0, 1.0) / math.sqrt(m) for _ in range(n)] for _ in range(m)]


def hadamard(m):
    """Sylvester Hadamard matrix of order m (a power of 2)."""
    h = [[1.0]]
    while len(h) < m:
        h = [row + row for row in h] + [row + [-v for v in row] for row in h]
    return h


def identity_hadamard(m):
    """[I | H / sqrt(m)]: two orthonormal bases with coherence 1 / sqrt(m)."""
    h = hadamard(m)
    c = 1.0 / math.sqrt(m)
    return [[1.0 if i == j else 0.0 for j in range(m)] + [c * v for v in h[i]] for i in range(m)]


def sparse_vector(rng, n, s):
    x = [0.0] * n
    for i in rng.sample(range(n), s):
        x[i] = rng.choice([-1.0, 1.0]) * (1.0 + rng.random())
    return x


def dist(u, v):
    return norm2([a - b for a, b in zip(u, v)])


def test_hard_threshold_is_best_s_term_approximation():
    rng = random.Random(1)
    for _ in range(30):
        v = [rng.gauss(0.0, 1.0) for _ in range(8)]
        for s in range(9):
            h = hard_threshold(v, s)
            assert sum(1 for t in h if t != 0.0) <= s
            best = min(
                math.sqrt(sum(v[i] ** 2 for i in range(8) if i not in set(sup)))
                for sup in itertools.combinations(range(8), s)
            )
            assert abs(dist(v, h) - best) <= 1e-12


def test_hard_threshold_ties_take_lower_index():
    assert hard_threshold([1.0, -1.0, 1.0, 0.5], 2) == [1.0, -1.0, 0.0, 0.0]


def test_linear_convergence_when_delta_3s_is_below_one_half():
    # A = [I | H/8] with m = 64 and s = 2. For 6 columns, k from I and 6 - k
    # from H/8, the Gram matrix is I plus a block C with entries +-1/8, so
    # delta_6 <= ||C||_F <= sqrt(9)/8 = 3/8 and the contraction is 2 delta <= 3/4.
    m, s, rho = 64, 2, 0.75
    a = identity_hadamard(m)
    rng = random.Random(2)
    for _ in range(3):
        x = sparse_vector(rng, 2 * m, s)
        y = matvec(a, x)
        x0 = [0.0] * (2 * m)
        xk = x0
        for k in range(1, 40):
            xk, _ = iht(a, y, s, iters=1, x0=xk)
            assert dist(xk, x) <= rho ** k * norm2(x) + 1e-12
        assert dist(xk, x) <= 1e-4


def test_noisy_error_bound_when_delta_3s_is_below_one_half():
    m, s, delta = 64, 2, 0.375
    a = identity_hadamard(m)
    rng = random.Random(3)
    x = sparse_vector(rng, 2 * m, s)
    e = [rng.gauss(0.0, 0.01) for _ in range(m)]
    y = [u + v for u, v in zip(matvec(a, x), e)]
    xk, _ = iht(a, y, s, iters=60)
    bound = 2.0 * math.sqrt(1.0 + delta) * norm2(e) / (1.0 - 2.0 * delta)
    assert dist(xk, x) <= 0.75 ** 60 * norm2(x) + bound


def test_one_step_bound_of_the_proof_holds_for_any_matrix():
    # ||x^{k+1} - x|| <= 2 ||I - A_T^T A_T|| ||x^k - x|| + 2 ||A_T^T e||, with
    # T = supp(x) + supp(x^k) + supp(x^{k+1}); no assumption on A is needed.
    rng = random.Random(4)
    m, n, s = 24, 48, 3
    a = gauss_matrix(rng, m, n)
    x = sparse_vector(rng, n, s)
    e = [rng.gauss(0.0, 0.05) for _ in range(m)]
    y = [u + v for u, v in zip(matvec(a, x), e)]
    xk = [0.0] * n
    for _ in range(25):
        xn, _ = iht(a, y, s, iters=1, x0=xk)
        t = sorted({i for i in range(n) if x[i] != 0.0 or xk[i] != 0.0 or xn[i] != 0.0})
        g = [[(1.0 if i == j else 0.0) - sum(a[r][i] * a[r][j] for r in range(m)) for j in t] for i in t]
        w, _ = sym_eig(g)
        op = max(abs(w[0]), abs(w[-1]))
        ate = norm2([sum(a[r][i] * e[r] for r in range(m)) for i in t])
        assert dist(xn, x) <= 2.0 * op * dist(xk, x) + 2.0 * ate + 1e-10
        xk = xn


def test_residual_does_not_increase_when_norm_of_a_is_below_one():
    rng = random.Random(5)
    m, n, s = 20, 40, 4
    a = gauss_matrix(rng, m, n)
    top = svd(a)[1][0]
    a = [[0.99 * v / top for v in row] for row in a]
    for trial in range(3):
        y = [rng.gauss(0.0, 1.0) for _ in range(m)]
        x0 = [rng.gauss(0.0, 1.0) for _ in range(n)] if trial else None
        _, res = iht(a, y, s, iters=80, x0=x0)
        for k in range(1, len(res) - 1):
            assert res[k + 1] <= res[k] + 1e-12


def test_exact_recovery_matches_exhaustive_l0_search():
    # Noiseless data, tiny sizes: the s-sparse least squares solution found
    # by trying all supports has zero residual only at the true x.
    a = identity_hadamard(8)
    rng = random.Random(6)
    x = sparse_vector(rng, 16, 1)
    y = matvec(a, x)
    xk, res = iht(a, y, 1, iters=200, tol=1e-13)
    best = None
    for j in range(16):
        col = [a[r][j] for r in range(8)]
        c = sum(u * v for u, v in zip(col, y)) / sum(u * u for u in col)
        r = norm2([u - c * v for u, v in zip(y, col)])
        if best is None or r < best[0]:
            best = (r, j, c)
    z = [0.0] * 16
    z[best[1]] = best[2]
    assert dist(z, x) <= 1e-12
    assert dist(xk, z) <= 1e-10
    assert res[-1] <= 1e-12
