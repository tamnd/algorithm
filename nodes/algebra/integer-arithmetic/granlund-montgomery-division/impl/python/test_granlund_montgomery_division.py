# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/granlund-montgomery-division/. The authors are listed in prov/N5CE12.jsonl.

import random

import pytest

from granlund_montgomery_division import div_2by1, divide, precompute, reciprocal


def test_example_w8_d7():
    dv = precompute(7, 8)
    assert (dv.m, dv.s1, dv.s2) == (37, 1, 2)
    assert divide(200, dv) == (28, 4)


def test_exhaustive_w8():
    for d in range(1, 256):
        dv = precompute(d, 8)
        for n in range(256):
            assert divide(n, dv) == divmod(n, d)


def test_random_wide():
    rng = random.Random(1994)
    for w in (16, 32, 64, 128):
        for _ in range(250):
            d = rng.randint(1, (1 << w) - 1)
            if rng.random() < 0.3:
                d = (1 << rng.randint(0, w - 1)) + rng.randint(-1, 1)
                d = min(max(d, 1), (1 << w) - 1)
            dv = precompute(d, w)
            for n in (rng.getrandbits(w), (1 << w) - 1, 0, d, d - 1):
                assert divide(n, dv) == divmod(n, d)


def test_2by1_exhaustive_w6():
    w = 6
    for d in range(1 << (w - 1), 1 << w):
        v = reciprocal(d, w)
        for u1 in range(d):
            for u0 in range(1 << w):
                assert div_2by1(u1, u0, d, v, w) == divmod((u1 << w) + u0, d)


def test_2by1_example_w8():
    v = reciprocal(200, 8)
    assert v == 71
    assert div_2by1(150, 77, 200, v, 8) == divmod(150 * 256 + 77, 200)


def test_2by1_random():
    rng = random.Random(2011)
    for w in (8, 16, 32, 64):
        for _ in range(400):
            d = rng.randint(1 << (w - 1), (1 << w) - 1)
            v = reciprocal(d, w)
            u1, u0 = rng.randint(0, d - 1), rng.getrandbits(w)
            assert div_2by1(u1, u0, d, v, w) == divmod((u1 << w) + u0, d)
            assert div_2by1(d - 1, (1 << w) - 1, d, v, w) == divmod(((d - 1) << w) + (1 << w) - 1, d)


def test_errors():
    with pytest.raises(ValueError):
        precompute(0, 8)
    with pytest.raises(ValueError):
        precompute(256, 8)
    with pytest.raises(ValueError):
        reciprocal(100, 8)
    with pytest.raises(ValueError):
        div_2by1(200, 0, 200, 71, 8)
