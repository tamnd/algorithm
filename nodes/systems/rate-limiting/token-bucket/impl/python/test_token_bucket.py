# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/token-bucket/. The authors are listed in prov/PSJD1J.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from token_bucket import TokenBucket, conforms, police


def test_page_example():
    times = [0, 0, 0, 0, 1, 2, 3, 4, 5, 9, 9, 9, 9]
    got = police([(t, 1) for t in times], F(1, 2), 3)
    assert got == [True, True, True, False, False, True, False, True, False, True, True, False, False]


def test_lazy_state():
    b = TokenBucket(F(1, 2), 3, 0)
    for _ in range(3):
        assert b.allow(0)
    assert b.tokens == 0
    assert not b.allow(1)
    assert b.tokens == F(1, 2)
    assert b.allow(100)
    assert b.tokens == 2  # capped at 3 before the take


def test_bad_input():
    with pytest.raises(ValueError):
        TokenBucket(0, 1)
    b = TokenBucket(1, 1, 5)
    with pytest.raises(ValueError):
        b.allow(4)


def sequences(max_len, times, sizes):
    for n in range(max_len + 1):
        for ts in itertools.combinations_with_replacement(times, n):
            for ls in itertools.product(sizes, repeat=n):
                yield list(zip(ts, ls))


PARAMS = [(F(1, 2), 2), (F(1, 2), 3), (1, 2), (1, 3), (F(3, 2), 2), (F(3, 2), F(5, 2))]


def test_exhaustive_soundness_and_tightness():
    """On every small integer time line: the output conforms, and a conforming input passes whole."""
    count = 0
    for r, b in PARAMS:
        for arr in sequences(4, range(5), (1, 2)):
            dec = police(arr, r, b)
            out = [a for a, d in zip(arr, dec) if d]
            assert conforms(out, r, b)
            if conforms(arr, r, b):
                assert all(dec)
            count += 1
    assert count > 5000


def test_exhaustive_greedy():
    """Each packet passes if and only if the passed packets with it still conform."""
    for r, b in PARAMS:
        for arr in sequences(4, range(5), (1, 2)):
            dec = police(arr, r, b)
            out = []
            for a, d in zip(arr, dec):
                assert d == conforms(out + [a], r, b)
                if d:
                    out.append(a)


def test_random_long_traces():
    rng = random.Random(7)
    for _ in range(200):
        r = F(rng.randint(1, 6), rng.randint(1, 4))
        b = rng.randint(2, 6)
        t = F(0)
        arr = []
        for _ in range(rng.randint(1, 40)):
            t += F(rng.randint(0, 6), rng.randint(1, 3))
            arr.append((t, rng.randint(1, 2)))
        dec = police(arr, r, b)
        out = [a for a, d in zip(arr, dec) if d]
        assert conforms(out, r, b)
        # the burst bound on every closed interval of length tau
        for i in range(len(out)):
            tot = 0
            for j in range(i, len(out)):
                tot += out[j][1]
                assert tot <= r * (out[j][0] - out[i][0]) + b
