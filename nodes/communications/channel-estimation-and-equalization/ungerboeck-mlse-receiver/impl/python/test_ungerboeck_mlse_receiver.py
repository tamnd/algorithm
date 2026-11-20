# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ungerboeck-mlse-receiver/. The authors are listed in prov/REAJPJ.jsonl.

import math
import random

import pytest

from ungerboeck_mlse_receiver import (
    autocorrelation,
    brute_force,
    convolve,
    matched_filter,
    ungerboeck_metric,
    ungerboeck_mlse,
)


def cn(rng, var):
    s = math.sqrt(var / 2)
    return complex(rng.gauss(0, s), rng.gauss(0, s))


def sq(v):
    return sum(abs(a) ** 2 for a in v)


def test_example_on_the_page() -> None:
    h, y = [1, 0.5], [0.9, 0.1, -1.2, 0.6, 0.4]
    z = matched_filter(y, h, 4)
    assert max(abs(a - b) for a, b in zip(z, [0.95, -0.5, -0.9, 0.8])) < 1e-12
    assert autocorrelation(h) == [1.25, 0.5]
    d = ungerboeck_mlse(y, h, [1, -1])
    assert d == [1, -1, -1, 1]
    assert abs(ungerboeck_metric(z, autocorrelation(h), d) - 2.3) < 1e-12
    assert abs(sq(y) - sq([a - b for a, b in zip(y, convolve(h, d))]) - 2.3) < 1e-12


def test_metric_identity_for_any_y_and_x() -> None:
    rng = random.Random(7601)
    for _ in range(50):
        h = [cn(rng, 1.0) for _ in range(rng.randint(1, 5))]
        n = rng.randint(1, 12)
        x = [cn(rng, 1.0) for _ in range(n)]
        y = [cn(rng, 2.0) for _ in range(n + len(h) - 1)]
        z = matched_filter(y, h, n)
        lhs = ungerboeck_metric(z, autocorrelation(h), x)
        rhs = sq(y) - sq([a - b for a, b in zip(y, convolve(h, x))])
        assert abs(lhs - rhs) < 1e-9


def test_equals_brute_force_bpsk_with_and_without_tail() -> None:
    rng = random.Random(7602)
    for trial in range(16):
        h = [rng.gauss(0, 1) for _ in range(rng.randint(1, 4))]
        tail = [rng.choice((-1, 1)) for _ in range(len(h) - 1)] if trial % 2 else []
        x = [rng.choice((-1, 1)) for _ in range(10)] + tail
        y = [v + rng.gauss(0, 0.8) for v in convolve(h, x)]
        assert ungerboeck_mlse(y, h, [1, -1], tail=tail) == brute_force(y, h, [1, -1], tail=tail)


def test_equals_brute_force_complex_qpsk_and_4pam() -> None:
    rng = random.Random(7603)
    qpsk = [complex(a, b) for a in (-1, 1) for b in (-1, 1)]
    for _ in range(10):
        h = [cn(rng, 1.0) for _ in range(rng.randint(2, 3))]
        x = [rng.choice(qpsk) for _ in range(5)]
        y = [v + cn(rng, 1.0) for v in convolve(h, x)]
        assert ungerboeck_mlse(y, h, qpsk) == brute_force(y, h, qpsk)
    pam = [3, 1, -1, -3]
    for _ in range(3):
        h = [1.0, rng.uniform(-1, 1)]
        x = [rng.choice(pam) for _ in range(5)]
        y = [v + rng.gauss(0, 0.7) for v in convolve(h, x)]
        assert ungerboeck_mlse(y, h, pam) == brute_force(y, h, pam)


def test_noiseless_recovery_on_known_channels() -> None:
    rng = random.Random(7604)
    for h in ([1, 0.5], [0.5, 1], [0.407, 0.815, 0.407], [0.227, 0.460, 0.688, 0.460, 0.227]):
        x = [rng.choice((-1, 1)) for _ in range(300)]
        assert ungerboeck_mlse(convolve(h, x), h, [1, -1]) == x


def test_input_checks() -> None:
    with pytest.raises(ValueError):
        ungerboeck_mlse([1.0], [1, 0.5], [1, -1])
    with pytest.raises(ValueError):
        ungerboeck_mlse([1.0, 2.0, 3.0], [1, 0.5], [1, -1], tail=[2])
