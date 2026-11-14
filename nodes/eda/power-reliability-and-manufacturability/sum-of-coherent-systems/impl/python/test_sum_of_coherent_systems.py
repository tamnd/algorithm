# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sum-of-coherent-systems/. The authors are listed in prov/5NQR8Z.jsonl.

import cmath
import math
import random

from sum_of_coherent_systems import (
    abbe_image,
    band,
    hopkins_image,
    ideal_pupil,
    jacobi_hermitian,
    mask_spectrum,
    socs_image,
    socs_kernels,
    source_points,
    sum_of_coherent_systems,
    tcc,
)

P = 4.0
SIGMA = 0.7
SOURCE = source_points(SIGMA, 9)
H = ideal_pupil(defocus=0.15, coma=0.05)
KS = band(P, SIGMA)
T = tcc(KS, P, SOURCE, H)
N = 48
XS = [P * i / N for i in range(N)]


def random_mask(rng):
    """A binary mask made of a few random openings on the sample grid."""
    m = [0.0] * N
    for _ in range(3):
        a = rng.randrange(N)
        for d in range(rng.randint(2, 10)):
            m[(a + d) % N] = 1.0
    return m


def test_tcc_is_hermitian_and_psd():
    n = len(T)
    for a in range(n):
        for b in range(n):
            assert abs(T[a][b] - T[b][a].conjugate()) < 1e-14
    assert any(abs(T[a][b].imag) > 1e-3 for a in range(n) for b in range(n))
    lams, _ = jacobi_hermitian(T)
    assert min(lams) > -1e-12


def test_jacobi_reconstructs_random_hermitian():
    rng = random.Random(1)
    n = 12
    A = [[0j] * n for _ in range(n)]
    for i in range(n):
        A[i][i] = complex(rng.uniform(-2, 2), 0)
        for j in range(i + 1, n):
            z = complex(rng.uniform(-1, 1), rng.uniform(-1, 1))
            A[i][j], A[j][i] = z, z.conjugate()
    lams, V = jacobi_hermitian(A)
    for i in range(n):
        for j in range(n):
            vv = sum(V[k][i].conjugate() * V[k][j] for k in range(n))
            assert abs(vv - (1 if i == j else 0)) < 1e-12
            rec = sum(V[i][k] * lams[k] * V[j][k].conjugate() for k in range(n))
            assert abs(rec - A[i][j]) < 1e-12
    # The trace and the Frobenius norm are invariants.
    assert abs(sum(lams) - sum(A[i][i].real for i in range(n))) < 1e-12
    frob = sum(abs(A[i][j]) ** 2 for i in range(n) for j in range(n))
    assert abs(sum(l * l for l in lams) - frob) < 1e-10


def test_full_socs_equals_direct_hopkins_and_abbe():
    rng = random.Random(2)
    kernels = socs_kernels(T, len(KS))
    for _ in range(3):
        mask = random_mask(rng)
        M = mask_spectrum(mask, KS)
        direct = hopkins_image(T, M, KS, XS, P)
        socs = socs_image(kernels, M, KS, XS, P)
        abbe = abbe_image(SOURCE, H, M, KS, XS, P)
        for a, b, c in zip(direct, socs, abbe):
            assert abs(a - b) < 1e-11
            assert abs(a - c) < 1e-11


def test_rank_at_most_number_of_source_points():
    kernels = socs_kernels(T, len(KS))
    lams = [lam for lam, _ in kernels]
    assert len(KS) > len(SOURCE)
    assert all(abs(l) < 1e-12 for l in lams[len(SOURCE):])
    assert lams == sorted(lams, reverse=True)


def test_truncation_error_against_tail_eigenvalues():
    rng = random.Random(3)
    kernels = socs_kernels(T, len(KS))
    lams = [lam for lam, _ in kernels]
    for _ in range(3):
        mask = random_mask(rng)
        M = mask_spectrum(mask, KS)
        energy = sum(abs(m) ** 2 for m in M)
        direct = hopkins_image(T, M, KS, XS, P)
        for K in range(0, len(SOURCE) + 1):
            approx = socs_image(kernels[:K], M, KS, XS, P)
            tail_max = lams[K] if K < len(lams) else 0.0
            for a, b in zip(direct, approx):
                err = a - b
                # 0 <= I - I_K <= lam_{K+1} * sum |M|^2 at every point.
                assert -1e-11 <= err <= max(tail_max, 0.0) * energy + 1e-11
    # Summed over the single-frequency masks e^{2 pi i k x / P}, the error at a point
    # is exactly the sum of the tail eigenvalues (the trace norm of T - T_K).
    for K in range(0, len(SOURCE) + 1):
        total = 0.0
        for idx, k in enumerate(KS):
            M = [1.0 if j == idx else 0.0 for j in range(len(KS))]
            x = 0.37
            total += hopkins_image(T, M, KS, [x], P)[0] - socs_image(kernels[:K], M, KS, [x], P)[0]
        assert abs(total - sum(lams[K:])) < 1e-11


