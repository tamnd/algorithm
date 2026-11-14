# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sweep-representation/. The authors are listed in prov/QNVPYX.jsonl.

import math
import random
import unittest
from fractions import Fraction as F

from sweep_representation import IN, ON, OUT, Extrusion, Revolution, area2, is_simple

EPS = F(1, 1000)


# ---------------------------------------------------------------------------
# Independent oracles. The profile test is a winding number, not the crossing
# number of the implementation, and the sweep is the plain union of M(t) X
# over a finite sample of the parameter t.
# ---------------------------------------------------------------------------

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def in_closed_polygon(poly, q):
    """Winding number with an exact on-edge test. True for points of the
    closed polygon."""
    n = len(poly)
    w = 0
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if cross(a, b, q) == 0 and min(a[0], b[0]) <= q[0] <= max(a[0], b[0]) \
                and min(a[1], b[1]) <= q[1] <= max(a[1], b[1]):
            return True
        if a[1] <= q[1]:
            if b[1] > q[1] and cross(a, b, q) > 0:
                w += 1
        elif b[1] <= q[1] and cross(a, b, q) < 0:
            w -= 1
    return w != 0


def extrusion_member(profile, d, p, ts):
    """p is in the union of X + t d over the sampled t."""
    for t in ts:
        if p[2] == t * d[2] and in_closed_polygon(profile, (p[0] - t * d[0], p[1] - t * d[1])):
            return True
    return False


def rot(c, s, p):
    return (c * p[0] - s * p[1], s * p[0] + c * p[1], p[2])


def revolution_member(profile, p, rots):
    """p is in the union of R(a) X over the sampled rotations R(a), where X
    sits in the half-plane y = 0, x >= 0."""
    for c, s in rots:
        x, y, z = rot(c, -s, p)  # R(a)^-1 p
        if y == 0 and x >= 0 and in_closed_polygon(profile, (x, z)):
            return True
    return False


def pythagorean_rotations(limit):
    """Rational rotations (cos, sin) = ((a^2 - b^2)/h, 2ab/h), h = a^2 + b^2,
    together with their quarter turns and their negatives."""
    out = {(F(1), F(0))}
    for a in range(1, limit + 1):
        for b in range(0, limit + 1):
            h = a * a + b * b
            c, s = F(a * a - b * b, h), F(2 * a * b, h)
            for cc, ss in ((c, s), (-s, c), (-c, -s), (s, -c)):
                out.add((cc, ss))
    return sorted(out)


ROTS = pythagorean_rotations(3)


def primitive_directions(m):
    return [(a, b) for a in range(-m, m + 1) for b in range(-m, m + 1)
            if (a, b) != (0, 0) and math.gcd(a, b) == 1]


DIRS = primitive_directions(8)


def random_star_polygon(rng, lo=0, hi=4):
    """A simple lattice polygon: lattice points sorted by angle around a
    centre that is on no line through two lattice points of the box."""
    while True:
        k = rng.randrange(3, 8)
        pts = list({(rng.randrange(lo, hi + 1), rng.randrange(lo, hi + 1)) for _ in range(k)})
        if len(pts) < 3:
            continue
        cx, cy = sum(p[0] for p in pts) / len(pts) + 0.0137, sum(p[1] for p in pts) / len(pts) + 0.0071
        pts.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
        poly = [(F(x), F(y)) for x, y in pts]
        if is_simple(poly):
            if area2(poly) < 0:
                poly.reverse()
            return poly


def random_rational(rng, lo, hi, den=4):
    return F(rng.randrange(lo * den, hi * den + 1), den)


