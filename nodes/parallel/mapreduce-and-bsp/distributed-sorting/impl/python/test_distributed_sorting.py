# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/distributed-sorting/. The authors are listed in prov/1SRXBE.jsonl.

import math
import random

from distributed_sorting import (balance_bound, distributed_sort, make_splits, max_bucket_with_fixed_splitters,
                                 sample_size_per_reducer, sort_round)


def test_page_example_sort_round():
    keys = [17, 3, 12, 8, 20, 1, 15, 6, 11, 9]
    out, sizes = sort_round(make_splits(keys, 2), [7, 13], 3)
    assert out == [[1, 3, 6], [8, 9, 11, 12], [15, 17, 20]]
    assert sizes == [3, 4, 3]


def test_sample_size_formula():
    assert sample_size_per_reducer(2000, 0.5, 0.1) == 119
    assert sample_size_per_reducer(10**9, 0.1, 0.01) == 5573
    a = sample_size_per_reducer(20000, 0.5, 0.1)
    assert a == 147 and balance_bound(20000, a, 0.5) <= 0.1


def test_output_is_sorted_on_seeded_inputs():
    rng = random.Random(13)
    for _ in range(150):
        n = rng.randrange(0, 200)
        keys = [rng.randrange(rng.choice([1, 5, 1000])) for _ in range(n)]
        m, r, a = rng.randrange(1, 6), rng.randrange(1, 9), rng.randrange(1, 10)
        out, costs = distributed_sort(keys, m, r, a, rng)
        assert out == sorted(keys)
        if n:
            assert costs["rounds"] == 2 and costs["sample_pairs"] == a * r and costs["sort_pairs"] == n
            assert sum(costs["bucket_sizes"]) == n


def test_balance_meets_the_proved_bound():
    rng = random.Random(14)
    n, r, eps, delta = 4000, 8, 0.5, 0.2
    a = sample_size_per_reducer(n, eps, delta)
    assert balance_bound(n, a, eps) <= delta
    w = math.ceil((1 + eps) * n / r)
    trials, failures = 25, 0
    for _ in range(trials):
        keys = [rng.random() for _ in range(n)]
        out, costs = distributed_sort(keys, 5, r, a, rng)
        assert out == sorted(keys)
        failures += max(costs["bucket_sizes"]) > w
    assert failures / trials <= delta


def test_heavy_duplicates_are_split_by_the_tie_break():
    rng = random.Random(15)
    keys = [7] * 3000 + [rng.randrange(100) for _ in range(1000)]
    a = sample_size_per_reducer(len(keys), 0.5, 0.2)
    out, costs = distributed_sort(keys, 4, 8, a, rng)
    assert out == sorted(keys)
    assert max(costs["bucket_sizes"]) <= math.ceil(1.5 * len(keys) / 8)


def test_fixed_splitters_fail_on_clustered_keys():
    rng = random.Random(5)
    keys = [rng.random() ** 4 for _ in range(20000)]
    assert max_bucket_with_fixed_splitters(keys, [j / 8 for j in range(1, 8)]) > 11000
    out, costs = distributed_sort(keys, 10, 8, 147, rng)
    assert out == sorted(keys) and max(costs["bucket_sizes"]) <= 3750
