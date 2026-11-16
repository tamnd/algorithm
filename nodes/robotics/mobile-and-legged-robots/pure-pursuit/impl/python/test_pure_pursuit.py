# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pure-pursuit/. The authors are listed in prov/RC03NN.jsonl.

import math
import random

from pure_pursuit import PurePursuit, goal_point, closest_on_path, rk4_step, simulate, wrap


def test_the_arc_passes_through_the_goal_point():
    # The arc of curvature kappa, tangent to the heading at the rear axle, has its center at
    # distance 1 / kappa to the left of the vehicle. The goal point must lie on that circle.
    rng = random.Random(1)
    for _ in range(2000):
        path = [(rng.uniform(-20, 20), rng.uniform(-20, 20)) for _ in range(rng.randint(2, 6))]
        pose = (rng.uniform(-20, 20), rng.uniform(-20, 20), rng.uniform(-math.pi, math.pi))
        pp = PurePursuit(path, rng.uniform(0.5, 10.0), 2.5)
        pp.steer(pose)
        gx, gy = pp.goal
        if abs(pp.kappa) < 1e-9:
            # A straight line: the goal point is on the heading line.
            assert abs(-math.sin(pose[2]) * (gx - pose[0]) + math.cos(pose[2]) * (gy - pose[1])) < 1e-6
            continue
        r = 1.0 / pp.kappa
        cx, cy = pose[0] - r * math.sin(pose[2]), pose[1] + r * math.cos(pose[2])
        assert abs(math.hypot(gx - cx, gy - cy) - abs(r)) < 1e-9 * max(1.0, abs(r))


def test_goal_point_is_at_the_lookahead_distance():
    rng = random.Random(2)
    for _ in range(2000):
        path = [(rng.uniform(-20, 20), rng.uniform(-20, 20)) for _ in range(rng.randint(2, 6))]
        p = (rng.uniform(-20, 20), rng.uniform(-20, 20))
        ld = rng.uniform(0.5, 10.0)
        i, u = closest_on_path(path, p, 0)
        g = goal_point(path, p, i, u, ld)
        if g != path[-1]:
            assert abs(math.hypot(g[0] - p[0], g[1] - p[1]) - ld) < 1e-9


def test_straight_line_convergence():
    # Start 1 m to the left of the x axis and 0.3 rad off the heading.
    path = [(-10.0, 0.0), (500.0, 0.0)]
    pp = PurePursuit(path, 5.0, 2.5)
    poses, steers = simulate(pp, (0.0, 1.0, 0.3), 5.0, 0.02, 1500)
    x, y, th = poses[-1]
    assert abs(y) < 1e-6 and abs(wrap(th)) < 1e-6
    assert abs(steers[-1]) < 1e-6


def test_small_error_matches_the_linear_closed_form():
    # Linearized on a straight line: e'' + (2 v / ld) e' + (2 v^2 / ld^2) e = 0, so with
    # a = v / ld and zero heading error at t = 0, e(t) = e0 exp(-a t) (cos a t + sin a t).
    v, ld, e0, dt = 5.0, 5.0, 1e-3, 0.001
    a = v / ld
    pp = PurePursuit([(-10.0, 0.0), (500.0, 0.0)], ld, 2.5)
    poses, _ = simulate(pp, (0.0, e0, 0.0), v, dt, 6000)
    worst = 0.0
    for k in range(0, 6001, 50):
        t = k * dt
        lin = e0 * math.exp(-a * t) * (math.cos(a * t) + math.sin(a * t))
        worst = max(worst, abs(poses[k][1] - lin))
    # The steering is held for dt, which acts like a delay of dt / 2.
    assert worst < 1e-3 * e0


def test_tracks_a_circle_exactly():
    # On a circle of radius R the goal point stays on the circle, the arc through it is the
    # circle itself, and the steering is atan(L / R).
    R, L, n = 10.0, 2.5, 4000
    path = [(R * math.sin(2 * math.pi * k / n), R - R * math.cos(2 * math.pi * k / n)) for k in range(n + 1)]
    pp = PurePursuit(path, 4.0, L)
    poses, steers = simulate(pp, (0.0, 0.0, 0.0), 2.0, 0.05, 250)
    for (x, y, _), d in zip(poses, steers):
        # The polyline has 4000 chords, so the circle is exact to about 1e-5 m.
        assert abs(math.hypot(x, y - R) - R) < 1e-5
        assert abs(d - math.atan(L / R)) < 1e-5


def test_steering_limit_is_respected():
    rng = random.Random(3)
    for _ in range(500):
        path = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(3)]
        pp = PurePursuit(path, rng.uniform(0.5, 3.0), 2.5, max_steer=0.5)
        pose = (rng.uniform(-5, 5), rng.uniform(-5, 5), rng.uniform(-math.pi, math.pi))
        assert -0.5 <= pp.steer(pose) <= 0.5


def test_rk4_follows_the_exact_arc():
    # With a constant steering angle the rear axle moves on a circle of radius L / tan(delta).
    L, delta, v, dt = 2.5, 0.3, 3.0, 0.01
    q = (0.0, 0.0, 0.0)
    for _ in range(300):
        q = rk4_step(q, v, delta, L, dt)
    r = L / math.tan(delta)
    th = v * 3.0 / r
    assert abs(q[0] - r * math.sin(th)) < 1e-9 and abs(q[1] - r * (1 - math.cos(th))) < 1e-9
