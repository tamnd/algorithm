# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/iterative-back-projection-super-resolution/. The authors are listed in prov/KACAK6.jsonl.

import cmath
import math
import random
from fractions import Fraction as F

from iterative_back_projection_super_resolution import (
    back_project,
    covers_all_residues,
    forward,
    ibp,
    mirror,
    residual_norm2,
    shift_and_add,
)


def dft(x):
    n = len(x)
    return [sum(x[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def norm(v):
    if v and isinstance(v[0], list):
        v = [t for row in v for t in row]
    return math.sqrt(sum(abs(t) ** 2 for t in v))


def sub(a, b):
    if a and isinstance(a[0], list):
        return [[p - q for p, q in zip(ra, rb)] for ra, rb in zip(a, b)]
    return [p - q for p, q in zip(a, b)]


def psf(n, taps):
    h = [0] * n
    for d, v in taps.items():
        h[d % n] += v
    return h


def frames_of(x, shifts, h, factor):
    return [forward(x, s, h, factor) for s in shifts]


def test_back_projection_is_the_adjoint_for_the_mirrored_kernel():
    rng = random.Random(1)
    n, factor = 12, 3
    h = [rng.random() for _ in range(n)]
    for s in (0, 1, 5, 11):
        x = [rng.gauss(0, 1) for _ in range(n)]
        r = [rng.gauss(0, 1) for _ in range(n // factor)]
        ax = forward(x, s, h, factor)
        lhs = sum(a * b for a, b in zip(ax, r))
        rhs = sum(a * b for a, b in zip(x, back_project(r, s, mirror(h), factor)))
        assert abs(lhs - rhs) <= 1e-10 * norm(ax) * norm(r)
    h2 = [[rng.random() for _ in range(6)] for _ in range(6)]
    for s in ((0, 0), (1, 4), (5, 3)):
        x = [[rng.gauss(0, 1) for _ in range(6)] for _ in range(6)]
        r = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(3)]
        ax = forward(x, s, h2, 2)
        lhs = sum(a * b for ra, rb in zip(ax, r) for a, b in zip(ra, rb))
        bp = back_project(r, s, mirror(h2), 2)
        rhs = sum(a * b for ra, rb in zip(x, bp) for a, b in zip(ra, rb))
        assert abs(lhs - rhs) <= 1e-10 * norm(ax) * norm(r)


def test_equals_landweber_on_the_stacked_matrix_exactly():
    rng = random.Random(2)
    for _ in range(3):
        n, factor = 6, 2
        raw = [rng.randint(0, 3) for _ in range(n)]
        raw[0] += 2
        h = [F(v, sum(raw)) for v in raw]
        shifts = rng.sample(range(n), 3)
        rows = []
        for s in shifts:
            cols = [forward([F(int(i == j)) for i in range(n)], s, h, factor) for j in range(n)]
            rows.extend([cols[j][r] for j in range(n)] for r in range(n // factor))
        y = [F(rng.randint(-4, 4)) for _ in rows]
        frames = [y[k * (n // factor):(k + 1) * (n // factor)] for k in range(len(shifts))]
        beta = F(rng.randint(1, 3), 2)
        omega = beta / len(shifts)
        iters = rng.randint(1, 4)
        x = [F(0)] * n
        for _ in range(iters):
            res = [yi - sum(a * b for a, b in zip(row, x)) for yi, row in zip(y, rows)]
            x = [x[j] + omega * sum(rows[i][j] * res[i] for i in range(len(rows))) for j in range(n)]
        assert ibp(frames, shifts, h, factor, beta=beta, iters=iters) == x


def test_filter_factors_with_a_complete_set_of_shifts():
    # With every residue mod L once, A^T A = B^T B, so the iterate is a spectral
    # filter of z = sum_k W_k^T U y_k with factors 1 - (1 - omega |H_q|^2)^T.
    rng = random.Random(3)
    n, factor = 12, 3
    h = psf(n, {0: 0.5, 1: 0.2, -1: 0.2, 2: 0.05, -2: 0.05})
    shifts = [5, 1, 9]
    assert covers_all_residues(shifts, factor)
    y = [[rng.gauss(0, 1) for _ in range(n // factor)] for _ in shifts]
    beta, iters = 2.5, 7
    omega = beta / len(shifts)
    xq = dft(ibp(y, shifts, h, factor, beta=beta, iters=iters))
    zq = dft(shift_and_add(y, shifts, factor))
    hq = dft(h)
    for q in range(n):
        f = 1 - (1 - omega * abs(hq[q]) ** 2) ** iters
        expect = f * zq[q] / hq[q]
        assert abs(xq[q] - expect) <= 1e-9 * (1 + abs(expect))


def test_exact_data_converges_and_the_error_never_grows():
    n, factor = 16, 2
    h = psf(n, {0: F(2, 3), 1: F(1, 6), -1: F(1, 6)})
    hf = [float(v) for v in h]
    rng = random.Random(4)
    xt = [rng.choice([0.0, 0.0, 1.0, 4.0]) for _ in range(n)]
    shifts = [0, 1]
    y = frames_of(xt, shifts, hf, factor)
    errs = []
    ibp(y, shifts, hf, factor, beta=2.0, iters=220, callback=lambda t, x: errs.append(norm(sub(x, xt))))
    for a, b in zip(errs, errs[1:]):
        assert b <= a * (1 + 1e-12)
    assert errs[-1] < 1e-8 * norm(xt)


def test_delta_blur_and_a_complete_set_is_solved_in_one_step():
    rng = random.Random(5)
    n, factor = 9, 3
    delta = [F(1)] + [F(0)] * (n - 1)
    xt = [F(rng.randint(0, 9)) for _ in range(n)]
    shifts = [0, 4, 8]
    y = frames_of(xt, shifts, delta, factor)
    assert shift_and_add(y, shifts, factor) == xt
    assert ibp(y, shifts, delta, factor, beta=3, iters=1) == xt


def test_one_residue_twice_is_not_identifiable():
    n, factor = 8, 2
    delta = [F(1)] + [F(0)] * (n - 1)
    shifts = [0, 2]
    assert not covers_all_residues(shifts, factor)
    xt = [F(v) for v in (1, 2, 3, 4, 5, 6, 7, 8)]
    other = [v + (5 if j % 2 else 0) for j, v in enumerate(xt)]
    assert frames_of(xt, shifts, delta, factor) == frames_of(other, shifts, delta, factor)
    x = ibp(frames_of(xt, shifts, delta, factor), shifts, delta, factor, beta=1, iters=5)
    assert all(x[j] == 0 for j in range(1, n, 2))
    assert residual_norm2(x, frames_of(xt, shifts, delta, factor), shifts, delta, factor) == 0


def test_the_kernel_condition_decides_convergence():
    # Box of width 5 on 16 points: H_4 = -1/5. With a complete set of shifts and
    # beta = K the error at frequency q is multiplied by 1 - P_q H_q.
    n, factor = 16, 2
    h = psf(n, {d: 0.2 for d in range(-2, 3)})
    delta = [1.0] + [0.0] * (n - 1)
    shifts = [0, 1]
    xt = [math.cos(2 * math.pi * 4 * j / n) for j in range(n)]
    y = frames_of(xt, shifts, h, factor)
    e10 = norm(sub(ibp(y, shifts, h, factor, p=delta, beta=2.0, iters=10), xt))
    e20 = norm(sub(ibp(y, shifts, h, factor, p=delta, beta=2.0, iters=20), xt))
    assert abs(e20 / e10 - 1.2 ** 10) < 1e-6 * 1.2 ** 10
    errs = [norm(sub(ibp(y, shifts, h, factor, beta=2.0, iters=k), xt)) for k in (0, 5, 10, 30)]
    for a, b in zip(errs, errs[1:]):
        assert b <= a * (1 + 1e-12)
    assert errs[-1] < 0.5 * errs[0]


def test_two_dimensional_frames():
    n, factor = 8, 2
    w = {0: 0.8, 1: 0.1, n - 1: 0.1}
    h = [[w.get(i, 0.0) * w.get(j, 0.0) for j in range(n)] for i in range(n)]
    rng = random.Random(6)
    xt = [[rng.choice([0.0, 1.0, 2.0]) for _ in range(n)] for _ in range(n)]
    shifts = [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert covers_all_residues(shifts, factor)
    y = frames_of(xt, shifts, h, factor)
    x = ibp(y, shifts, h, factor, beta=4.0, iters=150)
    assert norm(sub(x, xt)) < 1e-7 * norm(xt)
    # Three of the four shifts leave a quarter of the HR pixels unseen.
    assert not covers_all_residues(shifts[:3], factor)
