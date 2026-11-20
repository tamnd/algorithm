# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/plug-and-play-priors/. The authors are listed in prov/S92WZQ.jsonl.

import math
import random

from plug_and_play_priors import (
    haar_matrix,
    haar_soft_denoiser,
    least_squares_prox,
    linear_denoiser,
    matvec,
    pnp_admm,
    rmatvec,
    soft,
    solve,
)


def close(u, v, tol):
    return max(abs(p - q) for p, q in zip(u, v)) < tol


def ista_in_haar_domain(a, y, lam, iters):
    """Independent reference: minimize (1/2)||A H^T c - y||^2 + lam ||c||_1 by ISTA."""
    n = len(a[0])
    h = haar_matrix(n)
    b = [matvec(h, row) for row in a]  # B = A H^T, row by row
    lip = 0.0
    v = [1.0] * n
    for _ in range(200):  # power iteration for ||B||^2
        w = rmatvec(b, matvec(b, v))
        lip = math.sqrt(sum(t * t for t in w))
        v = [t / lip for t in w]
    step = 1.0 / (1.01 * lip)
    c = [0.0] * n
    for _ in range(iters):
        r = [p - q for p, q in zip(matvec(b, c), y)]
        g = rmatvec(b, r)
        c = soft([ci - step * gi for ci, gi in zip(c, g)], step * lam)
    return rmatvec(h, c)


def seeded_deblurring(seed, n=8):
    rng = random.Random(seed)
    kernel = [0.5, 0.3, 0.2]
    a = [[sum(kernel[k] for k in range(3) if (i + k) % n == j) for j in range(n)]
         for i in range(n)]
    x = [1.0 if 2 <= j < 6 else 0.0 for j in range(n)]
    y = [v + rng.gauss(0.0, 0.05) for v in matvec(a, x)]
    return a, y


def test_haar_is_orthonormal():
    for n in (2, 4, 8):
        h = haar_matrix(n)
        for i in range(n):
            for j in range(n):
                dot = sum(p * q for p, q in zip(h[i], h[j]))
                assert abs(dot - (1.0 if i == j else 0.0)) < 1e-12


def test_haar_soft_threshold_is_a_proximal_map():
    # v = D(w) satisfies the optimality condition of
    # min (1/2)||v - w||^2 + theta ||H v||_1, written in c = H v.
    rng = random.Random(1)
    n, theta = 8, 0.4
    h = haar_matrix(n)
    d = haar_soft_denoiser(n, theta)
    w = [rng.gauss(0.0, 1.0) for _ in range(n)]
    c, hw = matvec(h, d(w)), matvec(h, w)
    for ci, hi in zip(c, hw):
        if ci != 0.0:
            assert abs(hi - ci - theta * math.copysign(1.0, ci)) < 1e-12
        else:
            assert abs(hi) <= theta + 1e-12


def test_hand_example():
    pf = least_squares_prox([[1.0, 0.0], [0.0, 1.0]], [3.0, 1.0], 1.0)
    d = haar_soft_denoiser(2, 1.0)
    x, v, u = pnp_admm(pf, d, [0.0, 0.0], 1)
    assert close(x, [1.5, 0.5], 1e-12)
    assert close(v, [1.0 - 1.0 / math.sqrt(2.0)] * 2, 1e-12)
    x, v, u = pnp_admm(pf, d, [0.0, 0.0], 2)
    assert close(x, [1.042893, 0.542893], 1e-6) and close(v, [0.835786, 0.75], 1e-6)
    x, v, u = pnp_admm(pf, d, [0.0, 0.0], 4)
    assert close(v, [1.398286, 0.9375], 1e-6)
    x, v, u = pnp_admm(pf, d, [0.0, 0.0], 60)
    # The limit is H^T soft(H y, 1) = (3 - sqrt(2), 1).
    assert close(v, [3.0 - math.sqrt(2.0), 1.0], 1e-12)


def test_pnp_with_a_proximal_denoiser_is_admm_for_the_lasso():
    for seed in (2, 3):
        a, y = seeded_deblurring(seed)
        for rho, theta in ((1.0, 0.05), (0.5, 0.1)):
            pf = least_squares_prox(a, y, rho)
            x, v, _ = pnp_admm(pf, haar_soft_denoiser(8, theta), [0.0] * 8, 400)
            ref = ista_in_haar_domain(a, y, rho * theta, 4000)
            assert close(v, ref, 1e-7) and close(x, v, 1e-7)


def test_symmetric_linear_denoiser_solves_a_quadratic_problem():
    # W = Q diag(d) Q^T with d in (0, 1] is the prox of g(x) = (1/2) x^T (W^-1 - I) x,
    # so PnP solves (A^T A + rho (W^-1 - I)) x = A^T y.
    a, y = seeded_deblurring(4)
    q = haar_matrix(8)
    d = [1.0, 0.9, 0.7, 0.6, 0.4, 0.4, 0.3, 0.3]
    w = [[sum(q[k][i] * d[k] * q[k][j] for k in range(8)) for j in range(8)] for i in range(8)]
    winv_minus_i = [[sum(q[k][i] * (1.0 / d[k] - 1.0) * q[k][j] for k in range(8))
                     for j in range(8)] for i in range(8)]
    rho = 0.5
    pf = least_squares_prox(a, y, rho)
    _, v, _ = pnp_admm(pf, linear_denoiser(w), [0.0] * 8, 300)
    m = [[sum(a[r][i] * a[r][j] for r in range(8)) + rho * winv_minus_i[i][j]
          for j in range(8)] for i in range(8)]
    assert close(v, solve(m, rmatvec(a, y)), 1e-9)
