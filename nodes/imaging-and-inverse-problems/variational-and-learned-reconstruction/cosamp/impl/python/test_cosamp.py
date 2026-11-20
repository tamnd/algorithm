# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cosamp/. The authors are listed in prov/E7NF54.jsonl.

import itertools
import math
import random

from cosamp import cosamp, largest, least_squares_on
from imgla import matvec, norm2, solve, sym_eig


def gauss_matrix(rng, m, n):
    return [[rng.gauss(0.0, 1.0) / math.sqrt(m) for _ in range(n)] for _ in range(m)]


def sparse_vector(rng, n, s):
    x = [0.0] * n
    for i in rng.sample(range(n), s):
        x[i] = rng.choice([-1.0, 1.0]) * (1.0 + rng.random())
    return x


def dist(u, v):
    return norm2([p - q for p, q in zip(u, v)])


def rho(d):
    """Contraction factor of the proof: 4 d sqrt(1 + (d/(1-d))^2) / (1 - d)."""
    c = d / (1.0 - d)
    return 4.0 * d * math.sqrt(1.0 + c * c) / (1.0 - d)


def tau(d):
    """Noise factor of the proof."""
    c = d / (1.0 - d)
    return 4.0 * math.sqrt(1.0 + c * c) * math.sqrt(1.0 + d) / (1.0 - d) + 2.0 / math.sqrt(1.0 - d)


def local_delta(a, cols):
    """||I - A_U^T A_U|| for the column set U."""
    g = [[(1.0 if i == j else 0.0) - sum(row[i] * row[j] for row in a) for j in cols] for i in cols]
    w, _ = sym_eig(g)
    return max(abs(w[0]), abs(w[-1]))


def test_proof_constants_at_delta_one_tenth():
    assert abs(rho(0.1) - 0.44718) < 1e-5
    assert abs(tau(0.1) - 6.79824) < 1e-5
    assert rho(0.1954) < 1.0 < rho(0.1955)


def test_largest_picks_top_magnitudes():
    assert largest([0.5, -3.0, 2.0, -2.0, 1.0], 3) == [1, 2, 3]


def test_least_squares_matches_normal_equations_and_min_norm():
    rng = random.Random(1)
    a = gauss_matrix(rng, 10, 6)
    y = [rng.gauss(0.0, 1.0) for _ in range(10)]
    cols = [0, 2, 3, 5]
    g = [[sum(row[i] * row[j] for row in a) for j in cols] for i in cols]
    rhs = [sum(row[i] * yi for row, yi in zip(a, y)) for i in cols]
    assert dist(least_squares_on(a, y, cols), solve(g, rhs)) <= 1e-10
    # Dependent columns: the same column twice. The minimum norm solution
    # splits the coefficient equally, and the residual is orthogonal to A_T.
    b = [[row[0], row[0], row[1]] for row in a]
    z = least_squares_on(b, y, [0, 1, 2])
    assert abs(z[0] - z[1]) <= 1e-10
    r = [yi - sum(bi * zi for bi, zi in zip(row, z)) for row, yi in zip(b, y)]
    for j in range(3):
        assert abs(sum(row[j] * ri for row, ri in zip(b, r))) <= 1e-10


def test_exact_recovery_of_sparse_vectors_from_gaussian_measurements():
    for seed in range(10):
        rng = random.Random(100 + seed)
        a = gauss_matrix(rng, 32, 64)
        x = sparse_vector(rng, 64, 4)
        xh, res = cosamp(a, matvec(a, x), 4)
        assert dist(xh, x) <= 1e-9
        assert len(res) - 1 <= 5


def test_one_step_bound_of_the_proof_holds_with_the_local_constant():
    # For an s-sparse start a, let U = supp(x) + supp(a) + Omega (|U| <= 4s).
    # The proof only uses ||I - A_U^T A_U|| = d, so whenever d < 1:
    # ||x - a_new|| <= rho(d) ||x - a|| + tau(d) ||e||.
    rng = random.Random(2)
    m, n, s = 40, 60, 3
    a = gauss_matrix(rng, m, n)
    checked = 0
    for _ in range(40):
        x = sparse_vector(rng, n, s)
        e = [rng.gauss(0.0, 0.02) for _ in range(m)]
        y = [u + v for u, v in zip(matvec(a, x), e)]
        start = sparse_vector(rng, n, s)
        a_new, _ = cosamp(a, y, s, iters=1, x0=start)
        v = [yi - ai for yi, ai in zip(y, matvec(a, start))]
        omega = largest([sum(row[j] * vi for row, vi in zip(a, v)) for j in range(n)], 2 * s)
        u = sorted({i for i in range(n) if x[i] != 0.0 or start[i] != 0.0} | set(omega))
        d = local_delta(a, u)
        if d >= 1.0:
            continue
        checked += 1
        assert dist(a_new, x) <= rho(d) * dist(start, x) + tau(d) * norm2(e) + 1e-10
    assert checked >= 10


def test_noiseless_result_equals_exhaustive_l0_search():
    for seed in range(6):
        rng = random.Random(300 + seed)
        m, n, s = 7, 12, 2
        a = gauss_matrix(rng, m, n)
        x = sparse_vector(rng, n, s)
        y = matvec(a, x)
        best = None
        for sup in itertools.combinations(range(n), s):
            z = least_squares_on(a, y, list(sup))
            r = norm2([yi - sum(a[i][j] * zj for j, zj in zip(sup, z)) for i, yi in enumerate(y)])
            if best is None or r < best[0]:
                best = (r, sup, z)
        brute = [0.0] * n
        for j, zj in zip(best[1], best[2]):
            brute[j] = zj
        assert dist(brute, x) <= 1e-9
        xh, _ = cosamp(a, y, s)
        assert dist(xh, brute) <= 1e-9


def test_noisy_error_is_a_small_multiple_of_the_noise():
    rng = random.Random(4)
    a = gauss_matrix(rng, 48, 64)
    x = sparse_vector(rng, 64, 3)
    e = [rng.gauss(0.0, 0.01) for _ in range(48)]
    y = [u + v for u, v in zip(matvec(a, x), e)]
    xh, _ = cosamp(a, y, 3)
    assert sum(1 for t in xh if t != 0.0) <= 3
    assert dist(xh, x) <= 3.0 * norm2(e)
