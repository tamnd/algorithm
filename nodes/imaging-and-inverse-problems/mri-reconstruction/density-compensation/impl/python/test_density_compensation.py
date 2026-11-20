# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/density-compensation/. The authors are listed in prov/4CW95Q.jsonl.

import math
import random

import pytest

from density_compensation import (
    bessel_i0,
    kaiser_bessel,
    kernel_matrix,
    neighbours,
    pipe_menon,
    radial_points,
    residual,
    triangle,
)
from imgla import matvec, solve


def test_bessel_i0_values():
    # I0(0) = 1; I0(1) = 1.2660658777520082; I0(x) e^(-x) sqrt(2 pi x) -> 1 for large x.
    assert bessel_i0(0.0) == 1.0
    assert bessel_i0(1.0) == pytest.approx(1.2660658777520082, rel=1e-14)
    assert bessel_i0(6.0) == pytest.approx(67.23440697647797, rel=1e-13)


def test_neighbour_lists_match_dense_matrix():
    rng = random.Random(11)
    pts = [(rng.uniform(0, 6), rng.uniform(0, 6)) for _ in range(30)]
    kb = kaiser_bessel(3.0, 6.0)
    nb = neighbours(pts, kb, 3.0)
    dense = kernel_matrix(pts, kb)
    for i in range(len(pts)):
        row = [0.0] * len(pts)
        for j, c in nb[i]:
            row[j] = c
        assert max(abs(a - b) for a, b in zip(row, dense[i])) < 1e-15


def test_weights_stay_positive():
    rng = random.Random(12)
    pts = [(rng.uniform(0, 10),) for _ in range(25)]
    kb = kaiser_bessel(4.0, 8.0)
    for k in (0, 1, 5, 40):
        assert min(pipe_menon(pts, kb, 4.0, k)) > 0.0


def test_matches_direct_solve_when_positive_solution_exists():
    # Jittered samples with a wide triangle kernel: C w = 1 has a positive solution.
    rng = random.Random(13)
    pts = [(i + rng.uniform(-0.15, 0.15),) for i in range(40)]
    tri = triangle(3.0)
    ref = solve(kernel_matrix(pts, tri), [1.0] * len(pts))
    assert min(ref) > 0.0
    w = pipe_menon(pts, tri, 3.0, 300)
    assert max(abs(a - b) for a, b in zip(w, ref)) < 1e-6
    assert residual(pts, tri, w) < 1e-6


def test_positive_solution_is_a_fixed_point():
    rng = random.Random(14)
    pts = [(i + rng.uniform(-0.15, 0.15),) for i in range(30)]
    tri = triangle(3.0)
    c = kernel_matrix(pts, tri)
    ref = solve(c, [1.0] * len(pts))
    d = matvec(c, ref)
    nxt = [wi / di for wi, di in zip(ref, d)]
    assert max(abs(a - b) for a, b in zip(nxt, ref)) < 1e-12


def test_kernel_scaling_divides_weights():
    rng = random.Random(15)
    pts = [(rng.uniform(0, 8), rng.uniform(0, 8)) for _ in range(40)]
    kb = kaiser_bessel(3.0, 6.0)

    def kb3(r):
        return 3.0 * kb(r)

    a = pipe_menon(pts, kb, 3.0, 10)
    b = pipe_menon(pts, kb3, 3.0, 10)
    assert max(abs(x - 3.0 * y) for x, y in zip(a, b)) < 1e-12


def test_duplicate_sample_splits_its_weight():
    rng = random.Random(16)
    pts = [(i + rng.uniform(-0.15, 0.15),) for i in range(20)]
    tri = triangle(3.0)
    w = pipe_menon(pts, tri, 3.0, 300)
    dup = pts[:10] + [pts[10], pts[10]] + pts[11:]
    wd = pipe_menon(dup, tri, 3.0, 300)
    assert wd[10] == pytest.approx(wd[11], rel=1e-12)
    assert wd[10] + wd[11] == pytest.approx(w[10], rel=1e-6)
    assert max(abs(a - b) for a, b in zip(wd[:10], w[:10])) < 1e-6


def test_radial_weights_follow_the_ramp():
    spokes, samples, kmax = 16, 16, 8.0
    pts = radial_points(spokes, samples, kmax)
    kb = kaiser_bessel(3.0, 6.0)
    w = pipe_menon(pts, kb, 3.0, 50)
    assert residual(pts, kb, w) < 1e-10
    # Expected ramp: w(r) ~ 2 pi r delta / (2 spokes integral of C), delta the step along a spoke.
    steps = 3000
    h = 1.5 / steps
    area = 2.0 * math.pi * h * sum((i + 0.5) * h * kb((i + 0.5) * h) for i in range(steps))
    slope = 2.0 * math.pi * (2.0 * kmax / samples) / (2 * spokes * area)
    for q in range(samples // 2 + 1, samples - 2):
        r = math.hypot(*pts[q])
        assert w[q] == pytest.approx(slope * r, rel=0.06)
    # Every spoke gets the same weights by symmetry.
    for s in range(1, spokes):
        assert max(abs(w[s * samples + q] - w[q]) for q in range(samples)) < 1e-9


def test_rejects_kernel_zero_at_origin():
    with pytest.raises(ValueError):
        pipe_menon([(0.0,)], lambda r: 0.0, 1.0)
