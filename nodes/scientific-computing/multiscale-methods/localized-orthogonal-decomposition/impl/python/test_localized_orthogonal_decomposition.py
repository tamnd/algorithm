# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/localized-orthogonal-decomposition/. The authors are listed in prov/DNA9DW.jsonl.
import math
import random

from localized_orthogonal_decomposition import (
    coarse_hat,
    correctors,
    energy,
    fine_solve,
    interpolation_rows,
    lod_1d,
    p1_solve,
)

N = 64


def rough(seed):
    rng = random.Random(seed)
    return [rng.choice([0.1, 1.0, 10.0]) * rng.uniform(0.5, 1.5) for _ in range(N)]


def source():
    return [1.0 + math.sin(3 * j / N) for j in range(N + 1)]


def enorm(a, u, v):
    d = [x - y for x, y in zip(u, v)]
    return energy(a, d, d) ** 0.5


def apply_rows(rows, v):
    return [sum(r[j] * v[j] for j in range(N + 1)) for r in rows]


def test_quasi_interpolation_is_a_projection_onto_the_coarse_space():
    for M in (4, 8):
        rows = interpolation_rows(N, M)
        for i in range(1, M):
            vals = apply_rows(rows, coarse_hat(N, M, i))
            for m, v in enumerate(vals):
                assert abs(v - (1.0 if m == i - 1 else 0.0)) < 1e-13


def test_correctors_lie_in_the_kernel_and_the_ideal_basis_is_orthogonal_to_it():
    a, M = rough(1), 8
    rows = interpolation_rows(N, M)
    for v in correctors(a, M, 2).values():
        assert max(abs(x) for x in apply_rows(rows, v)) < 1e-11
    _, _, basis = lod_1d(a, source(), M, None)
    rng = random.Random(4)
    for _ in range(3):
        v = [0.0] + [rng.uniform(-1, 1) for _ in range(N - 1)] + [0.0]
        coef = apply_rows(rows, v)
        w = list(v)
        for i in range(1, M):
            hat = coarse_hat(N, M, i)
            w = [x - coef[i - 1] * y for x, y in zip(w, hat)]
        assert max(abs(x) for x in apply_rows(rows, w)) < 1e-12
        scale = energy(a, w, w) ** 0.5
        for phi in basis:
            assert abs(energy(a, phi, w)) < 1e-9 * scale * energy(a, phi, phi) ** 0.5


def test_ideal_method_converges_at_least_linearly_and_beats_p1():
    a, f = rough(1), source()
    ref = fine_solve(a, f)
    errors = []
    for M in (4, 8, 16):
        _, u, _ = lod_1d(a, f, M, None)
        err = enorm(a, u, ref)
        assert err < 0.2 * enorm(a, p1_solve(a, f, M), ref)
        errors.append(err)
    for e1, e2 in zip(errors, errors[1:]):
        assert e1 / e2 > 1.8


def test_localization_error_decays_exponentially_in_the_layers():
    a, f = rough(1), source()
    for M in (8, 16):
        _, ideal, _ = lod_1d(a, f, M, None)
        diffs = [enorm(a, lod_1d(a, f, M, k)[1], ideal) for k in (1, 2, 3, 4)]
        for d1, d2 in zip(diffs, diffs[1:]):
            assert d1 / d2 > 3
        _, whole, _ = lod_1d(a, f, M, M)
        assert enorm(a, whole, ideal) < 1e-12


def test_two_layers_already_give_most_of_the_ideal_accuracy():
    a, f = rough(2), source()
    ref = fine_solve(a, f)
    M = 8
    _, ideal, _ = lod_1d(a, f, M, None)
    _, local, _ = lod_1d(a, f, M, 2)
    assert enorm(a, local, ref) < 2 * enorm(a, ideal, ref)
