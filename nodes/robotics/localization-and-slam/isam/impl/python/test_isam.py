# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/isam/. The authors are listed in prov/CYW7G6.jsonl.

import math
import random

import pytest

from isam import ISAM, RHS, Factor, squared_error, wrap

OD = [0.05, 0.05, 0.02]
BR = [0.05, 0.02]
STEPS = 12
RANGE = 3.0


def compose(p, u):
    c, s = math.cos(p[2]), math.sin(p[2])
    return [p[0] + c * u[0] - s * u[1], p[1] + s * u[0] + c * u[1], wrap(p[2] + u[2])]


def between(a, b):
    c, s = math.cos(a[2]), math.sin(a[2])
    dx, dy = b[0] - a[0], b[1] - a[1]
    return [c * dx + s * dy, -s * dx + c * dy, wrap(b[2] - a[2])]


def stream(seed, laps=2, noise=True, n_landmarks=6):
    """Per step t: (odometry from t - 1 or None, [(landmark, range and bearing)]).

    The robot drives laps of a 12-sided polygon with sides of 1 m.
    """
    rng = random.Random(seed)
    radius = 0.5 / math.sin(math.pi / STEPS)
    marks = []
    for j in range(n_landmarks):
        a = 2.0 * math.pi * j / n_landmarks + rng.uniform(-0.3, 0.3)
        d = radius + rng.uniform(-1.2, 1.2)
        marks.append([d * math.cos(a), radius + d * math.sin(a)])
    u = [1.0, 0.0, 2.0 * math.pi / STEPS]
    truth = [[0.0, 0.0, 0.0]]
    steps = []
    for t in range(laps * STEPS + 1):
        odo = None
        if t > 0:
            truth.append(compose(truth[-1], u))
            odo = between(truth[t - 1], truth[t])
            if noise:
                odo = [odo[0] + rng.gauss(0, OD[0]), odo[1] + rng.gauss(0, OD[1]), wrap(odo[2] + rng.gauss(0, OD[2]))]
        seen = []
        x = truth[t]
        for j, m in enumerate(marks):
            dx, dy = m[0] - x[0], m[1] - x[1]
            r = math.hypot(dx, dy)
            if r <= RANGE:
                z = [r, wrap(math.atan2(dy, dx) - x[2])]
                if noise:
                    z = [z[0] + rng.gauss(0, BR[0]), wrap(z[1] + rng.gauss(0, BR[1]))]
                seen.append((j, z))
        steps.append((odo, seen))
    truth_map = {("x", t): p for t, p in enumerate(truth)}
    truth_map.update({("l", j): m for j, m in enumerate(marks)})
    return steps, truth_map


def new_values_and_factors(t, step, est):
    """Build the factors of step t and initial values from the current estimate est."""
    odo, seen = step
    if odo is None:
        pose = [0.0, 0.0, 0.0]
        factors = [Factor("prior", [("x", 0)], pose, [1e-3, 1e-3, 1e-3])]
    else:
        pose = compose(est[("x", t - 1)], odo)
        factors = [Factor("odometry", [("x", t - 1), ("x", t)], odo, OD)]
    values = {("x", t): pose}
    for j, z in seen:
        factors.append(Factor("bearing_range", [("x", t), ("l", j)], z, BR))
        if ("l", j) not in est and ("l", j) not in values:
            values[("l", j)] = [pose[0] + z[0] * math.cos(pose[2] + z[1]), pose[1] + z[0] * math.sin(pose[2] + z[1])]
    return values, factors


def run(isam, steps, check=None):
    est = {}
    for t, step in enumerate(steps):
        values, factors = new_values_and_factors(t, step, est)
        est = isam.update(values, factors)
        if check:
            check(t, isam)
    return est


def dense_check(isam, tol=1e-7):
    """R^T R = A^T A, R^T d = A^T b, and delta solves the normal equations."""
    n = isam.n
    rows = isam.rows(isam.factors)
    ata = [[0.0] * n for _ in range(n)]
    atb = [0.0] * n
    for row in rows:
        items = [(c, x) for c, x in row.items() if c != RHS]
        for c1, x1 in items:
            atb[c1] += x1 * row[RHS]
            for c2, x2 in items:
                ata[c1][c2] += x1 * x2
    rtr = [[0.0] * n for _ in range(n)]
    rtd = [0.0] * n
    for c, row in isam.r.items():
        assert all(j == RHS or j >= c for j in row)  # upper triangular
        items = [(j, x) for j, x in row.items() if j != RHS]
        for c1, x1 in items:
            rtd[c1] += x1 * row.get(RHS, 0.0)
            for c2, x2 in items:
                rtr[c1][c2] += x1 * x2
    scale = max(abs(x) for r in ata for x in r)
    assert max(abs(a - b) for r1, r2 in zip(ata, rtr) for a, b in zip(r1, r2)) < tol * scale
    assert max(abs(a - b) for a, b in zip(atb, rtd)) < tol * scale
    res = [sum(ata[i][j] * isam.delta[j] for j in range(n)) - atb[i] for i in range(n)]
    assert max(abs(x) for x in res) < tol * scale


def batch_optimum(factors, start, iters=3):
    """Gauss-Newton on all factors from start, by batch steps of a fresh solver."""
    values = dict(start)
    for _ in range(iters):
        values = ISAM(k=1).update(values, factors)
    return values


def test_factor_matches_the_normal_equations_after_every_update_without_batch_steps():
    steps, _ = stream(1)
    isam = ISAM(k=10 ** 9)
    run(isam, steps, lambda t, s: dense_check(s) if t % 6 == 0 or t == len(steps) - 1 else None)
    assert isam.batch_steps == 0


def test_factor_matches_the_normal_equations_across_batch_steps():
    steps, _ = stream(2)
    isam = ISAM(k=4)
    run(isam, steps, lambda t, s: dense_check(s) if t % 5 == 0 or t == len(steps) - 1 else None)
    assert isam.batch_steps == len(steps) // 4


def test_noise_free_stream_gives_the_true_map_and_path():
    steps, truth = stream(3, noise=False)
    est = run(ISAM(k=7), steps)
    for key, x in truth.items():
        assert max(abs(wrap(a - b)) for a, b in zip(est[key], x)) < 1e-9


def test_estimate_is_close_to_the_batch_optimum():
    steps, _ = stream(4)
    isam = ISAM(k=5)
    est = run(isam, steps)
    ref = batch_optimum(isam.factors, est)
    c_isam, c_ref = squared_error(isam.factors, est), squared_error(isam.factors, ref)
    assert c_ref <= c_isam < 1.2 * c_ref


def test_reordering_keeps_the_factor_sparse():
    steps, _ = stream(4)
    plain, reordered = ISAM(k=10 ** 9), ISAM(k=5)
    g_plain, g_reordered = [], []
    run(plain, steps, lambda t, s: g_plain.append(s.last_givens))
    run(reordered, steps, lambda t, s: g_reordered.append(s.last_givens))
    assert reordered.nnz() < plain.nnz()
    # updates right after a batch step need fewer rotations than without reordering
    for t in (20, 21, 22, 23):
        assert g_reordered[t] < g_plain[t]


def test_an_unconstrained_variable_is_an_error():
    isam = ISAM()
    with pytest.raises(ValueError):
        isam.update({("x", 0): [0.0, 0.0, 0.0]}, [])
