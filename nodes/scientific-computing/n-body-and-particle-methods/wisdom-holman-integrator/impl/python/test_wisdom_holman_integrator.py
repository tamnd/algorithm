# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/wisdom-holman-integrator/. The authors are listed in prov/JQMB4C.jsonl.
import math
import random

import pytest

from wisdom_holman_integrator import (accelerations, energy, from_jacobi, integrate, kepler_drift,
                                      to_jacobi, wh_step)

P = 2 * math.pi


def planets(eps):
    """A star and two planets of masses eps and 0.3 eps, near circular orbits at radii 1 and 1.6."""
    m = [1.0, eps, 0.3 * eps]
    x = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.6, 0.05]]
    v = [[0.0, 0.0, 0.0], [0.0, 1.0, 0.02], [-1 / math.sqrt(1.6), 0.0, 0.0]]
    return m, x, v


def rk4_kepler(x, v, mu, dt, n):
    s = list(x) + list(v)

    def f(s):
        r = math.sqrt(sum(c * c for c in s[:3]))
        return s[3:] + [-mu * c / r ** 3 for c in s[:3]]

    for _ in range(n):
        k1 = f(s)
        k2 = f([s[i] + dt / 2 * k1[i] for i in range(6)])
        k3 = f([s[i] + dt / 2 * k2[i] for i in range(6)])
        k4 = f([s[i] + dt * k3[i] for i in range(6)])
        s = [s[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(6)]
    return s[:3], s[3:]


def rk4_nbody(m, x, v, dt, n):
    """Classical Runge-Kutta in Cartesian coordinates, the independent reference."""
    nb = len(m)

    def axpy(y, c, z):
        return [[y[i][k] + c * z[i][k] for k in range(3)] for i in range(nb)]

    for _ in range(n):
        a1 = accelerations(m, x)
        x2, v2 = axpy(x, dt / 2, v), axpy(v, dt / 2, a1)
        a2 = accelerations(m, x2)
        x3, v3 = axpy(x, dt / 2, v2), axpy(v, dt / 2, a2)
        a3 = accelerations(m, x3)
        x4, v4 = axpy(x, dt, v3), axpy(v, dt, a3)
        a4 = accelerations(m, x4)
        x = [[x[i][k] + dt / 6 * (v[i][k] + 2 * v2[i][k] + 2 * v3[i][k] + v4[i][k]) for k in range(3)]
             for i in range(nb)]
        v = [[v[i][k] + dt / 6 * (a1[i][k] + 2 * a2[i][k] + 2 * a3[i][k] + a4[i][k]) for k in range(3)]
             for i in range(nb)]
    return x, v


def test_jacobi_round_trip():
    rng = random.Random(1)
    m = [rng.uniform(0.1, 2.0) for _ in range(6)]
    x = [[rng.uniform(-1, 1) for _ in range(3)] for _ in range(6)]
    back = from_jacobi(m, to_jacobi(m, x))
    for p, q in zip(back, x):
        assert p == pytest.approx(q, abs=1e-14)
    # entry 0 is the center of mass
    com = [sum(m[i] * x[i][k] for i in range(6)) / sum(m) for k in range(3)]
    assert to_jacobi(m, x)[0] == pytest.approx(com, abs=1e-14)


def test_kepler_drift_circular_quarter_turn():
    x1, v1 = kepler_drift([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], 1.0, P / 4)
    assert x1 == pytest.approx([0.0, 1.0, 0.0], abs=1e-13)
    assert v1 == pytest.approx([-1.0, 0.0, 0.0], abs=1e-13)


def test_kepler_drift_against_runge_kutta():
    rng = random.Random(3)
    for _ in range(3):
        x = [rng.uniform(-1.5, 1.5) for _ in range(3)]
        r = math.sqrt(sum(c * c for c in x))
        speed = rng.uniform(0.5, 0.9) * math.sqrt(2 / r)  # bound orbit
        d = [rng.gauss(0, 1) for _ in range(3)]
        nd = math.sqrt(sum(c * c for c in d))
        v = [speed * c / nd for c in d]
        dt = rng.uniform(0.5, 4.0)
        xk, vk = kepler_drift(x, v, 1.0, dt)
        xr, vr = rk4_kepler(x, v, 1.0, dt / 6000, 6000)
        assert math.dist(xk, xr) < 1e-7
        assert math.dist(vk, vr) < 1e-7


def test_one_planet_is_exact_for_any_step():
    m = [1.0, 1e-3]
    x = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    v = [[0.0, 0.0, 0.0], [0.0, 1.1, 0.0]]
    xa, _ = integrate(m, x, v, 0.9, 7)
    xj, vj = to_jacobi(m, x), to_jacobi(m, v)
    xe, _ = kepler_drift(xj[1], vj[1], 1.001, 6.3)
    exact = from_jacobi(m, [[xj[0][k] + 6.3 * vj[0][k] for k in range(3)], xe])
    for p, q in zip(xa, exact):
        assert math.dist(p, q) < 1e-12


def test_time_reversible():
    m, x, v = planets(1e-3)
    x1, v1 = integrate(m, x, v, P / 40, 300)
    x2, v2 = integrate(m, x1, [[-c for c in q] for q in v1], P / 40, 300)
    for p, q in zip(x2, x):
        assert math.dist(p, q) < 1e-9
    for p, q in zip(v2, v):
        assert math.dist([-c for c in p], q) < 1e-9


def test_bounded_energy_error_and_momentum():
    m, x, v = planets(1e-3)
    e0 = energy(m, x, v)
    p0 = [sum(m[i] * v[i][k] for i in range(3)) for k in range(3)]
    errs = []
    for _ in range(2000):
        x, v = wh_step(m, x, v, P / 40)
        errs.append(abs(energy(m, x, v) - e0) / abs(e0))
    assert max(errs) < 5e-6
    assert max(errs[1000:]) < 1.2 * max(errs[:1000])  # no drift
    for k in range(3):
        assert sum(m[i] * v[i][k] for i in range(3)) == pytest.approx(p0[k], abs=1e-15)


def test_second_order_against_runge_kutta_reference():
    m, x, v = planets(1e-3)
    ref, _ = rk4_nbody(m, x, v, P / 6000, 6000)
    errs = []
    for steps in (20, 40):
        xw, _ = integrate(m, x, v, P / steps, steps)
        errs.append(max(math.dist(p, q) for p, q in zip(xw, ref)))
    assert errs[1] < 1e-5
    assert 3.5 < errs[0] / errs[1] < 4.5  # 2^2 = 4
