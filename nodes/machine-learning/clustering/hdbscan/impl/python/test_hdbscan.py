# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hdbscan/. The authors are listed in prov/Q8SHE1.jsonl.

import itertools
import random

from hdbscan import (NOISE, condensed_tree, core_distances, euclidean, hdbscan, mst_prim,
                     mutual_reachability, select_clusters, stability)


def blobs(rng, n, centers, spread=0.6):
    return [(cx + rng.gauss(0, spread), cy + rng.gauss(0, spread))
            for cx, cy in (rng.choice(centers) for _ in range(n))]


def all_pairs(points, core):
    n = len(points)
    return [(i, j, mutual_reachability(points, core, i, j)) for i in range(n) for j in range(i + 1, n)]


def connected(n, edges):
    root = list(range(n))

    def find(x):
        while root[x] != x:
            x = root[x]
        return x

    for u, v, _ in edges:
        root[find(u)] = find(v)
    return len({find(x) for x in range(n)}) == 1


def test_mst_against_brute_force():
    rng = random.Random(1)
    for _ in range(25):
        n = rng.randrange(2, 7)
        pts = [(rng.uniform(0, 5), rng.uniform(0, 5)) for _ in range(n)]
        core = core_distances(pts, rng.randrange(1, n + 1))
        edges = mst_prim(pts, core)
        assert len(edges) == n - 1 and connected(n, edges)
        best = min(sum(w for _, _, w in t) for t in itertools.combinations(all_pairs(pts, core), n - 1)
                   if connected(n, t))
        assert abs(sum(w for _, _, w in edges) - best) < 1e-9


def components(n, present, edges, t):
    comp = {p: p for p in present}
    changed = True
    while changed:
        changed = False
        for u, v, w in edges:
            if w <= t and u in comp and v in comp and comp[u] != comp[v]:
                comp[u] = comp[v] = min(comp[u], comp[v])
                changed = True
    return comp


def test_levels_equal_dbscan_star():
    # At each level eps, the MST components over the points with core <= eps are the
    # components of the DBSCAN core graph with radius eps and MinPts = min_pts.
    rng = random.Random(2)
    for _ in range(25):
        n = rng.randrange(2, 30)
        pts = blobs(rng, n, [(0, 0), (5, 0), (2, 4)])
        m = rng.randrange(1, 5)
        core = core_distances(pts, m)
        mst = mst_prim(pts, core)
        for t in sorted({w for _, _, w in mst})[:6]:
            present = [x for x in range(n) if core[x] <= t]
            ref_core = [sum(euclidean(pts[i], q) <= t for q in pts) >= m for i in range(n)]
            assert present == [x for x in range(n) if ref_core[x]]
            a = components(n, present, mst, t)
            b = components(n, present, [(i, j, euclidean(pts[i], pts[j])) for i in present for j in present if i < j], t)
            for i in present:
                for j in present:
                    assert (a[i] == a[j]) == (b[i] == b[j])


def test_condensed_tree_from_mst_equals_from_full_graph():
    rng = random.Random(3)
    for _ in range(20):
        n = rng.randrange(2, 35)
        pts = blobs(rng, n, [(0, 0), (6, 0), (3, 5)])
        m, mcs = rng.randrange(2, 5), rng.randrange(2, 6)
        core = core_distances(pts, m)
        t1 = condensed_tree(n, mst_prim(pts, core), core, mcs)
        t2 = condensed_tree(n, all_pairs(pts, core), core, mcs)
        assert t1 == t2
        parent, birth, members, exit_lambda = t1
        for c in range(1, len(parent)):
            assert len(members[c]) >= mcs
            assert members[c] <= members[parent[c]]
            assert birth[c] > birth[parent[c]]
        for c in range(len(parent)):
            assert set(exit_lambda[c]) == members[c]
            assert all(exit_lambda[c][x] >= birth[c] for x in members[c])
            kids = [k for k in range(len(parent)) if parent[k] == c]
            for a, b in itertools.combinations(kids, 2):
                assert not members[a] & members[b]


def is_antichain(parent, nodes):
    for c in nodes:
        a = parent[c]
        while a >= 0:
            if a in nodes:
                return False
            a = parent[a]
    return True


def test_selection_against_all_antichains():
    rng = random.Random(4)
    for _ in range(300):
        m = rng.randrange(1, 10)
        parent = [-1] + [rng.randrange(c) for c in range(1, m)]
        stab = [rng.choice([0.0, 0.5, 1.0, 1.5, 2.0, 3.0]) for _ in range(m)]
        for allow in (False, True):
            cands = list(range(m)) if allow else list(range(1, m))
            want = max(sum(stab[c] for c in s)
                       for r in range(len(cands) + 1)
                       for s in itertools.combinations(cands, r) if is_antichain(parent, set(s)))
            sel, value = select_clusters(parent, stab, allow)
            assert is_antichain(parent, set(sel)) and set(sel) <= set(cands)
            assert abs(value - want) < 1e-12
            assert abs(sum(stab[c] for c in sel) - want) < 1e-12


def test_two_blobs_and_noise():
    rng = random.Random(5)
    pts = blobs(rng, 40, [(0, 0)], 0.5) + blobs(rng, 40, [(10, 0)], 0.5) + [(5, 8)]
    labels = hdbscan(pts, 5)
    assert labels[80] == NOISE
    assert len({labels[i] for i in range(40)} - {NOISE}) == 1
    assert len({labels[i] for i in range(40, 80)} - {NOISE}) == 1
    assert labels[0] != labels[40]
    assert sum(lab != NOISE for lab in labels) >= 70


def test_small_example():
    pts = [(0,), (1,), (2,), (3,), (10,), (11,), (12,), (13,), (30,)]
    labels = hdbscan(pts, 2, 3)
    assert labels == [0, 0, 0, 0, 1, 1, 1, 1, NOISE]
    core = core_distances(pts, 2)
    parent, birth, members, exit_lambda = condensed_tree(len(pts), mst_prim(pts, core), core, 3)
    assert parent == [-1, 0, 0]
    stab = stability(birth, members, exit_lambda)
    assert [round(s, 6) for s in stab] == [round(8 / 7 + 1 / 17, 6), round(4 * (1 - 1 / 7), 6), round(4 * (1 - 1 / 7), 6)]
