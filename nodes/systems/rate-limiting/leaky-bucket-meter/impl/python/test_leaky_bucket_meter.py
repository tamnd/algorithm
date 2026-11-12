# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/leaky-bucket-meter/. The authors are listed in prov/JQZSX6.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from leaky_bucket_meter import LeakyBucketMeter, conforms, police


def token_bucket(arrivals, rate, depth):
    """Reference: a token bucket that starts full, with the tokens after each call."""
    x, last, out = depth, arrivals[0][0] if arrivals else 0, []
    for t, size in arrivals:
        x = min(depth, x + rate * (t - last))
        last = t
        ok = x >= size
        if ok:
            x -= size
        out.append((ok, x))
    return out


def test_page_example():
    arr = [(0, 1500), (0, 1500), (0, 500), (F(1, 2), 1000), (1, 1500), (F(3, 2), 1500), (2, 500), (4, 1500), (4, 1500), (4, 1500)]
    m = LeakyBucketMeter(1000, 3000, 0)
    got = [(m.allow(t, size), m.level) for t, size in arr]
    assert got == [(True, 1500), (True, 3000), (False, 3000), (False, 2500), (False, 2000), (True, 3000), (True, 3000), (True, 2500), (False, 2500), (False, 2500)]


def test_bad_input():
    with pytest.raises(ValueError):
        LeakyBucketMeter(1, 0)
    m = LeakyBucketMeter(1, 1, 3)
    with pytest.raises(ValueError):
        m.allow(2)


def test_mirror_of_token_bucket_random():
    """Same decisions as a token bucket, and level = depth - tokens after each call."""
    rng = random.Random(7)
    for _ in range(400):
        rate = F(rng.randint(1, 6), rng.randint(1, 4))
        depth = F(rng.randint(2, 12), rng.randint(1, 3))
        t = F(0)
        arr = []
        for _ in range(rng.randint(1, 40)):
            t += F(rng.randint(0, 6), rng.randint(1, 4))
            arr.append((t, F(rng.randint(1, 4), rng.randint(1, 2))))
        meter = LeakyBucketMeter(rate, depth, arr[0][0])
        for (t, size), (ok, x) in zip(arr, token_bucket(arr, rate, depth)):
            assert meter.allow(t, size) == ok
            assert meter.level == depth - x


def sequences(max_len, times, sizes):
    for n in range(max_len + 1):
        for ts in itertools.combinations_with_replacement(times, n):
            for ls in itertools.product(sizes, repeat=n):
                yield list(zip(ts, ls))


def test_exhaustive_sound_greedy_tight():
    """On small integer inputs: the output conforms, a packet passes iff it keeps the output conforming,
    and a conforming input passes whole."""
    for r, b in [(F(1, 2), 2), (1, 2), (1, 3), (F(3, 2), F(5, 2))]:
        for arr in sequences(4, range(5), (1, 2)):
            dec = police(arr, r, b)
            kept = []
            for a, d in zip(arr, dec):
                assert d == conforms(kept + [a], r, b)
                if d:
                    kept.append(a)
            assert conforms(kept, r, b)
            if conforms(arr, r, b):
                assert all(dec)
