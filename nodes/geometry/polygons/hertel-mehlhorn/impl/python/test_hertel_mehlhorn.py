# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hertel-mehlhorn/. The authors are listed in prov/F65KA1.jsonl.

import itertools
import random
from fractions import Fraction
from math import gcd

import pytest

from hertel_mehlhorn import convex_partition, ear_clipping, hertel_mehlhorn


def cross3(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def area2(poly):
    n = len(poly)
    return sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def on_seg(a, b, p):
    return cross3(a, b, p) == 0 and (p[0] - a[0]) * (p[0] - b[0]) + (p[1] - a[1]) * (p[1] - b[1]) <= 0


def seg_meet(a, b, c, d):
    """Closed segments ab and cd share a point."""
    d1, d2, d3, d4 = cross3(c, d, a), cross3(c, d, b), cross3(a, b, c), cross3(a, b, d)
    if ((d1 > 0) != (d2 > 0)) and d1 != 0 and d2 != 0 and ((d3 > 0) != (d4 > 0)) and d3 != 0 and d4 != 0:
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


def reflex_count(poly):
    n = len(poly)
    return sum(1 for i in range(n) if cross3(poly[i - 1], poly[i], poly[(i + 1) % n]) < 0)


def is_convex_ccw(poly):
    """All turns nonnegative, positive area, edge directions wind once (no reversal)."""
    n = len(poly)
    if area2(poly) <= 0:
        return False
    for i in range(n):
        a, b, c = poly[i - 1], poly[i], poly[(i + 1) % n]
        t = cross3(a, b, c)
        if t < 0:
            return False
        if t == 0 and (b[0] - a[0]) * (c[0] - b[0]) + (b[1] - a[1]) * (c[1] - b[1]) <= 0:
            return False
    return is_simple(poly)


def inside_convex(poly, p):
    return all(cross3(poly[i], poly[(i + 1) % len(poly)], p) > 0 for i in range(len(poly)))


def check_partition(poly, pieces, tris):
    n = len(poly)
    total = 0
    for f in pieces:
        pts = [poly[i] for i in f]
        assert is_convex_ccw(pts), (poly, f)
        # the indices of a piece cut off by diagonals appear in cyclic order of the polygon
        k = len(f)
        steps = sum((f[(i + 1) % k] - f[i]) % n for i in range(k))
        assert steps == n, (poly, f)
        total += area2(pts)
    assert total == area2(poly)
    # every triangle of the triangulation lies in exactly one piece
    for t in tris:
        c = (Fraction(sum(poly[i][0] for i in t), 3), Fraction(sum(poly[i][1] for i in t), 3))
        assert sum(1 for f in pieces if inside_convex([poly[i] for i in f], c)) == 1
    r = reflex_count(poly)
    assert len(pieces) <= 2 * r + 1
    assert len(pieces) >= (r + 1) // 2 + 1


def diagonals_of(pieces, n):
    out = set()
    for f in pieces:
        for i in range(len(f)):
            a, b = f[i], f[(i + 1) % len(f)]
            if (b - a) % n != 1:
                out.add((min(a, b), max(a, b)))
    return out


def check_essential(poly, pieces):
    """Merging the two pieces at any remaining diagonal must give a nonconvex polygon."""
    n = len(poly)
    for a, b in diagonals_of(pieces, n):
        two = [f for f in pieces if a in f and b in f and (
            (f.index(b) - f.index(a)) % len(f) in (1, len(f) - 1))]
        assert len(two) == 2
        f, g = two
        if (f.index(b) - f.index(a)) % len(f) != 1:
            f, g = g, f
        # f has the directed edge a -> b, g has b -> a
        i = f.index(b)
        part1 = [f[(i + k) % len(f)] for k in range(len(f))]  # b ... a
        j = g.index(a)
        part2 = [g[(j + k) % len(g)] for k in range(1, len(g) - 1)]  # after a ... before b
        merged = [poly[x] for x in part1 + part2]
        assert not is_convex_ccw(merged), (poly, pieces, (a, b))


def is_diagonal(poly, i, j):
    n = len(poly)
    if (j - i) % n in (0, 1, n - 1):
        return False
    a, b = poly[i], poly[j]
    for k in range(n):
        if k not in (i, j) and on_seg(a, b, poly[k]):
            return False
    for k in range(n):
        c, d = poly[k], poly[(k + 1) % n]
        if k in (i, j) or (k + 1) % n in (i, j):
            continue
        if seg_meet(a, b, c, d):
            return False
    # the midpoint is inside, by crossing parity
    m = (Fraction(a[0] + b[0], 2), Fraction(a[1] + b[1], 2))
    inside = False
    for k in range(n):
        c, d = poly[k], poly[(k + 1) % n]
        if (c[1] > m[1]) != (d[1] > m[1]):
            x = c[0] + (m[1] - c[1]) * Fraction(d[0] - c[0], d[1] - c[1])
            if x > m[0]:
                inside = not inside
    return inside


def faces_from_diagonals(poly, diags):
    """Split the polygon along non-crossing diagonals, by recursion on index ranges."""
    n = len(poly)
    pieces = [list(range(n))]
    for a, b in diags:
        for f in pieces:
            if a in f and b in f:
                ia, ib = f.index(a), f.index(b)
                if ia > ib:
                    ia, ib = ib, ia
                if ib - ia in (1, len(f) - 1):
                    continue
                pieces.remove(f)
                pieces.append(f[ia:ib + 1])
                pieces.append(f[ib:] + f[:ia + 1])
                break
    return pieces


def min_convex_by_brute_force(poly):
    n = len(poly)
    r = reflex_count(poly)
    if r == 0:
        return 1
    refl = {i for i in range(n) if cross3(poly[i - 1], poly[i], poly[(i + 1) % n]) < 0}
    cands = [(i, j) for i in range(n) for j in range(i + 1, n) if (i in refl or j in refl) and is_diagonal(poly, i, j)]
    for k in range((r + 1) // 2, 2 * r + 1):
        for S in itertools.combinations(cands, k):
            ok = True
            for x in range(k):
                for y in range(x + 1, k):
                    p, q = S[x], S[y]
                    if len({p[0], p[1], q[0], q[1]}) == 4 and seg_meet(poly[p[0]], poly[p[1]], poly[q[0]], poly[q[1]]):
                        ok = False
            if ok and all(is_convex_ccw([poly[i] for i in f]) for f in faces_from_diagonals(poly, S)):
                return k + 1
    raise AssertionError("no partition found")


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


def random_simple(rng, n, g):
    """A random simple polygon: a random order of grid points, untangled by 2-opt moves."""
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
                    a, b, c, d = pts[i], pts[i + 1], pts[j], pts[(j + 1) % m]
                    if seg_meet(a, b, c, d):
                        bad = (i, j)
                        break
                if bad:
                    break
            if not bad:
                break
            i, j = bad
            pts[i + 1:j + 1] = pts[i + 1:j + 1][::-1]
        if is_simple(pts) and area2(pts) != 0:
            return pts if area2(pts) > 0 else pts[::-1]
    return None


COMB = [(0, 0), (5, 0), (5, 3), (4, 3), (4, 1), (3, 1), (3, 3), (2, 3), (2, 1), (1, 1), (1, 3), (0, 3)]
PINWHEEL = [(0, 0), (4, 0), (11, 6), (6, 0), (30, 0), (27, 5), (22, 8), (24, 10), (15, 25), (9, 15), (10, 12), (6, 10)]
EXAMPLE = [(0, 0), (6, 0), (6, 4), (4, 4), (4, 2), (2, 2), (2, 4), (0, 4)]


def test_example() -> None:
    tris = ear_clipping(EXAMPLE)
    pieces = hertel_mehlhorn(EXAMPLE, tris)
    check_partition(EXAMPLE, pieces, tris)
    check_essential(EXAMPLE, pieces)
    assert pieces == [[0, 1, 4, 5], [0, 5, 6, 7], [1, 2, 3, 4]]


def test_convex_polygon_gives_one_piece() -> None:
    sq = [(0, 0), (1, 0), (2, 0), (2, 2), (1, 2), (0, 2), (0, 1)]
    assert convex_partition(sq) == [list(range(7))]
    tri = [(0, 0), (Fraction(1, 2), 0), (0, Fraction(1, 3))]
    assert convex_partition(tri) == [[0, 1, 2]]


def test_fixed_shapes() -> None:
    for poly in (COMB, PINWHEEL, EXAMPLE, [(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)]):
        tris = ear_clipping(poly)
        pieces = hertel_mehlhorn(poly, tris)
        check_partition(poly, pieces, tris)
        check_essential(poly, pieces)
    assert len(convex_partition([(0, 0), (4, 0), (4, 2), (2, 2), (2, 4), (0, 4)])) == 2


def test_any_triangulation_works() -> None:
    # a fan from a kernel vertex of a star-shaped polygon is another triangulation
    poly = [(3, 0), (6, 1), (5, 3), (6, 6), (3, 4), (0, 6), (1, 3), (0, 1)]
    assert all(is_diagonal(poly, 0, i) for i in range(2, len(poly) - 1))
    fan = [(0, i, i + 1) for i in range(1, len(poly) - 1)]
    pieces = hertel_mehlhorn(poly, fan)
    check_partition(poly, pieces, fan)
    check_essential(poly, pieces)


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        ear_clipping([(0, 0), (0, 2), (2, 0)])  # clockwise
    with pytest.raises(ValueError):
        hertel_mehlhorn([(0, 0), (1, 0), (2, 0)], [(0, 1, 2)])


def test_random_polygons() -> None:
    rng = random.Random(20261109)
    done = 0
    while done < 700:
        poly = random_simple(rng, rng.randint(3, 16), rng.choice([5, 8, 12, 20]))
        if poly is None:
            continue
        if rng.random() < 0.4:
            poly = add_collinear(rng, poly)
            if not is_simple(poly):
                continue
        k = rng.randrange(len(poly))
        poly = poly[k:] + poly[:k]
        tris = ear_clipping(poly)
        assert len(tris) == len(poly) - 2
        pieces = hertel_mehlhorn(poly, tris)
        check_partition(poly, pieces, tris)
        check_essential(poly, pieces)
        done += 1


def test_ratio_against_brute_force() -> None:
    rng = random.Random(77)
    done = worse = 0
    while done < 150:
        poly = random_simple(rng, rng.randint(4, 8), 6)
        if poly is None or len(poly) > 8:
            continue
        got = len(convex_partition(poly))
        best = min_convex_by_brute_force(poly)
        assert best <= got < 4 * best
        worse += got > best
        done += 1
    assert worse > 0  # the method is not optimal on some inputs
