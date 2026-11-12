# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sliding-window-counter/. The authors are listed in prov/5CM6Z2.jsonl.

import random
from fractions import Fraction as F
from math import floor

import pytest

from sliding_window_counter import SlidingWindowCounter, max_in_window, run


def random_times(rng, count, step_num, step_den):
    t, out = F(0), []
    for _ in range(count):
        t += F(rng.randint(0, step_num), rng.randint(1, step_den))
        out.append(t)
    return out


def log_run(times, n, w):
    """Exact sliding window log, for comparison."""
    kept, out = [], []
    for t in times:
        ok = sum(1 for s in kept if s > t - w) < n
        out.append(ok)
        if ok:
            kept.append(t)
    return out


def test_page_example():
    times = [F(x) for x in ["8", "9", "9.5", "10", "10.5", "11", "12", "15", "18", "19", "21", "25", "28.5"]]
    assert run(times, 3, 10) == [True, True, True, False, False, False, False, True, True, False, True, True, False]
    s = SlidingWindowCounter(3, 10)
    for t in times[:3]:
        s.allow(t)
    assert s.estimate(F("10.5")) == F("2.85")


def test_bad_input():
    with pytest.raises(ValueError):
        SlidingWindowCounter(1, 0)
    s = SlidingWindowCounter(2, 10)
    s.allow(35)
    with pytest.raises(ValueError):
        s.allow(12)


def test_bounds_on_random_input():
    """At most n per aligned window, and at most 2n - 1 in any window (s - w, s]."""
    rng = random.Random(21)
    for _ in range(400):
        n, w = rng.randint(1, 6), F(rng.randint(1, 12), rng.randint(1, 3))
        times = random_times(rng, rng.randint(1, 80), 3, 4)
        kept = [t for t, ok in zip(times, run(times, n, w)) if ok]
        per = {}
        for t in kept:
            per[floor(t / w)] = per.get(floor(t / w), 0) + 1
        assert max(per.values(), default=0) <= n
        assert max_in_window(kept, w) <= 2 * n - 1


def test_worst_case_reaches_2n_minus_1():
    """n requests at w - w / (2n), then n requests at 2w - w / n: 2n - 1 pass, all in one window."""
    w = 60
    for n in range(1, 12):
        times = [w - F(w, 2 * n)] * n + [2 * w - F(w, n)] * n
        kept = [t for t, ok in zip(times, run(times, n, w)) if ok]
        assert len(kept) == 2 * n - 1 and max_in_window(kept, w) == 2 * n - 1
    times = [F(57)] * 10 + [F(114)] * 10
    assert run(times, 10, 60) == [True] * 19 + [False]


def test_under_admits_where_log_admits():
    times = [F(0)] * 10 + [F(61)]
    assert run(times, 10, 60)[-1] is False
    assert log_run(times, 10, 60)[-1] is True


def random_load(seed, per_window, n, w, count):
    """Gaps uniform in (0, 2 w / per_window], so about per_window requests arrive per window."""
    rng = random.Random(seed)
    t, times = F(0), []
    for _ in range(count):
        t += F(rng.randint(1, 1000), 1000) * F(2 * w, per_window)
        times.append(t)
    return times


def test_random_load_compared_with_log():
    """Seeded measurement: below the limit few decisions differ; above it, the totals stay close."""
    n, w = 100, 60
    times = random_load(5, 90, n, w, 10000)
    a, b = run(times, n, w), log_run_fast(times, n, w)
    assert sum(x != y for x, y in zip(a, b)) / len(times) < F(1, 50)
    for per_window in (110, 150):
        times = random_load(5, per_window, n, w, 10000)
        a, b = run(times, n, w), log_run_fast(times, n, w)
        assert abs(sum(a) - sum(b)) / sum(b) < F(1, 50)


def log_run_fast(times, n, w):
    from collections import deque

    q, out = deque(), []
    for t in times:
        while q and q[0] <= t - w:
            q.popleft()
        ok = len(q) < n
        out.append(ok)
        if ok:
            q.append(t)
    return out
