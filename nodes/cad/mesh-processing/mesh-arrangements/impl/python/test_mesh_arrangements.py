# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mesh-arrangements/. The authors are listed in prov/NG1GH7.jsonl.

import random
from fractions import Fraction

from mesh_arrangements import (
    DIFFERENCE,
    INTERSECTION,
    UNION,
    Arrangement,
    area,
    boolean,
    winding_at,
)


def square(x0, y0, size, clockwise=False):
    pts = [(x0, y0), (x0 + size, y0), (x0 + size, y0 + size), (x0, y0 + size)]
    return pts[::-1] if clockwise else pts


def face_label(arr, p):
    """The label of the face that contains p, found by an exact ray to the right; None if the ray meets a vertex or p is on an edge."""
    if any(u[1] == p[1] or v[1] == p[1] for u, v in arr.mult):
        return None
    best = None
    for u, v in arr.mult:
        lo, hi = (u, v) if u[1] < v[1] else (v, u)
        if lo[1] < p[1] < hi[1]:
            x = lo[0] + (p[1] - lo[1]) * (hi[0] - lo[0]) / (hi[1] - lo[1])
            if x == p[0]:
                return None
            if x > p[0] and (best is None or x < best[0]):
                best = (x, (lo, hi))
    if best is None:
        return (0,) * arr.n                    # p is outside every component
    return arr.label[best[1]]                  # an upward edge right of p has p's face on its left


def random_polyline(rng, size=6):
    return [(rng.randint(0, size), rng.randint(0, size)) for _ in range(rng.randint(3, 6))]


def test_two_squares() -> None:
    a, b = [square(0, 0, 2)], [square(1, 1, 2)]
    for rule, want in ((UNION, 7), (INTERSECTION, 1), (DIFFERENCE, 3)):
        assert boolean(a, b, rule)[1] == want
    arr = Arrangement([(a[0], 0), (b[0], 1)], 2)
    half = Fraction(1, 2)
    for p, w in (((half, half), (1, 0)), ((Fraction(3, 2), Fraction(3, 2)), (1, 1)), ((Fraction(5, 2), Fraction(5, 2)), (0, 1)), ((Fraction(7, 2), half), (0, 0))):
        assert face_label(arr, p) == w == winding_at(p, arr.edges, 2)
    # the union boundary has 8 half-edges: the 8 outer pieces of the two squares
    assert len(boolean(a, b, UNION)[0]) == 8


def test_labels_match_the_exact_winding_number() -> None:
    rng = random.Random(2016)
    checked = 0
    for _ in range(30):
        polys = [(random_polyline(rng), k) for k in (0, 0, 1, 1)]
        arr = Arrangement(polys, 2)
        for _ in range(40):
            p = (Fraction(rng.randint(-20, 140), 20), Fraction(2 * rng.randint(-10, 70) + 1, 22))
            got = face_label(arr, p)
            if got is not None:
                assert got == winding_at(p, arr.edges, 2)
                checked += 1
    assert checked > 1000


def test_inclusion_exclusion_on_random_input() -> None:
    rng = random.Random(35)
    for _ in range(25):
        a = [random_polyline(rng) for _ in range(2)]
        b = [random_polyline(rng) for _ in range(2)]
        arr = Arrangement([(p, 0) for p in a] + [(p, 1) for p in b], 2)
        u, i, d = (area(arr.boundary(rule)) for rule in (UNION, INTERSECTION, DIFFERENCE))
        aa = area(arr.boundary(lambda w: w[0] > 0))
        bb = area(arr.boundary(lambda w: w[1] > 0))
        assert u + i == aa + bb
        assert d == aa - i
        assert min(u, i, d) >= 0


def test_coincident_and_touching_squares() -> None:
    a = [square(0, 0, 1)]
    edges, size = boolean(a, [square(0, 0, 1)], UNION)
    assert size == 1 and len(edges) == 4
    assert boolean(a, [square(0, 0, 1)], DIFFERENCE) == ([], 0)
    edges, size = boolean(a, [square(1, 0, 1)], UNION)
    assert size == 2 and len(edges) == 6          # the shared edge is inside and is dropped
    assert boolean(a, [square(1, 0, 1)], INTERSECTION) == ([], 0)


def test_hole_and_self_intersection() -> None:
    ring = [square(0, 0, 4), square(1, 1, 2, clockwise=True)]
    assert boolean(ring, [], UNION)[1] == 12
    # a bow tie winds +1 around its left lobe and -1 around its right lobe
    bowtie = [(0, 0), (2, 2), (2, 0), (0, 2)]
    arr = Arrangement([(bowtie, 0)], 1)
    assert face_label(arr, (Fraction(1, 2), Fraction(9, 10))) == (1,)
    assert face_label(arr, (Fraction(3, 2), Fraction(9, 10))) == (-1,)
    assert area(arr.boundary(lambda w: w[0] > 0)) == 1
    assert area(arr.boundary(lambda w: w[0] != 0)) == 2
