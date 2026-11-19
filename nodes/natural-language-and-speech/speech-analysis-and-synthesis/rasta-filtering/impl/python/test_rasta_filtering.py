# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rasta-filtering/. The authors are listed in prov/C4662N.jsonl.

import cmath
import math
import random

from rasta_filtering import rasta_bands, rasta_filter


def _h(f, rho, frame_rate=100.0):
    z = cmath.exp(2j * math.pi * f / frame_rate)
    return 0.1 * (2 + z**-1 - z**-3 - 2 * z**-4) / (1 - rho * z**-1)


def test_impulse_response():
    rho = 0.98
    x = [0.0] * 5 + [1.0] + [0.0] * 30
    y = rasta_filter(x, rho)
    assert y[:5] == [0.0] * 5
    b = [0.2, 0.1, 0.0, -0.1, -0.2]
    # h[n] = sum_{k <= min(n, 4)} b_k rho^(n - k)
    for n in range(30):
        ref = sum(b[k] * rho ** (n - k) for k in range(min(n, 4) + 1))
        assert abs(y[5 + n] - ref) < 1e-12


def test_constant_gives_zero():
    assert all(v == 0.0 for v in rasta_filter([3.5] * 50))


def test_offset_does_not_change_the_output():
    rng = random.Random(2)
    x = [rng.uniform(-5, 5) for _ in range(300)]
    for rho in (0.98, 0.94):
        a = rasta_filter(x, rho)
        b = rasta_filter([v + 17.0 for v in x], rho)
        assert all(abs(u - v) < 1e-9 for u, v in zip(a, b))


def test_step_decays_geometrically():
    rho = 0.98
    x = [0.0] * 10 + [1.0] * 200
    y = rasta_filter(x, rho)
    # after the 5 numerator taps have all seen the step, only the pole acts
    for t in range(14, 210):
        assert abs(y[t] - rho * y[t - 1]) < 1e-12
    # the first outputs are the partial sums of the taps: 0.2, then 0.2 rho + 0.1, ...
    assert abs(y[10] - 0.2) < 1e-12 and abs(y[11] - (0.2 * rho + 0.3)) < 1e-12
    assert y[209] < 0.03 * max(y)


def test_sine_gain_matches_the_transfer_function():
    rho = 0.98
    for f in (0.5, 4.0, 12.0, 25.0):
        n = 4000
        x = [math.sin(2 * math.pi * f * t / 100.0) for t in range(n)]
        y = rasta_filter(x, rho)
        tail = range(2000, n)
        c = sum(y[t] * math.cos(2 * math.pi * f * t / 100.0) for t in tail) * 2 / len(tail)
        s = sum(y[t] * math.sin(2 * math.pi * f * t / 100.0) for t in tail) * 2 / len(tail)
        assert abs(math.hypot(c, s) - abs(_h(f, rho))) < 2e-3


def test_pass_band_numbers():
    # the -3 dB points of the paper's filter at 100 frames per second
    assert abs(_h(0.0 + 1e-9, 0.98)) < 1e-6
    peak = max(abs(_h(i / 100.0, 0.98)) for i in range(1, 5000))
    assert abs(_h(0.30, 0.98)) < peak / math.sqrt(2) < abs(_h(0.32, 0.98))
    assert abs(_h(12.9, 0.98)) < peak / math.sqrt(2) < abs(_h(12.8, 0.98))


def test_bands_remove_a_fixed_channel():
    rng = random.Random(4)
    spec = [[rng.uniform(-3, 3) for _ in range(6)] for _ in range(80)]
    channel = [0.5, -1.0, 2.0, 0.0, 3.0, -0.25]  # a fixed log gain per band
    a = rasta_bands(spec)
    b = rasta_bands([[v + g for v, g in zip(row, channel)] for row in spec])
    assert len(a) == 80 and all(len(r) == 6 for r in a)
    assert all(abs(u - v) < 1e-9 for ra, rb in zip(a, b) for u, v in zip(ra, rb))
    col = rasta_filter([row[2] for row in spec])
    assert all(abs(a[t][2] - col[t]) < 1e-15 for t in range(80))


def test_bad_arguments():
    assert rasta_filter([]) == [] and rasta_bands([]) == []
    for bad in (1.0, -0.1):
        try:
            rasta_filter([1.0], bad)
        except ValueError:
            continue
        raise AssertionError(bad)
    try:
        rasta_bands([[1.0, 2.0], [1.0]])
    except ValueError:
        pass
    else:
        raise AssertionError("ragged input must fail")
