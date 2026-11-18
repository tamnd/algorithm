# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/impact-zones/. The authors are listed in prov/BJ4E1Y.jsonl.

"""Tests of rigid impact zones against sampling, exact rational tests and exact identities."""

import math
import random
from fractions import Fraction

from anim import cross2, sub
import impact_zones as iz


def f_cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def exact_segments_meet(p, q, r, s):
    """Exact test with Fractions: do the closed segments pq and rs share a point?"""
    p, q, r, s = ([Fraction(c) for c in pt] for pt in (p, q, r, s))
    d1, d2 = f_cross(r, s, p), f_cross(r, s, q)
    d3, d4 = f_cross(p, q, r), f_cross(p, q, s)
    if ((d1 > 0) != (d2 > 0)) and d1 != 0 and d2 != 0 and ((d3 > 0) != (d4 > 0)) and d3 != 0 and d4 != 0:
        return True

    def on(a, b, c):
        return f_cross(a, b, c) == 0 and min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) \
            and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
    return on(r, s, p) or on(r, s, q) or on(p, q, r) or on(p, q, s)


def exact_interference_free(x, edges):
    for k, (a, b) in enumerate(edges):
        for c, d in edges[k + 1:]:
            if len({a, b, c, d}) == 4 and exact_segments_meet(x[a], x[b], x[c], x[d]):
                return False
        for i in range(len(x)):
            if i not in (a, b) and exact_segments_meet(x[a], x[b], x[i], x[i]):
                return False
    return True


def sampled_time(p0, p1, a0, a1, b0, b1, samples=20000):
    """The first collision by fine sampling of the collinearity sign and bisection."""
    def at(s):
        p, a, b = (iz.lerp_point(u, w, s) for u, w in ((p0, p1), (a0, a1), (b0, b1)))
        return cross2(sub(b, a), sub(p, a)), p, a, b

    prev = at(0.0)[0]
    for k in range(1, samples + 1):
        s = k / samples
        cur = at(s)[0]
        if (prev > 0) != (cur > 0) or cur == 0.0:
            lo, hi = (k - 1) / samples, s
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if (at(mid)[0] > 0) == (prev > 0) and at(mid)[0] != 0.0:
                    lo = mid
                else:
                    hi = mid
            _, p, a, b = at(hi)
            if iz._on_segment(p, a, b):
                return hi
        prev = cur
    return None


def test_point_edge_time_against_sampling_and_bisection():
    rng = random.Random(1)
    hits = 0
    for _ in range(150):
        pts = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(6)]
        got = iz.point_edge_time(*pts)
        want = sampled_time(*pts, samples=3000)
        if want is None:
            assert got is None
        else:
            hits += 1
            assert got is not None and abs(got - want) < 1e-9
    assert hits > 15


def test_collinear_motion():
    # the point slides along the line of the edge and enters it at s = 0.5
    s = iz.point_edge_time((-1.0, 0.0), (1.0, 0.0), (0.0, 0.0), (0.0, 0.0), (1.0, 0.0), (1.0, 0.0))
    assert s == 0.5
    assert iz.point_edge_time((-3.0, 0.0), (-2.0, 0.0), (0.0, 0.0), (0.0, 0.0), (1.0, 0.0), (1.0, 0.0)) is None


def rigid_check(x0, x1, nodes, tol):
    for a in nodes:
        for b in nodes:
            assert abs(math.dist(x0[a], x0[b]) - math.dist(x1[a], x1[b])) <= tol


def test_rigid_zone_recovers_a_rigid_velocity_and_keeps_momentum():
    rng = random.Random(2)
    dt = 0.1
    for _ in range(20):
        nodes = list(range(6))
        x0 = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in nodes]
        mass = [rng.uniform(0.5, 2.0) for _ in nodes]
        c = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        w0 = rng.uniform(-5, 5)
        vt = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        v = [(vt[0] - w0 * (p[1] - c[1]), vt[1] + w0 * (p[0] - c[0])) for p in x0]
        out = iz.rigid_zone_motion(x0, v, mass, nodes, dt)
        x1 = [(x0[i][0] + dt * out[i][0], x0[i][1] + dt * out[i][1]) for i in nodes]
        rigid_check(x0, x1, nodes, 1e-12)
        # the rotation angle is dt w0
        ang = math.atan2(cross2(sub(x0[1], x0[0]), sub(x1[1], x1[0])),
                         sum(a * b for a, b in zip(sub(x0[1], x0[0]), sub(x1[1], x1[0]))))
        assert abs(ang - dt * w0) < 1e-12
        # linear momentum is kept exactly; the angular momentum of the mean velocities is L sin(phi) / phi
        m = sum(mass)
        for k in range(2):
            assert abs(sum(mi * vi[k] for mi, vi in zip(mass, v)) - sum(mass[i] * out[i][k] for i in nodes)) < 1e-12
        xcm = tuple(sum(mi * p[k] for mi, p in zip(mass, x0)) / m for k in range(2))
        lin = [sum(mass[i] * vi[k] for i, vi in enumerate(v)) / m for k in range(2)]

        def ang_mom(vel):
            return sum(mass[i] * cross2(sub(x0[i], xcm), sub(vel[i], lin)) for i in nodes)
        phi = dt * w0
        assert abs(ang_mom(out) - ang_mom(v) * math.sin(phi) / phi) < 1e-12 * max(1.0, abs(ang_mom(v)))


