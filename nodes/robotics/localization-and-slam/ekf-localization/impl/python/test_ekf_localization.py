# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ekf-localization/. The authors are listed in prov/EVPG4E.jsonl.

import math
import random

import pytest

import rbm
import robest
from ekf_localization import (
    associate,
    ekf_localization,
    measure,
    measure_jacobian,
    motion,
    motion_jacobians,
    predict,
    update,
)

LANDMARKS = [[5.0, 0.0], [5.0, 5.0], [0.0, 5.0], [-3.0, 2.0]]
ALPHAS = (0.01, 0.005, 0.005, 0.01)
Q = [[0.1 ** 2, 0.0], [0.0, 0.03 ** 2]]
DT = 0.5


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def mat_close(a, b, tol):
    return all(close(ra, rb, tol) for ra, rb in zip(a, b))


@pytest.mark.parametrize("mu,u", [([1.0, 2.0, 0.3], (1.0, 0.4)), ([0.0, 0.0, -2.0], (0.5, -1.2)), ([2.0, -1.0, 1.0], (0.8, 0.0))])
def test_motion_jacobians_against_finite_differences(mu, u):
    g, v = motion_jacobians(mu, u, DT)
    gn = rbm.num_jacobian(lambda x: motion(x, u, DT), mu)
    if abs(u[1]) > 0.0:
        vn = rbm.num_jacobian(lambda w: motion(mu, w, DT), list(u))
    else:
        # at omega = 0 the derivative in omega is the limit of the arc formula
        eps = 1e-5
        vn = rbm.num_jacobian(lambda w: motion(mu, [w[0], w[1] + eps], DT), list(u))
    assert mat_close(g, gn, 1e-6)
    assert mat_close(v, vn, 1e-4)


def test_measure_jacobian_against_finite_differences():
    mu = [1.0, -0.5, 0.7]
    for lm in LANDMARKS:
        h = measure_jacobian(mu, lm)
        hn = rbm.num_jacobian(lambda x: measure(x, lm), mu)
        assert mat_close(h, hn, 1e-6)


def test_noise_free_motion_follows_the_arc():
    # v = 1 and omega = 0.5 give a circle of radius 2 with the period 4 pi
    mu = [0.0, 0.0, 0.0]
    for _ in range(25):
        mu = motion(mu, (1.0, 0.5), 4.0 * math.pi / 25.0)
    assert close(mu, [0.0, 0.0, 0.0], 1e-9)
    mu = motion([0.0, 0.0, 0.0], (1.0, 0.5), math.pi)  # a quarter of the circle
    assert close(mu, [2.0, 2.0, math.pi / 2.0], 1e-12)
    mu = motion([0.0, 0.0, 0.0], (1.0, 0.5), 2.0 * math.pi)  # half of it
    assert close(mu, [0.0, 4.0, -math.pi], 1e-12)


def test_update_equals_information_form():
    mu = [0.5, 0.2, 0.1]
    sigma = [[0.2, 0.05, 0.01], [0.05, 0.3, -0.02], [0.01, -0.02, 0.1]]
    z = [4.8, -0.1]
    lm = LANDMARKS[0]
    mu1, s1 = update(mu, sigma, z, lm, Q)
    h = measure_jacobian(mu, lm)
    info = rbm.add(rbm.inv(sigma), rbm.mul(rbm.mul(rbm.transpose(h), rbm.inv(Q)), h))
    s2 = rbm.inv(info)
    zhat = measure(mu, lm)
    nu = [z[0] - zhat[0], robest.wrap_angle(z[1] - zhat[1])]
    dmu = rbm.matvec(rbm.mul(rbm.mul(s2, rbm.transpose(h)), rbm.inv(Q)), nu)
    assert mat_close(s1, s2, 1e-12)
    assert close(mu1, [mu[i] + dmu[i] for i in range(3)], 1e-12)


def test_bearing_innovation_wraps():
    mu = [0.0, 0.0, math.pi - 0.01]
    lm = [-10.0, 0.0]  # straight behind the x axis, bearing 0.01 from the heading
    sigma = [[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.01]]
    z = [10.0, -0.01 + 2.0 * math.pi]  # the same angle as -0.01, written beyond pi
    mu1, _ = update(mu, sigma, z, lm, Q)
    # the innovation is -0.02, so theta moves by a small amount and not by 2 pi
    assert abs(robest.wrap_angle(mu1[2] - mu[2])) < 0.02


