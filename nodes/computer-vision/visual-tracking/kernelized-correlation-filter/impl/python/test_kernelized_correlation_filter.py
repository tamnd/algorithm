# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kernelized-correlation-filter/. The authors are listed in prov/D8MKGV.jsonl.

import math
import random

from cvla import solve
from kernelized_correlation_filter import (
    KCF,
    detect,
    fft2,
    gaussian_labels,
    kernel,
    shift,
    train,
)

R, C = 4, 8
SHIFTS = [(du, dv) for dv in range(R) for du in range(C)]


def rand_patch(rng):
    return [[rng.uniform(-1, 1) for _ in range(C)] for _ in range(R)]


def kappa(a, b, sigma):
    p = R * C
    if sigma is None:
        return sum(s * t for ra, rb in zip(a, b) for s, t in zip(ra, rb)) / p
    return math.exp(-sum((s - t) ** 2 for ra, rb in zip(a, b) for s, t in zip(ra, rb)) / (sigma * sigma * p))


def test_shifts_and_labels():
    rng = random.Random(1)
    x = rand_patch(rng)
    assert shift(shift(x, (3, 1)), (-3, -1)) == x
    assert shift(shift(x, (2, 3)), (5, 2)) == shift(x, (7, 5))
    y = gaussian_labels(R, C, 1.0)
    assert y[0][0] == 1.0
    for v in range(R):
        for u in range(C):
            assert y[v][u] == y[(-v) % R][(-u) % C]


def test_kernel_by_fft_matches_the_definition():
    rng = random.Random(2)
    x, z = rand_patch(rng), rand_patch(rng)
    for sigma in [None, 0.5, 2.0]:
        k = kernel(z, x, sigma)
        for du, dv in SHIFTS:
            assert abs(k[dv][du] - kappa(z, shift(x, (du, dv)), sigma)) < 1e-12


def brute_force(x, y, z, lam, sigma):
    """Kernel ridge regression on all P shifts, solved as a P x P system."""
    xs = [shift(x, d) for d in SHIFTS]
    gram = [[kappa(a, b, sigma) + (lam if i == j else 0.0) for j, b in enumerate(xs)]
            for i, a in enumerate(xs)]
    alpha = solve(gram, [y[dv][du] for du, dv in SHIFTS])
    resp = []
    for du, dv in SHIFTS:
        zd = shift(z, (-du, -dv))
        resp.append(sum(a * kappa(zd, b, sigma) for a, b in zip(alpha, xs)))
    return alpha, resp


def test_dual_coefficients_and_response_match_brute_force():
    rng = random.Random(3)
    y = gaussian_labels(R, C, 1.0)
    for sigma in [None, 0.7]:
        x, z = rand_patch(rng), rand_patch(rng)
        alpha_f = train(x, y, 0.1, sigma)
        alpha = fft2(alpha_f, inverse=True)
        resp = detect(alpha_f, x, z, sigma)
        want_alpha, want_resp = brute_force(x, y, z, 0.1, sigma)
        for i, (du, dv) in enumerate(SHIFTS):
            assert abs(alpha[dv][du] - want_alpha[i]) < 1e-9
            assert abs(resp[dv][du] - want_resp[i]) < 1e-9


def test_linear_kernel_equals_primal_ridge_regression():
    rng = random.Random(4)
    x, z = rand_patch(rng), rand_patch(rng)
    y = gaussian_labels(R, C, 1.0)
    lam, p = 0.1, R * C
    rows = [[t / math.sqrt(p) for row in shift(x, d) for t in row] for d in SHIFTS]
    labels = [y[dv][du] for du, dv in SHIFTS]
    gram = [[sum(r[i] * r[j] for r in rows) + (lam if i == j else 0.0) for j in range(p)] for i in range(p)]
    rhs = [sum(r[i] * t for r, t in zip(rows, labels)) for i in range(p)]
    w = solve(gram, rhs)
    resp = detect(train(x, y, lam), x, z)
    for du, dv in SHIFTS:
        feat = [t / math.sqrt(p) for row in shift(z, (-du, -dv)) for t in row]
        assert abs(sum(a * b for a, b in zip(w, feat)) - resp[dv][du]) < 1e-9


def test_a_position_weighted_kernel_is_not_circulant():
    rng = random.Random(5)
    x = rand_patch(rng)
    weight = [[1.0 + u + v for u in range(C)] for v in range(R)]

    def weighted(a, b):
        return sum(weight[v][u] * a[v][u] * b[v][u] for v in range(R) for u in range(C))

    xs = [shift(x, d) for d in SHIFTS]
    # with a permutation-invariant kernel K[i][j] depends only on the shift between i and j
    assert abs(kappa(xs[0], xs[1], 0.7) - kappa(xs[1], xs[2], 0.7)) < 1e-12
    assert abs(weighted(xs[0], xs[1]) - weighted(xs[1], xs[2])) > 1e-3


def texture(seed, k, lo, hi):
    rng = random.Random(seed)
    blobs = [(rng.uniform(lo, hi), rng.uniform(lo, hi), rng.uniform(1.5, 3), rng.uniform(40, 160))
             for _ in range(k)]

    def f(u, v):
        return 20 + sum(a * math.exp(-((u - x) ** 2 + (v - y) ** 2) / (2 * s * s)) for x, y, s, a in blobs)

    return f


def test_tracks_a_moving_target():
    n, half = 64, 6
    back = texture(1, 40, -5, n + 5)
    bg = [[back(u, v) for u in range(n)] for v in range(n)]
    target = texture(2, 8, -2, 2 * half + 2)

    def frame(c):
        img = [row[:] for row in bg]
        for v in range(n):
            for u in range(n):
                du, dv = u - c[0], v - c[1]
                if abs(du) <= half and abs(dv) <= half:
                    img[v][u] = target(du + half, dv + half)
        return img

    truth = [(20 + 2.4 * t, 22 + 1.7 * t) for t in range(10)]
    tracker = KCF(frame(truth[0]), truth[0])
    for c in truth[1:]:
        assert math.dist(tracker.update(frame(c)), c) < 1.5
