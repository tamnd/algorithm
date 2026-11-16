# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/optimal-reciprocal-collision-avoidance/. The authors are listed in prov/D7S5SH.jsonl.

import math
import random

from optimal_reciprocal_collision_avoidance import (
    Agent,
    Line,
    det,
    dot,
    lp2,
    lp3,
    new_velocity,
    norm,
    orca_line,
    step,
    sub,
)

TOL = 1e-9


def violation(line, v):
    """Distance by which v is on the forbidden (right) side of the line, or <= 0."""
    return det(line.direction, sub(line.point, v))


def min_distance(pa, va, pb, vb, horizon):
    """Smallest distance between two points that move with constant velocities on [0, horizon]."""
    p = sub(pb, pa)
    v = sub(vb, va)
    vv = dot(v, v)
    t = 0.0 if vv == 0.0 else min(max(-dot(p, v) / vv, 0.0), horizon)
    return norm((p[0] + v[0] * t, p[1] + v[1] * t))


def brute_lp(lines, radius, opt):
    """Brute force: the nearest feasible point to opt among all candidate points."""
    cands = [opt]
    for ln in lines:
        t = dot(ln.direction, sub(opt, ln.point))
        cands.append((ln.point[0] + t * ln.direction[0], ln.point[1] + t * ln.direction[1]))
        d = dot(ln.point, ln.direction)
        disc = d * d + radius * radius - dot(ln.point, ln.point)
        if disc >= 0:
            for s in (-1, 1):
                t = -d + s * math.sqrt(disc)
                cands.append((ln.point[0] + t * ln.direction[0], ln.point[1] + t * ln.direction[1]))
    for i in range(len(lines)):
        for k in range(i + 1, len(lines)):
            a, b = lines[i], lines[k]
            den = det(a.direction, b.direction)
            if abs(den) > 1e-12:
                t = det(b.direction, sub(a.point, b.point)) / den
                cands.append((a.point[0] + t * a.direction[0], a.point[1] + t * a.direction[1]))
    n = norm(opt)
    if n > 0:
        cands.append((opt[0] * radius / n, opt[1] * radius / n))
    best = None
    for c in cands:
        if norm(c) <= radius + 1e-9 and all(violation(ln, c) <= 1e-9 for ln in lines):
            d = norm(sub(c, opt))
            if best is None or d < best:
                best = d
    return best


def random_line(rng):
    ang = rng.uniform(0, 2 * math.pi)
    return Line((rng.uniform(-2, 2), rng.uniform(-2, 2)), (math.cos(ang), math.sin(ang)))


def test_head_on_example():
    a = Agent((0.0, 0.0), (1.0, 0.0), 0.5, 1.0, (1.0, 0.0))
    b = Agent((4.0, 0.0), (-1.0, 0.0), 0.5, 1.0, (-1.0, 0.0))
    s15 = math.sqrt(15.0)
    line = orca_line(a, b, 2.0, 0.1)
    assert abs(line.point[0] - 15 / 16) < TOL and abs(line.point[1] + s15 / 16) < TOL
    assert abs(line.direction[0] + s15 / 4) < TOL and abs(line.direction[1] - 0.25) < TOL
    va, ok_a = new_velocity(a, [b], 2.0, 0.1)
    vb, ok_b = new_velocity(b, [a], 2.0, 0.1)
    assert ok_a and ok_b
    assert abs(va[0] - 15 / 16) < TOL and abs(va[1] + s15 / 16) < TOL
    assert abs(vb[0] + 15 / 16) < TOL and abs(vb[1] - s15 / 16) < TOL
    assert min_distance(a.position, va, b.position, vb, 10.0) >= 1.0 - TOL
    # With tau = 1 the collision at t = 1.5 is outside the horizon: no change.
    line1 = orca_line(a, b, 1.0, 0.1)
    assert abs(line1.point[0] - 1.5) < TOL and abs(line1.point[1]) < TOL
    v1, ok = new_velocity(a, [b], 1.0, 0.1)
    assert ok and abs(v1[0] - 1.0) < TOL and abs(v1[1]) < TOL


def test_lines_are_mirror_images():
    rng = random.Random(4)
    for _ in range(200):
        a = Agent((rng.uniform(-3, 3), rng.uniform(-3, 3)), (rng.uniform(-1, 1), rng.uniform(-1, 1)), 0.4, 2.0, (0, 0))
        b = Agent((rng.uniform(-3, 3), rng.uniform(-3, 3)), (rng.uniform(-1, 1), rng.uniform(-1, 1)), 0.3, 2.0, (0, 0))
        if norm(sub(a.position, b.position)) <= 0.7:
            continue
        la = orca_line(a, b, 2.0, 0.1)
        lb = orca_line(b, a, 2.0, 0.1)
        ua = sub(la.point, a.velocity)
        ub = sub(lb.point, b.velocity)
        assert norm((ua[0] + ub[0], ua[1] + ub[1])) < 1e-9
        assert norm((la.direction[0] + lb.direction[0], la.direction[1] + lb.direction[1])) < 1e-9


