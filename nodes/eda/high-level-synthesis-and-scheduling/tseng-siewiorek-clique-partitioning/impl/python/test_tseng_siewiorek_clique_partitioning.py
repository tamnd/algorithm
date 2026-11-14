# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tseng-siewiorek-clique-partitioning/. The authors are listed in prov/FCVE23.jsonl.

import random

from tseng_siewiorek_clique_partitioning import (depth, interval_compatibility, is_clique_partition,
                                                 merge_trace, min_clique_partition, tseng_siewiorek)

# The lifetimes of the example on the page, in the order a, b, c, d, e, f, g.
LIFETIMES = [(1, 2), (1, 1), (2, 3), (3, 5), (4, 4), (5, 5), (2, 3)]
# Interval lifetimes on which the greedy needs 5 registers and 4 suffice.
BAD_INTERVALS = [(0, 0), (0, 2), (1, 1), (1, 3), (1, 3), (2, 4), (3, 3), (4, 4)]
# The net: a triangle with one pendant vertex on each corner.
NET = [(0, 1), (0, 2), (0, 5), (1, 2), (1, 4), (2, 3)]


def brute_min_partition(n: int, edges: list[tuple[int, int]]) -> int:
    """The least number of cliques, by trying every map of the vertices to labels."""
    adj = {(min(u, v), max(u, v)) for u, v in edges}
    best = n
    for k in range(1, n + 1):
        def place(v: int, label: list[int]) -> bool:
            if v == n:
                return True
            for c in range(min(k, max(label, default=-1) + 2)):
                if all((min(u, v), max(u, v)) in adj for u in range(v) if label[u] == c):
                    if place(v + 1, label + [c]):
                        return True
            return False
        if place(0, []):
            return k
    return best


def maximal(n: int, edges: list[tuple[int, int]], parts: list[list[int]]) -> bool:
    """True when no two parts could be joined into one larger clique."""
    adj = {(min(u, v), max(u, v)) for u, v in edges}
    for a in range(len(parts)):
        for b in range(a + 1, len(parts)):
            if all((min(x, y), max(x, y)) in adj for x in parts[a] for y in parts[b]):
                return False
    return True


def test_page_example():
    n = len(LIFETIMES)
    edges = interval_compatibility(LIFETIMES)
    assert merge_trace(n, edges) == [(4, 5, 4, 5), (1, 4, 2, 5), (0, 3, 0, 1), (1, 2, 0, 2)]
    assert tseng_siewiorek(n, edges) == [[0, 3], [1, 2, 4, 5], [6]]
    assert depth(LIFETIMES) == 3


def sizes_over_all_tie_orders(n: int, edges: list[tuple[int, int]]) -> set[int]:
    """The numbers of cliques the greedy can end with, over every way of breaking ties in (common, deleted)."""
    start = {v: frozenset() for v in range(n)}
    for u, v in edges:
        start[u] = start[u] | {v}
        start[v] = start[v] | {u}
    out: set[int] = set()

    def run(nbr: dict[int, frozenset]) -> None:
        pairs = [(i, j) for i in nbr for j in nbr[i] if i < j]
        if not pairs:
            out.add(len(nbr))
            return
        def key(p):
            c = len(nbr[p[0]] & nbr[p[1]])
            return (-c, len(nbr[p[0]]) + len(nbr[p[1]]) - 1 - c)
        best = min(key(p) for p in pairs)
        for i, j in pairs:
            if key((i, j)) != best:
                continue
            keep = (nbr[i] & nbr[j]) - {i, j}
            nxt = {x: s - {i, j} for x, s in nbr.items() if x != j}
            nxt[i] = keep
            for x in keep:
                nxt[x] = nxt[x] | {i}
            run(nxt)

    run(start)
    return out


def test_interval_counterexample():
    edges = interval_compatibility(BAD_INTERVALS)
    assert merge_trace(8, edges) == [(0, 7, 4, 7), (2, 6, 1, 4), (0, 2, 0, 3)]
    parts = tseng_siewiorek(8, edges)
    assert is_clique_partition(8, edges, parts)
    assert len(parts) == 5
    assert depth(BAD_INTERVALS) == 4
    assert min_clique_partition(8, edges) == 4
    assert sizes_over_all_tie_orders(8, edges) == {5}


def test_net_counterexample():
    parts = tseng_siewiorek(6, NET)
    assert parts == [[0, 1, 2], [3], [4], [5]]
    assert min_clique_partition(6, NET) == 3


def test_subset_dp_matches_label_search():
    rng = random.Random(7)
    for _ in range(300):
        n = rng.randint(1, 7)
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < 0.5]
        assert min_clique_partition(n, edges) == brute_min_partition(n, edges)


def test_random_graphs_measured_against_optimum():
    rng = random.Random(1)
    gaps: dict[int, int] = {}
    for _ in range(1000):
        n = rng.randint(2, 9)
        p = rng.choice([0.3, 0.5, 0.7])
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if rng.random() < p]
        parts = tseng_siewiorek(n, edges)
        assert is_clique_partition(n, edges, parts)
        assert maximal(n, edges, parts)
        gap = len(parts) - min_clique_partition(n, edges)
        assert gap >= 0
        gaps[gap] = gaps.get(gap, 0) + 1
    assert gaps == {0: 989, 1: 11}


def test_all_small_graphs():
    fails = {}
    for n in (1, 2, 3, 4, 5, 6):
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        fails[n] = 0
        for mask in range(1 << len(pairs)):
            edges = [pairs[k] for k in range(len(pairs)) if mask >> k & 1]
            parts = tseng_siewiorek(n, edges)
            assert is_clique_partition(n, edges, parts)
            if len(parts) > min_clique_partition(n, edges):
                fails[n] += 1
    assert fails == {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 180}


def test_interval_classes_where_greedy_is_optimal():
    rng = random.Random(3)
    for _ in range(500):
        horizon = rng.randint(4, 12)
        # Short lifetimes that never overlap, plus long ones that span the whole horizon.
        cuts = sorted(rng.sample(range(horizon), rng.randint(1, horizon // 2)))
        short = [(c, c) for c in cuts]
        long = [(0, horizon - 1)] * rng.randint(0, 3)
        lifetimes = short + long
        rng.shuffle(lifetimes)
        n = len(lifetimes)
        edges = interval_compatibility(lifetimes)
        parts = tseng_siewiorek(n, edges)
        assert is_clique_partition(n, edges, parts)
        assert len(parts) == depth(lifetimes) == min_clique_partition(n, edges)
    for _ in range(500):
        # A compatibility graph that is a disjoint union of cliques.
        n = rng.randint(1, 10)
        label = [rng.randrange(4) for _ in range(n)]
        edges = [(u, v) for u in range(n) for v in range(u + 1, n) if label[u] == label[v]]
        assert len(tseng_siewiorek(n, edges)) == len(set(label))


def test_random_interval_instances_measured():
    rng = random.Random(2)
    matched = 0
    for _ in range(1000):
        n = rng.randint(2, 9)
        horizon = rng.randint(3, 8)
        lifetimes = []
        for _ in range(n):
            a = rng.randrange(horizon)
            lifetimes.append((a, rng.randrange(a, horizon)))
        edges = interval_compatibility(lifetimes)
        parts = tseng_siewiorek(n, edges)
        assert is_clique_partition(n, edges, parts)
        assert len(parts) >= depth(lifetimes)
        matched += len(parts) == depth(lifetimes)
    assert matched == 1000