def test_large_angle_falls_back_to_translation():
    x0 = [(1.0, 0.0), (-1.0, 0.0)]
    v = [(0.0, 40.0), (0.0, -40.0)]  # omega = 40 rad/s, dt omega = 4 > pi
    out = iz.rigid_zone_motion(x0, v, [1.0, 1.0], [0, 1], 0.1)
    assert out[0] == (0.0, 0.0) and out[1] == (0.0, 0.0)


def chain(n, x0, y0, spacing, start=0):
    pts = [(x0 + i * spacing, y0) for i in range(n)]
    edges = [(start + i, start + i + 1) for i in range(n - 1)]
    return pts, edges


def components(n, record, edges):
    """Brute force: connected components of the graph of all collisions found."""
    adj = [set() for _ in range(n)]
    for found in record:
        for i, k, _ in found:
            a, b = edges[k]
            for p, q in ((i, a), (i, b), (a, b)):
                adj[p].add(q)
                adj[q].add(p)
    seen, comps = set(), []
    for s in range(n):
        if s in seen or not adj[s]:
            continue
        stack, comp = [s], []
        seen.add(s)
        while stack:
            u = stack.pop()
            comp.append(u)
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        comps.append(sorted(comp))
    return sorted(comps)


def check_resolved(x0, v0, v, mass, edges, zones, record, dt):
    n = len(x0)
    x1 = [(x0[i][0] + dt * v[i][0], x0[i][1] + dt * v[i][1]) for i in range(n)]
    assert iz.collisions(x0, x1, edges) == []
    assert exact_interference_free(x1, edges)
    for k in range(2):
        p0 = sum(m * w[k] for m, w in zip(mass, v0))
        p1 = sum(m * w[k] for m, w in zip(mass, v))
        assert abs(p1 - p0) <= 1e-10 * max(1.0, sum(m * abs(w[k]) for m, w in zip(mass, v0)))
    for z in zones:
        rigid_check(x0, x1, z, 1e-12)
    assert sorted(sorted(z) for z in zones) == components(n, record, edges)


def test_two_chains_passing_through_each_other():
    a, ea = chain(10, 0.0, 0.0, 0.1)
    b, eb = chain(10, 0.03, 0.05, 0.1, start=10)
    x0 = a + b
    edges = ea + eb
    rng = random.Random(3)
    v0 = [(0.0, 0.0)] * 10 + [(rng.uniform(-0.1, 0.1), -1.0 + rng.uniform(-0.1, 0.1)) for _ in range(10)]
    mass = [1.0] * 20
    assert exact_interference_free(x0, edges)
    record = []
    v, zones, passes = iz.impact_zones(x0, v0, mass, edges, 0.1, record=record)
    assert passes >= 1 and zones
    check_resolved(x0, v0, v, mass, edges, zones, record, 0.1)


def test_random_self_collisions_of_one_chain():
    rng = random.Random(4)
    total_passes = 0
    for trial in range(8):
        n = 12
        x0 = [(0.1 * i, rng.uniform(-0.02, 0.02)) for i in range(n)]
        edges = [(i, i + 1) for i in range(n - 1)]
        assert exact_interference_free(x0, edges)
        v0 = [(rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5)) for _ in range(n)]
        mass = [rng.uniform(0.5, 2.0) for _ in range(n)]
        record = []
        v, zones, passes = iz.impact_zones(x0, v0, mass, edges, 0.1, record=record)
        assert passes <= n - 1
        total_passes += passes
        check_resolved(x0, v0, v, mass, edges, zones, record, 0.1)
    assert total_passes > 0


def test_no_collision_changes_nothing():
    x0, edges = chain(5, 0.0, 0.0, 0.1)
    v0 = [(0.0, -1.0)] * 5
    v, zones, passes = iz.impact_zones(x0, v0, [1.0] * 5, edges, 0.1)
    assert v == v0 and zones == [] and passes == 0
