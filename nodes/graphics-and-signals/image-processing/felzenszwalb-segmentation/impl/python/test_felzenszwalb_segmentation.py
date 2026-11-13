# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/felzenszwalb-segmentation/. The authors are listed in prov/SE60TX.jsonl.

import random
from fractions import Fraction

import pytest

from felzenszwalb_segmentation import grid_edges, relabel, segment_graph, segment_image

EXAMPLE = [
    [10, 11, 30, 31],
    [12, 10, 33, 30],
]

INF = float("inf")


# Direct definitions from the paper, computed from scratch on explicit sets.

def mst_max_edge(nodes, edges):
    """Int(C): the largest weight of a minimum spanning tree of C (Kruskal on C)."""
    if len(nodes) == 1:
        return 0
    inside = sorted((w, u, v) for w, u, v in edges if u in nodes and v in nodes)
    parent = {v: v for v in nodes}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    largest, joined = None, 0
    for w, u, v in inside:
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            largest, joined = w, joined + 1
    assert joined == len(nodes) - 1, "a component must be connected"
    return largest


def dif(c1, c2, edges):
    """Dif(C1, C2): the smallest weight of an edge between the two sets."""
    ws = [w for w, u, v in edges if (u in c1 and v in c2) or (u in c2 and v in c1)]
    return min(ws) if ws else INF


def m_int(c1, c2, edges, k):
    return min(mst_max_edge(c1, edges) + Fraction(k, len(c1)), mst_max_edge(c2, edges) + Fraction(k, len(c2)))


def boundary(c1, c2, edges, k):
    """The pairwise predicate D(C1, C2): true when there is evidence for a boundary."""
    return dif(c1, c2, edges) > m_int(c1, c2, edges, k)


def reference(n, edges, k):
    """Algorithm 1 with explicit sets and the predicate evaluated from scratch."""
    comps = [frozenset([v]) for v in range(n)]
    for w, u, v in sorted(edges, key=lambda e: e[0]):
        cu = next(c for c in comps if u in c)
        cv = next(c for c in comps if v in c)
        if cu is not cv and not boundary(cu, cv, edges, k):
            comps = [c for c in comps if c is not cu and c is not cv] + [cu | cv]
    return comps


def as_sets(comp):
    groups = {}
    for v, c in enumerate(comp):
        groups.setdefault(c, set()).add(v)
    return {frozenset(g) for g in groups.values()}


def random_graph(rng, n, p, wmax):
    edges = []
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < p:
                edges.append((rng.randint(0, wmax), u, v))
    return edges


def connected(nodes, edges):
    nodes = set(nodes)
    start = next(iter(nodes))
    seen, stack = {start}, [start]
    while stack:
        x = stack.pop()
        for w, u, v in edges:
            for a, b in ((u, v), (v, u)):
                if a == x and b in nodes and b not in seen:
                    seen.add(b)
                    stack.append(b)
    return seen == nodes


def partitions(items):
    """All set partitions of a list (Bell number many)."""
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in partitions(rest):
        for i in range(len(p)):
            yield p[:i] + [p[i] | {first}] + p[i + 1:]
        yield p + [frozenset([first])]


def not_too_fine(segs, edges, k):
    segs = list(segs)
    for i in range(len(segs)):
        for j in range(i + 1, len(segs)):
            if dif(segs[i], segs[j], edges) < INF and not boundary(segs[i], segs[j], edges, k):
                return False
    return True


def proper_refinements(segs, edges):
    """Every proper refinement of segs into connected parts."""
    segs = list(segs)
    choices = []
    for c in segs:
        opts = [p for p in partitions(sorted(c)) if all(connected(part, edges) for part in p)]
        choices.append(opts)

    def rec(i, acc):
        if i == len(segs):
            yield acc
            return
        for p in choices[i]:
            yield from rec(i + 1, acc + p)

    for t in rec(0, []):
        if len(t) > len(segs):
            yield t


