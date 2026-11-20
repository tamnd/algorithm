# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/coarse-projective-integration/. The authors are listed in prov/6HJ81K.jsonl.
import math
import random

from coarse_projective_integration import (
    amplification,
    coarse_projective_integration,
    euler,
    euler_step,
    projective_forward_euler,
)

H = 5e-4
TH = 0.3
C, S = math.cos(TH), math.sin(TH)
LAM = (-1.0, -1000.0)
A = [
    [C * C * LAM[0] + S * S * LAM[1], C * S * (LAM[0] - LAM[1])],
    [C * S * (LAM[0] - LAM[1]), S * S * LAM[0] + C * C * LAM[1]],
]


def stiff(y):
    return [A[0][0] * y[0] + A[0][1] * y[1], A[1][0] * y[0] + A[1][1] * y[1]]


def stiff_exact(y0, t):
    p = (C * y0[0] + S * y0[1]) * math.exp(LAM[0] * t)
    q = (-S * y0[0] + C * y0[1]) * math.exp(LAM[1] * t)
    return [C * p - S * q, S * p + C * q]


def dist(u, v):
    return math.hypot(u[0] - v[0], u[1] - v[1])


def test_one_outer_step_multiplies_a_mode_by_the_amplification_factor():
    rng = random.Random(3)
    for _ in range(20):
        lam = -rng.uniform(0.1, 3000)
        k, M = rng.randint(0, 10), rng.randint(0, 200)
        y = projective_forward_euler(lambda y: [lam * y[0]], [1.0], H, k, M, 1)
        assert abs(y[0] - amplification(1 + H * lam, k, M)) < 1e-12 * max(1.0, abs(y[0]))


def test_no_projection_is_plain_forward_euler():
    y0 = [1.0, -0.5]
    for k in (0, 3):
        y = projective_forward_euler(stiff, y0, H, k, 0, 7)
        assert dist(y, euler(stiff, y0, H, 7 * (k + 1))) < 1e-14


def test_enough_inner_steps_make_a_long_projective_step_stable():
    y0 = [1.0, 1.0]
    M, n = 100, 10
    T = n * (M + 9) * H
    assert abs(amplification(1 + H * LAM[1], 8, M)) < 0.2
    y = projective_forward_euler(stiff, y0, H, 8, M, n)
    assert dist(y, stiff_exact(y0, T)) < 0.02
    assert abs(amplification(1 + H * LAM[1], 4, M)) > 3
    y = projective_forward_euler(stiff, y0, H, 4, M, n)
    assert math.hypot(*y) > 1e3


def test_the_error_is_first_order_in_the_outer_step():
    y0 = [1.0, 1.0]
    errors = []
    for M, n in ((40, 40), (89, 20), (187, 10)):
        # outer steps 49 h, 98 h and 196 h, all ending at T = 0.98
        y = projective_forward_euler(stiff, y0, H, 8, M, n)
        errors.append(dist(y, stiff_exact(y0, n * (M + 9) * H)))
    assert errors[0] < 0.005
    for e1, e2 in zip(errors, errors[1:]):
        assert 1.8 < e2 / e1 < 2.6


def test_coarse_lifting_errors_heal_during_the_inner_steps():
    lam = 1000.0
    calls = [0]

    def fine(u):
        calls[0] += 1
        return [-u[1], lam * (u[0] - u[1])]

    mu = (-lam + math.sqrt(lam * lam - 4 * lam)) / 2
    ref = math.exp(mu * 0.98)

    def restrict(u):
        return [u[0]]

    errors = []
    for k in (0, 2, 4, 8):
        M = 48 - k
        X = coarse_projective_integration([1.0], lambda X: [X[0], 0.0], euler_step(fine), restrict, H, k, M, 40)
        errors.append(abs(X[0] - ref))
    for e1, e2 in zip(errors, errors[1:]):
        assert e2 < e1 / 2
    calls[0] = 0
    X = coarse_projective_integration([1.0], lambda X: [X[0], X[0]], euler_step(fine), restrict, H, 8, 40, 40)
    assert abs(X[0] - ref) < 0.005
    assert calls[0] == 40 * 9
