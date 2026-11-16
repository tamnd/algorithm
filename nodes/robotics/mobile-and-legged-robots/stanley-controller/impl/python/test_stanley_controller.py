# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stanley-controller/. The authors are listed in prov/8QP9X9.jsonl.

import math
import random

from stanley_controller import Stanley, front_rhs, implicit_time, simulate, wrap

L = 2.85  # the wheelbase of the vehicle in Thrun et al. (2006)
STRAIGHT = [(-100.0, 0.0), (5000.0, 0.0)]


def test_error_rate_is_independent_of_the_heading():
    # On a straight path, without saturation, e' = -k e / sqrt(1 + (k e / u)^2) for any heading.
    rng = random.Random(1)
    checked = 0
    for _ in range(3000):
        k, u = rng.uniform(0.2, 5.0), rng.uniform(0.5, 20.0)
        y, th = rng.uniform(-10, 10), rng.uniform(-1.2, 1.2)
        st = Stanley(STRAIGHT, k, L)
        delta = st.steer((0.0, y, th), u)
        e = -y  # positive when the front axle is to the right of the path
        assert abs(st.error - e) < 1e-12 and abs(st.heading_error + th) < 1e-12
        if abs(-th + math.atan(k * e / u)) >= st.max_steer:
            continue  # saturated: the formula does not hold
        checked += 1
        de = -front_rhs((0.0, y, th), u, delta, L)[1]
        assert abs(de - (-k * e / math.sqrt(1.0 + (k * e / u) ** 2))) < 1e-9
    assert checked > 2000


def test_continuous_loop_matches_the_implicit_solution():
    # k t = F(s0) - F(s(t)) with s = k e / u, for the continuous closed loop.
    k, u, dt = 1.0, 5.0, 0.01
    st = Stanley(STRAIGHT, k, L)
    poses, _ = simulate(st, (0.0, 2.0, 0.3), u, dt, 800, hold=False)
    s0 = k * -2.0 / u
    for n, p in enumerate(poses[1:], 1):
        e = -p[1]
        assert e < 0.0  # monotone: no overshoot
        assert abs(implicit_time(s0, k * e / u) / k - n * dt) < 1e-8


def test_small_error_decays_like_exp_minus_kt():
    # For |k e / u| small the solution is close to e0 exp(-k t).
    k, u, e0 = 2.0, 10.0, 1e-3
    st = Stanley(STRAIGHT, k, L)
    poses, _ = simulate(st, (0.0, -e0, 0.0), u, 0.01, 300, hold=False)
    for n, p in enumerate(poses):
        assert abs(p[1] + e0 * math.exp(-k * n * 0.01)) < 1e-9


def test_circle_is_an_equilibrium():
    # On a circle of radius R the front axle stays on the circle with delta = asin(L / R)
    # and the vehicle heading behind the path heading by the same angle.
    R, n = 20.0, 20000
    path = [(R * math.sin(2 * math.pi * j / n), R - R * math.cos(2 * math.pi * j / n)) for j in range(n + 1)]
    st = Stanley(path, 2.0, L, window=200)
    poses, steers = simulate(st, (0.0, 0.0, -math.asin(L / R)), 3.0, 0.02, 500)
    for (x, y, _), d in zip(poses, steers):
        # The chords of the polyline turn by 2 pi / n = 3.1e-4 rad, which bounds the error.
        assert abs(math.hypot(x, y - R) - R) < 1e-4
        assert abs(d - math.asin(L / R)) < 4e-4


def test_converges_with_a_steering_limit():
    # With the 24 degree limit of the paper, from errors up to 10 m and 1 rad.
    rng = random.Random(4)
    for _ in range(25):
        y0, th0 = rng.uniform(-10, 10), rng.uniform(-1, 1)
        st = Stanley(STRAIGHT, rng.uniform(0.5, 3.0), L, max_steer=math.radians(24))
        poses, steers = simulate(st, (0.0, y0, th0), rng.uniform(2.0, 10.0), 0.01, 4000)
        assert all(abs(d) <= math.radians(24) + 1e-15 for d in steers)
        assert abs(poses[-1][1]) < 1e-6 and abs(wrap(poses[-1][2])) < 1e-6


def test_digital_controller_is_close_to_the_continuous_one():
    k, u = 1.0, 5.0
    a, _ = simulate(Stanley(STRAIGHT, k, L), (0.0, 2.0, 0.3), u, 0.01, 800, hold=False)
    b, _ = simulate(Stanley(STRAIGHT, k, L), (0.0, 2.0, 0.3), u, 0.01, 800, hold=True)
    assert max(abs(p[1] - q[1]) for p, q in zip(a, b)) < 0.02


def test_softening_constant():
    # With ks > 0 the law is defined at u = 0 and gives the cross-track term atan(k e / ks).
    st = Stanley(STRAIGHT, 1.0, L, soft=1.0)
    assert abs(st.steer((0.0, 0.5, 0.0), 0.0) - math.atan(-0.5)) < 1e-15
