# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gcra/. The authors are listed in prov/5WH9D0.jsonl.

import copy
import random
from fractions import Fraction as F

import pytest

from gcra import GCRA, GCRALeakyBucket, gcra


def token_bucket(arrivals, rate, depth, start):
    """Reference token bucket, full at `start`, over (time, size) pairs."""
    x, last, out = depth, start, []
    for t, size in arrivals:
        x = min(depth, x + rate * (t - last))
        last = t
        ok = x >= size
        if ok:
            x -= size
        out.append(ok)
    return out


def random_times(rng, count, step_num, step_den):
    t, out = F(0), []
    for _ in range(count):
        t += F(rng.randint(0, step_num), rng.randint(1, step_den))
        out.append(t)
    return out


def test_le_boudec_table():
    # Le Boudec and Thiran, Table 1.1, first example, GCRA(10, 2), then four more cells.
    times = [0, 10, 18, 28, 38, 48, 57, 60, 61]
    g = GCRA(10, 2, 0)
    tats = []
    for t in times:
        tats.append(g.tat)
        g.allow(t)
    assert tats == [0, 10, 20, 30, 40, 50, 60, 60, 70]
    assert gcra(times, 10, 2, 0) == [True] * 6 + [False, True, False]


def test_bad_input():
    with pytest.raises(ValueError):
        GCRA(0, 1)
    with pytest.raises(ValueError):
        GCRA(1, -1)
    g = GCRA(1, 1, 5)
    with pytest.raises(ValueError):
        g.allow(4)


def test_two_forms_agree():
    rng = random.Random(11)
    for _ in range(500):
        T = F(rng.randint(1, 8), rng.randint(1, 3))
        tau = F(rng.randint(0, 20), rng.randint(1, 3))
        times = random_times(rng, rng.randint(1, 50), 6, 4)
        a, b = GCRA(T, tau, times[0]), GCRALeakyBucket(T, tau, times[0])
        for t in times:
            assert a.allow(t) == b.allow(t)
            # the invariant X + lct = tat holds after every cell
            assert b.X + b.lct == a.tat


def test_equals_token_bucket():
    """GCRA(T, tau) on unit cells = token bucket with r = 1/T and b = 1 + tau/T (Le Boudec Corollary 1.2.1)."""
    rng = random.Random(5)
    for _ in range(500):
        T = F(rng.randint(1, 8), rng.randint(1, 3))
        tau = F(rng.randint(0, 20), rng.randint(1, 3))
        times = random_times(rng, rng.randint(1, 50), 6, 4)
        want = token_bucket([(t, 1) for t in times], 1 / T, 1 + tau / T, times[0])
        assert gcra(times, T, tau) == want


def test_allow_n_equals_token_bucket():
    rng = random.Random(9)
    for _ in range(400):
        T = F(rng.randint(1, 6), rng.randint(1, 3))
        tau = F(rng.randint(0, 30), rng.randint(1, 3))
        times = random_times(rng, rng.randint(1, 40), 8, 3)
        sizes = [rng.randint(1, 4) for _ in times]
        g = GCRA(T, tau, times[0])
        got = [g.allow_n(t, n) for t, n in zip(times, sizes)]
        assert got == token_bucket(list(zip(times, sizes)), 1 / T, 1 + tau / T, times[0])


def test_retry_at():
    rng = random.Random(3)
    for _ in range(300):
        T = F(rng.randint(1, 6), rng.randint(1, 3))
        tau = F(rng.randint(0, 30), rng.randint(1, 3))
        g = GCRA(T, tau, 0)
        for t in random_times(rng, rng.randint(0, 20), 4, 3):
            g.allow(t)
        for n in range(1, 4):
            if n * T > tau + T:
                continue  # can never pass
            s = max(g.last, g.retry_at(n))
            assert copy.deepcopy(g).allow_n(s, n)
            eps = F(1, 1000)
            if g.retry_at(n) - eps >= g.last:
                assert not copy.deepcopy(g).allow_n(g.retry_at(n) - eps, n)


def test_stair_bound_and_window_bound():
    """Conforming cells satisfy t_(m+k) >= t_m + k T - tau, so any closed window of length L holds at most L/T + 1 + tau/T cells."""
    rng = random.Random(1)
    for _ in range(300):
        T = rng.randint(1, 6)
        tau = rng.randint(0, 15)
        times = sorted(rng.randint(0, 60) for _ in range(rng.randint(1, 40)))
        kept = [t for t, ok in zip(times, gcra(times, T, tau)) if ok]
        for i in range(len(kept)):
            for j in range(i, len(kept)):
                assert kept[j] >= kept[i] + (j - i) * T - tau
                assert j - i + 1 <= F(kept[j] - kept[i], T) + 1 + F(tau, T)