class TestHandCases(unittest.TestCase):
    def test_oblique_prism(self):
        e = Extrusion([(0, 0), (2, 0), (2, 2), (0, 2)], (1, 0, 3))
        self.assertTrue(e.check_invariant())
        self.assertEqual(e.classify((2, 1, F(3, 2))), IN)
        self.assertEqual(e.classify((3, 1, 3)), ON)
        self.assertEqual(e.classify((F(1, 5), 1, F(3, 2))), OUT)
        self.assertEqual(e.classify((1, 1, 0)), ON)
        self.assertEqual(e.classify((1, 1, -1)), OUT)
        self.assertEqual(e.volume(), 12)

    def test_ring_and_cylinder(self):
        ring = Revolution([(1, 0), (2, 0), (2, 1), (1, 1)])
        self.assertTrue(ring.check_invariant())
        self.assertEqual(ring.classify((1, 1, F(1, 2))), IN)       # radius sqrt 2
        self.assertEqual(ring.classify((0, 0, F(1, 2))), OUT)
        self.assertEqual(ring.classify((F(3, 5), F(4, 5), F(1, 2))), ON)  # radius 1
        self.assertEqual(ring.volume_over_pi(), 3)
        cyl = Revolution([(0, 0), (2, 0), (2, 1), (0, 1)])
        self.assertEqual(cyl.classify((0, 0, F(1, 2))), IN)        # axis point
        self.assertEqual(cyl.classify((0, 0, 1)), ON)
        self.assertEqual(cyl.classify((1, 1, 1)), ON)               # top face, radius sqrt 2
        self.assertEqual(cyl.classify((1, 1, F(1, 2))), IN)
        self.assertEqual(cyl.classify((2, 1, F(1, 2))), OUT)        # radius sqrt 5
        self.assertEqual(cyl.volume_over_pi(), 4)

    def test_cone_apex(self):
        cone = Revolution([(0, 0), (1, 0), (0, 1)])
        self.assertEqual(cone.classify((0, 0, 1)), ON)
        self.assertEqual(cone.classify((0, 0, F(1, 2))), IN)
        self.assertEqual(cone.volume_over_pi(), F(1, 3))

    def test_invalid(self):
        self.assertFalse(Extrusion([(0, 0), (1, 0), (0, 1)], (1, 1, 0)).check_invariant())
        self.assertFalse(Revolution([(-1, 0), (1, 0), (0, 1)]).check_invariant())
        self.assertFalse(Revolution([(0, 0), (2, 2), (2, 0), (0, 2)]).check_invariant())


class TestExtrusionAgainstSampling(unittest.TestCase):
    def test_membership(self):
        rng = random.Random(11)
        n = 20
        for _ in range(500):
            poly = random_star_polygon(rng)
            d = (rng.randrange(-2, 3), rng.randrange(-2, 3), rng.choice([-3, -2, -1, 1, 2, 3]))
            d = tuple(F(v) for v in d)
            e = Extrusion(poly, d)
            ts = [F(k, n) for k in range(-2, n + 3)]
            t = rng.choice(ts)
            p = (random_rational(rng, -3, 7), random_rational(rng, -3, 7), t * d[2])
            want = extrusion_member(poly, d, p, [x for x in ts if 0 <= x <= 1])
            self.assertEqual(e.classify(p) != OUT, want, (poly, d, p))

    def test_in_and_on_by_probes(self):
        rng = random.Random(12)
        n = 4
        for _ in range(300):
            poly = random_star_polygon(rng)
            d = (F(rng.randrange(-2, 3)), F(rng.randrange(-2, 3)), F(rng.choice([1, 2, 3])))
            e = Extrusion(poly, d)
            t = F(rng.randrange(0, n + 1), n)
            q = (random_rational(rng, 0, 4), random_rational(rng, 0, 4))
            p = (q[0] + t * d[0], q[1] + t * d[1], t * d[2])
            got = e.classify(p)
            ts = [t, t - EPS, t + EPS]
            ts = [x for x in ts if 0 <= x <= 1]
            if not extrusion_member(poly, d, p, ts):
                self.assertEqual(got, OUT)
                continue
            probes = [(p[0] + EPS * a, p[1] + EPS * b, p[2]) for a, b in DIRS]
            probes += [tuple(p[i] + sg * EPS * d[i] for i in range(3)) for sg in (1, -1)]
            inside = all(extrusion_member(poly, d, x, ts) for x in probes)
            self.assertEqual(got, IN if inside else ON, (poly, d, p))

    def test_sweep_of_profile_points(self):
        """Every point x + t d with x in X and t in [0, 1] is in the solid."""
        rng = random.Random(13)
        for _ in range(500):
            poly = random_star_polygon(rng)
            d = (F(rng.randrange(-2, 3)), F(rng.randrange(-2, 3)), F(rng.choice([-2, -1, 1, 2])))
            e = Extrusion(poly, d)
            x = rng.choice(poly) if rng.random() < 0.3 else \
                (random_rational(rng, 0, 4, 7), random_rational(rng, 0, 4, 7))
            if not in_closed_polygon(poly, x):
                continue
            t = F(rng.randrange(0, 1001), 1000)
            p = (x[0] + t * d[0], x[1] + t * d[1], t * d[2])
            self.assertNotEqual(e.classify(p), OUT)

    def test_volume_against_grid(self):
        rng = random.Random(14)
        for _ in range(3):
            poly = random_star_polygon(rng)
            d = (F(1), F(0), F(2))
            e = Extrusion(poly, d)
            m = 8
            count = 0
            for i in range(m):
                for j in range(5 * m):
                    for k in range(5 * m):
                        p = (F(2 * j + 1, 2 * m) - 0, F(2 * k + 1, 2 * m), F(2 * i + 1, m))
                        if e.classify(p) != OUT:
                            count += 1
            est = F(count, m * m * m) * 2
            self.assertLess(abs(float(est - e.volume())), 0.6)