def test_error_decreases_with_k():
    rng = random.Random(4)
    kernels = socs_kernels(T, len(KS))
    mask = random_mask(rng)
    M = mask_spectrum(mask, KS)
    direct = hopkins_image(T, M, KS, XS, P)
    prev = None
    for K in range(0, len(SOURCE) + 1):
        approx = socs_image(kernels[:K], M, KS, XS, P)
        worst = max(a - b for a, b in zip(direct, approx))
        if prev is not None:
            assert worst <= prev + 1e-12
        prev = worst
    assert prev < 1e-11


def test_page_example():
    source = [(-0.5, 1 / 3), (0.0, 1 / 3), (0.5, 1 / 3)]
    Hi = ideal_pupil()
    ks = band(2.0, 0.5)
    assert ks == [-3, -2, -1, 0, 1, 2, 3]
    T2 = tcc(ks, 2.0, source, Hi)
    # The TCC entries are multiples of 1/3, as in the table on the page.
    third = [
        [1, 1, 1, 1, 1, 0, 0],
        [1, 2, 2, 2, 2, 1, 0],
        [1, 2, 3, 3, 3, 2, 1],
        [1, 2, 3, 3, 3, 2, 1],
        [1, 2, 3, 3, 3, 2, 1],
        [0, 1, 2, 2, 2, 2, 1],
        [0, 0, 1, 1, 1, 1, 1],
    ]
    for a in range(7):
        for b in range(7):
            assert abs(T2[a][b] - third[a][b] / 3) < 1e-12
    kernels = socs_kernels(T2, 7)
    lams = [lam for lam, _ in kernels]
    r = math.sqrt(137)
    for got, want in zip(lams, [(13 + r) / 6, 2 / 3, (13 - r) / 6, 0, 0, 0, 0]):
        assert abs(got - want) < 1e-12
    # The second kernel is (1, 1, 0, 0, 0, -1, -1) / 2 up to a phase.
    v2 = kernels[1][1]
    assert abs(abs(sum(x * y for x, y in zip(v2, [0.5, 0.5, 0, 0, 0, -0.5, -0.5]))) - 1) < 1e-12
    # Lines and spaces: m = 1 on [-1/2, 1/2] in each period 2, so M(k) = sin(pi k / 2) / (pi k).
    M = [0.5 if k == 0 else math.sin(math.pi * k / 2) / (math.pi * k) for k in ks]
    xs = [0.0, 0.5, 1.0]
    direct = hopkins_image(T2, M, ks, xs, 2.0)
    for got, want in zip(direct, [1.138611, 0.257505, 0.006842]):
        assert abs(got - want) < 1e-6
    i1 = socs_image(kernels[:1], M, ks, xs, 2.0)
    i2 = socs_image(kernels[:2], M, ks, xs, 2.0)
    i3 = socs_image(kernels[:3], M, ks, xs, 2.0)
    for got, want in zip(i1, [1.138562, 0.249594, 0.004603]):
        assert abs(got - want) < 1e-6
    for got, want in zip(i2, [1.138562, 0.257099, 0.004603]):
        assert abs(got - want) < 1e-6
    assert all(abs(a - b) < 1e-12 for a, b in zip(i3, direct))
    # The sampled mask through the whole pipeline agrees with the direct sum.
    mask = [1.0 if i < 4 or i >= 12 else 0.0 for i in range(16)]
    image, all_lams = sum_of_coherent_systems(mask, 2.0, source, Hi, 3, xs)
    sampled = hopkins_image(T2, mask_spectrum(mask, ks), ks, xs, 2.0)
    assert all(abs(a - b) < 1e-12 for a, b in zip(image, sampled))
    assert all(abs(l) < 1e-12 for l in all_lams[3:])
