# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genetic-programming/. The authors are listed in prov/R0CA6Z.jsonl.

import math
import random
from collections import Counter

from genetic_programming import (
    depth,
    evaluate,
    full,
    genetic_programming,
    grow,
    ramped_half_and_half,
    replace_at,
    size,
    subtree_at,
    subtree_crossover,
    subtree_mutation,
    total_error,
)

QUADRATIC = [(x, x * x + x + 1) for x in range(-5, 6)]
QUARTIC = [(x, x**4 + x**3 + x * x + x) for x in range(-5, 6)]


def leaf_depths(tree, d=0):
    if isinstance(tree, tuple):
        return leaf_depths(tree[1], d + 1) + leaf_depths(tree[2], d + 1)
    return [d]


def test_evaluation_and_the_example_errors() -> None:
    a = ("add", ("mul", "x", "x"), 1)
    b = ("add", "x", 1)
    assert [evaluate(a, x) for x in (-2, 0, 3)] == [5, 1, 10]
    assert total_error(a, QUADRATIC) == 30
    assert total_error(b, QUADRATIC) == 110
    assert total_error(("add", ("mul", "x", "x"), ("add", "x", 1)), QUADRATIC) == 0
    assert total_error(("add", ("add", "x", 1), 1), QUADRATIC) == 101
    assert size(a) == 5 and depth(a) == 2 and depth("x") == 0


def test_example_crossover_children() -> None:
    a = ("add", ("mul", "x", "x"), 1)
    b = ("add", "x", 1)
    children = [replace_at(a, i, subtree_at(b, j)) for i in range(size(a)) for j in range(size(b))]
    assert len(children) == 15
    exact = [c for c in children if total_error(c, QUADRATIC) == 0]
    assert len(exact) == 3
    assert ("add", ("mul", ("add", "x", 1), "x"), 1) in exact


def test_full_grow_and_ramped_half_and_half() -> None:
    rng = random.Random(1)
    for d in range(5):
        for _ in range(50):
            assert set(leaf_depths(full(d, rng))) == {d}
            assert depth(grow(d, rng)) <= d
    pop = ramped_half_and_half(60, 2, 4, random.Random(2))
    for i, t in enumerate(pop):
        limit = 2 + (i // 2) % 3
        if i % 2 == 0:
            assert set(leaf_depths(t)) == {limit}
        else:
            assert depth(t) <= limit
    assert Counter(2 + (i // 2) % 3 for i in range(60)) == {2: 20, 3: 20, 4: 20}


def test_grow_distribution_at_depth_one() -> None:
    # Root: each of the 5 primitives with probability 1/5; a function then gets two terminals, 1/2 each.
    rng = random.Random(3)
    trials = 40000
    counts = Counter(grow(1, rng) for _ in range(trials))
    assert len(counts) == 2 + 3 * 4
    for t, c in counts.items():
        p = 1 / 5 if not isinstance(t, tuple) else 1 / 20
        assert abs(c / trials - p) < 5 * math.sqrt(p * (1 - p) / trials)


def test_crossover_and_mutation_replace_one_subtree() -> None:
    rng = random.Random(4)
    for _ in range(300):
        a, b = grow(5, rng), grow(5, rng)
        seed = rng.random()
        r1, r2 = random.Random(seed), random.Random(seed)
        child = subtree_crossover(a, b, r1)
        i, j = r2.randrange(size(a)), r2.randrange(size(b))
        assert child == replace_at(a, i, subtree_at(b, j))
        assert size(child) == size(a) - size(subtree_at(a, i)) + size(subtree_at(b, j))
        assert subtree_at(child, i) == subtree_at(b, j)
        m = subtree_mutation(a, 3, random.Random(seed))
        k = random.Random(seed).randrange(size(a))
        assert replace_at(m, k, subtree_at(a, k)) == a
        assert depth(subtree_at(m, k)) <= 3


def test_depth_limit_and_elitism() -> None:
    max_depth = 6
    seen = []

    def check(g, pop, errors):
        assert all(depth(t) <= max_depth for t in pop)
        assert errors == [total_error(t, QUARTIC) for t in pop]
        seen.append(min(errors))

    _, err, hist = genetic_programming(QUARTIC, 60, 15, 4, 0.8, 0.1, 2, 4, max_depth, 4, random.Random(5), check)
    assert hist[1:] == seen
    assert all(hist[g + 1] <= hist[g] for g in range(len(hist) - 1))
    assert err == hist[-1]


def test_fixed_seed_finds_the_quartic() -> None:
    best, err, hist = genetic_programming(QUARTIC, 100, 50, 7, 0.8, 0.1, 1, 4, 8, 4, random.Random(0))
    assert err == 0 and hist[-1] == 0 and hist[0] > 0
    assert all(evaluate(best, x) == y for x, y in QUARTIC)
    assert depth(best) <= 8
