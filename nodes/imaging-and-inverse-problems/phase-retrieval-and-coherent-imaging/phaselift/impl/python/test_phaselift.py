# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/phaselift/. The authors are listed in prov/K3F300.jsonl.

import random

from phaselift import (apply_a, apply_a_adjoint, dist, extract, frob_inner, frob_norm, gaussian_design,
                       hermitian_eig, lift, measure, norm, objective, op_norm_sq, phaselift, psd_project,
                       random_hermitian, real_rows, trace)


def unit_signal(rng, n):
    x = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
    s = norm(x)
    return [v / s for v in x]


def sub(p, q):
    return [[u - v for u, v in zip(rp, rq)] for rp, rq in zip(p, q)]


def matmul(p, q):
    return [[sum(p[i][k] * q[k][j] for k in range(len(q))) for j in range(len(q[0]))] for i in range(len(p))]


def test_lifted_data_are_linear() -> None:
    rng = random.Random(1)
    x = unit_signal(rng, 4)
    a = gaussian_design(rng, 10, 4)
    assert max(abs(u - v) for u, v in zip(apply_a(a, lift(x)), measure(a, x))) < 1e-12


def test_adjoint() -> None:
    rng = random.Random(2)
    a = gaussian_design(rng, 9, 4)
    for _ in range(3):
        mat = random_hermitian(rng, 4)
        v = [rng.gauss(0, 1) for _ in range(9)]
        left = sum(u * w for u, w in zip(apply_a(a, mat), v))
        right = frob_inner(mat, apply_a_adjoint(a, v))
        assert abs(left - right) < 1e-10 * max(1.0, abs(left))


def test_hermitian_eig_reconstructs() -> None:
    rng = random.Random(3)
    mat = random_hermitian(rng, 4)
    w, v = hermitian_eig(mat)
    back = [[sum(w[k] * v[k][i] * v[k][j].conjugate() for k in range(4)) for j in range(4)] for i in range(4)]
    assert frob_norm(sub(back, mat)) < 1e-10
    assert all(u <= t for u, t in zip(w, w[1:]))


def test_psd_projection_is_the_nearest_point() -> None:
    rng = random.Random(4)
    for _ in range(3):
        mat = random_hermitian(rng, 4)
        proj = psd_project(mat)
        w, _ = hermitian_eig(proj)
        assert w[0] > -1e-10
        for i in range(4):
            for j in range(4):
                assert abs(proj[i][j] - proj[j][i].conjugate()) < 1e-12
        # The parts X+ and X+ - X are orthogonal: X+ (X+ - X) = 0.
        assert frob_norm(matmul(proj, sub(proj, mat))) < 1e-10
        # Variational inequality <X - X+, Y - X+> <= 0 for every PSD Y.
        for _ in range(5):
            g = random_hermitian(rng, 4)
            psd = matmul(g, g)
            assert frob_inner(sub(mat, proj), sub(psd, proj)) < 1e-10
        # A PSD matrix is its own projection.
        assert frob_norm(sub(psd_project(proj), proj)) < 1e-10


def test_operator_norm() -> None:
    rng = random.Random(5)
    a = gaussian_design(rng, 12, 3)
    big_l = op_norm_sq(a)
    fourth = sum(norm(r) ** 4 for r in a)
    assert fourth / 3 <= big_l * (1 + 1e-12) and big_l <= fourth * (1 + 1e-12)
    rows = real_rows(a)
    mat = random_hermitian(rng, 3)
    coords = [mat[i][i].real for i in range(3)]
    for i in range(3):
        for j in range(i + 1, 3):
            coords += [2 ** 0.5 * mat[i][j].real, 2 ** 0.5 * mat[i][j].imag]
    direct = apply_a(a, mat)
    via_rows = [sum(u * v for u, v in zip(row, coords)) for row in rows]
    assert max(abs(u - v) for u, v in zip(direct, via_rows)) < 1e-10
    assert sum(t * t for t in direct) <= big_l * frob_norm(mat) ** 2 * (1 + 1e-9)


def test_hand_example_two_by_two() -> None:
    # x = (1, 1 + i), vectors e1, e2, e1 + e2, e1 + i e2: A is one to one on 2 x 2 Hermitian matrices.
    a = [[1, 0], [0, 1], [1, 1], [1, 1j]]
    a = [[complex(v) for v in row] for row in a]
    x = [1 + 0j, 1 + 1j]
    y = measure(a, x)
    assert max(abs(u - v) for u, v in zip(y, [1.0, 2.0, 5.0, 5.0])) < 1e-12
    rec = []
    mat = phaselift(a, y, 1000, record=rec)
    want = [[1, 1 - 1j], [1 + 1j, 2]]
    assert frob_norm(sub(mat, want)) < 1e-9
    w, _ = hermitian_eig(mat)
    assert abs(w[-1] - 3.0) < 1e-9 and abs(w[0]) < 1e-9
    assert dist(extract(mat), x) < 1e-9


def test_monotone_and_rate_bound() -> None:
    # F(X_k) - F* <= L ||X_0 - X*||^2 / (2 k), with X* = x x^H, F* = 0 and X_0 = 0.
    rng = random.Random(6)
    n = 3
    x = unit_signal(rng, n)
    a = gaussian_design(rng, 18, n)
    y = measure(a, x)
    big_l = op_norm_sq(a) * (1.0 + 1e-9)
    rec = []
    phaselift(a, y, 60, record=rec)
    values = [objective(a, y, mat) for mat in rec]
    assert all(v <= u + 1e-12 for u, v in zip(values, values[1:]))
    for k in range(1, len(values)):
        assert values[k] <= big_l * 1.0 / (2 * k) + 1e-12


def test_trace_penalty_is_monotone() -> None:
    rng = random.Random(7)
    n = 3
    x = unit_signal(rng, n)
    a = gaussian_design(rng, 18, n)
    y = measure(a, x)
    rec = []
    phaselift(a, y, 40, lam=0.5, record=rec)
    values = [objective(a, y, mat, 0.5) for mat in rec]
    assert all(v <= u + 1e-12 for u, v in zip(values, values[1:]))
    assert trace(rec[-1]) < 1.0


def test_recovery_measurement() -> None:
    # Measurement, not a theorem: n = 3, m = 8 n, complex Gaussian design, 300 steps.
    for seed in range(1, 4):
        rng = random.Random(seed)
        x = unit_signal(rng, 3)
        a = gaussian_design(rng, 24, 3)
        mat = phaselift(a, measure(a, x), 300)
        assert dist(extract(mat), x) < 5e-3
