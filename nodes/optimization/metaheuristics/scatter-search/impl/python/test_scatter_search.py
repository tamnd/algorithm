# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/scatter-search/. The authors are listed in prov/GRJBJP.jsonl.

import itertools
import random

import pytest

from scatter_search import Knapsack, hamming, improve, repair, scatter_search

K7 = Knapsack([8, 16, 16, 12, 18, 9, 18], [10, 4, 10, 10, 5, 2, 2], 21)


def bits(s: str) -> tuple[int, ...]:
    return tuple(int(c) for c in s)


def brute_force(k: Knapsack) -> int:
    return max(k.value(x) for x in itertools.product([0, 1], repeat=len(k.values)) if k.weight(x) <= k.capacity)


def is_maximal(k: Knapsack, x) -> bool:
    return k.weight(x) <= k.capacity and all(x[i] or k.weight(x) + k.weights[i] > k.capacity for i in range(len(x)))


def test_example_of_the_page() -> None:
    assert brute_force(K7) == 68 and K7.ratio_order() == [6, 5, 1, 4, 2, 3, 0]
    assert improve(K7, (0,) * 7) == bits("0100111") and K7.value(bits("0100111")) == 61
    best, value, history = scatter_search(K7, 6, 2, 2, random.Random(0))
    assert [["".join(map(str, x)) for x in ref] for ref in history] == [
        ["0100111", "1100101", "1010000", "0110011"],
        ["0100111", "1100101", "0110101", "0110011"],
    ]
    assert hamming(bits("1010000"), bits("0100111")) == 6 and hamming(bits("1010000"), bits("1100101")) == 4
    union = bits("1110101")
    assert K7.weight(union) == 31 and repair(K7, union) == bits("0110101")
    assert (best, value) == (bits("0110101"), 68)


def random_knapsack(rng: random.Random) -> Knapsack:
    n = rng.randint(1, 9)
    weights = [rng.randint(1, 12) for _ in range(n)]
    return Knapsack([rng.randint(1, 20) for _ in range(n)], weights, rng.randint(0, sum(weights)))


def test_repair_and_improve() -> None:
    rng = random.Random(88)
    for _ in range(500):
        k = random_knapsack(rng)
        x = tuple(rng.randint(0, 1) for _ in k.values)
        r = repair(k, x)
        assert k.weight(r) <= k.capacity and all(a >= b for a, b in zip(x, r))
        if k.weight(x) <= k.capacity:
            assert r == x
        z = improve(k, r)
        assert is_maximal(k, z) and all(a <= b for a, b in zip(r, z))


def test_invariants_on_random_instances() -> None:
    rng = random.Random(1234)
    for _ in range(200):
        k = random_knapsack(rng)
        b1, b2 = rng.randint(1, 3), rng.randint(0, 3)
        best, value, history = scatter_search(k, rng.randint(1, 10), b1, b2, random.Random(rng.random()))
        size = len(history[0])
        assert 1 <= size <= b1 + b2
        totals = []
        for ref in history:
            assert len(ref) == size and len(set(ref)) == size
            assert all(is_maximal(k, x) for x in ref)
            totals.append(sum(k.value(x) for x in ref))
        # each round that changes the reference set raises the total value, and the best never drops
        assert all(a < b for a, b in zip(totals, totals[1:]))
        bests = [max(k.value(x) for x in ref) for ref in history]
        assert bests == sorted(bests)
        assert value == k.value(best) == bests[-1] <= brute_force(k)
        assert best in history[-1]


def test_edges() -> None:
    with pytest.raises(ValueError):
        scatter_search(K7, 0, 2, 2, random.Random(1))
    with pytest.raises(ValueError):
        scatter_search(K7, 5, 0, 2, random.Random(1))
    empty = Knapsack([5, 6], [3, 4], 0)
    assert scatter_search(empty, 4, 2, 2, random.Random(1))[:2] == ((0, 0), 0)
    assert scatter_search(Knapsack([], [], 3), 3, 1, 1, random.Random(1))[:2] == ((), 0)


def test_fixed_seed_reaches_the_optimum() -> None:
    r = random.Random(27)
    values = [r.randint(10, 60) for _ in range(12)]
    weights = [r.randint(5, 40) for _ in range(12)]
    k = Knapsack(values, weights, sum(weights) // 2)
    opt = brute_force(k)
    best, value, history = scatter_search(k, 10, 3, 3, random.Random(0))
    assert max(k.value(x) for x in history[0]) < opt
    assert value == opt == k.value(best) and k.weight(best) <= k.capacity
