# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/adaptive-slicing/. The authors are listed in prov/BT4MQH.jsonl.

import math
import random
from fractions import Fraction as F
from functools import lru_cache

import pytest

from adaptive_slicing import adaptive_slice, facet_data, feasible, max_cusp_ratio

# ---- meshes ----


def ring_solid(rings, cap_low, cap_high):
    """Closed mesh from rings (z, [(x, y), ...]) with z increasing, counterclockwise points."""
    v, f = [], []
    c = len(rings[0][1])
    for z, pts in rings:
        v.extend((x, y, z) for x, y in pts)
    idx = lambda i, j: i * c + (j % c)
    for i in range(len(rings) - 1):
        for j in range(c):
            a, b, cc, d = idx(i, j), idx(i, j + 1), idx(i + 1, j + 1), idx(i + 1, j)
            f += [(a, b, cc), (a, cc, d)]
    lo, hi = len(v), len(v) + 1
    v += [cap_low, cap_high]
    top = len(rings) - 1
    for j in range(c):
        f.append((lo, idx(0, j + 1), idx(0, j)))
        f.append((hi, idx(top, j), idx(top, j + 1)))
    return v, f


def circle_points():
    ws = [F(0), F(1, 4), F(1, 2), F(1), F(2), F(4), None, F(-4), F(-2), F(-1), F(-1, 2), F(-1, 4)]
    pts = []
    for w in ws:
        if w is None:
            pts.append((F(-1), F(0)))
        else:
            pts.append(((1 - w * w) / (1 + w * w), 2 * w / (1 + w * w)))
    return pts


def rational_sphere(radius):
    """Vertices exactly on the sphere x^2 + y^2 + z^2 = radius^2."""
    rings = []
    for u in [F(4), F(2), F(4, 3), F(1), F(3, 4), F(1, 2), F(1, 4)]:  # z increases
        z, rho = (1 - u * u) / (1 + u * u), 2 * u / (1 + u * u)
        rings.append((radius * z, [(radius * rho * x, radius * rho * y) for x, y in circle_points()]))
    return ring_solid(rings, (0, 0, -radius), (0, 0, radius))


def cone(radius, height):
    pts = circle_points()
    rings = [(0, [(radius * x, radius * y) for x, y in pts])]
    return ring_solid(rings, (0, 0, 0), (0, 0, height))


def roof_house():
    v = [(0, 0, 0), (4, 0, 0), (4, 4, 0), (0, 4, 0), (0, 0, 2), (4, 0, 2), (4, 4, 2), (0, 4, 2), (2, 2, 3)]
    f = [(0, 2, 1), (0, 3, 2), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6),
         (3, 0, 4), (3, 4, 7), (4, 5, 8), (5, 6, 8), (6, 7, 8), (7, 4, 8)]
    return v, f


# ---- independent checks ----


def cusp_ok_brute(vertices, faces, z, t, c):
    """Direct check of every face: the cusp t |cos theta| is at most c.

    The normal is computed at a different corner, (c - b) x (a - b), and the
    slab test uses the vertex heights directly.
    """
    for i, j, k in faces:
        a, b, cc = vertices[i], vertices[j], vertices[k]
        zs = [a[2], b[2], cc[2]]
        if not (min(zs) < z + t and max(zs) > z):
            continue
        u = [cc[m] - b[m] for m in range(3)]
        w = [a[m] - b[m] for m in range(3)]
        n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
        if t * t * n[2] * n[2] > c * c * sum(x * x for x in n):
            return False
    return True


def check_layers(vertices, faces, ts, c, tops):
    ts = sorted(F(t) for t in ts)
    z = F(min(p[2] for p in vertices))
    zhi = max(p[2] for p in vertices)
    assert tops[-1] >= zhi and (len(tops) == 1 or tops[-2] < zhi)
    for top in tops:
        t = top - z
        assert t in ts
        larger = [s for s in ts if s > t]
        if cusp_ok_brute(vertices, faces, z, t, c):
            for s in larger:  # the choice is the largest feasible one
                assert not cusp_ok_brute(vertices, faces, z, s, c)
        else:
            assert t == ts[0]  # fallback only when nothing is feasible
            assert not any(cusp_ok_brute(vertices, faces, z, s, c) for s in ts)
        z = top


# ---- tests ----


def test_page_example_house():
    v, f = roof_house()
    tops = adaptive_slice(v, f, [F(1, 4), F(1, 2), 1], F(1, 4))
    assert tops == [1, 2, F(9, 4), F(5, 2), F(11, 4), 3]
    check_layers(v, f, [F(1, 4), F(1, 2), 1], F(1, 4), tops)
    # roof normal (0, -4, 8): t = 1/2 fails, t = 1/4 holds
    assert F(1, 2) ** 2 * 64 > F(1, 4) ** 2 * 80
    assert F(1, 4) ** 2 * 64 <= F(1, 4) ** 2 * 80


