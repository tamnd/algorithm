# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leaky-bucket-queue/. The authors are listed in prov/QSRTMA.jsonl.

import random
from fractions import Fraction as F

import pytest

from leaky_bucket_queue import LeakyBucketQueue, departures_by_recursion, shape


def meter(arrivals, rate, size):
    """Reference leaky bucket meter (empty at the start); returns (decision, level before) per packet."""
    level, last, out = 0, arrivals[0][0] if arrivals else 0, []
    for t, length in arrivals:
        level = max(0, level - rate * (t - last))
        last = t
        before = level
        ok = level + length <= size
        if ok:
            level += length
        out.append((ok, before))
    return out


def random_arrivals(rng, count, sizes=(1,)):
    t, out = F(0), []
    for _ in range(count):
        t += F(rng.randint(0, 5), rng.randint(1, 4))
        out.append((t, rng.choice(sizes)))
    return out


def test_page_example():
    arr = [(0, 1), (0, 1), (0, 1), (0, 1), (F(1, 2), 1), (F(3, 2), 1), (2, 1), (2, 1), (F(5, 2), 1), (6, 1)]
    assert shape(arr, 1, 3) == [1, 2, 3, None, None, 4, 5, None, None, 7]


def test_bad_input():
    with pytest.raises(ValueError):
        LeakyBucketQueue(1, 0)
    q = LeakyBucketQueue(1, 2, 5)
    with pytest.raises(ValueError):
        q.arrive(4, "p")


def test_unit_packets_match_meter_and_recursion():
    """Unit packets: accepted iff a meter with b = K passes; d_k = max(t_k, d_prev) + 1/r; delay = (X + 1)/r <= K/r."""
    rng = random.Random(2)
    for _ in range(500):
        rate = F(rng.randint(1, 5), rng.randint(1, 3))
        cap = rng.randint(1, 6)
        arr = random_arrivals(rng, rng.randint(1, 40))
        deps = shape(arr, rate, cap)
        assert deps == departures_by_recursion(arr, rate, cap)
        for (t, _), d, (ok, level) in zip(arr, deps, meter(arr, rate, cap)):
            assert (d is not None) == ok
            if d is not None:
                assert d - t == (level + 1) / rate
                assert d - t <= cap / rate


def test_output_is_smooth_and_fifo():
    """Any sizes: FIFO order, departures spaced by at least L/r, and the server never idles while a packet waits."""
    rng = random.Random(4)
    for _ in range(400):
        rate = F(rng.randint(1, 5), rng.randint(1, 3))
        cap = rng.randint(1, 6)
        arr = random_arrivals(rng, rng.randint(1, 40), sizes=(1, 2, 3))
        deps = shape(arr, rate, cap)
        prev = None
        for (t, size), d in zip(arr, deps):
            if d is None:
                continue
            start = t if prev is None else max(t, prev)
            assert d == start + F(size) / rate
            prev = d
        done = sorted((d, size) for (t, size), d in zip(arr, deps) if d is not None)
        # bytes sent in any closed interval [d_i, d_j] are at most r (d_j - d_i) + size of the first
        for i in range(len(done)):
            total = 0
            for j in range(i, len(done)):
                total += done[j][1]
                assert total - done[i][1] <= rate * (done[j][0] - done[i][0])
