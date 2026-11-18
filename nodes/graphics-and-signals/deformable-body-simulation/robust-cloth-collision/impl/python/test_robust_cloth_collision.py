# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robust-cloth-collision/. The authors are listed in prov/QXMR1R.jsonl.

"""Tests of the cloth collision pipeline against sampling, brute force and exact rational tests."""

import math
import random
from fractions import Fraction

from anim import add, cross, dot, mul, norm, q_from_axis_angle, q_to_mat3, scale, sub, transpose
import robust_cloth_collision as rc


# ---------------------------------------------------------------- exact intersection test


def orient(a, b, c, d):
    u, v, w = sub(b, a), sub(c, a), sub(d, a)
    return dot(cross(u, v), w)


def orient2(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def segments_meet2(p, q, r, s):
    d1, d2, d3, d4 = orient2(r, s, p), orient2(r, s, q), orient2(p, q, r), orient2(p, q, s)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True

    def on(a, b, c):
        return orient2(a, b, c) == 0 and min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) \
            and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])
    return on(r, s, p) or on(r, s, q) or on(p, q, r) or on(p, q, s)


def in_triangle2(p, a, b, c):
    s1, s2, s3 = orient2(a, b, p), orient2(b, c, p), orient2(c, a, p)
    return (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)


def segment_meets_triangle(p, q, a, b, c):
    """Exact test with Fractions: does the closed segment pq meet the closed triangle abc?"""
    p, q, a, b, c = ([Fraction(z) for z in pt] for pt in (p, q, a, b, c))
    o1, o2 = orient(a, b, c, p), orient(a, b, c, q)
    if o1 == 0 and o2 == 0:
        n = cross(sub(b, a), sub(c, a))
        drop = max(range(3), key=lambda k: abs(n[k]))
        p, q, a, b, c = ([z for k, z in enumerate(pt) if k != drop] for pt in (p, q, a, b, c))
        return in_triangle2(p, a, b, c) or in_triangle2(q, a, b, c) or any(
            segments_meet2(p, q, u, w) for u, w in ((a, b), (b, c), (c, a)))
    if (o1 > 0 and o2 > 0) or (o1 < 0 and o2 < 0):
        return False
    s1, s2, s3 = orient(p, q, a, b), orient(p, q, b, c), orient(p, q, c, a)
    return (s1 >= 0 and s2 >= 0 and s3 >= 0) or (s1 <= 0 and s2 <= 0 and s3 <= 0)


def boxes_meet(p, q):
    """Float comparisons are exact, so disjoint boxes prove that the parts do not meet."""
    return all(min(a[k] for a in p) <= max(b[k] for b in q) and min(b[k] for b in q) <= max(a[k] for a in p)
               for k in range(3))


def exact_intersection_free(x, triangles):
    for e in rc.mesh_edges(triangles):
        for t in triangles:
            if e[0] in t or e[1] in t:
                continue
            seg, tri = (x[e[0]], x[e[1]]), tuple(x[i] for i in t)
            if boxes_meet(seg, tri) and segment_meets_triangle(*seg, *tri):
                return False
    return True


# ---------------------------------------------------------------- continuous detection against sampling


def lerp(a, b, s):
    return add(a, scale(sub(b, a), s))


def sampled_time(kind, p0, p1, samples=400):
    """First contact by sampling the sign of the coplanarity volume, bisection and a proximity test."""
    def at(s):
        q = [lerp(a, b, s) for a, b in zip(p0, p1)]
        return orient(*q), q

    def close(q):
        if kind == "pt":
            return rc.point_triangle_proximity(q[3], q[0], q[1], q[2], rc.ROUNDING_TOL) is not None
        return rc.edge_edge_proximity(q[0], q[1], q[2], q[3], rc.ROUNDING_TOL) is not None

    prev = at(0.0)[0]
    for k in range(1, samples + 1):
        cur = at(k / samples)[0]
        if (prev > 0) != (cur > 0) or cur == 0.0:
            lo, hi = (k - 1) / samples, k / samples
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                fm = at(mid)[0]
                if fm != 0.0 and (fm > 0) == (prev > 0):
                    lo = mid
                else:
                    hi = mid
            if close(at(hi)[1]):
                return hi
        prev = cur
    return None