def test_lp2_against_brute_force():
    rng = random.Random(11)
    feasible = 0
    for _ in range(400):
        lines = [random_line(rng) for _ in range(rng.randint(1, 6))]
        radius = rng.uniform(0.5, 3.0)
        opt = (rng.uniform(-3, 3), rng.uniform(-3, 3))
        count, v = lp2(lines, radius, opt)
        best = brute_lp(lines, radius, opt)
        if count == len(lines):
            feasible += 1
            assert norm(v) <= radius + 1e-9
            assert all(violation(ln, v) <= 1e-9 for ln in lines)
            assert best is not None and abs(norm(sub(v, opt)) - best) < 1e-7
        else:
            assert best is None
    assert feasible > 100


def test_lp3_minimizes_the_largest_violation():
    rng = random.Random(5)
    checked = 0
    while checked < 40:
        lines = [random_line(rng) for _ in range(rng.randint(2, 5))]
        radius = 1.0
        count, v = lp2(lines, radius, (0.0, 0.0))
        if count == len(lines):
            continue
        checked += 1
        v = lp3(lines, count, radius, v)
        assert norm(v) <= radius + 1e-9
        got = max(violation(ln, v) for ln in lines)
        grid = 1e9
        n = 60
        for i in range(-n, n + 1):
            for k in range(-n, n + 1):
                c = (i / n, k / n)
                if norm(c) <= radius:
                    grid = min(grid, max(violation(ln, c) for ln in lines))
        assert got <= grid + 1e-9
        assert got > 0


def test_pairs_avoid_each_other_for_tau():
    rng = random.Random(3)
    for _ in range(400):
        tau = rng.choice([1.0, 2.0, 5.0])
        a = Agent((0.0, 0.0), (rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)), 0.5, 1.5, (rng.uniform(-1, 1), rng.uniform(-1, 1)))
        b = Agent((rng.uniform(-4, 4), rng.uniform(-4, 4)), (rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)), 0.5, 1.5, (rng.uniform(-1, 1), rng.uniform(-1, 1)))
        if norm(b.position) <= 1.0:
            continue
        va, ok_a = new_velocity(a, [b], tau, 0.1)
        vb, ok_b = new_velocity(b, [a], tau, 0.1)
        assert ok_a and ok_b
        assert min_distance(a.position, va, b.position, vb, tau) >= 1.0 - 1e-9


def circle_scenario(n, ring, rad, seed):
    rng = random.Random(seed)
    agents, goals = [], []
    for i in range(n):
        th = 2 * math.pi * i / n + rng.uniform(-0.05, 0.05)
        p = (ring * math.cos(th), ring * math.sin(th))
        agents.append(Agent(p, (0.0, 0.0), rad, 1.0, (0.0, 0.0)))
        goals.append((-p[0], -p[1]))
    return rng, agents, goals


def with_preferences(rng, agents, goals):
    out = []
    for a, g in zip(agents, goals):
        d = sub(g, a.position)
        s = max(norm(d), 1.0)
        ang = rng.uniform(0, 2 * math.pi)
        m = rng.uniform(0, 0.01)  # a small push that breaks symmetric deadlocks
        out.append(a._replace(pref=(d[0] / s + m * math.cos(ang), d[1] / s + m * math.sin(ang))))
    return out


def closest_pair(agents):
    return min(
        norm(sub(agents[i].position, agents[k].position)) - agents[i].radius - agents[k].radius
        for i in range(len(agents))
        for k in range(i + 1, len(agents))
    )


def test_eight_robots_swap_without_overlap():
    rng, agents, goals = circle_scenario(8, 6.0, 0.4, 3)
    for k in range(1500):
        agents, ok = step(with_preferences(rng, agents, goals), 2.0, 0.1)
        assert ok
        assert closest_pair(agents) >= -1e-9
        if all(norm(sub(a.position, g)) < 0.1 for a, g in zip(agents, goals)):
            break
    assert all(norm(sub(a.position, g)) < 0.1 for a, g in zip(agents, goals))


def test_feasible_steps_never_create_overlap():
    rng, agents, goals = circle_scenario(8, 6.0, 0.5, 2)
    fallback = 0
    for k in range(800):
        before = closest_pair(agents)
        agents, ok = step(with_preferences(rng, agents, goals), 2.0, 0.1)
        if not ok:
            fallback += 1
        elif before >= -1e-9:
            assert closest_pair(agents) >= -1e-9
    assert fallback > 0
