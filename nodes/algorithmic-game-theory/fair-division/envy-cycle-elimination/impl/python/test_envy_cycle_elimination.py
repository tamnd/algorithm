# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/envy-cycle-elimination/. The authors are listed in prov/0PA93X.jsonl.

import itertools
import random

import pytest

from envy_cycle_elimination import additive, envy_cycle_elimination, envy_graph, find_cycle


def is_ef1(vals, bundles) -> bool:
    """EF1 by its definition, for any valuation functions."""
    n = len(bundles)
    for i in range(n):
        mine = vals[i](bundles[i])
        for j in range(n):
            if i == j or not bundles[j]:
                continue
            if not any(mine >= vals[i](bundles[j] - {g}) for g in bundles[j]):
                return False
    return True


def random_monotone(rng: random.Random, m: int):
    """A random monotone set function: random values on subsets, then the running maximum over subsets."""
    table = {}
    for mask in range(1 << m):
        best = rng.randint(0, 20)
        for g in range(m):
            if mask >> g & 1:
                best = max(best, table[mask ^ (1 << g)])
        table[mask] = best

    def v(s):
        mask = 0
        for g in s:
            mask |= 1 << g
        return table[mask]

    return v


def random_coverage(rng: random.Random, m: int):
    cover = [frozenset(e for e in range(4) if rng.random() < 0.4) for _ in range(m)]
    weight = [rng.randint(1, 6) for _ in range(4)]

    def v(s):
        seen = set()
        for g in s:
            seen |= cover[g]
        return sum(weight[e] for e in seen)

    return v


def test_worked_example():
    values = [[5, 6, 9, 1, 8], [4, 1, 3, 2, 6], [8, 4, 7, 9, 2]]
    vals = additive(values)
    stats = {}
    bundles = envy_cycle_elimination(vals, 5, stats=stats)
    assert bundles == [frozenset({2, 4}), frozenset({0}), frozenset({1, 3})]
    assert stats["rotations"] == 2
    assert [vals[i](bundles[i]) for i in range(3)] == [17, 4, 13]
    assert envy_graph(vals, bundles) == [[], [0], []]
    assert vals[1](bundles[0] - {4}) <= 4
    assert is_ef1(vals, bundles)


def test_find_cycle():
    out = [[1], [2], [0]]
    cycle = find_cycle(out)
    k = len(cycle)
    for t in range(k):
        assert cycle[t] in out[cycle[(t + 1) % k]]


def test_ef1_additive_random():
    rng = random.Random(11)
    for _ in range(600):
        n, m = rng.randint(1, 4), rng.randint(0, 7)
        values = [[rng.randint(0, 9) for _ in range(m)] for _ in range(n)]
        order = list(range(m))
        rng.shuffle(order)
        stats = {}
        bundles = envy_cycle_elimination(additive(values), m, order, stats)
        assert sorted(g for b in bundles for g in b) == list(range(m))
        assert is_ef1(additive(values), bundles)
        assert stats["rotations"] <= m * n * (n - 1) // 2


def test_ef1_monotone_random():
    rng = random.Random(12)
    for _ in range(400):
        n, m = rng.randint(2, 4), rng.randint(1, 7)
        vals = [random_monotone(rng, m) if rng.random() < 0.5 else random_coverage(rng, m) for _ in range(n)]
        stats = {}
        bundles = envy_cycle_elimination(vals, m, stats=stats)
        assert sorted(g for b in bundles for g in b) == list(range(m))
        assert is_ef1(vals, bundles)
        assert stats["rotations"] <= m * n * (n - 1) // 2


def test_identical_valuations_need_no_rotation():
    rng = random.Random(13)
    for _ in range(100):
        n, m = rng.randint(2, 4), rng.randint(1, 7)
        row = [rng.randint(0, 9) for _ in range(m)]
        stats = {}
        bundles = envy_cycle_elimination(additive([row] * n), m, stats=stats)
        assert stats["rotations"] == 0
        assert is_ef1(additive([row] * n), bundles)


def test_non_monotone_can_fail():
    # A valuation that drops when a second good is added breaks the invariant.
    found = False
    rng = random.Random(14)
    for _ in range(3000):
        m = 3
        table = {s: rng.randint(0, 5) for k in range(m + 1) for s in itertools.combinations(range(m), k)}
        vals = [lambda s, t=table: t[tuple(sorted(s))]] * 2
        bundles = envy_cycle_elimination(vals, m)
        if not is_ef1(vals, bundles):
            found = True
            break
    assert found


def test_bad_input():
    with pytest.raises(ValueError):
        envy_cycle_elimination([], 2)
    with pytest.raises(ValueError):
        envy_cycle_elimination(additive([[1, 2]]), 2, order=[0, 0])
