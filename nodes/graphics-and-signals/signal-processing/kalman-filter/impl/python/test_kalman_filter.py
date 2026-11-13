# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kalman-filter/. The authors are listed in prov/74AZEE.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from kalman_filter import add, inverse, kalman_filter, kalman_step, matmul, scalar_kalman, transpose


def identity(n):
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]


def matpow(a, t):
    out = identity(len(a))
    for _ in range(t):
        out = matmul(out, a)
    return out


def posterior_by_conditioning(m0, p0, a, q, c, r, ys):
    """Mean and covariance of x_T given y_1..y_T from the joint Gaussian, by the Schur complement.

    The independent inputs are z = (x_0, q_1..q_T, r_1..r_T); x_T and every y_s
    are linear in z, so (x_T, y_1..y_T) = L z with covariance L D L^T.
    """
    n, k, t_end = len(a), len(c), len(ys)
    blocks = [p0] + [q] * t_end + [r] * t_end
    sizes = [n] + [n] * t_end + [k] * t_end
    offs = [sum(sizes[:i]) for i in range(len(sizes))]
    dim = sum(sizes)
    d = [[F(0)] * dim for _ in range(dim)]
    for b, o in zip(blocks, offs):
        for i in range(len(b)):
            for j in range(len(b)):
                d[o + i][o + j] = F(b[i][j])
    mu_z = [F(m0[i][0]) for i in range(n)] + [F(0)] * (dim - n)

    def state_map(t):  # rows of L for x_t
        rows = [[F(0)] * dim for _ in range(n)]
        at = matpow(a, t)
        for i in range(n):
            for j in range(n):
                rows[i][j] = at[i][j]
        for s in range(1, t + 1):
            ats = matpow(a, t - s)
            for i in range(n):
                for j in range(n):
                    rows[i][offs[s] + j] = ats[i][j]
        return rows

    lmat = state_map(t_end)
    for s in range(1, t_end + 1):
        rows = matmul(c, state_map(s))
        for i in range(k):
            rows[i][offs[t_end + s] + i] += 1
        lmat += rows
    cov = matmul(matmul(lmat, d), transpose(lmat))
    mean = [sum(row[j] * mu_z[j] for j in range(dim)) for row in lmat]
    sxx = [row[:n] for row in cov[:n]]
    sxy = [row[n:] for row in cov[:n]]
    syy = [row[n:] for row in cov[n:]]
    yvec = [[F(ys[s][i][0])] for s in range(t_end) for i in range(k)]
    resid = [[yvec[i][0] - mean[n + i]] for i in range(len(yvec))]
    gain = matmul(sxy, inverse(syy))
    post_mean = add([[mean[i]] for i in range(n)], matmul(gain, resid))
    post_cov = add(sxx, matmul(gain, transpose(sxy)), -1)
    return post_mean, post_cov


def random_spd(rng, n):
    b = [[F(rng.randint(-2, 2)) for _ in range(n)] for _ in range(n)]
    return add(matmul(transpose(b), b), [[F(rng.randint(1, 3), rng.randint(1, 3)) if i == j else F(0) for j in range(n)] for i in range(n)])


def test_scalar_example_on_the_page() -> None:
    out = scalar_kalman(F(0), F(4), F(1), F(1), F(1), F(2), [F(2), F(3), F(1)])
    assert out == [(F(10, 7), F(10, 7)), (F(71, 31), F(34, 31)), (F(207, 127), F(130, 127))]


def test_equals_exact_posterior_of_the_joint_gaussian() -> None:
    rng = random.Random(5501)
    for case in range(500):
        n, k = (1, 1) if case < 250 else (rng.randint(1, 2), rng.randint(1, 2))
        t_end = rng.randint(1, 4)
        a = [[F(rng.randint(-3, 3), 2) for _ in range(n)] for _ in range(n)]
        c = [[F(rng.randint(-2, 2)) for _ in range(n)] for _ in range(k)]
        q, r, p0 = random_spd(rng, n), random_spd(rng, k), random_spd(rng, n)
        m0 = [[F(rng.randint(-3, 3))] for _ in range(n)]
        ys = [[[F(rng.randint(-5, 5))] for _ in range(k)] for _ in range(t_end)]
        got = kalman_filter(m0, p0, a, q, c, r, ys)
        for t in range(1, t_end + 1):  # every prefix, not only the last step
            want_m, want_p = posterior_by_conditioning(m0, p0, a, q, c, r, ys[:t])
            assert got[t - 1][0] == want_m and got[t - 1][1] == want_p