class TestRevolutionAgainstSampling(unittest.TestCase):
    def profile(self, rng):
        poly = random_star_polygon(rng)
        if rng.random() < 0.5:
            shift = min(r for r, _ in poly)
            poly = [(r - shift, z) for r, z in poly]
        return poly

    def test_membership(self):
        rng = random.Random(21)
        for _ in range(500):
            poly = self.profile(rng)
            v = Revolution(poly)
            self.assertTrue(v.check_invariant())
            c, s = rng.choice(ROTS)
            base = (random_rational(rng, 0, 5), F(0), random_rational(rng, -1, 5))
            if rng.random() < 0.1:
                base = (F(0), F(0), base[2])
            p = rot(c, s, base)
            want = revolution_member(poly, p, ROTS)
            self.assertEqual(v.classify(p) != OUT, want, (poly, p))

    def test_in_and_on_by_probes(self):
        rng = random.Random(22)
        tiny = (F(1000 * 1000 - 1, 1000 * 1000 + 1), F(2 * 1000, 1000 * 1000 + 1))
        for _ in range(300):
            poly = self.profile(rng)
            v = Revolution(poly)
            c, s = rng.choice(ROTS)
            r = random_rational(rng, 0, 4) if rng.random() < 0.8 else F(0)
            z = random_rational(rng, 0, 4)
            p = rot(c, s, (r, F(0), z))
            got = v.classify(p)
            rots = list(ROTS)
            # the turns that bring the probes back into the profile half-plane
            rots += [(c * tiny[0] - s * tiny[1], s * tiny[0] + c * tiny[1]),
                     (c * tiny[0] + s * tiny[1], s * tiny[0] - c * tiny[1])]
            if not revolution_member(poly, p, rots):
                self.assertEqual(got, OUT)
                continue
            # probes in the half-plane of p, and two small turns of p
            probes = [rot(c, s, (r + EPS * a, F(0), z + EPS * b)) for a, b in DIRS]
            probes += [rot(tiny[0], tiny[1], p), rot(tiny[0], -tiny[1], p)]
            inside = all(revolution_member(poly, x, rots) for x in probes)
            self.assertEqual(got, IN if inside else ON, (poly, p))

    def test_irrational_radius_against_floats(self):
        rng = random.Random(23)
        checked = 0
        for _ in range(500):
            poly = self.profile(rng)
            v = Revolution(poly)
            p = (random_rational(rng, -4, 4, 3), random_rational(rng, -4, 4, 3),
                 random_rational(rng, 0, 4, 3))
            r = math.hypot(float(p[0]), float(p[1]))
            z = float(p[2])
            q = (r, z)
            fpoly = [(float(a), float(b)) for a, b in poly]
            # distance from (r, z) to the profile boundary, in floats
            dist = min(seg_dist(q, fpoly[i], fpoly[(i + 1) % len(fpoly)]) for i in range(len(fpoly)))
            if dist < 1e-6:
                continue
            want = IN if in_closed_polygon(fpoly, q) else OUT
            self.assertEqual(v.classify(p), want, (poly, p))
            checked += 1
        self.assertGreater(checked, 400)

    def test_volume_against_grid(self):
        rng = random.Random(24)
        for _ in range(5):
            poly = self.profile(rng)
            v = Revolution(poly)
            m = 40
            total = 0.0
            for i in range(4 * m):
                for j in range(4 * m):
                    rr, zz = (i + 0.5) / m, (j + 0.5) / m
                    if in_closed_polygon([(float(a), float(b)) for a, b in poly], (rr, zz)):
                        total += 2 * math.pi * rr / (m * m)
            self.assertLess(abs(total - float(v.volume_over_pi()) * math.pi), 0.5)

    def test_rotation_invariance(self):
        rng = random.Random(25)
        for _ in range(500):
            poly = self.profile(rng)
            v = Revolution(poly)
            p = (random_rational(rng, -4, 4, 2), random_rational(rng, -4, 4, 2),
                 random_rational(rng, 0, 4, 2))
            c, s = rng.choice(ROTS)
            self.assertEqual(v.classify(p), v.classify(rot(c, s, p)))


def seg_dist(q, a, b):
    ax, ay = b[0] - a[0], b[1] - a[1]
    t = ((q[0] - a[0]) * ax + (q[1] - a[1]) * ay) / (ax * ax + ay * ay)
    t = max(0.0, min(1.0, t))
    return math.hypot(q[0] - a[0] - t * ax, q[1] - a[1] - t * ay)


if __name__ == "__main__":
    unittest.main()
