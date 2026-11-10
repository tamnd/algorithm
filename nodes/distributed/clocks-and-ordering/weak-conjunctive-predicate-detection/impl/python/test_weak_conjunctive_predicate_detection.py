# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/weak-conjunctive-predicate-detection/. The authors are listed in prov/A6CJ2B.jsonl.

import random

from weak_conjunctive_predicate_detection import brute_force, candidates, detect, random_computation, state_clocks

# The page example: p0 sends m0 to p1, p1 receives it and sends m1 to p2.
EXAMPLE = [
    [("send", 0, 1), ("int",)],
    [("recv", 0, 0), ("send", 1, 2)],
    [("int",), ("recv", 1, 1)],
]
PRED = [[True, False, True], [False, True, False], [True, False, True]]


def test_page_example() -> None:
    clocks = state_clocks(EXAMPLE)
    q = candidates(clocks, PRED)
    assert q == [[(0, 0, 0), (2, 0, 0)], [(1, 1, 0)], [(0, 0, 0), (1, 2, 2)]]
    cut, cmp = detect(q)
    assert cut == (2, 1, 0)
    assert brute_force(q) == [(2, 1, 0)]
    assert cmp == 13


def test_against_brute_force() -> None:
    found = missed = 0
    for seed in range(400):
        rng = random.Random(seed)
        n = rng.randrange(2, 5)
        comp = random_computation(n, rng.randrange(3, 16), rng)
        clocks = state_clocks(comp)
        pred = [[rng.random() < 0.35 for _ in c] for c in clocks]
        q = candidates(clocks, pred)
        cut, cmp = detect(q)
        sols = brute_force(q)
        if not sols:
            assert cut is None
            missed += 1
            continue
        found += 1
        least = tuple(min(s[k] for s in sols) for k in range(n))
        assert least in sols  # the solutions form a lattice
        assert cut == least  # the checker finds the least one
        m = max(len(x) for x in q)
        assert cmp <= 2 * (n - 1) * n * m
    assert found > 50 and missed > 50