def test_sphere_cusp_bound_holds():
    v, f = rational_sphere(10)
    assert all(x * x + y * y + z * z == 100 for x, y, z in v)
    ts = [F(1, 20), F(1, 10), F(1, 5), F(3, 10)]
    c = F(1, 20)
    tops = adaptive_slice(v, f, ts, c)
    check_layers(v, f, ts, c, tops)
    facets = facet_data(v, f)
    z = F(-10)
    for top in tops:
        assert max_cusp_ratio(facets, z, top - z) <= c * c
        z = top
    thick = [b - a for a, b in zip([F(-10)] + tops, tops)]
    assert min(thick) == F(1, 20) and max(thick) == F(3, 10)  # thin near the poles, thick at the equator
    assert len(tops) < 20 * 20  # fewer layers than uniform slicing with t = 1/20


def test_cone_cusp_bound_holds():
    v, f = cone(6, 8)
    ts = [F(1, 10), F(1, 5), F(3, 10), F(2, 5)]
    for c in [F(1, 10), F(3, 20), F(1, 4)]:
        tops = adaptive_slice(v, f, ts, c)
        check_layers(v, f, ts, c, tops)


def test_fallback_to_thinnest_layer():
    v, f = roof_house()
    tops = adaptive_slice(v, f, [F(1, 2), 1], F(1, 10))
    check_layers(v, f, [F(1, 2), 1], F(1, 10), tops)
    assert tops == [1, 2, F(5, 2), 3]


def test_horizontal_face_inside_a_layer():
    # a box from z = 0 to z = 1: its top face lies inside the slab (0, 2)
    v = [(x, y, z) for z in (0, 1) for y in (0, 1) for x in (0, 1)]
    f = [(0, 2, 1), (1, 2, 3), (4, 5, 6), (5, 7, 6), (0, 1, 4), (1, 5, 4),
         (2, 6, 3), (3, 6, 7), (0, 4, 2), (2, 4, 6), (1, 3, 5), (3, 7, 5)]
    facets = facet_data(v, f)
    assert not feasible(facets, 0, 2, F(1, 4))  # the top face is inside (0, 2)
    assert feasible(facets, 0, 1, F(1, 4))  # but on the boundary of (0, 1)
    assert adaptive_slice(v, f, [F(1, 2), 1, 2], F(1, 4)) == [1]


def greedy_count(facets, ts, c, zlo, zhi):
    z, n = zlo, 0
    while z < zhi:
        t = ts[0]
        for s in reversed(ts):
            if feasible(facets, z, s, c):
                t = s
                break
        z, n = z + t, n + 1
    return n


def optimum_count(facets, ts, c, zlo, zhi):
    @lru_cache(maxsize=None)
    def best(z):
        if z >= zhi:
            return 0
        return 1 + min(best(z + s) for s in ts if s == ts[0] or feasible(facets, z, s, c))

    return best(zlo)


def test_greedy_is_not_always_minimal():
    # two bands with |cos theta| = 1/3 at heights 2 to 3 and 7 to 8, walls elsewhere
    facets = [(0, 9, 0, 1), (2, 3, 1, 9), (7, 8, 1, 9)]
    ts, c = [1, 2, 4], 1
    assert greedy_count(facets, ts, c, 0, 9) == 5  # 2, 2, 2, 2, 4
    assert optimum_count(facets, ts, c, 0, 9) == 4  # 2, 1, 4, 2


def test_greedy_against_exhaustive_minimum():
    rng = random.Random(4)
    worse = 0
    for _ in range(3000):
        ts = rng.choice([[1, 2], [1, 3], [1, 2, 4], [2, 3, 5]])
        hi = rng.randint(3, 12)
        facets = [(0, hi, 0, 1)]
        for _ in range(rng.randint(1, 4)):
            lo = rng.randint(0, hi - 1)
            facets.append((lo, rng.randint(lo + 1, min(hi, lo + 3)), 1, rng.choice([1, 4, 9, 16, 25])))
        g = greedy_count(facets, ts, 1, 0, hi)
        o = optimum_count(facets, ts, 1, 0, hi)
        assert g >= o
        worse += g > o
    assert worse > 0


def test_float_cusp_matches_exact_on_sphere():
    v, f = rational_sphere(10)
    for lo, hi, nz2, nn in facet_data(v, f):
        cos_float = abs(math.sqrt(float(nz2) / float(nn)))
        assert abs(cos_float ** 2 - float(F(nz2) / nn)) < 1e-12


def test_bad_parameters():
    v, f = roof_house()
    with pytest.raises(ValueError):
        adaptive_slice(v, f, [], F(1, 4))
    with pytest.raises(ValueError):
        adaptive_slice(v, f, [F(1, 4)], 0)
