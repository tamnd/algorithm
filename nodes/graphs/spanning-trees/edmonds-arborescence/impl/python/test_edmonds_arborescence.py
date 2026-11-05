# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/edmonds-arborescence/. The authors are listed in prov/04S04K.jsonl.

import itertools
import random

from edmonds_arborescence import edmonds_arborescence

# r = 0, a = 1, b = 2, c = 3: ra 5, rb 6, ab 1, ba 2, ac 4, bc 3, rc 10.
EXAMPLE = [(0, 1, 5), (0, 2, 6), (1, 2, 1), (2, 1, 2), (1, 3, 4), (2, 3, 3), (0, 3, 10)]


def is_arborescence(n, arcs, root, chosen):
    """Check that chosen has one arc into each non-root vertex and reaches all."""
    parent = {}
    for i in chosen:
        u, v, _ = arcs[i]
        if v == root or v in parent or u == v:
            return False
        parent[v] = u
    if len(parent) != n - 1:
        return False
    for v in range(n):
        seen = set()
        while v != root:
            if v in seen:
                return False
            seen.add(v)
            v = parent[v]
    return True


def cost(arcs, chosen):
    return sum(arcs[i][2] for i in chosen)


def brute_force(n, arcs, root):
    """Least cost over all choices of one entering arc per vertex, or None."""
    options = []
    for v in range(n):
        if v == root:
            continue
        into = [i for i, (a, b, _) in enumerate(arcs) if b == v and a != v]
        if not into:
            return None
        options.append(into)
    best = None
    for pick in itertools.product(*options):
        if is_arborescence(n, arcs, root, pick):
            c = cost(arcs, pick)
            if best is None or c < best:
                best = c
    return best


def random_graph(rng, n, m, lo, hi):
    return [(rng.randrange(n), rng.randrange(n), rng.randint(lo, hi)) for _ in range(m)]


def test_example():
    assert edmonds_arborescence(4, EXAMPLE, 0) == [0, 2, 5]
    assert cost(EXAMPLE, [0, 2, 5]) == 9


def test_prim_like_growth_fails():
    arcs = [(0, 1, 2), (0, 2, 3), (2, 1, 1)]
    assert edmonds_arborescence(3, arcs, 0) == [1, 2]


def test_single_vertex():
    assert edmonds_arborescence(1, [], 0) == []
    assert edmonds_arborescence(1, [(0, 0, 5)], 0) == []


def test_unreachable_vertex():
    assert edmonds_arborescence(2, [], 0) is None
    assert edmonds_arborescence(3, [(0, 1, 1), (2, 1, 1)], 0) is None
    # Vertices 1 and 2 feed each other but the root reaches neither.
    assert edmonds_arborescence(3, [(1, 2, 1), (2, 1, 1)], 0) is None


def test_unreachable_after_contraction():
    # Every vertex has an entering arc, but the cycle 1, 2 has no arc from outside.
    assert edmonds_arborescence(4, [(0, 3, 1), (1, 2, 1), (2, 1, 1), (3, 3, 1)], 0) is None


def test_ties_choose_smaller_index():
    arcs = [(0, 1, 1), (0, 1, 1), (0, 2, 1), (1, 2, 1)]
    assert edmonds_arborescence(3, arcs, 0) == [0, 2]


def test_negative_costs_and_self_loops():
    arcs = [(0, 1, -3), (1, 1, -100), (1, 2, -1), (0, 2, 4), (2, 0, -50)]
    assert edmonds_arborescence(3, arcs, 0) == [0, 2]


def test_nested_cycles():
    # Cycle 1 -> 2 -> 3 -> 1 and, after it is contracted, a second cycle with 4.
    arcs = [(1, 2, 1), (2, 3, 1), (3, 1, 1), (4, 1, 1), (3, 4, 1), (0, 4, 10), (0, 2, 20)]
    got = edmonds_arborescence(5, arcs, 0)
    assert is_arborescence(5, arcs, 0, got)
    assert cost(arcs, got) == brute_force(5, arcs, 0) == 13


def test_other_root():
    for root in range(4):
        got = edmonds_arborescence(4, EXAMPLE, root)
        want = brute_force(4, EXAMPLE, root)
        assert (got is None) == (want is None)
        if got is not None:
            assert cost(EXAMPLE, got) == want


def test_random_against_brute_force():
    rng = random.Random(20261105)
    for trial in range(800):
        n = rng.randint(1, 5)
        m = rng.randint(0, 10)
        lo, hi = (-3, 3) if trial % 2 else (1, 4)
        arcs = random_graph(rng, n, m, lo, hi)
        root = rng.randrange(n)
        got = edmonds_arborescence(n, arcs, root)
        want = brute_force(n, arcs, root)
        if want is None:
            assert got is None
        else:
            assert got is not None and is_arborescence(n, arcs, root, got)
            assert cost(arcs, got) == want


def test_random_dense_reachable():
    rng = random.Random(7)
    for _ in range(100):
        n = rng.randint(2, 6)
        arcs = [(0, v, rng.randint(5, 9)) for v in range(1, n)]
        arcs += random_graph(rng, n, 2 * n, 0, 3)
        rng.shuffle(arcs)
        got = edmonds_arborescence(n, arcs, 0)
        assert is_arborescence(n, arcs, 0, got)
        assert cost(arcs, got) == brute_force(n, arcs, 0)
