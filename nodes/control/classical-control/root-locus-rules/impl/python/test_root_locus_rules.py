# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/root-locus-rules/. The authors are listed in prov/V7FWWP.jsonl.

import cmath
import math
import random

import pytest

from ctlmat import polyroots, polyval
from root_locus_rules import closed_loop_poly, poly_from_roots, root_locus_rules

# Closed-loop roots come from ctlmat.polyroots (Durand-Kerner, float).
# Tolerances: 1e-9 on simple roots, 1e-6 on double roots, 1 degree on
# angles read from roots at a distance 1e-3 from a pole or a zero.

SQ2, SQ3 = math.sqrt(2.0), math.sqrt(3.0)


def angle_deg(z):
    return math.degrees(cmath.phase(z)) % 360.0


def angle_gap(a, b):
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def match_angles(got, want, tol):
    """True if the two lists of angles agree as multisets, within tol degrees."""
    left = list(want)
    for a in got:
        best = min(range(len(left)), key=lambda i: angle_gap(a, left[i]))
        if angle_gap(a, left[best]) > tol:
            return False
        left.pop(best)
    return not left


def on_segments(x, segs, tol=1e-6):
    return any(lo - tol <= x <= hi + tol for lo, hi in segs)


def test_third_order_check_values():
    r = root_locus_rules([0, -1, -2])
    assert r.segments == [(-math.inf, -2.0), (-1.0, 0.0)]
    assert r.centroid == -1.0 and r.asymptote_angles == [60.0, 180.0, 300.0]
    assert len(r.breakaways) == 1
    s, k = r.breakaways[0]
    assert abs(s - (-1 + 1 / SQ3)) < 1e-12 and abs(k - 2 / (3 * SQ3)) < 1e-12
    assert len(r.crossings) == 1
    w, k = r.crossings[0]
    assert abs(w - SQ2) < 1e-12 and abs(k - 6.0) < 1e-12
    assert [a for _, (a,) in r.departures] == [180.0, 0.0, 180.0]
    # at K = 6 the closed loop is (s + 3)(s^2 + 2)
    roots = polyroots(closed_loop_poly(poly_from_roots([0, -1, -2]), [1.0], 6.0))
    assert abs(roots[0] + 3) < 1e-9 and abs(roots[1] + SQ2 * 1j) < 1e-9


def test_complex_poles_and_a_zero():
    r = root_locus_rules([-1 + 1j, -1 - 1j], [-2])
    assert r.segments == [(-math.inf, -2.0)]
    assert r.asymptote_angles == [180.0]
    (s, k), = r.breakaways
    assert abs(s - (-2 - SQ2)) < 1e-12 and abs(k - (2 + 2 * SQ2)) < 1e-10
    dep = dict((p, a) for p, a in r.departures)
    assert abs(dep[-1 + 1j][0] - 135.0) < 1e-9 and abs(dep[-1 - 1j][0] - 225.0) < 1e-9
    assert abs(r.arrivals[0][1][0] - 180.0) < 1e-9
    assert r.crossings == []
    # the complex branch is the circle |s + 2| = sqrt 2
    for k in (0.5, 1.0, 2.0, 4.0):
        for z in polyroots(closed_loop_poly(poly_from_roots([-1 + 1j, -1 - 1j]), [1.0, 2.0], k)):
            assert abs(abs(z + 2) - SQ2) < 1e-9


def test_triple_pole_ultimate_gain():
    r = root_locus_rules([-1, -1, -1])
    assert r.segments == [(-math.inf, -1.0)]
    assert r.breakaways == []
    (p, angles), = r.departures
    assert p == -1 and match_angles(angles, [60.0, 180.0, 300.0], 1e-9)
    (w, k), = r.crossings
    assert abs(w - SQ3) < 1e-12 and abs(k - 8.0) < 1e-12


def test_lead_design_loop():
    # K / (s (s + 2)(s + 6)) with K = 117/8 has the poles -6.5 and -0.75 +- 1.299j
    roots = polyroots(closed_loop_poly(poly_from_roots([0, -2, -6]), [1.0], 117 / 8))
    assert abs(roots[0] + 6.5) < 1e-9
    assert abs(roots[1] - complex(-0.75, -1.5 * SQ3 / 2)) < 1e-9
    r = root_locus_rules([0, -2, -6])
    (w, k), = r.crossings
    assert abs(w - math.sqrt(12)) < 1e-12 and abs(k - 96.0) < 1e-9


def test_imaginary_axis_on_locus():
    r = root_locus_rules([1j, -1j])
    assert r.imaginary_axis_on_locus and r.crossings == []
    assert r.segments == [] and r.breakaways == []
    assert match_angles([a for _, (a,) in r.departures], [90.0, 270.0], 1e-9)


def test_crossing_at_the_origin():
    # (s - 1)(s + 2) + K: a real pole passes 0 at K = 2
    r = root_locus_rules([1, -2])
    assert (0.0, 2.0) in [(w, round(k, 12)) for w, k in r.crossings]


def test_bad_input():
    with pytest.raises(ValueError):
        root_locus_rules([])
    with pytest.raises(ValueError):
        root_locus_rules([-1], [-2, -3])
    with pytest.raises(ValueError):
        root_locus_rules([-1 + 1j, -2])
    with pytest.raises(ValueError):
        root_locus_rules([-1, -2], [-1])


