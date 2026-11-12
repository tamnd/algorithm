# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shadow-volume-algorithm/. The authors are listed in prov/K1P3D1.jsonl.

import random
from fractions import Fraction

from shadow_volume_algorithm import build_volume, cross, dot, faces_toward, normal, shadow_volumes, sub


def det3(a, b, c):
    return dot(a, cross(b, c))


def segment_meets(tri, p, q):
    """Does the closed segment pq meet the closed triangle? Exact, with Fraction (Cramer's rule)."""
    a, b, c = tri
    e1, e2, d, r = sub(b, a), sub(c, a), sub(p, q), sub(p, a)
    m = det3(e1, e2, d)
    if m == 0:
        return False  # parallel; the tests avoid coplanar cases
    u, v, t = Fraction(det3(r, e2, d), m), Fraction(det3(e1, r, d), m), Fraction(det3(e1, e2, r), m)
    return u >= 0 and v >= 0 and u + v <= 1 and 0 <= t <= 1


def lit_brute(p, light, occluders):
    """Exact ray-to-light test: p is in shadow when the segment from p to the light meets an occluder."""
    return not any(segment_meets(f, p, light) for occ in occluders for f in occ)


def seen(p, eye, occluders):
    """Is the ground point p the first thing on the eye ray? No occluder face meets the segment."""
    return not any(segment_meets(f, eye, p) for occ in occluders for f in occ)


def outward(tri, inner):
    a, b, c = tri
    return (a, b, c) if dot(normal((a, b, c)), sub(inner, a)) < 0 else (a, c, b)


def tetra(pts):
    inner = tuple(Fraction(sum(p[k] for p in pts), 4) for k in range(3))
    return [outward(tuple(pts[i] for i in range(4) if i != o), inner) for o in range(4)]


def degenerate(eye, p, volume):
    """Is the eye line through p in the plane of an edge or a face of the volume, or is p on a face plane?"""
    for tri in volume:
        n = normal(tri)
        if dot(n, sub(p, tri[0])) == 0 or dot(n, sub(p, eye)) == 0:
            return True
        for i in range(3):
            a, b = tri[i], tri[(i + 1) % 3]
            if dot(sub(p, eye), cross(sub(a, eye), sub(b, eye))) == 0:
                return True
    return False


EX_OCC = [tetra([(2, 2, 2), (6, 2, 2), (2, 6, 2), (2, 2, 4)])]
EX_LIGHT = (3, 3, 12)
EX_POINTS = [(1, 7, 0), (3, 4, 0), (5, 4, 0), (9, 1, 0)]


def test_worked_example():
    vol = build_volume(EX_OCC[0], EX_LIGHT)
    # The light sees only the slanted face x + y + 2z = 12; the base and the faces x = 2, y = 2 face away.
    lit = [faces_toward(f, EX_LIGHT) for f in EX_OCC[0]]
    assert lit == [True, False, False, False]
    assert len(vol) == 1 + 2 * 3 + 3  # near cap, three silhouette quads as six triangles, far cap
    truth = [not lit_brute(p, EX_LIGHT, EX_OCC) for p in EX_POINTS]
    assert truth == [False, True, False, False]
    eye = (19, 13, 16)  # outside the shadow
    assert lit_brute(eye, EX_LIGHT, EX_OCC)
    assert all(seen(p, eye, EX_OCC) and not degenerate(eye, p, vol) for p in EX_POINTS)
    for method in ("zpass", "zfail"):
        assert shadow_volumes(EX_OCC, EX_LIGHT, eye, EX_POINTS, method) == truth
    # An eye inside the shadow, under the occluder: z-pass is wrong, z-fail is right.
    low = (3, 4, 1)
    assert not lit_brute(low, EX_LIGHT, EX_OCC)
    pts = [(4, 3, 0), (9, 1, 0)]
    truth = [not lit_brute(p, EX_LIGHT, EX_OCC) for p in pts]
    assert truth == [True, False]
    assert shadow_volumes(EX_OCC, EX_LIGHT, low, pts, "zfail") == truth
    assert shadow_volumes(EX_OCC, EX_LIGHT, low, pts, "zpass") == [False, True]


def random_scene(rng):
    occluders = []
    for _ in range(rng.randint(1, 3)):
        while True:
            pts = [(rng.randint(0, 800), rng.randint(0, 800), rng.randint(100, 500)) for _ in range(4)]
            if det3(sub(pts[1], pts[0]), sub(pts[2], pts[0]), sub(pts[3], pts[0])) != 0:
                break
        occluders.append(tetra(pts))
    light = (rng.randint(-300, 1100), rng.randint(-300, 1100), rng.randint(700, 1300))
    return occluders, light


def test_both_rules_match_ray_to_light_when_the_eye_is_lit():
    rng = random.Random(71)
    shadowed = checked = 0
    for case in range(500):
        occluders, light = random_scene(rng)
        eye = (rng.randint(-500, 1300), rng.randint(-500, 1300), rng.randint(600, 1500))
        if not lit_brute(eye, light, occluders):
            continue
        volume = [t for occ in occluders for t in build_volume(occ, light)]
        pts = [(rng.randint(0, 800), rng.randint(0, 800), 0) for _ in range(6)]
        pts = [p for p in pts if seen(p, eye, occluders) and not degenerate(eye, p, volume)]
        truth = [not lit_brute(p, light, occluders) for p in pts]
        assert shadow_volumes(occluders, light, eye, pts, "zpass") == truth
        assert shadow_volumes(occluders, light, eye, pts, "zfail") == truth
        shadowed += sum(truth)
        checked += len(pts)
    assert checked > 1500 and 0 < shadowed < checked


def test_zfail_is_right_for_each_eye_and_zpass_fails_in_shadow():
    rng = random.Random(72)
    zpass_wrong = 0
    for case in range(150):
        occluders, light = random_scene(rng)
        occ = occluders[0]
        g = [Fraction(sum(f[i][k] for f in occ for i in range(3)), 12) for k in range(3)]
        under = (g[0], g[1], Fraction(g[2] * rng.randint(1, 9), 10))  # often in the shadow of occ
        eye = tuple(Fraction(round(c * 7)) / 7 + Fraction(1, 97) for c in under)
        if eye[2] <= 0:
            continue  # an eye inside an occluder sees no ground point, so `seen` drops all points
        volume = [t for o in occluders for t in build_volume(o, light)]
        pts = [(rng.randint(0, 800), rng.randint(0, 800), 0) for _ in range(5)]
        pts = [p for p in pts if seen(p, eye, occluders) and not degenerate(eye, p, volume)]
        truth = [not lit_brute(p, light, occluders) for p in pts]
        assert shadow_volumes(occluders, light, eye, pts, "zfail") == truth
        if shadow_volumes(occluders, light, eye, pts, "zpass") != truth:
            zpass_wrong += 1
            assert not lit_brute(eye, light, occluders)
    assert zpass_wrong > 0


def test_volume_is_closed_and_oriented():
    rng = random.Random(73)
    for case in range(100):
        occluders, light = random_scene(rng)
        vol = build_volume(occluders[0], light)
        edges = {}
        for tri in vol:
            for i in range(3):
                e = (tri[i], tri[(i + 1) % 3])
                edges[e] = edges.get(e, 0) + 1
        assert all(c == 1 and edges.get((e[1], e[0])) == 1 for e, c in edges.items())


def test_edges():
    assert shadow_volumes([], (0, 0, 10), (5, 5, 5), [(1, 1, 0)]) == [False]
    assert shadow_volumes(EX_OCC, EX_LIGHT, (20, 20, 15), [], "zpass") == []
