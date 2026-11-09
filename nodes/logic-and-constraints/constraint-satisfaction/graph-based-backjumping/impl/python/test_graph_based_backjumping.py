# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/graph-based-backjumping/. The authors are listed in prov/F25KS3.jsonl.

import itertools
import random

from graph_based_backjumping import graph_based_backjumping, graph_based_backjumping_search


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
    doms = [[1, 2]] * 4
    cons = {(0, 3): {(2, 1), (2, 2)}, (2, 3): {(1, 2), (2, 1)}}
    assert graph_based_backjumping_search(doms, cons) == ([[2, 1, 1, 2]], 13)
    assert backtracking(doms, cons, first=True) == ([[2, 1, 1, 2]], 20)
    sols, nodes = graph_based_backjumping_search(doms, cons, all_solutions=True)
    assert sorted(sols) == sorted(brute_force(doms, cons))
    assert nodes == 23


def test_jump_over_unconnected_variables():
    # x0 = 0 makes x5 impossible; x1 .. x4 are not connected to x5.
    d = 3
    doms = [list(range(d))] * 6
    cons = {(0, 5): {(a, b) for a in range(d) for b in range(d) if a != 0}}
    for i in range(1, 4):
        cons[(i, i + 1)] = {(a, b) for a in range(d) for b in range(d) if a != b}
    sol, nodes = graph_based_backjumping_search(doms, cons)
    bt, bt_nodes = backtracking(doms, cons, first=True)
    assert sol == bt
    # GBJ leaves x0 = 0 after one dead end at x5; backtracking tries every x1 .. x4.
    assert nodes == 18
    assert bt_nodes > 100


def test_queens():
    for n, count in [(1, 1), (2, 0), (3, 0), (4, 2), (5, 10), (6, 4)]:
        doms, cons = queens(n)
        sols, nodes = graph_based_backjumping_search(doms, cons, all_solutions=True)
        assert len(sols) == count
        # A complete constraint graph: GBJ is chronological backtracking.
        assert (sols, nodes) == backtracking(doms, cons)


def test_edges():
    assert graph_based_backjumping([], {}) == []
    assert graph_based_backjumping([[]], {}) is None
    assert graph_based_backjumping([[1], []], {}) is None
    assert graph_based_backjumping([[1], [2]], {}) == [1, 2]
    cons = {(0, 1): {(1, 1), (2, 2)}, (1, 0): {(1, 1)}}
    assert graph_based_backjumping_search([[1, 2], [1, 2]], cons, True)[0] == [[1, 1]]


def test_against_brute_force_and_backtracking():
    rng = random.Random(1990)
    for _ in range(800):
        n = rng.randint(1, 7)
        d = rng.randint(1, 4)
        doms, cons = random_csp(rng, n, d, rng.random() * 0.8, rng.random() * 0.8)
        want = brute_force(doms, cons)
        sols, nodes = graph_based_backjumping_search(doms, cons, all_solutions=True)
        assert sorted(sols) == sorted(want)
        bt_sols, bt_nodes = backtracking(doms, cons)
        assert sols == bt_sols  # the same solutions in the same order
        assert nodes <= bt_nodes
        first, first_nodes = graph_based_backjumping_search(doms, cons)
        bt_first, bt_first_nodes = backtracking(doms, cons, first=True)
        assert first == bt_first == want[:1]
        assert first_nodes <= bt_first_nodes
