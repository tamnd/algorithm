# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greiner-hormann-algorithm/. The authors are listed in prov/34CRJR.jsonl.

import random
from fractions import Fraction
from math import ceil, floor, gcd

import pytest

from greiner_hormann_algorithm import DegenerateError, greiner_hormann, ring_area2

OPS = ("intersection", "union", "difference")


def cross3(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def area2(poly):
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def on_seg(a, b, p):
    return cross3(a, b, p) == 0 and (p[0] - a[0]) * (p[0] - b[0]) + (p[1] - a[1]) * (p[1] - b[1]) <= 0


def on_boundary(poly, p):
    return any(on_seg(poly[i], poly[(i + 1) % len(poly)], p) for i in range(len(poly)))


def inside(poly, p):
    """Exact crossing rule with a Fraction crossing point; p must not be on the boundary."""
    c = False
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (a[1] > p[1]) != (b[1] > p[1]):
            x = a[0] + Fraction(p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x > p[0]:
                c = not c
    return c


def seg_meet(a, b, c, d):
    d1, d2, d3, d4 = cross3(c, d, a), cross3(c, d, b), cross3(a, b, c), cross3(a, b, d)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    return on_seg(c, d, a) or on_seg(c, d, b) or on_seg(a, b, c) or on_seg(a, b, d)


def is_simple(poly):
    n = len(poly)
    if len(set(poly)) != n or n < 3:
        return False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for j in range(i + 1, n):
            c, d = poly[j], poly[(j + 1) % n]
            if j == i + 1 or (i == 0 and j == n - 1):
                s, o1, o2 = (b, a, d) if j == i + 1 else (a, b, c)
                if cross3(s, o1, o2) == 0 and (o1[0] - s[0]) * (o2[0] - s[0]) + (o1[1] - s[1]) * (o2[1] - s[1]) > 0:
                    return False
            elif seg_meet(a, b, c, d):
                return False
    return True


def random_simple(rng, n, g):
    """A random simple polygon on a grid, untangled by 2-opt moves; either orientation."""
    for _ in range(50):
        pts = list({(rng.randint(0, g), rng.randint(0, g)) for _ in range(n)})
        if len(pts) < 3:
            continue
        rng.shuffle(pts)
        for _ in range(200):
            m = len(pts)
            bad = None
            for i in range(m):
                for j in range(i + 2, m):
                    if i == 0 and j == m - 1:
                        continue
                    if seg_meet(pts[i], pts[i + 1], pts[j], pts[(j + 1) % m]):
                        bad = (i, j)
                        break
                if bad:
                    break
            if not bad:
                break
            i, j = bad
            pts[i + 1:j + 1] = pts[i + 1:j + 1][::-1]
        if is_simple(pts) and area2(pts) != 0:
            return pts
    return None


def add_collinear(rng, poly):
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        out.append(a)
        dx, dy = b[0] - a[0], b[1] - a[1]
        g = gcd(abs(dx), abs(dy))
        for k in range(1, g):
            if rng.random() < 0.3:
                out.append((a[0] + k * dx // g, a[1] + k * dy // g))
    return out


def degenerate(s, c):
    """Independent test: the boundaries meet non-transversally exactly when a vertex lies on the other boundary."""
    return any(on_boundary(c, p) for p in s) or any(on_boundary(s, p) for p in c)


def ccw(poly):
    return poly if area2(poly) > 0 else poly[::-1]


def oracle_area2(s, c, op):
    """Twice the area by Green's theorem over the pieces of the two boundaries that bound the result."""
    s, c = ccw(s), ccw(c)

    def pieces(poly, other, want_inside, reverse):
        total = Fraction(0)
        n = len(poly)
        for i in range(n):
            a, b = poly[i], poly[(i + 1) % n]
            cuts = {Fraction(0), Fraction(1)}
            for j in range(len(other)):
                p, q = other[j], other[(j + 1) % len(other)]
                den = (b[0] - a[0]) * (q[1] - p[1]) - (b[1] - a[1]) * (q[0] - p[0])
                if den != 0:
                    t = Fraction((p[0] - a[0]) * (q[1] - p[1]) - (p[1] - a[1]) * (q[0] - p[0])) / den
                    u = Fraction((p[0] - a[0]) * (b[1] - a[1]) - (p[1] - a[1]) * (b[0] - a[0])) / den
                    if 0 < t < 1 and 0 < u < 1:
                        cuts.add(t)
            cuts = sorted(cuts)
            for lo, hi in zip(cuts, cuts[1:]):
                mid = (lo + hi) / 2
                if inside(other, (a[0] + mid * (b[0] - a[0]), a[1] + mid * (b[1] - a[1]))) == want_inside:
                    x0, y0 = a[0] + lo * (b[0] - a[0]), a[1] + lo * (b[1] - a[1])
                    x1, y1 = a[0] + hi * (b[0] - a[0]), a[1] + hi * (b[1] - a[1])
                    total += (x1 * y0 - x0 * y1) if reverse else (x0 * y1 - x1 * y0)
        return total

    if op == "intersection":
        return pieces(s, c, True, False) + pieces(c, s, True, False)
    if op == "union":
        return pieces(s, c, False, False) + pieces(c, s, False, False)
    return pieces(s, c, False, False) + pieces(c, s, True, True)


def result_area2(rings):
    """Twice the area of the even-odd union of the rings: holes count negative."""
    total = Fraction(0)
    for i, r in enumerate(rings):
        depth = sum(1 for j, q in enumerate(rings) if j != i and inside(q, r[0]))
        total += abs(ring_area2(r)) * (1 if depth % 2 == 0 else -1)
    return total


def in_result(rings, p):
    return sum(1 for r in rings if inside(r, p)) % 2 == 1


def want(op, a, b):
    return a and b if op == "intersection" else a or b if op == "union" else a and not b


def check(s, c, rng, samples=30):
    xs = [p[0] for p in s + c]
    ys = [p[1] for p in s + c]
    for op in OPS:
        rings = greiner_hormann(s, c, op)
        for r in rings:
            assert len(r) >= 3 and is_simple(r), (s, c, op, r)
        assert result_area2(rings) == oracle_area2(s, c, op), (s, c, op)
        for _ in range(samples):
            p = (Fraction(rng.randint(floor(4 * min(xs)) - 4, ceil(4 * max(xs)) + 4), 4) + Fraction(1, 97),
                 Fraction(rng.randint(floor(4 * min(ys)) - 4, ceil(4 * max(ys)) + 4), 4) + Fraction(1, 89))
            if on_boundary(s, p) or on_boundary(c, p) or any(on_boundary(r, p) for r in rings):
                continue
            assert in_result(rings, p) == want(op, inside(s, p), inside(c, p)), (s, c, op, p)
    # points on the subject boundary, strictly inside or outside the clip, lie on the result boundary
    inter, union, diff = (greiner_hormann(s, c, op) for op in OPS)
    for i in range(len(s)):
        a, b = s[i], s[(i + 1) % len(s)]
        p = ((a[0] + b[0]) / Fraction(2), (a[1] + b[1]) / Fraction(2))
        if on_boundary(c, p):
            continue
        if inside(c, p):
            assert any(on_boundary(r, p) for r in inter)
        else:
            assert any(on_boundary(r, p) for r in union) and any(on_boundary(r, p) for r in diff)


def shifted(poly, dx, dy):
    return [(x + dx, y + dy) for x, y in poly]


SQUARE = [(0, 0), (4, 0), (4, 4), (0, 4)]
KITE = [(2, -1), (7, 1), (5, 5), (1, 2)]


def test_example() -> None:
    f = Fraction
    assert greiner_hormann(SQUARE, KITE, "intersection") == [[(f(5, 3), 0), (4, 0), (4, 4), (f(11, 3), 4), (1, 2)]]
    assert greiner_hormann(SQUARE, KITE, "difference") == [[(f(5, 3), 0), (0, 0), (0, 4), (f(11, 3), 4), (1, 2)]]
    union = greiner_hormann(SQUARE, KITE, "union")
    assert len(union) == 1 and abs(ring_area2(union[0])) == f(161, 3)
    check(SQUARE, KITE, random.Random(1))


def test_union_with_a_hole() -> None:
    # two C-shapes that close a square hole between them
    left = [(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (3, 3), (3, 4), (0, 4)]
    right = shifted([(-1, 0), (3, 0), (3, 4), (-1, 4), (-1, 3), (2, 3), (2, 1), (-1, 1)], Fraction(1, 2), Fraction(1, 3))
    rings = greiner_hormann(left, right, "union")
    assert len(rings) == 2
    check(left, right, random.Random(2))


def test_several_pieces() -> None:
    comb = [(0, 0), (5, 0), (5, 3), (4, 3), (4, 1), (3, 1), (3, 3), (2, 3), (2, 1), (1, 1), (1, 3), (0, 3)]
    bar = shifted([(-1, 2), (6, 2), (6, 4), (-1, 4)], 0, Fraction(1, 2))
    assert len(greiner_hormann(comb, bar, "intersection")) == 3
    assert len(greiner_hormann(comb, bar, "difference")) == 1
    check(comb, bar, random.Random(3))


def test_no_crossing() -> None:
    inner = shifted([(1, 1), (2, 1), (2, 2), (1, 2)], Fraction(1, 3), 0)
    far = shifted(SQUARE, 10, 0)
    assert greiner_hormann(SQUARE, inner, "intersection") == [inner]
    assert greiner_hormann(SQUARE, inner, "union") == [SQUARE]
    assert greiner_hormann(SQUARE, inner, "difference") == [SQUARE, inner]
    assert greiner_hormann(inner, SQUARE, "difference") == []
    assert greiner_hormann(SQUARE, far, "intersection") == []
    assert greiner_hormann(SQUARE, far, "union") == [SQUARE, far]
    for c in (inner, far):
        check(SQUARE, c, random.Random(4))
        check(c, SQUARE, random.Random(5))


def test_collinear_vertices_and_orientation() -> None:
    square = [(0, 0), (2, 0), (4, 0), (4, 2), (4, 4), (0, 4)]
    tri = [(Fraction(1, 2), -1), (5, Fraction(5, 2)), (Fraction(1, 2), Fraction(9, 2))]
    for s in (square, square[::-1]):
        for c in (tri, tri[::-1]):
            check(s, c, random.Random(6))


def test_degenerate_input_is_rejected() -> None:
    cases = [
        [(4, 0), (6, 0), (6, 2), (4, 2)],          # shares the edge x = 4 with the square
        [(4, 4), (6, 4), (6, 6)],                  # shares the vertex (4, 4)
        [(2, 4), (3, 6), (1, 6)],                  # a vertex on the top edge
        [(-2, 1), (0, 2), (-2, 3)],                # touches the left edge at (0, 2) from outside
        [(-1, -1), (2, 2), (-1, 2)],               # passes through the corner (0, 0)
    ]
    for c in cases:
        assert degenerate(SQUARE, c)
        for op in OPS:
            with pytest.raises(DegenerateError):
                greiner_hormann(SQUARE, c, op)
    with pytest.raises(ValueError):
        greiner_hormann(SQUARE, [(0, 0), (1, 1), (2, 2)])
    with pytest.raises(ValueError):
        greiner_hormann(SQUARE, KITE, "xor")


def test_random_pairs() -> None:
    rng = random.Random(20261109)
    done = rejected = 0
    while done < 500:
        s = random_simple(rng, rng.randint(3, 9), rng.choice([4, 6, 9]))
        c = random_simple(rng, rng.randint(3, 9), rng.choice([4, 6, 9]))
        if s is None or c is None:
            continue
        if rng.random() < 0.4:
            s = add_collinear(rng, s)
        if rng.random() < 0.3:
            c = add_collinear(rng, c)
        if rng.random() < 0.85:
            c = shifted(c, Fraction(rng.randint(1, 5), 7), Fraction(rng.randint(1, 4), 5))
        if degenerate(s, c):
            for op in OPS:
                with pytest.raises(DegenerateError):
                    greiner_hormann(s, c, op)
            rejected += 1
            continue
        check(s, c, rng, samples=12)
        done += 1
    assert rejected > 20
