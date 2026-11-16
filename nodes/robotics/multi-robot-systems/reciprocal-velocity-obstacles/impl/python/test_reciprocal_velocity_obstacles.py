# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reciprocal-velocity-obstacles/. The authors are listed in prov/VJAYA8.jsonl.

import math
import random

from reciprocal_velocity_obstacles import (
    Agent,
    candidates,
    det,
    dot,
    in_rvo,
    new_velocity,
    norm,
    step,
    sub,
    time_to_collision,
)


def in_cone(rel_pos, w, rad):
    """Reference test of the collision cone: the ray t w, t > 0, passes closer than rad to rel_pos."""
    if norm(w) == 0.0:
        return False
    return dot(w, rel_pos) > 0.0 and abs(det(w, rel_pos)) / norm(w) < rad


def legs(rel_pos, rad):
    """Unit directions of the left and right legs of the cone."""
    d = norm(rel_pos)
    alpha = math.asin(rad / d)
    base = math.atan2(rel_pos[1], rel_pos[0])
    return (math.cos(base + alpha), math.sin(base + alpha)), (math.cos(base - alpha), math.sin(base - alpha))


def random_pair(rng):
    a = Agent((0.0, 0.0), (rng.uniform(-1, 1), rng.uniform(-1, 1)), 0.5, 1.0, (1.0, 0.0))
    while True:
        p = (rng.uniform(-5, 5), rng.uniform(-5, 5))
        if norm(p) > 1.2:
            break
    b = Agent(p, (rng.uniform(-1, 1), rng.uniform(-1, 1)), 0.5, 1.0, (-1.0, 0.0))
    return a, b


def test_rvo_is_the_velocity_obstacle_with_its_apex_moved_halfway():
    rng = random.Random(1)
    inside = 0
    for _ in range(3000):
        a, b = random_pair(rng)
        v = (rng.uniform(-1.5, 1.5), rng.uniform(-1.5, 1.5))
        rel = sub(b.position, a.position)
        got = in_rvo(a, b, v)
        # v is in RVO_A|B exactly when 2 v - v_A is in the plain velocity obstacle of B.
        w = (2 * v[0] - a.velocity[0] - b.velocity[0], 2 * v[1] - a.velocity[1] - b.velocity[1])
        assert got == in_cone(rel, w, 1.0)
        inside += got
        # The apex (v_A + v_B) / 2 is never inside.
        apex = ((a.velocity[0] + b.velocity[0]) / 2, (a.velocity[1] + b.velocity[1]) / 2)
        assert not in_rvo(a, b, apex)
    assert 150 < inside < 2850


def test_same_side_choices_never_collide():
    rng = random.Random(2)
    opposite_collisions = 0
    for _ in range(3000):
        a, b = random_pair(rng)
        rel = sub(b.position, a.position)
        left, right = legs(rel, 1.0)

        def on_side(leg, sign):
            # A point in the closed half-plane beyond the leg line: sign det(leg, w) >= 0.
            while True:
                w = (rng.uniform(-3, 3), rng.uniform(-3, 3))
                if sign * det(leg, w) >= 0.0:
                    return w

        side = rng.choice([(left, 1.0), (right, -1.0)])
        wa, wb = on_side(*side), on_side(*side)
        va = ((wa[0] + a.velocity[0] + b.velocity[0]) / 2, (wa[1] + a.velocity[1] + b.velocity[1]) / 2)
        vb = ((a.velocity[0] + b.velocity[0] - wb[0]) / 2, (a.velocity[1] + b.velocity[1] - wb[1]) / 2)
        assert not in_rvo(a, b, va) and not in_rvo(b, a, vb)
        assert time_to_collision(rel, sub(va, vb), 1.0) == math.inf
        # Opposite sides: each choice is outside its own RVO, but the pair can still collide.
        wb2 = on_side(right, -1.0) if side[0] is left else on_side(left, 1.0)
        vb2 = ((a.velocity[0] + b.velocity[0] - wb2[0]) / 2, (a.velocity[1] + b.velocity[1] - wb2[1]) / 2)
        assert not in_rvo(b, a, vb2)
        if time_to_collision(rel, sub(va, vb2), 1.0) < math.inf:
            opposite_collisions += 1
    assert opposite_collisions > 100