def random_crossing(rng, kind):
    """Four moving points of a pair that often meet: the second part crosses the plane z = 0."""
    if kind == "pt":
        p0 = [(rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-0.2, 0.2)) for _ in range(3)]
        p0.append((rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.4), 0.5))
        p1 = [add(p, (rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3))) for p in p0[:3]]
        p1.append((rng.uniform(-0.4, 0.4), rng.uniform(-0.4, 0.4), -0.5))
    else:
        p0 = [(-1.0, rng.uniform(-0.5, 0.5), rng.uniform(-0.2, 0.2)), (1.0, rng.uniform(-0.5, 0.5), rng.uniform(-0.2, 0.2)),
              (rng.uniform(-0.5, 0.5), -1.0, 0.5), (rng.uniform(-0.5, 0.5), 1.0, 0.5)]
        p1 = [add(p, (rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), rng.uniform(-0.2, 0.2))) for p in p0[:2]]
        p1 += [add(p, (rng.uniform(-0.3, 0.3), rng.uniform(-0.3, 0.3), -1.0)) for p in p0[2:]]
    return p0, p1


def test_collision_time_against_sampling_and_bisection():
    rng = random.Random(1)
    for kind in ("pt", "ee"):
        hits = 0
        for _ in range(50):
            p0, p1 = random_crossing(rng, kind)
            x0 = {i: p for i, p in enumerate(p0)}
            x1 = {i: p for i, p in enumerate(p1)}
            pair = (3, (0, 1, 2)) if kind == "pt" else ((0, 1), (2, 3))
            got = rc.collision_time(x0, x1, kind, pair)
            want = sampled_time(kind, p0, p1)
            if want is None:
                assert got is None
            else:
                hits += 1
                assert got is not None and abs(got - want) < 1e-9
        assert hits > 10


def test_coplanarity_cubic_matches_the_volume():
    rng = random.Random(2)
    for _ in range(50):
        p = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(4)]
        u = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(4)]
        k = rc.coplanarity_cubic(p, u)
        for s in (0.0, 0.3, 0.7, 1.0):
            q = [add(a, scale(b, s)) for a, b in zip(p, u)]
            assert abs(rc._poly(k, s) - orient(*q)) < 1e-12


# ---------------------------------------------------------------- proximity against brute force


def point_segment_distance(p, a, b):
    d = sub(b, a)
    t = dot(sub(p, a), d) / dot(d, d)
    t = min(1.0, max(0.0, t))
    return norm(sub(p, add(a, scale(d, t))))


def test_edge_edge_closest_points_against_enumeration():
    rng = random.Random(3)
    for trial in range(300):
        q = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(4)]
        if trial % 10 == 0:  # parallel edges
            q[3] = add(q[2], scale(sub(q[1], q[0]), rng.uniform(-1, 1)))
        s, t = rc.segment_closest(*q)
        got = norm(sub(lerp(q[0], q[1], s), lerp(q[2], q[3], t)))
        cands = [point_segment_distance(q[0], q[2], q[3]), point_segment_distance(q[1], q[2], q[3]),
                 point_segment_distance(q[2], q[0], q[1]), point_segment_distance(q[3], q[0], q[1])]
        n = cross(sub(q[1], q[0]), sub(q[3], q[2]))
        if norm(n) > 1e-9:
            # interior critical point: the closest points of the two lines
            d1, d2, r = sub(q[1], q[0]), sub(q[3], q[2]), sub(q[0], q[2])
            a, b, e = dot(d1, d1), dot(d1, d2), dot(d2, d2)
            c, f = dot(d1, r), dot(d2, r)
            den = a * e - b * b
            s0, t0 = (b * f - c * e) / den, (a * f - b * c) / den
            if 0 <= s0 <= 1 and 0 <= t0 <= 1:
                cands.append(norm(sub(lerp(q[0], q[1], s0), lerp(q[2], q[3], t0))))
        assert abs(got - min(cands)) < 1e-12


def test_point_triangle_weights_against_area_ratios():
    rng = random.Random(4)
    for _ in range(200):
        a, b, c = (tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(3))
        n = cross(sub(b, a), sub(c, a))
        w = [rng.uniform(-0.1, 1.0) for _ in range(2)]
        w.append(1.0 - w[0] - w[1])
        h = rng.uniform(-0.01, 0.01)
        p = add(add(add(scale(a, w[0]), scale(b, w[1])), scale(c, w[2])), scale(n, h / norm(n)))
        r = rc.point_triangle_proximity(p, a, b, c, 0.02)
        inside = min(w) >= 0.0
        if r is None:
            assert not inside
            continue
        nn = dot(n, n)
        want = [dot(n, cross(sub(b, p), sub(c, p))) / nn, dot(n, cross(sub(c, p), sub(a, p))) / nn]
        assert abs(r[0] - want[0]) < 1e-9 and abs(r[1] - want[1]) < 1e-9
        assert abs(r[4] - abs(h)) < 1e-12 and r[4] >= 0.0


# ---------------------------------------------------------------- impulses


def momentum(v, mass):
    return tuple(sum(m * w[k] for m, w in zip(mass, v)) for k in range(3))


