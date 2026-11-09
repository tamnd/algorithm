# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sutherland-hodgman/. The authors are listed in prov/2W87VM.jsonl.

import random
from fractions import Fraction

import pytest

from sutherland_hodgman import clip_half_plane, is_convex_ccw, sutherland_hodgman


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def edges_of(poly):
    n = len(poly)
    return [(poly[i], poly[(i + 1) % n]) for i in range(n) if poly[i] != poly[(i + 1) % n]]


def on_boundary(poly, q):
    for a, b in edges_of(poly):
        if orient(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= q[1] <= max(a[1], b[1]):
            return True
    return len(poly) == 1 and poly[0] == q


def winding(poly, q):
    """Winding number by signed crossings of the downward vertical ray (q off the boundary)."""
    w = 0
    for a, b in edges_of(poly):
        if a[0] <= q[0] < b[0] and orient(a, b, q) > 0:
            w += 1
        elif b[0] <= q[0] < a[0] and orient(a, b, q) < 0:
            w -= 1
    return w


def twice_area(poly):
    return sum(orient((0, 0), a, b) for a, b in edges_of(poly))


def crossing_xs(e, f):
    (a, b), (c, d) = e, f
    den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
    if den == 0:
        return []
    t = Fraction((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0]), den)
    u = Fraction((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0]), den)
    if 0 <= t <= 1 and 0 <= u <= 1:
        return [a[0] + t * (b[0] - a[0])]
    return []


def slab_integral(polys, weight):
    """Exact integral over the plane of weight(w_1, ..., w_k), w_j the winding number of polys[j].

    The plane is cut at every vertex x and every crossing x. Inside one slab no two edges cross,
    so each vertical cross-section has the same pattern and its length is linear in x; the value
    at the middle of the slab times its width is the exact integral over the slab.
    """
    groups = [edges_of(p) for p in polys]
    alle = [e for g in groups for e in g]
    xs = {Fraction(p[0]) for e in alle for p in e}
    for i in range(len(alle)):
        for j in range(i + 1, len(alle)):
            xs.update(crossing_xs(alle[i], alle[j]))
    xs = sorted(xs)
    total = Fraction(0)
    for x0, x1 in zip(xs, xs[1:]):
        xm = (x0 + x1) / 2
        hits = []
        for k, g in enumerate(groups):
            for a, b in g:
                if min(a[0], b[0]) < xm < max(a[0], b[0]):
                    y = a[1] + (xm - a[0]) * Fraction(b[1] - a[1]) / (b[0] - a[0])
                    hits.append((y, k, 1 if b[0] > a[0] else -1))
        hits.sort()
        w = [0] * len(groups)
        length = Fraction(0)
        for idx in range(len(hits) - 1):
            y, k, s = hits[idx]
            w[k] += s
            length += (hits[idx + 1][0] - y) * weight(*w)
        total += (x1 - x0) * length
    return total


def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


SUBJECT = [(0, 0), (6, 0), (6, 6), (3, 2), (0, 6)]
WINDOW = [(1, 1), (5, 1), (5, 5), (1, 5)]


def test_worked_example() -> None:
    out = sutherland_hodgman(SUBJECT, WINDOW)
    expected = [(1, 1), (5, 1), (5, Fraction(14, 3)), (3, 2), (1, Fraction(14, 3))]
    # The output starts where the last clip pass starts; compare as cycles.
    k = out.index((1, 1))
    assert out[k:] + out[:k] == expected
    assert twice_area(out) == 2 * Fraction(28, 3)


def test_concave_subject_gives_a_zero_width_bridge() -> None:
    # A U shape whose two arms both reach into the window: the output is one cycle that runs
    # along the bottom edge of the window twice, in opposite directions.
    u = [(0, 0), (6, 0), (6, 10), (4, 10), (4, 2), (2, 2), (2, 10), (0, 10)]
    window = [(-1, 4), (7, 4), (7, 8), (-1, 8)]
    out = sutherland_hodgman(u, window)
    assert twice_area(out) == 2 * (2 * 4 + 2 * 4)
    on_line = [p for p in out if p[1] == 4]
    assert len(on_line) == 4
    assert winding(out, (3, 6)) == 0 and winding(out, (1, 6)) == 1 and winding(out, (5, 6)) == 1


