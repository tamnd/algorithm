# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stewart-trinkle-time-stepping/. The authors are listed in prov/EWJYN8.jsonl.
"""Tests of Stewart-Trinkle time stepping. Units are SI, g = 9.81 m/s^2.

The integration is the one of the scheme itself (a semi-implicit Euler step on
the velocity, then q+ = q + h v+), with the step h given in each test.
"""

import math
import random

from stewart_trinkle_time_stepping import (
    PlanarBody,
    build_lcp,
    contact_data,
    lcp_enumerate,
    lcp_residual,
    lemke,
    simulate,
    step,
    velocity_from_impulses,
)

G = 9.81


def close(a, b, tol):
    return all(abs(x - y) <= tol for x, y in zip(a, b))


def random_lcp(rng, m, psd_only=False):
    """A = B B^T + 0.1 I plus a skew part: positive definite, so the LCP has one solution."""
    B = [[rng.uniform(-1, 1) for _ in range(m)] for _ in range(m)]
    S = [[0.0 if psd_only else rng.uniform(-1, 1) for _ in range(m)] for _ in range(m)]
    A = [[sum(B[i][k] * B[j][k] for k in range(m)) + (0.1 if i == j else 0.0) + S[i][j] - S[j][i]
          for j in range(m)] for i in range(m)]
    b = [rng.uniform(-1, 1) for _ in range(m)]
    return A, b


def test_lemke_matches_enumeration_on_positive_definite_matrices():
    rng = random.Random(7)
    for _ in range(150):
        A, b = random_lcp(rng, rng.randint(1, 5))
        z = lemke(A, b)
        sols = lcp_enumerate(A, b)
        assert z is not None and len(sols) == 1
        assert close(z, sols[0], 1e-8)
        assert lcp_residual(A, b, z) < 1e-9


def test_lemke_trivial_and_ray_cases():
    assert lemke([[2.0, 1.0], [1.0, 2.0]], [1.0, 0.0]) == [0.0, 0.0]
    # w = -z - 1 >= 0 has no solution with z >= 0, so the method ends on a ray.
    assert lemke([[-1.0]], [-1.0]) is None
    # A degenerate case with equal entries of b: the lexicographic rule must not cycle.
    z = lemke([[1.0, 1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 1.0]], [-1.0, -1.0, -1.0])
    assert z is not None and lcp_residual([[1.0, 1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 1.0]], [-1.0, -1.0, -1.0], z) < 1e-12


def particle(mu=0.5, m=1.0):
    return PlanarBody(m, 1.0, mu, [(0.0, 0.0)])


def test_particle_at_rest_gets_weight_impulse():
    h = 0.01
    q, v, z = step(particle(), [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], h)
    assert close(v, [0.0, 0.0, 0.0], 1e-14)
    assert abs(z[0] - G * h) < 1e-14 and abs(z[1]) < 1e-14 and abs(z[2]) < 1e-14


def test_stick_below_and_slip_above_the_friction_limit():
    h, mu = 0.01, 0.5
    # 3 N < mu m g = 4.905 N: the particle sticks, friction impulse 3 h opposes the push.
    _, v, z = step(particle(mu), [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], h, f_ext=[3.0, 0.0, 0.0])
    assert close(v, [0.0, 0.0, 0.0], 1e-14)
    assert abs(z[2] - 3.0 * h) < 1e-14 and z[1] < 1e-14
    # 7 N > 4.905 N: it slides with acceleration 7 - 4.905 = 2.095 m/s^2.
    _, v, z = step(particle(mu), [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], h, f_ext=[7.0, 0.0, 0.0])
    assert abs(v[0] - (7.0 - mu * G) * h) < 1e-12
    assert abs(z[2] - mu * G * h) < 1e-12 and abs(z[3] - v[0]) < 1e-12


def test_sliding_particle_stops_at_the_closed_form_distance():
    h, mu, v0 = 0.001, 0.5, 2.0
    q, v = [0.0, 0.0, 0.0], [v0, 0.0, 0.0]
    n = 0
    while v[0] > 0.0:
        q, v, _ = step(particle(mu), q, v, h)
        n += 1
    assert n == math.ceil(v0 / (mu * G * h))
    # The exact stopping distance is v0^2 / (2 mu g) = 0.40775 m; the scheme is first order.
    assert abs(q[0] - v0 * v0 / (2 * mu * G)) < v0 * h
    assert abs(q[1]) < 1e-15


def test_falling_particle_lands_without_penetration_or_bounce():
    p = particle()
    q, v = [0.0, 0.1, 0.0], [0.3, 0.0, 0.0]
    lowest = q[1]
    for _ in range(300):
        q, v, _ = step(p, q, v, 0.001)
        lowest = min(lowest, q[1])
    assert lowest > -1e-12
    assert abs(v[1]) < 1e-12


