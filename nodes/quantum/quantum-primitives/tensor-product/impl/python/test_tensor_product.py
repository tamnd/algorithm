# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tensor-product/. The authors are listed in prov/XDTSZS.jsonl.

import math
import random

import pytest

from qsim import apply_1q, basis_state, close, dagger, identity, is_unitary, matmul, matvec
from tensor_product import (
    factor_2q, general_state_parameters, is_product_2q, kron, kron_all, kron_vec, on_qubit, plus,
    product_defect, product_state_parameters, swap_matrix,
)

KET = [[1 + 0j, 0j], [0j, 1 + 0j]]
X = [[0j, 1 + 0j], [1 + 0j, 0j]]
Z = [[1 + 0j, 0j], [0j, -1 + 0j]]
H = [[complex(math.sqrt(0.5)), complex(math.sqrt(0.5))], [complex(math.sqrt(0.5)), complex(-math.sqrt(0.5))]]
I2 = identity(2)


def rand_matrix(rng: random.Random, r: int, c: int) -> list[list[complex]]:
    return [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(c)] for _ in range(r)]


def rand_vector(rng: random.Random, d: int) -> list[complex]:
    v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(d)]
    s = math.sqrt(sum(abs(a) ** 2 for a in v))
    return [a / s for a in v]


def test_index_rule() -> None:
    rng = random.Random(11)
    a, b = rand_matrix(rng, 2, 3), rand_matrix(rng, 3, 2)
    k = kron(a, b)
    assert len(k) == 6 and len(k[0]) == 6
    for i in range(2):
        for j in range(3):
            for p in range(3):
                for q in range(2):
                    assert k[i * 3 + p][j * 2 + q] == a[i][j] * b[p][q]


def test_basis_kets_follow_the_qubit_order() -> None:
    # |b_{n-1}> (x) ... (x) |b_0> = |x> with x = sum b_j 2^j.
    for n in range(1, 5):
        for x in range(1 << n):
            factors = [KET[(x >> j) & 1] for j in reversed(range(n))]
            assert kron_all(factors) == basis_state(n, x)
    assert kron_vec(KET[1], KET[0]) == basis_state(2, 2)  # |1>|0> = |10> = |2>


def test_mixed_product_and_adjoint() -> None:
    rng = random.Random(12)
    for _ in range(10):
        a, b, c, d = (rand_matrix(rng, 2, 2) for _ in range(4))
        assert close(matmul(kron(a, b), kron(c, d)), kron(matmul(a, c), matmul(b, d)))
        assert close(dagger(kron(a, b)), kron(dagger(a), dagger(b)))
        u, v = rand_vector(rng, 2), rand_vector(rng, 2)
        assert close(matvec(kron(a, b), kron_vec(u, v)), kron_vec(matvec(a, u), matvec(b, v)))
    assert is_unitary(kron(H, X)) and is_unitary(kron(Z, kron(H, X)))


def test_on_qubit_matches_the_simulator() -> None:
    rng = random.Random(13)
    for n in range(1, 5):
        for j in range(n):
            u = rand_matrix(rng, 2, 2)
            s = rand_vector(rng, 1 << n)
            assert close(matvec(on_qubit(n, u, j), s), apply_1q(s, u, j))
    # U (x) V applies V to qubit 0 and U to qubit 1.
    assert close(kron(H, X), matmul(on_qubit(2, H, 1), on_qubit(2, X, 0)))


def test_not_commutative_and_swap() -> None:
    assert kron(X, I2) != kron(I2, X)
    s = swap_matrix()
    assert is_unitary(s) and close(matmul(s, s), identity(4))
    rng = random.Random(14)
    for _ in range(10):
        a, b = rand_matrix(rng, 2, 2), rand_matrix(rng, 2, 2)
        assert close(matmul(matmul(s, kron(a, b)), s), kron(b, a))
        u, v = rand_vector(rng, 2), rand_vector(rng, 2)
        assert close(matvec(s, kron_vec(u, v)), kron_vec(v, u))


def test_products_and_entangled_states() -> None:
    rng = random.Random(15)
    for _ in range(50):
        u, v = rand_vector(rng, 2), rand_vector(rng, 2)
        s = kron_vec(u, v)
        assert is_product_2q(s)
        fu, fv = factor_2q(s)
        assert close(kron_vec(fu, fv), s)
    bell = [complex(math.sqrt(0.5)), 0j, 0j, complex(math.sqrt(0.5))]
    assert abs(product_defect(bell) - 0.5) < 1e-12
    with pytest.raises(ValueError):
        factor_2q(bell)
    # |+>|+> is a product state even though all four amplitudes are nonzero.
    assert is_product_2q(kron_vec(plus(), plus()))
    # a random two-qubit state is entangled
    assert all(not is_product_2q(rand_vector(rng, 4)) for _ in range(50))


def test_parameter_counts() -> None:
    assert [product_state_parameters(n) for n in (1, 2, 3, 10)] == [2, 4, 6, 20]
    assert [general_state_parameters(n) for n in (1, 2, 3, 10)] == [2, 6, 14, 2046]
