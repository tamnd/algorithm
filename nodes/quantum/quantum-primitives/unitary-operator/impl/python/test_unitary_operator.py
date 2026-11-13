# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/unitary-operator/. The authors are listed in prov/M3YVJN.jsonl.

import cmath
import math
import random

import pytest

from qsim import close, dagger, identity, inner, is_unitary, matmul, matvec, scale
from unitary_operator import (
    X, Y, Z, det_2x2, eigenvalues_2x2, exp_i_hermitian_2x2, expm_taylor, from_zyz, inverse, random_unitary,
    rz, ry, zyz,
)

R = math.sqrt(0.5)
H = [[complex(R), complex(R)], [complex(R), complex(-R)]]
CNOT = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]


def rand_vec(rng: random.Random, d: int) -> list[complex]:
    return [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]


def test_standard_gates_are_unitary() -> None:
    for g in (X, Y, Z, H, rz(0.3), ry(1.1), [[1, 0], [0, 1j]], [[1, 0], [0, cmath.exp(1j * math.pi / 4)]]):
        assert is_unitary(g)
    assert is_unitary([[complex(x) for x in row] for row in CNOT])


def test_non_examples() -> None:
    assert not is_unitary([[1, 1], [0, 1]])  # invertible, but it does not keep lengths
    assert not is_unitary(scale(2, identity(2)))
    assert not is_unitary([[1, 0], [0, 0]])  # a projector: Hermitian, not unitary
    assert not is_unitary([[R, R], [0, 0]])  # one unit column is not enough
    with pytest.raises(ValueError):
        zyz([[1, 1], [0, 1]])


def test_eigenvalues_and_determinant_have_modulus_one() -> None:
    rng = random.Random(71)
    for _ in range(200):
        u = random_unitary(2, rng)
        assert is_unitary(u)
        l1, l2 = eigenvalues_2x2(u)
        assert abs(abs(l1) - 1) < 1e-9 and abs(abs(l2) - 1) < 1e-9
        assert abs(abs(det_2x2(u)) - 1) < 1e-9
        assert close(inverse(u), dagger(u)) and close(matmul(inverse(u), u), identity(2))
    assert eigenvalues_2x2(X) == (1, -1)


def test_inner_products_and_norms_are_kept() -> None:
    rng = random.Random(72)
    for d in (2, 4, 8):
        u = random_unitary(d, rng)
        assert is_unitary(u)
        for _ in range(10):
            phi, psi = rand_vec(rng, d), rand_vec(rng, d)
            assert abs(inner(matvec(u, phi), matvec(u, psi)) - inner(phi, psi)) < 1e-9
        v = random_unitary(d, rng)
        assert is_unitary(matmul(u, v)) and is_unitary(dagger(u))


def test_exponential_of_a_hermitian_matrix() -> None:
    rng = random.Random(73)
    for _ in range(30):
        a = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)] for _ in range(2)]
        h = [[(a[i][j] + a[j][i].conjugate()) / 2 for j in range(2)] for i in range(2)]
        u = exp_i_hermitian_2x2(h)
        assert is_unitary(u)
        assert close(u, expm_taylor(scale(1j, h), 40), 1e-9)
    # Rz(t) = exp(-i t Z / 2)
    assert close(rz(0.7), exp_i_hermitian_2x2(scale(-0.35, Z)))
    # exp(i pi X / 2) = i X
    assert close(exp_i_hermitian_2x2(scale(math.pi / 2, X)), scale(1j, X))


def test_zyz_decomposition() -> None:
    rng = random.Random(74)
    cases = [random_unitary(2, rng) for _ in range(100)] + [X, Y, Z, H, identity(2), [[1, 0], [0, 1j]]]
    for u in cases:
        alpha, beta, gamma, delta = zyz(u)
        assert close(from_zyz(alpha, beta, gamma, delta), u)
