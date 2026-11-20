# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kalman-channel-tracking/. The authors are listed in prov/JMK6AT.jsonl.

import math
import random

import pytest

import cbb
from kalman_channel_tracking import (
    ar1_channel,
    ar1_coefficient,
    bessel_j0,
    kalman_track,
    regressor,
    transmit,
)


def qpsk(rng):
    return complex(rng.choice((-1, 1)), rng.choice((-1, 1))) / math.sqrt(2)


def test_bessel_j0() -> None:
    assert bessel_j0(0.0) == 1.0
    assert abs(bessel_j0(2.404825557695773)) < 1e-13  # the first zero
    assert abs(bessel_j0(1.0) - 0.7651976865579666) < 1e-14
    assert abs(ar1_coefficient(0.01) - 0.99901328) < 1e-8


def test_static_channel_gives_the_batch_estimate() -> None:
    # a = 1 makes Q = 0: the filter is the batch Bayesian LMMSE estimate of one fixed h
    rng = random.Random(1)
    p, n0, k = [1.0, 0.5, 0.25], 0.2, 20
    x = [qpsk(rng) for _ in range(k)]
    h = [cbb.cn(rng, v) for v in p]
    y = transmit(rng, [h] * k, x, n0)
    est, cov = kalman_track(y, x, 1.0, p, n0)
    c = [regressor(x, t, 3) for t in range(k)]
    a = cbb.add(cbb.scale(1 / n0, cbb.matmul(cbb.herm(c), c)), [[1 / p[i] if i == j else 0 for j in range(3)] for i in range(3)])
    want = cbb.solve(a, cbb.scale(1 / n0, cbb.matvec(cbb.herm(c), y)))
    assert max(abs(u - v) for u, v in zip(est[-1], want)) < 1e-9
    want_cov = cbb.inv(a)
    assert max(abs(cov[-1][i][j] - want_cov[i][j]) for i in range(3) for j in range(3)) < 1e-9


def test_filter_equals_the_joint_lmmse_estimate() -> None:
    # the stacked taps (h_0, ..., h_(T-1)) are Gaussian with Cov(h_k[l], h_m[l]) = a^|k-m| P[l]
    rng = random.Random(2)
    a, p, n0, t = 0.9, [1.0, 0.4], 0.3, 6
    x = [qpsk(rng) for _ in range(t)]
    hs = ar1_channel(rng, a, p, t)
    y = transmit(rng, hs, x, n0)
    est, cov = kalman_track(y, x, a, p, n0)
    n = 2 * t
    sig = [[a ** abs(i // 2 - j // 2) * p[i % 2] if i % 2 == j % 2 else 0 for j in range(n)] for i in range(n)]
    obs = [[0j] * n for _ in range(t)]
    for k in range(t):
        obs[k][2 * k:2 * k + 2] = regressor(x, k, 2)
    for last in range(1, t + 1):
        # the estimate of h_(last-1) from y[0], ..., y[last-1]
        o = [row for row in obs[:last]]
        s_oh = cbb.matmul(o, sig)
        cyy = cbb.add(cbb.matmul(s_oh, cbb.herm(o)), cbb.scale(n0, cbb.eye(last)))
        gain_t = cbb.solve(cyy, s_oh)  # Cyy^-1 O Sigma
        rows = [2 * (last - 1), 2 * (last - 1) + 1]
        want = [sum(gain_t[r][i].conjugate() * y[r] for r in range(last)) for i in rows]
        assert max(abs(u - v) for u, v in zip(est[last - 1], want)) < 1e-9
        want_cov = [[sig[i][j] - sum(s_oh[r][i].conjugate() * gain_t[r][j] for r in range(last)) for j in rows] for i in rows]
        assert max(abs(cov[last - 1][u][v] - want_cov[u][v]) for u in range(2) for v in range(2)) < 1e-9


def test_error_power_matches_the_trace_of_the_covariance() -> None:
    # E ||h_k - h^_k||^2 = trace of the error covariance, checked by simulation (seed 3)
    rng = random.Random(3)
    # 100 runs of 100 symbols; the measured ratio is 1.0005
    a, p, n0 = ar1_coefficient(0.05), [0.6, 0.4], 0.1
    err = tr = 0.0
    for _ in range(100):
        x = [qpsk(rng) for _ in range(100)]
        hs = ar1_channel(rng, a, p, 100)
        y = transmit(rng, hs, x, n0)
        est, cov = kalman_track(y, x, a, p, n0)
        for k in range(100):
            err += cbb.norm2(cbb.sub(hs[k], est[k]))
            tr += cov[k][0][0].real + cov[k][1][1].real
    assert abs(err / tr - 1.0) < 0.05


def test_tracking_beats_a_static_model() -> None:
    # on a fading channel, the filter with the right a has a smaller error than the filter with a = 1
    rng = random.Random(4)
    a, p, n0, k = ar1_coefficient(0.02), [0.6, 0.4], 0.05, 600
    x = [qpsk(rng) for _ in range(k)]
    hs = ar1_channel(rng, a, p, k)
    y = transmit(rng, hs, x, n0)
    good, _ = kalman_track(y, x, a, p, n0)
    stale, _ = kalman_track(y, x, 1.0, p, n0)
    e_good = sum(cbb.norm2(cbb.sub(hs[t], good[t])) for t in range(300, k))
    e_stale = sum(cbb.norm2(cbb.sub(hs[t], stale[t])) for t in range(300, k))
    assert e_good < 0.2 * e_stale


def test_covariance_stays_hermitian_and_bounded() -> None:
    rng = random.Random(5)
    a, p, n0 = 0.95, [1.0, 0.5, 0.2], 0.5
    x = [qpsk(rng) for _ in range(200)]
    y = transmit(rng, ar1_channel(rng, a, p, 200), x, n0)
    _, cov = kalman_track(y, x, a, p, n0)
    for s in cov:
        for i in range(3):
            assert 0 < s[i][i].real <= p[i] + 1e-12
            for j in range(3):
                assert abs(s[i][j] - s[j][i].conjugate()) < 1e-12


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        kalman_track([1j], [1, 1], 0.9, [1.0], 0.1)
    with pytest.raises(ValueError):
        kalman_track([1j], [1], 1.5, [1.0], 0.1)
    with pytest.raises(ValueError):
        kalman_track([1j], [1], 0.9, [1.0], 0.0)
