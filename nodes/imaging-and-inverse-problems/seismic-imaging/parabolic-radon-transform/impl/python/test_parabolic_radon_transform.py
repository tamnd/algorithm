# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parabolic-radon-transform/. The authors are listed in prov/5J6KMF.jsonl.

import math
import random

import imgla as la
from parabolic_radon_transform import (
    adjoint,
    demultiple,
    forward,
    parabolic_curvature,
    residual_moveout,
)


def ricker(t, f=20.0):
    a = (math.pi * f * t) ** 2
    return (1.0 - 2.0 * a) * math.exp(-a)


def flat(rows):
    return [v for r in rows for v in r]


def rel_err(a, b):
    num = math.sqrt(sum((p - q) ** 2 for p, q in zip(flat(a), flat(b))))
    return num / math.sqrt(sum(q * q for q in flat(b)))


def test_example_numbers():
    assert abs(residual_moveout(1.0, 2000.0, 2500.0, 2000.0) - 0.16619) < 1e-5
    q = parabolic_curvature(1.0, 2500.0, 2000.0)
    assert abs(q - 4.5e-8) < 1e-20
    assert abs(q * 2000.0 ** 2 - 0.18) < 1e-12


def test_integer_shift_is_exact():
    n, dt = 15, 0.004
    x = 200.0
    q = 3 * dt / (x * x)
    rng = random.Random(1)
    tr = [rng.gauss(0.0, 1.0) for _ in range(n)]
    d = forward([tr], [0.0, x], [q], dt)
    assert max(abs(a - b) for a, b in zip(d[0], tr)) < 1e-12
    shifted = [tr[(k - 3) % n] for k in range(n)]
    assert max(abs(a - b) for a, b in zip(d[1], shifted)) < 1e-12


def test_adjoint():
    rng = random.Random(2)
    n, dt = 21, 0.004
    offsets = [0.0, 150.0, 400.0, 700.0, 900.0]
    qs = [-1e-8, 0.0, 2e-8, 5e-8]
    x = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in qs]
    y = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in offsets]
    gap = la.adjoint_gap(lambda v: forward(v, offsets, qs, dt),
                         lambda v: adjoint(v, offsets, qs, dt), x, y)
    assert gap < 1e-12


def test_equals_dense_time_domain_least_squares():
    rng = random.Random(3)
    n, dt, mu = 7, 0.004, 0.3
    offsets = [0.0, 300.0, 600.0]
    qs = [0.0, 1.5e-8]
    d = [[rng.gauss(0.0, 1.0) for _ in range(n)] for _ in offsets]
    cols = []
    for j in range(len(qs)):
        for k in range(n):
            e = [[0.0] * n for _ in qs]
            e[j][k] = 1.0
            cols.append(flat(forward(e, offsets, qs, dt)))
    a = la.transpose(cols)
    at = cols
    normal = la.matmul(at, a)
    for i in range(len(normal)):
        normal[i][i] += mu
    m_dense = la.solve(normal, la.matvec(at, flat(d)))
    m, _, _ = demultiple(d, offsets, qs, dt, mu, q_cut=1.0)
    assert max(abs(p - q) for p, q in zip(flat(m), m_dense)) < 1e-9


def test_removes_a_curved_multiple():
    n, dt = 63, 0.008
    offsets = [100.0 * i for i in range(16)]
    qs = [-1e-8 + 0.5e-8 * j for j in range(14)]
    jp, jm = 2, 10
    model = [[0.0] * n for _ in qs]
    model[jp] = [ricker(k * dt - 0.15) for k in range(n)]
    model[jm] = [-0.7 * ricker(k * dt - 0.2) for k in range(n)]
    d = forward(model, offsets, qs, dt)
    only_primary = [row if j == jp else [0.0] * n for j, row in enumerate(model)]
    p_true = forward(only_primary, offsets, qs, dt)
    m, primaries, multiples = demultiple(d, offsets, qs, dt, 1e-2, 1.2e-8)
    assert rel_err(d, p_true) > 0.69
    assert rel_err(primaries, p_true) < 0.15
    energy = [sum(v * v for v in row) for row in m]
    assert max(range(len(qs)), key=lambda j: energy[j]) in (jp, jm)
    assert energy[jm] > 10 * energy[jm - 4]
