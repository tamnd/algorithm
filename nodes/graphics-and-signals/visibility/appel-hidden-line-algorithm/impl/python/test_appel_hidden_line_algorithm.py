# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/appel-hidden-line-algorithm/. The authors are listed in prov/EFMSAP.jsonl.

"""Check Appel's QI walk against a direct depth test at sample points.

The brute force does not walk along edges. For a sample point p on an edge
it counts the front faces whose projection contains p (winding number) and
whose plane is above p. It samples every edge between all the points where
its projection meets the projection of another edge.
"""

import random
from fractions import Fraction as F

from appel_hidden_line_algorithm import CUBE_FACES, appel_hidden_lines, cube


def winding(poly2, x, y):
    w = 0
    m = len(poly2)
    for k in range(m):
        x1, y1 = poly2[k]
        x2, y2 = poly2[(k + 1) % m]
        c = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        if y1 <= y < y2 and c > 0:
            w += 1
        elif y2 <= y < y1 and c < 0:
            w -= 1
    return w


def brute_qi(scene, p, skip):
    count = 0
    for fi, f in enumerate(scene.faces):
        if fi in skip:
            continue
        pts = [scene.vertices[v] for v in f]
        # plane through the first three points that are not on one line
        n = None
        for k in range(1, len(pts) - 1):
            a, b, c = pts[0], pts[k], pts[k + 1]
            u = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
            v = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
            cand = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
            if cand != (0, 0, 0):
                n = cand
                break
        area2 = sum(pts[k][0] * pts[(k + 1) % len(pts)][1] - pts[(k + 1) % len(pts)][0] * pts[k][1]
                    for k in range(len(pts)))
        if area2 <= 0:  # not a front face: its projection is clockwise
            continue
        if winding([(q[0], q[1]) for q in pts], p[0], p[1]) == 0:
            continue
        a = pts[0]
        z = a[2] - (n[0] * (p[0] - a[0]) + n[1] * (p[1] - a[1])) / n[2]
        if z > p[2]:
            count += 1
    return count


def projected_cuts(scene, u, w):
    p0, p1 = scene.vertices[u], scene.vertices[w]
    ex, ey = p1[0] - p0[0], p1[1] - p0[1]
    ts = {F(0), F(1)}
    for a, b in scene.edges:
        q0, q1 = scene.vertices[a], scene.vertices[b]
        cx, cy = q1[0] - q0[0], q1[1] - q0[1]
        den = ex * cy - ey * cx
        if den == 0:
            continue
        rx, ry = q0[0] - p0[0], q0[1] - p0[1]
        t = (rx * cy - ry * cx) / den
        s = (rx * ey - ry * ex) / den
        if 0 < t < 1 and 0 <= s <= 1:
            ts.add(t)
    return sorted(ts)


def check(solids):
    scene, pieces = appel_hidden_lines(solids)
    assert set(pieces) == set(scene.edges)
    samples = 0
    for (u, w), run in pieces.items():
        assert run[0][0] == 0 and run[-1][1] == 1
        assert all(run[k][1] == run[k + 1][0] for k in range(len(run) - 1))
        skip = set(scene.edge_faces[(u, w)])
        ts = projected_cuts(scene, u, w)
        p0, p1 = scene.vertices[u], scene.vertices[w]
        for t0, t1 in zip(ts, ts[1:]):
            t = (t0 + t1) / 2
            p = tuple(p0[c] + t * (p1[c] - p0[c]) for c in range(3))
            got = next(k for a, b, k in run if a < t < b)
            assert got == brute_qi(scene, p, skip), ((u, w), t)
            samples += 1
    return samples


def transform(solid, m, shift):
    verts, faces = solid
    out = []
    for v in verts:
        out.append(tuple(sum(m[r][c] * v[c] for c in range(3)) + shift[r] for r in range(3)))
    return out, faces


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def l_prism(z0, z1):
    """An L shaped prism: nonconvex top and bottom faces."""
    base = [(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)]
    m = len(base)
    verts = [(x, y, z0) for x, y in base] + [(x, y, z1) for x, y in base]
    faces = [list(range(m - 1, -1, -1)), list(range(m, 2 * m))]
    for k in range(m):
        j = (k + 1) % m
        faces.append([k, j, m + j, m + k])
    return verts, faces


SHEAR = [[F(1), F(0), F(1, 3)], [F(0), F(1), F(1, 5)], [F(0), F(0), F(1)]]


def test_box_over_slab_partly_hides_its_edges():
    slab = cube((0, 0, 0), (4, 4, 1))
    block = cube((3, 3, 2), (6, 5, 3))  # sticks out past the slab corner
    solids = [transform(slab, SHEAR, (0, 0, 0)), transform(block, SHEAR, (0, 0, 0))]
    assert check(solids) > 0
    scene, pieces = appel_hidden_lines(solids)
    assert any(len(run) > 1 for run in pieces.values())  # some QI change inside an edge


def test_nonconvex_solid_hides_itself():
    m = [[F(1), F(0), F(2, 7)], [F(0), F(1), F(3, 11)], [F(1, 13), F(-1, 17), F(1)]]
    assert det3(m) > 0
    solids = [transform(l_prism(0, 1), m, (0, 0, 0)), transform(cube((0, 0, 0), (1, 1, 1)), m, (F(1, 2), F(1, 3), 2))]
    assert check(solids) > 0


def test_single_cube_matches_back_face_count():
    solids = [transform(cube((0, 0, 0), (1, 1, 1)), SHEAR, (0, 0, 0))]
    scene, pieces = appel_hidden_lines(solids)
    hidden = [e for e, run in pieces.items() if all(k > 0 for _, _, k in run)]
    assert len(hidden) == 3  # the three edges at the far corner
    check(solids)


def test_random_scenes():
    rng = random.Random(7)
    tested = 0
    for _ in range(12):
        solids = []
        for layer in range(rng.randint(2, 3)):
            x0, y0 = rng.randint(0, 4), rng.randint(0, 4)
            lo = (x0, y0, 3 * layer)
            hi = (x0 + rng.randint(1, 4), y0 + rng.randint(1, 4), 3 * layer + rng.randint(1, 2))
            solids.append(cube(lo, hi) if rng.random() < 0.7 else
                          transform(l_prism(0, 1), [[F(1), 0, 0], [0, F(1), 0], [0, 0, F(1)]], lo))
        while True:
            m = [[F(rng.randint(-3, 3), 7) + (1 if r == c else 0) for c in range(3)] for r in range(3)]
            if det3(m) > 0:
                break
        solids = [transform(s, m, (0, 0, 0)) for s in solids]
        try:
            check(solids)
        except ValueError:
            continue  # a degenerate view, outside the general position assumption
        tested += 1
    assert tested >= 9
