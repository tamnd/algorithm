# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cusum/. The authors are listed in prov/ST2SET.jsonl.
import math
import random
from fractions import Fraction

import pytest

from cusum import (
    brute_force_statistic,
    cusum,
    cusum_scores,
    gaussian_log_density,
    gaussian_mean_shift_scores,
    two_sided_gaussian,
)

EXAMPLE = [0.3, -0.6, 0.2, 1.4, 0.9, 1.6]


def test_worked_example():
    zs = gaussian_mean_shift_scores(EXAMPLE, 0.0, 1.0, 1.0)
    t, k, path = cusum_scores(zs, 2.0)
    assert (t, k) == (6, 4)
    assert all(abs(a - b) < 1e-12 for a, b in zip(path, [0, 0, 0, 0.9, 1.3, 2.4]))
    assert cusum(EXAMPLE, gaussian_log_density(0.0, 1.0), gaussian_log_density(1.0, 1.0), 2.0) == (6, 4)


def test_no_alarm_and_empty():
    assert cusum_scores([], 1.0) == (None, None, [])
    t, k, path = cusum_scores([-1, -2, 0, 1], 5)
    assert (t, k) == (None, None) and path == [0, 0, 0, 1]
    with pytest.raises(ValueError):
        cusum_scores([1.0], 0.0)


def test_recursion_equals_maximum_over_change_times_exact():
    rng = random.Random(1954)
    for _ in range(600):
        n = rng.randint(1, 25)
        zs = [Fraction(rng.randint(-6, 6), rng.randint(1, 4)) for _ in range(n)]
        _, _, path = cusum_scores(zs, Fraction(10 ** 9))
        s, k = 0, 1
        for t in range(1, n + 1):
            best, arg = brute_force_statistic(zs, t)
            assert path[t - 1] == best
            s = s + zs[t - 1]
            if s <= 0:
                s, k = 0, t + 1
            assert k == arg


def test_alarm_and_estimate_against_brute_force():
    rng = random.Random(42)
    for _ in range(500):
        n = rng.randint(1, 30)
        zs = [rng.randint(-3, 3) for _ in range(n)]
        h = rng.randint(1, 8)
        t, k, _ = cusum_scores(zs, h)
        want_t = next((u for u in range(1, n + 1) if brute_force_statistic(zs, u)[0] >= h), None)
        assert t == want_t
        if t is not None:
            assert k == brute_force_statistic(zs, t)[1]


def test_false_alarm_rate_above_lorden_bound():
    # Lorden: E_infinity[T] >= e^h for the one-sided CUSUM with the true log likelihood ratio.
    rng = random.Random(9)
    for h in (2.0, 3.0):
        reps = 1500
        total = 0
        for _ in range(reps):
            s, t = 0.0, 0
            while s < h:
                t += 1
                s = max(0.0, s + rng.gauss(0.0, 1.0) - 0.5)
            total += t
        assert total / reps > math.exp(h)


def test_detection_delay_grows_like_h_over_kl():
    rng = random.Random(10)
    delays = []
    for h in (4.0, 8.0):
        reps = 1000
        total = 0
        for _ in range(reps):
            s, t = 0.0, 0
            while s < h:
                t += 1
                s = max(0.0, s + rng.gauss(1.0, 1.0) - 0.5)
            total += t
        delays.append(total / reps)
        # The KL divergence is 1/2, so the delay is h / (1/2) plus a bounded overshoot term.
        assert 2 * h < delays[-1] < 2 * h + 3
    assert delays[1] > delays[0]


def test_two_sided_detects_both_directions():
    rng = random.Random(4)
    up = [rng.gauss(0, 1) for _ in range(50)] + [rng.gauss(2, 1) for _ in range(50)]
    down = [rng.gauss(0, 1) for _ in range(50)] + [rng.gauss(-2, 1) for _ in range(50)]
    for xs in (up, down):
        t = two_sided_gaussian(xs, 0.0, 2.0, 1.0, 5.0)
        assert t is not None and 50 < t <= 60
