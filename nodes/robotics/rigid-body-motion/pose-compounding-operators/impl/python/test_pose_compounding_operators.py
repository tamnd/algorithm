# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pose-compounding-operators/. The authors are listed in prov/Z8QZF9.jsonl.
"""Tests of the compounding operators against SE(3) products, finite
differences, the hand example of the page and Monte Carlo estimates."""

import math
import random

import rbm
from pose_compounding_operators import (
    compound,
    head_to_head,
    invert,
    jac_ominus,
    jac_oplus,
    ominus,
    oplus,
    tail_to_tail,
    wrap,
)


def maxdiff(a, b):
    if a and isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def pose_diff(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(wrap(a[2] - b[2])))


def to_T(a):
    return rbm.make_T(rbm.rot_z(a[2]), [a[0], a[1], 0.0])


def from_T(t):
    return [t[0][3], t[1][3], math.atan2(t[1][0], t[0][0])]


def random_pose(rng, ang=3.0):
    return [rng.uniform(-5.0, 5.0), rng.uniform(-5.0, 5.0), rng.uniform(-ang, ang)]


def sample_cov(points, mean):
    n = len(points)
    return [[sum((p[i] - mean[i]) * (p[j] - mean[j]) for p in points) / (n - 1) for j in range(3)] for i in range(3)]


def sampler(rng, mean, cov):
    low = rbm.cholesky(cov)

    def draw():
        z = [rng.gauss(0.0, 1.0) for _ in range(3)]
        return [mean[i] + sum(low[i][k] * z[k] for k in range(i + 1)) for i in range(3)]

    return draw


def test_oplus_and_ominus_match_se3_products():
    rng = random.Random(1)
    for _ in range(200):
        a, b = random_pose(rng), random_pose(rng)
        assert pose_diff(oplus(a, b), from_T(rbm.mul(to_T(a), to_T(b)))) < 1e-12
        assert pose_diff(ominus(a), from_T(rbm.T_inv(to_T(a)))) < 1e-12
        assert pose_diff(oplus(ominus(a), a), [0.0, 0.0, 0.0]) < 1e-12
        assert pose_diff(oplus(a, ominus(a)), [0.0, 0.0, 0.0]) < 1e-12


def test_associative_not_commutative():
    rng = random.Random(2)
    for _ in range(100):
        a, b, c = random_pose(rng), random_pose(rng), random_pose(rng)
        assert pose_diff(oplus(oplus(a, b), c), oplus(a, oplus(b, c))) < 1e-12
    a, b = [2.0, 1.0, math.pi / 2], [1.0, 0.0, 0.0]
    assert pose_diff(oplus(b, a), [3.0, 1.0, math.pi / 2]) < 1e-12
    assert pose_diff(oplus(a, b), oplus(b, a)) > 0.5


def test_hand_example():
    a, b = [2.0, 1.0, math.pi / 2], [1.0, 0.0, 0.0]
    ca = [[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.0025]]
    m, c = compound(a, ca, b, ca)
    assert pose_diff(m, [2.0, 2.0, math.pi / 2]) < 1e-12
    want = [[0.0225, 0.0, -0.0025], [0.0, 0.02, 0.0], [-0.0025, 0.0, 0.005]]
    assert maxdiff(c, want) < 1e-12
    mi, ci = invert(a, ca)
    assert pose_diff(mi, [-1.0, 2.0, -math.pi / 2]) < 1e-12
    want_i = [[0.02, 0.005, -0.005], [0.005, 0.0125, -0.0025], [-0.005, -0.0025, 0.0025]]
    assert maxdiff(ci, want_i) < 1e-12


def test_jacobians_match_finite_differences():
    rng = random.Random(3)
    for _ in range(50):
        a, b = random_pose(rng, 1.4), random_pose(rng, 1.4)
        j1, j2 = jac_oplus(a, b)
        assert maxdiff(j1, rbm.num_jacobian(lambda u: oplus(u, b), a)) < 1e-6
        assert maxdiff(j2, rbm.num_jacobian(lambda u: oplus(a, u), b)) < 1e-6
        assert maxdiff(jac_ominus(a), rbm.num_jacobian(ominus, a)) < 1e-6