def test_bad_clip_polygons_are_rejected() -> None:
    concave = [(0, 0), (4, 0), (4, 4), (2, 1), (0, 4)]
    with pytest.raises(ValueError):
        sutherland_hodgman(SUBJECT, concave)
    pentagram = [(0, 10), (-6, -8), (10, 3), (-10, 3), (6, -8)]
    with pytest.raises(ValueError):
        sutherland_hodgman(SUBJECT, pentagram)
    with pytest.raises(ValueError):
        sutherland_hodgman(SUBJECT, [(0, 0), (1, 1), (2, 2)])
    with pytest.raises(ValueError):
        sutherland_hodgman(SUBJECT, [(0, 0), (1, 1)])
    assert is_convex_ccw([(0, 0), (2, 0), (2, 0), (4, 0), (4, 4), (0, 4)])
    assert not is_convex_ccw([(0, 0), (4, 0), (0, 0), (0, 4)])


def test_clockwise_clip_and_degenerate_subjects() -> None:
    cw = WINDOW[::-1]
    assert twice_area(sutherland_hodgman(SUBJECT, cw)) == twice_area(sutherland_hodgman(SUBJECT, WINDOW))
    assert sutherland_hodgman([], WINDOW) == []
    assert sutherland_hodgman([(10, 10), (12, 10), (12, 12)], WINDOW) == []
    inner = [(2, 2), (3, 2), (3, 3)]
    assert sutherland_hodgman(inner, WINDOW) == inner
    assert twice_area(sutherland_hodgman(WINDOW, [(0, 0), (9, 0), (9, 9), (0, 9)])) == 32
    # A subject vertex exactly on a clip line is kept once and not duplicated by an intersection.
    assert clip_half_plane([(0, 0), (2, 0), (4, 2), (2, 2)], (2, -5), (2, 5)) == [(0, 0), (2, 0), (2, 2)]
    assert clip_half_plane([(0, 0), (2, 0), (2, 2)], (1, -5), (1, 5)) == [(1, 1), (0, 0), (1, 0)]


def random_case(rng):
    size = rng.choice([4, 6, 10])
    subject = [(rng.randint(0, size), rng.randint(0, size)) for _ in range(rng.randint(3, 8))]
    while True:
        clip = convex_hull([(rng.randint(0, size), rng.randint(0, size)) for _ in range(rng.randint(3, 7))])
        if len(clip) >= 3:
            break
    if rng.random() < 0.5:
        clip = clip[::-1]
    return size, subject, clip


def test_area_against_slab_integral() -> None:
    rng = random.Random(2024)
    for _ in range(250):
        _, subject, clip = random_case(rng)
        out = sutherland_hodgman(subject, clip)
        sign = 1 if twice_area(clip) > 0 else -1
        expected = slab_integral([subject, clip], lambda ws, wc: ws if wc * sign > 0 else 0)
        assert Fraction(twice_area(out), 2) == expected


def test_winding_at_sample_points() -> None:
    rng = random.Random(99)
    checked = 0
    for _ in range(250):
        size, subject, clip = random_case(rng)
        out = sutherland_hodgman(subject, clip)
        for _ in range(12):
            q = (Fraction(rng.randint(-3, 3 * size + 3), 3), Fraction(rng.randint(-3, 3 * size + 3), 3))
            if on_boundary(subject, q) or on_boundary(clip, q):
                continue
            inside_clip = winding(clip, q) != 0
            assert winding(out, q) == (winding(subject, q) if inside_clip else 0)
            checked += 1
    assert checked > 2000
