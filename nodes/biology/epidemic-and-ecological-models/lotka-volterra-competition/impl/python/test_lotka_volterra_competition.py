# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lotka-volterra-competition/. The authors are listed in prov/8SQFG6.jsonl.

import random

from lotka_volterra_competition import (
    eigenvalues,
    field,
    interior_equilibrium,
    jacobian,
    lyapunov,
    outcome,
    rk4,
)


def test_examples_of_the_page() -> None:
    p = (1.0, 1.0, 100.0, 100.0, 0.5, 0.5)
    assert outcome(p) == "coexist"
    e1, e2 = interior_equilibrium(p)
    assert abs(e1 - 200 / 3) < 1e-12 and abs(e2 - 200 / 3) < 1e-12
    ev = sorted(z.real for z in eigenvalues(jacobian(e1, e2, p)))
    assert abs(ev[0] + 1.0) < 1e-12 and abs(ev[1] + 1 / 3) < 1e-12
    n = rk4(5.0, 1.0, 0.05, 4000, p)
    assert abs(n[0] - 200 / 3) < 1e-6 and abs(n[1] - 200 / 3) < 1e-6

    q = (1.0, 1.0, 100.0, 100.0, 1.5, 1.5)
    assert outcome(q) == "bistable"
    e1, e2 = interior_equilibrium(q)
    assert abs(e1 - 40.0) < 1e-12 and abs(e2 - 40.0) < 1e-12
    ev = sorted(z.real for z in eigenvalues(jacobian(e1, e2, q)))
    assert abs(ev[0] + 1.0) < 1e-12 and abs(ev[1] - 0.2) < 1e-12
    a = rk4(45.0, 35.0, 0.05, 4000, q)
    b = rk4(35.0, 45.0, 0.05, 4000, q)
    assert abs(a[0] - 100.0) < 1e-6 and a[1] < 1e-6
    assert abs(b[1] - 100.0) < 1e-6 and b[0] < 1e-6

    s = (1.0, 1.0, 100.0, 80.0, 0.6, 1.5)
    assert outcome(s) == "species 1"
    c = rk4(1.0, 50.0, 0.05, 4000, s)
    assert abs(c[0] - 100.0) < 1e-6 and c[1] < 1e-6


def test_boundary_equilibrium_eigenvalues() -> None:
    # At (K1, 0) the eigenvalues are -r1 and r2 (1 - a21 K1 / K2).
    p = (0.7, 1.3, 100.0, 80.0, 0.6, 1.5)
    ev = sorted(z.real for z in eigenvalues(jacobian(100.0, 0.0, p)))
    assert abs(ev[0] - 1.3 * (1 - 1.5 * 100 / 80)) < 1e-12 and abs(ev[1] + 0.7) < 1e-12


def test_classification_matches_simulation() -> None:
    # Random parameters with seed 3; the outcome rule against RK4 from several starts.
    rng = random.Random(3)
    starts = [(1.0, 1.0), (10.0, 90.0), (90.0, 10.0), (150.0, 150.0)]
    seen = set()
    for _ in range(30):
        p = (rng.uniform(0.5, 2.0), rng.uniform(0.5, 2.0), rng.uniform(50, 150),
             rng.uniform(50, 150), rng.uniform(0.2, 1.8), rng.uniform(0.2, 1.8))
        kind = outcome(p)
        seen.add(kind)
        ends = [rk4(x, y, 0.05, 6000, p) for x, y in starts]
        k1, k2 = p[2], p[3]
        if kind == "coexist":
            e = interior_equilibrium(p)
            assert all(abs(u - e[0]) < 1e-3 and abs(v - e[1]) < 1e-3 for u, v in ends)
        elif kind == "species 1":
            assert all(abs(u - k1) < 1e-3 and v < 1e-3 for u, v in ends)
        elif kind == "species 2":
            assert all(abs(v - k2) < 1e-3 and u < 1e-3 for u, v in ends)
        elif kind == "bistable":
            # Each end is one of the two single-species states.
            assert all((abs(u - k1) < 1e-3 and v < 1e-3) or (abs(v - k2) < 1e-3 and u < 1e-3) for u, v in ends)
    assert {"coexist", "species 1", "species 2", "bistable"} <= seen


def test_lyapunov_function_decreases_in_coexistence() -> None:
    p = (1.0, 0.6, 100.0, 70.0, 0.4, 0.5)
    assert outcome(p) == "coexist"
    x, y = 3.0, 120.0
    v = lyapunov(x, y, p)
    for _ in range(300):
        x, y = rk4(x, y, 0.05, 2, p)
        w = lyapunov(x, y, p)
        assert w <= v + 1e-12
        v = w


def test_field_vanishes_at_equilibria() -> None:
    p = (1.0, 1.0, 100.0, 80.0, 0.6, 0.5)
    e = interior_equilibrium(p)
    for pt in [(0.0, 0.0), (100.0, 0.0), (0.0, 80.0), e]:
        fx, fy = field(pt[0], pt[1], p)
        assert abs(fx) < 1e-12 and abs(fy) < 1e-12
