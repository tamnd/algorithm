# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/elimination-ordering/. The authors are listed in prov/BG2816.jsonl.

import random
from itertools import combinations, permutations

import pytest

from elimination_ordering import (eliminate, exact_min_width, induced_width,
                                  min_degree_order, min_fill_order)


def grid(r, c):
    edges = []
    for i in range(r):
        for j in range(c):
            v = i * c + j
            if j + 1 < c:
                edges.append((v, v + 1))
            if i + 1 < r:
                edges.append((v, v + c))
    return r * c, edges


def is_chordal_by_definition(n, es):
    """No induced cycle of length 4 or more (checked on every vertex subset)."""
    for k in range(4, n + 1):
        for sub in combinations(range(n), k):
            s = set(sub)
            deg = {v: [u for u in s if frozenset((u, v)) in es] for v in s}
            if any(len(x) != 2 for x in deg.values()):
                continue
            # all degrees 2: a union of cycles; induced cycle if connected
            seen, stack = {sub[0]}, [sub[0]]
            while stack:
                x = stack.pop()
                for y in deg[x]:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
            if len(seen) == k:
                return False
    return True


def clique_number(n, es):
    best = 1 if n else 0
    for k in range(2, n + 1):
        if any(all(frozenset(p) in es for p in combinations(sub, 2)) for sub in combinations(range(n), k)):
            best = k
        else:
            break
    return best


def treewidth_by_chordal_completion(n, edges):
    """min over chordal supergraphs H of (clique number of H) - 1."""
    es = {frozenset(e) for e in edges}
    missing = [frozenset(p) for p in combinations(range(n), 2) if frozenset(p) not in es]
    best = n - 1
    for mask in range(1 << len(missing)):
        h = es | {missing[i] for i in range(len(missing)) if mask >> i & 1}
        if is_chordal_by_definition(n, h):
            best = min(best, clique_number(n, h) - 1)
    return best


def brute_min_width(n, edges):
    return min(induced_width(n, edges, p) for p in permutations(range(n)))


def random_graph(rng, n, p):
    return [e for e in combinations(range(n), 2) if rng.random() < p]


def test_small_cases():
    assert exact_min_width(0, [])[0] == 0
    assert exact_min_width(1, [])[0] == 0
    assert exact_min_width(4, [(0, 1), (1, 2), (2, 3)])[0] == 1
    assert exact_min_width(4, [(0, 1), (1, 2), (2, 3), (3, 0)])[0] == 2
    assert exact_min_width(5, list(combinations(range(5), 2)))[0] == 4
    n, e = grid(3, 3)
    assert exact_min_width(n, e)[0] == 3


def test_star_order_matters():
    star = [(0, i) for i in range(1, 6)]
    assert induced_width(6, star, [0, 1, 2, 3, 4, 5]) == 5
    assert induced_width(6, star, [1, 2, 3, 4, 5, 0]) == 1
    assert induced_width(6, star, min_degree_order(6, star)) == 1
    assert induced_width(6, star, min_fill_order(6, star)) == 1


def test_grid_heuristics():
    n, e = grid(3, 3)
    assert induced_width(n, e, min_degree_order(n, e)) == 3
    assert eliminate(n, e, min_fill_order(n, e)) == (3, [(1, 3), (1, 5), (3, 5), (3, 7), (5, 7)])


def test_page_examples_where_one_heuristic_loses():
    a = [(0, 5), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 3), (2, 5), (2, 7), (3, 6), (5, 6), (6, 7)]
    assert exact_min_width(8, a)[0] == 3
    assert induced_width(8, a, min_degree_order(8, a)) == 4
    assert induced_width(8, a, min_fill_order(8, a)) == 3
    b = [(0, 1), (0, 5), (0, 8), (1, 2), (1, 4), (1, 5), (1, 7), (1, 8), (2, 6), (3, 5), (3, 7),
         (4, 8), (6, 8), (6, 9), (8, 9)]
    assert exact_min_width(10, b)[0] == 2
    assert induced_width(10, b, min_degree_order(10, b)) == 2
    assert induced_width(10, b, min_fill_order(10, b)) == 3


def test_bad_order():
    with pytest.raises(ValueError):
        eliminate(3, [(0, 1)], [0, 1])
    with pytest.raises(ValueError):
        eliminate(3, [], [0, 0, 1])


def test_exact_equals_all_orders_and_heuristics_never_better():
    rng = random.Random(31)
    for _ in range(500):
        n = rng.randint(1, 6)
        edges = random_graph(rng, n, rng.choice([0.3, 0.5, 0.7]))
        w, order = exact_min_width(n, edges)
        assert induced_width(n, edges, order) == w
        if n <= 5 or _ % 5 == 0:
            assert w == brute_min_width(n, edges)
        assert induced_width(n, edges, min_degree_order(n, edges)) >= w
        assert induced_width(n, edges, min_fill_order(n, edges)) >= w


def test_exact_equals_treewidth():
    rng = random.Random(5)
    done = 0
    while done < 40:
        n = rng.randint(3, 7)
        edges = random_graph(rng, n, 0.6)
        missing = n * (n - 1) // 2 - len(edges)
        if missing > 9:
            continue
        done += 1
        assert exact_min_width(n, edges)[0] == treewidth_by_chordal_completion(n, edges)


def test_chordal_graph_perfect_order_and_min_fill():
    rng = random.Random(11)
    for _ in range(300):
        n = rng.randint(1, 8)
        edges = random_graph(rng, n, 0.3)
        order = list(range(n))
        rng.shuffle(order)
        width, fill = eliminate(n, edges, order)
        chordal = edges + fill  # chordal, and order is a perfect elimination ordering of it
        w2, fill2 = eliminate(n, chordal, order)
        assert fill2 == [] and w2 == width
        assert eliminate(n, chordal, min_fill_order(n, chordal))[1] == []
        es = {frozenset(e) for e in chordal}
        if n <= 7:
            assert is_chordal_by_definition(n, es)
            assert exact_min_width(n, chordal)[0] == clique_number(n, es) - 1
