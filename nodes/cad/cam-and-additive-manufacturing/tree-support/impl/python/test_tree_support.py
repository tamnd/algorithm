# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tree-support/. The authors are listed in prov/YRE332.jsonl.

import math
import random
from fractions import Fraction as F

from tree_support import dist2, is_overhang, merge, shorter, sqrt_up, support_points, total_length, tree_support

# ---- meshes ----


def box(x0, y0, z0, x1, y1, z1):
    v = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    f = [(0, 2, 1), (1, 2, 3), (4, 5, 6), (5, 7, 6), (0, 1, 4), (1, 5, 4),
         (2, 6, 3), (3, 6, 7), (0, 4, 2), (2, 4, 6), (1, 3, 5), (3, 7, 5)]
    return v, f


def inverted_pyramid(apex_z, top_z):
    v = [(0, 0, top_z), (4, 0, top_z), (4, 4, top_z), (0, 4, top_z), (2, 2, apex_z)]
    f = [(0, 1, 2), (0, 2, 3), (4, 1, 0), (4, 2, 1), (4, 3, 2), (4, 0, 3)]
    return v, f


# ---- independent checks ----


def brute_overhang(p, q, r, angle_deg):
    """Float angle test, used away from ties only."""
    n = [((q[1] - p[1]) * (r[2] - p[2]) - (q[2] - p[2]) * (r[1] - p[1])),
         ((q[2] - p[2]) * (r[0] - p[0]) - (q[0] - p[0]) * (r[2] - p[2])),
         ((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]))]
    n = [float(x) for x in n]
    tilt = math.degrees(math.acos(max(-1.0, min(1.0, -n[2] / math.sqrt(sum(x * x for x in n))))))
    return n[2] < 0 and tilt < 90 - angle_deg, tilt


def check_tree(points, nodes, struts, k):
    """Every given point has a path of struts down to z = 0, inside the cones."""
    down = {}
    for a, b in struts:
        assert a not in down  # one strut below each node: a forest
        down[a] = b
        p, q = nodes[a], nodes[b]
        dz = p[2] - q[2]
        h2 = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
        assert dz > 0 and h2 <= k * k * dz * dz  # strictly down, inside the cone
    for i, p in enumerate(points):
        assert nodes[i] == tuple(F(x) for x in p)
        j, steps = i, 0
        while nodes[j][2] > 0:
            j = down[j]
            steps += 1
            assert steps <= len(nodes)
        assert nodes[j][2] == 0


def greedy_slow(points, k=1, grid=1 << 10):
    """Same greedy rule without a heap: rescan all pairs after each merge."""
    k = F(k)
    nodes = [tuple(F(x) for x in p) for p in points]
    active = list(range(len(nodes)))
    struts = []
    while True:
        best = None
        for x in range(len(active)):
            for y in range(x + 1, len(active)):
                i, j = active[x], active[y]
                a, b = (i, j) if nodes[i][2] >= nodes[j][2] else (j, i)
                m, saves = merge(nodes[a], nodes[b], k, grid)
                if saves and (best is None or m[2] > best[0]):
                    best = (m[2], a, b, m)
        if best is None:
            break
        _, a, b, m = best
        active.remove(a)
        active.remove(b)
        if m == nodes[b]:
            struts.append((a, b))
            active.append(b)
        else:
            same = [r for r in active if nodes[r] == m]
            if same:
                struts += [(a, same[0]), (b, same[0])]
            else:
                nodes.append(m)
                struts += [(a, len(nodes) - 1), (b, len(nodes) - 1)]
                active.append(len(nodes) - 1)
    for a in sorted(active):
        nodes.append((nodes[a][0], nodes[a][1], F(0)))
        struts.append((a, len(nodes) - 1))
    return nodes, struts


def random_points(rng, n):
    pts = set()
    while len(pts) < n:
        pts.add((rng.randint(0, 12), rng.randint(0, 12), rng.randint(1, 8)))
    return sorted(pts)


# ---- tests ----


def test_page_example():
    pts = [(0, 0, 6), (4, 0, 6), (3, 0, 3), (12, 0, 4)]
    nodes, struts = tree_support(pts)
    check_tree(pts, nodes, struts, 1)
    edges = {(tuple(nodes[a]), tuple(nodes[b])) for a, b in struts}
    assert ((0, 0, 6), (2, 0, 4)) in edges and ((4, 0, 6), (2, 0, 4)) in edges
    assert ((2, 0, 4), (3, 0, 3)) in edges  # (3, 0, 3) lies in the cone of (2, 0, 4)
    assert ((12, 0, 4), (12, 0, 0)) in edges and ((3, 0, 3), (3, 0, 0)) in edges
    assert abs(total_length(nodes, struts) - (4 * math.sqrt(2) + math.sqrt(2) + 3 + 4)) < 1e-9


