# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/impulse-based-simulation/. The authors are listed in prov/P8GDCY.jsonl.

import math
import random
from fractions import Fraction as F

from impulse_based_simulation import (
    GROUND,
    Disc,
    angular_momentum,
    apply_impulse,
    collide,
    contact_matrix,
    contact_velocity,
    kinetic_energy,
    linear_momentum,
    microcollision_impulse,
    simulate,
)

G = 9.81


def energy_change(K, u, p):
    """T+ - T- = p . u + p^T K p / 2 for an impulse p at the contact."""
    ktt, ktn, knn = K
    return p[0] * u[0] + p[1] * u[1] + (ktt * p[0] ** 2 + 2 * ktn * p[0] * p[1] + knn * p[1] ** 2) / 2


def random_spd(rng, exact):
    if exact:
        a, b = F(rng.randint(-8, 8), rng.randint(1, 4)), F(rng.randint(-8, 8), rng.randint(1, 4))
        c = F(rng.randint(1, 8), rng.randint(1, 4))
        return a * a + F(1, 5), a * b, b * b + c * c
    a, b, c = rng.uniform(0.3, 1.5), rng.uniform(-1.5, 1.5), rng.uniform(0.3, 1.5)
    return a * a, a * b, b * b + c * c


def test_page_example_rod():
    K = (F(73, 25), F(36, 25), F(52, 25))
    u = (F(-1, 2), F(-1))
    trace = []
    p = collide(K, u, F(1, 2), F(1), trace)
    assert [(m, ev) for m, ev, *_ in trace] == [("slide", "stop"), ("stick", "max"), ("stick", "end")]
    assert trace[0][2:] == (F(5, 58), F(5, 29), 0, F(-15, 29))
    assert trace[1][2:4] == (F(-1, 10), F(11, 20))
    assert p == (F(-271, 730), F(11, 10))
    assert (u[0] + K[0] * p[0] + K[1] * p[1], u[1] + K[1] * p[0] + K[2] * p[1]) == (0, F(55, 73))
    assert energy_change(K, u, p) == F(-25, 584)
    trace = []
    collide(K, u, F(1, 5), F(1), trace)
    assert [m for m, *_ in trace] == ["slide", "slide again", "slide"]


def test_collide_poisson_cone_and_phase_bound_exact():
    rng = random.Random(2)
    for _ in range(300):
        K = random_spd(rng, True)
        u = (F(rng.randint(-12, 12), 4), F(-rng.randint(1, 12), 4))
        mu, e = F(rng.randint(0, 12), 10), F(rng.randint(0, 4), 4)
        trace = []
        p = collide(K, u, mu, e, trace)
        assert len(trace) <= 3
        assert abs(p[0]) <= mu * p[1]
        p_mc = [s[3] for s in trace if s[1] == "max"]
        assert len(p_mc) == 1 and p[1] == (1 + e) * p_mc[0]
        for mode, _, pt, pn, ut, un in trace:
            assert abs(pt) <= mu * pn
            if mode == "stick":
                assert ut == 0
        modes = [s[0] for s in trace]
        if "stick" in modes:
            assert modes[modes.index("stick"):] == ["stick"] * (len(modes) - modes.index("stick"))
            u_end = u[0] + K[0] * p[0] + K[1] * p[1]
            assert u_end == 0


def test_collide_frictionless_is_the_newton_impulse():
    rng = random.Random(4)
    for _ in range(100):
        K = random_spd(rng, True)
        u = (F(rng.randint(-12, 12), 4), F(-rng.randint(1, 12), 4))
        e = F(rng.randint(0, 4), 4)
        assert collide(K, u, 0, e) == (0, -(1 + e) * u[1] / K[2])


def euler_collide(K, u, mu, e, h):
    """Small fixed steps in p_n with the sign rule of Coulomb friction and no sticking logic."""
    ktt, ktn, knn = K
    ut, un = u
    pt = pn = 0.0
    target = None
    while target is None or pn < target:
        dt = -mu if ut > 0 else (mu if ut < 0 else 0.0)
        pt, pn = pt + dt * h, pn + h
        ut, un = ut + (ktt * dt + ktn) * h, un + (ktn * dt + knn) * h
        if target is None and un >= 0:
            target = (1 + e) * pn
    return pt, pn


def test_collide_matches_fine_integration():
    rng = random.Random(6)
    for _ in range(12):
        K = random_spd(rng, False)
        u = (rng.uniform(-2, 2), rng.uniform(-1.5, -0.3))
        mu, e = rng.uniform(0, 1), rng.uniform(0, 1)
        p = collide(K, u, mu, e)
        q = euler_collide(K, u, mu, e, 2e-4)
        assert abs(p[0] - q[0]) < 5e-3 * (1 + abs(p[0])) and abs(p[1] - q[1]) < 5e-3 * (1 + p[1])


