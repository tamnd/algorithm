# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clustered-index/. The authors are listed in prov/KP39G2.jsonl.

import random
from fractions import Fraction
from itertools import combinations

from clustered_index import (IndexedTable, layout_clustered, layout_random,
                             layout_striped, yao_expected_pages)

N, P, F = 1000, 10, 50


def test_example_counts():
    clu = IndexedTable(layout_clustered(N, P), F)
    stri = IndexedTable(layout_striped(N, P), F)
    rnd = IndexedTable(layout_random(N, P, 7), F)
    assert clu.height == 2 and clu.scan_cost() == 100
    keys, ix, data = clu.range_query(200, 299)
    assert keys == list(range(200, 300)) and (ix, data) == (3, 10)
    assert stri.range_query(200, 299)[1:] == (3, 100)
    assert rnd.range_query(200, 299)[1:] == (3, 98)
    assert rnd.range_query(200, 299, sort_rids=True)[1:] == (3, 65)
    assert clu.range_query(0, 999)[1:] == (21, 100)
    assert stri.range_query(0, 999)[1:] == (21, 1000)
    assert stri.range_query(0, 999, sort_rids=True)[1:] == (21, 100)
    assert clu.range_query(500, 500)[1:] == (2, 1)


def test_clustered_cost_is_probe_plus_matching_pages():
    rng = random.Random(1)
    for _ in range(200):
        p = rng.randint(1, 12)
        n = p * rng.randint(1, 40)
        f = rng.randint(2, 9)
        t = IndexedTable(layout_clustered(n, p), f)
        lo = rng.randint(0, n - 1)
        hi = rng.randint(lo, n - 1)
        keys, ix, data = t.range_query(lo, hi)
        assert keys == list(range(lo, hi + 1))
        assert ix == (t.height - 1) + (hi // f - lo // f + 1)
        assert data == hi // p - lo // p + 1


def test_unclustered_costs_one_io_per_tuple():
    rng = random.Random(2)
    for _ in range(200):
        p = rng.randint(2, 12)
        n = p * rng.randint(2, 40)
        t = IndexedTable(layout_striped(n, p), 4)
        lo = rng.randint(0, n - 1)
        hi = rng.randint(lo, n - 1)
        _, _, data = t.range_query(lo, hi)
        assert data == hi - lo + 1                     # every match on a new page
        _, _, sorted_data = t.range_query(lo, hi, sort_rids=True)
        assert sorted_data == min(hi - lo + 1, n // p)


def test_sorting_rids_never_costs_more():
    rng = random.Random(3)
    for seed in range(50):
        t = IndexedTable(layout_random(300, 6, seed), 8)
        lo = rng.randint(0, 299)
        hi = rng.randint(lo, 299)
        keys, _, a = t.range_query(lo, hi)
        _, _, b = t.range_query(lo, hi, sort_rids=True)
        assert b == len({t.page_of[k] for k in keys}) <= a <= len(keys)


def test_yao_formula_is_the_exact_expectation():
    n, p = 8, 2
    page = [i // p for i in range(n)]
    for k in range(n + 1):
        subsets = list(combinations(range(n), k))
        mean = Fraction(sum(len({page[i] for i in s}) for s in subsets), len(subsets))
        assert yao_expected_pages(n, p, k) == mean
    assert abs(float(yao_expected_pages(1000, 10, 100)) - 65.3072) < 1e-4
