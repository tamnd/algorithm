# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spectral-initialization/. The authors are listed in prov/5K2MNA.jsonl.

import cmath
import random

from imgla import sym_eig
from spectral_initialization import (apply_y, dist, gaussian_design, inner, kept_terms, measure, norm,
                                     spectral_init, spectral_matrix)


def unit_signal(rng, n, complex_valued=True):
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) if complex_valued else rng.gauss(0, 1) for _ in range(n)]
    s = norm(x)
    return [v / s for v in x]


def test_y_is_hermitian_and_positive_semidefinite() -> None:
    rng = random.Random(1)
    a = gaussian_design(rng, 40, 5)
    y = measure(a, unit_signal(rng, 5))
    mat = spectral_matrix(a, y)
    for i in range(5):
        for j in range(5):
            assert abs(mat[i][j] - mat[j][i].conjugate()) < 1e-12
    for _ in range(10):
        v = unit_signal(rng, 5)
        assert inner(v, apply_y(a, y, v)).real >= -1e-12


def test_power_iteration_finds_the_top_eigenvector() -> None:
    # Compare with the Jacobi method on the real form [[B, -C], [C, B]] of Y = B + iC.
    rng = random.Random(2)
    n = 6
    a = gaussian_design(rng, 60, n)
    y = measure(a, unit_signal(rng, n))
    mat = spectral_matrix(a, y)
    real_form = [[mat[i][j].real for j in range(n)] + [-mat[i][j].imag for j in range(n)] for i in range(n)]
    real_form += [[mat[i][j].imag for j in range(n)] + [mat[i][j].real for j in range(n)] for i in range(n)]
    w, q = sym_eig(real_form)
    top = [complex(q[i][-1], q[i + n][-1]) for i in range(n)]
    z, eig = spectral_init(a, y, iters=300, seed=3)
    assert abs(eig - w[-1]) < 1e-9 * w[-1]
    v = [c / norm(z) for c in z]
    assert abs(abs(inner(top, v)) - 1.0) < 1e-8


def test_scale_lambda() -> None:
    rng = random.Random(4)
    a = gaussian_design(rng, 30, 4)
    y = measure(a, unit_signal(rng, 4))
    z, _ = spectral_init(a, y, iters=20)
    lam2 = 4 * sum(y) / sum(norm(r) ** 2 for r in a)
    assert abs(norm(z) ** 2 - lam2) < 1e-12


def test_expected_matrix_complex_and_real() -> None:
    # Monte Carlo: E[Y] = I + x x^H for complex Gaussian a and ||x|| = 1, and I + 2 x x^T for real a.
    for complex_valued, factor in ((True, 1.0), (False, 2.0)):
        rng = random.Random(5)
        n = 3
        x = unit_signal(rng, n, complex_valued)
        a = gaussian_design(rng, 20000, n, complex_valued)
        mat = spectral_matrix(a, measure(a, x))
        for i in range(n):
            for j in range(n):
                want = (1.0 if i == j else 0.0) + factor * x[i] * complex(x[j]).conjugate()
                assert abs(mat[i][j] - want) < 0.1


def test_global_phase_does_not_matter() -> None:
    rng = random.Random(6)
    x = unit_signal(rng, 5)
    a = gaussian_design(rng, 50, 5)
    y = measure(a, x)
    y2 = measure(a, [cmath.exp(0.7j) * v for v in x])
    assert max(abs(u - v) for u, v in zip(y, y2)) < 1e-12
    z, _ = spectral_init(a, y)
    assert abs(dist(z, x) - dist(z, [cmath.exp(0.7j) * v for v in x])) < 1e-12


def test_truncation_keeps_the_small_terms() -> None:
    y = [1.0, 2.0, 30.0, 0.5]  # mean 8.375; the cut for alpha_y = 1.5 is 2.25 * 8.375
    assert kept_terms(y, 1.5) == [0, 1, 3]
    assert kept_terms(y) == [0, 1, 2, 3]


def test_accuracy_measurement() -> None:
    # Measurement, not a theorem: n = 8, m = 32 n, five seeds, complex Gaussian design.
    n, m = 8, 256
    for seed in range(1, 6):
        rng = random.Random(seed)
        x = unit_signal(rng, n)
        a = gaussian_design(rng, m, n)
        z, _ = spectral_init(a, measure(a, x), 100, seed)
        assert dist(z, x) < 0.5
