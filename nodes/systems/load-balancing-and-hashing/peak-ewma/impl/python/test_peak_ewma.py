# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/peak-ewma/. The authors are listed in prov/MD9K0X.jsonl.

import heapq
import math
import random

import pytest

from peak_ewma import PENALTY, PeakEwma, decayed_peak, first_time_cheaper, trace


def test_trace_of_the_page() -> None:
    ev = [("obs", 0, 0.010, 0.0), ("obs", 0, 0.500, 1.0), ("read", 0, 0, 2.0),
          ("obs", 0, 0.010, 2.0), ("obs", 0, 0.010, 3.0), ("read", 0, 0, 8.0),
          ("obs", 0, 0.010, 30.0)]
    got = [round(c * 1000, 1) for c in trace(ev, 1)]
    assert got == [10.0, 500.0, 452.4, 452.4, 410.3, 248.9, 36.5]


def test_numbers_of_the_page() -> None:
    assert PENALTY == 2 ** 47 - 1
    assert round(PENALTY / 1e9 / 3600, 1) == 39.1
    assert round(first_time_cheaper(0.5, 0.02, 10.0), 1) == 32.2
    assert round(10 * math.log(2), 2) == 6.93
    pe = PeakEwma(2)
    pe.c = [0.4524, 0.020]
    pe.s = [5.0, 5.0]
    pe.p = [0, 3]
    assert round(pe.load(0, 5.0), 4) == 0.4524 and round(pe.load(1, 5.0), 4) == 0.08


def test_penalty_and_probe() -> None:
    pe = PeakEwma(2)
    assert pe.load(0, 1.0) == 0.0          # nothing pending, no sample: load 0
    pe.p[0] = 2
    assert pe.load(0, 1.0) == PENALTY + 2   # pending but no sample yet
    with pytest.raises(ValueError):
        PeakEwma(1).done(0, 0.0, 1.0)
    with pytest.raises(ValueError):
        PeakEwma(1, tau=0)


def test_bounds_against_decayed_peak() -> None:
    rng = random.Random(21)
    for _ in range(300):
        tau = rng.choice([1.0, 5.0, 10.0])
        pe = PeakEwma(1, tau)
        t, samples = 0.0, []
        for _ in range(30):
            t += rng.choice([0.0, rng.random() * 3])
            if rng.random() < 0.6:
                x = rng.random() * rng.choice([0.01, 0.5])
                pe.observe(0, x, t)
                samples.append((t, x))
            else:
                pe.load(0, t)
            low = decayed_peak(samples, t, tau)
            high = max([x for _, x in samples] + [0.0])
            assert low - 1e-12 <= pe.c[0] <= high + 1e-12
            if samples and samples[-1][0] == t and samples[-1][1] >= 0:
                assert pe.c[0] >= samples[-1][1] - 1e-12


def test_pure_decay_does_not_depend_on_reads() -> None:
    rng = random.Random(8)
    for _ in range(200):
        pe = PeakEwma(1, 10.0)
        pe.observe(0, 0.3, 0.0)
        t = 0.0
        for _ in range(rng.randint(0, 10)):
            t += rng.random()
            pe.load(0, t)
        end = t + rng.random()
        pe.load(0, end)
        assert math.isclose(pe.c[0], 0.3 * math.exp(-end / 10.0), rel_tol=1e-12)


def test_pick_matches_reference() -> None:
    rng = random.Random(13)
    for _ in range(500):
        n = rng.randint(1, 6)
        pe = PeakEwma(n, 10.0)
        pe.c = [rng.choice([0.0, rng.random()]) for _ in range(n)]
        pe.s = [rng.random() for _ in range(n)]
        pe.p = [rng.randint(0, 3) for _ in range(n)]
        t = 1.0 + rng.random()

        def ref_load(j):
            c = pe.c[j] * math.exp(-(t - pe.s[j]) / 10.0)
            return PENALTY + pe.p[j] if c == 0.0 and pe.p[j] else c * (pe.p[j] + 1)

        loads = [ref_load(j) for j in range(n)]
        seed = rng.random()
        g = random.Random(seed)
        if n == 1:
            want = 0
        else:
            i = g.randrange(n)
            k = g.randrange(n - 1)
            k += k >= i
            assert k != i
            want = k if loads[k] < loads[i] else i
        p_before = list(pe.p)
        assert pe.pick(t, random.Random(seed)) == want
        assert pe.p[want] == p_before[want] + 1


def test_slow_backend_gets_little_traffic() -> None:
    lat = [0.100, 0.010, 0.010, 0.010, 0.010]
    for seed in range(1, 6):
        rng = random.Random(seed)
        pe = PeakEwma(len(lat))
        ends, counts = [], [0] * len(lat)
        for r in range(4000):
            t = r * 0.002
            while ends and ends[0][0] <= t:
                te, j, t0 = heapq.heappop(ends)
                pe.done(j, t0, te)
            j = pe.pick(t, rng)
            counts[j] += 1
            heapq.heappush(ends, (t + lat[j], j, t))
        assert 1 <= counts[0] <= 2
        assert all(900 <= c <= 1100 for c in counts[1:])
