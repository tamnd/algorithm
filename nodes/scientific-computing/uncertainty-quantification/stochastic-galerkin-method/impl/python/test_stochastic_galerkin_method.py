# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stochastic-galerkin-method/. The authors are listed in prov/850TYY.jsonl.
import math
import random

from scimat import cholesky, matvec, solve
from stochastic_galerkin_method import (
    diffusion_matrices,
    evaluate,
    galerkin_matrices,
    legendre_basis,
    load_vector,
    mean_and_variance,
    stochastic_galerkin,
    total_degree_set,
)


def gauss_legendre(n):
    """Gauss-Legendre nodes and weights on [-1, 1] by Newton's method."""
    xs, ws = [], []
    for i in range(1, n + 1):
        x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
        for _ in range(100):
            p0, p1 = 1.0, x
            for k in range(2, n + 1):
                p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
            dp = n * (x * p1 - p0) / (x * x - 1)
            step = p1 / dp
            x -= step
            if abs(step) < 1e-15:
                break
        p0, p1 = 1.0, x
        for k in range(2, n + 1):
            p0, p1 = p1, ((2 * k - 1) * x * p1 - (k - 1) * p0) / k
        dp = n * (x * p1 - p0) / (x * x - 1)
        xs.append(x)
        ws.append(2 / ((1 - x * x) * dp * dp))
    return xs, ws


def test_index_set_size_is_binomial():
    for d in range(1, 4):
        for p in range(0, 5):
            idx = total_degree_set(d, p)
            assert len(idx) == math.comb(d + p, p)
            assert idx[0] == (0,) * d
            assert len(set(idx)) == len(idx)


def test_triple_products_match_quadrature():
    xs, ws = gauss_legendre(12)
    for m in range(6):
        for n in range(6):
            q = sum(0.5 * w * x * legendre_basis(x, 6)[m] * legendre_basis(x, 6)[n] for x, w in zip(xs, ws))
            g = galerkin_matrices([(k,) for k in range(6)], 1)[1][m][n]
            assert abs(q - g) < 1e-13


def test_scalar_problem_converges_to_exact_moments():
    # (2 + xi) u = 1, xi uniform on [-1, 1]: E[u] = ln(3) / 2, E[u^2] = 1/3
    exact_mean = math.log(3.0) / 2.0
    exact_var = 1.0 / 3.0 - exact_mean**2
    errors = []
    for p in range(0, 9):
        _, c = stochastic_galerkin([[[2.0]], [[1.0]]], [1.0], p)
        m, v = mean_and_variance(c)
        errors.append(abs(m[0] - exact_mean))
    assert errors[0] > 4e-2
    assert errors[-1] < 1e-10
    assert all(errors[i + 1] < errors[i] / 5 for i in range(len(errors) - 1))
    assert abs(v[0] - exact_var) < 1e-9


def test_deterministic_matrix_gives_deterministic_solution():
    a0 = [[4.0, 1.0], [1.0, 3.0]]
    zero = [[0.0, 0.0], [0.0, 0.0]]
    f = [1.0, 2.0]
    _, c = stochastic_galerkin([a0, zero, zero], f, 3)
    u = solve(a0, f)
    assert all(abs(c[0][r] - u[r]) < 1e-14 for r in range(2))
    assert all(abs(x) < 1e-14 for cv in c[1:] for x in cv)


def test_galerkin_residual_is_orthogonal_to_the_basis():
    mats = diffusion_matrices(4, 0.6)
    f = load_vector(4)
    idx, c = stochastic_galerkin(mats, f, 3)
    xs, ws = gauss_legendre(6)
    n = len(f)
    worst = 0.0
    for b in idx:
        acc = [0.0] * n
        for x1, w1 in zip(xs, ws):
            for x2, w2 in zip(xs, ws):
                u = evaluate(idx, c, [x1, x2])
                a = [[mats[0][i][j] + x1 * mats[1][i][j] + x2 * mats[2][i][j] for j in range(n)] for i in range(n)]
                res = [ra - fa for ra, fa in zip(matvec(a, u), f)]
                psi = legendre_basis(x1, 3)[b[0]] * legendre_basis(x2, 3)[b[1]]
                for r in range(n):
                    acc[r] += w1 * w2 / 4.0 * res[r] * psi
        worst = max(worst, max(abs(v) for v in acc))
    assert worst < 1e-13


def test_block_matrix_is_positive_definite():
    mats = diffusion_matrices(4, 0.9)
    idx = total_degree_set(2, 3)
    g = galerkin_matrices(idx, 2)
    n = 3
    size = len(idx)
    big = [[sum(g[k][i // n][j // n] * mats[k][i % n][j % n] for k in range(3)) for j in range(size * n)] for i in range(size * n)]
    assert all(big[i][j] == big[j][i] for i in range(size * n) for j in range(size * n))
    cholesky(big)


def test_diffusion_moments_match_tensor_quadrature():
    def u_half(x1, x2, amp):
        a1, a2 = 1 + amp * x1, 1 + amp * x2
        cc = (a2 + 3 * a1) / (4 * (a1 + a2))
        return (cc / 2 - 1 / 8) / a1

    xs, ws = gauss_legendre(30)
    m = s2 = 0.0
    for x1, w1 in zip(xs, ws):
        for x2, w2 in zip(xs, ws):
            u = u_half(x1, x2, 0.5)
            m += w1 * w2 / 4 * u
            s2 += w1 * w2 / 4 * u * u
    _, c = stochastic_galerkin(diffusion_matrices(4, 0.5), load_vector(4), 5)
    mean, var = mean_and_variance(c)
    assert abs(mean[1] - m) < 1e-7
    assert abs(var[1] - (s2 - m * m)) < 1e-7


def test_one_input_equals_gauss_projection():
    a0 = [[3.0, -1.0, 0.0], [-1.0, 3.0, -1.0], [0.0, -1.0, 3.0]]
    a1 = [[1.0, 0.5, 0.0], [0.5, -1.0, 0.0], [0.0, 0.0, 0.5]]
    f = [1.0, 0.0, 2.0]
    for p in range(0, 6):
        _, c = stochastic_galerkin([a0, a1], f, p)
        xs, ws = gauss_legendre(p + 1)
        sols = [solve([[a0[i][j] + x * a1[i][j] for j in range(3)] for i in range(3)], f) for x in xs]
        for a in range(p + 1):
            proj = [sum(0.5 * w * legendre_basis(x, p)[a] * u[r] for x, w, u in zip(xs, ws, sols)) for r in range(3)]
            assert all(abs(proj[r] - c[a][r]) < 1e-12 for r in range(3))


def test_surrogate_is_close_at_random_points():
    rng = random.Random(7)
    _, c = stochastic_galerkin([[[2.0]], [[1.0]]], [1.0], 10)
    idx = total_degree_set(1, 10)
    for _ in range(20):
        x = rng.uniform(-1.0, 1.0)
        assert abs(evaluate(idx, c, [x])[0] - 1.0 / (2.0 + x)) < 1e-5
