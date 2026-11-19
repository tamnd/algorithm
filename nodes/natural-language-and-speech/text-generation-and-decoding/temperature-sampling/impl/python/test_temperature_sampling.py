# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/temperature-sampling/. The authors are listed in prov/C3YE2Y.jsonl.

import math
import random

from nlslog import NEG_INF, argmax
from temperature_sampling import limit_distribution, temperature_distribution, temperature_sample

Z = [2.0, 1.0, 0.0]


def entropy(p):
    return -math.fsum(x * math.log(x) for x in p if x > 0)


def test_check_values() -> None:
    for t, want in (
        (1.0, (0.66524, 0.24473, 0.09003)),
        (0.5, (0.86681, 0.11731, 0.01588)),
        (2.0, (0.50648, 0.30720, 0.18632)),
    ):
        got = temperature_distribution(Z, t)
        for g, w in zip(got, want):
            assert abs(g - w) < 5e-6
    assert abs(entropy(temperature_distribution(Z, 1.0)) - 0.8324) < 1e-4


def test_power_form_is_the_same() -> None:
    # softmax(z / T) equals p^(1/T) renormalized, with p = softmax(z)
    rng = random.Random(1)
    for _ in range(200):
        z = [rng.uniform(-4, 4) for _ in range(6)]
        t = rng.uniform(0.2, 5)
        p = temperature_distribution(z, 1.0)
        powered = [x ** (1 / t) for x in p]
        s = math.fsum(powered)
        for a, b in zip(temperature_distribution(z, t), (x / s for x in powered)):
            assert abs(a - b) < 1e-12


def test_entropy_grows_with_the_temperature() -> None:
    rng = random.Random(2)
    temps = [0.05 * j for j in range(1, 101)]
    for _ in range(100):
        z = [rng.uniform(-3, 3) for _ in range(5)]
        hs = [entropy(temperature_distribution(z, t)) for t in temps]
        for a, b in zip(hs, hs[1:]):
            assert b >= a - 1e-12
        assert hs[-1] <= math.log(5) + 1e-12


def test_limits() -> None:
    assert limit_distribution(Z, "zero") == [1.0, 0.0, 0.0]
    assert limit_distribution([2.0, 2.0, 0.0], "zero") == [0.5, 0.5, 0.0]
    assert limit_distribution([2.0, NEG_INF, 0.0], "inf") == [0.5, 0.0, 0.5]
    for z in (Z, [2.0, 2.0, 0.0], [3.0, NEG_INF, 1.0, 0.5]):
        cold = temperature_distribution(z, 0.01)
        hot = temperature_distribution(z, 1e6)
        for a, b in zip(cold, limit_distribution(z, "zero")):
            assert abs(a - b) < 1e-6
        for a, b in zip(hot, limit_distribution(z, "inf")):
            assert abs(a - b) < 1e-5


def test_shift_does_not_matter_and_masked_tokens_stay_out() -> None:
    rng = random.Random(3)
    for _ in range(100):
        z = [rng.uniform(-3, 3) for _ in range(4)]
        c = rng.uniform(-100, 100)
        for a, b in zip(temperature_distribution(z, 0.7), temperature_distribution([x + c for x in z], 0.7)):
            assert abs(a - b) < 1e-9
    z = [1.0, NEG_INF, 0.0]
    for t in (0.1, 1.0, 50.0):
        assert temperature_distribution(z, t)[1] == 0.0
        assert all(temperature_sample(z, t, rng) != 1 for _ in range(300))


def test_sampling_frequencies_and_gumbel_max() -> None:
    rng = random.Random(4)
    draws = 20000
    for t in (0.5, 2.0):
        want = temperature_distribution(Z, t)
        direct = [0, 0, 0]
        gumbel = [0, 0, 0]
        for _ in range(draws):
            direct[temperature_sample(Z, t, rng)] += 1
            # a second method: argmax of z / T plus Gumbel noise
            g = [x / t - math.log(-math.log(1.0 - rng.random())) for x in Z]
            gumbel[argmax(g)] += 1
        for a, b, w in zip(direct, gumbel, want):
            assert abs(a / draws - w) < 0.01
            assert abs(b / draws - w) < 0.01


def test_huge_logits_do_not_overflow() -> None:
    p = temperature_distribution([1000.0, 999.0], 0.01)
    assert p[0] > 0.999999 and p[1] < 1e-6
    rng = random.Random(5)
    assert temperature_sample([1e6, 0.0], 1.0, rng) == 0


def test_bad_temperature() -> None:
    for t in (0.0, -1.0):
        try:
            temperature_sample(Z, t, random.Random(6))
        except ValueError:
            pass
        else:
            raise AssertionError("no ValueError")
