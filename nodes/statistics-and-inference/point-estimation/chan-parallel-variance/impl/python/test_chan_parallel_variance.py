# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chan-parallel-variance/. The authors are listed in prov/EJXH8E.jsonl.

import math
import random
from fractions import Fraction

from chan_parallel_variance import Summary, chan_parallel_variance, combine, summarize


def exact_summary(xs):
    """Oracle: the two-pass formula in exact arithmetic."""
    n = len(xs)
    m = sum(xs, Fraction(0)) / n
    return Summary(n, m, sum(((x - m) ** 2 for x in xs), Fraction(0)))


def welford(xs):
    """Welford's one-value update, written out independently."""
    k, m, s = 0, Fraction(0), Fraction(0)
    for x in xs:
        k += 1
        d = x - m
        m += d / k
        s += d * (x - m)
    return Summary(k, m, s)


def random_tree_merge(rng, parts):
    """Merge a list of summaries in a random order and a random tree shape."""
    parts = list(parts)
    while len(parts) > 1:
        i = rng.randrange(len(parts) - 1)
        a, b = parts[i], parts[i + 1]
        if rng.random() < 0.5:
            a, b = b, a
        parts[i:i + 2] = [combine(a, b)]
    return parts[0]


def test_running_example():
    a = exact_summary([Fraction(3), Fraction(7)])
    b = exact_summary([Fraction(7), Fraction(9), Fraction(14)])
    assert a == (2, 5, 8) and b == (3, 10, 26)
    assert combine(a, b) == (5, 8, 64)
    assert chan_parallel_variance([Fraction(v) for v in (3, 7, 7, 9, 14)]) == (8, 16, 64)


def test_split_and_pairwise_equal_two_pass():
    rng = random.Random(1983)
    for _ in range(600):
        n = rng.randint(2, 14)
        xs = [Fraction(rng.randint(-40, 40), rng.randint(1, 7)) for _ in range(n)]
        cut = rng.randint(1, n - 1)
        whole = exact_summary(xs)
        assert combine(exact_summary(xs[:cut]), exact_summary(xs[cut:])) == whole
        assert summarize(xs) == whole
        assert welford(xs) == whole
        m, v, s = chan_parallel_variance(xs)
        assert (m, s) == (whole.mean, whole.m2) and v == whole.m2 / (n - 1)


def test_any_tree_of_merges_gives_the_same_result():
    rng = random.Random(77)
    for _ in range(500):
        n = rng.randint(2, 12)
        xs = [Fraction(rng.randint(-20, 20)) for _ in range(n)]
        cuts = sorted(rng.sample(range(1, n), rng.randint(0, n - 1)))
        bounds = [0] + cuts + [n]
        parts = [exact_summary(xs[i:j]) for i, j in zip(bounds, bounds[1:])]
        assert random_tree_merge(rng, parts) == exact_summary(xs)


def test_associative_and_commutative_on_arbitrary_summaries():
    rng = random.Random(5)

    def rand_summary():
        return Summary(rng.randint(1, 9), Fraction(rng.randint(-30, 30), rng.randint(1, 5)),
                       Fraction(rng.randint(0, 50), rng.randint(1, 5)))

    for _ in range(500):
        a, b, c = rand_summary(), rand_summary(), rand_summary()
        assert combine(a, b) == combine(b, a)
        assert combine(combine(a, b), c) == combine(a, combine(b, c))


def test_welford_is_the_case_of_one_new_value():
    rng = random.Random(11)
    for _ in range(500):
        k = rng.randint(1, 20)
        a = Summary(k, Fraction(rng.randint(-50, 50), 3), Fraction(rng.randint(0, 99), 7))
        x = Fraction(rng.randint(-50, 50), 2)
        d = x - a.mean
        merged = combine(a, Summary(1, x, Fraction(0)))
        assert merged.mean == a.mean + d / (k + 1)
        assert merged.m2 == a.m2 + d * (x - merged.mean) == a.m2 + Fraction(k, k + 1) * d * d


def test_identity_and_short_input():
    a = Summary(3, Fraction(2), Fraction(5))
    empty = Summary(0, Fraction(0), Fraction(0))
    assert combine(a, empty) == a and combine(empty, a) == a
    try:
        chan_parallel_variance([1.0])
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")


def test_float_error_on_shifted_data():
    rng = random.Random(3)
    u = 2.0 ** -53
    for c in (0.0, 1e4, 1e6):
        for n in (2, 17, 1000):
            xs = [c + rng.gauss(0.0, 1.0) for _ in range(n)]
            whole = exact_summary([Fraction(x) for x in xs])
            _, v, _ = chan_parallel_variance(xs)
            kappa = math.sqrt(1 + n * float(whole.mean) ** 2 / float(whole.m2))
            rel = abs(Fraction(v) - whole.m2 / (n - 1)) / (whole.m2 / (n - 1))
            assert rel <= 50 * kappa * u * max(1.0, math.log2(n))