def simulate(rng, steps, x0):
    x, us, zss = list(x0), [], []
    for t in range(steps):
        u = (1.0, 0.3 if (t // 10) % 2 == 0 else -0.3)
        v, w = u
        a1, a2, a3, a4 = ALPHAS
        vt = v + rng.gauss(0.0, math.sqrt(a1 * v * v + a2 * w * w))
        wt = w + rng.gauss(0.0, math.sqrt(a3 * v * v + a4 * w * w))
        x = motion(x, (vt, wt), DT)
        zs = []
        for lm in LANDMARKS:
            r, phi = measure(x, lm)
            zs.append([r + rng.gauss(0.0, 0.1), robest.wrap_angle(phi + rng.gauss(0.0, 0.03))])
        us.append(u)
        zss.append(zs)
        yield x, u, zs


def test_consistency_by_nees():
    rng = random.Random(11)
    runs, steps, total = 50, 20, 0.0
    sigma0 = [[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.0025]]
    for _ in range(runs):
        x0 = [0.0, 0.0, 0.0]
        mu = robest.gauss_sample(rng, x0, sigma0)
        sigma = sigma0
        for x, u, zs in simulate(rng, steps, x0):
            mu, sigma, _ = ekf_localization(mu, sigma, u, DT, zs, LANDMARKS, ALPHAS, Q, correspondences=[0, 1, 2, 3])
            e = [x[0] - mu[0], x[1] - mu[1], robest.wrap_angle(x[2] - mu[2])]
            total += robest.mahalanobis2(e, [0.0, 0.0, 0.0], sigma)
    # The average NEES of a consistent filter is 3. The bounds are the 0.025
    # and 0.975 quantiles of chi-square(3000) / 1000, about 2.85 and 3.15;
    # the steps of one run are correlated, so the test allows [2.5, 3.5].
    avg = total / (runs * steps)
    assert 2.5 < avg < 3.5


def test_unknown_correspondences_match_known_ones():
    rng = random.Random(5)
    sigma0 = [[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.0025]]
    mu_k, s_k = [0.0, 0.0, 0.0], sigma0
    mu_u, s_u = [0.0, 0.0, 0.0], sigma0
    mu_g, s_g, rejected = [0.0, 0.0, 0.0], sigma0, 0
    for x, u, zs in simulate(rng, 30, [0.0, 0.0, 0.0]):
        order = [2, 0, 3, 1]
        zs = [zs[j] for j in order]
        mu_k, s_k, _ = ekf_localization(mu_k, s_k, u, DT, zs, LANDMARKS, ALPHAS, Q, correspondences=order)
        # maximum likelihood association with no gate
        mu_u, s_u, used = ekf_localization(mu_u, s_u, u, DT, zs, LANDMARKS, ALPHAS, Q, gate=math.inf)
        assert used == order
        # with the 0.99 gate, about 1 in 100 correct readings is dropped
        mu_g, s_g, used = ekf_localization(mu_g, s_g, u, DT, zs, LANDMARKS, ALPHAS, Q)
        assert all(j is None or j == o for j, o in zip(used, order))
        rejected += used.count(None)
    assert close(mu_k, mu_u, 1e-12)
    assert math.hypot(mu_k[0] - x[0], mu_k[1] - x[1]) < 0.2
    assert rejected <= 6  # of 120 readings


def test_gate_rejects_an_outlier():
    mu = [0.0, 0.0, 0.0]
    sigma = [[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.0025]]
    good = measure(mu, LANDMARKS[1])
    assert associate(mu, sigma, good, LANDMARKS, Q, robest.CHI2[(2, 0.99)]) == 1
    outlier = [good[0] + 2.0, good[1]]
    mu2, sigma2, used = ekf_localization(mu, sigma, (0.0, 0.0), DT, [outlier], LANDMARKS, ALPHAS, Q)
    assert used == [None]
    assert close(mu2, mu, 1e-12) and mat_close(sigma2, sigma, 1e-12)


def test_prediction_grows_and_update_shrinks_the_covariance():
    mu = [0.0, 0.0, 0.0]
    sigma = [[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.0025]]
    mu_bar, sigma_bar = predict(mu, sigma, (1.0, 0.3), DT, ALPHAS)
    assert rbm.det(sigma_bar) > rbm.det(sigma)
    mu1, sigma1 = update(mu_bar, sigma_bar, measure(mu_bar, LANDMARKS[0]), LANDMARKS[0], Q)
    assert rbm.det(sigma1) < rbm.det(sigma_bar)
    assert close(mu1, mu_bar, 1e-12)  # a reading equal to its prediction leaves mu unchanged