def test_head_to_head_and_tail_to_tail():
    rng = random.Random(4)
    c1 = [[0.02, 0.003, 0.0], [0.003, 0.01, 0.001], [0.0, 0.001, 0.004]]
    c2 = [[0.01, 0.0, 0.002], [0.0, 0.03, 0.0], [0.002, 0.0, 0.005]]
    c12 = [[0.002, 0.0, 0.0], [0.0, 0.001, 0.0], [0.0, 0.0, 0.0005]]
    for _ in range(20):
        a, b = random_pose(rng, 1.4), random_pose(rng, 1.4)
        m, c = tail_to_tail(a, c1, b, c2, c12)
        assert pose_diff(m, oplus(ominus(a), b)) < 1e-12
        f = lambda u: oplus(ominus(u[:3]), u[3:])
        j = rbm.num_jacobian(f, a + b)
        big = [row[:3] + [0.0] * 3 for row in c1] + [row[:] + [0.0] * 3 for row in rbm.transpose(c12)]
        for i in range(3):
            big[i][3:] = c12[i]
            big[i + 3][3:] = c2[i]
        want = rbm.mul(rbm.mul(j, big), rbm.transpose(j))
        assert maxdiff(c, want) < 1e-6
        m, c = head_to_head(a, c1, b, c2, c12)
        assert pose_diff(m, oplus(a, ominus(b))) < 1e-12
        g = lambda u: oplus(u[:3], ominus(u[3:]))
        j = rbm.num_jacobian(g, a + b)
        want = rbm.mul(rbm.mul(j, big), rbm.transpose(j))
        assert maxdiff(c, want) < 1e-6


def test_correlation_must_be_kept():
    a = [2.0, 1.0, math.pi / 2]
    ca = [[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.0025]]
    # x_ij (+) (-) x_ij is the identity pose, with no uncertainty at all.
    m, c = head_to_head(a, ca, a, ca, ca)
    assert pose_diff(m, [0.0, 0.0, 0.0]) < 1e-12
    assert maxdiff(c, rbm.zeros(3, 3)) < 1e-15
    # Dropping the cross-covariance gives a large wrong covariance.
    m, c = head_to_head(a, ca, a, ca)
    want = [[0.025, -0.01, 0.005], [-0.01, 0.04, -0.01], [0.005, -0.01, 0.005]]
    assert maxdiff(c, want) < 1e-12


def test_small_noise_matches_monte_carlo():
    rng = random.Random(5)
    a, b = [2.0, 1.0, math.pi / 2], [1.0, 0.0, 0.0]
    ca = [[0.01, 0.0, 0.0], [0.0, 0.01, 0.0], [0.0, 0.0, 0.0025]]
    m, c = compound(a, ca, b, ca)
    da, db = sampler(rng, a, ca), sampler(rng, b, ca)
    pts = [oplus(da(), db()) for _ in range(20000)]
    mean = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
    assert maxdiff(mean, m) < 0.01
    assert maxdiff(sample_cov(pts, mean), c) < 0.05 * 0.0225
    mi, ci = invert(a, ca)
    pts = [ominus(da()) for _ in range(20000)]
    mean = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
    assert maxdiff(mean, mi) < 0.01
    assert maxdiff(sample_cov(pts, mean), ci) < 0.05 * 0.0225


def test_large_heading_noise_breaks_the_linearization():
    # Drive 10 m with a heading error of standard deviation 0.5 rad.
    rng = random.Random(6)
    tiny = 1e-10
    a, ca = [0.0, 0.0, 0.0], [[tiny, 0.0, 0.0], [0.0, tiny, 0.0], [0.0, 0.0, 0.25]]
    b, cb = [10.0, 0.0, 0.0], [[tiny, 0.0, 0.0], [0.0, tiny, 0.0], [0.0, 0.0, tiny]]
    m, c = compound(a, ca, b, cb)
    assert maxdiff(m, [10.0, 0.0, 0.0]) < 1e-12
    assert abs(c[0][0]) < 1e-8 and abs(c[1][1] - 25.0) < 1e-8
    # Exact moments of (10 cos phi, 10 sin phi) with phi ~ N(0, 0.25).
    ex = 10.0 * math.exp(-0.125)
    vx = 100.0 * ((1.0 + math.exp(-0.5)) / 2.0 - math.exp(-0.25))
    vy = 100.0 * (1.0 - math.exp(-0.5)) / 2.0
    da, db = sampler(rng, a, ca), sampler(rng, b, cb)
    pts = [oplus(da(), db()) for _ in range(20000)]
    mean = [sum(p[i] for p in pts) / len(pts) for i in range(3)]
    cov = sample_cov(pts, mean)
    assert abs(mean[0] - ex) < 0.05
    assert abs(cov[0][0] - vx) < 0.15
    assert abs(cov[1][1] - vy) < 0.8
    # The first-order answer misses the mean by more than 1 m and the
    # variance across the track by more than 5 m^2.
    assert m[0] - mean[0] > 1.0
    assert c[1][1] - cov[1][1] > 5.0
