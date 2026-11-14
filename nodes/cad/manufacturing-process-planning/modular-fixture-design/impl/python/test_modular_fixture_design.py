# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modular-fixture-design/. The authors are listed in prov/SBR91R.jsonl.

import random
import unittest
from fractions import Fraction
from itertools import combinations, product
from math import isqrt

from modular_fixture_design import DIRECTIONS, Q2, diameter_sq, fixtures, form_closure

TRIANGLE = [(0, 0), (2, 0), (1, Fraction(3, 2))]
RIGHT = [(0, 0), (2, 0), (0, Fraction(3, 2))]
QUAD = [(0, 0), (Fraction(3, 2), 0), (Fraction(3, 2), 1), (0, Fraction(3, 2))]


def sgn(x):
    if isinstance(x, Q2):
        return x.sign()
    return (x > 0) - (x < 0)


def solve3(cols, target):
    """Solve sum_j x_j cols[j] = target for three vectors of R^3 by Cramer's rule."""

    def det(a, b, c):
        return a[0] * (b[1] * c[2] - b[2] * c[1]) - b[0] * (a[1] * c[2] - a[2] * c[1]) + c[0] * (a[1] * b[2] - a[2] * b[1])

    d = det(*cols)
    if sgn(d) == 0:
        return None
    return [
        det(target, cols[1], cols[2]) / d,
        det(cols[0], target, cols[2]) / d,
        det(cols[0], cols[1], target) / d,
    ]


def closure_by_caratheodory(wrenches):
    """Each of +-e_k is a nonnegative combination of three of the wrenches."""
    for k in range(3):
        for s in (1, -1):
            target = [0, 0, 0]
            target[k] = s
            ok = False
            for trio in combinations(wrenches, 3):
                x = solve3(list(trio), target)
                if x is not None and all(sgn(v) >= 0 for v in x):
                    ok = True
                    break
            if not ok:
                return False
    return True


