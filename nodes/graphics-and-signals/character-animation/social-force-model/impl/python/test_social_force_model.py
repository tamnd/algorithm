# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/social-force-model/. The authors are listed in prov/4BAJB2.jsonl.
"""Tests of the social force model toy.

Pair forces are antisymmetric, so the interaction forces sum to zero. A
single person relaxes to the desired velocity by the factor (1 - dt / tau)
per step under symplectic Euler. Two groups that walk through each other
keep a minimum gap, which is a measurement of this toy and not a bound.
"""

import math
import random

import social_force_model as sf


def test_pair_forces_are_antisymmetric():
    rng = random.Random(1)
    for _ in range(300):
        xi = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        xj = (rng.uniform(-1, 1), rng.uniform(-1, 1))
        vi = (rng.uniform(-2, 2), rng.uniform(-2, 2))
        vj = (rng.uniform(-2, 2), rng.uniform(-2, 2))
        ri, rj = rng.uniform(0.25, 0.35), rng.uniform(0.25, 0.35)
        a = sf.pair_force(xi, xj, vi, vj, ri, rj)
        b = sf.pair_force(xj, xi, vj, vi, rj, ri)
        s = max(1.0, abs(a[0]), abs(a[1]))
        assert abs(a[0] + b[0]) < 1e-9 * s and abs(a[1] + b[1]) < 1e-9 * s
    # the net interaction force of a group is zero
    X = [(rng.uniform(0, 3), rng.uniform(0, 3)) for _ in range(12)]
    V = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(12)]
    R = [0.3] * 12
    F = sf.forces(X, V, R, X, [0.0] * 12)
    D = [sf.driving_force(x, v, x, 0.0) for x, v in zip(X, V)]
    scale = max(abs(c) for f in F for c in f)
    assert abs(sum(f[0] - d[0] for f, d in zip(F, D))) < 1e-9 * scale
    assert abs(sum(f[1] - d[1] for f, d in zip(F, D))) < 1e-9 * scale


def test_relaxation_to_desired_velocity():
    dt, tau, v0 = 0.01, sf.PARAMS["tau"], 1.3
    # along the goal direction: v_n = v0 + (v_0 - v0) (1 - dt / tau)^n
    X, V = [(0.0, 0.0)], [(0.4, 0.0)]
    goal = [(1000.0, 0.0)]
    for n in range(1, 101):
        X, V = sf.step(X, V, [0.3], goal, [v0], dt)
        c = (1.0 - dt / tau) ** n
        assert abs(V[0][0] - (v0 + (0.4 - v0) * c)) < 1e-12
        assert V[0][1] == 0.0
    # with v0 = 0 any velocity decays by the same factor
    X, V = [(0.0, 0.0)], [(0.7, -0.4)]
    for n in range(1, 101):
        X, V = sf.step(X, V, [0.3], goal, [0.0], dt)
        c = (1.0 - dt / tau) ** n
        assert abs(V[0][0] - 0.7 * c) < 1e-12 and abs(V[0][1] + 0.4 * c) < 1e-12


def test_far_apart_repulsion_is_small():
    f = sf.pair_force((0.0, 0.0), (5.0, 0.0), (0.0, 0.0), (0.0, 0.0), 0.3, 0.3)
    assert abs(f[0]) < 2e3 * math.exp((0.6 - 5.0) / 0.08) * 1.0001 and f[0] < 0
    g = sf.pair_force((0.0, 0.0), (0.5, 0.0), (0.0, 0.0), (0.0, 0.0), 0.3, 0.3)
    assert g[0] < -sf.PARAMS["k"] * 0.1


def test_measured_gap_of_crossing_groups():
    rng = random.Random(4)
    X, goals, R = [], [], []
    for k in range(5):
        y = 0.8 * k + rng.uniform(-0.05, 0.05)
        X.append((0.0, y))
        goals.append((100.0, y))
        X.append((8.0, y + 0.4))
        goals.append((-92.0, y + 0.4))
    R = [rng.uniform(0.25, 0.35) for _ in X]
    V = [(0.0, 0.0)] * len(X)
    v0 = [1.0] * len(X)
    X, V, gap = sf.simulate(X, V, R, goals, v0, dt=0.01, steps=2000)
    # measured on this seed: the groups pass each other in 20 s and the
    # smallest gap between two bodies is about 0.068 m (no overlap)
    assert 0.0 < gap < 0.2
    assert all(x[0] > 8.0 for x in X[0::2]) and all(x[0] < 0.0 for x in X[1::2])