def test_microcollision_does_no_work():
    rng = random.Random(8)
    for _ in range(50):
        a = Disc((0, F(1, 2)), (F(rng.randint(-8, 8), 8), F(-rng.randint(1, 8), 8)), F(rng.randint(-8, 8), 4),
                 F(rng.randint(1, 6)), F(1, 2))
        b = Disc((F(rng.randint(-4, 4), 4), F(-1)), (F(rng.randint(-8, 8), 8), F(0)), F(rng.randint(-8, 8), 4),
                 F(rng.randint(1, 6)), F(1, 3))
        for other in (GROUND, b):
            n = (0, 1)
            r_a = (0, -a.radius)
            r_b = (0, 0) if other is GROUND else (a.x[0] - other.x[0], a.x[1] - a.radius - other.x[1])
            K = contact_matrix(a, other, r_a, r_b, n)
            u = contact_velocity(a, other, r_a, r_b, n)
            bodies = [a] if other is GROUND else [a, other]
            t0 = kinetic_energy(bodies)
            apply_impulse(a, other, r_a, r_b, n, microcollision_impulse(K, u))
            assert kinetic_energy(bodies) == t0
            assert contact_velocity(a, other, r_a, r_b, n) == (-u[0], -u[1])


def test_drop_check_value():
    eps = 1e-4
    ball = Disc((0.0, 0.5 + eps + 1.0), (0.0, 0.0), 0.0, 1.0, 0.5)
    log = simulate([ball], 0.6, mu=0.5, e=0.5, eps_c=eps)
    assert len(log) == 1 and log[0][3] == "collision"
    assert abs(log[0][0] - math.sqrt(2 / G)) < 1e-12
    height = ball.x[1] - 0.5 - eps + ball.v[1] ** 2 / (2 * G)
    assert abs(height - 0.25) < 1e-12


def random_gas(rng, count):
    discs = []
    while len(discs) < count:
        x = (rng.uniform(-3, 3), rng.uniform(-3, 3))
        r = rng.uniform(0.2, 0.5)
        if all(math.hypot(x[0] - d.x[0], x[1] - d.x[1]) > r + d.radius + 0.1 for d in discs):
            v = (-x[0] / 2 + rng.uniform(-1, 1), -x[1] / 2 + rng.uniform(-1, 1))
            discs.append(Disc(x, v, rng.uniform(-2, 2), rng.uniform(0.5, 3), r))
    return discs


def test_elastic_frictionless_gas_keeps_energy_and_momentum():
    rng = random.Random(10)
    discs = random_gas(rng, 6)
    t0, p0, l0 = kinetic_energy(discs), linear_momentum(discs), angular_momentum(discs)
    log = simulate(discs, 6.0, mu=0.0, e=1.0, eps_c=1e-3, g=0.0, ground=False)
    assert len(log) >= 5
    assert abs(kinetic_energy(discs) - t0) < 1e-9 * t0
    assert all(abs(x - y) < 1e-9 for x, y in zip(linear_momentum(discs), p0))
    assert abs(angular_momentum(discs) - l0) < 1e-9


def test_frictional_gas_keeps_momentum_and_loses_energy():
    rng = random.Random(12)
    discs = random_gas(rng, 6)
    t0, p0, l0 = kinetic_energy(discs), linear_momentum(discs), angular_momentum(discs)
    log = simulate(discs, 6.0, mu=0.4, e=0.7, eps_c=1e-3, g=0.0, ground=False)
    assert len(log) >= 2
    assert kinetic_energy(discs) < t0
    assert all(abs(x - y) < 1e-9 for x, y in zip(linear_momentum(discs), p0))
    assert abs(angular_momentum(discs) - l0) < 1e-9


def test_disc_with_backspin_ends_rolling_at_the_coulomb_speed():
    for w0, v_final in ((4.0, 2 / 3), (12.0, -2 / 3)):
        disc = Disc((0.0, 0.5 + 1e-3 + 0.1), (2.0, 0.0), w0, 1.0, 0.5)
        simulate([disc], 2.0, mu=0.5, e=0.5, eps_c=1e-3)
        assert abs(disc.v[0] + disc.w * disc.radius) < 1e-9
        assert abs(disc.v[0] - v_final) < 1e-9


def test_resting_disc_has_a_bounded_event_rate():
    eps = 1e-3
    v_e = math.sqrt(2 * G * eps)
    disc = Disc((0.0, 0.5 + eps + 0.05), (0.3, 0.0), 0.0, 1.0, 0.5)
    log = simulate([disc], 3.0, mu=0.3, e=0.5, eps_c=eps)
    late = [ev for ev in log if ev[0] >= 2.0]
    assert late and all(kind == "micro" for _, _, _, kind, _ in late)
    assert all(0.5 * v_e <= -un < v_e for *_, un in late)
    assert len(late) <= G / (2 * 0.5 * v_e) + 1
    gap = disc.x[1] - disc.radius
    assert eps - 1e-12 <= gap + disc.v[1] ** 2 / (2 * G) < 2 * eps
