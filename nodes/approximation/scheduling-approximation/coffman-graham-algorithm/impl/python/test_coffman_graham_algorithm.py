# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coffman-graham-algorithm/. The authors are listed in prov/7X27J2.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from coffman_graham_algorithm import coffman_graham, coffman_graham_labels, transitive_reduction


def check_feasible(succ, m, slot):
    n = len(succ)
    assert len(slot) == n
    assert all(s >= 1 for s in slot)
    for t in set(slot):
        assert sum(1 for s in slot if s == t) <= m
    for v in range(n):
        for w in succ[v]:
            assert slot[v] < slot[w]


def brute_opt(succ, m):
    """Least makespan of unit jobs under precedence, by breadth-first search over done sets."""
    n = len(succ)
    predm = [0] * n
    for v in range(n):
        for w in succ[v]:
            predm[w] |= 1 << v
    full = (1 << n) - 1
    frontier, t = {0}, 0
    while full not in frontier:
        t += 1
        nxt = set()
        for done in frontier:
            av = [v for v in range(n) if not done >> v & 1 and predm[v] & done == predm[v]]
            for c in itertools.combinations(av, min(m, len(av))):
                nxt.add(done | sum(1 << v for v in c))
        frontier = nxt
    return t


def random_dag(rng, n, p):
    perm = list(range(n))
    rng.shuffle(perm)
    succ = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                succ[perm[i]].add(perm[j])
    return succ


def reach_sets(succ):
    n = len(succ)
    out = []
    for v in range(n):
        seen, stack = set(), list(succ[v])
        while stack:
            w = stack.pop()
            if w not in seen:
                seen.add(w)
                stack.extend(succ[w])
        out.append(seen)
    return out


def test_page_example():
    succ = [{5}, {3}, {3, 4, 5}, set(), set(), set()]
    assert coffman_graham_labels(transitive_reduction(succ)) == [5, 4, 6, 1, 2, 3]
    slot = coffman_graham(succ, 2)
    check_feasible(succ, 2, slot)
    assert slot == [1, 2, 1, 3, 3, 2]
    assert max(slot) == brute_opt(succ, 2) == 3


def test_three_machine_gap():
    succ = [{7}, set(), {3}, {1, 6, 8}, {1, 8}, {1, 6, 8}, set(), set(), set()]
    assert coffman_graham_labels(transitive_reduction(succ)) == [5, 1, 9, 7, 6, 8, 2, 3, 4]
    slot = coffman_graham(succ, 3)
    check_feasible(succ, 3, slot)
    assert max(slot) == 4
    assert brute_opt(succ, 3) == 3


def test_transitive_reduction():
    rng = random.Random(5)
    for _ in range(200):
        succ = random_dag(rng, rng.randint(1, 9), 0.4)
        red = transitive_reduction(succ)
        assert reach_sets(red) == reach_sets(succ)
        for v in range(len(succ)):
            assert red[v] <= succ[v]
            for w in red[v]:
                smaller = [set(s) for s in red]
                smaller[v].discard(w)
                assert w not in reach_sets(smaller)[v]


def test_labels_decrease_along_arcs():
    rng = random.Random(9)
    for _ in range(200):
        succ = random_dag(rng, rng.randint(1, 10), 0.35)
        label = coffman_graham_labels(transitive_reduction(succ))
        assert sorted(label) == list(range(1, len(succ) + 1))
        for v in range(len(succ)):
            for w in succ[v]:
                assert label[v] > label[w]


def test_optimal_on_two_machines():
    rng = random.Random(2024)
    for _ in range(400):
        n = rng.randint(1, 9)
        succ = random_dag(rng, n, rng.choice([0.15, 0.3, 0.5]))
        slot = coffman_graham(succ, 2)
        check_feasible(succ, 2, slot)
        assert max(slot) == brute_opt(succ, 2)


def test_ratio_on_more_machines():
    rng = random.Random(31)
    for _ in range(250):
        n = rng.randint(1, 9)
        m = rng.randint(3, 4)
        succ = random_dag(rng, n, rng.choice([0.15, 0.3]))
        slot = coffman_graham(succ, m)
        check_feasible(succ, m, slot)
        opt = brute_opt(succ, m)
        assert opt <= max(slot) <= (2 - Fraction(2, m)) * opt


def test_edges():
    assert coffman_graham([], 2) == []
    assert coffman_graham([set()], 2) == [1]
    assert coffman_graham([{1}, {2}, set()], 2) == [1, 2, 3]
    assert max(coffman_graham([set()] * 5, 2)) == 3
    assert coffman_graham([{1}, {2}, set()], 1) == [1, 2, 3]
    with pytest.raises(ValueError):
        coffman_graham([{1}, {0}], 2)
    with pytest.raises(ValueError):
        coffman_graham([set()], 0)
