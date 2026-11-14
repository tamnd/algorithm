# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/liepa-hole-filling/. The authors are listed in prov/4HZ1HE.jsonl.

import random
from math import acos, comb

from liepa_hole_filling import (border_loops, dihedral, area, fill_hole, liepa_triangulation, normal,
                                outside_apex, triangulate_loop, dot)

# ---- brute force: every triangulation of the loop 0, ..., n - 1 ----


def all_triangulations(i, k, memo=None):
    if memo is None:
        memo = {}
    if k - i < 2:
        return [[]]
    if (i, k) not in memo:
        out = []
        for m in range(i + 1, k):
            for left in all_triangulations(i, m, memo):
                for right in all_triangulations(m, k, memo):
                    out.append(left + right + [(i, m, k)])
        memo[(i, k)] = out
    return memo[(i, k)]


def catalan(n):
    return comb(2 * n, n) // (n + 1)


def random_loop(rng, n, r=6):
    return [(rng.randint(-r, r), rng.randint(-r, r), rng.randint(-r, r)) for _ in range(n)]


def sq_double_area(p, t):
    nv = normal(p, *t)
    return dot(nv, nv)


# ---- the dynamic program against exhaustive search ----


def test_number_of_triangulations_is_catalan():
    for n in range(3, 10):
        assert len(all_triangulations(0, n - 1)) == catalan(n - 2)


def test_sum_weight_is_optimal():
    rng = random.Random(2003)
    for _ in range(250):
        n = rng.randint(3, 8)
        p = random_loop(rng, n)
        r = triangulate_loop(n, lambda i, m, k, a, b: sq_double_area(p, (i, m, k)), lambda x, y: x + y, 0)
        best = min(sum(sq_double_area(p, t) for t in T) for T in all_triangulations(0, n - 1))
        assert r.weight == best
        assert sum(sq_double_area(p, t) for t in r.triangles) == best
        assert len(r.triangles) == n - 2


def test_table_weights_sum_and_max_are_optimal():
    rng = random.Random(1995)
    for _ in range(250):
        n = rng.randint(3, 8)
        w = {(i, m, k): rng.randint(0, 50) for i in range(n) for m in range(i + 1, n) for k in range(m + 1, n)}
        om = lambda i, m, k, a, b: w[(i, m, k)]
        for plus, agg in ((lambda x, y: x + y, sum), (max, max)):
            r = triangulate_loop(n, om, plus, 0)
            best = min(agg(w[t] for t in T) for T in all_triangulations(0, n - 1))
            assert r.weight == best == agg(w[t] for t in r.triangles)


def test_lexicographic_pair_is_not_decomposable():
    """(max, +) in lexicographic order is not monotone, so the program can miss the optimum."""
    rng = random.Random(7)
    strict = 0
    for _ in range(400):
        n = rng.randint(4, 8)
        w = {(i, m, k): (rng.randint(0, 3), rng.randint(0, 9))
             for i in range(n) for m in range(i + 1, n) for k in range(m + 1, n)}
        plus = lambda x, y: (max(x[0], y[0]), x[1] + y[1])

        def total(T):
            return (max(w[t][0] for t in T), sum(w[t][1] for t in T))

        r = triangulate_loop(n, lambda i, m, k, a, b: w[(i, m, k)], plus, (0, 0))
        best = min(total(T) for T in all_triangulations(0, n - 1))
        assert r.weight == total(r.triangles)
        assert r.weight >= best
        strict += r.weight > best
    assert strict > 0


def test_lexicographic_counterexample_of_the_proof():
    w = {t: (9, 0) for t in [(i, m, k) for i in range(5) for m in range(i + 1, 5) for k in range(m + 1, 5)]}
    w[(0, 1, 4)] = (5, 0)
    w[(1, 2, 4)], w[(2, 3, 4)] = (1, 10), (0, 0)
    w[(1, 2, 3)], w[(1, 3, 4)] = (2, 0), (0, 0)
    plus = lambda x, y: (max(x[0], y[0]), x[1] + y[1])
    r = triangulate_loop(5, lambda i, m, k, a, b: w[(i, m, k)], plus, (0, 0))
    assert r.weight == (5, 10) and r.triangles == [(0, 1, 4), (1, 2, 4), (2, 3, 4)]
    assert (5, 0) == plus(plus(w[(0, 1, 4)], w[(1, 2, 3)]), w[(1, 3, 4)])


def liepa_true_weight(p, loop, out, T):
    """The weight of a full triangulation: the largest dihedral angle over all adjacent pairs, then the area."""
    tri = [(loop[i], loop[m], loop[k]) for i, m, k in T]
    where = {}
    for t in tri:
        for j in range(3):
            where[(t[j], t[(j + 1) % 3])] = t
    n = len(loop)
    for i in range(n):
        if out[i] is not None:
            where[(loop[(i + 1) % n], loop[i])] = (loop[(i + 1) % n], loop[i], out[i])
    worst = 0.0
    for t in tri:
        for j in range(3):
            u = where.get((t[(j + 1) % 3], t[j]))
            if u is not None:
                worst = max(worst, dihedral(p, t, u))
    return (worst, sum(area(p, *t) for t in tri))


