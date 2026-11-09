# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/forward-checking/. The authors are listed in prov/346K9S.jsonl.

import itertools
import random

from forward_checking import forward_checking, forward_checking_search


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


def backtracking_nodes(doms, cons, first=False):
    """Chronological backtracking: number of assignments tried (all solutions, or up to the first)."""
    n = len(doms)
    count = 0
    sigma = []
    done = False

    def ok(i, a):
        for j in range(i):
            if (j, i) in cons and (sigma[j], a) not in cons[(j, i)]:
                return False
            if (i, j) in cons and (a, sigma[j]) not in cons[(i, j)]:
                return False
        return True

    def rec(i):
        nonlocal count, done
        if i == n:
            done = first
            return
        for a in doms[i]:
            if done:
                return
            count += 1
            if ok(i, a):
                sigma.append(a)
                rec(i + 1)
                sigma.pop()

    rec(0)
    return count


def test_four_queens_example():
    doms, cons = queens(4)
    sols, nodes = forward_checking_search(doms, cons)
    assert sols == [[1, 3, 0, 2]]
    assert nodes == 8
    sols, nodes = forward_checking_search(doms, cons, all_solutions=True)
    assert sorted(sols) == [[1, 3, 0, 2], [2, 0, 3, 1]]
    assert nodes == 16
    assert backtracking_nodes(doms, cons) == 60


def test_queens_counts():
    for n, want in [(1, 1), (2, 0), (3, 0), (5, 10), (6, 4), (7, 40), (8, 92)]:
        doms, cons = queens(n)
        sols, _ = forward_checking_search(doms, cons, all_solutions=True)
        assert len(sols) == want
        assert all(satisfies(s, cons) for s in sols)


def test_edges():
    assert forward_checking([], {}) == []
    assert forward_checking([[]], {}) is None
    assert forward_checking([[1], [2]], {}) == [1, 2]
    assert forward_checking([[1, 2], []], {}) is None
    # Two constraints on the same pair are intersected.
    cons = {(0, 1): {(1, 1), (2, 2)}, (1, 0): {(1, 1)}}
    assert forward_checking_search([[1, 2], [1, 2]], cons, True)[0] == [[1, 1]]


def test_against_brute_force():
    rng = random.Random(1980)
    for _ in range(600):
        n = rng.randint(1, 6)
        d = rng.randint(1, 4)
        doms, cons = random_csp(rng, n, d, rng.random(), rng.random() * 0.6)
        want = brute_force(doms, cons)
        sols, nodes = forward_checking_search(doms, cons, all_solutions=True)
        assert sorted(sols) == sorted(want)
        assert nodes <= backtracking_nodes(doms, cons)
        first, first_nodes = forward_checking_search(doms, cons)
        assert first_nodes <= backtracking_nodes(doms, cons, first=True)
        one = forward_checking(doms, cons)
        assert (one is None) == (not want)
        if one is not None:
            assert satisfies(one, cons)
            # Same variable and value order as brute force: the same first solution.
            assert one == want[0] == first[0]