def random_case(rng):
    """Poles and zeros of a random real G, with distinct values at least 0.2 apart."""
    while True:
        n = rng.randint(1, 5)
        m = rng.randint(0, n)
        values = []

        def fill(count):
            out = []
            while len(out) < count:
                if count - len(out) >= 2 and rng.random() < 0.4:
                    a, b = rng.uniform(-4, 1), rng.uniform(0.3, 3)
                    out += [complex(a, b), complex(a, -b)]
                elif out and rng.random() < 0.2 and abs(out[-1].imag) == 0:
                    out.append(out[-1])
                else:
                    out.append(complex(rng.uniform(-5, 1.5), 0.0))
            return out
        poles, zeros = fill(n), fill(m)
        values = []
        for v in poles + zeros:
            if all(v != w for w in values):
                values.append(v)
        if any(abs(v - w) < 0.2 for i, v in enumerate(values) for w in values[:i]):
            continue
        if any(z == p for z in zeros for p in poles):
            continue
        return poles, zeros


def kgrid(lo, hi, count):
    return [lo * (hi / lo) ** (i / (count - 1)) for i in range(count)]


def cases(seed, count):
    rng = random.Random(seed)
    return [random_case(rng) for _ in range(count)]


def test_real_axis_rule_random():
    for poles, zeros in cases(1, 60):
        r = root_locus_rules(poles, zeros)
        den, num = poly_from_roots(poles), poly_from_roots(zeros)
        crit = [v.real for v in poles + zeros if v.imag == 0]
        for i in range(301):
            x = -10 + 15 * i / 300 + 0.001
            if any(abs(x - c) < 1e-3 for c in crit):
                continue
            k = -polyval(den, x) / polyval(num, x)
            assert (k > 0) == on_segments(x, r.segments, 0.0), (poles, zeros, x)
        # every real closed-loop pole lies on a segment
        for k in kgrid(1e-3, 1e3, 13):
            for z in polyroots(closed_loop_poly(den, num, k)):
                if z.imag == 0:
                    assert on_segments(z.real, r.segments, 1e-6 * (1 + abs(z))), (poles, zeros, k, z)


def test_asymptotes_random():
    for poles, zeros in cases(2, 60):
        r = root_locus_rules(poles, zeros)
        q = len(poles) - len(zeros)
        if q == 0:
            assert r.centroid is None and r.asymptote_angles == []
            continue
        den, num = poly_from_roots(poles), poly_from_roots(zeros)
        k = 1e8
        roots = sorted(polyroots(closed_loop_poly(den, num, k)), key=abs)
        far = roots[-q:]
        assert match_angles([angle_deg(z - r.centroid) for z in far], r.asymptote_angles, 1.0)
        if q >= 2:
            mean = sum(far) / q
            assert abs(mean - r.centroid) < 1e-3, (poles, zeros)


def test_departure_and_arrival_random():
    for poles, zeros in cases(3, 60):
        r = root_locus_rules(poles, zeros)
        den, num = poly_from_roots(poles), poly_from_roots(zeros)
        rho = 1e-3
        for p, angles in r.departures:
            mu = len(angles)
            rest = [q for q in poles if q != p]
            c = abs(polyval(num, p)) / math.prod(abs(p - q) for q in rest)
            k = rho ** mu / c
            near = [z for z in polyroots(closed_loop_poly(den, num, k)) if abs(z - p) < 10 * rho]
            assert len(near) == mu
            assert match_angles([angle_deg(z - p) for z in near], angles, 1.0), (poles, zeros, p)
        for zr, angles in r.arrivals:
            nu = len(angles)
            rest = [y for y in zeros if y != zr]
            c = abs(polyval(den, zr)) / math.prod(abs(zr - y) for y in rest)
            k = c / rho ** nu
            near = [z for z in polyroots(closed_loop_poly(den, num, k)) if abs(z - zr) < 10 * rho]
            assert len(near) == nu
            assert match_angles([angle_deg(z - zr) for z in near], angles, 1.0), (poles, zeros, zr)


def count_changes(den, num, grid, predicate):
    """Indices i where the number of closed-loop roots with the property changes from grid[i] to grid[i + 1]."""
    counts = [sum(1 for z in polyroots(closed_loop_poly(den, num, k)) if predicate(z)) for k in grid]
    return [i for i in range(len(grid) - 1) if counts[i] != counts[i + 1]]


def test_breakaways_and_crossings_random():
    grid = kgrid(1e-3, 1e3, 91)
    for poles, zeros in cases(4, 25):
        r = root_locus_rules(poles, zeros)
        den, num = poly_from_roots(poles), poly_from_roots(zeros)
        for s, k in r.breakaways:
            roots = polyroots(closed_loop_poly(den, num, k))
            assert sum(1 for z in roots if abs(z - s) < 1e-6 * (1 + abs(s))) >= 2, (poles, zeros, s, k)
        for w, k in r.crossings:
            roots = polyroots(closed_loop_poly(den, num, k))
            assert min(abs(z - 1j * w) for z in roots) < 1e-6 * (1 + w), (poles, zeros, w, k)
        real_k = [k for s, k in r.breakaways if s.imag == 0]
        for i in count_changes(den, num, grid, lambda z: z.imag == 0):
            lo, hi = grid[max(i - 1, 0)], grid[min(i + 2, len(grid) - 1)]
            assert any(lo <= k <= hi for k in real_k), (poles, zeros, grid[i])
        cross_k = [k for w, k in r.crossings]
        for i in count_changes(den, num, grid, lambda z: z.real > 0):
            lo, hi = grid[max(i - 1, 0)], grid[min(i + 2, len(grid) - 1)]
            assert any(lo <= k <= hi for k in cross_k), (poles, zeros, grid[i])
