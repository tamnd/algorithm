# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/inverse-compositional-alignment/. The authors are listed in prov/ZVVMQX.jsonl.

import math
import random

import pytest

from cvla import inv
from inverse_compositional_alignment import (
    compose_inverse,
    fa_align,
    ic_align,
    params,
    precompute,
    sample,
    warp,
    warp_jacobian,
    warp_matrix,
)

N = 40
REGION = [(u, v) for v in range(10, 31) for u in range(10, 31)]
TRUE_P = [0.05, -0.03, 0.02, -0.04, 1.5, -1.0]


def texture():
    rng = random.Random(5)
    blobs = [(rng.uniform(5, 35), rng.uniform(5, 35), rng.uniform(2.5, 4.5), rng.uniform(50, 150))
             for _ in range(12)]

    def f(u, v):
        return sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / (2 * s * s)) for x, y, s, a in blobs)

    return f


def affine_pair(p):
    """Template T = f on the grid, and image I with I(W(x; p)) = T(x)."""
    f = texture()
    t = [[f(u, v) for u in range(N)] for v in range(N)]
    q = params(inv(warp_matrix(p)))
    img = [[f(*warp(q, u, v)) for u in range(N)] for v in range(N)]
    return t, img


def point_error(p, q):
    return max(math.dist(warp(p, u, v), warp(q, u, v)) for u, v in REGION)


def test_warp_jacobian_matches_finite_differences():
    rng = random.Random(1)
    p = [rng.uniform(-0.1, 0.1) for _ in range(6)]
    h = 1e-6
    for u, v in [(0, 0), (3, -2), (12.5, 7.25)]:
        jac = warp_jacobian(u, v)
        for i in range(6):
            pp, pm = list(p), list(p)
            pp[i] += h
            pm[i] -= h
            a, b = warp(pp, u, v), warp(pm, u, v)
            assert abs((a[0] - b[0]) / (2 * h) - jac[0][i]) < 1e-6
            assert abs((a[1] - b[1]) / (2 * h) - jac[1][i]) < 1e-6


def test_compose_inverse_undoes_the_increment():
    rng = random.Random(2)
    for _ in range(5):
        p = [rng.uniform(-0.2, 0.2) for _ in range(6)]
        dp = [rng.uniform(-0.2, 0.2) for _ in range(6)]
        r = compose_inverse(p, dp)
        for u, v in [(0, 0), (5, 9), (-3, 4)]:
            a = warp(r, *warp(dp, u, v))
            b = warp(p, u, v)
            assert math.dist(a, b) < 1e-12


def test_steepest_descent_images_by_the_chain_rule():
    ramp = [[2.0 * u + 3.0 * v + 1.0 for u in range(N)] for v in range(N)]
    region = [(u, v) for v in range(5, 9) for u in range(5, 9)]
    sd, hess = precompute(ramp, region)
    h = 1e-4
    for (u, v), s in zip(region, sd):
        for i in range(6):
            dp = [0.0] * 6
            dp[i] = h
            num = (sample(ramp, *warp(dp, u, v)) - sample(ramp, u, v)) / h
            assert abs(num - s[i]) < 1e-6
    for i in range(6):
        for j in range(6):
            assert abs(hess[i][j] - sum(s[i] * s[j] for s in sd)) < 1e-9
            assert hess[i][j] == hess[j][i]


def test_integer_translation_is_recovered_exactly():
    f = texture()
    t = [[f(u, v) for u in range(N)] for v in range(N)]
    img = [[f(u - 3, v + 2) for u in range(N)] for v in range(N)]
    p, costs = ic_align(t, REGION, img)
    assert max(abs(a - b) for a, b in zip(p, [0, 0, 0, 0, 3, -2])) < 1e-8
    assert costs[-1] < 1e-12


def test_affine_warp_is_recovered():
    t, img = affine_pair(TRUE_P)
    p, costs = ic_align(t, REGION, img)
    assert point_error(p, TRUE_P) < 0.1
    # the cost drops at every step until it reaches the floor set by interpolation
    final = costs[-1]
    for a, b in zip(costs, costs[1:]):
        if a > 1.05 * final:
            assert b < a
    assert costs[0] > 1000 * final


def test_agrees_with_forwards_additive():
    t, img = affine_pair(TRUE_P)
    p, _ = ic_align(t, REGION, img)
    q = fa_align(t, REGION, img)
    assert point_error(p, q) < 0.02


def test_flat_template_has_a_singular_hessian():
    flat = [[5.0] * N for _ in range(N)]
    with pytest.raises(ValueError):
        ic_align(flat, REGION, flat)
