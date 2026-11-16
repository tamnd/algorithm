# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extended-information-filter/. The authors are listed in prov/DYEYTV.jsonl.

import math
import random

import rbm
import robest
from extended_information_filter import eif, predict, recover_mean, to_information, to_moments, update

# ---------------------------------------------------------------- a planar SLAM model with two landmarks

N = 7  # (x, y, theta, m1x, m1y, m2x, m2y)
DT = 1.0


def g(u, x):
    v, w = u
    out = list(x)
    out[0] = x[0] + v * DT * math.cos(x[2])
    out[1] = x[1] + v * DT * math.sin(x[2])
    out[2] = x[2] + w * DT
    return out


def gjac(u, x):
    v, _ = u
    a = rbm.eye(N)
    a[0][2] = -v * DT * math.sin(x[2])
    a[1][2] = v * DT * math.cos(x[2])
    return a


def h(x, i):
    j = 3 + 2 * i
    dx, dy = x[j] - x[0], x[j + 1] - x[1]
    return [math.hypot(dx, dy), math.atan2(dy, dx) - x[2]]


def hjac(x, i):
    j = 3 + 2 * i
    dx, dy = x[j] - x[0], x[j + 1] - x[1]
    q = dx * dx + dy * dy
    s = math.sqrt(q)
    out = rbm.zeros(2, N)
    out[0][0], out[0][1] = -dx / s, -dy / s
    out[0][j], out[0][j + 1] = dx / s, dy / s
    out[1][0], out[1][1], out[1][2] = dy / q, -dx / q, -1.0
    out[1][j], out[1][j + 1] = -dy / q, dx / q
    return out


def residual(z, zhat):
    return [z[0] - zhat[0], robest.wrap_angle(z[1] - zhat[1])]


R = [[0.01 if i == j and i < 2 else (0.002 if i == j == 2 else 0.0) for j in range(N)] for i in range(N)]
Q = [[0.01, 0.0], [0.0, 0.0009]]


def ekf_step(mu, sigma, u, zs):
    """The reference: an EKF that linearizes all readings of a step at the predicted mean."""
    gm = gjac(u, mu)
    sigma = rbm.add(rbm.mul(rbm.mul(gm, sigma), rbm.transpose(gm)), R)
    mu = g(u, mu)
    if not zs:
        return mu, sigma
    hs, nus = [], []
    for i, z in enumerate(zs):
        hs.extend(hjac(mu, i))
        nus.extend(residual(z, h(mu, i)))
    k = len(nus)
    qs = rbm.zeros(k, k)
    for a in range(0, k, 2):
        for b in range(2):
            for c in range(2):
                qs[a + b][a + c] = Q[b][c]
    s = rbm.add(rbm.mul(rbm.mul(hs, sigma), rbm.transpose(hs)), qs)
    gain = rbm.mul(rbm.mul(sigma, rbm.transpose(hs)), rbm.inv(s))
    mu = rbm.add(mu, rbm.matvec(gain, nus))
    sigma = rbm.mul(rbm.sub(rbm.eye(N), rbm.mul(gain, hs)), sigma)
    return mu, sigma


def simulate(rng, steps):
    truth = [0.0, 0.0, 0.0, 3.0, 1.0, 2.0, -2.0]
    data = []
    for _ in range(steps):
        u = (0.5, 0.15)
        truth = g(u, truth)
        truth[0] += rng.gauss(0.0, 0.1)
        truth[1] += rng.gauss(0.0, 0.1)
        zs = [rbm.add(h(truth, i), [rng.gauss(0.0, 0.1), rng.gauss(0.0, 0.03)]) for i in range(2)]
        data.append((u, zs))
    return data


def max_abs_diff(a, b):
    if isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def test_eif_equals_ekf_on_a_nonlinear_slam_run():
    rng = random.Random(1)
    mu = [0.0, 0.0, 0.0, 2.8, 1.2, 2.2, -1.8]
    sigma = [[(0.01 if i < 3 else 0.25) if i == j else 0.0 for j in range(N)] for i in range(N)]
    xi, omega = to_information(mu, sigma)
    for u, zs in simulate(rng, 12):
        mu, sigma = ekf_step(mu, sigma, u, zs)
        xi, omega = eif(xi, omega, u, zs, g, gjac, R, h, hjac, Q, residual)
        mu_e, sigma_e = to_moments(xi, omega)
        assert max_abs_diff(mu, mu_e) < 1e-8
        assert max_abs_diff(sigma, sigma_e) < 1e-9


def test_update_changes_only_the_entries_of_the_pose_and_the_landmark():
    rng = random.Random(2)
    a = [[rng.uniform(-1.0, 1.0) for _ in range(N)] for _ in range(N)]
    omega = rbm.add(rbm.mul(a, rbm.transpose(a)), rbm.scale(rbm.eye(N), 0.5))
    xi = [rng.uniform(-1.0, 1.0) for _ in range(N)]
    mu_bar = recover_mean(xi, omega)
    xi2, omega2 = update(xi, omega, mu_bar, [2.0, 0.3], lambda x: h(x, 1), lambda x: hjac(x, 1), Q, residual)
    touched = {0, 1, 2, 5, 6}
    for r in range(N):
        for c in range(N):
            if r not in touched or c not in touched:
                assert omega2[r][c] == omega[r][c]
        if r not in touched:
            assert xi2[r] == xi[r]
    assert any(omega2[r][c] != omega[r][c] for r in touched for c in touched)


