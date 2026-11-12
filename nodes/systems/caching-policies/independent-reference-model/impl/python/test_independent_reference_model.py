# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independent-reference-model/. The authors are listed in prov/A6MTB2.jsonl.

import random
from collections import OrderedDict
from fractions import Fraction as F

from independent_reference_model import (a0_hit_ratio, fifo_hit_ratio_by_chain, irm_trace, lru_hit_ratio,
                                         lru_hit_ratio_by_chain, lru_stationary, lru_state_probability,
                                         product_form_hit_ratio, random_hit_ratio_by_chain)

SMALL = [F(1, 2), F(1, 3), F(1, 6)]


def test_small_example() -> None:
    assert a0_hit_ratio(SMALL, 2) == F(7, 9)
    assert lru_hit_ratio(SMALL, 2) == F(133, 180)
    assert lru_hit_ratio_by_chain(SMALL, 2) == F(133, 180)
    assert lru_state_probability(SMALL, (0, 1)) == F(1, 3)
    assert lru_hit_ratio(SMALL, 1) == F(7, 18)


def test_closed_form_equals_stationary_distribution() -> None:
    cases = [
        [F(1, 4)] * 4,
        [F(2, 5), F(3, 10), F(1, 5), F(1, 10)],
        [F(1, 2), F(1, 4), F(1, 8), F(1, 16), F(1, 16)],
        [F(6, 10), F(1, 10), F(1, 10), F(1, 10), F(1, 10)],
    ]
    for p in cases:
        for k in range(1, len(p)):
            pi = lru_stationary(p, k)
            for s, w in pi.items():
                assert w == lru_state_probability(p, s)
            assert sum(pi.values()) == 1
            assert lru_hit_ratio(p, k) == lru_hit_ratio_by_chain(p, k)


def test_uniform_and_bounds() -> None:
    p = [F(1, 5)] * 5
    for k in range(1, 6):
        assert lru_hit_ratio(p, k) == F(k, 5) == a0_hit_ratio(p, k)
    q = [F(2, 5), F(3, 10), F(1, 5), F(1, 10)]
    assert lru_hit_ratio(q, 1) == a0_hit_ratio(q, 1) == sum(x * x for x in q)
    for k in range(1, 4):
        if k > 1:
            assert lru_hit_ratio(q, k) < a0_hit_ratio(q, k)
        assert lru_hit_ratio(q, k) < lru_hit_ratio(q, k + 1)


def test_fifo_and_random_have_the_product_form() -> None:
    assert product_form_hit_ratio(SMALL, 2) == F(8, 11)
    assert fifo_hit_ratio_by_chain(SMALL, 2) == F(8, 11)
    assert random_hit_ratio_by_chain(SMALL, 2) == F(8, 11)
    cases = [
        [F(2, 5), F(3, 10), F(1, 5), F(1, 10)],
        [F(1, 2), F(1, 4), F(1, 8), F(1, 16), F(1, 16)],
    ]
    for p in cases:
        for k in range(1, len(p)):
            want = product_form_hit_ratio(p, k)
            assert fifo_hit_ratio_by_chain(p, k) == want
            assert random_hit_ratio_by_chain(p, k) == want
            assert want <= lru_hit_ratio(p, k) <= a0_hit_ratio(p, k)


def test_simulation_is_close() -> None:
    rng = random.Random(17)
    p = [0.5, 1 / 3, 1 / 6]
    seq = irm_trace(p, 60000, rng)
    cache, hits = OrderedDict(), 0
    for x in seq:
        if x in cache:
            hits += 1
            cache.move_to_end(x)
        else:
            if len(cache) == 2:
                cache.popitem(last=False)
            cache[x] = True
    assert abs(hits / len(seq) - 133 / 180) < 0.01


def test_a0_simulation_is_close() -> None:
    rng = random.Random(18)
    p = [0.5, 1 / 3, 1 / 6]
    seq = irm_trace(p, 60000, rng)
    cache, hits = set(), 0
    for x in seq:
        if x in cache:
            hits += 1
        else:
            if len(cache) == 2:
                cache.remove(max(cache))
            cache.add(x)
    assert abs(hits / len(seq) - 7 / 9) < 0.01