def block(mu=0.4):
    a, b = 0.2, 0.1  # half width and half height in m
    m = 2.0
    I = m * ((2 * a) ** 2 + (2 * b) ** 2) / 12.0
    return PlanarBody(m, I, mu, [(-a, -b), (a, -b), (a, b), (-a, b)])


def test_block_at_rest_splits_its_weight():
    h = 0.01
    blk = block()
    _, v, z = step(blk, [0.0, 0.1, 0.0], [0.0, 0.0, 0.0], h)
    assert close(v, [0.0, 0.0, 0.0], 1e-13)
    assert abs(z[0] - G * h) < 1e-12 and abs(z[1] - G * h) < 1e-12


def test_block_step_matches_enumeration_of_all_complementarity_cases():
    rng = random.Random(3)
    blk = block()
    h = 0.01
    for _ in range(25):
        q = [0.0, 0.1, 0.0]
        v = [rng.uniform(-1, 1), rng.uniform(-0.5, 0.0), rng.uniform(-1, 1)]
        f = [rng.uniform(-10, 10), -blk.m * G, rng.uniform(-1, 1)]
        A, b, v_star, cols, _ = build_lcp(blk, q, v, h, f, 0.01)
        z = lemke(A, b)
        assert z is not None and lcp_residual(A, b, z) < 1e-10
        sols = lcp_enumerate(A, b)
        assert any(close(z, s, 1e-8) for s in sols)
        v_lemke, _ = velocity_from_impulses(blk, v_star, cols, z)
        for s in sols:
            assert close(velocity_from_impulses(blk, v_star, cols, s)[0], v_lemke, 1e-8)


def kinetic(body, v):
    return 0.5 * (body.m * (v[0] ** 2 + v[1] ** 2) + body.I * v[2] ** 2)


def test_contact_impulses_lie_in_the_cone_and_remove_energy():
    rng = random.Random(11)
    blk = block()
    h = 0.005
    for _ in range(40):
        # Every gap is at least 0 at the start of the step; the lemma needs this.
        q = [0.0, 0.0, rng.uniform(-0.02, 0.02)]
        lowest = min(contact_data(q, p)[0] for p in blk.points)
        q[1] = -lowest + rng.uniform(0.0, 0.004)
        v = [rng.uniform(-2, 2), rng.uniform(-2, 0.5), rng.uniform(-3, 3)]
        f = [0.0, -blk.m * G, 0.0]
        A, b, v_star, cols, phis = build_lcp(blk, q, v, h, f, 0.01)
        if A is None:
            continue
        z = lemke(A, b)
        c = len(phis)
        for i in range(c):
            assert z[i] >= 0.0
            assert z[c + 2 * i] + z[c + 2 * i + 1] <= blk.mu * z[i] + 1e-12
        v_next, _ = velocity_from_impulses(blk, v_star, cols, z)
        assert kinetic(blk, v_next) <= kinetic(blk, v_star) + 1e-12


def test_painleve_rod_gets_an_impulsive_stop():
    # A rod of length 1 m and mass 1 kg leans at theta = atan 2 with mu = 1.5 > 4/3.
    # Its lower end slides away from the center at 1 m/s. The acceleration form has
    # no solution here; the impulse form stops the end with an impulse near (0.4, 0.3) N s.
    l, th = 0.5, math.atan(2.0)
    rod = PlanarBody(1.0, (2 * l) ** 2 / 12.0, 1.5, [(-l, 0.0)])
    q = [l * math.cos(th), l * math.sin(th), th]
    v = [-1.0, 0.0, 0.0]
    for h, tol in ((1e-3, 0.02), (1e-4, 0.002)):
        A, b, v_star, cols, _ = build_lcp(rod, q, v, h, [0.0, -G, 0.0], 0.01)
        z = lemke(A, b)
        assert z is not None and lcp_residual(A, b, z) < 1e-12
        v_next, _ = velocity_from_impulses(rod, v_star, cols, z)
        _, n, d = contact_data(q, (-l, 0.0))
        slip = sum(d[k] * v_next[k] for k in range(3))
        assert abs(slip) < 1e-12
        assert abs(z[0] - 0.3) < tol and abs(z[1] - z[2] - 0.4) < tol


def test_sliding_block_keeps_both_corners_down_and_stops():
    blk = block(mu=0.3)
    q, v = simulate(blk, [0.0, 0.1, 0.0], [1.5, 0.0, 0.0], 0.002, 400)
    assert close(v, [0.0, 0.0, 0.0], 1e-9)
    assert abs(q[2]) < 1e-9 and abs(q[1] - 0.1) < 1e-9
    assert abs(q[0] - 1.5 ** 2 / (2 * 0.3 * G)) < 1.5 * 0.002
