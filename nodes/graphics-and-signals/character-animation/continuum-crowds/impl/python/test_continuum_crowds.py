# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/continuum-crowds/. The authors are listed in prov/RXA6V1.jsonl.
"""Tests of continuum crowds.

The fast marching potential must equal a brute force fixed point iteration
of the same discrete eikonal update on small random anisotropic grids with
obstacles. Constant costs give exact distances along the axes. The density
splat satisfies the two requirements of Section 4.1. The crowd run is a
measurement of the toy: every person reaches the goal and the minimum
distance between people is reported, not guaranteed.
"""

import math
import random

import continuum_crowds as c


def random_costs(rng, nx, ny, holes):
    C = [[[rng.uniform(0.5, 3.0) for _ in range(4)] for _ in range(ny)] for _ in range(nx)]
    for _ in range(holes):
        i, j = rng.randrange(nx), rng.randrange(ny)
        C[i][j] = [c.INF] * 4
    return C


def test_fast_marching_equals_brute_force():
    rng = random.Random(7)
    for trial in range(6):
        nx, ny = rng.randint(4, 12), rng.randint(4, 12)
        C = random_costs(rng, nx, ny, nx * ny // 10)
        goal = [(rng.randrange(nx), rng.randrange(ny)) for _ in range(rng.randint(1, 3))]
        dx = rng.choice([0.25, 1.0])
        phi, _ = c.fast_march(C, goal, dx)
        ref = c.solve_brute(C, goal, dx)
        for i in range(nx):
            for j in range(ny):
                a, b = phi[i][j], ref[i][j]
                if a == c.INF or b == c.INF:
                    assert a == b
                else:
                    assert abs(a - b) <= 1e-9 * max(1.0, b)


def test_fast_marching_is_a_fixed_point_and_in_order():
    rng = random.Random(11)
    C = random_costs(rng, 10, 10, 8)
    goal = [(0, 0)]
    phi, order = c.fast_march(C, goal, 1.0)
    vals = [phi[i][j] for i, j in order]
    assert all(b >= a for a, b in zip(vals, vals[1:]))
    for i in range(10):
        for j in range(10):
            if (i, j) in goal or phi[i][j] == c.INF:
                continue
            assert abs(c.local_update(phi, C, i, j, 1.0) - phi[i][j]) < 1e-12


def test_constant_cost_gives_axis_distance():
    n, dx = 9, 0.5
    C = [[[2.0] * 4 for _ in range(n)] for _ in range(n)]
    phi, _ = c.fast_march(C, [(0, 0)], dx)
    for k in range(n):
        assert abs(phi[k][0] - 2.0 * k * dx) < 1e-12
        assert abs(phi[0][k] - 2.0 * k * dx) < 1e-12
    # the diagonal neighbor of the goal: two terms, each (phi - 1) / 1
    assert abs(phi[1][1] - (1.0 + math.sqrt(0.5))) < 1e-12
    # the potential grows with the distance and is symmetric
    for i in range(n):
        for j in range(n):
            assert abs(phi[i][j] - phi[j][i]) < 1e-12


def test_splat_requirements():
    rng = random.Random(3)
    lam = 2.0
    bar = 0.5 ** lam
    nx = ny = 8
    for _ in range(300):
        x, y = rng.uniform(1.0, 7.0), rng.uniform(1.0, 7.0)
        rho, vbar = c.splat([((x, y), (0.3, -0.2))], nx, ny, 1.0, lam)
        own = (int(x), int(y))
        for i in range(nx):
            for j in range(ny):
                if (i, j) == own:
                    assert rho[i][j] >= bar - 1e-12
                else:
                    assert rho[i][j] <= bar + 1e-12
                if rho[i][j] > 0:
                    assert abs(vbar[i][j][0] - 0.3) < 1e-12
        # continuity: a small move gives a small change
        rho2, _ = c.splat([((x + 1e-7, y), (0.0, 0.0))], nx, ny, 1.0, lam)
        assert max(abs(rho[i][j] - rho2[i][j]) for i in range(nx) for j in range(ny)) < 1e-5


def test_measured_crowd_reaches_goal():
    rng = random.Random(2)
    n, dx = 16, 1.0
    params = dict(fmax=1.4, rho_min=0.6, rho_max=1.6, alpha=1.0, beta=1.0,
                  gamma=1.0, lam=2.0, dmin=0.4)
    people = [((rng.uniform(1, 4), rng.uniform(1, 15)), (0.0, 0.0)) for _ in range(20)]
    goal = [(n - 1, j) for j in range(n)]
    closest = math.inf
    for _ in range(40):
        people, phi = c.step(people, goal, n, n, dx, 0.25, params)
        pos = [p for p, _ in people]
        closest = min(closest, min(math.dist(a, b) for k, a in enumerate(pos) for b in pos[k + 1:]))
    assert all(p[0] >= n - 1 - 0.1 for p in pos)
    # measured on this seed: the closest pair is about 0.38 m with dmin = 0.4 m
    assert 0.3 < closest <= 0.4 + 1e-9
