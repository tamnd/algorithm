# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optics/. The authors are listed in prov/P3H623.jsonl.

import random

from optics import INF, NOISE, assign_missed_border_points, euclidean, extract_dbscan, optics


def r_dist(points, core, o, p, eps):
    """Reachability distance of p with respect to o (Definition 6)."""
    d = euclidean(points[o], points[p])
    if core[o] == INF or d > eps:
        return INF
    return max(core[o], d)


def dbscan_reference(points, eps, min_pts):
    """The DBSCAN core set, the components of the core graph and the noise set, by definition."""
    n = len(points)
    nb = [[j for j in range(n) if euclidean(points[i], points[j]) <= eps] for i in range(n)]
    core = [len(nb[i]) >= min_pts for i in range(n)]
    comp = [None] * n
    c = 0
    for s in range(n):
        if core[s] and comp[s] is None:
            comp[s] = c
            stack = [s]
            while stack:
                u = stack.pop()
                for v in nb[u]:
                    if core[v] and comp[v] is None:
                        comp[v] = c
                        stack.append(v)
            c += 1
    noise = {i for i in range(n) if not core[i] and not any(core[j] for j in nb[i])}
    return core, comp, noise


def random_points(rng, n):
    pts = []
    for _ in range(n):
        cx, cy = rng.choice([(0, 0), (6, 0), (3, 5)])
        pts.append((cx + rng.gauss(0, 1), cy + rng.gauss(0, 1)))
    return pts


def test_definitions_of_core_and_reachability():
    rng = random.Random(3)
    for _ in range(40):
        n = rng.randrange(1, 35)
        pts = random_points(rng, n)
        eps, min_pts = rng.uniform(0.5, 4), rng.randrange(1, 6)
        order, reach, core = optics(pts, eps, min_pts)
        assert sorted(order) == list(range(n))
        for p in range(n):
            ds = sorted(euclidean(pts[p], q) for q in pts)
            want = ds[min_pts - 1] if sum(x <= eps for x in ds) >= min_pts else INF
            assert core[p] == want
        for i, p in enumerate(order):
            assert reach[p] == min([r_dist(pts, core, o, p, eps) for o in order[:i]], default=INF)
            # Greedy: p has the smallest current reachability among the unprocessed points.
            for u in order[i + 1:]:
                cur = min([r_dist(pts, core, o, u, eps) for o in order[:i]], default=INF)
                assert reach[p] <= cur


def test_extract_dbscan_matches_dbscan():
    rng = random.Random(11)
    extra_noise_seen = 0
    for _ in range(60):
        n = rng.randrange(1, 40)
        pts = random_points(rng, n)
        eps, min_pts = rng.uniform(1, 4), rng.randrange(1, 7)
        order, reach, core = optics(pts, eps, min_pts)
        for eps_prime in [eps * f for f in (0.3, 0.5, 0.7, 0.9, 1.0)]:
            labels = extract_dbscan(order, reach, core, eps_prime)
            ref_core, comp, ref_noise = dbscan_reference(pts, eps_prime, min_pts)
            is_core = [core[p] <= eps_prime for p in range(n)]
            assert is_core == ref_core
            for i in range(n):
                for j in range(n):
                    if ref_core[i] and ref_core[j]:
                        assert (labels[i] == labels[j]) == (comp[i] == comp[j])
                if ref_core[i]:
                    assert labels[i] != NOISE
            got_noise = {i for i in range(n) if labels[i] == NOISE}
            assert ref_noise <= got_noise
            for i in got_noise - ref_noise:
                assert not ref_core[i]  # only border points can be missed
                extra_noise_seen += 1
            for i in range(n):
                if labels[i] != NOISE and not ref_core[i]:
                    assert any(ref_core[j] and labels[j] == labels[i] and euclidean(pts[i], pts[j]) <= eps_prime for j in range(n))
            fixed = assign_missed_border_points(pts, labels, core, eps_prime)
            assert {i for i in range(n) if fixed[i] == NOISE} == ref_noise
    assert extra_noise_seen > 0  # the missed border points of the paper do occur


def test_missed_border_point_example():
    pts = [(0,), (2,), (3,), (4,), (5,)]
    order, reach, core = optics(pts, 4, 3)
    assert order == [0, 1, 2, 3, 4]
    assert reach == [INF, 3, 2, 1, 1]
    assert core == [3, 2, 1, 1, 2]
    # DBSCAN with eps' = 2 makes the point at 0 a border point (it is 2 from the core point at 2).
    labels = extract_dbscan(order, reach, core, 2)
    assert labels == [NOISE, 0, 0, 0, 0]
    assert assign_missed_border_points(pts, labels, core, 2) == [0, 0, 0, 0, 0]
    # With eps' = 1 the point at 2 is a border point of DBSCAN, but the extraction misses it.
    labels = extract_dbscan(order, reach, core, 1)
    assert labels == [NOISE, NOISE, 0, 0, 0]
    assert assign_missed_border_points(pts, labels, core, 1) == [NOISE, 0, 0, 0, 0]
    # With eps' = 3 the point 0 is a core point, so nothing is missed.
    assert extract_dbscan(order, reach, core, 3) == [0, 0, 0, 0, 0]


def test_min_pts_two_is_prim():
    # With MinPts = 2 and an infinite eps, the reachability values are the edge
    # weights that Prim's algorithm adds, so their sum is the MST weight.
    rng = random.Random(5)
    for _ in range(30):
        n = rng.randrange(2, 25)
        pts = random_points(rng, n)
        order, reach, core = optics(pts, INF, 2)
        in_tree, best, total = {0}, [euclidean(pts[0], q) for q in pts], 0.0
        while len(in_tree) < n:
            v = min((i for i in range(n) if i not in in_tree), key=lambda i: best[i])
            total += best[v]
            in_tree.add(v)
            best = [min(best[i], euclidean(pts[v], pts[i])) for i in range(n)]
        assert abs(sum(reach[p] for p in order[1:]) - total) < 1e-9


def test_edges():
    assert optics([], 1, 2) == ([], [], [])
    order, reach, core = optics([(0.0,)], 1, 1)
    assert order == [0] and reach == [INF] and core == [0.0]
    assert extract_dbscan(order, reach, core, 1) == [0]
