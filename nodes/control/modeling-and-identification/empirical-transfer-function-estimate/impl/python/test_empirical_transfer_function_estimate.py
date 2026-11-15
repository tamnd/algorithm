# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/empirical-transfer-function-estimate/. The authors are listed in prov/H22G0R.jsonl.

import cmath
import math
import random
import statistics

from empirical_transfer_function_estimate import dft, etfe


def _g(w):
    z1 = cmath.exp(-1j * w)
    return z1 / (1 - 0.5 * z1)


def _simulate(u, e=None):
    # y(t) = 0.5 y(t-1) + u(t-1) + e(t), from rest.
    y = []
    x = 0.0
    prev_u = 0.0
    for t in range(len(u)):
        x = 0.5 * x + prev_u
        prev_u = u[t]
        y.append(x + (e[t] if e else 0.0))
    return y


def test_worked_example():
    u = [1, 1, -1, -1]
    y = [-1.2, 0.4, 1.2, -0.4]
    out = etfe(y, u)
    assert [w for w, _ in out] == [0.0, math.pi / 2, math.pi]
    assert out[0][1] is None and out[2][1] is None
    assert abs(out[1][1] - (-0.4 - 0.8j)) < 1e-12
    assert abs(out[1][1] - _g(math.pi / 2)) < 1e-12


def test_random_fft_matches_direct_sum():
    rng = random.Random(1)
    for _ in range(500):
        n = rng.choice([1, 2, 3, 4, 5, 6, 8, 12, 16])
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(n)]
        got = dft(x)
        for k in range(n):
            want = sum(x[t] * cmath.exp(-2j * math.pi * k * t / n) for t in range(n))
            assert abs(got[k] - want) < 1e-9


def test_exact_in_periodic_steady_state():
    rng = random.Random(2)
    period = 16
    one = [rng.choice((-1.0, 1.0)) for _ in range(period)]
    u = one * 8
    y = _simulate(u)
    out = etfe(y[-period:], u[-period:])
    seen = 0
    for w, g in out:
        if g is not None:
            assert abs(g - _g(w)) < 1e-9
            seen += 1
    assert seen >= 3


def _errors(n, gamma, seed):
    rng = random.Random(seed)
    burn = 200
    u = [rng.choice((-1.0, 1.0)) for _ in range(n + burn)]
    e = [rng.gauss(0.0, 0.5) for _ in range(n + burn)]
    y = _simulate(u, e)
    out = etfe(y[burn:], u[burn:], gamma)
    return statistics.median(abs(g - _g(w)) ** 2 for w, g in out[1:-1] if g is not None)


def test_raw_error_does_not_fall_but_smoothed_error_does():
    raw_small = _errors(256, 0, 7)
    raw_big = _errors(4096, 0, 7)
    assert 0.5 < raw_big / raw_small < 2.0
    sm_small = _errors(256, 256 // 32, 7)
    sm_big = _errors(4096, 4096 // 32, 7)
    assert sm_big < sm_small / 8
    assert sm_small < raw_small


def test_gamma_zero_is_raw_ratio():
    rng = random.Random(3)
    u = [rng.uniform(-1, 1) for _ in range(8)]
    y = [rng.uniform(-1, 1) for _ in range(8)]
    uu, yy = dft(u), dft(y)
    for k, (w, g) in enumerate(etfe(y, u)):
        assert abs(w - 2 * math.pi * k / 8) < 1e-15
        assert abs(g - yy[k] / uu[k]) < 1e-12


def test_edges_and_bad_arguments():
    assert etfe([2.0], [1.0]) == [(0.0, 2.0)]
    assert etfe([0.0, 0.0], [0.0, 1.0])[0][1] == 0.0
    for args in (([1.0], [1.0, 2.0]), ([], []), ([1.0] * 4, [1.0] * 4, 2), ([1.0] * 4, [1.0] * 4, -1)):
        try:
            etfe(*args)
        except ValueError:
            continue
        raise AssertionError("expected ValueError for %r" % (args,))
