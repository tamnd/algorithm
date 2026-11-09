# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/conflict-directed-backjumping/. The authors are listed in prov/7XCRR6.jsonl.

import itertools
import random

from conflict_directed_backjumping import conflict_directed_backjumping, conflict_directed_backjumping_search


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


def backtracking(doms, cons, first=False):
    """Chronological backtracking: (solutions, assignments tried)."""
    n = len(doms)
    count = 0
    sols = []
    sigma = []

    def ok(i, a):
        for j in range(i):
            if (j, i) in cons and (sigma[j], a) not in cons[(j, i)]:
                return False
            if (i, j) in cons and (a, sigma[j]) not in cons[(i, j)]:
                return False
        return True

    def rec(i):
        nonlocal count
        if i == n:
            sols.append(list(sigma))
            return
        for a in doms[i]:
            if first and sols:
                return
            count += 1
            if ok(i, a):
                sigma.append(a)
                rec(i + 1)
                sigma.pop()

    rec(0)
    return sols, count


def test_page_example():
    # x1 = 1 rules out every value of x4; x3 and x4 must differ; x2 is free.
    doms = [[1, 2]] * 4
    cons = {(0, 3): {(2, 1), (2, 2)}, (2, 3): {(1, 2), (2, 1)}}
    assert conflict_directed_backjumping_search(doms, cons) == ([[2, 1, 1, 2]], 10)
    assert backtracking(doms, cons, first=True) == ([[2, 1, 1, 2]], 20)
    sols, nodes = conflict_directed_backjumping_search(doms, cons, all_solutions=True)
    assert sorted(sols) == sorted(brute_force(doms, cons))
    assert nodes == 20
    assert backtracking(doms, cons)[1] == 30


def test_internal_dead_end_merges_conflict_sets():
    # x3 fails only because of x1 (with x2 = anything); x4 fails only because of x2.
    # A correct merge must not jump past a variable that is part of the reason.
    doms = [[0, 1], [0, 1], [0, 1], [0]]
    cons = {
        (0, 2): {(1, 0), (1, 1), (0, 0)},
        (1, 3): {(1, 0)},
        (2, 3): {(0, 0)},
    }
    want = brute_force(doms, cons)
    sols, _ = conflict_directed_backjumping_search(doms, cons, all_solutions=True)
    assert sorted(sols) == sorted(want)
    assert conflict_directed_backjumping(doms, cons) == want[0]


def test_queens():
    for n, count in [(1, 1), (2, 0), (3, 0), (4, 2), (5, 10), (6, 4), (7, 40)]:
        doms, cons = queens(n)
        sols, nodes = conflict_directed_backjumping_search(doms, cons, all_solutions=True)
        assert len(sols) == count
        assert all(satisfies(s, cons) for s in sols)
        assert nodes <= backtracking(doms, cons)[1]
    doms, cons = queens(8)
    one, nodes = conflict_directed_backjumping_search(doms, cons)
    bt, bt_nodes = backtracking(doms, cons, first=True)
    assert one == bt and (nodes, bt_nodes) == (765, 876)


def test_edges():
    assert conflict_directed_backjumping([], {}) == []
    assert conflict_directed_backjumping([[]], {}) is None
    assert conflict_directed_backjumping([[1], []], {}) is None
    assert conflict_directed_backjumping([[1], [2]], {}) == [1, 2]
    cons = {(0, 1): {(1, 1), (2, 2)}, (1, 0): {(1, 1)}}
    assert conflict_directed_backjumping_search([[1, 2], [1, 2]], cons, True)[0] == [[1, 1]]


def test_against_brute_force_and_backtracking():
    rng = random.Random(1993)
    for _ in range(800):
        n = rng.randint(1, 7)
        d = rng.randint(1, 4)
        doms, cons = random_csp(rng, n, d, rng.random(), rng.random() * 0.7)
        want = brute_force(doms, cons)
        sols, nodes = conflict_directed_backjumping_search(doms, cons, all_solutions=True)
        assert sorted(sols) == sorted(want)
        assert len(sols) == len(want)
        bt_sols, bt_nodes = backtracking(doms, cons)
        assert sols == bt_sols  # the same solutions in the same order
        assert nodes <= bt_nodes
        first, first_nodes = conflict_directed_backjumping_search(doms, cons)
        bt_first, bt_first_nodes = backtracking(doms, cons, first=True)
        assert first == bt_first == want[:1]
        assert first_nodes <= bt_first_nodes