def test_the_order_of_the_readings_does_not_matter():
    mu = [0.1, -0.2, 0.05, 3.0, 1.0, 2.0, -2.0]
    sigma = [[0.2 if i == j else 0.0 for j in range(N)] for i in range(N)]
    xi, omega = to_information(mu, sigma)
    zs = [[3.1, 0.3], [2.9, -0.9]]
    a = update(xi, omega, mu, zs[0], lambda x: h(x, 0), lambda x: hjac(x, 0), Q, residual)
    a = update(*a, mu, zs[1], lambda x: h(x, 1), lambda x: hjac(x, 1), Q, residual)
    b = update(xi, omega, mu, zs[1], lambda x: h(x, 1), lambda x: hjac(x, 1), Q, residual)
    b = update(*b, mu, zs[0], lambda x: h(x, 0), lambda x: hjac(x, 0), Q, residual)
    assert max_abs_diff(a[0], b[0]) < 1e-12
    assert max_abs_diff(a[1], b[1]) < 1e-12


def test_round_trip_between_the_two_forms():
    rng = random.Random(4)
    for _ in range(10):
        a = [[rng.uniform(-1.0, 1.0) for _ in range(4)] for _ in range(4)]
        sigma = rbm.add(rbm.mul(a, rbm.transpose(a)), rbm.scale(rbm.eye(4), 0.1))
        mu = [rng.uniform(-5.0, 5.0) for _ in range(4)]
        mu2, sigma2 = to_moments(*to_information(mu, sigma))
        assert max_abs_diff(mu, mu2) < 1e-9
        assert max_abs_diff(sigma, sigma2) < 1e-9


# ---------------------------------------------------------------- the 1-D example of the page


def line_reading(j):
    """z = m_j - x on a line, with the state (x, A, B)."""
    hm = [[-1.0, 0.0, 0.0]]
    hm[0][j] = 1.0
    return (lambda x: [x[j] - x[0]]), (lambda x: hm)


def test_example_of_the_page():
    q = [[0.04]]
    xi = [0.0, 0.0, 0.0]
    omega = [[100.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]  # nothing is known about A and B
    for j, z in ((1, 2.0), (2, 5.0)):
        xi, omega = update(xi, omega, [0.0, 0.0, 0.0], [z], *line_reading(j), q)
    assert omega == [[150.0, -25.0, -25.0], [-25.0, 25.0, 0.0], [-25.0, 0.0, 25.0]]
    mu, sigma = to_moments(xi, omega)
    assert max_abs_diff(mu, [0.0, 2.0, 5.0]) < 1e-12
    # the same as an EKF that adds each landmark through the inverse model
    assert max_abs_diff(sigma, [[0.01, 0.01, 0.01], [0.01, 0.05, 0.01], [0.01, 0.01, 0.05]]) < 1e-12

    r = [[0.01, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    xi, omega, mu_bar = predict(xi, omega, 1.0, lambda u, x: [x[0] + u, x[1], x[2]], lambda u, x: rbm.eye(3), r)
    assert max_abs_diff(omega, [[60.0, -10.0, -10.0], [-10.0, 22.5, -2.5], [-10.0, -2.5, 22.5]]) < 1e-9
    assert abs(omega[1][2] + 2.5) < 1e-9  # the motion links A and B
    xi, omega = update(xi, omega, mu_bar, [0.95], *line_reading(1), q)
    mu, sigma = to_moments(xi, omega)
    assert max_abs_diff(mu, [1.0055556, 1.9777778, 5.0]) < 1e-6
    sd = [math.sqrt(sigma[i][i]) for i in range(3)]
    assert max_abs_diff(sd, [0.1374, 0.1795, 0.2236]) < 1e-4


def test_linear_filter_with_a_flat_prior_matches_batch_least_squares():
    """A robot on a line reads two landmarks for 6 steps; the EIF equals the batch solution."""
    rng = random.Random(5)
    q, rv = 0.04, 0.01
    steps = 6
    zs_all, us = [], []
    x, a, b = 0.0, 2.0, 5.0
    for t in range(steps):
        if t > 0:
            u = 0.5
            us.append(u)
            x += u + rng.gauss(0.0, math.sqrt(rv))
        zs_all.append([a - x + rng.gauss(0.0, 0.2), b - x + rng.gauss(0.0, 0.2)])
    # EIF
    xi, omega = [0.0, 0.0, 0.0], [[1e4, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    mu_bar = [0.0, 0.0, 0.0]
    r = [[rv, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    for t in range(steps):
        if t > 0:
            xi, omega, mu_bar = predict(xi, omega, us[t - 1], lambda u, s: [s[0] + u, s[1], s[2]], lambda u, s: rbm.eye(3), r)
        for j in (1, 2):
            xi, omega = update(xi, omega, mu_bar, [zs_all[t][j - 1]], *line_reading(j), [[q]])
    mu = recover_mean(xi, omega)
    # batch least squares over (x_0 .. x_{T-1}, A, B)
    n = steps + 2
    big = rbm.zeros(n, n)
    vec = [0.0] * n

    def add_row(coef, val, w):
        for i, ci in coef:
            vec[i] += w * ci * val
            for k, ck in coef:
                big[i][k] += w * ci * ck

    add_row([(0, 1.0)], 0.0, 1e4)
    for t in range(steps):
        if t > 0:
            add_row([(t, 1.0), (t - 1, -1.0)], us[t - 1], 1.0 / rv)
        add_row([(steps, 1.0), (t, -1.0)], zs_all[t][0], 1.0 / q)
        add_row([(steps + 1, 1.0), (t, -1.0)], zs_all[t][1], 1.0 / q)
    full = rbm.solve(big, vec)
    want = [full[steps - 1], full[steps], full[steps + 1]]
    assert max_abs_diff(mu, want) < 1e-9
