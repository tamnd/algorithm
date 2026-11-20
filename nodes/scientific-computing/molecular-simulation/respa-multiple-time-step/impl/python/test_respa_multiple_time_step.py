# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/respa-multiple-time-step/. The authors are listed in prov/2SQEWG.jsonl.

import math
import random

from respa_multiple_time_step import respa_step, velocity_verlet_step

OMEGA = 10.0  # frequency of the fast spring


def fast(x):
    return [-OMEGA * OMEGA * c for c in x]


def slow(x):
    return [-math.sin(c) for c in x]


def energy(x, v):
    return sum(0.5 * b * b + 0.5 * OMEGA * OMEGA * a * a + 1 - math.cos(a) for a, b in zip(x, v))


def test_one_inner_step_is_velocity_verlet() -> None:
    rng = random.Random(1)
    x = [rng.uniform(-1, 1) for _ in range(3)]
    v = [rng.uniform(-1, 1) for _ in range(3)]
    w = [1.0, 0.5, 2.0]
    a, b = list(x), list(v)
    for _ in range(50):
        x, v = respa_step(x, v, w, fast, slow, 0.03, 1)
        a, b = velocity_verlet_step(a, b, w, lambda y: [p + q for p, q in zip(fast(y), slow(y))], 0.03)
    assert max(abs(p - q) for p, q in zip(x + v, a + b)) < 1e-12


def test_without_slow_force_it_is_verlet_with_the_small_step() -> None:
    x, v, w = [0.4], [0.1], [1.0]
    a, b = list(x), list(v)
    for _ in range(20):
        x, v = respa_step(x, v, w, fast, lambda y: [0.0], 0.1, 5)
        for _ in range(5):
            a, b = velocity_verlet_step(a, b, w, fast, 0.02)
    assert abs(x[0] - a[0]) < 1e-12 and abs(v[0] - b[0]) < 1e-12


def test_reversibility() -> None:
    x0, v0, w = [0.3, -0.7], [0.5, 0.2], [1.0, 1.0]
    x, v = x0, v0
    for _ in range(100):
        x, v = respa_step(x, v, w, fast, slow, 0.1, 8)
    v = [-c for c in v]
    for _ in range(100):
        x, v = respa_step(x, v, w, fast, slow, 0.1, 8)
    assert max(abs(p - q) for p, q in zip(x, x0)) < 1e-10
    assert max(abs(-p - q) for p, q in zip(v, v0)) < 1e-10


def test_map_preserves_phase_area() -> None:
    def flow(x, v):
        a, b = [x], [v]
        for _ in range(7):
            a, b = respa_step(a, b, [1.0], fast, slow, 0.1, 4)
        return a[0], b[0]

    e = 1e-6
    dx = [(p - m) / (2 * e) for p, m in zip(flow(0.5 + e, 0.2), flow(0.5 - e, 0.2))]
    dv = [(p - m) / (2 * e) for p, m in zip(flow(0.5, 0.2 + e), flow(0.5, 0.2 - e))]
    assert abs(dx[0] * dv[1] - dx[1] * dv[0] - 1.0) < 1e-6


def max_energy_error(h: float, n: int, t_end: float) -> float:
    x, v = [1.0], [0.0]
    e0 = energy(x, v)
    worst = 0.0
    for _ in range(int(round(t_end / h))):
        x, v = respa_step(x, v, [1.0], fast, slow, h, n)
        worst = max(worst, abs(energy(x, v) - e0))
    return worst


def test_energy_error_is_second_order() -> None:
    e1 = max_energy_error(0.1, 10, 20.0)
    e2 = max_energy_error(0.05, 10, 20.0)
    assert e1 < 0.05 * energy([1.0], [0.0])
    assert 3.0 < e1 / e2 < 5.0


def trace_of_linear_map(h: float, kappa: float, n: int) -> float:
    def step(x, v):
        a, b = respa_step([x], [v], [1.0], fast, lambda y: [-kappa * y[0]], h, n)
        return a[0], b[0]

    return step(1.0, 0.0)[0] + step(0.0, 1.0)[1]


def test_resonance_near_half_the_fast_period() -> None:
    kappa, n = 1.0, 200
    # with the inner motion integrated almost exactly, the trace is 2 cos(Omega h) - kappa h sin(Omega h) / Omega
    for h in (0.1, 0.25):
        exact = 2 * math.cos(OMEGA * h) - kappa * h * math.sin(OMEGA * h) / OMEGA
        assert abs(trace_of_linear_map(h, kappa, n) - exact) < 1e-3
        assert abs(trace_of_linear_map(h, kappa, n)) < 2.0
    h_bad = (math.pi - 0.015) / OMEGA
    assert abs(trace_of_linear_map(h_bad, kappa, n)) > 2.0
    # the same total force with a small enough step is stable
    assert abs(trace_of_linear_map(h_bad / 3, kappa, n)) < 2.0
    # an unstable map makes the amplitude grow without bound
    x, v = [1.0], [0.0]
    for _ in range(3000):
        x, v = respa_step(x, v, [1.0], fast, lambda y: [-kappa * y[0]], h_bad, 20)
    assert abs(x[0]) + abs(v[0]) / OMEGA > 10.0
