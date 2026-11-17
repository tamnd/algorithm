# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/learned-index/. The authors are listed in prov/935TPJ.jsonl.

import random
from fractions import Fraction

import pytest

from learned_index import RMI, fit_line

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]


def test_example():
    r = RMI(PRIMES, 4)
    assert r.root == (Fraction(6328, 22413), Fraction(5804, 7471))
    assert [r.route(k) for k in PRIMES] == [0] * 5 + [1] * 4 + [2] * 3 + [3] * 4
    assert r.models[2] == (Fraction(3, 13), Fraction(33, 13))
    assert r.err == [(0, 1)] * 4
    assert r.window(37) == (11, 12) and r.lookup(37) == 11
    assert r.window(30) == (9, 10) and r.lookup(30) is None
    assert r.lookup(4) is None and r.lookup(0) is None and r.lookup(60) is None


def test_fit_line_is_exact_least_squares():
    rng = random.Random(8)
    for _ in range(50):
        n = rng.randint(2, 30)
        xs = [rng.randint(-100, 100) for _ in range(n)]
        ys = [rng.randint(-100, 100) for _ in range(n)]
        a, b = fit_line(xs, ys)
        res = [y - a * x - b for x, y in zip(xs, ys)]
        assert sum(res) == 0
        if len(set(xs)) > 1:
            assert sum(x * e for x, e in zip(xs, res)) == 0
        else:
            assert a == 0
    assert fit_line([5], [7]) == (0, 7)


def check_all(keys, m):
    r = RMI(keys, m)
    for i, k in enumerate(keys):
        lo, hi = r.window(k)
        assert lo <= i <= hi                         # the key is inside its stored window
        assert r.lookup(k) == i
    present = set(keys)
    for q in range((keys[0] if keys else 0) - 3, (keys[-1] if keys else 0) + 4):
        if q not in present:
            assert r.lookup(q) is None
    # the stored bounds are the extreme errors of each model's own keys
    for j, line in enumerate(r.models):
        own = [i for i, k in enumerate(keys) if r.route(k) == j]
        if line is None:
            assert own == []
            continue
        errs = [i - r._predict(line, keys[i]) for i in own]
        assert r.err[j] == (min(errs), max(errs))
    return r


def test_random_key_sets():
    rng = random.Random(2018)
    for _ in range(200):
        n = rng.randint(0, 60)
        keys = sorted(rng.sample(range(-300, 300), n))
        if rng.random() < 0.3 and n:
            keys = sorted({int(1.3 ** rng.randint(0, 25)) for _ in range(n)})
        check_all(keys, rng.randint(1, 12))


def test_small_and_invalid():
    assert RMI([], 3).lookup(5) is None
    r = check_all([42], 3)
    assert r.lookup(42) == 0
    check_all([1, 2], 5)
    with pytest.raises(ValueError):
        RMI([1, 1, 2], 2)
    with pytest.raises(ValueError):
        RMI([3, 2], 2)
    with pytest.raises(ValueError):
        RMI([1, 2], 0)


def test_larger_uniform_windows():
    rng = random.Random(4)
    keys = sorted(rng.sample(range(10 ** 7), 10000))
    r = RMI(keys, 100)
    assert r.max_window() == 23
    for i in range(0, 10000, 7):
        assert r.lookup(keys[i]) == i
    for q in rng.sample(range(10 ** 7), 300):
        assert (r.lookup(q) is not None) == (q in set(keys))