def test_example():
    lab = segment_image(EXAMPLE, 10, connectivity=4)
    assert lab == [[0, 0, 1, 1], [0, 0, 1, 1]]
    # With k = 1 the edges of weight 2 and 3 are rejected.
    assert segment_image(EXAMPLE, 1, connectivity=4) == [[0, 0, 1, 1], [2, 0, 3, 1]]
    # The step of 19 is merged once 2 + k/4 >= 19, that is k >= 68.
    assert segment_image(EXAMPLE, 67, connectivity=4) == [[0, 0, 1, 1], [0, 0, 1, 1]]
    assert segment_image(EXAMPLE, 68, connectivity=4) == [[0, 0, 0, 0], [0, 0, 0, 0]]


@pytest.mark.parametrize("seed", range(4))
def test_against_direct_predicate(seed):
    rng = random.Random(2004 + seed)
    for _ in range(150):
        n = rng.randint(1, 8)
        edges = random_graph(rng, n, rng.choice([0.3, 0.5, 0.8]), rng.choice([3, 10, 40]))
        k = rng.choice([0, 1, 3, Fraction(7, 2), 10, 30])
        got = as_sets(segment_graph(n, edges, k))
        assert got == set(reference(n, edges, k))


def test_not_too_fine_and_not_too_coarse():
    rng = random.Random(59)
    for _ in range(120):
        n = rng.randint(1, 6)
        edges = random_graph(rng, n, 0.6, 9)
        k = rng.choice([0, 1, 2, 5, 12])
        segs = as_sets(segment_graph(n, edges, k))
        for c in segs:
            assert connected(c, edges)
        assert not_too_fine(segs, edges, k)
        assert not any(not_too_fine(t, edges, k) for t in proper_refinements(segs, edges))


def test_order_of_equal_weights_does_not_matter():
    rng = random.Random(167)
    for _ in range(300):
        n = rng.randint(2, 9)
        edges = random_graph(rng, n, 0.6, 3)  # many ties
        k = rng.choice([1, 2, 4, Fraction(5, 2)])
        base = as_sets(segment_graph(n, edges, k))
        for _ in range(5):
            shuffled = edges[:]
            rng.shuffle(shuffled)
            shuffled = [(w, v, u) if rng.random() < 0.5 else (w, u, v) for w, u, v in shuffled]
            assert as_sets(segment_graph(n, shuffled, k)) == base


def test_k_zero_gives_zero_weight_components():
    rng = random.Random(8)
    for _ in range(100):
        img = [[rng.randint(0, 2) for _ in range(5)] for _ in range(4)]
        # With k = 0 the components are the connected sets of equal value:
        # only edges of weight 0 can merge.
        lab = segment_image(img, 0, connectivity=4)
        for y in range(4):
            for x in range(5):
                for dx, dy in ((1, 0), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if nx < 5 and ny < 4 and img[y][x] == img[ny][nx]:
                        assert lab[y][x] == lab[ny][nx]
        edges = grid_edges(img, 4)
        zero = [(w, u, v) for w, u, v in edges if w == 0]
        assert as_sets(segment_graph(20, edges, 0)) == as_sets(segment_graph(20, zero, 0))


def test_min_size_postprocessing():
    img = [[0, 0, 0, 0], [0, 50, 0, 0], [0, 0, 0, 90]]
    lab = segment_image(img, 1, connectivity=4)
    assert len({v for row in lab for v in row}) == 3
    merged = segment_image(img, 1, connectivity=4, min_size=2)
    assert len({v for row in merged for v in row}) == 1


def test_color_and_relabel():
    img = [[(0, 0, 0), (3, 4, 0)], [(100, 0, 0), (100, 0, 0)]]
    lab = segment_image(img, 6, connectivity=4)
    assert lab == [[0, 0], [1, 1]]
    assert relabel([5, 5, 2, 9, 2]) == [0, 0, 1, 2, 1]
    with pytest.raises(ValueError):
        grid_edges(img, 6)