def poses_by_linear_family(poly, sites, chosen):
    """Poses from the linear system in (c, s, T1, T2), T = R^T t, then c^2 + s^2 = 1.

    The condition for site q on the line m . x = h of an edge in the part
    frame is m . R^T (q - t) = h, that is c (m . q) + s (m x q) - m . T = h.
    """
    n = len(poly)
    rows = []
    for q, e in zip(sites, chosen):
        p0 = poly[e]
        p1 = poly[(e + 1) % n]
        m = (Fraction(p1[1]) - p0[1], Fraction(p0[0]) - p1[0])
        h = m[0] * p0[0] + m[1] * p0[1]
        rows.append([m[0] * q[0] + m[1] * q[1], m[0] * q[1] - m[1] * q[0], -m[0], -m[1], h])
    # Gauss-Jordan on the 3 x 5 augmented matrix.
    a = [list(r) for r in rows]
    piv_cols = []
    r = 0
    for c in range(4):
        piv = next((i for i in range(r, 3) if a[i][c] != 0), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        a[r] = [v / a[r][c] for v in a[r]]
        for i in range(3):
            if i != r and a[i][c] != 0:
                f = a[i][c]
                a[i] = [x - f * y for x, y in zip(a[i], a[r])]
        piv_cols.append(c)
        r += 1
    if r < 3:
        return []
    free = next(c for c in range(4) if c not in piv_cols)
    x0 = [Fraction(0)] * 4
    x1 = [Fraction(0)] * 4
    x1[free] = Fraction(1)
    for i, c in enumerate(piv_cols):
        x0[c] = a[i][4]
        x1[c] = -a[i][free]
    qa = x1[0] ** 2 + x1[1] ** 2
    qb = 2 * (x0[0] * x1[0] + x0[1] * x1[1])
    qc = x0[0] ** 2 + x0[1] ** 2 - 1
    out = []
    if qa == 0:
        if qb == 0:
            return []
        taus = [Q2(-qc / qb)]
    else:
        disc = qb * qb - 4 * qa * qc
        if disc < 0:
            return []
        rp, rq = isqrt(disc.numerator), isqrt(disc.denominator)
        if rp * rp == disc.numerator and rq * rq == disc.denominator:
            root = Fraction(rp, rq)
            taus = [Q2((-qb + root) / (2 * qa)), Q2((-qb - root) / (2 * qa))]
        else:
            taus = [Q2(-qb / (2 * qa), 1 / (2 * qa), disc), Q2(-qb / (2 * qa), -1 / (2 * qa), disc)]
        if disc == 0:
            taus = taus[:1]
    for tau in taus:
        c, s, t1, t2 = (x0[k] + tau * x1[k] for k in range(4))
        out.append((c, s, t1, t2))
    return out


def brute_force(poly, reach=1):
    """All fixtures, found by trying every triple of holes in a box and every clamp hole near it."""
    n = len(poly)
    poly = [tuple(Fraction(v) for v in p) for p in poly]
    # The holes of a fixture are points of the part, so their x range and
    # their y range are at most the diameter. A translation by an integer
    # vector moves them into [0, floor(diameter)]^2.
    big = isqrt(int(diameter_sq(poly)))
    box = [(x, y) for x in range(big + 1) for y in range(big + 1)]
    keys = set()
    for sites in combinations(box, 3):
        for chosen in product(range(n), repeat=3):
            for c, s, t1, t2 in poses_by_linear_family(poly, sites, chosen):
                # Contact points in the part frame: R^T q - T.
                local = [(c * q[0] + s * q[1] - t1, -s * q[0] + c * q[1] - t2) for q in sites]
                if not all(inside_edge(poly, e, x) for e, x in zip(chosen, local)):
                    continue
                wrenches = [wrench_world(poly, e, q, c, s) for e, q in zip(chosen, sites)]
                tx, ty = c * t1 - s * t2, s * t1 + c * t2
                world = [
                    (float(c * p[0] - s * p[1] + tx), float(s * p[0] + c * p[1] + ty)) for p in poly
                ]
                for v in product(range(-big - 3, 2 * big + 4), repeat=2):
                    # A clamp at v touches the part within reach, so v is
                    # within reach of the boundary. This float test keeps a
                    # margin and never drops such a hole.
                    if near_boundary(world, v) > reach + 1e-7:
                        continue
                    for d in DIRECTIONS:
                        hit = clamp_hit(poly, v, d, c, s, t1, t2, reach)
                        if hit is None:
                            continue
                        e, u = hit
                        if any(sgn(u[0] - q[0]) == 0 and sgn(u[1] - q[1]) == 0 for q in sites):
                            continue
                        if not closure_by_caratheodory(wrenches + [wrench_world(poly, e, u, c, s)]):
                            continue
                        keys.add(canonical(sites, chosen, (c, s, tx, ty), v, d, e))
    return keys


def near_boundary(world, v):
    """Float distance from the point v to the boundary of the polygon."""
    best = float("inf")
    n = len(world)
    for k in range(n):
        a, b = world[k], world[(k + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        u = ((v[0] - a[0]) * dx + (v[1] - a[1]) * dy) / (dx * dx + dy * dy)
        u = max(0.0, min(1.0, u))
        ex, ey = a[0] + u * dx - v[0], a[1] + u * dy - v[1]
        best = min(best, (ex * ex + ey * ey) ** 0.5)
    return best


def inside_edge(poly, e, x):
    """x lies strictly inside edge e of the polygon (part frame)."""
    n = len(poly)
    p, q = poly[e], poly[(e + 1) % n]
    d = (q[0] - p[0], q[1] - p[1])
    w = (x[0] - p[0], x[1] - p[1])
    if sgn(d[0] * w[1] - d[1] * w[0]) != 0:
        return False
    u = d[0] * w[0] + d[1] * w[1]
    return sgn(u) > 0 and sgn(d[0] * d[0] + d[1] * d[1] - u) > 0


def wrench_world(poly, e, point, c, s):
    n = len(poly)
    p, q = poly[e], poly[(e + 1) % n]
    m_in = (p[1] - q[1], q[0] - p[0])  # inner normal of a counterclockwise polygon
    w = (c * m_in[0] - s * m_in[1], s * m_in[0] + c * m_in[1])
    return [w[0], w[1], point[0] * w[1] - point[1] * w[0]]


def clamp_hit(poly, v, d, c, s, t1, t2, reach):
    """Work in the part frame. The first boundary point on the ray from v
    must be in an edge interior, at distance at most reach, and entering
    the part (which also proves that v is outside)."""
    n = len(poly)
    vl = (c * v[0] + s * v[1] - t1, -s * v[0] + c * v[1] - t2)
    dl = (c * d[0] + s * d[1], -s * d[0] + c * d[1])
    for k in range(n):
        if inside_edge(poly, k, vl):
            return None
    best = None
    for k in range(n):
        p, q = poly[k], poly[(k + 1) % n]
        e = (q[0] - p[0], q[1] - p[1])
        den = dl[0] * (-e[1]) + e[0] * dl[1]  # det [dl, -e]
        if sgn(den) == 0:
            continue
        r = (p[0] - vl[0], p[1] - vl[1])
        sd = (r[0] * (-e[1]) + e[0] * r[1]) / den
        lam = (dl[0] * r[1] - dl[1] * r[0]) / den
        if sgn(sd) <= 0 or sgn(lam) < 0 or sgn(lam - 1) > 0:
            continue
        vertex = sgn(lam) == 0 or sgn(lam - 1) == 0
        if best is None or sgn(sd - best[0]) < 0:
            best = (sd, k, vertex)
        elif sgn(sd - best[0]) == 0:
            best = (sd, k, True)
    # A vertex on the ray that is not on any crossing edge (touching) is
    # also found above as an end of two edges.
    if best is None or best[2] or sgn(best[0] - reach) > 0:
        return None
    sd, k, _ = best
    p, q = poly[k], poly[(k + 1) % n]
    m_out = (q[1] - p[1], p[0] - q[0])
    if sgn(dl[0] * m_out[0] + dl[1] * m_out[1]) >= 0:
        return None  # leaving the part: v was inside
    u = (v[0] + sd * d[0], v[1] + sd * d[1])
    return k, u


def canonical(sites, chosen, pose, v, d, e):
    pairs = sorted(zip(sites, chosen))
    ox, oy = pairs[0][0]
    shifted = tuple(((q[0] - ox, q[1] - oy), ed) for q, ed in pairs)
    c, s, tx, ty = pose
    pose_key = tuple(round(float(x), 9) for x in (c, s, tx - ox, ty - oy))
    return (shifted, pose_key, (v[0] - ox, v[1] - oy), d, e)


def key_of(f):
    return canonical(f.locators, f.edges, f.pose, f.clamp[0], f.clamp[1], f.clamp[2])


class TestQ2(unittest.TestCase):
    def test_sign_against_float(self):
        rng = random.Random(1)
        for _ in range(2000):
            a = Fraction(rng.randint(-50, 50), rng.randint(1, 9))
            b = Fraction(rng.randint(-50, 50), rng.randint(1, 9))
            d = Fraction(rng.choice([2, 3, 5, 7, 11, 13]), rng.choice([1, 4, 9]))
            x = Q2(a, b, d)
            f = float(a) + float(b) * float(d) ** 0.5
            self.assertEqual(x.sign(), (f > 0) - (f < 0))

    def test_field_operations(self):
        x = Q2(1, 2, 3)
        y = Q2(Fraction(1, 2), -1, 3)
        self.assertAlmostEqual(float(x * y), float(x) * float(y))
        self.assertAlmostEqual(float(x / y), float(x) / float(y))
        self.assertEqual((x - x).sign(), 0)


class TestFormClosure(unittest.TestCase):
    def test_pinwheel_and_symmetric_square(self):
        def w(p, n):
            return [n[0], n[1], p[0] * n[1] - p[1] * n[0]]

        half = Fraction(1, 2)
        pin = [w((0, 3 * half), (1, 0)), w((2, half), (-1, 0)), w((3 * half, 0), (0, 1)), w((half, 2), (0, -1))]
        sym = [w((0, 1), (1, 0)), w((2, 1), (-1, 0)), w((1, 0), (0, 1)), w((1, 2), (0, -1))]
        self.assertTrue(form_closure(pin))
        self.assertFalse(form_closure(sym))

    def test_against_caratheodory(self):
        rng = random.Random(4)
        for _ in range(400):
            ws = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(4)]
            self.assertEqual(form_closure(ws), closure_by_caratheodory(ws))


class TestAgainstBruteForce(unittest.TestCase):
    def check(self, poly):
        found = fixtures(poly)
        keys = [key_of(f) for f in found]
        self.assertEqual(len(keys), len(set(keys)), "a fixture was listed twice")
        self.assertEqual(set(keys), brute_force(poly))
        return found

    def test_isosceles_triangle(self):
        found = self.check(TRIANGLE)
        self.assertGreater(len(found), 0)

    def test_quadrilateral(self):
        found = self.check(QUAD)
        self.assertGreater(len(found), 0)

    def test_each_fixture_is_valid(self):
        for f in fixtures(RIGHT):
            c, s, tx, ty = f.pose
            self.assertEqual(sgn(c * c + s * s - 1), 0)
            self.assertEqual(f.locators[0], (0, 0))
            self.assertTrue(f.locators[0] < f.locators[1] < f.locators[2])
            t1, t2 = c * tx + s * ty, -s * tx + c * ty
            poly = [tuple(Fraction(v) for v in p) for p in RIGHT]
            for q, e in zip(f.locators, f.edges):
                local = (c * q[0] + s * q[1] - t1, -s * q[0] + c * q[1] - t2)
                self.assertTrue(inside_edge(poly, e, local))
            v, d, e, u = f.clamp
            self.assertEqual(clamp_hit(poly, v, d, c, s, t1, t2, 1)[0], e)
            ws = [wrench_world(poly, ed, q, c, s) for ed, q in zip(f.edges, f.locators)]
            self.assertTrue(closure_by_caratheodory(ws + [wrench_world(poly, e, u, c, s)]))


if __name__ == "__main__":
    unittest.main()
