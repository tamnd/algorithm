# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-matching-coarse-graining/. The authors are listed in prov/3CW63P.jsonl.
import math
import random

import pytest

from force_matching_coarse_graining import (HatBasis, cg_forces, chi2, design_rows, force_matching,
                                            minimum_image)

BOX = 6.0
RC = 2.5
R0 = 0.85


def configs(seed, count, n=20, box=BOX, dmin=R0):
    """Random configurations of n sites with no pair closer than dmin."""
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        x = []
        while len(x) < n:
            p = (rng.uniform(0.0, box), rng.uniform(0.0, box))
            if all(math.hypot(minimum_image(p[0] - q[0], box), minimum_image(p[1] - q[1], box)) >= dmin for q in x):
                x.append(p)
        out.append(x)
    return out


def smooth_force(r):
    return 3.0 * math.cos(3.0 * r) * (RC - r)


def pair_forces(x, f, box=BOX, rc=RC):
    """Brute force: the forces of the pair force f(r) for r <= rc."""
    n = len(x)
    out = [0.0] * (2 * n)
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = minimum_image(x[i][0] - x[j][0], box)
                dy = minimum_image(x[i][1] - x[j][1], box)
                r = math.hypot(dx, dy)
                if r <= rc:
                    out[2 * i] += f(r) * dx / r
                    out[2 * i + 1] += f(r) * dy / r
    return out


def test_hat_basis_is_a_partition_of_unity_and_integrates_exactly():
    b = HatBasis(1.0, 2.0, 5)
    for k in range(101):
        r = 1.0 + k / 100
        assert sum(v for _, v in b.values(r)) == pytest.approx(1.0, abs=1e-14)
    assert b.values(0.99) == [] and b.values(2.01) == []
    c = [2.0 * r - 1.0 for r in b.nodes]  # f(r) = 2 r - 1, V(r) = (rc^2 - r^2) - (rc - r)
    for r in (1.0, 1.1, 1.5, 1.99, 2.0):
        assert b.force(c, r) == pytest.approx(2.0 * r - 1.0, abs=1e-14)
        assert b.potential(c, r) == pytest.approx((4.0 - r * r) - (2.0 - r), abs=1e-14)


def test_small_example_by_hand():
    b = HatBasis(1.0, 2.0, 2)
    data = [(1.25, 1.0), (1.75, 0.2), (1.5, 0.5)]
    xs = [[(r, 0.0), (0.0, 0.0)] for r, _ in data]
    fs = [[f, 0.0, -f, 0.0] for _, f in data]
    c = force_matching(xs, fs, 10.0, b)
    assert c[0] == pytest.approx(41 / 30, abs=1e-12)
    assert c[1] == pytest.approx(-7 / 30, abs=1e-12)
    assert chi2(xs, fs, 10.0, b, c) == pytest.approx(2 * 6 / 900, abs=1e-12)
    assert b.potential(c, 1.0) == pytest.approx(17 / 30, abs=1e-12)


def test_design_rows_match_brute_force_forces():
    b = HatBasis(R0, RC, 11)
    rng = random.Random(4)
    c = [rng.uniform(-2.0, 2.0) for _ in range(b.k)]
    for x in configs(5, 3):
        assert cg_forces(x, BOX, b, c) == pytest.approx(pair_forces(x, lambda r: b.force(c, r)), abs=1e-12)
        rows = design_rows(x, BOX, b)
        for p in range(b.k):  # the pair forces cancel, so every column sums to zero over sites
            assert abs(sum(rows[2 * i][p] for i in range(len(x)))) < 1e-12
            assert abs(sum(rows[2 * i + 1][p] for i in range(len(x)))) < 1e-12


def test_force_in_the_basis_is_recovered_exactly():
    b = HatBasis(R0, RC, 11)
    c_star = [smooth_force(r) for r in b.nodes]
    xs = configs(3, 5)
    fs = [cg_forces(x, BOX, b, c_star) for x in xs]
    c = force_matching(xs, fs, BOX, b)
    assert max(abs(p - q) for p, q in zip(c, c_star)) < 1e-10


def test_solution_is_the_least_squares_minimizer():
    b = HatBasis(R0, RC, 8)
    xs = configs(6, 4)
    fs = [pair_forces(x, smooth_force) for x in xs]
    c = force_matching(xs, fs, BOX, b)
    grad = [0.0] * b.k
    for x, f_ref in zip(xs, fs):
        for a, f in zip(design_rows(x, BOX, b), f_ref):
            res = sum(ap * cp for ap, cp in zip(a, c)) - f
            for p in range(b.k):
                grad[p] += 2.0 * a[p] * res
    assert max(abs(g) for g in grad) < 1e-8
    best = chi2(xs, fs, BOX, b, c)
    rng = random.Random(8)
    for _ in range(10):
        d = [rng.uniform(-0.01, 0.01) for _ in range(b.k)]
        assert chi2(xs, fs, BOX, b, [p + q for p, q in zip(c, d)]) > best


def test_second_order_convergence_on_a_smooth_force():
    xs = configs(1, 20)
    fs = [pair_forces(x, smooth_force) for x in xs]
    errors = []
    for k in (6, 11, 21, 41):
        b = HatBasis(R0, RC, k)
        c = force_matching(xs, fs, BOX, b)
        errors.append(max(abs(c[m] - smooth_force(b.nodes[m])) for m in range(k)))
    ratios = [errors[i] / errors[i + 1] for i in range(3)]
    assert all(q > 3.0 for q in ratios)
    assert errors[-1] < 0.01


def test_zero_mean_noise_averages_out():
    b = HatBasis(R0, RC, 11)
    c_star = [smooth_force(r) for r in b.nodes]
    rng = random.Random(7)
    err = []
    for count in (5, 80):
        xs = configs(2, count)
        fs = [[f + rng.gauss(0.0, 1.0) for f in cg_forces(x, BOX, b, c_star)] for x in xs]
        c = force_matching(xs, fs, BOX, b)
        err.append(math.sqrt(sum((p - q) ** 2 for p, q in zip(c, c_star))))
    assert err[1] < 0.5 * err[0]
    assert err[1] < 0.3


def test_unused_basis_function_gets_zero():
    b = HatBasis(0.1, RC, 25)  # no pair is closer than 0.85, so the first hats are never touched
    xs = configs(9, 3)
    fs = [pair_forces(x, smooth_force) for x in xs]
    c = force_matching(xs, fs, BOX, b)
    assert c[0] == 0.0 and c[1] == 0.0
    with pytest.raises(ValueError):
        HatBasis(2.0, 1.0, 5)
