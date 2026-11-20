# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shrinkwrap/. The authors are listed in prov/J58G2A.jsonl.

import random

from imgkit import dft2
from shrinkwrap import (autocorrelation, distance, gaussian_kernel, hio_step, object_projection,
                        shrinkwrap, threshold_support, update_support)

N = 16
BLOB = [[0, 1, 2, 1, 0], [1, 3, 4, 2, 0], [2, 4, 5, 3, 1], [0, 2, 3, 2, 2], [0, 0, 1, 2, 3]]


def page_object():
    f = [[0.0] * N for _ in range(N)]
    for i in range(5):
        for j in range(5):
            f[3 + i][4 + j] = float(BLOB[i][j])
    return f


def amplitudes(f):
    return [[abs(v) for v in row] for row in dft2(f)]


def shifted(img, a, b):
    n1, n2 = len(img), len(img[0])
    return [[img[(i - a) % n1][(j - b) % n2] for j in range(n2)] for i in range(n1)]


def test_autocorrelation_is_the_direct_sum() -> None:
    rng = random.Random(1)
    f = [[complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(8)] for _ in range(8)]
    c = autocorrelation(amplitudes(f))
    for a in range(8):
        for b in range(8):
            direct = sum(f[(i + a) % 8][(j + b) % 8] * f[i][j].conjugate()
                         for i in range(8) for j in range(8))
            assert abs(c[a][b] - direct) < 1e-9


def test_autocorrelation_holds_a_shifted_support() -> None:
    # For f >= 0 and r0 in the support, c(t) >= f(r0) f(r0 + t) > 0 for every t in supp f - r0.
    f = page_object()
    c = autocorrelation(amplitudes(f))
    top = max(abs(v) for row in c for v in row)
    r0 = (3, 5)
    for i in range(N):
        for j in range(N):
            if f[i][j] > 0:
                assert c[(i - r0[0]) % N][(j - r0[1]) % N].real > 1e-9 * top


def test_gaussian_kernel() -> None:
    k = gaussian_kernel(16, 16, 1.5)
    assert abs(sum(sum(row) for row in k) - 1.0) < 1e-12
    assert k[0][0] == max(max(row) for row in k)
    for i in range(16):
        for j in range(16):
            assert abs(k[i][j] - k[(-i) % 16][(-j) % 16]) < 1e-15


def test_threshold_supports_are_nested() -> None:
    rng = random.Random(2)
    img = [[rng.random() for _ in range(N)] for _ in range(N)]
    low, high = threshold_support(img, 0.2), threshold_support(img, 0.6)
    assert all(lo or not hi for rl, rh in zip(low, high) for lo, hi in zip(rl, rh))
    assert sum(map(sum, high)) < sum(map(sum, low))


def test_update_keeps_the_support_under_the_lemma_condition() -> None:
    # If min f * k(0) >= thresh * max f on supp f (f >= 0), the update holds supp f.
    f = [[v + 2.0 if v > 0 else 0.0 for v in row] for row in page_object()]
    sigma, thresh = 0.5, 0.2
    k0 = gaussian_kernel(N, N, sigma)[0][0]
    vals = [v for row in f for v in row if v > 0]
    assert min(vals) * k0 >= thresh * max(vals)
    new = update_support(f, sigma, thresh)
    assert all(s or v == 0 for rs, rv in zip(new, f) for s, v in zip(rs, rv))


def test_true_object_is_a_fixed_point_of_the_hio_step() -> None:
    f = page_object()
    support = [[v > 0 for v in row] for row in f]
    g, gp = hio_step(f, amplitudes(f), support, 0.9)
    assert distance(g, f) < 1e-9
    assert distance(object_projection(gp, support), f) < 1e-9


def test_reconstruction_on_the_page_example() -> None:
    # Measurement, not a theorem. The support is not given; the answer is the object or its
    # twin up to a cyclic shift, and the final support holds the support of that copy.
    f = page_object()
    twin = [[f[(-i) % N][(-j) % N] for j in range(N)] for i in range(N)]
    rng = random.Random(3)
    g0 = [[rng.random() for _ in range(N)] for _ in range(N)]
    est, support, _ = shrinkwrap(amplitudes(f), g0, 300, sigma0=1.0, sigma_min=0.5)
    best = min((distance(est, shifted(ref, a, b)), ref, a, b)
               for ref in (f, twin) for a in range(N) for b in range(N))
    assert best[0] < 1e-4
    copy = shifted(best[1], best[2], best[3])
    assert all(s or v == 0 for rs, rv in zip(support, copy) for s, v in zip(rs, rv))