def test_merge_point_equal_to_an_active_point():
    for pts in ([(0, 0, 4), (4, 0, 4), (2, 0, 2)], [(0, 0, 4), (4, 0, 4), (2, 0, 2), (2, 0, 1)]):
        nodes, struts = tree_support(pts)
        check_tree(pts, nodes, struts, 1)
        assert len(set(nodes)) == len(nodes)


def test_overhang_test_exact_at_45_degrees():
    s2 = F(1, 2)
    v, f = inverted_pyramid(1, 3)  # side faces at exactly 45 degrees
    assert not any(is_overhang(*(v[i] for i in face), s2) for face in f)
    v, f = inverted_pyramid(2, 3)  # shallower, 26.6 degrees from horizontal
    assert sum(is_overhang(*(v[i] for i in face), s2) for face in f) == 4
    v, f = box(0, 0, 0, 2, 2, 2)  # bottom face on the plate needs nothing
    assert not any(is_overhang(*(v[i] for i in face), s2) for face in f)


def test_overhang_against_float_angles():
    rng = random.Random(9)
    for _ in range(3000):
        p, q, r = [(rng.randint(-5, 5), rng.randint(-5, 5), rng.randint(1, 6)) for _ in range(3)]
        n = (((q[1] - p[1]) * (r[2] - p[2]) - (q[2] - p[2]) * (r[1] - p[1])),
             ((q[2] - p[2]) * (r[0] - p[0]) - (q[0] - p[0]) * (r[2] - p[2])),
             ((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])))
        if n == (0, 0, 0):
            continue
        want, tilt = brute_overhang(p, q, r, 45)
        if abs(tilt - 45) < 1e-6:
            continue
        assert is_overhang(p, q, r, F(1, 2)) == want


def test_support_points_of_meshes():
    v, f = box(0, 0, 2, 4, 4, 3)  # a hovering box
    pts = support_points(v, f, F(1, 2), 2)
    assert all(p[2] == 2 for p in pts)
    assert len(pts) == 9  # the 3 x 3 grid of step 2 on the bottom face
    v, f = inverted_pyramid(2, 3)
    pts = support_points(v, f, F(1, 2), 1)
    assert (2, 2, 2) in pts  # the apex is a local minimum
    nodes, struts = tree_support(pts)
    check_tree(pts, nodes, struts, 1)


def test_heap_matches_slow_greedy():
    rng = random.Random(21)
    for _ in range(40):
        pts = random_points(rng, rng.randint(2, 9))
        n1, s1 = tree_support(pts)
        n2, s2 = greedy_slow(pts)
        assert {(n1[a], n1[b]) for a, b in s1} == {(n2[a], n2[b]) for a, b in s2}


def test_all_points_supported_and_shorter_than_pillars():
    rng = random.Random(2)
    for _ in range(60):
        pts = random_points(rng, rng.randint(1, 14))
        k = rng.choice([F(1), F(1, 2), F(2)])
        nodes, struts = tree_support(pts, k)
        check_tree(pts, nodes, struts, k)
        assert total_length(nodes, struts) <= sum(p[2] for p in pts) + 1e-9


def test_random_meshes_supported():
    rng = random.Random(6)
    for _ in range(4):
        z0 = rng.randint(1, 3)
        v, f = box(0, 0, z0, rng.randint(2, 6), rng.randint(2, 6), z0 + 2)
        a = rng.randint(1, 2)
        v2, f2 = inverted_pyramid(z0 + 5, z0 + 5 + a)
        off = len(v)
        v = v + [(x + 8, y, z) for x, y, z in v2]
        f = f + [(i + off, j + off, l + off) for i, j, l in f2]
        pts = support_points(v, f, F(1, 2), 2)
        nodes, struts = tree_support(pts)
        check_tree(pts, nodes, struts, 1)


def test_exact_helpers():
    rng = random.Random(3)
    for _ in range(2000):
        x = F(rng.randint(0, 10 ** 6), rng.randint(1, 1000))
        u = sqrt_up(x)
        assert u * u >= x and u - F(1, 1 << 23) < math.sqrt(x) + 1e-9
        a2, b2 = F(rng.randint(0, 50)), F(rng.randint(0, 50))
        c = F(rng.randint(0, 200), 10)
        lhs = math.sqrt(a2) + math.sqrt(b2)
        if abs(lhs - c) > 1e-9:
            assert shorter(a2, b2, c) == (lhs < c)
    assert not shorter(9, 16, 7) and shorter(9, 16, F(7000001, 1000000))  # 3 + 4 = 7 is a tie
