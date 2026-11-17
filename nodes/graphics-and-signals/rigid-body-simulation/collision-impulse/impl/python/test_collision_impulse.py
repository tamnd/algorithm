# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/collision-impulse/. The authors are listed in prov/RVWXT5.jsonl.

import math
import random
from fractions import Fraction as F

from anim import q_normalize, q_to_mat3
from collision_impulse import (
    Body,
    angular_momentum,
    collision_impulse,
    effective_inverse_mass,
    energy_loss,
    kinetic_energy,
    linear_momentum,
    relative_normal_velocity,
    static_body,
)


def conj(r, d):
    """R diag(d) R^T, exact for Fraction entries."""
    return [[sum(r[i][k] * d[k] * r[j][k] for k in range(3)) for j in range(3)] for i in range(3)]


def rational_rotation(rng):
    """An exact rotation matrix from an integer quaternion (a, b, c, d) divided by its squared norm."""
    while True:
        a, b, c, d = (rng.randint(-5, 5) for _ in range(4))
        s = a * a + b * b + c * c + d * d
        if s:
            break
    return [
        [F(a * a + b * b - c * c - d * d, s), F(2 * (b * c - a * d), s), F(2 * (b * d + a * c), s)],
        [F(2 * (b * c + a * d), s), F(a * a - b * b + c * c - d * d, s), F(2 * (c * d - a * b), s)],
        [F(2 * (b * d - a * c), s), F(2 * (c * d + a * b), s), F(a * a - b * b - c * c + d * d, s)],
    ]


def rand_frac(rng, lo=-3, hi=3, den=4):
    return F(rng.randint(lo * den, hi * den), den)


def random_body(rng, exact=True):
    m = F(rng.randint(1, 8), rng.randint(1, 4))
    d = [F(rng.randint(1, 9), rng.randint(1, 5)) for _ in range(3)]
    r = rational_rotation(rng)
    x = tuple(rand_frac(rng) for _ in range(3))
    v = tuple(rand_frac(rng) for _ in range(3))
    w = tuple(rand_frac(rng) for _ in range(3))
    return Body(x, v, w, 1 / m, conj(r, [1 / t for t in d]), m=m, I=conj(r, d))


def unit_normal(rng):
    """A rational unit vector from an integer quaternion: R e_y."""
    r = rational_rotation(rng)
    return (r[0][1], r[1][1], r[2][1])


def approaching_pair(rng):
    while True:
        a, b = random_body(rng), random_body(rng)
        p = tuple(rand_frac(rng) for _ in range(3))
        n = unit_normal(rng)
        if relative_normal_velocity(a, b, p, n) < 0:
            return a, b, p, n


