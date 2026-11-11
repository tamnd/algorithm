# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/information-set-decoding/. The authors are listed in prov/97Z92V.jsonl.
"""Tests for the ISD harness.

ISD is a family of attacks, not a standard, so there are no official test
vectors. The tests check every variant against brute force, the mean number
of rounds against the formulas, and the worst case exponent of Prange against
the value 0.1207 that Kachigar and Tillich (PQCrypto 2017) state.
"""

import random
from itertools import combinations

from information_set_decoding import (
    gv_distance,
    isd,
    lee_brickell_candidates,
    mean_rounds,
    prange_candidates,
    prange_exponent,
    random_instance,
    stern_candidates,
    success_lee_brickell,
    success_prange,
    success_stern,
    syndrome,
)


def brute_force(h, s, n, w):
    out = []
    for pos in combinations(range(n), w):
        e = sum(1 << c for c in pos)
        if syndrome(h, e) == s:
            out.append(e)
    return out


def test_every_variant_returns_only_solutions():
    rng = random.Random(1962)
    variants = [prange_candidates(), lee_brickell_candidates(1), lee_brickell_candidates(2),
                stern_candidates(1, 1)]
    found = 0
    for case in range(500):
        n = rng.randint(6, 12)
        k = rng.randint(2, n - 3)
        w = rng.randint(2, min(4, n - k))
        h, s, _ = random_instance(n, k, w, rng)
        sols = brute_force(h, s, n, w)
        e, _, _ = isd(h, s, n, w, variants[case % 4], rng, max_iter=300)
        if e is not None:
            assert e in sols
            found += 1
    assert found > 450


def test_mean_rounds_match_the_formulas_on_the_same_instances():
    n, k, w, trials, seed = 50, 25, 5, 40, 7
    pr, pr_tried = mean_rounds(n, k, w, prange_candidates(), trials, seed)
    lb, lb_tried = mean_rounds(n, k, w, lee_brickell_candidates(2), trials, seed)
    st, st_tried = mean_rounds(n, k, w, stern_candidates(1, 3), trials, seed)
    for got, p in ((pr, success_prange(n, k, w)), (lb, success_lee_brickell(n, k, w, 2)),
                   (st, success_stern(n, k, w, 1, 3))):
        assert abs(got - 1 / p) < 0.3 / p
    assert lb < st < pr
    assert pr_tried == pr


def test_prange_worst_case_exponent():
    worst = max(prange_exponent(r / 1000, gv_distance(r / 1000)) for r in range(10, 990))
    assert abs(worst - 0.1207) < 0.0005


def test_exponent_agrees_with_the_finite_formula():
    from math import comb, log2
    n, rate = 2000, 0.5
    k = int(rate * n)
    w = int(gv_distance(rate) * n)
    exact = log2(comb(n, w) / comb(n - k, w)) / n
    assert abs(exact - prange_exponent(k / n, w / n)) < 0.01
