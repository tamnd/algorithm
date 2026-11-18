# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-elastic-rods/. The authors are listed in prov/56ZBR0.jsonl.
"""Tests of discrete elastic rods (isotropic, straight at rest).

The forces are compared with central differences of the energy, for the
bending and stretching terms on free rods and for the twist term through
the holonomy on rods with clamped ends. Further tests: the length of the
curvature binormal, a planar rod has no holonomy, rigid motions keep the
energy, the quasistatic twist is the minimum over the interior angles, and
a cantilever approaches beam theory as the rod is refined.
"""

import math
import random

import anim
from discrete_elastic_rods import (Rod, bishop_frames, curvature_binormal, energy, forces, parallel_transport,
                                   step, twist_angle)


def straight(n, h=0.2):
    return [(h * i, 0.0, 0.0) for i in range(n + 1)]


def jitter(rng, pts, amount, keep=()):
    out = []
    for i, p in enumerate(pts):
        if i in keep:
            out.append(p)
        else:
            out.append(tuple(c + rng.uniform(-amount, amount) for c in p))
    return out


def flat(x):
    return [c for p in x for c in p]


def unflat(z):
    return [tuple(z[3 * i:3 * i + 3]) for i in range(len(z) // 3)]


def test_curvature_binormal_length_and_direction():
    rng = random.Random(1)
    for _ in range(200):
        a = tuple(rng.uniform(-1, 1) for _ in range(3))
        b = tuple(rng.uniform(-1, 1) for _ in range(3))
        phi = math.acos(max(-1.0, min(1.0, anim.dot(a, b) / (anim.norm(a) * anim.norm(b)))))
        if phi > 3.0:
            continue
        kb = curvature_binormal(a, b)
        assert abs(anim.norm(kb) - 2.0 * math.tan(phi / 2.0)) < 1e-9 * (1 + anim.norm(kb))
        assert abs(anim.dot(kb, a)) < 1e-9 and abs(anim.dot(kb, b)) < 1e-9
    assert anim.norm(curvature_binormal((1, 0, 0), (2, 0, 0))) == 0.0


def test_parallel_transport_is_a_rotation_taking_t1_to_t2():
    rng = random.Random(2)
    for _ in range(200):
        t1 = anim.normalize(tuple(rng.uniform(-1, 1) for _ in range(3)))
        t2 = anim.normalize(tuple(rng.uniform(-1, 1) for _ in range(3)))
        if anim.dot(t1, t2) < -0.9:
            continue
        assert anim.norm(anim.sub(parallel_transport(t1, t2, t1), t2)) < 1e-12
        b = anim.cross(t1, t2)
        v = tuple(rng.uniform(-1, 1) for _ in range(3))
        w = parallel_transport(t1, t2, v)
        assert abs(anim.norm(w) - anim.norm(v)) < 1e-12
        if anim.norm(b) > 1e-6:
            assert abs(anim.dot(w, b) - anim.dot(v, b)) < 1e-12


def test_bend_and_stretch_force_is_minus_gradient():
    rng = random.Random(3)
    rod = Rod(straight(6), alpha=1.3, beta=0.7, ks=40.0)
    for _ in range(10):
        x = jitter(rng, rod.rest, 0.08)
        f = forces(rod, x, twist=0.0)
        g = anim.num_grad(lambda z: energy(rod, unflat(z)), flat(x))
        s = max(map(abs, g))
        for a, b in zip(flat(f), g):
            assert abs(a + b) <= 1e-6 * s


def test_twist_force_through_holonomy_is_minus_gradient():
    rng = random.Random(4)
    n = 7
    rod = Rod(straight(n), alpha=0.0, beta=0.9, ks=0.0)
    u0 = (0.0, 1.0, 0.0)
    clamped = {0, 1, n - 1, n}
    for k in range(10):
        x = jitter(rng, rod.rest, 0.1, keep=clamped)
        d_end = (0.0, math.cos(0.5 * k), math.sin(0.5 * k))
        tw = twist_angle(x, u0, d_end)
        f = forces(rod, x, twist=tw)
        free = [i for i in range(n + 1) if i not in clamped]

        def e_free(z):
            y = list(x)
            for j, i in enumerate(free):
                y[i] = tuple(z[3 * j:3 * j + 3])
            return energy(rod, y, u0, d_end, near=tw)

        g = anim.num_grad(e_free, [c for i in free for c in x[i]])
        got = [c for i in free for c in f[i]]
        s = max(map(abs, g))
        assert s > 1e-3
        for a, b in zip(got, g):
            assert abs(a + b) <= 1e-6 * s


def test_full_force_with_clamped_twist_is_minus_gradient():
    rng = random.Random(5)
    n = 6
    rod = Rod(straight(n), alpha=0.8, beta=1.1, ks=30.0)
    u0 = (0.0, 0.0, 1.0)
    clamped = {0, 1, n - 1, n}
    x = jitter(rng, rod.rest, 0.07, keep=clamped)
    d_end = (0.0, -math.sin(2.0), math.cos(2.0))
    tw = twist_angle(x, u0, d_end, near=2.0 + 2 * math.pi)
    assert tw > 2 * math.pi
    f = forces(rod, x, twist=tw)
    free = [i for i in range(n + 1) if i not in clamped]

    def e_free(z):
        y = list(x)
        for j, i in enumerate(free):
            y[i] = tuple(z[3 * j:3 * j + 3])
        return energy(rod, y, u0, d_end, near=tw)

    g = anim.num_grad(e_free, [c for i in free for c in x[i]])
    s = max(map(abs, g))
    for a, b in zip([c for i in free for c in f[i]], g):
        assert abs(a + b) <= 1e-6 * s


def test_planar_rod_has_no_holonomy():
    rng = random.Random(6)
    for _ in range(20):
        x = [(0.2 * i + rng.uniform(-0.05, 0.05), rng.uniform(-0.1, 0.1), 0.0) for i in range(8)]
        u, _ = bishop_frames(x, (0.0, 0.0, 1.0))
        for v in u:
            assert anim.norm(anim.sub(v, (0.0, 0.0, 1.0))) < 1e-12
        assert abs(twist_angle(x, (0.0, 0.0, 1.0), (0.0, 0.0, 1.0))) < 1e-12


def test_rigid_motion_keeps_energy_and_rotates_forces():
    rng = random.Random(7)
    n = 6
    rod = Rod(straight(n), alpha=1.0, beta=1.0, ks=20.0)
    u0 = (0.0, 1.0, 0.0)
    clamped = {0, 1, n - 1, n}
    x = jitter(rng, rod.rest, 0.1, keep=clamped)
    d_end = (0.0, math.cos(0.8), math.sin(0.8))
    tw = twist_angle(x, u0, d_end)
    q = anim.q_to_mat3(anim.q_from_axis_angle((0.3, -1.0, 0.5), 1.1))
    t = (0.4, -2.0, 1.0)
    y = [anim.add(anim.matvec(q, p), t) for p in x]
    tw2 = twist_angle(y, anim.matvec(q, u0), anim.matvec(q, d_end), near=tw)
    assert abs(tw2 - tw) < 1e-12
    assert abs(energy(rod, x, u0, d_end) - energy(rod, y, anim.matvec(q, u0), anim.matvec(q, d_end))) < 1e-12
    fx, fy = forces(rod, x, tw), forces(rod, y, tw2)
    for a, b in zip(fx, fy):
        assert anim.norm(anim.sub(anim.matvec(q, a), b)) < 1e-10


def test_straight_rod_has_no_force_even_when_twisted():
    rod = Rod(straight(5), alpha=1.0, beta=1.0, ks=10.0)
    for tw in (0.0, 1.0, 7.0):
        f = forces(rod, rod.rest, twist=tw)
        assert max(abs(c) for p in f for c in p) < 1e-14
    assert abs(energy(rod, rod.rest, (0, 1, 0), (0, 0, 1)) - rod.beta * (math.pi / 2) ** 2 / rod.Lbar) < 1e-12


def test_free_rod_net_force_and_torque_are_zero():
    rng = random.Random(8)
    rod = Rod(straight(7), alpha=1.0, beta=1.0, ks=25.0)
    x = jitter(rng, rod.rest, 0.1)
    f = forces(rod, x)
    net = [sum(p[k] for p in f) for k in range(3)]
    torque = [0.0, 0.0, 0.0]
    for p, fp in zip(x, f):
        torque = list(anim.add(torque, anim.cross(p, fp)))
    assert max(map(abs, net)) < 1e-10 and max(map(abs, torque)) < 1e-10


def test_quasistatic_twist_is_the_minimum_over_interior_angles():
    rng = random.Random(9)
    lbar = [rng.uniform(0.2, 0.6) for _ in range(6)]
    beta, total = 0.7, 2.3

    def e(theta):
        return sum(beta * (theta[i + 1] - theta[i]) ** 2 / lbar[i] for i in range(len(lbar)))

    theta = [0.0] + [rng.uniform(-3, 3) for _ in range(len(lbar) - 1)] + [total]
    for _ in range(2000):
        for i in range(1, len(theta) - 1):
            a, b = lbar[i - 1], lbar[i]
            theta[i] = (theta[i - 1] / a + theta[i + 1] / b) / (1.0 / a + 1.0 / b)
    assert abs(e(theta) - beta * total ** 2 / sum(lbar)) < 1e-10


def test_twisted_clamped_rod_settles_straight():
    rng = random.Random(10)
    n = 6
    rod = Rod(straight(n), alpha=1.0, beta=1.0, ks=50.0)
    clamped = [0, 1, n - 1, n]
    x = jitter(rng, rod.rest, 0.05, keep=set(clamped))
    v = [(0.0, 0.0, 0.0)] * (n + 1)
    u0, d_end = (0.0, 1.0, 0.0), (0.0, math.cos(1.0), math.sin(1.0))
    tw = twist_angle(x, u0, d_end, near=1.0)
    e0 = energy(rod, x, u0, d_end, near=tw)
    for _ in range(3000):
        x, v, tw = step(rod, x, v, 0.002, fixed=clamped, damping=5.0, u0=u0, d_end=d_end, twist=tw)
    assert max(abs(c) for i in range(n + 1) for c in anim.sub(x[i], rod.rest[i])) < 1e-4
    assert abs(tw - 1.0) < 1e-6
    assert energy(rod, x, u0, d_end, near=tw) < e0


def cantilever_tip(n, dt, steps):
    h = 0.9 / (n - 1)
    rod = Rod([(h * (i - 1), 0.0, 0.0) for i in range(n + 1)], alpha=1.0, beta=1.0, ks=200.0)
    x, v = list(rod.rest), [(0.0, 0.0, 0.0)] * (n + 1)
    for _ in range(steps):
        x, v, _ = step(rod, x, v, dt, fixed=[0, 1], gravity=(0.0, -0.1, 0.0), damping=3.0)
    return x[-1][1]


def test_cantilever_converges_to_beam_theory():
    beam = -0.1 * 0.9 ** 4 / 8.0
    coarse = cantilever_tip(6, 0.004, 2500) - beam
    fine = cantilever_tip(11, 0.002, 3500) - beam
    assert coarse < 0.0 and fine < 0.0
    assert abs(fine) < 0.25 * abs(beam)
    assert 1.5 < coarse / fine < 2.6
