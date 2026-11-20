# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-entropy-method-imaging/. The authors are listed in prov/DHVCDM.jsonl.

import math
import random

from imgla import adjoint_gap, matvec, rmatvec
from maximum_entropy_method_imaging import (
    chi2,
    circulant_blur_matrix,
    entropy,
    gradient,
    maximum_entropy,
    objective,
    solve_fixed_lambda,
)


def blur_problem(seed, n=16, noise=0.3):
    h = [0.0] * n
    for d, v in {0: 0.4, 1: 0.2, -1: 0.2, 2: 0.1, -2: 0.1}.items():
        h[d % n] += v
    a = circulant_blur_matrix(h)
    xt = [1.0] * n
    xt[5], xt[6], xt[11] = 9.0, 5.0, 7.0
    rng = random.Random(seed)
    y = [v + rng.gauss(0, noise) for v in matvec(a, xt)]
    sigma = [noise] * n
    m = [sum(y) / n] * n
    return a, y, sigma, m, xt


def test_blur_matrix_adjoint():
    a, _, _, _, _ = blur_problem(1)
    rng = random.Random(9)
    x = [rng.gauss(0, 1) for _ in range(16)]
    y = [rng.gauss(0, 1) for _ in range(16)]
    assert adjoint_gap(lambda v: matvec(a, v), lambda w: rmatvec(a, w), x, y) < 1e-12


def test_two_pixel_example_closed_form():
    # A = I, sigma = 1, m = 1, y = (4, 1), target chi2 = 2 (the number of data).
    x, lam = maximum_entropy([[1.0, 0.0], [0.0, 1.0]], [4.0, 1.0], [1.0, 1.0], [1.0, 1.0])
    x1 = 4 - math.sqrt(2)
    assert abs(x[0] - x1) < 1e-6 and abs(x[1] - 1.0) < 1e-9
    assert abs(lam - math.log(x1) / math.sqrt(2)) < 1e-5
    assert abs(entropy(x, [1.0, 1.0]) - (x1 - 1 - x1 * math.log(x1))) < 1e-6


def test_gradient_matches_finite_differences():
    a, y, sigma, m, _ = blur_problem(2)
    rng = random.Random(4)
    x = [mj * rng.uniform(0.5, 1.5) for mj in m]
    g = gradient(x, a, y, sigma, m, 0.7)
    for j in (0, 5, 11):
        e = 1e-6
        xp = list(x)
        xm = list(x)
        xp[j] += e
        xm[j] -= e
        fd = (objective(xp, a, y, sigma, m, 0.7) - objective(xm, a, y, sigma, m, 0.7)) / (2 * e)
        assert abs(fd - g[j]) < 1e-5 * max(1.0, abs(g[j]))


def test_fixed_lambda_stationarity_positivity_and_monotone_newton():
    a, y, sigma, m, _ = blur_problem(1)
    for lam in (0.1, 1.0, 10.0):
        hist = []
        x = solve_fixed_lambda(a, y, sigma, m, lam, history=hist)
        assert min(x) > 0
        # F never increases along the Newton steps (backtracking).
        f0 = objective(m, a, y, sigma, m, lam)
        seq = [f0] + hist
        assert all(seq[k + 1] <= seq[k] + 1e-12 for k in range(len(seq) - 1))
        # Stationarity: x_j = m_j exp(-lam (A^T W (A x - y))_j).
        r = [(p - q) / (s * s) for p, q, s in zip(matvec(a, x), y, sigma)]
        g = rmatvec(a, r)
        for xj, mj, gj in zip(x, m, g):
            assert abs(xj - mj * math.exp(-lam * gj)) < 1e-7 * max(1.0, xj)


def test_denoising_case_matches_per_pixel_bisection():
    # With A = I the problem splits: log(x / m) + lam (x - y) / sigma^2 = 0 per pixel.
    rng = random.Random(6)
    n = 8
    a = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    y = [rng.uniform(0.2, 5.0) for _ in range(n)]
    sigma = [0.5] * n
    m = [1.5] * n
    lam = 0.8
    x = solve_fixed_lambda(a, y, sigma, m, lam)
    for xj, yj in zip(x, y):
        lo, hi = 1e-12, 100.0
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if math.log(mid / 1.5) + lam * (mid - yj) / 0.25 > 0:
                hi = mid
            else:
                lo = mid
        assert abs(xj - 0.5 * (lo + hi)) < 1e-9


def test_misfit_falls_and_entropy_falls_as_lambda_grows():
    a, y, sigma, m, _ = blur_problem(1)
    prev_c, prev_s = float("inf"), float("inf")
    x = None
    for lam in (0.01, 0.1, 0.5, 1.0, 5.0, 20.0):
        x = solve_fixed_lambda(a, y, sigma, m, lam, x0=x)
        c, s = chi2(x, a, y, sigma), entropy(x, m)
        assert c <= prev_c + 1e-9 and s <= prev_s + 1e-9
        prev_c, prev_s = c, s


def test_discrepancy_target_and_maximum_entropy_among_feasible_images():
    a, y, sigma, m, _ = blur_problem(1)
    x, lam = maximum_entropy(a, y, sigma, m)
    c = chi2(x, a, y, sigma)
    assert abs(c - 16.0) < 1e-4 and lam > 0
    s_best = entropy(x, m)
    # Brute force: random positive images that fit at least as well have less entropy.
    rng = random.Random(8)
    tried = 0
    for _ in range(3000):
        d = [rng.gauss(0, 1) for _ in x]
        eps = 10 ** rng.uniform(-4, -0.5)
        z = [xi + eps * di for xi, di in zip(x, d)]
        if min(z) <= 0 or chi2(z, a, y, sigma) > 16.0:
            continue
        tried += 1
        assert entropy(z, m) <= s_best + 1e-9
    assert tried > 50


def test_default_image_is_returned_when_it_already_fits():
    a = [[1.0, 0.0], [0.0, 1.0]]
    x, lam = maximum_entropy(a, [1.2, 0.9], [1.0, 1.0], [1.0, 1.0])
    assert x == [1.0, 1.0] and lam == 0.0


def test_unreachable_target_raises():
    # Data with a negative value cannot be fit by a positive image to chi2 = 0.1.
    a = [[1.0, 0.0], [0.0, 1.0]]
    try:
        maximum_entropy(a, [3.0, -3.0], [1.0, 1.0], [1.0, 1.0], target=0.1, lam_max=1e4)
    except ValueError:
        return
    assert False, "expected ValueError"