def test_head_on_pair_turns_to_the_same_side():
    a = Agent((0.0, 0.0), (1.0, 0.0), 0.5, 1.0, (1.0, 0.0))
    b = Agent((4.0, 0.0), (-1.0, 0.0), 0.5, 1.0, (-1.0, 0.0))
    assert in_rvo(a, b, (1.0, 0.0))
    va, vb = new_velocity(a, [b]), new_velocity(b, [a])
    c, s = math.cos(math.pi / 8), math.sin(math.pi / 8)
    assert abs(va[0] - c) < 1e-12 and abs(va[1] - s) < 1e-12
    assert abs(vb[0] + c) < 1e-12 and abs(vb[1] + s) < 1e-12
    assert time_to_collision(sub(b.position, a.position), sub(va, vb), 1.0) == math.inf
    agents, closest, ys = [a, b], math.inf, []
    for _ in range(80):
        agents = step(agents, 0.1)
        closest = min(closest, norm(sub(agents[0].position, agents[1].position)))
        ys.append(agents[0].velocity[1])
    assert closest >= 1.0
    assert min(ys) >= 0.0  # A never swings back to the other side
    assert agents[0].velocity == (1.0, 0.0) and agents[1].velocity == (-1.0, 0.0)


def plain_vo_velocity(a, others):
    """The same penalty rule with the plain velocity obstacle (relative velocity v - v_B)."""
    best, best_v = math.inf, None
    for v in candidates(a):
        tc = min(time_to_collision(sub(b.position, a.position), sub(v, b.velocity), a.radius + b.radius) for b in others)
        pen = math.inf if tc == 0.0 else 1.0 / tc + norm(sub(v, a.pref))
        if pen < best:
            best, best_v = pen, v
    return best_v


def test_plain_velocity_obstacles_oscillate():
    a = Agent((0.0, 0.0), (1.0, 0.0), 0.5, 1.0, (1.0, 0.0))
    b = Agent((4.0, 0.0), (-1.0, 0.0), 0.5, 1.0, (-1.0, 0.0))
    straight = []
    for _ in range(10):
        va, vb = plain_vo_velocity(a, [b]), plain_vo_velocity(b, [a])
        a = a._replace(velocity=va, position=(a.position[0] + 0.1 * va[0], a.position[1] + 0.1 * va[1]))
        b = b._replace(velocity=vb, position=(b.position[0] + 0.1 * vb[0], b.position[1] + 0.1 * vb[1]))
        straight.append(va == (1.0, 0.0))
    assert straight == [False, True] * 5


def test_free_preferred_velocity_is_kept():
    rng = random.Random(6)
    for _ in range(300):
        a, b = random_pair(rng)
        a = a._replace(pref=(rng.uniform(-0.7, 0.7), rng.uniform(-0.7, 0.7)))  # inside the speed disc
        if not in_rvo(a, b, a.pref):
            assert new_velocity(a, [b]) == a.pref


def test_six_robots_swap_without_overlap():
    rng = random.Random(1)
    n, ring, rad = 6, 6.0, 0.4
    agents, goals = [], []
    for i in range(n):
        th = 2 * math.pi * i / n + rng.uniform(-0.05, 0.05)
        p = (ring * math.cos(th), ring * math.sin(th))
        agents.append(Agent(p, (0.0, 0.0), rad, 1.0, (0.0, 0.0)))
        goals.append((-p[0], -p[1]))
    arrived = False
    for _ in range(600):
        prefs = []
        for a, g in zip(agents, goals):
            d = sub(g, a.position)
            s = max(norm(d), 1.0)
            prefs.append(a._replace(pref=(d[0] / s, d[1] / s)))
        agents = step(prefs, 0.1, rings=4, spokes=16)
        for i in range(n):
            for k in range(i + 1, n):
                assert norm(sub(agents[i].position, agents[k].position)) >= 2 * rad
        if all(norm(sub(a.position, g)) < 0.15 for a, g in zip(agents, goals)):
            arrived = True
            break
    assert arrived