def test_page_example():
    c, s = F(4, 5), F(3, 5)
    rot = [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    box = Body((0, 0, 0), (F(1), F(-2), F(0)), (0, 0, 0), F(1), conj(rot, [6, F(12, 5), F(12, 5)]), m=F(1),
               I=conj(rot, [F(1, 6), F(5, 12), F(5, 12)]))
    ground = static_body((0, -1, 0))
    p, n = (F(-1, 2), F(-1), F(0)), (0, 1, 0)
    assert effective_inverse_mass(box, ground, p, n) == F(8, 5)
    assert kinetic_energy([box]) == F(5, 2)
    j = collision_impulse(box, ground, p, n, F(1, 2))
    assert j == F(15, 8)
    assert box.v == (1, F(-1, 8), 0)
    assert box.w == (0, 0, F(-9, 4))
    assert box.point_velocity(p) == (F(-5, 4), 1, 0)
    assert kinetic_energy([box]) == F(25, 16)


def test_restitution_law_and_momentum_exact():
    rng = random.Random(7)
    for _ in range(60):
        a, b, p, n = approaching_pair(rng)
        e = F(rng.randint(0, 4), 4)
        v0 = relative_normal_velocity(a, b, p, n)
        k = effective_inverse_mass(a, b, p, n)
        lin0, ang0, ke0 = linear_momentum([a, b]), angular_momentum([a, b]), kinetic_energy([a, b])
        ang_p0 = angular_momentum([a, b], origin=p)
        j = collision_impulse(a, b, p, n, e)
        assert j > 0
        assert relative_normal_velocity(a, b, p, n) == -e * v0
        assert linear_momentum([a, b]) == lin0
        assert angular_momentum([a, b]) == ang0
        assert angular_momentum([a, b], origin=p) == ang_p0
        assert ke0 - kinetic_energy([a, b]) == energy_loss(v0, k, e)


def test_elastic_keeps_energy_and_plastic_stops_normal_motion():
    rng = random.Random(11)
    for _ in range(30):
        a, b, p, n = approaching_pair(rng)
        ke0 = kinetic_energy([a, b])
        collision_impulse(a, b, p, n, F(1))
        assert kinetic_energy([a, b]) == ke0
        a, b, p, n = approaching_pair(rng)
        collision_impulse(a, b, p, n, F(0))
        assert relative_normal_velocity(a, b, p, n) == 0


def test_separating_contact_is_unchanged():
    rng = random.Random(3)
    for _ in range(20):
        a, b = random_body(rng), random_body(rng)
        p = tuple(rand_frac(rng) for _ in range(3))
        n = unit_normal(rng)
        if relative_normal_velocity(a, b, p, n) < 0:
            n = tuple(-t for t in n)
        va, wa, vb, wb = a.v, a.w, b.v, b.w
        assert collision_impulse(a, b, p, n, F(1, 2)) == 0
        assert (a.v, a.w, b.v, b.w) == (va, wa, vb, wb)


def test_head_on_matches_newton_closed_form():
    rng = random.Random(5)
    zero = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for _ in range(30):
        m1, m2 = F(rng.randint(1, 9)), F(rng.randint(1, 9))
        u1, u2 = F(rng.randint(1, 9)), F(-rng.randint(0, 9))
        e = F(rng.randint(0, 4), 4)
        a = Body((-1, 0, 0), (u1, 0, 0), (0, 0, 0), 1 / m1, zero, m=m1, I=zero)
        b = Body((1, 0, 0), (u2, 0, 0), (0, 0, 0), 1 / m2, zero, m=m2, I=zero)
        collision_impulse(a, b, (0, 0, 0), (-1, 0, 0), e)  # the normal points from b to a
        v1 = (m1 * u1 + m2 * u2 - m2 * e * (u1 - u2)) / (m1 + m2)
        v2 = (m1 * u1 + m2 * u2 + m1 * e * (u1 - u2)) / (m1 + m2)
        assert a.v[0] == v1 and b.v[0] == v2


def test_drop_check_value():
    g, h, e = 9.81, 1.0, 0.5
    ball = Body((0, 0.1, 0), (0, -math.sqrt(2 * g * h), 0), (0, 0, 0), 1.0, [[25, 0, 0], [0, 25, 0], [0, 0, 25]])
    ground = static_body((0, -1, 0))
    collision_impulse(ball, ground, (0, 0, 0), (0, 1, 0), e)
    assert abs(ball.v[1] ** 2 / (2 * g) - 0.25) < 1e-12
    assert ball.w == (0.0, 0.0, 0.0)


def test_float_momentum_with_random_rotations():
    rng = random.Random(19)
    for _ in range(100):
        bodies = []
        for _ in range(2):
            q = q_normalize(tuple(rng.uniform(-1, 1) for _ in range(4)))
            r = q_to_mat3(q)
            d = [rng.uniform(0.2, 3.0) for _ in range(3)]
            m = rng.uniform(0.5, 5.0)
            bodies.append(Body(tuple(rng.uniform(-2, 2) for _ in range(3)), tuple(rng.uniform(-3, 3) for _ in range(3)),
                               tuple(rng.uniform(-3, 3) for _ in range(3)), 1 / m, conj(r, [1 / t for t in d]), m=m,
                               I=conj(r, d)))
        a, b = bodies
        p = tuple(rng.uniform(-2, 2) for _ in range(3))
        n = q_rotate_y(rng)
        if relative_normal_velocity(a, b, p, n) > 0:
            n = tuple(-t for t in n)
        lin0, ang0 = linear_momentum(bodies), angular_momentum(bodies)
        ke0 = kinetic_energy(bodies)
        collision_impulse(a, b, p, n, 1.0)
        for x, y in zip(linear_momentum(bodies) + angular_momentum(bodies), lin0 + ang0):
            assert abs(x - y) <= 1e-10 * (1 + abs(y))
        assert abs(kinetic_energy(bodies) - ke0) <= 1e-12 * max(1.0, ke0)


def q_rotate_y(rng):
    r = q_to_mat3(q_normalize(tuple(rng.uniform(-1, 1) for _ in range(4))))
    return (r[0][1], r[1][1], r[2][1])


def test_two_static_bodies_raise():
    a, b = static_body((0, 0, 0)), static_body((1, 0, 0))
    a.v = (1, 0, 0)
    try:
        collision_impulse(a, b, (0, 0, 0), (-1, 0, 0), 1)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
