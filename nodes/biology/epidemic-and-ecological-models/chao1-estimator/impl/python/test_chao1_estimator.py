# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chao1-estimator/. The authors are listed in prov/A0Z4WE.jsonl.
"""Tests of the Chao1 estimates.

The oracles are run-length counts of a sorted sample, exact enumeration of
all samples of a small community with Fraction, the exact moments of f1, and
a simulation with random.Random and a fixed seed.
"""

import itertools
import random
from fractions import Fraction

from biostoch import check_mean, mean_var
from chao1_estimator import (
    chao1,
    chao1_bias_corrected,
    chao1_classic,
    chao1_variance,
    expected_frequency,
)


def runs(sample):
    """Counts per species by sorting the labels: an oracle for line L1."""
    out = []
    for _, group in itertools.groupby(sorted(sample)):
        out.append(len(list(group)))
    return out


def test_check_values():
    assert chao1_classic(20, 6, 3) == 26
    assert chao1_bias_corrected(20, 6, 3) == Fraction(95, 4)
    assert chao1_variance(6, 3) == 42


def test_page_example():
    sample = list("AAAAABBBCCDDEFGH")
    res = chao1(sample)
    assert (res.n, res.s_obs, res.f1, res.f2) == (16, 8, 4, 2)
    assert res.classic == 12
    assert res.bias_corrected == 10
    assert res.variance == 28
    assert chao1_classic(8, 4, 2, n=16) == Fraction(47, 4)


def test_edge_cases():
    empty = chao1([])
    assert (empty.n, empty.s_obs, empty.classic, empty.bias_corrected) == (0, 0, None, 0)
    one = chao1(["x"])
    assert one.classic is None and one.bias_corrected == 1
    no_doubletons = chao1(list("abcd"))
    assert no_doubletons.classic is None and no_doubletons.variance is None
    assert no_doubletons.bias_corrected == 4 + 6
    all_common = chao1(list("aabbccc"))
    assert all_common.classic == 3 and all_common.bias_corrected == 3


def test_counts_against_sorting():
    rng = random.Random(21)
    for _ in range(500):
        k = rng.randint(1, 12)
        sample = [rng.randrange(k) for _ in range(rng.randint(0, 40))]
        res = chao1(sample)
        c = runs(sample)
        assert res.n == len(sample)
        assert res.s_obs == len(c)
        assert res.f1 == c.count(1) and res.f2 == c.count(2)
        assert res.bias_corrected >= res.s_obs
        if res.classic is not None:
            assert res.classic >= res.bias_corrected >= res.s_obs


def test_expected_frequency_by_enumeration():
    p = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)]
    n = 4
    exact = [Fraction(0)] * (n + 1)
    for seq in itertools.product(range(3), repeat=n):
        prob = Fraction(1)
        for i in seq:
            prob *= p[i]
        c = [seq.count(i) for i in range(3)]
        for k in range(n + 1):
            exact[k] += prob * c.count(k)
    for k in range(n + 1):
        assert expected_frequency(p, n, k) == exact[k]


def test_lower_bound_inequality():
    rng = random.Random(22)
    for _ in range(300):
        # Two or more species, so that E[f2] > 0.
        w = [rng.randint(1, 9) for _ in range(rng.randint(2, 6))]
        p = [Fraction(x, sum(w)) for x in w]
        n = rng.randint(2, 15)
        e0, e1, e2 = (expected_frequency(p, n, k) for k in range(3))
        bound = Fraction(n - 1, n) * e1 * e1 / (2 * e2)
        assert e0 >= bound
        if len(set(p)) == 1:
            assert e0 == bound
        else:
            assert e0 > bound


def test_simulated_singletons():
    s, n = 30, 100
    w = [1.0 / (i + 1) for i in range(s)]
    p = [x / sum(w) for x in w]
    mean_f1 = sum(n * q * (1 - q) ** (n - 1) for q in p)
    second = mean_f1
    for i in range(s):
        for j in range(s):
            if i != j:
                second += n * (n - 1) * p[i] * p[j] * (1 - p[i] - p[j]) ** (n - 2)
    var_f1 = second - mean_f1 ** 2
    rng = random.Random(23)
    f1s = []
    for _ in range(2000):
        f1s.append(chao1(rng.choices(range(s), weights=p, k=n)).f1)
    m, _ = mean_var(f1s)
    assert check_mean(m, mean_f1, var_f1, len(f1s))