def test_liepa_weight_against_exhaustive():
    rng = random.Random(42)
    for _ in range(120):
        n = rng.randint(3, 7)
        loop_pts = random_loop(rng, n)
        # a ring of mesh triangles around the loop, with apexes pushed outward
        pts = list(loop_pts)
        faces = []
        for i in range(n):
            a, b = loop_pts[i], loop_pts[(i + 1) % n]
            pts.append(tuple(2 * (a[j] + b[j]) + rng.randint(-2, 2) for j in range(3)))
            faces.append((i + 1 if i + 1 < n else 0, i, n + i))
        loop = list(range(n))
        out = outside_apex(faces, loop)
        assert out == [n + i for i in range(n)]
        got = liepa_triangulation(pts, faces, loop)
        pos = {v: i for i, v in enumerate(loop)}
        T = sorted(tuple(sorted(pos[v] for v in t)) for t in got)
        mine = liepa_true_weight(pts, loop, out, T)
        best = min(liepa_true_weight(pts, loop, out, S) for S in all_triangulations(0, n - 1))
        assert mine >= (best[0] - 1e-12, best[1] - 1e-9)
        assert len(got) == n - 2


# ---- the page example ----


def test_page_example_skew_quad():
    p = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 1)]
    r = triangulate_loop(4, lambda i, m, k, a, b: (0.0, area(p, i, m, k)),
                         lambda x, y: (max(x[0], y[0]), x[1] + y[1]), (0.0, 0.0))
    assert r.triangles == [(0, 1, 2), (0, 2, 3)]
    assert abs(r.weight[1] - (0.5 + 3 ** 0.5 / 2)) < 1e-12


def test_page_example_dihedral_choice():
    # the skew quad as a hole in a folded sheet: the angle term overrules the area term
    pts = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 1),
           (0.5, -1, -6), (2, 0.5, -1), (0.5, 2, 0.5), (-1, 0.5, 0.5)]
    faces = [(1, 0, 4), (2, 1, 5), (3, 2, 6), (0, 3, 7)]
    loop = [0, 1, 2, 3]
    assert outside_apex(faces, loop) == [4, 5, 6, 7]
    got = liepa_triangulation(pts, faces, loop)
    assert got == [(0, 1, 3), (1, 2, 3)]
    out = outside_apex(faces, loop)
    w13 = liepa_true_weight(pts, loop, out, [(0, 1, 3), (1, 2, 3)])
    w02 = liepa_true_weight(pts, loop, out, [(0, 1, 2), (0, 2, 3)])
    assert abs(w13[0] - acos(0.5)) < 1e-12 and abs(w13[1] - 2 ** 0.5) < 1e-12
    assert abs(w02[0] - acos(1 / 37 ** 0.5)) < 1e-12 and w02[1] < w13[1]


# ---- filling holes in meshes ----


def grid(n):
    pts = [(x, y, 0) for y in range(n + 1) for x in range(n + 1)]
    faces = []
    for y in range(n):
        for x in range(n):
            a = y * (n + 1) + x
            faces += [(a, a + 1, a + n + 2), (a, a + n + 2, a + n + 1)]
    return pts, faces


def directed_ok(faces):
    seen = set()
    for f in faces:
        for i in range(3):
            e = (f[i], f[(i + 1) % 3])
            if e in seen:
                return False
            seen.add(e)
    return True


def test_border_loops_of_a_disk():
    pts, faces = grid(2)
    loops = border_loops(faces)
    assert len(loops) == 1 and len(loops[0]) == 8
    # the patch walks the border against the faces: 0 -> 3 is the reverse of the face edge 3 -> 0
    assert loops[0][:2] == [0, 3]


def test_fill_planar_hole_in_grid():
    pts, faces = grid(6)
    hole = {(x, y) for x in range(2, 4) for y in range(1, 5)}
    kept = [f for idx, f in enumerate(faces) if ((idx // 2) % 6, (idx // 2) // 6) not in hole]
    loops = border_loops(kept)
    assert len(loops) == 2
    inner = min(loops, key=len)
    assert len(inner) == 12
    r = fill_hole(pts, kept, inner)
    allf = kept + r.patch
    assert directed_ok(allf)
    assert len(border_loops(allf)) == 1
    assert len(r.coarse) == len(inner) - 2
    assert len(r.points) > len(pts)  # the refinement added vertices
    for q in r.points[len(pts):]:
        assert abs(q[2]) < 1e-9  # the membrane of a flat loop is flat
    total = sum(area(r.points, *t) for t in r.patch)
    assert abs(total - 8.0) < 1e-9  # the patch covers the 2 x 4 hole exactly once


def test_fill_open_box_gives_closed_cube():
    pts = [(x, y, z) for z in (0, 1) for y in (0, 1) for x in (0, 1)]
    quads = [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]
    faces = []
    for a, b, c, d in quads[1:]:  # the bottom face is missing
        faces += [(a, b, c), (a, c, d)]
    loops = border_loops(faces)
    assert len(loops) == 1 and sorted(loops[0]) == [0, 1, 2, 3]
    r = fill_hole(pts, faces, loops[0])
    allf = faces + r.patch
    assert directed_ok(allf) and border_loops(allf) == []
    vol6 = 0.0
    for a, b, c in allf:
        P, Q, R = r.points[a], r.points[b], r.points[c]
        vol6 += dot(P, (Q[1] * R[2] - Q[2] * R[1], Q[2] * R[0] - Q[0] * R[2], Q[0] * R[1] - Q[1] * R[0]))
    assert abs(vol6 - 6.0) < 1e-9
    # the coarse patch is flat: the dihedral angle with the side walls is 90 degrees for both diagonals,
    # and between its two triangles it is 0
    assert len(r.coarse) == 2
