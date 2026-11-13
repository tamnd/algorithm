# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/music-algorithm/. The authors are listed in prov/PF6V7J.jsonl.

import cmath
import math
import random

import pytest

from music_algorithm import (
    diagonal_sums,
    hermitian_eigen,
    model_covariance,
    music,
    noise_projector,
    null_spectrum,
    pseudospectrum,
    sample_covariance,
    steering,
)


def random_hermitian(rng, m):
    A = [[0j] * m for _ in range(m)]
    for i in range(m):
        A[i][i] = complex(rng.gauss(0, 1))
        for j in range(i + 1, m):
            v = complex(rng.gauss(0, 1), rng.gauss(0, 1))
            A[i][j], A[j][i] = v, v.conjugate()
    return A


def test_eigen_solver_on_random_hermitian_matrices() -> None:
    rng = random.Random(4801)
    for _ in range(500):
        m = rng.randint(1, 6)
        A = random_hermitian(rng, m)
        lam, V = hermitian_eigen(A)
        assert lam == sorted(lam, reverse=True)
        for i in range(m):
            for j in range(m):
                # V^H V = I
                g = sum(V[k][i].conjugate() * V[k][j] for k in range(m))
                assert abs(g - (i == j)) < 1e-10
                # A V = V diag(lam)
                av = sum(A[i][k] * V[k][j] for k in range(m))
                assert abs(av - V[i][j] * lam[j]) < 1e-10
        assert abs(sum(lam) - sum(A[i][i].real for i in range(m))) < 1e-10


def test_eigen_solver_two_by_two_closed_form() -> None:
    a, d, b = 2.0, -1.0, complex(1, 2)
    lam, _ = hermitian_eigen([[a, b], [b.conjugate(), d]])
    root = math.sqrt(((a - d) / 2) ** 2 + abs(b) ** 2)
    assert abs(lam[0] - ((a + d) / 2 + root)) < 1e-12
    assert abs(lam[1] - ((a + d) / 2 - root)) < 1e-12


def test_page_example_exact_covariance() -> None:
    R = model_covariance([0.5, 0.9], [1.0, 1.0], 0.1, 8)
    lam, _ = hermitian_eigen(R)
    assert all(abs(v - 0.1) < 1e-10 for v in lam[2:])
    assert lam[1] > 1
    w = music(R, 2)
    assert abs(w[0] - 0.5) < 1e-6 and abs(w[1] - 0.9) < 1e-6
    P = noise_projector(R, 2)
    q = diagonal_sums(P)
    assert null_spectrum(q, 0.5) < 1e-12 and null_spectrum(q, 0.9) < 1e-12
    assert pseudospectrum(R, 2, 0.5) > 1e10
    # The O(m) evaluation equals the direct quadratic form a^H P a.
    for w in (-3.0, -1.0, 0.0, 0.7, 2.5):
        a = steering(w, 8)
        direct = sum(a[i].conjugate() * P[i][j] * a[j] for i in range(8) for j in range(8)).real
        assert abs(null_spectrum(q, w) - direct) < 1e-12
    # The null spectrum is the squared distance of a(w) from the signal subspace: at most m.
    assert all(-1e-12 <= null_spectrum(q, w) <= 8 + 1e-9 for w in (0.1 * k for k in range(-31, 32)))


def test_exact_covariances_random_frequencies() -> None:
    rng = random.Random(4802)
    for _ in range(60):
        m = rng.randint(4, 8)
        d = rng.randint(1, min(3, m // 2))
        while True:
            f = sorted(rng.uniform(-3.0, 3.0) for _ in range(d))
            gaps = [b - a for a, b in zip(f, f[1:])] + [f[0] + 2 * math.pi - f[-1]]
            if min(gaps) > 1.5 * 2 * math.pi / m:
                break
        R = model_covariance(f, [rng.uniform(0.5, 2) for _ in range(d)], rng.uniform(0.01, 1), m)
        w = music(R, d)
        assert max(abs(a - b) for a, b in zip(w, f)) < 1e-6


def test_edges() -> None:
    with pytest.raises(ValueError):
        music(model_covariance([0.5], [1], 1, 3), 3)
    with pytest.raises(ValueError):
        sample_covariance([1, 2], 3)
    assert hermitian_eigen([[3.0]]) == ([3.0], [[1]])
    R = sample_covariance([1, 1j, -1, -1j], 2)
    assert R == [[1, -1j], [1j, 1]]


def test_sample_covariance_of_noisy_tones() -> None:
    # Two unit tones at 0.5 and 0.9 rad/sample with random phases, complex noise of
    # variance 0.1, N = 200, m = 8; seeds 4803 to 4852.
    errs = []
    for seed in range(4803, 4853):
        rng = random.Random(seed)
        ph = [rng.uniform(0, 2 * math.pi) for _ in range(2)]
        s = math.sqrt(0.05)
        x = [cmath.exp(1j * (0.5 * n + ph[0])) + cmath.exp(1j * (0.9 * n + ph[1])) + complex(rng.gauss(0, s), rng.gauss(0, s)) for n in range(200)]
        w = music(sample_covariance(x, 8), 2)
        errs.append(max(abs(w[0] - 0.5), abs(w[1] - 0.9)))
    assert sum(errs) / len(errs) < 0.01
    assert max(errs) < 0.05


def test_steering() -> None:
    a = steering(math.pi / 2, 4)
    assert all(abs(u - v) < 1e-15 for u, v in zip(a, [1, 1j, -1, -1j]))
