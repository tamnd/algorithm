# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/exponential-mechanism/. The authors are listed in prov/T51N2F.jsonl.

import itertools
import math
import random

import pytest

import dpkit
from exponential_mechanism import exponential_mechanism, exponential_pmf, utility_threshold

UNIVERSE = (0, 1, 2)
CANDIDATES = (0, 1, 2)


def count(x, r):
    """Utility of candidate r: the number of records equal to r. Sensitivity 1."""
    return sum(1 for v in x if v == r)


def all_datasets(max_n):
    for n in range(max_n + 1):
        for x in itertools.combinations_with_replacement(UNIVERSE, n):
            yield x


def worst_loss(mech, pairs):
    best = 0.0
    for x, y in pairs:
        p, q = mech(x), mech(y)
        best = max(best, dpkit.max_privacy_loss(p, q), dpkit.max_privacy_loss(q, p))
    return best


ADD_REMOVE = [(x, y) for x in all_datasets(4) for y in dpkit.neighbors_add_remove(x, UNIVERSE)]
REPLACE = [(x, y) for x in all_datasets(4) for y in dpkit.neighbors_replace(x, UNIVERSE)]


def oracle_pmf(x, eps, c):
    """Direct normalization without the max shift."""
    w = {r: math.exp(eps * count(x, r) / c) for r in CANDIDATES}
    total = sum(w.values())
    return {r: v / total for r, v in w.items()}


def test_pmf_matches_direct_normalization():
    rng = random.Random(12)
    for _ in range(500):
        n = rng.randint(0, 8)
        x = tuple(rng.choice(UNIVERSE) for _ in range(n))
        eps = rng.uniform(0.05, 3.0)
        for monotone, c in ((False, 2.0), (True, 1.0)):
            got = exponential_pmf(x, CANDIDATES, count, 1.0, eps, monotone)
            want = oracle_pmf(x, eps, c)
            for r in CANDIDATES:
                assert abs(got[r] - want[r]) < 1e-12


def test_general_version_is_epsilon_dp_under_both_relations():
    eps = 1.0
    mech = lambda x: exponential_pmf(x, CANDIDATES, count, 1.0, eps)
    assert dpkit.is_pure_dp(mech, REPLACE, eps)
    assert dpkit.is_pure_dp(mech, ADD_REMOVE, eps)
    # Counts are monotone under add/remove, so the factor 2 wastes half the budget there.
    assert worst_loss(mech, ADD_REMOVE) <= eps / 2 + 1e-12


def test_monotone_version_is_epsilon_dp_under_add_remove():
    eps = 1.0
    mech = lambda x: exponential_pmf(x, CANDIDATES, count, 1.0, eps, monotone=True)
    assert dpkit.is_pure_dp(mech, ADD_REMOVE, eps)
    assert worst_loss(mech, ADD_REMOVE) > 0.9 * eps


def test_monotone_flag_breaks_under_replace():
    # Under replace one count rises and another falls, so the utility is not monotone.
    eps = 1.0
    mech = lambda x: exponential_pmf(x, CANDIDATES, count, 1.0, eps, monotone=True)
    assert not dpkit.is_pure_dp(mech, REPLACE, eps)
    assert worst_loss(mech, REPLACE) <= 2 * eps + 1e-12


def test_utility_bound_holds_exactly():
    rng = random.Random(13)
    for _ in range(500):
        m = rng.randint(1, 12)
        cands = tuple(range(m))
        n = rng.randint(0, 30)
        x = tuple(rng.randrange(m) for _ in range(n))
        eps = rng.uniform(0.1, 2.0)
        t = rng.uniform(0.0, 4.0)
        monotone = rng.random() < 0.5
        pmf = exponential_pmf(x, cands, count, 1.0, eps, monotone)
        opt = max(count(x, r) for r in cands)
        thr = utility_threshold(opt, 1.0, eps, m, t, monotone)
        bad = sum(p for r, p in pmf.items() if count(x, r) <= thr)
        assert bad <= math.exp(-t) + 1e-12


def test_sampler_matches_pmf():
    rng = random.Random(14)
    n = 2000
    x = (0, 0, 0, 1, 1, 2)
    t = dpkit.hoeffding_margin(n, 1e-6 / 3)
    for eps in (0.5, 2.0):
        pmf = exponential_pmf(x, CANDIDATES, count, 1.0, eps)
        emp = dpkit.empirical_pmf(exponential_mechanism(x, CANDIDATES, count, 1.0, eps, rng) for _ in range(n))
        for r in CANDIDATES:
            assert abs(emp.get(r, 0.0) - pmf[r]) <= t


def test_gumbel_argmax_gives_the_same_distribution():
    # Adding Gumbel noise to the scores and taking the argmax samples the same pmf.
    rng = random.Random(15)
    n = 2000
    x = (0, 1, 1, 2, 2, 2)
    eps = 1.0
    pmf = exponential_pmf(x, CANDIDATES, count, 1.0, eps)
    picks = []
    for _ in range(n):
        noisy = [eps * count(x, r) / 2 - math.log(-math.log(1.0 - rng.random())) for r in CANDIDATES]
        picks.append(max(CANDIDATES, key=lambda r: noisy[r]))
    emp = dpkit.empirical_pmf(picks)
    t = dpkit.hoeffding_margin(n, 1e-6 / 3)
    for r in CANDIDATES:
        assert abs(emp.get(r, 0.0) - pmf[r]) <= t


def test_large_utilities_do_not_overflow():
    rng = random.Random(16)
    big = lambda x, r: 1e6 * r
    pmf = exponential_pmf(None, (0, 1, 2), big, 1.0, 1.0)
    assert pmf[2] == pytest.approx(1.0)
    assert exponential_mechanism(None, (0, 1, 2), big, 1.0, 1.0, rng) == 2


def test_edge_cases():
    rng = random.Random(0)
    with pytest.raises(ValueError):
        exponential_mechanism((), (), count, 1.0, 1.0, rng)
    with pytest.raises(ValueError):
        exponential_mechanism((), (0,), count, 1.0, 0.0, rng)
    with pytest.raises(ValueError):
        exponential_pmf((), (0,), count, 0.0, 1.0)
    assert exponential_mechanism((), ("only",), lambda x, r: 0.0, 1.0, 1.0, rng) == "only"
    # Equal utilities give the uniform distribution.
    pmf = exponential_pmf((), CANDIDATES, count, 1.0, 1.0)
    assert all(abs(p - 1 / 3) < 1e-15 for p in pmf.values())
