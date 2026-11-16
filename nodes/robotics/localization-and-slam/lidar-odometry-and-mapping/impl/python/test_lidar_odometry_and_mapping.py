# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lidar-odometry-and-mapping/. The authors are listed in prov/GTC8AH.jsonl.

import math
import random

from lidar_odometry_and_mapping import (
    Grid,
    ToyLoam,
    compose,
    extract_features,
    fit_line,
    gauss_newton,
    inverse,
    line_residual,
    point_residual,
    scan_to_scan_terms,
    smoothness,
    transform,
    wrap,
)


def room():
    """An L-shaped room with two square pillars, as wall segments."""
    poly = [(0, 0), (12, 0), (12, 4), (8, 4), (8, 9), (0, 9)]
    segs = [(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
    for cx, cy in ((3, 3), (5, 6.5)):
        box = [(cx - 0.4, cy - 0.4), (cx + 0.4, cy - 0.4), (cx + 0.4, cy + 0.4), (cx - 0.4, cy + 0.4)]
        segs += [(box[i], box[(i + 1) % 4]) for i in range(4)]
    return segs


def cast(pose, segs, beams, rng=None, noise=0.0):
    """A 360 degree scan from `pose`, as points in the sensor frame in beam order."""
    pts = []
    for b in range(beams):
        la = 2 * math.pi * b / beams
        dx, dy = math.cos(pose[2] + la), math.sin(pose[2] + la)
        best = math.inf
        for (x1, y1), (x2, y2) in segs:
            ex, ey = x2 - x1, y2 - y1
            den = dx * ey - dy * ex
            if abs(den) < 1e-12:
                continue
            wx, wy = x1 - pose[0], y1 - pose[1]
            t = (wx * ey - wy * ex) / den
            u = (wx * dy - wy * dx) / den
            if t > 1e-9 and -1e-9 <= u <= 1 + 1e-9:
                best = min(best, t)
        r = best + (rng.gauss(0, noise) if noise else 0.0)
        pts.append((r * math.cos(la), r * math.sin(la)))
    return pts


def circle(n, per_lap=24):
    """n poses on a circle of radius 1.8 around the first pillar, facing forward."""
    out = []
    for k in range(n):
        a = -math.pi / 2 + 2 * math.pi * k / per_lap
        out.append((3 + 1.8 * math.cos(a), 3 + 1.8 * math.sin(a), wrap(a + math.pi / 2)))
    return out


def run(seed, n=30, noise=0.03):
    truth = circle(n)
    rng = random.Random(seed)
    loam = ToyLoam(map_every=5)
    for pose in truth:
        loam.add_scan(cast(pose, room(), 360, rng, noise))
    return truth, loam


def errors(poses, truth):
    start = truth[0]
    return [math.hypot(*(a - b for a, b in zip(compose(start, p)[:2], t[:2]))) for p, t in zip(poses, truth)]


def test_smoothness_is_zero_on_a_line_and_scale_free():
    line = [(3.0, -1.0 + 0.1 * j) for j in range(21)]
    assert smoothness(line, 10, 5) < 1e-12
    corner = [(3.0, 0.1 * j) for j in range(-5, 1)] + [(3.0 - 0.1 * j, 0.0) for j in range(1, 6)]
    c = smoothness(corner, 5, 5)
    assert c > 0.05
    for lam, th in ((2.0, 0.0), (0.5, 1.3)):
        moved = [(lam * (math.cos(th) * x - math.sin(th) * y), lam * (math.sin(th) * x + math.cos(th) * y)) for x, y in corner]
        assert abs(smoothness(moved, 5, 5) - c) < 1e-12


def test_sharp_points_lie_at_corners_and_flat_points_on_walls():
    segs = room()
    pose = (2.0, 1.5, 0.2)
    scan = cast(pose, segs, 360)
    sharp, flat, less_flat = extract_features(scan)
    corners = [p for s in segs for p in s]
    assert len(sharp) >= 3
    for i in sharp:
        q = transform(pose, scan[i])
        r = math.hypot(*scan[i])
        # within two beam spacings of a corner of the room or of a pillar
        assert min(math.hypot(q[0] - x, q[1] - y) for x, y in corners) < 2 * r * 2 * math.pi / 360
    for i in less_flat:
        q = transform(pose, scan[i])
        assert min(segment_distance(q, s) for s in segs) < 1e-9
    assert set(flat) <= set(less_flat)


def segment_distance(q, seg):
    (x1, y1), (x2, y2) = seg
    ex, ey = x2 - x1, y2 - y1
    t = max(0.0, min(1.0, ((q[0] - x1) * ex + (q[1] - y1) * ey) / (ex * ex + ey * ey)))
    return math.hypot(q[0] - x1 - t * ex, q[1] - y1 - t * ey)


def test_jacobians_match_finite_differences():
    rng = random.Random(4)
    for _ in range(20):
        pose = (rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-3, 3))
        p = (rng.uniform(-5, 5), rng.uniform(-5, 5))
        a = (rng.uniform(-5, 5), rng.uniform(-5, 5))
        th = rng.uniform(0, math.pi)
        normal = (math.cos(th), math.sin(th))
        for f in (lambda x: point_residual(x, p, a), lambda x: line_residual(x, p, a, normal)):
            rows, jac = f(pose)
            for k in range(3):
                h = 1e-6
                plus = list(pose)
                plus[k] += h
                minus = list(pose)
                minus[k] -= h
                for r in range(len(rows)):
                    num = (f(tuple(plus))[0][r] - f(tuple(minus))[0][r]) / (2 * h)
                    assert abs(num - jac[r][k]) < 1e-6


def test_grid_equals_brute_force():
    rng = random.Random(6)
    pts = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(300)]
    grid = Grid(pts, cell=0.7)
    for _ in range(50):
        q = (rng.uniform(-6, 6), rng.uniform(-6, 6))
        rad = rng.uniform(0.1, 2.0)
        brute = sorted((math.hypot(p[0] - q[0], p[1] - q[1]), i) for i, p in enumerate(pts))
        assert grid.near(q, rad) == [i for d, i in brute if d <= rad]


