# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/density-filtering/. The authors are listed in prov/FZQT96.jsonl.

import math
import random

from density_filtering import build, direct_matrix, filtered_descent, matvec, matvec_transpose

CASES = [(6, 4, 1.5), (7, 5, 2.5), (5, 5, 3.2), (9, 3, 2.0), (4, 6, 1.0)]


def test_sparse_filter_equals_the_direct_weighted_sum() -> None:
    rng = random.Random(1)
    for nx, ny, r in CASES:
        flt = build(nx, ny, r)
        w, d = direct_matrix(nx, ny, r)
        assert max(abs(a - b) for a, b in zip(flt.d, d)) < 1e-12
        for _ in range(5):
            x = [rng.random() for _ in range(nx * ny)]
            assert max(abs(a - b) for a, b in zip(flt.apply(x), matvec(w, x))) < 1e-12
            assert max(abs(a - b) for a, b in zip(flt.transpose(x), matvec_transpose(w, x))) < 1e-12


def test_rows_are_convex_weights_so_the_box_is_kept() -> None:
    rng = random.Random(2)
    for nx, ny, r in CASES:
        w, _ = direct_matrix(nx, ny, r)
        assert all(v >= 0 for row in w for v in row)
        assert all(abs(sum(row) - 1) < 1e-12 for row in w)
        flt = build(nx, ny, r)
        for _ in range(20):
            x = [rng.choice([0.0, 1.0, rng.random()]) for _ in range(nx * ny)]
            xt = flt.apply(x)
            assert min(x) - 1e-12 <= min(xt) and max(xt) <= max(x) + 1e-12


def test_radius_at_most_one_is_the_identity() -> None:
    flt = build(5, 4, 1.0)
    x = [i / 19 for i in range(20)]
    assert flt.apply(x) == x


def test_filter_is_self_adjoint_in_the_d_weighted_inner_product() -> None:
    rng = random.Random(3)
    for nx, ny, r in CASES:
        flt = build(nx, ny, r)
        x = [rng.uniform(-1, 1) for _ in range(nx * ny)]
        y = [rng.uniform(-1, 1) for _ in range(nx * ny)]
        wx, wy = flt.apply(x), flt.apply(y)
        left = sum(d * a * b for d, a, b in zip(flt.d, wx, y))
        right = sum(d * a * b for d, a, b in zip(flt.d, x, wy))
        assert abs(left - right) < 1e-12
        # and in the plain inner product the adjoint is the transpose, not the filter itself
        assert abs(sum(a * b for a, b in zip(wx, y)) - sum(a * b for a, b in zip(x, flt.transpose(y)))) < 1e-12


def test_chain_rule_against_central_differences() -> None:
    rng = random.Random(4)
    nx, ny, r = 8, 5, 2.2
    flt = build(nx, ny, r)
    n = nx * ny
    wts = [rng.uniform(0.5, 2) for _ in range(n)]

    def phi(xt):
        return sum(w * v**3 for w, v in zip(wts, xt))

    x = [rng.uniform(0.2, 0.8) for _ in range(n)]
    xt = flt.apply(x)
    gt = [3 * w * v * v for w, v in zip(wts, xt)]
    right = flt.transpose(gt)
    wrong = flt.apply(gt)  # filtering the gradient with the filter itself
    h = 1e-6
    worst_wrong = 0.0
    for f in range(n):
        xp, xm = list(x), list(x)
        xp[f] += h
        xm[f] -= h
        fd = (phi(flt.apply(xp)) - phi(flt.apply(xm))) / (2 * h)
        assert abs(right[f] - fd) < 1e-7
        worst_wrong = max(worst_wrong, abs(wrong[f] - fd) / abs(fd))
    assert worst_wrong > 0.05  # measured: the wrong rule is off by more than 5% near the boundary


def test_checkerboard_is_damped_by_the_closed_form_factor() -> None:
    nx, ny, r = 12, 12, 1.5
    flt = build(nx, ny, r)
    x = [(-1.0) ** (i + j) for i in range(nx) for j in range(ny)]
    xt = flt.apply(x)
    diag = r - math.sqrt(2)
    factor = (r - 4 * (r - 1) + 4 * diag) / (r + 4 * (r - 1) + 4 * diag)
    for i in range(2, nx - 2):
        for j in range(2, ny - 2):
            assert abs(xt[i * ny + j] - factor * x[i * ny + j]) < 1e-12
    assert abs(factor + 0.040814) < 1e-6


def test_volume_is_kept_inside_but_not_at_the_boundary() -> None:
    nx, ny, r = 10, 10, 1.5
    flt = build(nx, ny, r)
    n = nx * ny

    def column_sum(f):
        x = [0.0] * n
        x[f] = 1.0
        return sum(flt.apply(x))

    assert abs(column_sum(5 * ny + 5) - 1) < 1e-12  # interior: the mass is kept
    corner = column_sum(0)
    assert abs(corner - 0.9177) < 1e-4  # measured: the mass of a corner element shrinks by about 8%
    # the column sums are the chain rule applied to the volume sum(x~)
    assert abs(flt.transpose([1.0] * n)[0] - corner) < 1e-12


def test_filtered_descent_decreases_and_cannot_reach_a_checkerboard() -> None:
    nx, ny, r = 10, 8, 1.5
    flt = build(nx, ny, r)
    n = nx * ny
    target = [float((i + j) % 2) for i in range(nx) for j in range(ny)]

    def model(xt):
        return sum((a - b) ** 2 for a, b in zip(xt, target)), [2 * (a - b) for a, b in zip(xt, target)]

    def update(x, g):
        return [min(1.0, max(0.0, a - 0.25 * b)) for a, b in zip(x, g)]

    xt, hist = filtered_descent(flt, [0.5] * n, model, update, maxit=200)
    assert all(b <= a + 1e-12 for a, b in zip(hist, hist[1:]))
    inner = [xt[i * ny + j] for i in range(2, nx - 2) for j in range(2, ny - 2)]
    assert max(inner) - min(inner) < 0.2  # the filtered field stays nearly flat inside
