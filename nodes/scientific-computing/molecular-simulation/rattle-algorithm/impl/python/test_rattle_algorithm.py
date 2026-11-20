# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rattle-algorithm/. The authors are listed in prov/VJX93A.jsonl.

import math

from rattle_algorithm import constraint_errors, rattle_step


def gravity(x):
    return [[0.0, -1.0, 0.0] for _ in x]


def pendulum_state(theta, omega):
    # the anchor (index 0) is fixed by an inverse mass of 0; the bob has mass 1 and the rod length 1
    x = [[0.0, 0.0, 0.0], [math.sin(theta), -math.cos(theta), 0.0]]
    v = [[0.0, 0.0, 0.0], [omega * math.cos(theta), omega * math.sin(theta), 0.0]]
    return x, v


W_PEND, B_PEND = [0.0, 1.0], [(0, 1, 1.0)]


def angle_and_rate(x, v):
    bx, by = x[1][0], x[1][1]
    return math.atan2(bx, -by), bx * v[1][1] - by * v[1][0]


def agm(a, b):
    while abs(a - b) > 1e-15:
        a, b = 0.5 * (a + b), math.sqrt(a * b)
    return a


def measured_period(theta0, h):
    x, v = pendulum_state(theta0, 0.0)
    f = gravity(x)
    t, crossings = 0.0, []
    while len(crossings) < 3:
        xo = x[1][0]
        x, v, f = rattle_step(x, v, f, W_PEND, gravity, h, B_PEND)
        t += h
        if (xo > 0) != (x[1][0] > 0):
            crossings.append(t - h * x[1][0] / (x[1][0] - xo))
    return crossings[2] - crossings[0]


def test_pendulum_period_converges_at_second_order() -> None:
    theta0 = 1.0
    exact = 2 * math.pi / agm(1.0, math.cos(theta0 / 2))
    e1 = abs(measured_period(theta0, 0.02) - exact)
    e2 = abs(measured_period(theta0, 0.01) - exact)
    assert e1 < 1e-3
    assert 3.0 < e1 / e2 < 5.0


def chain():
    x = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.6, 0.8, 0.0], [1.4, 1.5, 0.7]]
    v = [[0.3, -0.2, 0.1], [0.0, 0.4, -0.3], [-0.5, 0.1, 0.2], [0.2, 0.0, 0.6]]
    bonds = [(k, k + 1, math.dist(x[k], x[k + 1])) for k in range(3)]
    w = [1.0, 0.5, 0.5, 1.0]
    # remove the velocity components that break the constraints before the first step
    _, v, _ = rattle_step(x, v, [[0.0] * 3 for _ in x], w, lambda y: [[0.0] * 3 for _ in y], 0.0, bonds)
    return x, v, w, bonds


def chain_force(x):
    f = [[0.0] * 3 for _ in x]
    for i, j in ((0, 2), (1, 3), (0, 3)):
        s = [x[i][a] - x[j][a] for a in range(3)]
        r = math.sqrt(sum(c * c for c in s))
        mag = -3.0 * (r - 1.5)
        for a in range(3):
            f[i][a] += mag * s[a] / r
            f[j][a] -= mag * s[a] / r
    return f


def test_both_constraints_hold_on_every_step() -> None:
    x, v, w, bonds = chain()
    f = chain_force(x)
    for _ in range(400):
        x, v, f = rattle_step(x, v, f, w, chain_force, 0.02, bonds)
        pos, vel = constraint_errors(x, v, bonds)
        assert pos < 1e-12 and vel < 1e-12


def test_reversibility() -> None:
    x0, v0, w, bonds = chain()
    x, v, f = x0, v0, chain_force(x0)
    for _ in range(200):
        x, v, f = rattle_step(x, v, f, w, chain_force, 0.05, bonds)
    v = [[-c for c in p] for p in v]
    for _ in range(200):
        x, v, f = rattle_step(x, v, f, w, chain_force, 0.05, bonds)
    assert max(math.dist(a, b) for a, b in zip(x, x0)) < 1e-9
    assert max(math.dist([-c for c in a], b) for a, b in zip(v, v0)) < 1e-9


def test_map_preserves_phase_area() -> None:
    def flow(theta, omega):
        x, v = pendulum_state(theta, omega)
        f = gravity(x)
        for _ in range(10):
            x, v, f = rattle_step(x, v, f, W_PEND, gravity, 0.1, B_PEND)
        return angle_and_rate(x, v)

    e = 1e-5
    th, om = 0.7, 0.4
    a = [(p - m) / (2 * e) for p, m in zip(flow(th + e, om), flow(th - e, om))]
    b = [(p - m) / (2 * e) for p, m in zip(flow(th, om + e), flow(th, om - e))]
    assert abs(a[0] * b[1] - a[1] * b[0] - 1.0) < 1e-7


def test_energy_error_stays_bounded() -> None:
    x, v = pendulum_state(1.5, 0.0)
    f = gravity(x)
    e0 = 0.5 * sum(c * c for c in v[1]) + x[1][1]
    worst_early = worst_late = 0.0
    for step in range(4000):
        x, v, f = rattle_step(x, v, f, W_PEND, gravity, 0.05, B_PEND)
        err = abs(0.5 * sum(c * c for c in v[1]) + x[1][1] - e0)
        if step < 400:
            worst_early = max(worst_early, err)
        else:
            worst_late = max(worst_late, err)
    assert worst_early < 2e-3
    assert worst_late < 1.2 * worst_early  # no drift over thirty periods


def test_positions_equal_the_shake_positions() -> None:
    x, v, w, bonds = chain()
    f = chain_force(x)
    h = 0.03
    xs = [x]
    for _ in range(30):
        x, v, f = rattle_step(x, v, f, w, chain_force, h, bonds)
        xs.append(x)
    # position Verlet with SHAKE corrections along the bonds at time n, from the same two first positions
    prev, cur = xs[0], xs[1]
    for k in range(2, 31):
        fc = chain_force(cur)
        nxt = [[2 * cur[i][a] - prev[i][a] + h * h * w[i] * fc[i][a] for a in range(3)] for i in range(4)]
        for _ in range(500):
            for i, j, d in bonds:
                s = [nxt[i][a] - nxt[j][a] for a in range(3)]
                r = [cur[i][a] - cur[j][a] for a in range(3)]
                g = (d * d - sum(c * c for c in s)) / (2 * (w[i] + w[j]) * sum(p * q for p, q in zip(s, r)))
                for a in range(3):
                    nxt[i][a] += w[i] * g * r[a]
                    nxt[j][a] -= w[j] * g * r[a]
        assert max(math.dist(p, q) for p, q in zip(nxt, xs[k])) < 1e-10
        prev, cur = cur, nxt
