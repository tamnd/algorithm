# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/and-or-graph-of-assembly-plans/. The authors are listed in prov/XTSFWX.jsonl.

import itertools
import random
from math import comb

from assembly_boxes import AXES6, face_contact, free_by_sampling, random_boxes
from and_or_graph_of_assembly_plans import AndOrGraph, from_boxes

# ---- independent references: every binary tree, checked on the geometry ----


def all_trees(parts):
    """Every full binary tree with the given leaves, children unordered."""
    if len(parts) == 1:
        yield parts[0]
        return
    first, rest = parts[0], parts[1:]
    for r in range(len(rest)):
        for left_rest in itertools.combinations(rest, r):
            left = (first,) + left_rest
            right = tuple(p for p in rest if p not in left_rest)
            for t1 in all_trees(left):
                for t2 in all_trees(right):
                    yield frozenset((t1, t2))


def leaves(t):
    if isinstance(t, int):
        return {t}
    a, b = tuple(t)
    return leaves(a) | leaves(b)


def connected(boxes, parts):
    parts = list(parts)
    seen = {parts[0]}
    stack = [parts[0]]
    while stack:
        u = stack.pop()
        for v in parts:
            if v not in seen and face_contact(boxes[u], boxes[v]) is not None:
                seen.add(v)
                stack.append(v)
    return len(seen) == len(parts)


def split_ok(boxes, p1, p2, motions):
    if not (connected(boxes, p1) and connected(boxes, p2)):
        return False
    b1 = [boxes[i] for i in p1]
    b2 = [boxes[i] for i in p2]
    return any(free_by_sampling(b1, b2, d) or free_by_sampling(b2, b1, d) for d in motions)


def tree_ok(boxes, t, motions, cache):
    if isinstance(t, int):
        return True
    a, b = tuple(t)
    la, lb = frozenset(leaves(a)), frozenset(leaves(b))
    key = frozenset((la, lb))
    if key not in cache:
        cache[key] = split_ok(boxes, la, lb, motions)
    return cache[key] and tree_ok(boxes, a, motions, cache) and tree_ok(boxes, b, motions, cache)


def brute_plans(boxes, motions):
    cache = {}
    return {t for t in all_trees(tuple(range(len(boxes)))) if tree_ok(boxes, t, motions, cache)}


def brute_linear_orders(boxes, motions):
    count = 0
    cache = {}
    for order in itertools.permutations(range(len(boxes))):
        ok = True
        for k in range(1, len(order)):
            key = (frozenset(order[:k]), order[k])
            if key not in cache:
                cache[key] = split_ok(boxes, order[:k], (order[k],), motions)
            if not cache[key]:
                ok = False
                break
        count += ok
    return count


def mask(parts):
    return sum(1 << p for p in parts)


EXAMPLE = [
    (0, 0, 0, 4, 2, 1),   # 0 base plate
    (0, 0, 1, 1, 2, 3),   # 1 left post
    (3, 0, 1, 4, 2, 3),   # 2 right post
    (1, 0, 1, 3, 2, 2),   # 3 block
    (0, 0, 3, 4, 2, 4),   # 4 top plate
]

# ---- tests ----


def test_plans_match_all_binary_trees():
    rng = random.Random(11)
    for trial in range(80):
        n = rng.randint(1, 5)
        boxes = random_boxes(rng, n, size=3, max_side=3, connected=rng.random() < 0.8)
        if trial % 3 == 0:
            motions = AXES6
        else:
            motions = tuple(rng.sample(AXES6, rng.randint(1, 3)))
        g = from_boxes(boxes, motions)
        brute = brute_plans(boxes, motions)
        assert set(g.plans()) == brute
        assert g.count_plans() == len(brute)


def test_six_parts():
    rng = random.Random(12)
    for _ in range(4):
        boxes = random_boxes(rng, 6, size=3, max_side=2, connected=True)
        motions = (AXES6[4], AXES6[1])
        g = from_boxes(boxes, motions)
        assert g.count_plans() == len(brute_plans(boxes, motions))


def test_linear_plans_against_all_orders():
    rng = random.Random(13)
    for trial in range(60):
        n = rng.randint(2, 5)
        boxes = random_boxes(rng, n, size=3, max_side=3, connected=rng.random() < 0.8)
        motions = AXES6 if trial % 2 else tuple(rng.sample(AXES6, 2))
        g = from_boxes(boxes, motions)
        assert 2 * g.count_linear_plans() == brute_linear_orders(boxes, motions)


def test_nodes_are_connected_and_bounded():
    rng = random.Random(14)
    for _ in range(60):
        n = rng.randint(1, 7)
        boxes = random_boxes(rng, n, size=4, max_side=2, connected=True)
        g = from_boxes(boxes)
        conn = [m for m in range(1, 1 << n)
                if connected(boxes, [i for i in range(n) if m >> i & 1])]
        assert set(g.nodes()) <= set(conn)
        assert len(g.nodes()) <= len(conn)
        for s, arcs in g.arcs.items():
            for s1, s2 in arcs:
                assert s1 | s2 == s and s1 & s2 == 0


def test_chain_counts():
    for n in range(1, 9):
        boxes = [(i, 0, 0, i + 1, 1, 1) for i in range(n)]
        g = from_boxes(boxes)
        assert len(g.nodes()) == n * (n + 1) // 2
        assert g.hyperarc_count() == comb(n + 1, 3)
        assert g.count_plans() == comb(2 * n - 2, n - 1) // n   # Catalan number C(n-1)
        assert g.count_linear_plans() == (2 ** (n - 2) if n >= 2 else 1)


def test_complete_and_free():
    for n in range(1, 9):
        full = (1 << n) - 1
        adj = [full & ~(1 << i) for i in range(n)]
        g = AndOrGraph(n, adj, lambda s1, s2: True)
        double_factorial = 1
        for k in range(1, 2 * n - 2, 2):
            double_factorial *= k
        assert g.count_plans() == double_factorial
        assert len(g.nodes()) == 2 ** n - 1
        assert g.hyperarc_count() == (3 ** n - 2 ** (n + 1) + 1) // 2


def test_example_frame():
    g = from_boxes(EXAMPLE)
    assert len(g.nodes()) == 27
    assert g.count_plans() == len(brute_plans(EXAMPLE, AXES6))
    up = from_boxes(EXAMPLE, ((0, 0, 1),))
    assert up.count_plans() == len(brute_plans(EXAMPLE, ((0, 0, 1),)))
