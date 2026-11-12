# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fixed-window-counter/. The authors are listed in prov/WERYMV.jsonl.

import random
from fractions import Fraction as F
from math import ceil, floor

import pytest

from fixed_window_counter import FixedWindowCounter, max_in_window, run


def random_times(rng, count, step_num, step_den):
    t, out = F(0), []
    for _ in range(count):
        t += F(rng.randint(0, step_num), rng.randint(1, step_den))
        out.append(t)
    return out


def test_page_example():
    times = [F(x) for x in ["8", "9", "9.5", "10", "10.5", "11", "12", "15", "18", "19", "21", "25", "28.5"]]
    assert run(times, 3, 10) == [True] * 6 + [False] * 4 + [True] * 3
    kept = [t for t, ok in zip(times, run(times, 3, 10)) if ok]
    assert max_in_window(kept, 10) == 6  # [8, 18) holds 6 = 2n


def test_bad_input():
    with pytest.raises(ValueError):
        FixedWindowCounter(0, 1)
    f = FixedWindowCounter(1, 10)
    f.allow(25)
    with pytest.raises(ValueError):
        f.allow(3)


def test_greedy_per_aligned_window():
    """A request passes iff fewer than n requests passed in its aligned window."""
    rng = random.Random(8)
    for _ in range(400):
        n, w = rng.randint(1, 5), F(rng.randint(1, 12), rng.randint(1, 3))
        times = random_times(rng, rng.randint(1, 60), 4, 3)
        seen = {}
        for t, ok in zip(times, run(times, n, w)):
            k = floor(t / w)
            assert ok == (seen.get(k, 0) < n)
            seen[k] = seen.get(k, 0) + ok


def test_interval_bound_and_tightness():
    """Any half-open interval of length tau holds at most n (ceil(tau / w) + 1) passed requests,
    at most (n / w) tau + 2n, and 2n is reached for tau = w."""
    rng = random.Random(6)
    for _ in range(300):
        n, w = rng.randint(1, 4), rng.randint(2, 10)
        times = random_times(rng, rng.randint(1, 50), 3, 2)
        kept = [t for t, ok in zip(times, run(times, n, w)) if ok]
        for tau in (F(1, 2), 1, w, F(3, 2) * w, 2 * w, 3 * w + 1):
            m = max_in_window(kept, tau)
            assert m <= n * (ceil(tau / w) + 1)
            assert m <= F(n, w) * tau + 2 * n
    for n in range(1, 6):
        w = 10
        times = [F(w) - F(1, 10)] * n + [F(w)] * n
        kept = [t for t, ok in zip(times, run(times, n, w)) if ok]
        assert len(kept) == 2 * n and max_in_window(kept, w) == 2 * n
