# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maintaining-arc-consistency/. The authors are listed in prov/178PFC.jsonl.

import itertools
import random

from maintaining_arc_consistency import maintaining_arc_consistency, maintaining_arc_consistency_search


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


def compatible(i, a, j, b, cons):
    if (i, j) in cons and (a, b) not in cons[(i, j)]:
        return False
    if (j, i) in cons and (b, a) not in cons[(j, i)]:
        return False
    return True


def fc_nodes(doms, cons, first=False):
    """An independent recursive forward checking: number of assignments tried."""
    n = len(doms)
    count = 0
    done = False

    def rec(i, cd):
        nonlocal count, done
        for a in cd[i]:
            if done:
                return
            count += 1
            nd = list(cd)
            nd[i] = [a]
            wiped = False
            for j in range(i + 1, n):
                nd[j] = [b for b in cd[j] if compatible(i, a, j, b, cons)]
                if not nd[j]:
                    wiped = True
                    break
            if wiped:
                continue
            if i == n - 1:
                done = first
            else:
                rec(i + 1, nd)

    if n:
        rec(0, [list(d) for d in doms])
    return count


def ac_closure(doms, cons):
    """Arc consistency by a naive fixed point: None on a wipe-out."""
    n = len(doms)
    cd = [list(d) for d in doms]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(n):
                if i == j or ((i, j) not in cons and (j, i) not in cons):
                    continue
                keep = [a for a in cd[i] if any(compatible(i, a, j, b, cons) for b in cd[j])]
                if len(keep) < len(cd[i]):
                    cd[i] = keep
                    changed = True
        if any(not c for c in cd):
            return None
    return cd


def test_four_queens_example():
    doms, cons = queens(4)
    sols, nodes = maintaining_arc_consistency_search(doms, cons)
    assert sols == [[1, 3, 0, 2]]
    assert nodes == 5
    sols, nodes = maintaining_arc_consistency_search(doms, cons, all_solutions=True)
    assert sorted(sols) == [[1, 3, 0, 2], [2, 0, 3, 1]]
    assert nodes == 10
    assert fc_nodes(doms, cons, first=True) == 8


def test_queens_counts():
    for n, want in [(1, 1), (2, 0), (3, 0), (5, 10), (6, 4), (7, 40), (8, 92)]:
        doms, cons = queens(n)
        sols, nodes = maintaining_arc_consistency_search(doms, cons, all_solutions=True)
        assert len(sols) == want
        assert all(satisfies(s, cons) for s in sols)
        assert nodes <= fc_nodes(doms, cons)


def test_edges():
    assert maintaining_arc_consistency([], {}) == []
    assert maintaining_arc_consistency([[]], {}) is None
    assert maintaining_arc_consistency([[1], [2]], {}) == [1, 2]
    # Arc consistency alone detects this one: no node is tried.
    assert maintaining_arc_consistency_search([[1, 2], [3]], {(0, 1): {(1, 4)}}) == ([], 0)
    # Two constraints on the same pair are intersected.
    cons = {(0, 1): {(1, 1), (2, 2)}, (1, 0): {(1, 1)}}
    assert maintaining_arc_consistency_search([[1, 2], [1, 2]], cons, True)[0] == [[1, 1]]
    # Arc consistent but no solution: three variables, two colours, all different.
    ne = {(a, b) for a in (0, 1) for b in (0, 1) if a != b}
    sols, nodes = maintaining_arc_consistency_search([[0, 1]] * 3, {(0, 1): ne, (0, 2): ne, (1, 2): ne})
    assert sols == [] and nodes == 2


def test_against_brute_force():
    rng = random.Random(1994)
    for _ in range(600):
        n = rng.randint(1, 6)
        d = rng.randint(1, 4)
        doms, cons = random_csp(rng, n, d, rng.random(), rng.random() * 0.7)
        want = brute_force(doms, cons)
        sols, nodes = maintaining_arc_consistency_search(doms, cons, all_solutions=True)
        assert sorted(sols) == sorted(want)
        assert all(satisfies(s, cons) for s in sols)
        assert nodes <= fc_nodes(doms, cons)
        if ac_closure(doms, cons) is None:
            assert nodes == 0 and not want
        first, first_nodes = maintaining_arc_consistency_search(doms, cons)
        assert first_nodes <= fc_nodes(doms, cons, first=True)
        one = maintaining_arc_consistency(doms, cons)
        assert (one is None) == (not want)
        if one is not None:
            # Same variable and value order as brute force: the same first solution.
            assert one == want[0] == first[0]


def test_larger_queens():
    for n in (10, 12):
        doms, cons = queens(n)
        sol = maintaining_arc_consistency(doms, cons)
        assert sol is not None and satisfies(sol, cons)
