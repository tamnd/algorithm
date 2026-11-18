# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bond-energy-algorithm/. The authors are listed in prov/J9KWFD.jsonl.

import random
from itertools import permutations

import pytest

from bond_energy_algorithm import (affinity_matrix, bea, bea_original, best_order, bond, cont,
                                   global_affinity, measure_of_effectiveness, split, split_scores)


def random_workload(rng, n):
    q = rng.randint(1, 6)
    use = [set(rng.sample(range(n), rng.randint(1, min(3, n)))) for _ in range(q)]
    freq = [rng.randint(1, 9) for _ in range(q)]
    return use, freq


PAGE_USE = [{0, 2}, {1, 2}, {1, 3}, {2, 3}]
PAGE_FREQ = [45, 5, 75, 3]


def test_page_example():
    m = affinity_matrix(4, PAGE_USE, PAGE_FREQ)
    assert m == [[45, 0, 45, 0], [0, 80, 5, 75], [45, 5, 53, 3], [0, 75, 3, 78]]
    trace = []
    order, clustered = bea(m, trace)
    assert order == [0, 2, 1, 3]
    assert clustered == [[45, 45, 0, 0], [45, 53, 5, 3], [0, 5, 80, 75], [0, 3, 75, 78]]
    assert trace == [(2, 0, 8820), (2, 1, 10150), (2, 2, 1780),
                     (3, 0, 270), (3, 1, -7014), (3, 2, 23486), (3, 3, 23730)]
    assert global_affinity(m, order) == 34330 == best_order(m)[0]
    assert split_scores(order, PAGE_USE, PAGE_FREQ) == [(0, 83, 45, -2025), (45, 75, 8, 3311), (50, 0, 78, -6084)]
    assert split(order, PAGE_USE, PAGE_FREQ) == ([0, 2], [1, 3])


def test_not_optimal_example():
    m = affinity_matrix(4, [{0, 1}, {0, 3}, {0, 2}], [4, 2, 1])
    order, _ = bea(m)
    assert order == [2, 3, 0, 1] and global_affinity(m, order) == 128
    assert best_order(m)[0] == 132
    assert global_affinity(m, bea_original(m, 0)) == 132
    assert global_affinity(m, bea_original(m, 2)) == 128


def test_original_form_can_miss_from_every_start():
    m = affinity_matrix(5, [{1, 2, 4}, {1, 2, 3}, {3}, {0, 2, 3}, {2, 3, 4}], [5, 5, 4, 5, 3])
    best = max(global_affinity(m, bea_original(m, s)) for s in range(5))
    assert best == 2436 < best_order(m)[0] == 2598


@pytest.mark.parametrize("seed", range(40))
def test_am_equals_measure_of_effectiveness(seed):
    rng = random.Random(seed)
    n = rng.randint(1, 6)
    m = affinity_matrix(n, *random_workload(rng, n))
    for _ in range(5):
        order = list(range(n))
        rng.shuffle(order)
        assert global_affinity(m, order) == measure_of_effectiveness(m, order)


@pytest.mark.parametrize("seed", range(40))
def test_cont_is_the_change_of_am(seed):
    rng = random.Random(1000 + seed)
    n = rng.randint(2, 6)
    m = affinity_matrix(n, *random_workload(rng, n))
    k = rng.randrange(n)
    others = [x for x in range(n) if x != k]
    rng.shuffle(others)
    for loc in range(len(others) + 1):
        left = others[loc - 1] if loc > 0 else None
        right = others[loc] if loc < len(others) else None
        new = others[:loc] + [k] + others[loc:]
        assert global_affinity(m, new) - global_affinity(m, others) == cont(m, left, k, right)


@pytest.mark.parametrize("seed", range(40))
def test_each_insertion_is_the_best_position(seed):
    rng = random.Random(2000 + seed)
    n = rng.randint(1, 7)
    m = affinity_matrix(n, *random_workload(rng, n))
    order, clustered = bea(m)
    assert sorted(order) == list(range(n))
    assert clustered == [[m[i][j] for j in order] for i in order]
    # Replay: the partial order after each step has the largest AM among all insertions of that column.
    partial = list(range(min(n, 2)))
    for k in range(2, n):
        options = [partial[:loc] + [k] + partial[loc:] for loc in range(len(partial) + 1)]
        values = [global_affinity(m, o) for o in options]
        partial = options[values.index(max(values))]
    assert partial == order
    assert global_affinity(m, order) <= best_order(m)[0]


@pytest.mark.parametrize("seed", range(20))
def test_split_matches_definition(seed):
    rng = random.Random(3000 + seed)
    n = rng.randint(2, 6)
    use, freq = random_workload(rng, n)
    order, _ = bea(affinity_matrix(n, use, freq))
    scores = split_scores(order, use, freq)
    for i, (ctq, cbq, coq, z) in enumerate(scores, start=1):
        top = set(order[:i])
        assert ctq == sum(f for a, f in zip(use, freq) if a and a <= top)
        assert cbq == sum(f for a, f in zip(use, freq) if a and not (a & top))
        assert ctq + cbq + coq == sum(freq)
        assert z == ctq * cbq - coq * coq
    top, bottom = split(order, use, freq, key=())
    assert sorted(top + bottom) == list(range(n))
    best = max(s[3] for s in scores)
    assert scores[len(top) - 1][3] == best


def test_key_goes_to_both_fragments():
    top, bottom = split([1, 3, 2, 4], [{1, 3}, {2, 4}], [10, 10], key=[0])
    assert top == [0, 1, 3] and bottom == [0, 2, 4]


def test_small_cases():
    assert bea([]) == ([], [])
    assert bea([[5]]) == ([0], [[5]])
    assert bond([[1, 2], [3, 4]], 0, 1) == 1 * 2 + 3 * 4
    assert bond([[1]], None, 0) == 0
    with pytest.raises(ValueError):
        split([0], [{0}], [1])
