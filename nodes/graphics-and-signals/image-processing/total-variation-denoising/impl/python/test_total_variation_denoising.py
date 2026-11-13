# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/total-variation-denoising/. The authors are listed in prov/BVXMK0.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from total_variation_denoising import (
    div,
    dual_energy,
    grad,
    rof_energy,
    total_variation,
    tv_denoise,
    tv_denoise_dual,
)


def rand_img(rng, h, w, exact=False):
    if exact:
        return [[F(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(w)] for _ in range(h)]
    return [[float(rng.randint(0, 10)) for _ in range(w)] for _ in range(h)]


def test_page_example():
    f = [[0, 0, 4, 4] for _ in range(4)]
    for lam, a, b in ((0.5, 0.25, 3.75), (1.0, 0.5, 3.5), (2.0, 1.0, 3.0), (5.0, 2.0, 2.0)):
        u = tv_denoise(f, lam, 5000)
        for row in u:
            assert row == pytest.approx([a, a, b, b], abs=1e-6)
    u = tv_denoise(f, 1.0, 5000)
    assert rof_energy(u, f, 1.0) == pytest.approx(14.0, abs=1e-9)


def test_adjoint_and_mean_exact():
    rng = random.Random(3)
    for _ in range(300):
        h, w = rng.randint(1, 5), rng.randint(1, 5)
        u = rand_img(rng, h, w, exact=True)
        px = rand_img(rng, h, w, exact=True)
        py = rand_img(rng, h, w, exact=True)
        gx, gy = grad(u)
        d = div(px, py)
        lhs = sum(a * b for ra, rb in zip(d, u) for a, b in zip(ra, rb))
        rhs = -sum(px[y][x] * gx[y][x] + py[y][x] * gy[y][x] for y in range(h) for x in range(w))
        assert lhs == rhs
        assert sum(map(sum, d)) == 0
        # the bound |div p|^2 <= 8 |p|^2 used for tau <= 1/8
        nd = sum(v * v for r in d for v in r)
        npp = sum(px[y][x] ** 2 + py[y][x] ** 2 for y in range(h) for x in range(w))
        assert nd <= 8 * npp


def test_objective_against_perturbations():
    rng = random.Random(2004)
    for _ in range(500):
        h, w = rng.randint(1, 3), rng.randint(1, 3)
        f = rand_img(rng, h, w)
        lam = rng.uniform(0.1, 3.0)
        u, px, py = tv_denoise_dual(f, lam, 20000, tol=1e-4)
        assert all(math.hypot(px[y][x], py[y][x]) <= 1 + 1e-12 for y in range(h) for x in range(w))
        e = rof_energy(u, f, lam)
        gap = e - dual_energy(px, py, f, lam)
        assert -1e-9 <= gap <= 1e-4
        assert e <= rof_energy(f, f, lam) + 1e-9
        for _ in range(4):
            v = [[u[y][x] + rng.choice((-1, 1)) * rng.uniform(0.05, 0.5) for x in range(w)] for y in range(h)]
            assert e <= rof_energy(v, f, lam)
        # the mean is kept
        assert sum(map(sum, u)) == pytest.approx(sum(map(sum, f)), abs=1e-9)


def test_weak_duality():
    rng = random.Random(8)
    for _ in range(300):
        h, w = rng.randint(1, 4), rng.randint(1, 4)
        f = rand_img(rng, h, w)
        lam = rng.uniform(0.1, 3.0)
        px = [[0.0] * w for _ in range(h)]
        py = [[0.0] * w for _ in range(h)]
        for y in range(h):
            for x in range(w):
                t, r = rng.uniform(0, 2 * math.pi), rng.uniform(0, 1)
                px[y][x], py[y][x] = r * math.cos(t), r * math.sin(t)
        v = rand_img(rng, h, w)
        assert dual_energy(px, py, f, lam) <= rof_energy(v, f, lam) + 1e-9


def test_large_lambda_gives_mean():
    rng = random.Random(1)
    for _ in range(30):
        h, w = rng.randint(1, 4), rng.randint(1, 4)
        f = rand_img(rng, h, w)
        mean = sum(map(sum, f)) / (w * h)
        u = tv_denoise(f, 1000.0, 20000, tol=1e-10)
        for row in u:
            assert row == pytest.approx([mean] * w, abs=1e-3)


def test_edges():
    assert tv_denoise([[3.0]], 1.0, 10) == [[3.0]]
    assert tv_denoise([[2.0, 2.0], [2.0, 2.0]], 1.0, 10) == [[2.0, 2.0], [2.0, 2.0]]
    assert total_variation([[0, 3], [4, 3]]) == pytest.approx(math.hypot(3, 4) + 1.0)
    with pytest.raises(ValueError):
        tv_denoise([[1.0]], 0.0)
    with pytest.raises(ValueError):
        tv_denoise([[1.0]], 1.0, tau=0.2)
    with pytest.raises(ValueError):
        tv_denoise([], 1.0)
