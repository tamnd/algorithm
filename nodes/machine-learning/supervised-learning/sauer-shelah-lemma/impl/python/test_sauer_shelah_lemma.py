# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sauer-shelah-lemma/. The authors are listed in prov/15YWCY.jsonl.

import random
from itertools import combinations

from sauer_shelah_lemma import (
    at_most_d_ones, exp_bound, growth, intervals_on_line, restriction, sauer_bound,
    shattered_subsets, vc_dimension,
)


def random_class(rng, N, size):
    return list({tuple(rng.randint(0, 1) for _ in range(N)) for _ in range(size)})


def test_pajor_inequality_on_random_classes():
    # |H_C| <= the number of subsets of C that H shatters (the claim the proof shows).
    rng = random.Random(1972)
    for _ in range(200):
        N = rng.randint(1, 7)
        H = random_class(rng, N, rng.randint(1, 40))
        C = list(range(N))
        assert len(restriction(H, C)) <= len(shattered_subsets(H, C))


def test_growth_function_meets_the_bound():
    rng = random.Random(11)
    for _ in range(60):
        N = rng.randint(2, 7)
        H = random_class(rng, N, rng.randint(1, 50))
        d = vc_dimension(H, list(range(N)))
        for n in range(1, N + 1):
            assert growth(H, list(range(N)), n) <= sauer_bound(n, d)


def test_closed_form_bound():
    for d in range(1, 12):
        for n in range(d, 60):
            assert sauer_bound(n, d) <= exp_bound(n, d)


def test_tightness_for_at_most_d_ones():
    for N in range(1, 8):
        for d in range(0, N + 1):
            H = at_most_d_ones(N, d)
            assert vc_dimension(H, list(range(N))) == d
            for n in range(1, N + 1):
                assert growth(H, list(range(N)), n) == sauer_bound(n, d)


def test_tightness_for_intervals():
    for N in range(1, 9):
        H = intervals_on_line(N)
        assert vc_dimension(H, list(range(N))) == min(2, N)
        assert len(restriction(H, list(range(N)))) == sauer_bound(N, 2)


def test_bound_is_not_tight_for_a_small_class():
    # Three hypotheses on three points: VC dimension 1, two labelings fewer than 1 + 3.
    H = [(0, 0, 0), (1, 0, 0), (1, 1, 0)]
    assert vc_dimension(H, [0, 1, 2]) == 1
    assert len(restriction(H, [0, 1, 2])) == 3 < sauer_bound(3, 1)
    assert all(len(restriction(H, list(C))) <= 3 for C in combinations(range(3), 2))