def test_impulse_keeps_momentum_and_matches_section_7_1():
    rng = random.Random(5)
    for _ in range(100):
        v = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in range(4)]
        mass = [rng.uniform(0.5, 2.0) for _ in range(4)]
        w = [rng.uniform(0, 1) for _ in range(2)]
        coeffs = (1.0, -w[0], -w[1], -(1.0 - w[0] - w[1]))
        dv = tuple(rng.uniform(-1, 1) for _ in range(3))
        before = rc.relative_velocity(v, range(4), coeffs)
        p0 = momentum(v, mass)
        rc.apply_impulse(v, mass, range(4), coeffs, dv)
        after = rc.relative_velocity(v, range(4), coeffs)
        assert norm(sub(sub(after, before), dv)) < 1e-12
        assert norm(sub(momentum(v, mass), p0)) <= 1e-10 * max(1.0, norm(p0))
    # equal masses: the point gets I~/m n and triangle node i gets -w_i I~/m n, I~ = 2 I / (1 + sum w^2)
    m, n_hat, dvn = 2.0, (0.0, 0.0, 1.0), 0.6
    w = (0.2, 0.3, 0.5)
    v = [(0.0, 0.0, 0.0)] * 4
    rc.apply_impulse(v, [m] * 4, range(4), (1.0, -w[0], -w[1], -w[2]), scale(n_hat, dvn))
    impulse = m * dvn / 2.0
    it = 2.0 * impulse / (1.0 + sum(z * z for z in w))
    assert abs(v[0][2] - it / m) < 1e-15
    for i in range(3):
        assert abs(v[i + 1][2] + w[i] * it / m) < 1e-15


def test_repulsion_spring_and_friction():
    # one node 0.4 h above the middle of a triangle, moving down slowly and sliding
    h, dt, k = 0.01, 0.01, 50.0
    x = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.25, 0.25, 0.4 * h)]
    mass = [0.1] * 4
    v = [(0.0, 0.0, 0.0)] * 3 + [(0.2, 0.0, -0.05)]
    con = rc.proximity(x, "pt", (3, (0, 1, 2)), h)
    assert con is not None and abs(con[3] - 0.4 * h) < 1e-15
    nodes, coeffs, n, dist = con
    d = h - dist
    m_eff = 1.0 / sum(c * c / mass[i] for i, c in zip(nodes, coeffs))
    p0 = momentum(v, mass)
    dvn = rc.repulsion(v, mass, con, h, dt, k, mu=0.5)
    vr = rc.relative_velocity(v, nodes, coeffs)
    want_vn = min(dt * k * d / m_eff, 0.1 * d / dt)
    assert abs(dot(vr, n) - want_vn) < 1e-12
    assert abs(dvn - (want_vn + 0.05)) < 1e-12
    # Coulomb friction: the sliding speed drops by mu dvN
    assert abs(vr[0] - (0.2 - 0.5 * dvn)) < 1e-12
    assert norm(sub(momentum(v, mass), p0)) < 1e-15


# ---------------------------------------------------------------- rigid zones


def test_rigid_zone_recovers_a_rigid_velocity():
    rng = random.Random(6)
    dt = 0.1
    for _ in range(20):
        nodes = list(range(5))
        x0 = [tuple(rng.uniform(-1, 1) for _ in range(3)) for _ in nodes]
        mass = [rng.uniform(0.5, 2.0) for _ in nodes]
        u = tuple(rng.uniform(-1, 1) for _ in range(3))
        w0 = tuple(rng.uniform(-5, 5) for _ in range(3))
        c = tuple(rng.uniform(-1, 1) for _ in range(3))
        v = [add(u, cross(w0, sub(p, c))) for p in x0]
        out = rc.rigid_zone_motion(x0, v, mass, nodes, dt)
        x1 = [add(x0[i], scale(out[i], dt)) for i in nodes]
        rot = q_to_mat3(q_from_axis_angle(w0, dt * norm(w0)))
        for i in nodes:
            for j in nodes:
                want = tuple(sum(rot[a][b] * (x0[i][b] - x0[j][b]) for b in range(3)) for a in range(3))
                assert norm(sub(sub(x1[i], x1[j]), want)) < 1e-12
        assert norm(sub(momentum(out.values(), mass), momentum(v, mass))) < 1e-12
    # the rotation matrix is orthogonal, so the check above is a rigid motion
    prod = mul(transpose(rot), rot)
    assert all(abs(prod[a][b] - (1.0 if a == b else 0.0)) < 1e-12 for a in range(3) for b in range(3))


# ---------------------------------------------------------------- whole pipeline


