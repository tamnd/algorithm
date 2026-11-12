# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unscented-kalman-filter/.

import random

from unscented_kalman_filter import (
    inverse,
    mat_add,
    mat_mul,
    mat_vec,
    sigma_points,
    transpose,
    unscented_kalman_filter,
    unscented_transform,
    vec_add,
)

PARAMS = [(1.0, 0.0, None), (1.0, 2.0, 0.0), (0.5, 2.0, 1.0), (1e-2, 2.0, 0.0), (1.0, 0.0, 2.0)]
TOL = 1e-8


def random_spd(n, rng):
    B = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
    P = mat_mul(B, transpose(B))
    for i in range(n):
        P[i][i] += 0.2
    return P


def close(a, b, tol=TOL):
    if isinstance(a[0], list):
        return all(close(ra, rb, tol) for ra, rb in zip(a, b))
    return all(abs(x - y) <= tol * (1 + abs(y)) for x, y in zip(a, b))


def test_sigma_points_match_mean_and_covariance() -> None:
    rng = random.Random(1)
    for n in (1, 2, 3, 4):
        m, P = [rng.gauss(0, 1) for _ in range(n)], random_spd(n, rng)
        for alpha, beta, kappa in PARAMS:
            X, wm, wc = sigma_points(m, P, alpha, beta, kappa)
            assert len(X) == 2 * n + 1 and abs(sum(wm) - 1) < 1e-9
            mean = [sum(w * x[i] for w, x in zip(wm, X)) for i in range(n)]
            cov = [[sum(w * (x[i] - m[i]) * (x[j] - m[j]) for w, x in zip(wm, X)) for j in range(n)] for i in range(n)]
            assert close(mean, m, 1e-6) and close(cov, P, 1e-6)


def test_exact_for_linear_maps() -> None:
    rng = random.Random(2)
    for n, k in [(1, 1), (2, 1), (2, 3), (3, 2)]:
        m, P = [rng.gauss(0, 1) for _ in range(n)], random_spd(n, rng)
        A = [[rng.uniform(-2, 2) for _ in range(n)] for _ in range(k)]
        b = [rng.gauss(0, 1) for _ in range(k)]
        for alpha, beta, kappa in PARAMS:
            mu, S, C = unscented_transform(lambda x: vec_add(mat_vec(A, x), b), m, P, alpha, beta, kappa)
            # The centre point maps to the exact mean, so its covariance
            # weight, which holds beta, multiplies a zero deviation.
            assert close(mu, vec_add(mat_vec(A, m), b))
            assert close(S, mat_mul(mat_mul(A, P), transpose(A)))
            assert close(C, mat_mul(P, transpose(A)))


def test_mean_exact_for_quadratic_maps() -> None:
    rng = random.Random(3)
    for n in (1, 2, 3):
        m, P = [rng.gauss(0, 1) for _ in range(n)], random_spd(n, rng)
        M = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        c = [rng.uniform(-1, 1) for _ in range(n)]

        def g(x):
            return [sum(x[i] * M[i][j] * x[j] for i in range(n) for j in range(n)) + sum(a * b for a, b in zip(c, x))]

        exact = sum(M[i][j] * (P[j][i] + m[i] * m[j]) for i in range(n) for j in range(n)) + sum(a * b for a, b in zip(c, m))
        for alpha, beta, kappa in PARAMS:
            mu, _, _ = unscented_transform(g, m, P, alpha, beta, kappa)
            assert abs(mu[0] - exact) < 1e-6 * (1 + abs(exact))


def test_mean_exact_for_cubic_and_quintic_in_one_dimension() -> None:
    m, P = -0.4, 0.8
    for alpha, beta, kappa in PARAMS:
        mu, _, _ = unscented_transform(lambda x: [x[0] ** 3], [m], [[P]], alpha, beta, kappa)
        assert abs(mu[0] - (m**3 + 3 * m * P)) < 1e-6
    # With n + lambda = 3 the points also match the fourth moment 3 P^2.
    mu, _, _ = unscented_transform(lambda x: [x[0] ** 5], [m], [[P]], 1.0, 0.0, 2.0)
    assert abs(mu[0] - (m**5 + 10 * m**3 * P + 15 * m * P * P)) < 1e-9


def test_square_variance_formula() -> None:
    # For g(x) = x^2 with x ~ N(m, P) in one dimension the transform gives
    # the variance 4 m^2 P + (alpha^2 kappa + beta) P^2; the true value has 2 P^2.
    m, P = 0.7, 1.3
    for alpha, beta, kappa in [(1.0, 0.0, 2.0), (1.0, 2.0, 0.0), (0.5, 1.0, 4.0), (1.0, 0.0, 0.0), (0.3, 2.0, 1.0)]:
        mu, S, _ = unscented_transform(lambda x: [x[0] ** 2], [m], [[P]], alpha, beta, kappa)
        assert abs(mu[0] - (m * m + P)) < 1e-9
        assert abs(S[0][0] - (4 * m * m * P + (alpha * alpha * kappa + beta) * P * P)) < 1e-9
        if alpha * alpha * kappa + beta == 2:
            assert abs(S[0][0] - (4 * m * m * P + 2 * P * P)) < 1e-9


def kalman_filter(A, Q, H, R, m0, P0, ys):
    m, P = list(m0), P0
    means, covs = [m], [P]
    for y in ys:
        m = mat_vec(A, m)
        P = mat_add(mat_mul(mat_mul(A, P), transpose(A)), Q)
        S = mat_add(mat_mul(mat_mul(H, P), transpose(H)), R)
        K = mat_mul(mat_mul(P, transpose(H)), inverse(S))
        m = vec_add(m, mat_vec(K, vec_add(y, mat_vec(H, m), -1)))
        P = mat_add(P, mat_mul(mat_mul(K, S), transpose(K)), -1)
        means.append(m)
        covs.append(P)
    return means, covs


def test_equals_kalman_filter_on_linear_models() -> None:
    rng = random.Random(4)
    for _ in range(15):
        n, k, T = rng.randint(1, 3), rng.randint(1, 2), rng.randint(1, 6)
        A = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        H = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(k)]
        Q, R = random_spd(n, rng), random_spd(k, rng)
        m0, P0 = [rng.gauss(0, 1) for _ in range(n)], random_spd(n, rng)
        ys = [[rng.gauss(0, 1) for _ in range(k)] for _ in range(T)]
        for alpha, beta, kappa in PARAMS[:3]:
            mu, Pu = unscented_kalman_filter(
                lambda x: mat_vec(A, x), lambda x: mat_vec(H, x), Q, R, m0, P0, ys, alpha, beta, kappa
            )
            mk, Pk = kalman_filter(A, Q, H, R, m0, P0, ys)
            for t in range(T + 1):
                assert close(mu[t], mk[t], 1e-7) and close(Pu[t], Pk[t], 1e-7)