def test_scalar_covariance_against_the_closed_form() -> None:
    # random walk, Q = 1, R = 2: P_t = (1 + 2 c 4^-t) / (1 - c 4^-t), c = (P0 - 1) / (P0 + 2)
    rng = random.Random(5502)
    for _ in range(200):
        p0 = F(rng.randint(1, 50), rng.randint(1, 10))
        cc = (p0 - 1) / (p0 + 2)
        out = scalar_kalman(F(0), p0, F(1), F(1), F(1), F(2), [F(0)] * 15)
        for t, (_, p) in enumerate(out, start=1):
            ct = cc / 4**t
            assert p == (1 + 2 * ct) / (1 - ct)
    # general scalar model: P_t is the Mobius map of [[r a^2, r q], [a^2, q + r]]^t applied to P0
    for _ in range(300):
        a, q, r = F(rng.randint(-4, 4), 2), F(rng.randint(0, 5), 2), F(rng.randint(1, 5), 3)
        p0 = F(rng.randint(0, 9), rng.randint(1, 4))
        mob = [[r * a * a, r * q], [a * a, q + r]]
        out = scalar_kalman(F(0), p0, a, q, F(1), r, [F(0)] * 8)
        for t, (_, p) in enumerate(out, start=1):
            mt = matpow(mob, t)
            assert p == (mt[0][0] * p0 + mt[0][1]) / (mt[1][0] * p0 + mt[1][1])


def test_steady_state_of_the_random_walk() -> None:
    out = scalar_kalman(0.0, 4.0, 1.0, 1.0, 1.0, 2.0, [0.0] * 40)
    assert abs(out[-1][1] - 1.0) < 1e-15  # P_inf = 1, so P_pred = 2 and K = 2 / 4 = 1/2


def test_best_linear_estimator_with_non_gaussian_noise() -> None:
    """Two-point noise: P_t is the exact mean-square error of m_t, the error is
    orthogonal to the data, and the true conditional mean does better."""
    a, q, c, r, p0 = F(1, 2), F(1), F(1), F(4), F(1)
    t_end = 3
    outcomes = list(itertools.product((-1, 1), repeat=1 + 2 * t_end))  # x0, q_1..q_T, r_1..r_T
    mse = F(0)
    orth = [F(0)] * t_end
    groups = {}
    for z in outcomes:
        x = F(z[0])  # variance 1 = p0
        ys, xs = [], []
        for t in range(t_end):
            x = a * x + z[1 + t]  # variance of q is 1
            xs.append(x)
            ys.append(c * x + 2 * z[1 + t_end + t])  # variance of r is 4
        m, _ = scalar_kalman(F(0), p0, a, q, c, r, ys)[-1]
        mse += (xs[-1] - m) ** 2
        for s in range(t_end):
            orth[s] += (xs[-1] - m) * ys[s]
        groups.setdefault(tuple(ys), []).append(xs[-1])
    mse /= len(outcomes)
    p_end = scalar_kalman(F(0), p0, a, q, c, r, [F(0)] * t_end)[-1][1]
    assert mse == p_end
    assert orth == [0] * t_end
    best = sum(sum((v - sum(g) / len(g)) ** 2 for v in g) for g in groups.values()) / len(outcomes)
    assert best < p_end


def test_monte_carlo_consistency_of_a_tracking_model() -> None:
    rng = random.Random(5503)
    a = [[1.0, 1.0], [0.0, 1.0]]
    q = [[0.25, 0.5], [0.5, 1.0]]  # rank one: white acceleration of variance 1
    c, r = [[1.0, 0.0]], [[4.0]]
    runs, t_end, err, nis = 400, 30, 0.0, 0.0
    for _ in range(runs):
        x = [rng.gauss(0, 1), rng.gauss(0, 1)]
        m, p = [[0.0], [0.0]], [[1.0, 0.0], [0.0, 1.0]]
        for _ in range(t_end):
            g = rng.gauss(0, 1)
            x = [x[0] + x[1] + 0.5 * g, x[1] + g]
            y = [[x[0] + rng.gauss(0, 2)]]
            m, p, v, s = kalman_step(m, p, y, a, q, c, r)
            nis += v[0][0] ** 2 / s[0][0]
        err += ((x[0] - m[0][0]) ** 2 + (x[1] - m[1][0]) ** 2) / (p[0][0] + p[1][1])
    assert abs(err / runs - 1) < 0.15  # squared error matches the trace of P
    assert abs(nis / (runs * t_end) - 1) < 0.05  # normalized innovations have unit variance


def test_inverse_errors() -> None:
    assert matmul(inverse([[F(2), F(1)], [F(1), F(1)]]), [[F(2), F(1)], [F(1), F(1)]]) == identity(2)
    with pytest.raises(ValueError):
        inverse([[1, 2], [2, 4]])
