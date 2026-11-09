# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-backtracking/. The authors are listed in prov/KDGJJC.jsonl.

import itertools
import random

from dynamic_backtracking import dynamic_backtracking, dynamic_backtracking_search


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


def backtracking(doms, cons):
    """Chronological backtracking, first solution or None."""
    n = len(doms)
    sigma = []

    def ok(i, a):
        for j in range(i):
            if (j, i) in cons and (sigma[j], a) not in cons[(j, i)]:
                return False
            if (i, j) in cons and (a, sigma[j]) not in cons[(i, j)]:
                return False
        return True

    def rec(i):
        if i == n:
            return list(sigma)
        for a in doms[i]:
            if ok(i, a):
                sigma.append(a)
                found = rec(i + 1)
                sigma.pop()
                if found is not None:
                    return found
        return None

    return rec(0)


def test_page_example():
    # x1 = 1 rules out every value of x4; x3 and x4 must differ; x2 is free.
    doms = [[1, 2]] * 4
    cons = {(0, 3): {(2, 1), (2, 2)}, (2, 3): {(1, 2), (2, 1)}}
    sols, stats = dynamic_backtracking_search(doms, cons)
    # x2 = 1 and x3 = 1 are kept when x1 changes.
    assert sols == [[2, 1, 1, 2]]
    assert stats["nodes"] == 5
    sols, _ = dynamic_backtracking_search(doms, cons, all_solutions=True)
    assert sorted(sols) == sorted(brute_force(doms, cons))


def test_queens():
    for n, count in [(1, 1), (2, 0), (3, 0), (4, 2), (5, 10), (6, 4), (7, 40), (8, 92)]:
        doms, cons = queens(n)
        sols, stats = dynamic_backtracking_search(doms, cons, all_solutions=True)
        assert len(sols) == count
        assert len({tuple(s) for s in sols}) == count
        assert all(satisfies(s, cons) for s in sols)
        assert stats["max_eliminations"] <= n * n
    doms, cons = queens(12)
    sol = dynamic_backtracking(doms, cons)
    assert sol is not None and satisfies(sol, cons)


def test_edges():
    assert dynamic_backtracking([], {}) == []
    assert dynamic_backtracking([[]], {}) is None
    assert dynamic_backtracking([[1], []], {}) is None
    assert dynamic_backtracking([[1], [2]], {}) == [1, 2]
    cons = {(0, 1): {(1, 1), (2, 2)}, (1, 0): {(1, 1)}}
    assert dynamic_backtracking_search([[1, 2], [1, 2]], cons, True)[0] == [[1, 1]]
    # Pigeonhole: three variables, two values, all different.
    ne = {(a, b) for a in (0, 1) for b in (0, 1) if a != b}
    assert dynamic_backtracking([[0, 1]] * 3, {(0, 1): ne, (0, 2): ne, (1, 2): ne}) is None


def test_against_brute_force_and_backtracking():
    rng = random.Random(1993)
    for _ in range(800):
        n = rng.randint(1, 7)
        d = rng.randint(1, 4)
        doms, cons = random_csp(rng, n, d, rng.random(), rng.random() * 0.7)
        want = brute_force(doms, cons)
        sols, stats = dynamic_backtracking_search(doms, cons, all_solutions=True)
        assert sorted(sols) == sorted(want)
        assert len(sols) == len(want)  # each solution once
        # Polynomial space: at most one stored elimination per value.
        assert stats["max_eliminations"] <= sum(len(x) for x in doms)
        one = dynamic_backtracking(doms, cons)
        bt = backtracking(doms, cons)
        assert (one is None) == (bt is None) == (not want)
        if one is not None:
            assert satisfies(one, cons)
