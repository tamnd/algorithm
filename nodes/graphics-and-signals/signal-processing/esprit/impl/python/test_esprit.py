# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/esprit/. The authors are listed in prov/X5EKAZ.jsonl.

import cmath
import math
import random

import pytest

from esprit import (
    characteristic_polynomial,
    eigenvalues,
    esprit,
    hermitian_eigen,
    model_covariance,
    rotation_operator,
    sample_covariance,
    solve,
)


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def match_error(found, true):
    left = list(found)
    worst = 0.0
    for r in true:
        i = min(range(len(left)), key=lambda j: abs(left[j] - r))
        worst = max(worst, abs(left.pop(i) - r))
    return worst


def test_page_example_exact_covariance() -> None:
    R = model_covariance([0.5, 0.9], [1.0, 1.0], 0.1, 8)
    phi = rotation_operator(R, 2)
    lam = eigenvalues(phi)
    assert match_error(lam, [cmath.exp(0.5j), cmath.exp(0.9j)]) < 1e-10
    assert all(abs(abs(v) - 1) < 1e-10 for v in lam)
    w = esprit(R, 2)
    assert abs(w[0] - 0.5) < 1e-10 and abs(w[1] - 0.9) < 1e-10


def test_edges() -> None:
    with pytest.raises(ValueError):
        esprit(model_covariance([0.5], [1], 1, 3), 3)
    with pytest.raises(ValueError):
        sample_covariance([1, 2], 3)
    with pytest.raises(ValueError):
        solve([[1, 2], [2, 4]], [[1], [2]])
    # One tone, m = 2: Phi is the 1 x 1 ratio of the two entries of the signal eigenvector.
    w = esprit(model_covariance([-2.0], [3.0], 0.5, 2), 1)
    assert abs(w[0] + 2.0) < 1e-12


def test_small_eigenvalues_against_known_spectra() -> None:
    rng = random.Random(4901)
    for _ in range(500):
        n = rng.randint(1, 4)
        lam = [complex(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(n)]
        while True:
            V = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)] for _ in range(n)]
            try:
                Vinv = solve(V, [[complex(i == j) for j in range(n)] for i in range(n)])
                break
            except ValueError:
                continue
        A = matmul(matmul(V, [[lam[i] if i == j else 0 for j in range(n)] for i in range(n)]), Vinv)
        assert abs(characteristic_polynomial(A)[1] + sum(lam)) < 1e-8
        if min((abs(a - b) for i, a in enumerate(lam) for b in lam[i + 1:]), default=1) > 0.2:
            assert match_error(eigenvalues(A), lam) < 1e-6


def test_hermitian_eigen_residual() -> None:
    rng = random.Random(4902)
    for _ in range(200):
        m = rng.randint(1, 6)
        A = [[0j] * m for _ in range(m)]
        for i in range(m):
            A[i][i] = complex(rng.gauss(0, 1))
            for j in range(i + 1, m):
                v = complex(rng.gauss(0, 1), rng.gauss(0, 1))
                A[i][j], A[j][i] = v, v.conjugate()
        lam, V = hermitian_eigen(A)
        AV = matmul(A, V)
        assert all(abs(AV[i][j] - V[i][j] * lam[j]) < 1e-10 for i in range(m) for j in range(m))


def test_exact_covariances_random_frequencies() -> None:
    rng = random.Random(4903)
    for _ in range(200):
        m = rng.randint(3, 8)
        d = rng.randint(1, min(3, m - 1))
        while True:
            f = sorted(rng.uniform(-3.1, 3.1) for _ in range(d))
            if all(b - a > 0.2 for a, b in zip(f, f[1:])) and f[0] + 2 * math.pi - f[-1] > 0.2:
                break
        R = model_covariance(f, [rng.uniform(0.5, 2) for _ in range(d)], rng.uniform(0.01, 1), m)
        assert max(abs(a - b) for a, b in zip(esprit(R, d), f)) < 1e-7


def test_sample_covariance_of_noisy_tones() -> None:
    # The MUSIC page's data: tones at 0.5 and 0.9, noise variance 0.1, N = 200, m = 8,
    # seeds 4803 to 4852.
    errs = []
    for seed in range(4803, 4853):
        rng = random.Random(seed)
        ph = [rng.uniform(0, 2 * math.pi) for _ in range(2)]
        s = math.sqrt(0.05)
        x = [cmath.exp(1j * (0.5 * n + ph[0])) + cmath.exp(1j * (0.9 * n + ph[1])) + complex(rng.gauss(0, s), rng.gauss(0, s)) for n in range(200)]
        w = esprit(sample_covariance(x, 8), 2)
        errs.append(max(abs(w[0] - 0.5), abs(w[1] - 0.9)))
    assert sum(errs) / len(errs) < 0.01
    assert max(errs) < 0.05
