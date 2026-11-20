# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ef1-and-pareto-optimal-algorithm/. The authors are listed in prov/HCYFF2.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from ef1_and_pareto_optimal_algorithm import bkv_exact, bundles_of, is_price_ef1

F = Fraction


def value(row, bundle):
    return sum(row[g] for g in bundle)


def is_ef1(values, bundles) -> bool:
    n = len(values)
    for i in range(n):
        mine = value(values[i], bundles[i])
        for k in range(n):
            if i != k and bundles[k]:
                other = value(values[i], bundles[k])
                if not any(mine >= other - values[i][g] for g in bundles[k]):
                    return False
    return True


def is_pareto_optimal(values, bundles) -> bool:
    """Brute force over all n^m allocations."""
    n, m = len(values), len(values[0])
    u = [value(values[i], bundles[i]) for i in range(n)]
    for owner in itertools.product(range(n), repeat=m):
        w = [0] * n
        for g, i in enumerate(owner):
            w[i] += values[i][g]
        if all(w[i] >= u[i] for i in range(n)) and any(w[i] > u[i] for i in range(n)):
            return False
    return True


def holds_only_mbb_goods(values, owner, p) -> bool:
    n, m = len(values), len(values[0])
    for i in range(n):
        best = max(F(values[i][j]) / p[j] for j in range(m))
        if any(owner[j] == i and F(values[i][j]) / p[j] != best for j in range(m)):
            return False
    return True


def test_worked_example():
    values = [[5, 8, 1, 6], [3, 1, 2, 2], [1, 5, 4, 4]]
    stats = {}
    bundles = bkv_exact(values, stats=stats)
    events = [(kind, owner, [str(q) for q in p]) for kind, owner, p in stats["trace"]]
    assert events == [
        ("start", [0, 0, 2, 0], ["5", "8", "4", "6"]),
        ("swap", [1, 0, 2, 0], ["5", "8", "4", "6"]),
        ("rise", [1, 0, 2, 0], ["5", "8", "5", "6"]),
        ("rise", [1, 0, 2, 0], ["6", "8", "6", "6"]),
    ]
    assert bundles == [[1, 3], [0], [2]]
    assert [value(values[i], bundles[i]) for i in range(3)] == [14, 3, 4]
    assert is_ef1(values, bundles)
    assert is_pareto_optimal(values, bundles)


def test_two_agents_with_a_tie():
    values = [[1, 3, 2], [1, 1, 1]]
    stats = {}
    assert bkv_exact(values, stats=stats) == [[1, 2], [0]]
    assert [kind for kind, _, _ in stats["trace"]] == ["start", "swap", "rise"]
    assert stats["prices"] == [2, 3, 2]


def test_random_ef1_and_pareto_optimal():
    rng = random.Random(31)
    count = 0
    while count < 700:
        n = rng.randint(2, 4)
        m = rng.randint(1, 6 if n < 4 else 5)
        top = rng.choice([2, 4, 10, 30])
        values = [[rng.randint(1, top) for _ in range(m)] for _ in range(n)]
        stats = {}
        bundles = bkv_exact(values, stats=stats)
        assert sorted(g for b in bundles for g in b) == list(range(m))
        assert is_ef1(values, bundles)
        assert is_pareto_optimal(values, bundles)
        count += 1


def test_invariants_along_the_run():
    rng = random.Random(32)
    for _ in range(400):
        n, m = rng.randint(2, 5), rng.randint(2, 9)
        values = [[rng.randint(1, 12) for _ in range(m)] for _ in range(n)]
        stats = {}
        bundles = bkv_exact(values, stats=stats)
        last = None
        for kind, owner, p in stats["trace"]:
            assert holds_only_mbb_goods(values, owner, p)
            if last is not None:
                assert all(a >= b for a, b in zip(p, last))
                if kind == "rise":
                    assert any(a > b for a, b in zip(p, last))
            last = p
        assert is_price_ef1(bundles, stats["prices"])
        assert is_ef1(values, bundles)


def test_one_agent_and_identical_values():
    assert bkv_exact([[3, 1, 2]]) == [[0, 1, 2]]
    rng = random.Random(33)
    for _ in range(100):
        n, m = rng.randint(2, 4), rng.randint(1, 7)
        row = [rng.randint(1, 9) for _ in range(m)]
        values = [row] * n
        assert is_ef1(values, bkv_exact(values))


def test_price_ef1_check():
    p = [F(5), F(8), F(4), F(6)]
    assert not is_price_ef1(bundles_of([0, 0, 2, 0], 3), p)
    assert is_price_ef1([[1, 3], [0], [2]], [F(6), F(8), F(6), F(6)])


def test_bad_input_and_step_limit():
    with pytest.raises(ValueError):
        bkv_exact([])
    with pytest.raises(ValueError):
        bkv_exact([[1, 0], [1, 1]])
    with pytest.raises(ValueError):
        bkv_exact([[1, 2], [1]])
    with pytest.raises(RuntimeError):
        bkv_exact([[5, 8, 1, 6], [3, 1, 2, 2], [1, 5, 4, 4]], max_steps=0)
