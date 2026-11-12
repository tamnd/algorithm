# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dbscan/. The authors are listed in prov/MFMXQM.jsonl.

import random

from dbscan import NOISE, dbscan, euclidean


def brute_core(points, eps, min_pts):
    n = len(points)
    return [sum(euclidean(points[i], points[j]) <= eps for j in range(n)) >= min_pts for i in range(n)]


def core_components(points, eps, core):
    """Connected components of the graph on core points with an edge when the distance is at most eps."""
    n = len(points)
    comp = [None] * n
    c = 0
    for s in range(n):
        if not core[s] or comp[s] is not None:
            continue
        comp[s] = c
        stack = [s]
        while stack:
            u = stack.pop()
            for v in range(n):
                if core[v] and comp[v] is None and euclidean(points[u], points[v]) <= eps:
                    comp[v] = c
                    stack.append(v)
        c += 1
    return comp


def check_against_definition(points, eps, min_pts):
    labels, is_core = dbscan(points, eps, min_pts)
    n = len(points)
    core = brute_core(points, eps, min_pts)
    assert is_core == core
    comp = core_components(points, eps, core)
    # Core points: same cluster if and only if same component of the core graph.
    for i in range(n):
        for j in range(n):
            if core[i] and core[j]:
                assert (labels[i] == labels[j]) == (comp[i] == comp[j])
    for i in range(n):
        near_core = [j for j in range(n) if core[j] and euclidean(points[i], points[j]) <= eps]
        if core[i]:
            assert labels[i] >= 0
        elif not near_core:
            assert labels[i] == NOISE  # noise by definition
        else:
            # Border point: it joins the cluster of one of its core neighbors.
            assert labels[i] in {labels[j] for j in near_core}
    used = sorted({x for x in labels if x >= 0})
    assert used == list(range(len(used)))
    return labels, core


def test_small_example():
    pts = [(0, 0), (1, 0), (0, 1), (1, 1), (2, 1), (6, 6), (7, 6), (6, 7), (7, 7), (4, 4), (9, 0)]
    labels, is_core = dbscan(pts, 1.5, 4)
    assert labels == [0, 0, 0, 0, 0, 1, 1, 1, 1, -1, -1]
    assert [i for i in range(len(pts)) if is_core[i]] == [0, 1, 2, 3, 5, 6, 7, 8]


def test_border_point_depends_on_order():
    # 15 is within eps of the core points 9 and 21 but is not a core point itself.
    pts = [(0,), (3,), (6,), (9,), (15,), (21,), (24,), (27,), (30,)]
    labels, core = dbscan(pts, 6, 4)
    assert not core[4] and core[3] and core[5]
    assert labels[4] == labels[3]
    rev = pts[::-1]
    labels2, core2 = dbscan(rev, 6, 4)
    assert core2 == core[::-1]
    assert labels2[4] == labels2[3]  # now 15 joins the cluster of 21 (index 3 of the reversed list)


def test_random_against_definition():
    rng = random.Random(7)
    for _ in range(60):
        n = rng.randrange(1, 40)
        pts = [(rng.uniform(0, 10), rng.uniform(0, 10)) for _ in range(n)]
        eps = rng.uniform(0.5, 3)
        min_pts = rng.randrange(1, 7)
        labels, core = check_against_definition(pts, eps, min_pts)
        # Core and noise sets do not depend on the order of the input.
        perm = list(range(n))
        rng.shuffle(perm)
        labels2, core2 = dbscan([pts[p] for p in perm], eps, min_pts)
        for a, p in enumerate(perm):
            assert core2[a] == core[p]
            assert (labels2[a] == NOISE) == (labels[p] == NOISE)


def test_min_pts_one_and_edges():
    assert dbscan([], 1.0, 3) == ([], [])
    labels, core = dbscan([(0.0,), (5.0,)], 1.0, 1)
    assert labels == [0, 1] and core == [True, True]
    labels, core = dbscan([(0.0,), (0.5,)], 1.0, 3)
    assert labels == [NOISE, NOISE]