def sheet(nx, ny, spacing, origin, rng, start=0, jitter=0.002):
    pts = [(origin[0] + i * spacing, origin[1] + j * spacing, origin[2] + rng.uniform(-jitter, jitter))
           for j in range(ny) for i in range(nx)]
    tris = []
    for j in range(ny - 1):
        for i in range(nx - 1):
            a = start + j * nx + i
            tris += [(a, a + 1, a + nx + 1), (a, a + nx + 1, a + nx)]
    return pts, tris


def check_result(x0, v0, v, mass, triangles, dt, zones):
    x1 = rc.end_positions(x0, v, dt)
    edges = rc.mesh_edges(triangles)
    pt, ee = rc.pairs(len(x0), triangles, edges)
    assert rc.all_collisions(x0, x1, pt, ee) == []
    assert exact_intersection_free(x1, triangles)
    p0, p1 = momentum(v0, mass), momentum(v, mass)
    scale_p = sum(m * norm(w) for m, w in zip(mass, v0))
    assert norm(sub(p1, p0)) <= 1e-10 * max(1.0, scale_p)
    for z in zones:
        for i in z:
            for j in z:
                assert abs(math.dist(x0[i], x0[j]) - math.dist(x1[i], x1[j])) < 1e-12


def two_sheets(gap, speed, seed, n=5, jitter=0.002):
    """Sheet b above sheet a. Its nodes fall with speeds from 0.2 speed to 1.2 speed, so it ends half through."""
    rng = random.Random(seed)
    a, ta = sheet(n, n, 0.1, (0.0, 0.0, 0.0), rng, jitter=jitter)
    b, tb = sheet(n, n, 0.1, (0.013, 0.021, gap), rng, start=n * n, jitter=jitter)
    v = [(0.0, 0.0, 0.0)] * (n * n) + [(rng.uniform(-0.1, 0.1), rng.uniform(-0.1, 0.1),
                                        -speed * (0.2 + (i % n) / (n - 1)) + rng.uniform(-0.05, 0.05))
                                       for i in range(n * n)]
    return a + b, ta + tb, v


def test_sheet_falling_through_a_sheet():
    x0, tris, v0 = two_sheets(0.05, 1.0, 1)
    mass = [0.01] * 50
    assert exact_intersection_free(x0, tris)
    assert not exact_intersection_free(rc.end_positions(x0, v0, 0.1), tris)
    for passes in (5, 0):
        rec = {}
        v, zones = rc.handle_collisions(x0, v0, mass, tris, 0.1, 0.005, 50.0, mu=0.3,
                                        collision_passes=passes, record=rec)
        check_result(x0, v0, v, mass, tris, 0.1, zones)
        if passes == 0:
            assert rec["zone_passes"] >= 1 and zones
        else:
            assert rec["collisions"][0] > 0 and rec["collisions"][-1] == 0


def test_close_sheets_get_repulsions():
    x0, tris, v0 = two_sheets(0.004, 0.02, 2, n=4, jitter=0.001)
    mass = [0.01] * 32
    assert exact_intersection_free(x0, tris)
    rec = {}
    v, zones = rc.handle_collisions(x0, v0, mass, tris, 0.01, 0.005, 50.0, mu=0.3, record=rec)
    assert rec["proximities"] > 0
    check_result(x0, v0, v, mass, tris, 0.01, zones)


def test_random_self_collisions_of_one_sheet():
    total = 0
    zone_runs = 0
    for trial in (1, 2):
        rng = random.Random(10 + trial)
        x0, tris = sheet(5, 5, 0.1, (0.0, 0.0, 0.0), rng, jitter=0.01)
        assert exact_intersection_free(x0, tris)
        v0 = [tuple(rng.uniform(-1.5, 1.5) for _ in range(3)) for _ in x0]
        mass = [rng.uniform(0.005, 0.02) for _ in x0]
        rec = {}
        v, zones = rc.handle_collisions(x0, v0, mass, tris, 0.1, 0.005, 50.0, mu=0.3,
                                        collision_passes=1, record=rec)
        total += rec["collisions"][0]
        zone_runs += rec["zone_passes"] > 0
        assert rec["zone_passes"] <= len(x0) - 1
        check_result(x0, v0, v, mass, tris, 0.1, zones)
    assert total > 0 and zone_runs > 0


def test_no_contact_changes_nothing():
    rng = random.Random(7)
    x0, tris = sheet(4, 4, 0.1, (0.0, 0.0, 0.0), rng)
    v0 = [(0.0, 0.0, -1.0)] * 16
    v, zones = rc.handle_collisions(x0, v0, [0.01] * 16, tris, 0.1, 0.005, 50.0)
    assert v == v0 and zones == []
