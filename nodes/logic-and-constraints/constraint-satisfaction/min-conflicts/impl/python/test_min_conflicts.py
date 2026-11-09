# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-conflicts/. The authors are listed in prov/P8QYS3.jsonl.

import itertools
import random

from min_conflicts import min_conflicts


def queens(n):
    doms = [list(range(n)) for _ in range(n)]
    cons = {}
    for i in range(n):
        for j in range(i + 1, n):
            cons[(i, j)] = {(a, b) for a in range(n) for b in range(n) if a != b and abs(a - b) != j - i}
    return doms, cons


def random_csp(rng, n, d, density, tightness):
    doms = [list(range(d)) for _ in range(n)]
    cons = {}
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < density:
                cons[(i, j)] = {(a, b) for a in range(d) for b in range(d) if rng.random() >= tightness}
    return doms, cons


def satisfies(sol, cons):
    return all((sol[i], sol[j]) in rel for (i, j), rel in cons.items())


def brute_force(doms, cons):
    return [list(t) for t in itertools.product(*doms) if satisfies(t, cons)]


def test_stuck_example_is_incomplete():
    # (1, 1, 1) is the only solution, but from (0, 0, 0) no step changes anything.
    doms = [[0, 1]] * 3
    eq = {(0, 0), (1, 1)}
    cons = {(0, 1): {(1, 1)}, (0, 2): eq, (1, 2): eq}
    assert brute_force(doms, cons) == [[1, 1, 1]]
    for seed in range(20):
        sol, steps = min_conflicts(doms, cons, max_steps=200, seed=seed, initial=[0, 0, 0])
        assert sol is None and steps == 200


def test_queens():
    for n in (4, 8, 16, 32, 50):
        doms, cons = queens(n)
        sol, steps = min_conflicts(doms, cons, max_steps=5000, seed=n)
        assert sol is not None and satisfies(sol, cons)
        assert steps < 5000


def test_edges():
    assert min_conflicts([], {}) == ([], 0)
    assert min_conflicts([[]], {}) == (None, 0)
    assert min_conflicts([[1], [2]], {}) == ([1, 2], 0)
    # Already a solution: zero steps.
    doms, cons = queens(4)
    assert min_conflicts(doms, cons, initial=[1, 3, 0, 2]) == ([1, 3, 0, 2], 0)


def test_against_brute_force():
    rng = random.Random(1992)
    found = 0
    solvable = 0
    for case in range(700):
        n = rng.randint(1, 6)
        d = rng.randint(1, 4)
        doms, cons = random_csp(rng, n, d, rng.random(), rng.random() * 0.6)
        want = brute_force(doms, cons)
        solvable += bool(want)
        sol, steps = min_conflicts(doms, cons, max_steps=300, seed=case)
        if sol is not None:
            # Sound: every answer is a solution.
            assert sol in want
            found += 1
        elif want:
            # Incomplete: a miss is allowed, but it must use the whole budget.
            assert steps == 300
        else:
            assert steps in (0, 300)
    # Measured with these seeds: 582 of the 586 solvable cases are solved in 300 steps.
    assert solvable == 586
    assert found == 582
