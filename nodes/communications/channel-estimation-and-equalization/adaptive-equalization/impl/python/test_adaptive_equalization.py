# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-equalization/. The authors are listed in prov/FM2HQC.jsonl.

import math
import random

import pytest

import cbb
from adaptive_equalization import adaptive_equalize, mse, nearest, wiener_taps

QPSK = [complex(a, b) / math.sqrt(2) for a in (-1, 1) for b in (-1, 1)]
PROAKIS_B = [0.407, 0.815, 0.407]


def run(h, n, delay, mu, k, n0, seed, n_train):
    rng = random.Random(seed)
    x = [rng.choice(QPSK) for _ in range(k)]
    y = cbb.awgn(rng, cbb.conv(x, h)[:k], n0)
    c, z, targets = adaptive_equalize(y, x[:n_train], n, delay, mu, QPSK)
    return x, c, z, targets


def test_wiener_taps_one_tap_closed_form() -> None:
    h = [0.8 - 0.3j, 0.4j, -0.2]
    n0 = 0.05
    c = wiener_taps(h, 1, 0, n0)
    want = h[0].conjugate() / (cbb.norm2(h) + n0)
    assert abs(c[0] - want) < 1e-12


def test_wiener_taps_are_a_minimum_of_the_mse() -> None:
    h = [1, 0.5]
    n0 = 0.01
    w = wiener_taps(h, 7, 3, n0)
    j0 = mse(w, h, 3, n0)
    rng = random.Random(7)
    for _ in range(20):
        dv = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) * 1e-3 for _ in w]
        assert mse([a + b for a, b in zip(w, dv)], h, 3, n0) > j0


def test_training_mode_converges_to_the_wiener_taps() -> None:
    h, n, d, n0 = [1, 0.5], 11, 5, 0.01
    x, c, z, targets = run(h, n, d, 0.01, 6000, n0, 1, 6000)
    w = wiener_taps(h, n, d, n0)
    assert max(abs(a - b) for a, b in zip(c, w)) < 0.05
    assert mse(c, h, d, n0) < 1.1 * mse(w, h, d, n0)
    assert all(t == x[k + n - 1 - d] for k, t in enumerate(targets))


def test_decision_mode_keeps_the_taps_after_training() -> None:
    h, n, d, n0 = [1, 0.5], 11, 5, 0.01
    x, c, z, targets = run(h, n, d, 0.01, 12000, n0, 2, 1000)
    errors = sum(nearest(z[t], QPSK) != x[t + n - 1 - d] for t in range(1000, len(z)))
    assert errors == 0
    assert mse(c, h, d, n0) < 1.1 * mse(wiener_taps(h, n, d, n0), h, d, n0)


def test_slow_modes_on_a_channel_with_a_deep_notch() -> None:
    # Proakis B: the MSE is near the Wiener value, but the taps are not, because of the eigenvalue spread
    n, d, n0 = 11, 6, 0.01
    x, c, z, targets = run(PROAKIS_B, n, d, 0.01, 6000, n0, 1, 6000)
    w = wiener_taps(PROAKIS_B, n, d, n0)
    assert mse(c, PROAKIS_B, d, n0) < 1.1 * mse(w, PROAKIS_B, d, n0)
    assert max(abs(a - b) for a, b in zip(c, w)) > 0.1


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        adaptive_equalize([1, 2], [], 0, 0, 0.01, QPSK)
    with pytest.raises(ValueError):
        adaptive_equalize([1, 2], [], 2, 2, 0.01, QPSK)
    with pytest.raises(ValueError):
        adaptive_equalize([1, 2], [], 2, 0, 0.0, QPSK)
