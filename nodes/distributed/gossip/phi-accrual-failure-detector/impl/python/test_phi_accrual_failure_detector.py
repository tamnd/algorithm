# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phi-accrual-failure-detector/. The authors are listed in prov/TY0JW4.jsonl.

import math
import random
from statistics import NormalDist

from phi_accrual_failure_detector import (PhiAccrualDetector, exponential_phi,
                                          logistic_phi, mistake_rate)


def normal_intervals(n: int, seed: int) -> list[float]:
    rng = random.Random(seed)
    return [max(1e-3, rng.gauss(100, 10)) for _ in range(n)]


def test_mistake_rate_is_ten_to_minus_phi():
    xs = normal_intervals(100000, 1)
    for threshold, tol in ((1, 0.05), (2, 0.15), (3, 0.35)):
        rate = mistake_rate(xs, threshold)
        assert abs(rate / 10 ** -threshold - 1) < tol


def test_phi_grows_with_silence():
    d = PhiAccrualDetector()
    rng = random.Random(2)
    t = 0.0
    for _ in range(500):
        d.heartbeat(t)
        t += rng.gauss(100, 10)
    mean, std = d.mean_std()
    # at the mean the next heartbeat is late with probability 1/2
    assert abs(d.phi(d.last + mean) - math.log10(2)) < 1e-9
    values = [d.phi(d.last + x) for x in range(0, 400, 10)]
    assert all(a <= b for a, b in zip(values, values[1:]))
    assert values[-1] > 50
    for threshold in (1, 3, 8, 12):
        ts = d.suspicion_time(threshold)
        assert abs(d.phi(d.last + ts) - threshold) < 1e-6
        assert not d.suspect(d.last + ts - 1, threshold)
        assert d.suspect(d.last + ts + 1, threshold)


def test_window_forgets_old_intervals():
    d = PhiAccrualDetector(window=100)
    t = 0.0
    for k in range(400):
        d.heartbeat(t)
        t += 100.0 if k < 200 else 300.0 + (k % 3)
    mean, _ = d.mean_std()
    assert abs(mean - 301) < 1


def test_exponential_model_of_cassandra():
    rng = random.Random(3)
    mean = 100.0
    ys = [rng.expovariate(1 / mean) for _ in range(100000)]
    for threshold, tol in ((1, 0.05), (2, 0.15)):
        cut = threshold * mean * math.log(10)
        assert abs(exponential_phi(cut, mean) - threshold) < 1e-12
        rate = sum(y >= cut for y in ys) / len(ys)
        assert abs(rate / 10 ** -threshold - 1) < tol


def test_logistic_approximation_of_akka():
    nd = NormalDist(100, 10)
    for y in (-2, -1, 0, 1, 2):
        exact = -math.log10(1 - nd.cdf(100 + 10 * y))
        assert abs(logistic_phi(100 + 10 * y, 100, 10) - exact) < 0.05
    # in the far tail the approximation gives a larger phi
    exact5 = -math.log10(0.5 * math.erfc(5 / math.sqrt(2)))
    assert logistic_phi(150, 100, 10) > exact5 + 0.5
    # the acceptable pause shifts the mean, the minimum std widens the curve
    assert logistic_phi(150, 100, 10, pause=50) == logistic_phi(100, 100, 10)
    assert logistic_phi(150, 100, 1, min_std=10) == logistic_phi(150, 100, 10)


def test_wrong_model_breaks_the_guarantee():
    rng = random.Random(4)
    ys = [rng.expovariate(1 / 100) for _ in range(100000)]
    assert mistake_rate(ys, 3) > 5 * 10 ** -3
