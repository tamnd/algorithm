# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ultrametric-contour-map/. The authors are listed in prov/6B2NMJ.jsonl.

import random
from fractions import Fraction as F

from ultrametric_contour_map import components, grid_edges, threshold, ultrametric_contour_map


def quadrant_example():
    """A 4 x 4 grid with four 2 x 2 regions A B / C D, as on the page."""
    labels = [[0, 0, 1, 1], [0, 0, 1, 1], [2, 2, 3, 3], [2, 2, 3, 3]]
    eh = [[F(0)] * 3 for _ in range(4)]
    ev = [[F(0)] * 4 for _ in range(3)]
    eh[0][1], eh[1][1] = F(2, 10), F(4, 10)  # A | B
    eh[2][1], eh[3][1] = F(6, 10), F(6, 10)  # C | D
    ev[1][0], ev[1][1] = F(9, 10), F(7, 10)  # A over C
    ev[1][2], ev[1][3] = F(5, 10), F(9, 10)  # B over D
    return labels, eh, ev


def random_case(rng, w, h, nlab):
    labels = [[rng.randrange(nlab) for _ in range(w)] for _ in range(h)]
    eh = [[F(rng.randint(0, 10), 10) for _ in range(w - 1)] for _ in range(h)]
    ev = [[F(rng.randint(0, 10), 10) for _ in range(w)] for _ in range(h - 1)]
    return labels, eh, ev


def naive_merges(labels, eh, ev):
    """Recompute every mean boundary strength from scratch before each merge."""
    h, w = len(labels), len(labels[0])
    comp, r0 = components(labels)
    region = {(u, v): comp[v][u] for v in range(h) for u in range(w)}
    nxt = r0
    merges = []
    while True:
        sums = {}
        for kind, u, v, p, q in grid_edges(w, h):
            a, b = region[p], region[q]
            if a == b:
                continue
            key = (min(a, b), max(a, b))
            s, n = sums.get(key, (0, 0))
            sums[key] = (s + (eh[v][u] if kind == 0 else ev[v][u]), n + 1)
        if not sums:
            return merges
        m, a, b = min((s / n, a, b) for (a, b), (s, n) in sums.items())
        merges.append((m, a, b, nxt))
        for p in region:
            if region[p] in (a, b):
                region[p] = nxt
        nxt += 1


def partition(lab):
    groups = {}
    for v, row in enumerate(lab):
        for u, x in enumerate(row):
            groups.setdefault(x, set()).add((u, v))
    return {frozenset(g) for g in groups.values()}


def partition_after(labels, merges, t):
    """The partition after all merges of level at most t, replayed with plain sets."""
    h, w = len(labels), len(labels[0])
    comp, _ = components(labels)
    sets = {}
    for v in range(h):
        for u in range(w):
            sets.setdefault(comp[v][u], set()).add((u, v))
    for m, a, b, c in merges:
        if m <= t:
            sets[c] = sets.pop(a) | sets.pop(b)
    return {frozenset(s) for s in sets.values()}


def test_quadrant_example():
    labels, eh, ev = quadrant_example()
    uh, uv, merges = ultrametric_contour_map(labels, eh, ev)
    assert [m for m, _, _, _ in merges] == [F(3, 10), F(3, 5), F(3, 4)]
    assert [(a, b, c) for _, a, b, c in merges] == [(0, 1, 4), (2, 3, 5), (4, 5, 6)]
    assert uh[0][1] == uh[1][1] == F(3, 10)
    assert uh[2][1] == uh[3][1] == F(3, 5)
    assert uv[1] == [F(3, 4)] * 4
    assert uh[0][0] == uv[0][0] == 0
    assert len(partition(threshold(uh, uv, F(1, 4)))) == 4
    assert len(partition(threshold(uh, uv, F(1, 2)))) == 3
    assert len(partition(threshold(uh, uv, F(7, 10)))) == 2
    assert len(partition(threshold(uh, uv, F(3, 4)))) == 1


def test_levels_do_not_decrease():
    rng = random.Random(1)
    for _ in range(40):
        labels, eh, ev = random_case(rng, 6, 5, 3)
        _, _, merges = ultrametric_contour_map(labels, eh, ev)
        levels = [m for m, _, _, _ in merges]
        assert levels == sorted(levels)
        _, r0 = components(labels)
        assert len(merges) == r0 - 1


def test_matches_naive_recompute():
    rng = random.Random(2)
    for _ in range(40):
        labels, eh, ev = random_case(rng, 5, 5, 4)
        _, _, merges = ultrametric_contour_map(labels, eh, ev)
        assert merges == naive_merges(labels, eh, ev)


def test_threshold_gives_the_partition_of_each_level():
    rng = random.Random(3)
    for _ in range(25):
        labels, eh, ev = random_case(rng, 5, 4, 3)
        uh, uv, merges = ultrametric_contour_map(labels, eh, ev)
        levels = sorted({m for m, _, _, _ in merges} | {F(0)})
        previous = None
        for t in levels:
            p = partition(threshold(uh, uv, t))
            assert p == partition_after(labels, merges, t)
            if previous is not None:
                # Nested: each region at the lower level lies inside one region here.
                assert all(any(r <= s for s in p) for r in previous)
            previous = p


def test_ultrametric_and_minimax_paths():
    rng = random.Random(4)
    for _ in range(10):
        w, h = 4, 3
        labels = [[v * w + u for u in range(w)] for v in range(h)]  # one region per pixel
        eh = [[F(rng.randint(1, 9), 10) for _ in range(w - 1)] for _ in range(h)]
        ev = [[F(rng.randint(1, 9), 10) for _ in range(w)] for _ in range(h - 1)]
        uh, uv, merges = ultrametric_contour_map(labels, eh, ev)
        n = w * h
        inf = F(10)
        d = [[F(0) if i == j else inf for j in range(n)] for i in range(n)]
        for kind, u, v, (u1, v1), (u2, v2) in grid_edges(w, h):
            val = uh[v][u] if kind == 0 else uv[v][u]
            i, j = v1 * w + u1, v2 * w + u2
            d[i][j] = d[j][i] = val
        for k in range(n):  # Floyd-Warshall with (min, max): the minimax path value
            for i in range(n):
                for j in range(n):
                    via = max(d[i][k], d[k][j])
                    if via < d[i][j]:
                        d[i][j] = via
        # The merge tree gives the same distance: the level where i and j first share a region.
        owner = list(range(n))
        tree = [[0] * n for _ in range(n)]
        for m, a, b, c in merges:
            for i in range(n):
                for j in range(n):
                    if owner[i] == a and owner[j] == b or owner[i] == b and owner[j] == a:
                        tree[i][j] = m
            owner = [c if o in (a, b) else o for o in owner]
        assert d == tree
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    assert d[i][k] <= max(d[i][j], d[j][k])


def test_edges_inside_a_region_are_zero_and_float_input_works():
    labels = [[0, 0, 1], [0, 0, 1]]
    eh = [[0.5, 0.2], [0.7, 0.4]]
    ev = [[0.9, 0.9, 0.1]]
    uh, uv, merges = ultrametric_contour_map(labels, eh, ev)
    assert uh[0][0] == uh[1][0] == 0 and uv[0] == [0, 0, 0]
    assert merges == [((0.2 + 0.4) / 2, 0, 1, 2)]
    assert abs(uh[0][1] - 0.3) < 1e-12 and abs(uh[1][1] - 0.3) < 1e-12
