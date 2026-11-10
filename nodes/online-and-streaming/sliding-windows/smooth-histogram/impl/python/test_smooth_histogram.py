# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/smooth-histogram/. The authors are listed in prov/PBPEZG.jsonl.

import itertools
import math
import random
from collections import Counter
from fractions import Fraction

from smooth_histogram import ExactDistinct, ExactMax, ExactSum, SmoothHistogram


def exact_sum(items):
    return sum(items)


def exact_distinct(items):
    return len(set(items))


def exact_max(items):
    return max(items, default=0)


def check(values, window, beta, make, exact, largest, all_w=True):
    """Check the guarantee with alpha = beta, the case of the three functions here."""
    sh = SmoothHistogram(window, beta, make)
    bound = 2 * math.ceil(math.log(largest + 1) / beta) + 3
    for t in range(1, len(values) + 1):
        sh.update(values[t - 1])
        state = sh.state()
        xs = [x for x, _ in state]
        fs = [f for _, f in state]
        assert xs == sorted(set(xs)) and xs[-1] == t
        assert all(f == exact(values[x - 1:t]) for x, f in state)
        assert len(state) <= bound
        for i in range(len(state) - 2):
            assert fs[i + 2] < (1 - beta) * fs[i]
        if t > window:
            assert xs[0] <= t - window < xs[1]
        for w in range(1, window + 1) if all_w else (window,):
            true = exact(values[max(0, t - w):t])
            got = sh.query(w)
            assert (1 - beta) * true <= got <= true


def test_page_example():
    sh = SmoothHistogram(4, Fraction(1, 2), ExactSum)
    seen = {}
    for t, v in enumerate([3, 1, 2, 0, 3, 1, 1, 2], 1):
        sh.update(v)
        seen[t] = (sh.state(), sh.query())
    assert seen[4] == ([(1, 6), (2, 3), (3, 2), (4, 0)], 6)
    assert seen[5] == ([(1, 9), (3, 5), (5, 3)], 5)
    assert seen[7] == ([(3, 7), (5, 5), (6, 2), (7, 1)], 5)
    assert seen[8] == ([(3, 9), (5, 7), (6, 4), (8, 2)], 7)


def test_all_short_sum_streams():
    for values in itertools.product(range(3), repeat=6):
        for beta in (Fraction(1, 2), Fraction(1, 5)):
            check(list(values), 3, beta, ExactSum, exact_sum, 3 * 2)


def test_seeded_streams():
    rng = random.Random(7)
    for _ in range(40):
        window = rng.randint(1, 30)
        beta = Fraction(1, rng.randint(2, 12))
        n = rng.randint(1, 90)
        sums = [rng.randint(0, 9) if rng.random() < 0.6 else 0 for _ in range(n)]
        check(sums, window, beta, ExactSum, exact_sum, 9 * window, all_w=window <= 8)
        items = [rng.randint(0, rng.randint(1, 20)) for _ in range(n)]
        check(items, window, beta, ExactDistinct, exact_distinct, window, all_w=window <= 8)
        check(items, window, beta, ExactMax, exact_max, 20, all_w=window <= 8)


def test_number_of_instances_is_logarithmic():
    sh = SmoothHistogram(2000, Fraction(1, 4), ExactSum)
    rng = random.Random(3)
    most = 0
    for _ in range(4000):
        sh.update(rng.randint(0, 5))
        most = max(most, len(sh.starts))
    assert most <= 2 * math.ceil(math.log(5 * 2000 + 1) * 4) + 3
    assert most < 80


class ExactMaxFrequency:
    """F_infinity, the largest frequency, which is not smooth."""

    def __init__(self):
        self.counts = Counter()

    def update(self, item):
        self.counts[item] += 1

    def value(self):
        return max(self.counts.values(), default=0)


def test_largest_frequency_is_not_smooth():
    k = 20
    values = ["x"] * k + ["y"] * k + ["x"] * k
    window = 3 * k - 1
    sh = SmoothHistogram(window, Fraction(1, 10), ExactMaxFrequency)
    for v in values:
        sh.update(v)
    true = Counter(values[1:]).most_common(1)[0][1]
    assert true == 2 * k - 1
    assert sh.query() == k
    assert sh.query() < Fraction(6, 10) * true


def test_bad_arguments():
    for window, beta in ((0, Fraction(1, 2)), (3, 0), (3, 1)):
        try:
            SmoothHistogram(window, beta, ExactSum)
        except ValueError:
            pass
        else:
            raise AssertionError("bad arguments must be rejected")
