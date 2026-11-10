# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-histogram/. The authors are listed in prov/PRB8V8.jsonl.

import itertools
import random
from fractions import Fraction

from exponential_histogram import ExponentialHistogram


def check_stream(values, window, k, max_value, all_w=False):
    eh = ExponentialHistogram(window, k, max_value)
    cap = (k + 1) // 2
    units = 0
    for t, v in enumerate(values, 1):
        eh.update(v)
        units += v
        true = sum(values[max(0, t - window):t])
        est = eh.query()
        assert est == true or 2 * cap * abs(est - true) < true
        assert k * abs(est - true) <= true
        sizes = [len(lev) for lev in eh.levels]
        for j, n in enumerate(sizes):
            assert (cap <= n <= cap + 1) if j < len(sizes) - 1 else (1 <= n <= cap + 1)
        assert all(ts > t - window for ts, _ in eh.buckets())
        assert len(eh.buckets()) <= eh.bucket_bound()
        assert eh.merges <= units
        if all_w:
            for w in range(1, window + 1):
                tw = sum(values[max(0, t - w):t])
                ew = eh.query(w)
                assert ew == tw or 2 * cap * abs(ew - tw) < tw


def test_page_example():
    eh = ExponentialHistogram(4, 2, 3)
    values = [2, 0, 3, 1, 2, 0, 3]
    seen = {}
    for t, v in enumerate(values, 1):
        eh.update(v)
        seen[t] = (eh.buckets(), eh.query())
    assert seen[3] == ([(3, 1), (3, 2), (1, 2)], Fraction(9, 2))
    assert seen[5] == ([(5, 1), (5, 1), (4, 2), (3, 2)], Fraction(11, 2))
    assert seen[7] == ([(7, 1), (7, 2), (5, 4)], Fraction(11, 2))


def test_all_short_streams_of_small_integers():
    for values in itertools.product(range(4), repeat=5):
        for k in (1, 2, 3):
            check_stream(list(values), 3, k, 3, all_w=(k == 2))


def test_seeded_streams_of_small_integers():
    rng = random.Random(11)
    for _ in range(80):
        window = rng.randint(1, 40)
        k = rng.randint(1, 10)
        max_value = rng.randint(1, 9)
        values = [rng.randint(0, max_value) if rng.random() < 0.7 else 0 for _ in range(rng.randint(1, 120))]
        check_stream(values, window, k, max_value, all_w=(window <= 10))


def test_adversarial_streams():
    for window in (1, 3, 8, 21):
        for k in (1, 2, 6):
            for max_value in (1, 5):
                n = 3 * window + 4
                check_stream([max_value] * n, window, k, max_value)
                check_stream([max_value if i % window == 0 else 0 for i in range(n)], window, k, max_value)
                check_stream(([max_value] * window + [0] * window) * 2, window, k, max_value)


def test_value_zero_bound_and_range():
    eh = ExponentialHistogram(5, 3, 0)
    for _ in range(10):
        eh.update(0)
    assert eh.query() == 0 and eh.bucket_bound() == 0
    try:
        ExponentialHistogram(5, 3, 2).update(3)
    except ValueError:
        pass
    else:
        raise AssertionError("value above R must be rejected")
