# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cutset-conditioning/. The authors are listed in prov/T6CQTJ.jsonl.

import itertools
import random

import pytest

from cutset_conditioning import cutset_count, cutset_solve, directed, find_cycle_cutset

WA, NT, SA, Q, NSW, V, T = range(7)
AUSTRALIA = [(WA, NT), (WA, SA), (NT, SA), (NT, Q), (SA, Q), (SA, NSW), (SA, V), (Q, NSW), (NSW, V)]


def solutions(domains, cons):
    rel = directed(cons)
    return [t for t in itertools.product(*[sorted(d) for d in domains])
            if all((t[i], t[j]) in r for (i, j), r in rel.items())]


def is_forest(n, edges, removed) -> bool:
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, j in edges:
        if i in removed or j in removed:
            continue
        a, b = find(i), find(j)
        if a == b:
            return False
        parent[a] = b
    return True


def test_australia() -> None:
    ne = {(a, b) for a in range(3) for b in range(3) if a != b}
    cons = {e: ne for e in AUSTRALIA}
    doms = [set(range(3))] * 7
    assert find_cycle_cutset(7, cons) == [SA]
    assert cutset_count(doms, cons, [SA]) == 18
    sol = cutset_solve(doms, cons, [SA])
    assert sol == [1, 2, 0, 1, 2, 1, 0]


def test_edges() -> None:
    assert cutset_solve([], {}) == []
    assert cutset_count([], {}) == 1
    assert cutset_count([{0, 1}, set()], {}) == 0
    assert cutset_solve([{0}, {0}], {(0, 1): set()}) is None
    ne = {(0, 1), (1, 0)}
    with pytest.raises(ValueError):
        cutset_count([{0, 1}] * 3, {(0, 1): ne, (1, 2): ne, (0, 2): ne}, [])


def test_random_against_brute_force() -> None:
    rng = random.Random(8)
    for _ in range(300):
        n, d = rng.randint(1, 7), rng.randint(1, 3)
        domains = [{a for a in range(d) if rng.random() > 0.1} for _ in range(n)]
        density = rng.random()
        cons = {(i, j): {(a, b) for a in range(d) for b in range(d) if rng.random() > 0.4}
                for i, j in itertools.combinations(range(n), 2) if rng.random() < density}
        cut = find_cycle_cutset(n, cons)
        assert is_forest(n, list(cons), set(cut))
        sols = solutions(domains, cons)
        extra = sorted(set(cut) | {v for v in range(n) if rng.random() < 0.2})
        for c in (cut, extra):
            assert cutset_count(domains, cons, c) == len(sols)
            got = cutset_solve(domains, cons, c)
            if sols:
                assert got is not None and tuple(got) in set(sols)
            else:
                assert got is None