def test_fit_line_finds_the_direction():
    pts = [(1.0 + t * math.cos(0.7), 2.0 + t * math.sin(0.7)) for t in (-1.0, -0.5, 0.0, 0.25, 1.5)]
    mean, d, big, small = fit_line(pts)
    assert abs(d[0] * math.sin(0.7) - d[1] * math.cos(0.7)) < 1e-12
    assert small < 1e-12 < big


def test_flat_points_recover_the_motion_exactly_without_noise():
    # on noise-free scans every flat point lies on the line of its match at
    # the true motion, so the true motion is a zero of the cost
    segs = room()
    a = (2.0, 1.5, 0.1)
    for motion in ((0.2, 0.05, 0.04), (0.3, -0.1, -0.06)):
        b = compose(a, motion)
        s0, s1 = cast(a, segs, 360), cast(b, segs, 360)
        sh0, fl0, lf0 = extract_features(s0)
        sh1, fl1, lf1 = extract_features(s1)
        terms = scan_to_scan_terms(s1, [], fl1, s0, [], lf0)
        got = gauss_newton((0.0, 0.0, 0.0), terms)
        assert all(abs(x - y) < 1e-6 for x, y in zip(got, motion))
        assert all(abs(r) < 1e-9 for rows, _, _ in terms(motion) for r in rows)


def test_mapping_reduces_the_drift_of_odometry():
    # 30 scans, a lap and a quarter around a pillar, with range noise 0.03
    for seed in (1, 2):
        truth, loam = run(seed)
        # odom_path is what odometry alone gives, since mapping does not feed back into it
        odom = errors(loam.odom_path, truth)
        mapped = errors(loam.path, truth)
        assert max(mapped) < 0.6 * max(odom)
        assert max(mapped) < 0.05 and mapped[-1] < 0.05


def test_inverse_and_compose():
    a = (1.0, -2.0, 0.7)
    e = compose(a, inverse(a))
    assert all(abs(x) < 1e-12 for x in e)
