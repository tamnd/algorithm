# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-separation-query/. The authors are listed in prov/W0ZM3T.jsonl.

import itertools
import random

import pytest

from d_separation_query import d_separated, reachable


def all_dags(n):
    pairs = list(itertools.combinations(range(n), 2))
    for choice in itertools.product(range(3), repeat=len(pairs)):
        edges = []
        for (a, b), c in zip(pairs, choice):
            if c == 1:
                edges.append((a, b))
            elif c == 2:
                edges.append((b, a))
        if is_acyclic(n, edges):
            yield edges


def is_acyclic(n, edges):
    indeg = [0] * n
    for _, v in edges:
        indeg[v] += 1
    stack = [v for v in range(n) if indeg[v] == 0]
    count = 0
    while stack:
        u = stack.pop()
        count += 1
        for a, b in edges:
            if a == u:
                indeg[b] -= 1
                if indeg[b] == 0:
                    stack.append(b)
    return count == n


def random_dag(n, p, rng):
    order = list(range(n))
    rng.shuffle(order)
    return [(order[i], order[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < p]


def descendants(n, edges, v):
    out, stack = set(), [v]
    while stack:
        u = stack.pop()
        for a, b in edges:
            if a == u and b not in out:
                out.add(b)
                stack.append(b)
    return out


def simple_paths(n, edges, x, y):
    nbr = [set() for _ in range(n)]
    for a, b in edges:
        nbr[a].add(b)
        nbr[b].add(a)
    stack = [[x]]
    while stack:
        path = stack.pop()
        if path[-1] == y:
            yield path
            continue
        for w in nbr[path[-1]]:
            if w not in path:
                stack.append(path + [w])


def brute_force(n, edges, xs, ys, zs):
    """d-separation by the definition: every simple path is blocked."""
    es = set(edges)
    desc = [descendants(n, edges, v) for v in range(n)]
    for x in xs:
        for y in ys:
            for path in simple_paths(n, edges, x, y):
                if all(not blocked(path, i, es, zs, desc) for i in range(1, len(path) - 1)):
                    return False
    return True


def blocked(path, i, es, zs, desc):
    a, v, b = path[i - 1], path[i], path[i + 1]
    if (a, v) in es and (b, v) in es:          # collider
        return v not in zs and not (desc[v] & zs)
    return v in zs                             # chain or fork


def subsets(items):
    for r in range(len(items) + 1):
        yield from itertools.combinations(items, r)


def test_number_of_dags():
    assert [sum(1 for _ in all_dags(n)) for n in range(1, 5)] == [1, 3, 25, 543]


def test_worked_example():
    # A=0, B=1, C=2, D=3, E=4 with A->B, A->C, B->D, C->D, D->E.
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
    assert d_separated(5, edges, {1}, {2}, {0})
    assert not d_separated(5, edges, {1}, {2}, {0, 4})
    assert not d_separated(5, edges, {1}, {2}, {0, 3})
    assert not d_separated(5, edges, {1}, {2}, set())
    assert d_separated(5, edges, {0}, {4}, {3})
    assert reachable(5, edges, {1}, {0, 4}) == {1, 2, 3}


def test_all_dags_up_to_four_nodes_all_queries():
    for n in range(1, 5):
        for edges in all_dags(n):
            for x, y in itertools.permutations(range(n), 2):
                rest = [v for v in range(n) if v not in (x, y)]
                for z in subsets(rest):
                    zs = set(z)
                    assert d_separated(n, edges, {x}, {y}, zs) == brute_force(n, edges, {x}, {y}, zs)


def test_sample_of_five_node_dags_all_single_queries():
    rng = random.Random(5)
    dags = list(all_dags(5))
    for edges in rng.sample(dags, 400):
        for x, y in itertools.combinations(range(5), 2):
            rest = [v for v in range(5) if v not in (x, y)]
            for z in subsets(rest):
                zs = set(z)
                assert d_separated(5, edges, {x}, {y}, zs) == brute_force(5, edges, {x}, {y}, zs)


def test_set_queries_on_random_dags():
    rng = random.Random(7)
    for _ in range(400):
        n = rng.randint(2, 7)
        edges = random_dag(n, rng.random(), rng)
        labels = [rng.randrange(4) for _ in range(n)]
        xs = {v for v in range(n) if labels[v] == 0}
        ys = {v for v in range(n) if labels[v] == 1}
        zs = {v for v in range(n) if labels[v] == 2}
        if xs and ys:
            assert d_separated(n, edges, xs, ys, zs) == brute_force(n, edges, xs, ys, zs)


def test_symmetry_and_disjointness():
    rng = random.Random(11)
    for _ in range(200):
        n = rng.randint(2, 6)
        edges = random_dag(n, 0.5, rng)
        x, y = rng.sample(range(n), 2)
        zs = {v for v in range(n) if v not in (x, y) and rng.random() < 0.4}
        assert d_separated(n, edges, {x}, {y}, zs) == d_separated(n, edges, {y}, {x}, zs)
    with pytest.raises(ValueError):
        d_separated(3, [(0, 1)], {0}, {1}, {1})


def test_parents_of_the_later_node_separate_a_non_adjacent_pair():
    for n in range(2, 5):
        for edges in all_dags(n):
            es = set(edges)
            for x, y in itertools.permutations(range(n), 2):
                if (x, y) in es or (y, x) in es:
                    assert not d_separated(n, edges, {x}, {y}, set(z for z in range(n) if z not in (x, y)))
                elif y not in descendants(n, edges, x):
                    pa = {u for u, v in edges if v == x}
                    assert d_separated(n, edges, {x}, {y}, pa)


def test_long_chain_is_linear_and_iterative():
    n = 20000
    edges = [(i, i + 1) for i in range(n - 1)]
    assert not d_separated(n, edges, {0}, {n - 1}, set())
    assert d_separated(n, edges, {0}, {n - 1}, {n // 2})
